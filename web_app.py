#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Training Platform Web Application
เว็บแอปพลิเคชันสำหรับ AI Training Platform Demo
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Literal
from datetime import datetime
from uuid import uuid4
from threading import Lock
import html
import re
import uvicorn
from fastapi import FastAPI, HTTPException, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, HttpUrl, Field, constr
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Knowledge workspace configuration
# ---------------------------------------------------------------------------

VALID_PROFESSIONS: Dict[str, Dict[str, str]] = {
    "writer": {"name": "นักเขียน"},
    "ai_researcher": {"name": "นักวิจัย AI"},
    "fullstack_dev": {"name": "Fullstack Dev"},
}

KNOWLEDGE_TEMPLATES: Dict[str, List[Dict[str, Any]]] = {
    "writer": [
        {
            "id": "writer_character_profile",
            "name": "Character Profile",
            "description": "สรุปคุณลักษณะและเป้าหมายของตัวละครหลัก",
            "fields": ["name", "role", "motivation", "conflict"],
        },
        {
            "id": "writer_plot_blueprint",
            "name": "Plot Blueprint",
            "description": "โครงเรื่องหลักพร้อมเหตุการณ์สำคัญ",
            "fields": ["act", "setup", "climax", "resolution"],
        },
        {
            "id": "writer_scene_tracker",
            "name": "Scene Tracker",
            "description": "ติดตามฉากและตัวละครที่เกี่ยวข้อง",
            "fields": ["scene", "location", "characters", "notes"],
        },
    ],
    "ai_researcher": [
        {
            "id": "ai_research_experiment_log",
            "name": "Experiment Log",
            "description": "บันทึกการทดลองพร้อม hyperparameters และผลลัพธ์",
            "fields": ["objective", "setup", "metrics", "insights"],
        },
        {
            "id": "ai_research_paper_digest",
            "name": "Paper Digest",
            "description": "สรุปงานวิจัยพร้อมประเด็นสำคัญ",
            "fields": ["title", "authors", "method", "contribution"],
        },
        {
            "id": "ai_research_dataset_card",
            "name": "Dataset Card",
            "description": "รายละเอียด dataset เพื่อใช้ในการทดลอง",
            "fields": ["name", "size", "modality", "ethics"],
        },
    ],
    "fullstack_dev": [
        {
            "id": "fullstack_component_doc",
            "name": "Component Doc",
            "description": "รายละเอียด component พร้อมตัวอย่างการใช้งาน",
            "fields": ["name", "props", "states", "usage"],
        },
        {
            "id": "fullstack_api_contract",
            "name": "API Contract",
            "description": "สัญญาการใช้งาน API พร้อมตัวอย่าง request/response",
            "fields": ["endpoint", "method", "payload", "response"],
        },
        {
            "id": "fullstack_bug_report",
            "name": "Bug Report",
            "description": "รายงานบั๊กพร้อมขั้นตอนการเกิดและผลกระทบ",
            "fields": ["title", "steps", "expected", "actual"],
        },
    ],
    "general": [
        {
            "id": "general_text_note",
            "name": "Text Note",
            "description": "โน้ตข้อความทั่วไป",
            "fields": ["title", "content"],
        },
        {
            "id": "general_web_clip",
            "name": "Web Clip",
            "description": "สรุปจากบทความหรือเว็บไซต์",
            "fields": ["url", "summary", "tags"],
        },
        {
            "id": "general_video_summary",
            "name": "Video Summary",
            "description": "สรุปจากวิดีโอหรือ YouTube",
            "fields": ["url", "key_points", "action_items"],
        },
        {
            "id": "general_link_hub",
            "name": "Link Hub",
            "description": "รวมลิงก์ที่เกี่ยวข้อง",
            "fields": ["title", "links", "notes"],
        },
        {
            "id": "general_task_tracker",
            "name": "Task Tracker",
            "description": "ติดตามงานและสถานะ",
            "fields": ["task", "status", "priority", "due"],
        },
        {
            "id": "general_meeting_notes",
            "name": "Meeting Notes",
            "description": "บันทึกการประชุม",
            "fields": ["date", "attendees", "summary", "actions"],
        },
    ],
}

KnowledgeSourceType = Literal["article", "youtube", "text"]


class KnowledgeItem(BaseModel):
    id: str
    source_type: KnowledgeSourceType
    title: constr(min_length=1, max_length=200)
    profession: str
    template_id: str
    template_name: str
    url: Optional[HttpUrl] = None
    tags: List[str] = Field(default_factory=list)
    content_preview: str = ""
    created_at: datetime


class ArticleImportRequest(BaseModel):
    url: HttpUrl
    title: constr(min_length=1, max_length=200)
    profession: str
    template_id: str
    summary: Optional[constr(max_length=2000)] = None
    tags: List[constr(min_length=1, max_length=32)] = Field(default_factory=list)


class YoutubeImportRequest(BaseModel):
    url: HttpUrl
    title: constr(min_length=1, max_length=200)
    profession: str
    template_id: str
    summary: Optional[constr(max_length=2000)] = None
    tags: List[constr(min_length=1, max_length=32)] = Field(default_factory=list)


class TextIngestRequest(BaseModel):
    title: constr(min_length=1, max_length=200)
    text: constr(min_length=1, max_length=200_000)
    profession: str
    template_id: str
    tags: List[constr(min_length=1, max_length=32)] = Field(default_factory=list)


class KnowledgeQuery(BaseModel):
    query: constr(min_length=1, max_length=500)
    top_k: Optional[int] = Field(default=5, ge=1, le=20)


KNOWLEDGE_ITEMS: List[KnowledgeItem] = []
KNOWLEDGE_LOCK = Lock()


def _normalise_tags(tags: List[str]) -> List[str]:
    """Return a constrained, sanitised list of tags."""

    cleaned: List[str] = []
    for tag in tags:
        # Only allow alphanumeric characters, underscores, and hyphens.
        safe = re.sub(r"[^\w\-]", "", tag.strip())
        if safe:
            cleaned.append(safe[:32])
    return cleaned[:10]


def _get_template(profession: str, template_id: str) -> Dict[str, Any]:
    """Fetch a template by id, searching profession-specific then general ones."""

    profession_templates = KNOWLEDGE_TEMPLATES.get(profession, [])
    general_templates = KNOWLEDGE_TEMPLATES.get("general", [])

    for template in profession_templates + general_templates:
        if template["id"] == template_id:
            return template

    raise HTTPException(status_code=404, detail="Template not found")


def _validate_profession(profession: str) -> None:
    """Ensure the requested profession is supported."""

    if profession not in VALID_PROFESSIONS:
        raise HTTPException(status_code=400, detail="Invalid profession")


def _create_knowledge_item(
    *,
    source_type: KnowledgeSourceType,
    title: str,
    profession: str,
    template_id: str,
    url: Optional[str] = None,
    content: Optional[str] = None,
    tags: Optional[List[str]] = None,
) -> KnowledgeItem:
    _validate_profession(profession)
    template = _get_template(profession, template_id)

    safe_tags = _normalise_tags(tags or [])

    content_text = (content or "").strip()
    preview_length = 400
    if not content_text:
        preview = ""
    elif len(content_text) <= preview_length:
        preview = html.escape(content_text)
    else:
        truncated = content_text[:preview_length]
        last_space = truncated.rfind(" ")
        if last_space > int(preview_length * 0.8):
            truncated = truncated[:last_space]
        preview = html.escape(truncated) + "..."

    item = KnowledgeItem(
        id=str(uuid4()),
        source_type=source_type,
        title=title,
        profession=profession,
        template_id=template_id,
        template_name=template["name"],
        url=url,
        tags=safe_tags,
        content_preview=preview,
        created_at=datetime.utcnow(),
    )
    with KNOWLEDGE_LOCK:
        KNOWLEDGE_ITEMS.insert(0, item)
        # Limit in-memory store size for stability
        max_items = int(os.environ.get("KNOWLEDGE_MAX_ITEMS", "1000"))
        if len(KNOWLEDGE_ITEMS) > max_items:
            # Remove oldest items (FIFO)
            KNOWLEDGE_ITEMS[:] = KNOWLEDGE_ITEMS[:max_items]


def _serialise_item(item: KnowledgeItem) -> Dict[str, Any]:
    data = item.model_dump()
    data["created_at"] = item.created_at.isoformat()
    return data

# Initialize FastAPI app
app = FastAPI(
    title="AI Training Platform",
    description="Fine-tuning Pipeline Demo Platform",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Pydantic models
class Conversation(BaseModel):
    user_message: str
    assistant_message: str

class DatasetInfo(BaseModel):
    total_conversations: int
    quality_score: float
    avg_message_length: float

class ModelInfo(BaseModel):
    model_name: str
    version: str
    status: str
    quality_score: float

# Global variables
DEMO_DATA = {
    "conversations": [],
    "model_info": None,
    "test_results": None
}

def load_demo_data():
    """โหลดข้อมูล demo จากไฟล์"""
    try:
        # Load conversations
        conversations_file = Path("data/raw/sample_conversations.json")
        if conversations_file.exists():
            with open(conversations_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                DEMO_DATA["conversations"] = data
        
        # Load model info
        model_file = Path("outputs/models/ai-training-platform-model-metadata.json")
        if model_file.exists():
            with open(model_file, 'r', encoding='utf-8') as f:
                DEMO_DATA["model_info"] = json.load(f)
        
        # Load test results
        test_file = Path("outputs/results/test_results.json")
        if test_file.exists():
            with open(test_file, 'r', encoding='utf-8') as f:
                DEMO_DATA["test_results"] = json.load(f)
        
        logger.info("Demo data loaded successfully")
    except Exception as e:
        logger.error(f"Error loading demo data: {e}")

# Load data on startup
load_demo_data()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """หน้าแรกของแอปพลิเคชัน"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "model_info": DEMO_DATA["model_info"],
        "test_results": DEMO_DATA["test_results"]
    })

@app.get("/dataset", response_class=HTMLResponse)
async def dataset_page(request: Request):
    """หน้าจัดการ dataset"""
    return templates.TemplateResponse("dataset.html", {
        "request": request,
        "conversations": DEMO_DATA["conversations"]
    })

@app.get("/model", response_class=HTMLResponse)
async def model_page(request: Request):
    """หน้าข้อมูลโมเดล"""
    return templates.TemplateResponse("model.html", {
        "request": request,
        "model_info": DEMO_DATA["model_info"],
        "test_results": DEMO_DATA["test_results"]
    })

@app.get("/deploy", response_class=HTMLResponse)
async def deploy_page(request: Request):
    """หน้าจัดการ deployment"""
    return templates.TemplateResponse("deploy.html", {
        "request": request,
        "model_info": DEMO_DATA["model_info"]
    })

@app.get("/knowledge", response_class=HTMLResponse)
async def knowledge_page(request: Request):
    """หน้า knowledge workspace"""
    return templates.TemplateResponse("knowledge.html", {"request": request})


@app.get("/api/knowledge/templates")
async def get_knowledge_templates() -> Dict[str, Any]:
    """Return knowledge workspace templates separated by profession."""
    return {
        "professions": VALID_PROFESSIONS,
        "templates": KNOWLEDGE_TEMPLATES,
    }


@app.get("/api/knowledge/items")
async def list_knowledge_items() -> Dict[str, Any]:
    """Return knowledge items stored in memory."""
    with KNOWLEDGE_LOCK:
        items = [_serialise_item(item) for item in KNOWLEDGE_ITEMS]
    return {"items": items}


@app.post("/api/knowledge/import/article")
async def import_article(payload: ArticleImportRequest) -> Dict[str, Any]:
    """Register a new article for the knowledge workspace."""
    item = _create_knowledge_item(
        source_type="article",
        title=payload.title,
        profession=payload.profession,
        template_id=payload.template_id,
        url=str(payload.url),
        content=payload.summary,
        tags=payload.tags,
    )
    return {"status": "success", "item": _serialise_item(item)}


@app.post("/api/knowledge/import/youtube")
async def import_youtube(payload: YoutubeImportRequest) -> Dict[str, Any]:
    """Register a new YouTube resource for the knowledge workspace."""
    item = _create_knowledge_item(
        source_type="youtube",
        title=payload.title,
        profession=payload.profession,
        template_id=payload.template_id,
        url=str(payload.url),
        content=payload.summary,
        tags=payload.tags,
    )
    return {"status": "success", "item": _serialise_item(item)}


@app.post("/api/knowledge/import/text")
async def import_text(payload: TextIngestRequest) -> Dict[str, Any]:
    """Ingest raw text content into the knowledge workspace."""
    item = _create_knowledge_item(
        source_type="text",
        title=payload.title,
        profession=payload.profession,
        template_id=payload.template_id,
        content=payload.text,
        tags=payload.tags,
    )
    return {"status": "success", "item": _serialise_item(item)}


@app.post("/api/knowledge/query")
async def query_knowledge(payload: KnowledgeQuery) -> Dict[str, Any]:
    """Perform a lightweight semantic search over stored knowledge items."""
    haystack: List[Dict[str, Any]]
    with KNOWLEDGE_LOCK:
        haystack = [_serialise_item(item) for item in KNOWLEDGE_ITEMS]

    query_text = payload.query.lower()
    results: List[Dict[str, Any]] = []
    for item in haystack:
        target = " ".join([
            item.get("title", ""),
            item.get("content_preview", ""),
            " ".join(item.get("tags", [])),
        ]).lower()
        if query_text in target:
            results.append(item)
        if len(results) >= payload.top_k:
            break

    return {"results": results, "count": len(results)}
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/api/dataset")
async def get_dataset():
    """API สำหรับดึงข้อมูล dataset"""
    return {
        "conversations": DEMO_DATA["conversations"],
        "total_count": len(DEMO_DATA["conversations"]),
        "quality_score": 8.5
    }

@app.get("/api/model")
async def get_model_info():
    """API สำหรับดึงข้อมูลโมเดล"""
    return DEMO_DATA["model_info"]

@app.get("/api/test-results")
async def get_test_results():
    """API สำหรับดึงผลการทดสอบ"""
    return DEMO_DATA["test_results"]

@app.post("/api/conversation")
async def add_conversation(conversation: Conversation):
    """API สำหรับเพิ่มการสนทนาใหม่"""
    try:
        new_conv = {
            "conversations": [
                {"from": "human", "value": conversation.user_message},
                {"from": "gpt", "value": conversation.assistant_message}
            ]
        }
        
        DEMO_DATA["conversations"].append(new_conv)
        
        # Save to file
        with open("data/raw/sample_conversations.json", 'w', encoding='utf-8') as f:
            json.dump(DEMO_DATA["conversations"], f, ensure_ascii=False, indent=2)
        
        return {"status": "success", "message": "Conversation added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/deploy")
async def deploy_model():
    """API สำหรับ deploy โมเดล"""
    try:
        # Simulate deployment process
        deployment_result = {
            "status": "deploying",
            "deployment_id": f"deploy-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "steps": [
                {"step": "validation", "status": "completed"},
                {"step": "upload", "status": "completed"},
                {"step": "deployment", "status": "in_progress"},
                {"step": "testing", "status": "pending"}
            ]
        }
        
        return deployment_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/deployment-status/{deployment_id}")
async def get_deployment_status(deployment_id: str):
    """API สำหรับตรวจสอบสถานะ deployment"""
    # Simulate deployment status
    return {
        "deployment_id": deployment_id,
        "status": "completed",
        "endpoint": "https://ai-training-platform.openai.azure.com/",
        "model_name": "ai-training-platform-model-v1",
        "created_at": datetime.now().isoformat()
    }

@app.post("/api/upload-dataset")
async def upload_dataset(file: UploadFile = File(...)):
    """API สำหรับอัปโหลด dataset"""
    try:
        if not file.filename.endswith('.json'):
            raise HTTPException(status_code=400, detail="Only JSON files are allowed")
        
        # Read and validate file
        content = await file.read()
        data = json.loads(content.decode('utf-8'))
        
        # Validate format
        if not isinstance(data, list):
            raise HTTPException(status_code=400, detail="Invalid dataset format")
        
        # Save file
        file_path = f"data/raw/{file.filename}"
        with open(file_path, 'wb') as f:
            f.write(content)
        
        # Update demo data
        DEMO_DATA["conversations"] = data
        
        return {
            "status": "success",
            "message": f"Dataset uploaded successfully: {len(data)} conversations",
            "file_path": file_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/export-azure-format")
async def export_azure_format():
    """API สำหรับ export ข้อมูลเป็น Azure format"""
    try:
        azure_format = []
        for conv in DEMO_DATA["conversations"]:
            messages = []
            for msg in conv["conversations"]:
                role = "assistant" if msg["from"] == "gpt" else "user"
                messages.append({
                    "role": role,
                    "content": msg["value"]
                })
            azure_format.append({"messages": messages})
        
        # Save to file
        output_path = "outputs/datasets/azure_fine_tuning_data.jsonl"
        with open(output_path, 'w', encoding='utf-8') as f:
            for item in azure_format:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
        
        return {
            "status": "success",
            "message": f"Azure format exported: {len(azure_format)} conversations",
            "file_path": output_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Create necessary directories
    os.makedirs("templates", exist_ok=True)
    os.makedirs("static", exist_ok=True)
    os.makedirs("static/css", exist_ok=True)
    os.makedirs("static/js", exist_ok=True)
    
    # Run the application
    uvicorn.run(
        "web_app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
