#!/usr/bin/env python3
import json
import re
import os
from collections import defaultdict, Counter

class PromptFilter:
    def __init__(self, min_length=10, max_length=1000, min_tokens=3, max_tokens=300):
        self.min_length = min_length
        self.max_length = max_length
        self.min_tokens = min_tokens
        self.max_tokens = max_tokens
    
    def count_tokens(self, text):
        """นับ tokens โดยประมาณ"""
        return len(re.findall(r'\w+', text))
    
    def is_valid_prompt(self, user_input, target_prompt):
        """ตรวจสอบว่า prompt ผ่านเงื่อนไขหรือไม่"""
        checks = {
            "user_length": self.min_length <= len(user_input) <= self.max_length,
            "target_length": self.min_length <= len(target_prompt) <= self.max_length,
            "user_tokens": self.min_tokens <= self.count_tokens(user_input) <= self.max_tokens,
            "target_tokens": self.min_tokens <= self.count_tokens(target_prompt) <= self.max_tokens,
            "not_empty": user_input.strip() and target_prompt.strip(),
            "no_special_chars": not any(char in user_input for char in ['<', '>', '{', '}', '[', ']'])
        }
        
        return all(checks.values()), checks

class IntentClassifier:
    def __init__(self):
        self.intent_patterns = {
            "instruction": [
                r"^(write|create|make|build|implement|design|develop)",
                r"^(how to|how do|how can)",
                r"(step by step|tutorial|guide|instructions)",
                r"^(explain|describe|define|clarify)"
            ],
            "question": [
                r"^(what|why|when|where|which|who)",
                r"^(is|are|can|could|would|should|do|does)",
                r"\?$"
            ],
            "roleplay": [
                r"^(act as|you are|role|pretend|imagine)",
                r"(assistant|teacher|expert|coach|advisor)",
                r"(persona|character|role-play)"
            ],
            "code": [
                r"(function|class|method|algorithm)",
                r"(python|javascript|java|c\+\+|code)",
                r"(programming|coding|software|debug)"
            ],
            "conversation": [
                r"^(hi|hello|hey|good|thanks)",
                r"(chat|talk|discuss|conversation)",
                r"(opinion|think|feel|suggest)"
            ]
        }
    
    def classify_intent(self, user_input):
        """จำแนก intent ของ prompt"""
        text = user_input.lower().strip()
        
        intent_scores = defaultdict(int)
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    intent_scores[intent] += 1
        
        if not intent_scores:
            return "general"
        
        return max(intent_scores, key=intent_scores.get)

class DatasetProcessor:
    def __init__(self):
        self.filter = PromptFilter()
        self.classifier = IntentClassifier()
        self.stats = {
            "total_processed": 0,
            "filtered_out": 0,
            "by_intent": defaultdict(int),
            "by_source": defaultdict(int),
            "filter_reasons": defaultdict(int)
        }
    
    def process_dataset(self, input_folder, output_file="enhanced_dataset.jsonl"):
        """ประมวลผล datasets พร้อม filtering และ intent classification"""
        
        print("🔍 Processing datasets with advanced filtering...")
        print("=" * 60)
        
        processed_records = []
        
        # โหลด manifest
        manifest_path = "data/dataset_manifest.json"
        manifest = {}
        if os.path.exists(manifest_path):
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest = json.load(f)
        
        # ประมวลผลไฟล์ทั้งหมด
        for filename in os.listdir(input_folder):
            if not filename.endswith(('.json', '.jsonl')):
                continue
                
            filepath = os.path.join(input_folder, filename)
            dataset_name = filename.split('.')[0]
            
            print(f"📄 Processing {dataset_name}...")
            
            # โหลดข้อมูล
            records = self.load_dataset_file(filepath)
            
            for record in records:
                self.stats["total_processed"] += 1
                self.stats["by_source"][dataset_name] += 1
                
                user_input = record.get("user_input", "")
                target_prompt = record.get("target_prompt", "")
                
                # ตรวจสอบความถูกต้อง
                is_valid, checks = self.filter.is_valid_prompt(user_input, target_prompt)
                
                if not is_valid:
                    self.stats["filtered_out"] += 1
                    for check, passed in checks.items():
                        if not passed:
                            self.stats["filter_reasons"][check] += 1
                    continue
                
                # จำแนก intent
                intent = self.classifier.classify_intent(user_input)
                self.stats["by_intent"][intent] += 1
                
                # เพิ่มข้อมูล metadata
                enhanced_record = {
                    "user_input": user_input,
                    "target_prompt": target_prompt,
                    "intent": intent,
                    "source": dataset_name,
                    "user_tokens": self.filter.count_tokens(user_input),
                    "target_tokens": self.filter.count_tokens(target_prompt),
                    "user_length": len(user_input),
                    "target_length": len(target_prompt)
                }
                
                # เพิ่ม metadata จาก manifest
                if dataset_name in manifest.get("datasets", {}):
                    enhanced_record["source_quality"] = manifest["datasets"][dataset_name].get("quality", "unknown")
                
                processed_records.append(enhanced_record)
        
        # บันทึกผลลัพธ์
        with open(output_file, "w", encoding="utf-8") as f:
            for record in processed_records:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        
        # สร้างรายงาน
        self.generate_report(processed_records, output_file)
        
        return processed_records
    
    def load_dataset_file(self, filepath):
        """โหลดไฟล์ dataset รองรับหลายรูปแบบ"""
        records = []
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                if filepath.endswith('.jsonl'):
                    for line in f:
                        if line.strip():
                            records.append(json.loads(line))
                else:
                    data = json.load(f)
                    if isinstance(data, list):
                        records = data
                    elif isinstance(data, dict) and "data" in data:
                        records = data["data"]
        except Exception as e:
            print(f"⚠️  Error loading {filepath}: {e}")
        
        return records
    
    def generate_report(self, processed_records, output_file):
        """สร้างรายงานการประมวลผล"""
        
        print(f"\n📊 Processing Report")
        print("=" * 60)
        print(f"Total processed: {self.stats['total_processed']}")
        print(f"Valid records: {len(processed_records)}")
        print(f"Filtered out: {self.stats['filtered_out']}")
        print(f"Success rate: {len(processed_records)/self.stats['total_processed']*100:.1f}%")
        
        print(f"\n🎯 Records by Intent:")
        for intent, count in sorted(self.stats["by_intent"].items(), key=lambda x: x[1], reverse=True):
            percentage = count / len(processed_records) * 100
            print(f"  {intent}: {count} ({percentage:.1f}%)")
        
        print(f"\n📁 Records by Source:")
        for source, count in sorted(self.stats["by_source"].items(), key=lambda x: x[1], reverse=True):
            valid_count = sum(1 for r in processed_records if r["source"] == source)
            success_rate = valid_count / count * 100 if count > 0 else 0
            print(f"  {source}: {valid_count}/{count} ({success_rate:.1f}%)")
        
        if self.stats["filter_reasons"]:
            print(f"\n❌ Top Filter Reasons:")
            for reason, count in sorted(self.stats["filter_reasons"].items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"  {reason}: {count}")
        
        # บันทึกรายงานเป็นไฟล์
        report = {
            "summary": {
                "total_processed": self.stats["total_processed"],
                "valid_records": len(processed_records),
                "filtered_out": self.stats["filtered_out"],
                "success_rate": len(processed_records)/self.stats["total_processed"]*100
            },
            "by_intent": dict(self.stats["by_intent"]),
            "by_source": dict(self.stats["by_source"]),
            "filter_reasons": dict(self.stats["filter_reasons"]),
            "output_file": output_file
        }
        
        with open("processing_report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ Enhanced dataset saved to: {output_file}")
        print(f"📋 Report saved to: processing_report.json")

def main():
    processor = DatasetProcessor()
    processor.process_dataset("data/raw", "enhanced_dataset.jsonl")

if __name__ == "__main__":
    main()
