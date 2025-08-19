#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Claude Code Setup and Configuration
ตั้งค่าและใช้งาน Claude Code กับ dataset ที่สร้างขึ้น
"""

import json
import os
import sys
from typing import List, Dict, Any, Optional
from pathlib import Path

class ClaudeCodeSetup:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.config_dir = self.project_root / "config"
        self.data_dir = self.project_root / "data"
        self.scripts_dir = self.project_root / "scripts"
        
        # สร้างโฟลเดอร์ที่จำเป็น
        self.config_dir.mkdir(exist_ok=True)
        self.data_dir.mkdir(exist_ok=True)
        
    def create_claude_config(self) -> Dict[str, Any]:
        """สร้าง Claude configuration"""
        config = {
            "claude_version": "3.5-sonnet",
            "model_settings": {
                "max_tokens": 4096,
                "temperature": 0.7,
                "top_p": 0.9,
                "anthropic_version": "2023-06-01"
            },
            "dataset_config": {
                "input_format": "jsonl",
                "output_format": "jsonl",
                "validation_split": 0.1,
                "test_split": 0.1
            },
            "evaluation_metrics": [
                "accuracy",
                "completeness", 
                "relevance",
                "coherence",
                "helpfulness"
            ],
            "prompt_templates": {
                "instruction_following": "You are a helpful AI assistant. Please respond to the following instruction: {input}",
                "code_generation": "Write code to solve the following problem: {input}",
                "text_analysis": "Analyze the following text and provide insights: {input}",
                "qa": "Answer the following question: {input}"
            }
        }
        
        config_file = self.config_dir / "claude_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Claude config created: {config_file}")
        return config
    
    def setup_dataset_splits(self, dataset_file: str) -> Dict[str, str]:
        """แบ่ง dataset เป็น train/validation/test"""
        print(f"📊 Setting up dataset splits from {dataset_file}...")
        
        # โหลด dataset
        data = []
        with open(dataset_file, 'r', encoding='utf-8') as f:
            for line in f:
                data.append(json.loads(line.strip()))
        
        total = len(data)
        val_size = int(total * 0.1)
        test_size = int(total * 0.1)
        train_size = total - val_size - test_size
        
        # แบ่งข้อมูล
        train_data = data[:train_size]
        val_data = data[train_size:train_size + val_size]
        test_data = data[train_size + val_size:]
        
        # บันทึกไฟล์
        splits = {}
        for name, split_data in [("train", train_data), ("val", val_data), ("test", test_data)]:
            output_file = self.data_dir / f"{name}.jsonl"
            with open(output_file, 'w', encoding='utf-8') as f:
                for item in split_data:
                    f.write(json.dumps(item, ensure_ascii=False) + '\n')
            splits[name] = str(output_file)
            print(f"  {name}: {len(split_data)} pairs -> {output_file}")
        
        return splits
    
    def create_evaluation_script(self) -> str:
        """สร้างสคริปต์สำหรับประเมิน Claude responses"""
        script_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Claude Response Evaluation Script
ประเมินคุณภาพการตอบกลับของ Claude
"""

import json
import sys
from typing import Dict, List, Any
import re

def evaluate_response(instruction: str, expected: str, actual: str) -> Dict[str, float]:
    """ประเมินคุณภาพการตอบกลับ"""
    scores = {}
    
    # 1. Completeness (ความครบถ้วน)
    expected_words = len(expected.split())
    actual_words = len(actual.split())
    if expected_words > 0:
        completeness = min(actual_words / expected_words, 1.0)
    else:
        completeness = 1.0 if actual_words > 0 else 0.0
    scores['completeness'] = completeness
    
    # 2. Relevance (ความเกี่ยวข้อง)
    # ตรวจสอบคำสำคัญใน instruction ที่ควรปรากฏใน response
    instruction_keywords = set(re.findall(r'\\b\\w+\\b', instruction.lower()))
    response_keywords = set(re.findall(r'\\b\\w+\\b', actual.lower()))
    if instruction_keywords:
        relevance = len(instruction_keywords & response_keywords) / len(instruction_keywords)
    else:
        relevance = 1.0
    scores['relevance'] = relevance
    
    # 3. Coherence (ความสอดคล้อง)
    # ตรวจสอบความยาวและโครงสร้าง
    if actual_words >= 10 and '.' in actual:
        coherence = 1.0
    elif actual_words >= 5:
        coherence = 0.7
    else:
        coherence = 0.3
    scores['coherence'] = coherence
    
    # 4. Helpfulness (ความช่วยเหลือ)
    # ตรวจสอบว่ามีคำที่แสดงความช่วยเหลือ
    helpful_words = ['help', 'assist', 'guide', 'explain', 'show', 'provide', 'suggest']
    helpful_count = sum(1 for word in helpful_words if word in actual.lower())
    helpfulness = min(helpful_count / 2, 1.0)
    scores['helpfulness'] = helpfulness
    
    # 5. Overall score
    scores['overall'] = sum(scores.values()) / len(scores)
    
    return scores

def main():
    if len(sys.argv) != 3:
        print("Usage: python claude_eval.py <test_data.jsonl> <claude_responses.jsonl>")
        sys.exit(1)
    
    test_file = sys.argv[1]
    responses_file = sys.argv[2]
    
    # โหลดข้อมูล
    test_data = []
    with open(test_file, 'r', encoding='utf-8') as f:
        for line in f:
            test_data.append(json.loads(line.strip()))
    
    responses = []
    with open(responses_file, 'r', encoding='utf-8') as f:
        for line in f:
            responses.append(json.loads(line.strip()))
    
    # ประเมิน
    total_scores = {'completeness': 0, 'relevance': 0, 'coherence': 0, 'helpfulness': 0, 'overall': 0}
    
    for i, (test_item, response_item) in enumerate(zip(test_data, responses)):
        instruction = test_item.get('input', '')
        expected = test_item.get('output', '')
        actual = response_item.get('response', '')
        
        scores = evaluate_response(instruction, expected, actual)
        
        for metric, score in scores.items():
            total_scores[metric] += score
        
        if i < 5:  # แสดงตัวอย่าง 5 อันแรก
            print(f"Sample {i+1}: {scores['overall']:.3f}")
    
    # คำนวณค่าเฉลี่ย
    n = len(test_data)
    avg_scores = {metric: score/n for metric, score in total_scores.items()}
    
    print("\\n📊 EVALUATION RESULTS:")
    print("=" * 40)
    for metric, score in avg_scores.items():
        print(f"{metric:12}: {score:.3f}")
    
    # บันทึกผลลัพธ์
    results = {
        'total_samples': n,
        'average_scores': avg_scores,
        'evaluation_timestamp': str(datetime.now())
    }
    
    with open('evaluation_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\\n💾 Results saved to evaluation_results.json")

if __name__ == "__main__":
    from datetime import datetime
    main()
'''
        
        script_file = self.scripts_dir / "claude_eval.py"
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        print(f"✅ Evaluation script created: {script_file}")
        return str(script_file)
    
    def create_prompt_templates(self) -> str:
        """สร้าง prompt templates สำหรับ Claude"""
        templates = {
            "system_prompts": {
                "general": "You are Claude, an AI assistant created by Anthropic. You are helpful, harmless, and honest.",
                "code": "You are Claude, an expert programmer. Write clean, efficient, and well-documented code.",
                "analysis": "You are Claude, an expert analyst. Provide clear, insightful analysis with supporting evidence.",
                "creative": "You are Claude, a creative assistant. Generate original, engaging, and imaginative content."
            },
            "user_prompts": {
                "instruction": "Please follow this instruction: {input}",
                "question": "Please answer this question: {input}",
                "code_request": "Please write code for: {input}",
                "analysis_request": "Please analyze: {input}"
            }
        }
        
        template_file = self.config_dir / "prompt_templates.json"
        with open(template_file, 'w', encoding='utf-8') as f:
            json.dump(templates, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Prompt templates created: {template_file}")
        return str(template_file)
    
    def create_usage_examples(self) -> str:
        """สร้างตัวอย่างการใช้งาน"""
        examples = {
            "basic_usage": {
                "description": "การใช้งานพื้นฐานกับ dataset",
                "code": '''
import json
from anthropic import Anthropic

# โหลด dataset
with open('data/train.jsonl', 'r') as f:
    dataset = [json.loads(line) for line in f]

# ตั้งค่า Claude
client = Anthropic(api_key="your-api-key")

# ตัวอย่างการใช้งาน
for item in dataset[:5]:
    instruction = item['input']
    expected = item['output']
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{"role": "user", "content": instruction}]
    )
    
    print(f"Instruction: {instruction}")
    print(f"Expected: {expected}")
    print(f"Claude: {response.content[0].text}")
    print("-" * 50)
'''
            },
            "batch_processing": {
                "description": "ประมวลผลแบบ batch",
                "code": '''
import json
import time
from anthropic import Anthropic

def process_batch(dataset, batch_size=10):
    client = Anthropic(api_key="your-api-key")
    results = []
    
    for i in range(0, len(dataset), batch_size):
        batch = dataset[i:i+batch_size]
        batch_results = []
        
        for item in batch:
            try:
                response = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1024,
                    messages=[{"role": "user", "content": item['input']}]
                )
                
                batch_results.append({
                    'id': item['id'],
                    'input': item['input'],
                    'expected': item['output'],
                    'response': response.content[0].text,
                    'timestamp': time.time()
                })
                
            except Exception as e:
                print(f"Error processing {item['id']}: {e}")
        
        results.extend(batch_results)
        time.sleep(1)  # Rate limiting
    
    return results

# ใช้งาน
with open('data/test.jsonl', 'r') as f:
    test_data = [json.loads(line) for line in f]

responses = process_batch(test_data)

# บันทึกผลลัพธ์
with open('claude_responses.jsonl', 'w') as f:
    for response in responses:
        f.write(json.dumps(response) + '\\n')
'''
            }
        }
        
        examples_file = self.config_dir / "usage_examples.json"
        with open(examples_file, 'w', encoding='utf-8') as f:
            json.dump(examples, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Usage examples created: {examples_file}")
        return str(examples_file)

def main():
    """Main setup function"""
    print("🚀 Claude Code Setup")
    print("=" * 50)
    
    setup = ClaudeCodeSetup()
    
    # สร้าง configuration
    config = setup.create_claude_config()
    
    # สร้าง prompt templates
    setup.create_prompt_templates()
    
    # สร้าง evaluation script
    setup.create_evaluation_script()
    
    # สร้าง usage examples
    setup.create_usage_examples()
    
    # ถ้ามี dataset file ให้แบ่ง split
    dataset_files = list(Path(".").glob("*.jsonl"))
    if dataset_files:
        print(f"\n📊 Found dataset files: {[f.name for f in dataset_files]}")
        for dataset_file in dataset_files:
            try:
                splits = setup.setup_dataset_splits(dataset_file.name)
                print(f"✅ Dataset splits created for {dataset_file.name}")
            except Exception as e:
                print(f"❌ Error processing {dataset_file.name}: {e}")
    
    print("\n🎉 Claude Code Setup Complete!")
    print("\n📁 Files created:")
    print("  - config/claude_config.json")
    print("  - config/prompt_templates.json") 
    print("  - config/usage_examples.json")
    print("  - scripts/claude_eval.py")
    print("  - data/train.jsonl, val.jsonl, test.jsonl")
    
    print("\n📋 Next steps:")
    print("  1. Install anthropic: pip install anthropic")
    print("  2. Set your API key: export ANTHROPIC_API_KEY='your-key'")
    print("  3. Run evaluation: python scripts/claude_eval.py data/test.jsonl responses.jsonl")

if __name__ == "__main__":
    main()
