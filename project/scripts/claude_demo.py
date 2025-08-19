#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Claude Demo Script
ตัวอย่างการใช้งาน Claude กับ dataset ที่สร้างขึ้น
"""

import json
import os
import sys
from typing import List, Dict, Any
from pathlib import Path

# ตรวจสอบ API key
def check_api_key():
    """ตรวจสอบว่ามี API key หรือไม่"""
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found!")
        print("Please set your API key:")
        print("  Windows: set ANTHROPIC_API_KEY=your-key-here")
        print("  Linux/Mac: export ANTHROPIC_API_KEY=your-key-here")
        return False
    return True

def load_dataset(file_path: str) -> List[Dict[str, Any]]:
    """โหลด dataset จาก JSONL file"""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line.strip()))
    return data

def demo_claude_usage():
    """ตัวอย่างการใช้งาน Claude"""
    if not check_api_key():
        return
    
    try:
        from anthropic import Anthropic
        
        # ตั้งค่า client
        client = Anthropic()
        
        # โหลด dataset
        dataset_file = "data/test.jsonl"
        if not os.path.exists(dataset_file):
            print(f"❌ Dataset file not found: {dataset_file}")
            print("Please run claude_setup.py first")
            return
        
        data = load_dataset(dataset_file)
        print(f"📊 Loaded {len(data)} test samples")
        
        # ทดสอบกับ 3 ตัวอย่างแรก
        for i, item in enumerate(data[:3]):
            instruction = item.get('input', '')
            expected = item.get('output', '')
            
            print(f"\n{'='*60}")
            print(f"Sample {i+1}")
            print(f"{'='*60}")
            print(f"Instruction: {instruction}")
            print(f"Expected: {expected}")
            
            try:
                # ส่งคำขอไปยัง Claude
                response = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1024,
                    messages=[{"role": "user", "content": instruction}]
                )
                
                claude_response = response.content[0].text
                print(f"Claude: {claude_response}")
                
                # เปรียบเทียบความยาว
                expected_words = len(expected.split())
                actual_words = len(claude_response.split())
                print(f"Length comparison: Expected {expected_words} words, Claude {actual_words} words")
                
            except Exception as e:
                print(f"❌ Error calling Claude: {e}")
        
        print(f"\n{'='*60}")
        print("Demo completed!")
        
    except ImportError:
        print("❌ Anthropic library not installed!")
        print("Please run: pip install anthropic")

def create_sample_responses():
    """สร้างตัวอย่าง responses สำหรับ evaluation"""
    if not check_api_key():
        return
    
    try:
        from anthropic import Anthropic
        import time
        
        client = Anthropic()
        
        # โหลด test data
        test_file = "data/test.jsonl"
        if not os.path.exists(test_file):
            print(f"❌ Test file not found: {test_file}")
            return
        
        test_data = load_dataset(test_file)
        print(f"📊 Processing {len(test_data)} test samples...")
        
        responses = []
        
        for i, item in enumerate(test_data):
            instruction = item.get('input', '')
            
            try:
                response = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1024,
                    messages=[{"role": "user", "content": instruction}]
                )
                
                responses.append({
                    'id': item.get('id', f'sample_{i}'),
                    'input': instruction,
                    'expected': item.get('output', ''),
                    'response': response.content[0].text,
                    'timestamp': time.time()
                })
                
                print(f"  Processed {i+1}/{len(test_data)}")
                
                # Rate limiting
                time.sleep(0.5)
                
            except Exception as e:
                print(f"❌ Error processing sample {i}: {e}")
                continue
        
        # บันทึก responses
        output_file = "claude_responses.jsonl"
        with open(output_file, 'w', encoding='utf-8') as f:
            for response in responses:
                f.write(json.dumps(response, ensure_ascii=False) + '\n')
        
        print(f"✅ Generated {len(responses)} responses -> {output_file}")
        
        # รัน evaluation
        if responses:
            print("\n🔍 Running evaluation...")
            os.system(f"python scripts/claude_eval.py {test_file} {output_file}")
        
    except ImportError:
        print("❌ Anthropic library not installed!")

def main():
    """Main function"""
    print("🤖 Claude Demo Script")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python claude_demo.py demo     - Run interactive demo")
        print("  python claude_demo.py generate - Generate responses for evaluation")
        return
    
    command = sys.argv[1]
    
    if command == "demo":
        demo_claude_usage()
    elif command == "generate":
        create_sample_responses()
    else:
        print(f"❌ Unknown command: {command}")

if __name__ == "__main__":
    main()
