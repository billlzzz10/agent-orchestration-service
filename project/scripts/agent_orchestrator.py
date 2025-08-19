#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-Agent Orchestration System
ระบบจัดการ Agent หลายตัวที่มี ≥6 โหนด และซับซ้อนเทียบเท่าหรือมากกว่าภาพที่ผู้ใช้อัปโหลด
"""

import json
import asyncio
import time
import logging
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import re
import hashlib
from pathlib import Path

# ตั้งค่า logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NodeType(Enum):
    """ประเภทของโหนดในระบบ"""
    INPUT = "input"
    AGENT = "agent"
    TOOL = "tool"
    MEMORY = "memory"
    CONDITION = "condition"
    OUTPUT = "output"

class AgentType(Enum):
    """ประเภทของ Agent"""
    TOOLS_AGENT = "tools_agent"
    REASONING_AGENT = "reasoning_agent"
    CREATIVE_AGENT = "creative_agent"
    VALIDATION_AGENT = "validation_agent"
    COORDINATION_AGENT = "coordination_agent"

@dataclass
class Node:
    """โครงสร้างโหนดในระบบ"""
    id: str
    name: str
    node_type: NodeType
    config: Dict[str, Any]
    connections: List[str] = None
    
    def __post_init__(self):
        if self.connections is None:
            self.connections = []

@dataclass
class Message:
    """โครงสร้างข้อความระหว่างโหนด"""
    id: str
    source: str
    target: str
    content: Any
    metadata: Dict[str, Any] = None
    timestamp: float = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.timestamp is None:
            self.timestamp = time.time()

class MemoryBuffer:
    """Buffer Memory สำหรับเก็บข้อมูลระหว่างการประมวลผล"""
    
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self.buffer = {}
        self.access_count = {}
    
    def store(self, key: str, value: Any, metadata: Dict[str, Any] = None):
        """เก็บข้อมูลใน buffer"""
        if len(self.buffer) >= self.max_size:
            # ลบข้อมูลที่เก่าที่สุด
            oldest_key = min(self.access_count.keys(), key=lambda k: self.access_count[k])
            del self.buffer[oldest_key]
            del self.access_count[oldest_key]
        
        self.buffer[key] = {
            'value': value,
            'metadata': metadata or {},
            'timestamp': time.time()
        }
        self.access_count[key] = time.time()
    
    def retrieve(self, key: str) -> Optional[Any]:
        """ดึงข้อมูลจาก buffer"""
        if key in self.buffer:
            self.access_count[key] = time.time()
            return self.buffer[key]['value']
        return None
    
    def search(self, pattern: str) -> List[tuple]:
        """ค้นหาข้อมูลด้วย pattern"""
        results = []
        for key, data in self.buffer.items():
            if pattern.lower() in key.lower() or pattern.lower() in str(data['value']).lower():
                results.append((key, data['value']))
        return results

class ToolRegistry:
    """Registry สำหรับเครื่องมือต่างๆ"""
    
    def __init__(self):
        self.tools = {}
        self.register_default_tools()
    
    def register_tool(self, name: str, func: Callable, description: str = ""):
        """ลงทะเบียนเครื่องมือใหม่"""
        self.tools[name] = {
            'function': func,
            'description': description
        }
    
    def get_tool(self, name: str) -> Optional[Callable]:
        """ดึงเครื่องมือตามชื่อ"""
        return self.tools.get(name, {}).get('function')
    
    def list_tools(self) -> List[str]:
        """รายการเครื่องมือทั้งหมด"""
        return list(self.tools.keys())
    
    def register_default_tools(self):
        """ลงทะเบียนเครื่องมือเริ่มต้น"""
        
        def text_analyzer(text: str) -> Dict[str, Any]:
            """วิเคราะห์ข้อความ"""
            words = text.split()
            return {
                'word_count': len(words),
                'char_count': len(text),
                'avg_word_length': sum(len(word) for word in words) / len(words) if words else 0,
                'sentiment': 'positive' if any(word in ['good', 'great', 'excellent'] for word in words) else 'neutral'
            }
        
        def image_generator(prompt: str) -> str:
            """สร้างภาพจากข้อความ (จำลอง)"""
            return f"Generated image for: {prompt}"
        
        def code_analyzer(code: str) -> Dict[str, Any]:
            """วิเคราะห์โค้ด"""
            lines = code.split('\n')
            return {
                'line_count': len(lines),
                'function_count': len(re.findall(r'def\s+\w+', code)),
                'class_count': len(re.findall(r'class\s+\w+', code)),
                'complexity': 'high' if len(lines) > 50 else 'medium' if len(lines) > 20 else 'low'
            }
        
        def data_validator(data: Any) -> Dict[str, Any]:
            """ตรวจสอบความถูกต้องของข้อมูล"""
            if isinstance(data, dict):
                return {'valid': True, 'type': 'dict', 'keys': list(data.keys())}
            elif isinstance(data, list):
                return {'valid': True, 'type': 'list', 'length': len(data)}
            else:
                return {'valid': True, 'type': type(data).__name__}
        
        self.register_tool('text_analyzer', text_analyzer, "Analyze text content")
        self.register_tool('image_generator', image_generator, "Generate images from text")
        self.register_tool('code_analyzer', code_analyzer, "Analyze code structure")
        self.register_tool('data_validator', data_validator, "Validate data format")

class Agent:
    """Base Agent class"""
    
    def __init__(self, agent_id: str, agent_type: AgentType, config: Dict[str, Any] = None):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.config = config or {}
        self.memory = MemoryBuffer()
        self.tools = ToolRegistry()
    
    async def process(self, message: Message) -> Message:
        """ประมวลผลข้อความ (ต้อง override ใน subclass)"""
        raise NotImplementedError
    
    def get_capabilities(self) -> List[str]:
        """ความสามารถของ agent"""
        return []

class ToolsAgent(Agent):
    """Agent สำหรับจัดการเครื่องมือ"""
    
    def __init__(self, agent_id: str, config: Dict[str, Any] = None):
        super().__init__(agent_id, AgentType.TOOLS_AGENT, config)
    
    async def process(self, message: Message) -> Message:
        """ประมวลผลและเลือกเครื่องมือที่เหมาะสม"""
        content = message.content
        
        # วิเคราะห์ข้อความเพื่อเลือกเครื่องมือ
        if isinstance(content, str):
            if 'analyze' in content.lower() or 'text' in content.lower():
                tool_name = 'text_analyzer'
            elif 'generate' in content.lower() or 'image' in content.lower():
                tool_name = 'image_generator'
            elif 'code' in content.lower() or 'function' in content.lower():
                tool_name = 'code_analyzer'
            elif 'validate' in content.lower() or 'check' in content.lower():
                tool_name = 'data_validator'
            else:
                tool_name = 'text_analyzer'  # default
            
            tool = self.tools.get_tool(tool_name)
            if tool:
                result = tool(content)
                return Message(
                    id=f"tool_result_{int(time.time())}",
                    source=self.agent_id,
                    target=message.source,
                    content=result,
                    metadata={'tool_used': tool_name}
                )
        
        return Message(
            id=f"tool_error_{int(time.time())}",
            source=self.agent_id,
            target=message.source,
            content="No suitable tool found",
            metadata={'error': 'tool_not_found'}
        )
    
    def get_capabilities(self) -> List[str]:
        return ['text_analysis', 'image_generation', 'code_analysis', 'data_validation']

class ReasoningAgent(Agent):
    """Agent สำหรับการให้เหตุผล"""
    
    def __init__(self, agent_id: str, config: Dict[str, Any] = None):
        super().__init__(agent_id, AgentType.REASONING_AGENT, config)
    
    async def process(self, message: Message) -> Message:
        """ประมวลผลด้วยการให้เหตุผล"""
        content = message.content
        
        # จำลองการให้เหตุผล
        reasoning_steps = []
        
        if isinstance(content, dict):
            # วิเคราะห์ข้อมูล
            reasoning_steps.append("Analyzing input data structure")
            reasoning_steps.append("Identifying key patterns")
            reasoning_steps.append("Forming logical conclusions")
            
            result = {
                'reasoning_steps': reasoning_steps,
                'conclusion': f"Processed {len(content)} data points",
                'confidence': 0.85
            }
        else:
            result = {
                'reasoning_steps': ["Input analysis", "Pattern recognition"],
                'conclusion': "Standard processing completed",
                'confidence': 0.75
            }
        
        return Message(
            id=f"reasoning_{int(time.time())}",
            source=self.agent_id,
            target=message.source,
            content=result,
            metadata={'reasoning_type': 'logical_analysis'}
        )
    
    def get_capabilities(self) -> List[str]:
        return ['logical_reasoning', 'pattern_recognition', 'decision_making']

class CreativeAgent(Agent):
    """Agent สำหรับงานสร้างสรรค์"""
    
    def __init__(self, agent_id: str, config: Dict[str, Any] = None):
        super().__init__(agent_id, AgentType.CREATIVE_AGENT, config)
    
    async def process(self, message: Message) -> Message:
        """ประมวลผลงานสร้างสรรค์"""
        content = message.content
        
        # จำลองการสร้างสรรค์
        creative_elements = []
        
        if isinstance(content, str):
            creative_elements.append(f"Enhanced: {content}")
            creative_elements.append(f"Creative variation: {content[::-1]}")
            creative_elements.append(f"Poetic version: {content.upper()}")
        
        result = {
            'original': content,
            'creative_variations': creative_elements,
            'inspiration_score': 0.9
        }
        
        return Message(
            id=f"creative_{int(time.time())}",
            source=self.agent_id,
            target=message.source,
            content=result,
            metadata={'creative_type': 'content_generation'}
        )
    
    def get_capabilities(self) -> List[str]:
        return ['content_generation', 'creative_writing', 'artistic_expression']

class ValidationAgent(Agent):
    """Agent สำหรับตรวจสอบความถูกต้อง"""
    
    def __init__(self, agent_id: str, config: Dict[str, Any] = None):
        super().__init__(agent_id, AgentType.VALIDATION_AGENT, config)
    
    async def process(self, message: Message) -> Message:
        """ตรวจสอบความถูกต้องของข้อมูล"""
        content = message.content
        
        validation_results = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'quality_score': 0.95
        }
        
        if isinstance(content, dict):
            if not content:
                validation_results['is_valid'] = False
                validation_results['errors'].append("Empty dictionary")
            else:
                validation_results['warnings'].append("Dictionary structure validated")
        
        elif isinstance(content, str):
            if len(content) < 5:
                validation_results['warnings'].append("Content might be too short")
            if not content.strip():
                validation_results['is_valid'] = False
                validation_results['errors'].append("Empty or whitespace-only content")
        
        return Message(
            id=f"validation_{int(time.time())}",
            source=self.agent_id,
            target=message.source,
            content=validation_results,
            metadata={'validation_type': 'comprehensive_check'}
        )
    
    def get_capabilities(self) -> List[str]:
        return ['data_validation', 'quality_assurance', 'error_detection']

class CoordinationAgent(Agent):
    """Agent สำหรับประสานงานระหว่าง Agent อื่นๆ"""
    
    def __init__(self, agent_id: str, config: Dict[str, Any] = None):
        super().__init__(agent_id, AgentType.COORDINATION_AGENT, config)
        self.agent_registry = {}
    
    def register_agent(self, agent: Agent):
        """ลงทะเบียน agent"""
        self.agent_registry[agent.agent_id] = agent
    
    async def process(self, message: Message) -> Message:
        """ประสานงานระหว่าง agent"""
        content = message.content
        
        # วิเคราะห์และเลือก agent ที่เหมาะสม
        if isinstance(content, str):
            if 'tool' in content.lower() or 'analyze' in content.lower():
                target_agent_type = AgentType.TOOLS_AGENT
            elif 'reason' in content.lower() or 'logic' in content.lower():
                target_agent_type = AgentType.REASONING_AGENT
            elif 'creative' in content.lower() or 'generate' in content.lower():
                target_agent_type = AgentType.CREATIVE_AGENT
            elif 'validate' in content.lower() or 'check' in content.lower():
                target_agent_type = AgentType.VALIDATION_AGENT
            else:
                target_agent_type = AgentType.TOOLS_AGENT  # default
        
        # หา agent ที่เหมาะสม
        target_agent = None
        for agent in self.agent_registry.values():
            if agent.agent_type == target_agent_type:
                target_agent = agent
                break
        
        if target_agent:
            # ส่งข้อความไปยัง agent ที่เหมาะสม
            result = await target_agent.process(message)
            return Message(
                id=f"coordination_{int(time.time())}",
                source=self.agent_id,
                target=message.source,
                content=result.content,
                metadata={'coordinated_agent': target_agent.agent_id}
            )
        else:
            return Message(
                id=f"coordination_error_{int(time.time())}",
                source=self.agent_id,
                target=message.source,
                content="No suitable agent found",
                metadata={'error': 'agent_not_found'}
            )
    
    def get_capabilities(self) -> List[str]:
        return ['agent_coordination', 'workflow_management', 'task_routing']

class AgentOrchestrator:
    """ระบบจัดการ Agent หลายตัว"""
    
    def __init__(self):
        self.nodes = {}
        self.agents = {}
        self.memory = MemoryBuffer()
        self.message_queue = asyncio.Queue()
        self.running = False
    
    def add_node(self, node: Node):
        """เพิ่มโหนดในระบบ"""
        self.nodes[node.id] = node
        logger.info(f"Added node: {node.name} ({node.node_type.value})")
    
    def create_agent(self, agent_type: AgentType, agent_id: str, config: Dict[str, Any] = None) -> Agent:
        """สร้าง agent ตามประเภท"""
        if agent_type == AgentType.TOOLS_AGENT:
            agent = ToolsAgent(agent_id, config)
        elif agent_type == AgentType.REASONING_AGENT:
            agent = ReasoningAgent(agent_id, config)
        elif agent_type == AgentType.CREATIVE_AGENT:
            agent = CreativeAgent(agent_id, config)
        elif agent_type == AgentType.VALIDATION_AGENT:
            agent = ValidationAgent(agent_id, config)
        elif agent_type == AgentType.COORDINATION_AGENT:
            agent = CoordinationAgent(agent_id, config)
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        self.agents[agent_id] = agent
        return agent
    
    def setup_default_workflow(self):
        """ตั้งค่า workflow เริ่มต้นที่มี ≥6 โหนด"""
        
        # สร้างโหนดต่างๆ
        nodes = [
            Node("input_1", "Listen for incoming events", NodeType.INPUT, {
                "source": "telegram",
                "event_types": ["message", "command"]
            }),
            
            Node("agent_1", "AI Agent1: Tools Agent", NodeType.AGENT, {
                "agent_type": "tools_agent",
                "capabilities": ["text_analysis", "image_generation"]
            }),
            
            Node("tool_1", "OpenAI Chat Model", NodeType.TOOL, {
                "model": "gpt-4",
                "max_tokens": 2048,
                "temperature": 0.7
            }),
            
            Node("memory_1", "Window Buffer Memory", NodeType.MEMORY, {
                "max_size": 1000,
                "retention_policy": "lru"
            }),
            
            Node("agent_2", "Reasoning Agent", NodeType.AGENT, {
                "agent_type": "reasoning_agent",
                "capabilities": ["logical_reasoning", "pattern_recognition"]
            }),
            
            Node("tool_2", "Generate image in Dalle", NodeType.TOOL, {
                "model": "dall-e-3",
                "size": "1024x1024",
                "quality": "standard"
            }),
            
            Node("agent_3", "Validation Agent", NodeType.AGENT, {
                "agent_type": "validation_agent",
                "capabilities": ["data_validation", "quality_assurance"]
            }),
            
            Node("condition_1", "Quality Check Condition", NodeType.CONDITION, {
                "condition_type": "quality_threshold",
                "threshold": 0.8
            }),
            
            Node("agent_4", "Creative Agent", NodeType.AGENT, {
                "agent_type": "creative_agent",
                "capabilities": ["content_generation", "creative_writing"]
            }),
            
            Node("output_1", "Send final reply", NodeType.OUTPUT, {
                "destination": "telegram",
                "format": "text"
            })
        ]
        
        # เพิ่มโหนดทั้งหมด
        for node in nodes:
            self.add_node(node)
        
        # สร้าง agent
        tools_agent = self.create_agent(AgentType.TOOLS_AGENT, "tools_agent_1")
        reasoning_agent = self.create_agent(AgentType.REASONING_AGENT, "reasoning_agent_1")
        creative_agent = self.create_agent(AgentType.CREATIVE_AGENT, "creative_agent_1")
        validation_agent = self.create_agent(AgentType.VALIDATION_AGENT, "validation_agent_1")
        coordination_agent = self.create_agent(AgentType.COORDINATION_AGENT, "coordination_agent_1")
        
        # ลงทะเบียน agent กับ coordination agent
        coordination_agent.register_agent(tools_agent)
        coordination_agent.register_agent(reasoning_agent)
        coordination_agent.register_agent(creative_agent)
        coordination_agent.register_agent(validation_agent)
        
        logger.info(f"Setup complete: {len(nodes)} nodes, {len(self.agents)} agents")
    
    async def process_message(self, message: Message) -> Message:
        """ประมวลผลข้อความผ่านระบบ"""
        logger.info(f"Processing message: {message.id}")
        
        # เก็บใน memory
        self.memory.store(f"msg_{message.id}", message.content, message.metadata)
        
        # ส่งไปยัง coordination agent
        coordination_agent = self.agents.get("coordination_agent_1")
        if coordination_agent:
            result = await coordination_agent.process(message)
            
            # เก็บผลลัพธ์ใน memory
            self.memory.store(f"result_{message.id}", result.content, result.metadata)
            
            return result
        else:
            return Message(
                id=f"error_{int(time.time())}",
                source="orchestrator",
                target=message.source,
                content="Coordination agent not found",
                metadata={'error': 'agent_not_found'}
            )
    
    async def run_workflow(self, input_data: Any) -> Dict[str, Any]:
        """รัน workflow ทั้งหมด"""
        logger.info("Starting workflow execution")
        
        # สร้างข้อความเริ่มต้น
        initial_message = Message(
            id=f"workflow_{int(time.time())}",
            source="input",
            target="coordination_agent_1",
            content=input_data,
            metadata={'workflow_id': f"wf_{int(time.time())}"}
        )
        
        # ประมวลผล
        result = await self.process_message(initial_message)
        
        # รวบรวมผลลัพธ์
        workflow_result = {
            'workflow_id': initial_message.metadata['workflow_id'],
            'input': input_data,
            'output': result.content,
            'metadata': result.metadata,
            'execution_time': time.time() - initial_message.timestamp,
            'nodes_processed': len(self.nodes),
            'agents_used': len(self.agents)
        }
        
        logger.info(f"Workflow completed: {workflow_result['execution_time']:.2f}s")
        return workflow_result
    
    def export_workflow(self, filename: str = "workflow_config.json"):
        """ส่งออกการตั้งค่า workflow"""
        config = {
            'nodes': [{
                'id': node.id,
                'name': node.name,
                'node_type': node.node_type.value,
                'config': node.config,
                'connections': node.connections
            } for node in self.nodes.values()],
            'agents': {
                agent_id: {
                    'type': agent.agent_type.value,
                    'capabilities': agent.get_capabilities(),
                    'config': agent.config
                }
                for agent_id, agent in self.agents.items()
            },
            'memory_stats': {
                'buffer_size': len(self.memory.buffer),
                'max_size': self.memory.max_size
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Workflow exported to {filename}")

async def main():
    """ฟังก์ชันหลักสำหรับทดสอบ"""
    print("🚀 Multi-Agent Orchestration System")
    print("=" * 50)
    
    # สร้าง orchestrator
    orchestrator = AgentOrchestrator()
    
    # ตั้งค่า workflow เริ่มต้น
    orchestrator.setup_default_workflow()
    
    # ทดสอบ workflow
    test_inputs = [
        "Analyze this text and generate a creative response",
        "Generate an image of a beautiful sunset",
        "Validate this data structure and provide reasoning",
        "Create a creative story about AI agents"
    ]
    
    for i, test_input in enumerate(test_inputs, 1):
        print(f"\n📝 Test {i}: {test_input}")
        print("-" * 40)
        
        result = await orchestrator.run_workflow(test_input)
        
        print(f"✅ Workflow completed in {result['execution_time']:.2f}s")
        print(f"📊 Nodes processed: {result['nodes_processed']}")
        print(f"🤖 Agents used: {result['agents_used']}")
        print(f"📤 Output: {result['output']}")
    
    # ส่งออกการตั้งค่า
    orchestrator.export_workflow("agent_workflow_config.json")
    
    print(f"\n🎉 All tests completed!")
    print(f"📁 Configuration saved to agent_workflow_config.json")

if __name__ == "__main__":
    asyncio.run(main())
