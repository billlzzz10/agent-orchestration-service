#!/usr/bin/env python3
import os
import urllib.request
import json
import re
from datetime import datetime

# Enhanced Datasets for Prompt Engineering & Agent Alignment
DATASETS = {
    # 🧠 Prompt Engineering
    "alpaca": {
        "url": "https://raw.githubusercontent.com/tatsu-lab/alpaca/main/alpaca_data.json",
        "intent": "instruction",
        "quality": "high",
        "size": "52K"
    },
    "dolly": {
        "url": "https://huggingface.co/datasets/databricks/databricks-dolly-15k/resolve/main/data/train-00000-of-00001.json",
        "intent": "instruction",
        "quality": "high", 
        "size": "15K"
    },
    "self-instruct": {
        "url": "https://raw.githubusercontent.com/yizhongw/self-instruct/main/data/self_instruct.json",
        "intent": "instruction",
        "quality": "medium",
        "size": "82K"
    },
    
    # 🤖 Agent/Role Prompt
    "open-orca": {
        "url": "https://huggingface.co/datasets/Open-Orca/OpenOrca/resolve/main/data/train.json",
        "intent": "roleplay",
        "quality": "high",
        "size": "1M"
    },
    "sharegpt": {
        "url": "https://huggingface.co/datasets/anon8231489123/ShareGPT_Vicuna_unfiltered/resolve/main/data/train.json",
        "intent": "conversation",
        "quality": "medium",
        "size": "90K"
    },
    "ultrachat": {
        "url": "https://huggingface.co/datasets/stingning/ultrachat/resolve/main/data/train.json",
        "intent": "conversation",
        "quality": "high",
        "size": "1.5M"
    },
    
    # 🧰 Code & Tools
    "evol-instruct": {
        "url": "https://huggingface.co/datasets/WizardLM/WizardLM_evol_instruct_V2_196k/resolve/main/data/train.json",
        "intent": "instruction",
        "quality": "high",
        "size": "196K"
    },
    "code-alpaca": {
        "url": "https://raw.githubusercontent.com/sahil280114/codealpaca/main/data/code_alpaca_20k.json",
        "intent": "code",
        "quality": "medium",
        "size": "20K"
    },
    
    # 🧪 Quality Control
    "openhermes": {
        "url": "https://huggingface.co/datasets/teknium/OpenHermes-2.5/resolve/main/data/train.json",
        "intent": "instruction",
        "quality": "very_high",
        "size": "1M"
    },
    "tulu": {
        "url": "https://huggingface.co/datasets/allenai/tulu-v2-sft-mixture/resolve/main/data/train.json",
        "intent": "mixed",
        "quality": "high",
        "size": "326K"
    }
}

def create_manifest():
    """สร้าง dataset manifest สำหรับ tracking"""
    manifest = {
        "created_at": datetime.now().isoformat(),
        "version": "1.0",
        "total_datasets": len(DATASETS),
        "datasets": {}
    }
    
    for name, info in DATASETS.items():
        manifest["datasets"][name] = {
            "source": info["url"],
            "intent": info["intent"],
            "quality": info["quality"],
            "estimated_size": info["size"],
            "downloaded": False,
            "file_path": None,
            "download_time": None,
            "file_size": None
        }
    
    return manifest

def download_with_fallback(name, dataset_info, manifest):
    """ดาวน์โหลดไฟล์พร้อม fallback และ update manifest"""
    url = dataset_info["url"]
    
    # สร้างข้อมูลตัวอย่างตาม intent
    sample_data = create_sample_by_intent(dataset_info["intent"], name)
    
    try:
        out_path = f"data/raw/{name}.json"
        print(f"⬇️  Downloading {name} ({dataset_info['intent']}) → {out_path}")
        urllib.request.urlretrieve(url, out_path)
        
        # ตรวจสอบขนาดไฟล์
        file_size = os.path.getsize(out_path)
        
        manifest["datasets"][name].update({
            "downloaded": True,
            "file_path": out_path,
            "download_time": datetime.now().isoformat(),
            "file_size": file_size
        })
        
        print(f"✅ Successfully downloaded {name} ({file_size} bytes)")
        return True
        
    except Exception as e:
        print(f"❌ Failed to download {name}: {e}")
        
        # สร้างข้อมูลตัวอย่างแทน
        out_path = f"data/raw/{name}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(sample_data, f, ensure_ascii=False, indent=2)
        
        manifest["datasets"][name].update({
            "downloaded": False,
            "file_path": out_path,
            "download_time": datetime.now().isoformat(),
            "file_size": os.path.getsize(out_path),
            "note": "Sample data created due to download failure"
        })
        
        print(f"📝 Created sample data for {name}")
        return False

def create_sample_by_intent(intent, name):
    """สร้างข้อมูลตัวอย่างตาม intent"""
    
    if intent == "instruction":
        return [
            {"user_input": "Write a Python function to sort a list", "target_prompt": "def sort_list(lst): return sorted(lst)"},
            {"user_input": "Explain the concept of recursion", "target_prompt": "Recursion is a programming technique where a function calls itself to solve smaller subproblems."},
            {"user_input": "How to optimize database queries?", "target_prompt": "Use indexes, avoid SELECT *, limit results, and analyze query execution plans."}
        ]
    
    elif intent == "roleplay":
        return [
            {"user_input": "Act as a helpful assistant and explain AI", "target_prompt": "As your helpful assistant, I'd say AI is technology that enables machines to simulate human intelligence."},
            {"user_input": "You are a teacher. Explain photosynthesis", "target_prompt": "As your teacher, let me explain: photosynthesis is how plants convert sunlight into energy using chlorophyll."},
            {"user_input": "Role: Chef. How to make pasta?", "target_prompt": "As a chef, I recommend boiling salted water, cooking pasta al dente, and finishing with quality sauce."}
        ]
    
    elif intent == "conversation":
        return [
            {"user_input": "Hi! How are you today?", "target_prompt": "Hello! I'm doing well, thank you for asking. How can I help you today?"},
            {"user_input": "What's the weather like?", "target_prompt": "I don't have access to real-time weather data, but I can help you find weather information if you tell me your location."},
            {"user_input": "Can you help me with my homework?", "target_prompt": "I'd be happy to help! What subject are you working on and what specific questions do you have?"}
        ]
    
    elif intent == "code":
        return [
            {"user_input": "Write a hello world program", "target_prompt": "print('Hello, World!')"},
            {"user_input": "Create a simple calculator function", "target_prompt": "def calculator(a, op, b):\n    if op == '+': return a + b\n    elif op == '-': return a - b\n    elif op == '*': return a * b\n    elif op == '/': return a / b if b != 0 else 'Error'"},
            {"user_input": "Implement bubble sort", "target_prompt": "def bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n-i-1):\n            if arr[j] > arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]\n    return arr"}
        ]
    
    else:  # mixed
        return [
            {"user_input": "Explain machine learning", "target_prompt": "Machine learning is a subset of AI that enables computers to learn from data without explicit programming."},
            {"user_input": "How to cook rice?", "target_prompt": "Rinse rice, add water (2:1 ratio), bring to boil, reduce heat, cover and simmer 18-20 minutes."},
            {"user_input": "What is climate change?", "target_prompt": "Climate change refers to long-term shifts in global weather patterns primarily caused by human activities."}
        ]

def main():
    os.makedirs("data/raw", exist_ok=True)
    
    print("🚀 Enhanced Dataset Download for Prompt Engineering & Agent Alignment")
    print("=" * 75)
    
    # สร้าง manifest
    manifest = create_manifest()
    
    success_count = 0
    total_count = len(DATASETS)
    
    # ดาวน์โหลด datasets
    for name, dataset_info in DATASETS.items():
        if download_with_fallback(name, dataset_info, manifest):
            success_count += 1
    
    # บันทึก manifest
    with open("data/dataset_manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 75)
    print(f"✅ Download Summary:")
    print(f"   Successfully downloaded: {success_count}/{total_count} datasets")
    print(f"   Location: data/raw/")
    print(f"   Manifest: data/dataset_manifest.json")
    
    # สรุปตาม intent
    intent_summary = {}
    for name, info in DATASETS.items():
        intent = info["intent"]
        if intent not in intent_summary:
            intent_summary[intent] = []
        intent_summary[intent].append(name)
    
    print(f"\n📊 Datasets by Intent:")
    for intent, datasets in intent_summary.items():
        print(f"   {intent}: {len(datasets)} datasets")
        for dataset in datasets:
            status = "✅" if manifest["datasets"][dataset]["downloaded"] else "📝"
            print(f"     {status} {dataset}")

if __name__ == "__main__":
    main()
