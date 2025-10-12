import os
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Generator

import pytest
import requests
import uvicorn
from playwright.sync_api import sync_playwright

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

SERVER_HOST = "127.0.0.1"
SERVER_PORT = int(os.environ.get("KNOWLEDGE_TEST_PORT", "8765"))
if not (1024 <= SERVER_PORT <= 65535):
    raise ValueError(f"Invalid test port {SERVER_PORT}. Must be between 1024-65535")
BASE_URL = f"http://{SERVER_HOST}:{SERVER_PORT}"
@pytest.fixture(scope="session", autouse=True)
def install_playwright_browsers() -> None:
    """Ensure the Chromium browser is available for end-to-end tests."""
    cache_dir = Path.home() / ".cache/ms-playwright"
    chromium_dir = cache_dir / "chromium-1187"
    command = ["playwright", "install", "chromium"]
    if not chromium_dir.exists():
        command.append("--with-deps")
    subprocess.run(command, check=True)


@pytest.fixture(scope="session")
def app_server() -> Generator[str, None, None]:
    """Spin up the FastAPI app using uvicorn for browser tests."""
    config = uvicorn.Config("web_app:app", host=SERVER_HOST, port=SERVER_PORT, log_level="error")
    server = uvicorn.Server(config)

    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    deadline = time.time() + 30
    last_error: Exception | None = None
    while time.time() < deadline:
        try:
            response = requests.get(f"{BASE_URL}/api/health", timeout=1)
            if response.status_code == 200:
                break
        except Exception as exc:  # pragma: no cover - diagnostic only
            last_error = exc
            time.sleep(0.5)
    else:
        raise RuntimeError(f"Server did not start: {last_error}")

    yield BASE_URL

    server.should_exit = True
    thread.join(timeout=10)


def test_knowledge_workspace_end_to_end(app_server: str) -> None:
    article_title = "Example Article"
    youtube_title = "Research Update"
    text_title = "Massive Context"
    large_text = "x" * 200_000

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()

        page.goto(f"{app_server}/knowledge", wait_until="networkidle")
        page.wait_for_selector('[data-testid="knowledge-app-loaded"]', timeout=60_000)

        assert page.locator('[data-testid="writer-template-card"]').count() == 3
        assert page.locator('[data-testid="general-template-card"]').count() == 6

        page.fill('[data-testid="article-title-input"]', article_title)
        page.fill('[data-testid="article-url-input"]', "https://example.com/article")
        page.select_option('[data-testid="article-template-select"]', value="writer_character_profile")
        page.fill('#article-tags', 'story, protagonist')
        page.click('form[aria-label="article-import-form"] button[type="submit"]')
        page.wait_for_selector('text=Article imported successfully')

        page.get_by_role("button", name="นักวิจัย AI").click()
        page.wait_for_timeout(300)
        page.fill('[data-testid="youtube-title-input"]', youtube_title)
        page.fill('[data-testid="youtube-url-input"]', "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        page.select_option('[data-testid="youtube-template-select"]', value="ai_research_experiment_log")
        page.fill('#youtube-tags', 'nlp, experiment')
        page.click('form[aria-label="youtube-import-form"] button[type="submit"]')
        page.wait_for_selector('text=YouTube imported successfully')

        page.fill('[data-testid="text-title-input"]', text_title)
        page.select_option('[data-testid="text-template-select"]', value="general_text_note")
        page.fill('#text-tags', 'context, ingestion')
        page.fill('[data-testid="text-body-input"]', large_text)
        with page.expect_response("**/api/knowledge/import/text") as text_response_info:
            page.click('form[aria-label="text-import-form"] button[type="submit"]')
        text_response = text_response_info.value
        assert text_response.status == 200, text_response.text()
        page.wait_for_selector('text=Text ingested successfully')

        table_rows = page.locator('[data-testid="knowledge-table-row"]')
        assert table_rows.count() >= 3
        table_rows.filter(has_text=article_title).first.wait_for()
        table_rows.filter(has_text=youtube_title).first.wait_for()
        table_rows.filter(has_text=text_title).first.wait_for()

        page.fill('[data-testid="query-input"]', article_title)
        page.click('[data-testid="query-submit"]')
        page.wait_for_selector('[data-testid="query-results"] >> text=' + article_title)

        browser.close()
