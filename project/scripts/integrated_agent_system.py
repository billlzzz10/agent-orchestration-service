#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integrated Agent System
ระบบบูรณาการ Google GenAI Toolbox และ Perplexity AI Toolkit เข้ากับ Multi-Agent Orchestration
"""

import json
import asyncio
import time
import logging
import os
import sys
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import requests
from pathlib import Path

# ตั้งค่า logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ToolType(Enum):
    """ประเภทของเครื่องมือ"""
    GENAI_TOOLBOX = "genai_toolbox"
    PERPLEXITY_AI = "perplexity_ai"
    CUSTOM_TOOL = "custom_tool"

@dataclass
class ToolConfig:
    """การตั้งค่าเครื่องมือ"""
    name: str
    tool_type: ToolType
    description: str
    config: Dict[str, Any]
    enabled: bool = True

class GenAIToolboxClient:
    """Client สำหรับ Google GenAI Toolbox"""
    
    def __init__(self, server_url: str = "http://localhost:8080"):
        self.server_url = server_url
        self.session = requests.Session()
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """รายการเครื่องมือที่มีใน Toolbox"""
        try:
            response = self.session.get(f"{self.server_url}/tools")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error listing GenAI Toolbox tools: {e}")
            return []
    
    async def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """รันเครื่องมือใน Toolbox"""
        try:
            payload = {
                "tool": tool_name,
                "parameters": parameters
            }
            response = self.session.post(f"{self.server_url}/execute", json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error executing GenAI Toolbox tool {tool_name}: {e}")
            return {"error": str(e)}
    
    async def get_tool_schema(self, tool_name: str) -> Dict[str, Any]:
        """ดึง schema ของเครื่องมือ"""
        try:
            response = self.session.get(f"{self.server_url}/tools/{tool_name}/schema")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting tool schema for {tool_name}: {e}")
            return {}

class PerplexityAIClient:
    """Client สำหรับ Perplexity AI Toolkit"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('PERPLEXITY_API_KEY')
        self.base_url = "https://api.perplexity.ai"
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            })
    
    async def chat_completion(self, messages: List[Dict[str, str]], 
                            model: str = "sonar-small-online",
                            temperature: float = 0.7,
                            max_tokens: int = 1024) -> Dict[str, Any]:
        """ส่งข้อความไปยัง Perplexity AI"""
        try:
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            response = self.session.post(f"{self.base_url}/chat/completions", json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error calling Perplexity AI: {e}")
            return {"error": str(e)}
    
    async def search(self, query: str, focus: str = "web") -> Dict[str, Any]:
        """ค้นหาข้อมูลด้วย Perplexity AI"""
        try:
            messages = [{"role": "user", "content": query}]
            return await self.chat_completion(messages, model="sonar-small-online")
        except Exception as e:
            logger.error(f"Error searching with Perplexity AI: {e}")
            return {"error": str(e)}

class IntegratedToolRegistry:
    """Registry สำหรับเครื่องมือที่บูรณาการ"""
    
    def __init__(self):
        self.tools = {}
        self.genai_client = None
        self.perplexity_client = None
        self.setup_clients()
        self.register_default_tools()
    
    def setup_clients(self):
        """ตั้งค่า clients"""
        try:
            self.genai_client = GenAIToolboxClient()
            logger.info("✅ GenAI Toolbox client initialized")
        except Exception as e:
            logger.warning(f"⚠️ Could not initialize GenAI Toolbox client: {e}")
        
        try:
            self.perplexity_client = PerplexityAIClient()
            logger.info("✅ Perplexity AI client initialized")
        except Exception as e:
            logger.warning(f"⚠️ Could not initialize Perplexity AI client: {e}")
    
    def register_tool(self, tool_config: ToolConfig):
        """ลงทะเบียนเครื่องมือใหม่"""
        self.tools[tool_config.name] = tool_config
        logger.info(f"Registered tool: {tool_config.name} ({tool_config.tool_type.value})")
    
    def get_tool(self, name: str) -> Optional[ToolConfig]:
        """ดึงเครื่องมือตามชื่อ"""
        return self.tools.get(name)
    
    def list_tools(self) -> List[str]:
        """รายการเครื่องมือทั้งหมด"""
        return list(self.tools.keys())
    
    async def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """รันเครื่องมือ"""
        tool = self.get_tool(tool_name)
        if not tool or not tool.enabled:
            return {"error": f"Tool {tool_name} not found or disabled"}
        
        try:
            if tool.tool_type == ToolType.GENAI_TOOLBOX:
                if self.genai_client:
                    return await self.genai_client.execute_tool(tool_name, parameters)
                else:
                    return {"error": "GenAI Toolbox client not available"}
            
            elif tool.tool_type == ToolType.PERPLEXITY_AI:
                if self.perplexity_client:
                    if tool_name == "perplexity_chat":
                        return await self.perplexity_client.chat_completion(
                            parameters.get("messages", []),
                            parameters.get("model", "sonar-small-online"),
                            parameters.get("temperature", 0.7),
                            parameters.get("max_tokens", 1024)
                        )
                    elif tool_name == "perplexity_search":
                        return await self.perplexity_client.search(
                            parameters.get("query", ""),
                            parameters.get("focus", "web")
                        )
                else:
                    return {"error": "Perplexity AI client not available"}
            
            elif tool.tool_type == ToolType.CUSTOM_TOOL:
                # รัน custom tool function
                func = tool.config.get("function")
                if func and callable(func):
                    return await func(parameters)
                else:
                    return {"error": "Custom tool function not found"}
            
            return {"error": f"Unknown tool type: {tool.tool_type}"}
        
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {e}")
            return {"error": str(e)}
    
    def register_default_tools(self):
        """ลงทะเบียนเครื่องมือเริ่มต้น"""
        
        # GenAI Toolbox tools
        if self.genai_client:
            self.register_tool(ToolConfig(
                name="database_query",
                tool_type=ToolType.GENAI_TOOLBOX,
                description="Execute SQL queries on connected databases",
                config={"category": "database", "requires_auth": True}
            ))
            
            self.register_tool(ToolConfig(
                name="data_analysis",
                tool_type=ToolType.GENAI_TOOLBOX,
                description="Analyze data using AI-powered insights",
                config={"category": "analytics", "requires_auth": True}
            ))
        
        # Perplexity AI tools
        if self.perplexity_client:
            self.register_tool(ToolConfig(
                name="perplexity_chat",
                tool_type=ToolType.PERPLEXITY_AI,
                description="Chat with Perplexity AI using Sonar models",
                config={"model": "sonar-small-online", "capabilities": ["chat", "reasoning"]}
            ))
            
            self.register_tool(ToolConfig(
                name="perplexity_search",
                tool_type=ToolType.PERPLEXITY_AI,
                description="Real-time web search with Perplexity AI",
                config={"focus": "web", "capabilities": ["search", "real-time"]}
            ))
        
        # Custom tools
        async def text_analyzer(params: Dict[str, Any]) -> Dict[str, Any]:
            """วิเคราะห์ข้อความ"""
            text = params.get("text", "")
            words = text.split()
            return {
                "word_count": len(words),
                "char_count": len(text),
                "avg_word_length": sum(len(word) for word in words) / len(words) if words else 0,
                "sentiment": "positive" if any(word in ['good', 'great', 'excellent'] for word in words) else "neutral"
            }
        
        async def code_generator(params: Dict[str, Any]) -> Dict[str, Any]:
            """สร้างโค้ด"""
            language = params.get("language", "python")
            description = params.get("description", "")
            return {
                "code": f"# Generated {language} code for: {description}\nprint('Hello, World!')",
                "language": language,
                "description": description
            }
        
        self.register_tool(ToolConfig(
            name="text_analyzer",
            tool_type=ToolType.CUSTOM_TOOL,
            description="Analyze text content for sentiment and structure",
            config={"function": text_analyzer, "category": "text_processing"}
        ))
        
        self.register_tool(ToolConfig(
            name="code_generator",
            tool_type=ToolType.CUSTOM_TOOL,
            description="Generate code based on description",
            config={"function": code_generator, "category": "code_generation"}
        ))

class EnhancedAgent:
    """Agent ที่ได้รับการปรับปรุงให้ใช้เครื่องมือที่บูรณาการ"""
    
    def __init__(self, agent_id: str, agent_type: str, config: Dict[str, Any] = None):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.config = config or {}
        self.tool_registry = IntegratedToolRegistry()
        self.memory = {}
    
    async def process(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """ประมวลผลข้อความ"""
        content = message.get("content", "")
        tools_needed = message.get("tools", [])
        
        results = {}
        
        # วิเคราะห์ข้อความเพื่อเลือกเครื่องมือ
        if "analyze" in content.lower() or "text" in content.lower():
            tool_result = await self.tool_registry.execute_tool("text_analyzer", {"text": content})
            results["text_analysis"] = tool_result
        
        if "search" in content.lower() or "find" in content.lower():
            tool_result = await self.tool_registry.execute_tool("perplexity_search", {"query": content})
            results["web_search"] = tool_result
        
        if "code" in content.lower() or "generate" in content.lower():
            tool_result = await self.tool_registry.execute_tool("code_generator", {
                "language": "python",
                "description": content
            })
            results["code_generation"] = tool_result
        
        # รันเครื่องมือที่ระบุ
        for tool_name in tools_needed:
            if tool_name in self.tool_registry.list_tools():
                tool_result = await self.tool_registry.execute_tool(tool_name, message.get("parameters", {}))
                results[tool_name] = tool_result
        
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "input": message,
            "results": results,
            "timestamp": time.time()
        }
    
    def get_capabilities(self) -> List[str]:
        """ความสามารถของ agent"""
        return [tool.name for tool in self.tool_registry.tools.values() if tool.enabled]

class IntegratedOrchestrator:
    """ระบบจัดการ Agent ที่บูรณาการ"""
    
    def __init__(self):
        self.agents = {}
        self.tool_registry = IntegratedToolRegistry()
        self.workflow_history = []
    
    def create_agent(self, agent_id: str, agent_type: str, config: Dict[str, Any] = None) -> EnhancedAgent:
        """สร้าง agent ใหม่"""
        agent = EnhancedAgent(agent_id, agent_type, config)
        self.agents[agent_id] = agent
        return agent
    
    async def run_workflow(self, input_data: Any, agent_id: str = None) -> Dict[str, Any]:
        """รัน workflow"""
        if not agent_id:
            agent_id = list(self.agents.keys())[0] if self.agents else None
        
        if not agent_id:
            return {"error": "No agent available"}
        
        agent = self.agents[agent_id]
        
        # สร้างข้อความ
        message = {
            "content": str(input_data),
            "timestamp": time.time(),
            "tools": []
        }
        
        # ประมวลผล
        result = await agent.process(message)
        
        # เก็บประวัติ
        self.workflow_history.append(result)
        
        return result
    
    def get_system_status(self) -> Dict[str, Any]:
        """สถานะของระบบ"""
        return {
            "total_agents": len(self.agents),
            "available_tools": len(self.tool_registry.list_tools()),
            "genai_toolbox_available": self.tool_registry.genai_client is not None,
            "perplexity_ai_available": self.tool_registry.perplexity_client is not None,
            "workflow_history_count": len(self.workflow_history)
        }
    
    def export_config(self, filename: str = "integrated_system_config.json"):
        """ส่งออกการตั้งค่า"""
        config = {
            "agents": {
                agent_id: {
                    "type": agent.agent_type,
                    "capabilities": agent.get_capabilities(),
                    "config": agent.config
                }
                for agent_id, agent in self.agents.items()
            },
            "tools": {
                tool_name: {
                    "type": tool.tool_type.value,
                    "description": tool.description,
                    "enabled": tool.enabled
                }
                for tool_name, tool in self.tool_registry.tools.items()
            },
            "system_status": self.get_system_status()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Configuration exported to {filename}")

async def main():
    """ฟังก์ชันหลักสำหรับทดสอบ"""
    print("🚀 Integrated Agent System")
    print("=" * 50)
    
    # สร้าง orchestrator
    orchestrator = IntegratedOrchestrator()
    
    # สร้าง agents
    tools_agent = orchestrator.create_agent("tools_agent", "tools", {
        "model": "claude-3-5-sonnet-20241022",
        "temperature": 0.7
    })
    
    analysis_agent = orchestrator.create_agent("analysis_agent", "analysis", {
        "model": "sonar-small-online",
        "temperature": 0.3
    })
    
    # ทดสอบ workflow
    test_inputs = [
        "Analyze this text for sentiment and structure",
        "Search for information about AI agents",
        "Generate Python code for a simple calculator",
        "Find the latest news about machine learning"
    ]
    
    for i, test_input in enumerate(test_inputs, 1):
        print(f"\n📝 Test {i}: {test_input}")
        print("-" * 40)
        
        result = await orchestrator.run_workflow(test_input, "tools_agent")
        
        print(f"✅ Workflow completed")
        print(f"🤖 Agent: {result['agent_id']}")
        print(f"📊 Results: {len(result['results'])} tools executed")
        
        for tool_name, tool_result in result['results'].items():
            if "error" not in tool_result:
                print(f"  ✅ {tool_name}: Success")
            else:
                print(f"  ❌ {tool_name}: {tool_result['error']}")
    
    # แสดงสถานะระบบ
    print(f"\n📊 System Status:")
    status = orchestrator.get_system_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    # ส่งออกการตั้งค่า
    orchestrator.export_config("integrated_system_config.json")
    
    print(f"\n🎉 All tests completed!")
    print(f"📁 Configuration saved to integrated_system_config.json")

if __name__ == "__main__":
    asyncio.run(main())
