# 🔗 MCP Integrated System

ระบบบูรณาการ **MCP (Model Context Protocol)** ที่เชื่อมต่อกับเครื่องมือต่างๆ ผ่าน MCP servers

## 📋 สรุปความสามารถ

### 🌐 Browser Automation (Puppeteer)
- **Navigate**: ไปยัง URL ที่กำหนด
- **Screenshot**: ถ่ายภาพหน้าจอ
- **Click**: คลิก element บนหน้าเว็บ
- **Type**: พิมพ์ข้อความ
- **Scroll**: เลื่อนหน้าเว็บ

### 📊 Project Management (GitLab)
- **Create Issue**: สร้าง issue ใหม่
- **List Projects**: รายการโปรเจค
- **Create Merge Request**: สร้าง merge request
- **Comment on Issue**: เพิ่ม comment

### 💬 Communication (Slack)
- **Send Message**: ส่งข้อความไปยัง channel
- **List Channels**: รายการ channels
- **Create Channel**: สร้าง channel ใหม่
- **Upload File**: อัปโหลดไฟล์

### 🗺️ Location Services (Google Maps)
- **Get Directions**: หาเส้นทาง
- **Place Search**: ค้นหาสถานที่
- **Place Details**: รายละเอียดสถานที่
- **Geocoding**: แปลงที่อยู่เป็นพิกัด

### 🗄️ Data Management (Database)
- **Execute Query**: รันคำสั่ง SQL
- **Analyze Schema**: วิเคราะห์โครงสร้างฐานข้อมูล
- **Create Table**: สร้างตารางใหม่
- **Backup Data**: สำรองข้อมูล

### 📁 File Operations (File System)
- **Read File**: อ่านไฟล์
- **Write File**: เขียนไฟล์
- **List Files**: รายการไฟล์
- **Create Directory**: สร้างโฟลเดอร์

### 🔍 AI Search (Perplexity)
- **Web Search**: ค้นหาข้อมูลจากเว็บ
- **Chat Completion**: สนทนากับ AI
- **Real-time Search**: ค้นหาแบบ real-time

## 🏗️ โครงสร้างระบบ

```
MCP Integrated System
├── 🔧 MCP Server Manager
│   ├── Puppeteer Server
│   ├── GitLab Server
│   ├── Slack Server
│   ├── Google Maps Server
│   ├── Database Server
│   ├── File System Server
│   └── Perplexity Server
├── 🛠️ Tool Registry
│   ├── Browser Tools
│   ├── Project Tools
│   ├── Communication Tools
│   ├── Location Tools
│   ├── Database Tools
│   ├── File Tools
│   └── AI Tools
├── 🤖 Enhanced Agents
│   ├── Automation Agent
│   ├── Project Agent
│   └── Research Agent
└── 🎯 Orchestrator
    ├── Workflow Management
    ├── Agent Coordination
    └── System Monitoring
```

## 🚀 การติดตั้ง

### 1. Prerequisites
```bash
# Node.js และ npm
node --version
npm --version

# Python 3.11+
python --version

# Git
git --version
```

### 2. Clone และ Setup
```bash
# Clone โปรเจค
git clone <repository-url>
cd project

# ติดตั้ง dependencies
pip install -r requirements_integrated.txt
npm install -g @modelcontextprotocol/server-puppeteer
npm install -g @modelcontextprotocol/server-gitlab
npm install -g @modelcontextprotocol/server-slack
npm install -g @modelcontextprotocol/server-google-maps
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-perplexity
```

### 3. API Keys Setup
```bash
# GitLab
export GITLAB_TOKEN="your-gitlab-token"
export GITLAB_URL="https://gitlab.com"

# Slack
export SLACK_BOT_TOKEN="your-slack-bot-token"
export SLACK_SIGNING_SECRET="your-slack-signing-secret"

# Google Maps
export GOOGLE_MAPS_API_KEY="your-google-maps-api-key"

# Perplexity AI
export PERPLEXITY_API_KEY="your-perplexity-api-key"

# Google Cloud (optional)
export GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"
```

## 🎮 การใช้งาน

### 1. รันระบบ MCP
```bash
# รันระบบหลัก
python scripts/mcp_integrated_system.py

# รันระบบ Multi-Agent Orchestration
python scripts/agent_orchestrator.py

# ทดสอบ workflow
python scripts/test_mcp_integration.py
```

### 2. ตัวอย่างการใช้งาน

#### Browser Automation
```python
from scripts.mcp_integrated_system import MCPIntegratedOrchestrator

# สร้าง orchestrator
orchestrator = MCPIntegratedOrchestrator()

# สร้าง agent
agent = orchestrator.create_agent("automation_agent", "automation")

# เริ่มต้นระบบ
await orchestrator.initialize_system()

# ใช้งาน browser automation
result = await orchestrator.run_workflow(
    "Navigate to https://github.com and take a screenshot",
    "automation_agent"
)
```

#### Project Management
```python
# สร้าง GitLab issue
result = await orchestrator.run_workflow(
    "Create a GitLab issue for bug tracking",
    "project_agent"
)

# ส่ง Slack message
result = await orchestrator.run_workflow(
    "Send a message to Slack channel about project update",
    "project_agent"
)
```

#### Research Task
```python
# ค้นหาข้อมูลด้วย AI
result = await orchestrator.run_workflow(
    "Search for latest AI developments",
    "research_agent"
)

# หาเส้นทาง
result = await orchestrator.run_workflow(
    "Get directions from Bangkok to Chiang Mai",
    "research_agent"
)
```

## 🔧 การตั้งค่า

### 1. MCP Configuration
```json
{
  "mcpServers": {
    "puppeteer": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-puppeteer"],
      "env": {"NODE_ENV": "production"}
    },
    "gitlab": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-gitlab"],
      "env": {"GITLAB_TOKEN": "${GITLAB_TOKEN}"}
    }
  }
}
```

### 2. Agent Configuration
```json
{
  "agents": {
    "automation_agent": {
      "type": "automation",
      "tools": ["browser_automation", "file_operations"],
      "model": "claude-3-5-sonnet-20241022",
      "temperature": 0.7
    },
    "project_agent": {
      "type": "management",
      "tools": ["project_management", "communication"],
      "model": "sonar-small-online",
      "temperature": 0.3
    }
  }
}
```

### 3. Workflow Configuration
```json
{
  "workflows": {
    "web_automation": {
      "description": "Automate web browser tasks",
      "steps": [
        {
          "agent": "automation_agent",
          "action": "navigate",
          "parameters": {"url": "https://example.com"}
        },
        {
          "agent": "automation_agent",
          "action": "screenshot",
          "parameters": {"path": "screenshot.png"}
        }
      ]
    }
  }
}
```

## 📊 การติดตามและวิเคราะห์

### 1. System Status
```python
# ดูสถานะระบบ
status = orchestrator.get_system_status()
print(f"Total Agents: {status['total_agents']}")
print(f"Total Tools: {status['total_tools']}")
print(f"Workflow History: {status['workflow_history_count']}")

# ดูสถานะ servers
server_status = status.get("server_status", {})
for server_name, server_info in server_status.get("servers", {}).items():
    status_icon = "🟢" if server_info["running"] else "🔴"
    print(f"{status_icon} {server_name}: {server_info['type']}")
```

### 2. Tool Usage Analytics
```python
# ดูการใช้งานเครื่องมือ
tool_usage = {}
for entry in orchestrator.workflow_history:
    for tool_name in entry['results'].keys():
        tool_usage[tool_name] = tool_usage.get(tool_name, 0) + 1

for tool, count in sorted(tool_usage.items(), key=lambda x: x[1], reverse=True):
    print(f"{tool}: {count} times")
```

### 3. Performance Metrics
```python
# ดูประสิทธิภาพ
import time

start_time = time.time()
result = await orchestrator.run_workflow("test task")
execution_time = time.time() - start_time

print(f"Execution time: {execution_time:.2f} seconds")
print(f"Success rate: {calculate_success_rate()}%")
```

## 🔍 การทดสอบ

### 1. Unit Tests
```bash
# รัน unit tests
pytest tests/unit/test_mcp_system.py

# รัน integration tests
pytest tests/integration/test_mcp_integration.py

# รัน all tests
pytest tests/
```

### 2. MCP Server Tests
```bash
# ทดสอบ Puppeteer server
npx @modelcontextprotocol/server-puppeteer --test

# ทดสอบ GitLab server
npx @modelcontextprotocol/server-gitlab --test

# ทดสอบ Slack server
npx @modelcontextprotocol/server-slack --test
```

### 3. End-to-End Tests
```bash
# ทดสอบ workflow ทั้งหมด
python scripts/test_mcp_workflows.py

# ทดสอบ performance
python scripts/performance_test.py
```

## 🛠️ การพัฒนา

### 1. Adding New MCP Server
```python
# เพิ่ม MCP server ใหม่
new_server_config = MCPServerConfig(
    name="custom_server",
    server_type=MCPServerType.CUSTOM,
    command="npx",
    args=["@modelcontextprotocol/server-custom"],
    env={"CUSTOM_API_KEY": "your-api-key"}
)

orchestrator.agents["automation_agent"].server_manager.register_server(new_server_config)
```

### 2. Adding New Tools
```python
# เพิ่มเครื่องมือใหม่
new_tool = MCPTool(
    name="custom_tool",
    description="Custom tool description",
    parameters={
        "param1": {"type": "string", "description": "Parameter 1"}
    },
    server_name="custom_server"
)

orchestrator.agents["automation_agent"].tool_registry.register_tool(new_tool)
```

### 3. Creating Custom Workflows
```python
# สร้าง workflow ใหม่
async def custom_workflow(orchestrator, input_data):
    # Step 1: Browser automation
    browser_result = await orchestrator.run_workflow(
        f"Navigate to {input_data['url']}",
        "automation_agent"
    )
    
    # Step 2: Take screenshot
    screenshot_result = await orchestrator.run_workflow(
        "Take screenshot of current page",
        "automation_agent"
    )
    
    # Step 3: Send to Slack
    slack_result = await orchestrator.run_workflow(
        f"Send screenshot to Slack channel {input_data['channel']}",
        "project_agent"
    )
    
    return {
        "browser": browser_result,
        "screenshot": screenshot_result,
        "slack": slack_result
    }
```

## 📈 การปรับปรุงประสิทธิภาพ

### 1. Server Pooling
```python
# ใช้ server pooling สำหรับ load balancing
class MCPServerPool:
    def __init__(self, server_config, pool_size=5):
        self.servers = []
        self.pool_size = pool_size
        self.current_index = 0
        
    async def get_server(self):
        if not self.servers:
            await self.initialize_pool()
        
        server = self.servers[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.servers)
        return server
```

### 2. Caching
```python
# ใช้ Redis สำหรับ caching
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, db=0)

async def cached_tool_execution(tool_name, parameters):
    cache_key = f"{tool_name}:{hash(json.dumps(parameters, sort_keys=True))}"
    
    # ตรวจสอบ cache
    cached_result = redis_client.get(cache_key)
    if cached_result:
        return json.loads(cached_result)
    
    # รันเครื่องมือ
    result = await execute_tool(tool_name, parameters)
    
    # เก็บใน cache
    redis_client.setex(cache_key, 3600, json.dumps(result))
    return result
```

### 3. Async Processing
```python
# ใช้ async/await สำหรับการประมวลผลแบบ concurrent
async def parallel_workflow(orchestrator, tasks):
    # รันหลาย tasks พร้อมกัน
    results = await asyncio.gather(*[
        orchestrator.run_workflow(task, agent_id)
        for task, agent_id in tasks
    ])
    return results
```

## 🔒 ความปลอดภัย

### 1. API Key Management
```python
# ใช้ environment variables
import os
from dotenv import load_dotenv

load_dotenv()

required_keys = [
    "GITLAB_TOKEN",
    "SLACK_BOT_TOKEN",
    "GOOGLE_MAPS_API_KEY",
    "PERPLEXITY_API_KEY"
]

for key in required_keys:
    if not os.getenv(key):
        raise ValueError(f"Missing required API key: {key}")
```

### 2. Input Validation
```python
# ตรวจสอบ input
from pydantic import BaseModel, validator

class MCPRequest(BaseModel):
    tool_name: str
    parameters: dict
    
    @validator('tool_name')
    def validate_tool_name(cls, v):
        allowed_tools = ['browser_navigate', 'gitlab_create_issue', 'slack_send_message']
        if v not in allowed_tools:
            raise ValueError(f"Invalid tool name: {v}")
        return v
```

### 3. Rate Limiting
```python
# จำกัดอัตราการเรียก API
import asyncio
from asyncio import Semaphore

class RateLimiter:
    def __init__(self, max_requests=60, time_window=60):
        self.semaphore = Semaphore(max_requests)
        self.time_window = time_window
    
    async def execute(self, func, *args):
        async with self.semaphore:
            return await func(*args)
```

## 🚨 การแก้ไขปัญหา

### 1. Common Issues

#### MCP Server Connection Error
```bash
# ตรวจสอบ server status
curl http://localhost:8080/health

# ตรวจสอบ logs
tail -f logs/mcp_system.log

# Restart server
pkill -f "npx @modelcontextprotocol/server"
```

#### API Key Issues
```bash
# ตรวจสอบ API keys
echo $GITLAB_TOKEN
echo $SLACK_BOT_TOKEN
echo $GOOGLE_MAPS_API_KEY

# ทดสอบ API
curl -H "Authorization: Bearer $GITLAB_TOKEN" \
     https://gitlab.com/api/v4/projects
```

#### Tool Execution Error
```python
# ตรวจสอบ tool availability
tools = orchestrator.agents["automation_agent"].tool_registry.list_tools()
print(f"Available tools: {tools}")

# ตรวจสอบ server status
server_status = orchestrator.agents["automation_agent"].server_manager.get_server_status()
print(f"Server status: {server_status}")
```

### 2. Debug Mode
```python
# เปิด debug mode
import logging
logging.basicConfig(level=logging.DEBUG)

# ดู detailed logs
logger.debug("Detailed debug information")
```

### 3. Health Checks
```python
# ตรวจสอบสุขภาพระบบ
async def health_check():
    checks = {
        "servers": await check_server_health(),
        "tools": await check_tool_health(),
        "agents": await check_agent_health(),
        "workflows": await check_workflow_health()
    }
    
    for component, status in checks.items():
        print(f"{component}: {'✅' if status else '❌'}")
```

## 📚 เอกสารอ้างอิง

### External Links
- [MCP Protocol Documentation](https://modelcontextprotocol.io/)
- [Puppeteer MCP Server](https://github.com/modelcontextprotocol/server-puppeteer)
- [GitLab MCP Server](https://github.com/modelcontextprotocol/server-gitlab)
- [Slack MCP Server](https://github.com/modelcontextprotocol/server-slack)
- [Google Maps MCP Server](https://github.com/modelcontextprotocol/server-google-maps)

### Internal Documentation
- [MCP Integration Guide](MCP_INTEGRATION.md)
- [Tool Development Guide](TOOL_DEVELOPMENT.md)
- [Workflow Management Guide](WORKFLOW_MANAGEMENT.md)

## 🤝 การมีส่วนร่วม

### 1. Reporting Issues
- ใช้ GitHub Issues สำหรับรายงานปัญหา
- ให้ข้อมูลที่ครบถ้วน: error messages, logs, steps to reproduce

### 2. Contributing Code
- Fork repository
- สร้าง feature branch
- เขียน tests
- Submit pull request

### 3. Code Style
```bash
# ใช้ black สำหรับ formatting
black scripts/

# ใช้ flake8 สำหรับ linting
flake8 scripts/

# ใช้ mypy สำหรับ type checking
mypy scripts/
```

## 📄 License

MIT License - ดูรายละเอียดใน [LICENSE](LICENSE) file

## 🙏 Acknowledgments

- MCP Protocol team สำหรับ protocol specification
- Puppeteer team สำหรับ browser automation
- GitLab team สำหรับ project management
- Slack team สำหรับ communication
- Google Maps team สำหรับ location services
- Perplexity AI team สำหรับ AI search
- Community contributors สำหรับ feedback และ improvements

---

**🎉 ขอบคุณที่ใช้ MCP Integrated System!**

หากมีคำถามหรือต้องการความช่วยเหลือ กรุณาติดต่อผ่าน GitHub Issues หรือ Discord community
