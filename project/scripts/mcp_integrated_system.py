#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP Integrated System
ระบบบูรณาการ MCP (Model Context Protocol) ที่เชื่อมต่อกับเครื่องมือต่างๆ
"""

import json
import asyncio
import time
import logging
import os
import sys
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import subprocess
import aiohttp
from pathlib import Path

# ตั้งค่า logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MCPServerType(Enum):
    """ประเภทของ MCP Server"""
    PUPPETEER = "puppeteer"
    GITLAB = "gitlab"
    SLACK = "slack"
    GOOGLE_MAPS = "google_maps"
    DATABASE = "database"
    FILE_SYSTEM = "file_system"
    CUSTOM = "custom"

@dataclass
class MCPServerConfig:
    """การตั้งค่า MCP Server"""
    name: str
    server_type: MCPServerType
    command: str
    args: List[str]
    env: Dict[str, str] = None
    enabled: bool = True
    
    def __post_init__(self):
        if self.env is None:
            self.env = {}

@dataclass
class MCPTool:
    """ข้อมูลเครื่องมือ MCP"""
    name: str
    description: str
    parameters: Dict[str, Any]
    server_name: str
    enabled: bool = True

class MCPServerManager:
    """จัดการ MCP Servers"""
    
    def __init__(self):
        self.servers = {}
        self.tools = {}
        self.processes = {}
        self.setup_default_servers()
    
    def setup_default_servers(self):
        """ตั้งค่า MCP Servers เริ่มต้น"""
        
        # Puppeteer MCP Server
        self.register_server(MCPServerConfig(
            name="puppeteer",
            server_type=MCPServerType.PUPPETEER,
            command="npx",
            args=["@modelcontextprotocol/server-puppeteer"],
            env={"NODE_ENV": "production"}
        ))
        
        # GitLab MCP Server
        self.register_server(MCPServerConfig(
            name="gitlab",
            server_type=MCPServerType.GITLAB,
            command="npx",
            args=["@modelcontextprotocol/server-gitlab"],
            env={"GITLAB_TOKEN": os.getenv("GITLAB_TOKEN", "")}
        ))
        
        # Slack MCP Server
        self.register_server(MCPServerConfig(
            name="slack",
            server_type=MCPServerType.SLACK,
            command="npx",
            args=["@modelcontextprotocol/server-slack"],
            env={"SLACK_BOT_TOKEN": os.getenv("SLACK_BOT_TOKEN", "")}
        ))
        
        # Google Maps MCP Server
        self.register_server(MCPServerConfig(
            name="google_maps",
            server_type=MCPServerType.GOOGLE_MAPS,
            command="npx",
            args=["@modelcontextprotocol/server-google-maps"],
            env={"GOOGLE_MAPS_API_KEY": os.getenv("GOOGLE_MAPS_API_KEY", "")}
        ))
        
        # Database MCP Server (GenAI Toolbox)
        self.register_server(MCPServerConfig(
            name="database",
            server_type=MCPServerType.DATABASE,
            command="genai-toolbox",
            args=["serve", "--config", "tools.yaml"],
            env={"GOOGLE_APPLICATION_CREDENTIALS": os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")}
        ))
        
        # File System MCP Server
        self.register_server(MCPServerConfig(
            name="file_system",
            server_type=MCPServerType.FILE_SYSTEM,
            command="npx",
            args=["@modelcontextprotocol/server-filesystem"],
            env={"ROOT_PATH": os.getcwd()}
        ))
    
    def register_server(self, config: MCPServerConfig):
        """ลงทะเบียน MCP Server"""
        self.servers[config.name] = config
        logger.info(f"Registered MCP server: {config.name} ({config.server_type.value})")
    
    async def start_server(self, server_name: str) -> bool:
        """เริ่มต้น MCP Server"""
        if server_name not in self.servers:
            logger.error(f"Server {server_name} not found")
            return False
        
        config = self.servers[server_name]
        if not config.enabled:
            logger.warning(f"Server {server_name} is disabled")
            return False
        
        try:
            # เริ่มต้น process
            process = await asyncio.create_subprocess_exec(
                config.command,
                *config.args,
                env={**os.environ, **config.env},
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            self.processes[server_name] = process
            logger.info(f"Started MCP server: {server_name}")
            
            # รอให้ server พร้อมใช้งาน
            await asyncio.sleep(2)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to start MCP server {server_name}: {e}")
            return False
    
    async def stop_server(self, server_name: str):
        """หยุด MCP Server"""
        if server_name in self.processes:
            process = self.processes[server_name]
            process.terminate()
            await process.wait()
            del self.processes[server_name]
            logger.info(f"Stopped MCP server: {server_name}")
    
    async def start_all_servers(self):
        """เริ่มต้น MCP Servers ทั้งหมด"""
        for server_name in self.servers.keys():
            await self.start_server(server_name)
    
    async def stop_all_servers(self):
        """หยุด MCP Servers ทั้งหมด"""
        for server_name in list(self.processes.keys()):
            await self.stop_server(server_name)
    
    def get_server_status(self) -> Dict[str, Any]:
        """สถานะของ MCP Servers"""
        return {
            "total_servers": len(self.servers),
            "running_servers": len(self.processes),
            "servers": {
                name: {
                    "type": config.server_type.value,
                    "enabled": config.enabled,
                    "running": name in self.processes
                }
                for name, config in self.servers.items()
            }
        }

class MCPToolRegistry:
    """Registry สำหรับเครื่องมือ MCP"""
    
    def __init__(self, server_manager: MCPServerManager):
        self.server_manager = server_manager
        self.tools = {}
        self.setup_default_tools()
    
    def setup_default_tools(self):
        """ตั้งค่าเครื่องมือเริ่มต้น"""
        
        # Puppeteer Tools
        self.register_tool(MCPTool(
            name="browser_navigate",
            description="Navigate to a URL in browser",
            parameters={
                "url": {"type": "string", "description": "URL to navigate to"}
            },
            server_name="puppeteer"
        ))
        
        self.register_tool(MCPTool(
            name="browser_screenshot",
            description="Take screenshot of current page",
            parameters={
                "path": {"type": "string", "description": "Path to save screenshot"}
            },
            server_name="puppeteer"
        ))
        
        self.register_tool(MCPTool(
            name="browser_click",
            description="Click element on page",
            parameters={
                "selector": {"type": "string", "description": "CSS selector"}
            },
            server_name="puppeteer"
        ))
        
        # GitLab Tools
        self.register_tool(MCPTool(
            name="gitlab_create_issue",
            description="Create GitLab issue",
            parameters={
                "project_id": {"type": "string", "description": "Project ID"},
                "title": {"type": "string", "description": "Issue title"},
                "description": {"type": "string", "description": "Issue description"}
            },
            server_name="gitlab"
        ))
        
        self.register_tool(MCPTool(
            name="gitlab_list_projects",
            description="List GitLab projects",
            parameters={},
            server_name="gitlab"
        ))
        
        self.register_tool(MCPTool(
            name="gitlab_create_merge_request",
            description="Create GitLab merge request",
            parameters={
                "project_id": {"type": "string", "description": "Project ID"},
                "source_branch": {"type": "string", "description": "Source branch"},
                "target_branch": {"type": "string", "description": "Target branch"},
                "title": {"type": "string", "description": "MR title"}
            },
            server_name="gitlab"
        ))
        
        # Slack Tools
        self.register_tool(MCPTool(
            name="slack_send_message",
            description="Send message to Slack channel",
            parameters={
                "channel": {"type": "string", "description": "Channel name or ID"},
                "message": {"type": "string", "description": "Message text"}
            },
            server_name="slack"
        ))
        
        self.register_tool(MCPTool(
            name="slack_list_channels",
            description="List Slack channels",
            parameters={},
            server_name="slack"
        ))
        
        self.register_tool(MCPTool(
            name="slack_create_channel",
            description="Create Slack channel",
            parameters={
                "name": {"type": "string", "description": "Channel name"},
                "is_private": {"type": "boolean", "description": "Private channel"}
            },
            server_name="slack"
        ))
        
        # Google Maps Tools
        self.register_tool(MCPTool(
            name="maps_get_directions",
            description="Get directions between locations",
            parameters={
                "origin": {"type": "string", "description": "Origin address"},
                "destination": {"type": "string", "description": "Destination address"},
                "mode": {"type": "string", "description": "Travel mode (driving, walking, transit)"}
            },
            server_name="google_maps"
        ))
        
        self.register_tool(MCPTool(
            name="maps_place_search",
            description="Search for places",
            parameters={
                "query": {"type": "string", "description": "Search query"},
                "location": {"type": "string", "description": "Location to search around"}
            },
            server_name="google_maps"
        ))
        
        self.register_tool(MCPTool(
            name="maps_place_details",
            description="Get place details",
            parameters={
                "place_id": {"type": "string", "description": "Google Place ID"}
            },
            server_name="google_maps"
        ))
        
        # Database Tools
        self.register_tool(MCPTool(
            name="database_query",
            description="Execute SQL query",
            parameters={
                "query": {"type": "string", "description": "SQL query"},
                "database": {"type": "string", "description": "Database name"}
            },
            server_name="database"
        ))
        
        self.register_tool(MCPTool(
            name="database_analyze",
            description="Analyze database schema",
            parameters={
                "database": {"type": "string", "description": "Database name"}
            },
            server_name="database"
        ))
        
        # File System Tools
        self.register_tool(MCPTool(
            name="file_read",
            description="Read file content",
            parameters={
                "path": {"type": "string", "description": "File path"}
            },
            server_name="file_system"
        ))
        
        self.register_tool(MCPTool(
            name="file_write",
            description="Write content to file",
            parameters={
                "path": {"type": "string", "description": "File path"},
                "content": {"type": "string", "description": "File content"}
            },
            server_name="file_system"
        ))
        
        self.register_tool(MCPTool(
            name="file_list",
            description="List files in directory",
            parameters={
                "path": {"type": "string", "description": "Directory path"}
            },
            server_name="file_system"
        ))
    
    def register_tool(self, tool: MCPTool):
        """ลงทะเบียนเครื่องมือ"""
        self.tools[tool.name] = tool
        logger.info(f"Registered MCP tool: {tool.name} (server: {tool.server_name})")
    
    def get_tool(self, name: str) -> Optional[MCPTool]:
        """ดึงเครื่องมือตามชื่อ"""
        return self.tools.get(name)
    
    def list_tools(self) -> List[str]:
        """รายการเครื่องมือทั้งหมด"""
        return list(self.tools.keys())
    
    def list_tools_by_server(self, server_name: str) -> List[str]:
        """รายการเครื่องมือตาม server"""
        return [name for name, tool in self.tools.items() if tool.server_name == server_name]
    
    async def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """รันเครื่องมือ MCP"""
        tool = self.get_tool(tool_name)
        if not tool or not tool.enabled:
            return {"error": f"Tool {tool_name} not found or disabled"}
        
        # ตรวจสอบว่า server กำลังทำงานอยู่หรือไม่
        if tool.server_name not in self.server_manager.processes:
            await self.server_manager.start_server(tool.server_name)
        
        try:
            # ส่งคำขอไปยัง MCP Server
            result = await self._send_mcp_request(tool, parameters)
            return result
            
        except Exception as e:
            logger.error(f"Error executing MCP tool {tool_name}: {e}")
            return {"error": str(e)}
    
    async def _send_mcp_request(self, tool: MCPTool, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """ส่งคำขอไปยัง MCP Server"""
        # จำลองการส่งคำขอไปยัง MCP Server
        # ในระบบจริงจะใช้ MCP protocol
        
        server_type = self.server_manager.servers[tool.server_name].server_type
        
        if server_type == MCPServerType.PUPPETEER:
            return await self._handle_puppeteer_request(tool, parameters)
        elif server_type == MCPServerType.GITLAB:
            return await self._handle_gitlab_request(tool, parameters)
        elif server_type == MCPServerType.SLACK:
            return await self._handle_slack_request(tool, parameters)
        elif server_type == MCPServerType.GOOGLE_MAPS:
            return await self._handle_google_maps_request(tool, parameters)
        elif server_type == MCPServerType.DATABASE:
            return await self._handle_database_request(tool, parameters)
        elif server_type == MCPServerType.FILE_SYSTEM:
            return await self._handle_file_system_request(tool, parameters)
        else:
            return {"error": f"Unknown server type: {server_type}"}
    
    async def _handle_puppeteer_request(self, tool: MCPTool, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """จัดการคำขอ Puppeteer"""
        if tool.name == "browser_navigate":
            url = parameters.get("url", "")
            return {"success": True, "message": f"Navigated to {url}"}
        elif tool.name == "browser_screenshot":
            path = parameters.get("path", "screenshot.png")
            return {"success": True, "message": f"Screenshot saved to {path}"}
        elif tool.name == "browser_click":
            selector = parameters.get("selector", "")
            return {"success": True, "message": f"Clicked element: {selector}"}
        return {"error": f"Unknown Puppeteer tool: {tool.name}"}
    
    async def _handle_gitlab_request(self, tool: MCPTool, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """จัดการคำขอ GitLab"""
        if tool.name == "gitlab_create_issue":
            title = parameters.get("title", "")
            return {"success": True, "message": f"Created issue: {title}"}
        elif tool.name == "gitlab_list_projects":
            return {"success": True, "projects": ["project1", "project2", "project3"]}
        elif tool.name == "gitlab_create_merge_request":
            title = parameters.get("title", "")
            return {"success": True, "message": f"Created MR: {title}"}
        return {"error": f"Unknown GitLab tool: {tool.name}"}
    
    async def _handle_slack_request(self, tool: MCPTool, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """จัดการคำขอ Slack"""
        if tool.name == "slack_send_message":
            channel = parameters.get("channel", "")
            message = parameters.get("message", "")
            return {"success": True, "message": f"Sent message to {channel}"}
        elif tool.name == "slack_list_channels":
            return {"success": True, "channels": ["general", "random", "dev"]}
        elif tool.name == "slack_create_channel":
            name = parameters.get("name", "")
            return {"success": True, "message": f"Created channel: {name}"}
        return {"error": f"Unknown Slack tool: {tool.name}"}
    
    async def _handle_google_maps_request(self, tool: MCPTool, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """จัดการคำขอ Google Maps"""
        if tool.name == "maps_get_directions":
            origin = parameters.get("origin", "")
            destination = parameters.get("destination", "")
            return {"success": True, "directions": f"Route from {origin} to {destination}"}
        elif tool.name == "maps_place_search":
            query = parameters.get("query", "")
            return {"success": True, "places": [f"Place 1 for {query}", f"Place 2 for {query}"]}
        elif tool.name == "maps_place_details":
            place_id = parameters.get("place_id", "")
            return {"success": True, "details": f"Details for place {place_id}"}
        return {"error": f"Unknown Google Maps tool: {tool.name}"}
    
    async def _handle_database_request(self, tool: MCPTool, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """จัดการคำขอ Database"""
        if tool.name == "database_query":
            query = parameters.get("query", "")
            return {"success": True, "result": f"Query result: {query}"}
        elif tool.name == "database_analyze":
            database = parameters.get("database", "")
            return {"success": True, "schema": f"Schema for {database}"}
        return {"error": f"Unknown Database tool: {tool.name}"}
    
    async def _handle_file_system_request(self, tool: MCPTool, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """จัดการคำขอ File System"""
        if tool.name == "file_read":
            path = parameters.get("path", "")
            return {"success": True, "content": f"Content of {path}"}
        elif tool.name == "file_write":
            path = parameters.get("path", "")
            content = parameters.get("content", "")
            return {"success": True, "message": f"Written to {path}"}
        elif tool.name == "file_list":
            path = parameters.get("path", "")
            return {"success": True, "files": ["file1.txt", "file2.py", "dir1/"]}
        return {"error": f"Unknown File System tool: {tool.name}"}

class MCPEnhancedAgent:
    """Agent ที่ใช้ MCP Tools"""
    
    def __init__(self, agent_id: str, agent_type: str, config: Dict[str, Any] = None):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.config = config or {}
        self.server_manager = MCPServerManager()
        self.tool_registry = MCPToolRegistry(self.server_manager)
        self.memory = {}
    
    async def initialize(self):
        """เริ่มต้น agent"""
        await self.server_manager.start_all_servers()
        logger.info(f"Initialized agent: {self.agent_id}")
    
    async def process(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """ประมวลผลข้อความ"""
        content = message.get("content", "")
        tools_needed = message.get("tools", [])
        
        results = {}
        
        # วิเคราะห์ข้อความเพื่อเลือกเครื่องมือ
        if "browser" in content.lower() or "navigate" in content.lower():
            tool_result = await self.tool_registry.execute_tool("browser_navigate", {"url": content})
            results["browser_action"] = tool_result
        
        if "gitlab" in content.lower() or "issue" in content.lower():
            tool_result = await self.tool_registry.execute_tool("gitlab_create_issue", {
                "title": "Auto-generated issue",
                "description": content
            })
            results["gitlab_action"] = tool_result
        
        if "slack" in content.lower() or "message" in content.lower():
            tool_result = await self.tool_registry.execute_tool("slack_send_message", {
                "channel": "general",
                "message": content
            })
            results["slack_action"] = tool_result
        
        if "map" in content.lower() or "direction" in content.lower():
            tool_result = await self.tool_registry.execute_tool("maps_get_directions", {
                "origin": "Current location",
                "destination": content
            })
            results["maps_action"] = tool_result
        
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
        return self.tool_registry.list_tools()
    
    async def cleanup(self):
        """ทำความสะอาด resources"""
        await self.server_manager.stop_all_servers()
        logger.info(f"Cleaned up agent: {self.agent_id}")

class MCPIntegratedOrchestrator:
    """ระบบจัดการ Agent ที่บูรณาการ MCP"""
    
    def __init__(self):
        self.agents = {}
        self.workflow_history = []
    
    def create_agent(self, agent_id: str, agent_type: str, config: Dict[str, Any] = None) -> MCPEnhancedAgent:
        """สร้าง agent ใหม่"""
        agent = MCPEnhancedAgent(agent_id, agent_type, config)
        self.agents[agent_id] = agent
        return agent
    
    async def initialize_system(self):
        """เริ่มต้นระบบ"""
        for agent in self.agents.values():
            await agent.initialize()
        logger.info("MCP Integrated System initialized")
    
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
        total_tools = sum(len(agent.tool_registry.list_tools()) for agent in self.agents.values())
        server_status = self.agents[list(self.agents.keys())[0]].server_manager.get_server_status() if self.agents else {}
        
        return {
            "total_agents": len(self.agents),
            "total_tools": total_tools,
            "workflow_history_count": len(self.workflow_history),
            "server_status": server_status
        }
    
    def export_config(self, filename: str = "mcp_integrated_config.json"):
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
            "servers": {
                name: {
                    "type": config.server_type.value,
                    "enabled": config.enabled,
                    "command": config.command,
                    "args": config.args
                }
                for name, config in self.agents[list(self.agents.keys())[0]].server_manager.servers.items() if self.agents
            },
            "tools": {
                tool_name: {
                    "description": tool.description,
                    "server": tool.server_name,
                    "enabled": tool.enabled
                }
                for tool_name, tool in self.agents[list(self.agents.keys())[0]].tool_registry.tools.items() if self.agents
            },
            "system_status": self.get_system_status()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Configuration exported to {filename}")
    
    async def cleanup(self):
        """ทำความสะอาดระบบ"""
        for agent in self.agents.values():
            await agent.cleanup()
        logger.info("MCP Integrated System cleaned up")

async def main():
    """ฟังก์ชันหลักสำหรับทดสอบ"""
    print("🚀 MCP Integrated System")
    print("=" * 50)
    
    # สร้าง orchestrator
    orchestrator = MCPIntegratedOrchestrator()
    
    # สร้าง agents
    browser_agent = orchestrator.create_agent("browser_agent", "automation", {
        "model": "claude-3-5-sonnet-20241022",
        "temperature": 0.7
    })
    
    project_agent = orchestrator.create_agent("project_agent", "management", {
        "model": "sonar-small-online",
        "temperature": 0.3
    })
    
    # เริ่มต้นระบบ
    await orchestrator.initialize_system()
    
    # ทดสอบ workflow
    test_inputs = [
        "Navigate to https://github.com and take a screenshot",
        "Create a GitLab issue for bug tracking",
        "Send a message to Slack channel about project update",
        "Get directions from Bangkok to Chiang Mai",
        "Query database for user statistics",
        "Read and analyze project files"
    ]
    
    for i, test_input in enumerate(test_inputs, 1):
        print(f"\n📝 Test {i}: {test_input}")
        print("-" * 40)
        
        result = await orchestrator.run_workflow(test_input, "browser_agent")
        
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
        if key != "server_status":
            print(f"  {key}: {value}")
    
    print(f"\n🔧 Server Status:")
    server_status = status.get("server_status", {})
    for server_name, server_info in server_status.get("servers", {}).items():
        status_icon = "🟢" if server_info["running"] else "🔴"
        print(f"  {status_icon} {server_name}: {server_info['type']}")
    
    # ส่งออกการตั้งค่า
    orchestrator.export_config("mcp_integrated_config.json")
    
    # ทำความสะอาด
    await orchestrator.cleanup()
    
    print(f"\n🎉 All tests completed!")
    print(f"📁 Configuration saved to mcp_integrated_config.json")

if __name__ == "__main__":
    asyncio.run(main())
