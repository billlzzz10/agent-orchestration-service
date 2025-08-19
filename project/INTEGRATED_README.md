# 🚀 Integrated Agent System

ระบบบูรณาการ **Google GenAI Toolbox** และ **Perplexity AI Toolkit** เข้ากับ **Multi-Agent Orchestration** ที่มี ≥6 โหนด และซับซ้อนเทียบเท่าหรือมากกว่าภาพที่อัปโหลด

## 📋 สรุปความสามารถ

### 🔧 Google GenAI Toolbox Integration
- **Database Tools**: เชื่อมต่อและจัดการฐานข้อมูลผ่าน MCP
- **SQL Execution**: รันคำสั่ง SQL แบบปลอดภัย
- **Data Analysis**: วิเคราะห์ข้อมูลด้วย AI
- **Schema Management**: จัดการโครงสร้างฐานข้อมูล

### 🤖 Perplexity AI Toolkit Integration
- **Real-time Search**: ค้นหาข้อมูลแบบ real-time
- **Sonar Models**: ใช้ LLama-3.1 based models
- **Chat Completion**: สนทนากับ AI แบบโต้ตอบ
- **Web Search**: ค้นหาข้อมูลจากเว็บ

### 🎯 Multi-Agent Orchestration
- **≥6 Nodes**: ระบบที่มีโหนดครบถ้วน
- **Tool Registry**: จัดการเครื่องมือแบบรวมศูนย์
- **Workflow Management**: จัดการ workflow แบบอัตโนมัติ
- **Memory Buffer**: เก็บข้อมูลระหว่างการประมวลผล

## 🏗️ โครงสร้างระบบ

```
Integrated Agent System
├── 🎯 Core Orchestrator
│   ├── Agent Management
│   ├── Tool Registry
│   └── Workflow Engine
├── 🔧 Tool Integration
│   ├── GenAI Toolbox Client
│   ├── Perplexity AI Client
│   └── Custom Tools
├── 🤖 Agent Types
│   ├── Tools Agent
│   ├── Analysis Agent
│   ├── Reasoning Agent
│   └── Creative Agent
└── 📊 Monitoring & Analytics
    ├── System Status
    ├── Performance Metrics
    └── Workflow History
```

## 🚀 การติดตั้ง

### 1. Prerequisites
```bash
# Python 3.11+
python --version

# Git
git --version

# Docker (optional)
docker --version
```

### 2. Clone และ Setup
```bash
# Clone โปรเจค
git clone <repository-url>
cd project

# ติดตั้ง dependencies
pip install -r requirements_integrated.txt

# ตั้งค่า environment variables
cp example.env .env
# แก้ไข .env file ตามต้องการ
```

### 3. API Keys Setup
```bash
# Perplexity AI API Key
export PERPLEXITY_API_KEY="your-perplexity-api-key"

# Google Cloud API Key (optional)
export GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"

# Anthropic API Key (optional)
export ANTHROPIC_API_KEY="your-anthropic-api-key"
```

## 🎮 การใช้งาน

### 1. รันระบบบูรณาการ
```bash
# รันระบบหลัก
python scripts/integrated_agent_system.py

# รันระบบ Multi-Agent Orchestration
python scripts/agent_orchestrator.py

# ทดสอบ workflow
python scripts/test_integration.py
```

### 2. ตัวอย่างการใช้งาน

#### การวิเคราะห์ข้อความ
```python
from scripts.integrated_agent_system import IntegratedOrchestrator

# สร้าง orchestrator
orchestrator = IntegratedOrchestrator()

# สร้าง agent
agent = orchestrator.create_agent("analysis_agent", "analysis")

# วิเคราะห์ข้อความ
result = await orchestrator.run_workflow(
    "Analyze this text for sentiment and structure",
    "analysis_agent"
)
```

#### การค้นหาข้อมูล
```python
# ค้นหาข้อมูลด้วย Perplexity AI
result = await orchestrator.run_workflow(
    "Search for latest AI news",
    "tools_agent"
)
```

#### การสร้างโค้ด
```python
# สร้างโค้ดด้วย AI
result = await orchestrator.run_workflow(
    "Generate Python code for a calculator",
    "tools_agent"
)
```

## 🔧 การตั้งค่า

### 1. GenAI Toolbox Configuration
```yaml
# tools.yaml
sources:
  my-database:
    kind: postgres
    host: localhost
    port: 5432
    database: mydb
    user: myuser
    password: mypassword

tools:
  query-data:
    kind: postgres-sql
    source: my-database
    description: Query data from database
    parameters:
      - name: query
        type: string
        description: SQL query
```

### 2. Perplexity AI Configuration
```python
# config.py
PERPLEXITY_CONFIG = {
    "model": "sonar-small-online",
    "temperature": 0.7,
    "max_tokens": 1024,
    "focus": "web"
}
```

### 3. Agent Configuration
```json
{
  "agents": {
    "tools_agent": {
      "type": "tools",
      "model": "claude-3-5-sonnet-20241022",
      "temperature": 0.7,
      "capabilities": ["text_analysis", "code_generation", "web_search"]
    },
    "analysis_agent": {
      "type": "analysis",
      "model": "sonar-small-online",
      "temperature": 0.3,
      "capabilities": ["data_analysis", "reasoning"]
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
print(f"Available Tools: {status['available_tools']}")
print(f"GenAI Toolbox: {status['genai_toolbox_available']}")
print(f"Perplexity AI: {status['perplexity_ai_available']}")
```

### 2. Workflow History
```python
# ดูประวัติ workflow
history = orchestrator.workflow_history
for entry in history:
    print(f"Agent: {entry['agent_id']}")
    print(f"Results: {len(entry['results'])} tools executed")
```

### 3. Performance Metrics
```python
# ดูประสิทธิภาพ
metrics = {
    "total_workflows": len(orchestrator.workflow_history),
    "success_rate": calculate_success_rate(),
    "avg_response_time": calculate_avg_response_time(),
    "tool_usage": get_tool_usage_stats()
}
```

## 🔍 การทดสอบ

### 1. Unit Tests
```bash
# รัน unit tests
pytest tests/unit/

# รัน integration tests
pytest tests/integration/

# รัน all tests
pytest tests/
```

### 2. Performance Tests
```bash
# ทดสอบประสิทธิภาพ
python scripts/performance_test.py

# ทดสอบ load
python scripts/load_test.py
```

### 3. API Tests
```bash
# ทดสอบ API endpoints
python scripts/api_test.py
```

## 🛠️ การพัฒนา

### 1. Adding New Tools
```python
# เพิ่มเครื่องมือใหม่
async def custom_tool(params: Dict[str, Any]) -> Dict[str, Any]:
    # Tool logic here
    return {"result": "success"}

# ลงทะเบียนเครื่องมือ
tool_config = ToolConfig(
    name="custom_tool",
    tool_type=ToolType.CUSTOM_TOOL,
    description="Custom tool description",
    config={"function": custom_tool}
)
orchestrator.tool_registry.register_tool(tool_config)
```

### 2. Adding New Agents
```python
# สร้าง agent ใหม่
class CustomAgent(EnhancedAgent):
    async def process(self, message: Dict[str, Any]) -> Dict[str, Any]:
        # Custom processing logic
        return {"result": "processed"}

# ลงทะเบียน agent
custom_agent = CustomAgent("custom_agent", "custom")
orchestrator.agents["custom_agent"] = custom_agent
```

### 3. Extending Workflows
```python
# ขยาย workflow
async def custom_workflow(orchestrator, input_data):
    # Custom workflow logic
    result1 = await orchestrator.run_workflow(input_data, "agent1")
    result2 = await orchestrator.run_workflow(result1, "agent2")
    return result2
```

## 📈 การปรับปรุงประสิทธิภาพ

### 1. Caching
```python
# ใช้ Redis สำหรับ caching
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Cache results
def cache_result(key: str, value: Any, ttl: int = 3600):
    redis_client.setex(key, ttl, json.dumps(value))
```

### 2. Async Processing
```python
# ใช้ async/await สำหรับการประมวลผลแบบ concurrent
async def process_multiple_tasks(tasks: List[str]):
    results = await asyncio.gather(*[
        orchestrator.run_workflow(task) for task in tasks
    ])
    return results
```

### 3. Load Balancing
```python
# กระจายโหลดระหว่าง agents
def select_agent(workload: str) -> str:
    agent_loads = get_agent_loads()
    return min(agent_loads, key=agent_loads.get)
```

## 🔒 ความปลอดภัย

### 1. API Key Management
```python
# ใช้ environment variables
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('PERPLEXITY_API_KEY')
```

### 2. Input Validation
```python
# ตรวจสอบ input
from pydantic import BaseModel, validator

class WorkflowInput(BaseModel):
    content: str
    tools: List[str] = []
    
    @validator('content')
    def validate_content(cls, v):
        if len(v) > 10000:
            raise ValueError('Content too long')
        return v
```

### 3. Rate Limiting
```python
# จำกัดอัตราการเรียก API
import asyncio
from asyncio import Semaphore

semaphore = Semaphore(10)  # Max 10 concurrent requests

async def rate_limited_request(func, *args):
    async with semaphore:
        return await func(*args)
```

## 🚨 การแก้ไขปัญหา

### 1. Common Issues

#### GenAI Toolbox Connection Error
```bash
# ตรวจสอบ server
curl http://localhost:8080/health

# ตรวจสอบ configuration
cat tools.yaml
```

#### Perplexity AI API Error
```bash
# ตรวจสอบ API key
echo $PERPLEXITY_API_KEY

# ทดสอบ API
curl -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
     https://api.perplexity.ai/chat/completions
```

#### Agent Processing Error
```python
# ตรวจสอบ agent status
status = orchestrator.get_system_status()
print(f"Agent count: {status['total_agents']}")

# ตรวจสอบ tool availability
tools = orchestrator.tool_registry.list_tools()
print(f"Available tools: {tools}")
```

### 2. Debug Mode
```python
# เปิด debug mode
import logging
logging.basicConfig(level=logging.DEBUG)

# ดู detailed logs
logger.debug("Detailed debug information")
```

## 📚 เอกสารอ้างอิง

### External Links
- [Google GenAI Toolbox Documentation](https://googleapis.github.io/genai-toolbox/)
- [Perplexity AI API Documentation](https://docs.perplexity.ai/)
- [MCP Protocol Documentation](https://modelcontextprotocol.io/)

### Internal Documentation
- [Agent Orchestrator Guide](AGENT_ORCHESTRATOR.md)
- [Tool Integration Guide](TOOL_INTEGRATION.md)
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
```

## 📄 License

MIT License - ดูรายละเอียดใน [LICENSE](LICENSE) file

## 🙏 Acknowledgments

- Google GenAI Toolbox team สำหรับ MCP server
- Perplexity AI team สำหรับ Sonar models
- Claude team สำหรับ AI assistance
- Community contributors สำหรับ feedback และ improvements

---

**🎉 ขอบคุณที่ใช้ Integrated Agent System!**

หากมีคำถามหรือต้องการความช่วยเหลือ กรุณาติดต่อผ่าน GitHub Issues หรือ Discord community
