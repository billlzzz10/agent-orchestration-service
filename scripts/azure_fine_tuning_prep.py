#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Azure OpenAI Fine-tuning Dataset Preparation
เตรียมข้อมูลสำหรับ fine-tuning บน Azure OpenAI
"""

import json
import logging
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional
import pandas as pd
from datasets import Dataset
import numpy as np
from sklearn.model_selection import train_test_split

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AzureFineTuningPreparator:
    """เตรียมข้อมูลสำหรับ Azure OpenAI Fine-tuning"""
    
    def __init__(self, output_dir: str = "data/azure_fine_tuning"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def load_existing_datasets(self) -> List[Dict[str, Any]]:
        """โหลดข้อมูลจาก datasets ที่มีอยู่"""
        datasets = []
        
        # โหลดจาก processed datasets
        processed_dir = Path("data/processed")
        if processed_dir.exists():
            for file_path in processed_dir.glob("*.json"):
                logger.info(f"Loading dataset: {file_path}")
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        datasets.extend(data)
                    else:
                        datasets.append(data)
        
        # โหลดจาก enhanced datasets
        enhanced_dir = Path("data/enhanced")
        if enhanced_dir.exists():
            for file_path in enhanced_dir.glob("*.json"):
                logger.info(f"Loading enhanced dataset: {file_path}")
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        datasets.extend(data)
                    else:
                        datasets.append(data)
        
        logger.info(f"Loaded {len(datasets)} total conversations")
        return datasets
    
    def convert_to_azure_format(self, conversations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """แปลงข้อมูลเป็นรูปแบบ Azure OpenAI Fine-tuning"""
        azure_format = []
        
        for conv in conversations:
            if 'conversations' in conv:
                # รูปแบบที่มี conversations array
                messages = []
                for msg in conv['conversations']:
                    role = "assistant" if msg.get('from') == 'gpt' else "user"
                    content = msg.get('value', '')
                    if content.strip():
                        messages.append({
                            "role": role,
                            "content": content
                        })
                
                if len(messages) >= 2:  # ต้องมีอย่างน้อย user และ assistant
                    azure_format.append({
                        "messages": messages
                    })
            
            elif 'instruction' in conv and 'response' in conv:
                # รูปแบบ instruction-response
                messages = [
                    {"role": "user", "content": conv['instruction']},
                    {"role": "assistant", "content": conv['response']}
                ]
                azure_format.append({
                    "messages": messages
                })
            
            elif 'prompt' in conv and 'completion' in conv:
                # รูปแบบ prompt-completion
                messages = [
                    {"role": "user", "content": conv['prompt']},
                    {"role": "assistant", "content": conv['completion']}
                ]
                azure_format.append({
                    "messages": messages
                })
        
        logger.info(f"Converted {len(azure_format)} conversations to Azure format")
        return azure_format
    
    def quality_filter(self, conversations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """กรองข้อมูลคุณภาพ"""
        filtered = []
        
        for conv in conversations:
            messages = conv.get('messages', [])
            
            # ตรวจสอบความยาว
            total_length = sum(len(msg.get('content', '')) for msg in messages)
            if total_length < 50 or total_length > 4000:
                continue
            
            # ตรวจสอบความสมดุล user/assistant
            user_msgs = [msg for msg in messages if msg.get('role') == 'user']
            assistant_msgs = [msg for msg in messages if msg.get('role') == 'assistant']
            
            if len(user_msgs) == 0 or len(assistant_msgs) == 0:
                continue
            
            # ตรวจสอบความยาวของ response
            avg_assistant_length = np.mean([len(msg.get('content', '')) for msg in assistant_msgs])
            if avg_assistant_length < 20:
                continue
            
            # ตรวจสอบความหลากหลาย
            if len(set(msg.get('content', '')[:50] for msg in messages)) < 2:
                continue
            
            filtered.append(conv)
        
        logger.info(f"Quality filtered: {len(filtered)}/{len(conversations)} conversations")
        return filtered
    
    def split_train_validation(self, conversations: List[Dict[str, Any]], 
                              test_size: float = 0.2) -> tuple:
        """แบ่งข้อมูลเป็น train และ validation"""
        train_data, val_data = train_test_split(
            conversations, 
            test_size=test_size, 
            random_state=42
        )
        
        logger.info(f"Split: {len(train_data)} train, {len(val_data)} validation")
        return train_data, val_data
    
    def save_jsonl(self, data: List[Dict[str, Any]], filename: str):
        """บันทึกข้อมูลเป็น JSONL format"""
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
        
        logger.info(f"Saved {len(data)} items to {filepath}")
    
    def create_metadata(self, train_data: List[Dict[str, Any]], 
                       val_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """สร้าง metadata สำหรับ dataset"""
        total_conversations = len(train_data) + len(val_data)
        total_messages = sum(len(conv.get('messages', [])) for conv in train_data + val_data)
        
        # คำนวณสถิติ
        message_lengths = []
        for conv in train_data + val_data:
            for msg in conv.get('messages', []):
                message_lengths.append(len(msg.get('content', '')))
        
        metadata = {
            "dataset_name": "ai_training_platform_fine_tuning",
            "version": "1.0.0",
            "created_date": pd.Timestamp.now().isoformat(),
            "statistics": {
                "total_conversations": total_conversations,
                "train_conversations": len(train_data),
                "validation_conversations": len(val_data),
                "total_messages": total_messages,
                "avg_message_length": np.mean(message_lengths),
                "min_message_length": np.min(message_lengths),
                "max_message_length": np.max(message_lengths)
            },
            "format": "Azure OpenAI Fine-tuning JSONL",
            "description": "Dataset prepared for Azure OpenAI fine-tuning with quality filtering"
        }
        
        return metadata
    
    def prepare_fine_tuning_dataset(self) -> Dict[str, Any]:
        """เตรียม dataset สำหรับ fine-tuning"""
        logger.info("Starting Azure fine-tuning dataset preparation...")
        
        # 1. โหลดข้อมูล
        conversations = self.load_existing_datasets()
        if not conversations:
            raise ValueError("No datasets found to process")
        
        # 2. แปลงรูปแบบ
        azure_format = self.convert_to_azure_format(conversations)
        
        # 3. กรองคุณภาพ
        filtered = self.quality_filter(azure_format)
        
        # 4. แบ่ง train/validation
        train_data, val_data = self.split_train_validation(filtered)
        
        # 5. บันทึกไฟล์
        self.save_jsonl(train_data, "train_data.jsonl")
        self.save_jsonl(val_data, "validation_data.jsonl")
        
        # 6. สร้าง metadata
        metadata = self.create_metadata(train_data, val_data)
        
        # บันทึก metadata
        with open(self.output_dir / "dataset_metadata.json", 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        logger.info("Azure fine-tuning dataset preparation completed!")
        return metadata

def main():
    parser = argparse.ArgumentParser(description="Prepare datasets for Azure OpenAI fine-tuning")
    parser.add_argument("--output-dir", default="data/azure_fine_tuning", 
                       help="Output directory for fine-tuning data")
    parser.add_argument("--test-size", type=float, default=0.2,
                       help="Validation set size (default: 0.2)")
    
    args = parser.parse_args()
    
    preparator = AzureFineTuningPreparator(args.output_dir)
    
    try:
        metadata = preparator.prepare_fine_tuning_dataset()
        print("\n" + "="*50)
        print("🎉 Azure Fine-tuning Dataset Ready!")
        print("="*50)
        print(f"📊 Total conversations: {metadata['statistics']['total_conversations']}")
        print(f"🚂 Train conversations: {metadata['statistics']['train_conversations']}")
        print(f"✅ Validation conversations: {metadata['statistics']['validation_conversations']}")
        print(f"📝 Total messages: {metadata['statistics']['total_messages']}")
        print(f"📏 Avg message length: {metadata['statistics']['avg_message_length']:.1f}")
        print(f"📁 Output directory: {args.output_dir}")
        print("\n📋 Next steps:")
        print("1. Upload train_data.jsonl to Azure Storage")
        print("2. Configure Azure OpenAI fine-tuning job")
        print("3. Monitor training progress")
        print("4. Deploy fine-tuned model")
        
    except Exception as e:
        logger.error(f"Error preparing fine-tuning dataset: {e}")
        raise

if __name__ == "__main__":
    main()
