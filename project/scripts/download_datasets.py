#!/usr/bin/env python3
import os
import urllib.request
import json

# Datasets สำหรับ Prompt Engineering, Agent Alignment, และ Embedding Retrieval
DATASETS = {
    # 🧠 Prompt Engineering
    "promptset": "https://huggingface.co/datasets/pisterlabs/promptset/resolve/main/data/train.jsonl",
    "self-instruct": "https://raw.githubusercontent.com/yizhongw/self-instruct/main/data/self_instruct.json",
    "alpaca": "https://raw.githubusercontent.com/tatsu-lab/alpaca/main/alpaca_data.json",
    
    # 🤖 Agent/Role Prompt
    "open-orca": "https://huggingface.co/datasets/Open-Orca/OpenOrca/resolve/main/data/openorca.jsonl",
    "vicuna": "https://huggingface.co/datasets/lmsys/vicuna/resolve/main/data/vicuna_data.json",
    "chatbot-arena": "https://huggingface.co/datasets/lmsys/chatbot_arena_conversations/resolve/main/conversations.json",
    
    # 🧰 Code & Tools
    "magicoder-evol": "https://huggingface.co/datasets/ise-uiuc/Magicoder-Evol-Instruct/resolve/main/data/train.json",
    "code-instruct": "https://huggingface.co/datasets/nlphuji/code_instruct/resolve/main/data/train.json",
    
    # 🧪 LLM Benchmark
    "flan-dialogsum": "https://huggingface.co/datasets/knkarthick/dialogsum/resolve/main/data/train.json",
    "agent-instruct": "https://huggingface.co/datasets/THUDM/AgentInstruct/resolve/main/data/train.json"
}

def download_with_fallback(name, url):
    """ดาวน์โหลดไฟล์พร้อม fallback URLs"""
    fallback_urls = {
        "promptset": [
            "https://huggingface.co/datasets/pisterlabs/promptset/resolve/main/data/train.jsonl",
            "https://raw.githubusercontent.com/pisterlabs/promptset/main/data/train.jsonl"
        ],
        "self-instruct": [
            "https://raw.githubusercontent.com/yizhongw/self-instruct/main/data/self_instruct.json",
            "https://huggingface.co/datasets/yizhongw/self-instruct/resolve/main/data/self_instruct.json"
        ],
        "alpaca": [
            "https://raw.githubusercontent.com/tatsu-lab/alpaca/main/alpaca_data.json",
            "https://huggingface.co/datasets/tatsu-lab/alpaca/resolve/main/alpaca_data.json"
        ]
    }
    
    urls_to_try = fallback_urls.get(name, [url])
    
    for i, try_url in enumerate(urls_to_try):
        try:
            out_path = f"data/raw/{name}.{try_url.split('.')[-1]}"
            print(f"⬇️  Downloading {name} (attempt {i+1}) → {out_path}")
            urllib.request.urlretrieve(try_url, out_path)
            print(f"✅ Successfully downloaded {name}")
            return True
        except Exception as e:
            print(f"❌ Failed to download {name} from {try_url}: {e}")
            if i == len(urls_to_try) - 1:
                print(f"⚠️  All attempts failed for {name}")
                return False
    return False

def create_sample_data():
    """สร้างข้อมูลตัวอย่างสำหรับ datasets ที่ดาวน์โหลดไม่ได้"""
    sample_datasets = {
        "promptset": [
            {"user_input": "Write a Python function to calculate factorial", "target_prompt": "def factorial(n): return 1 if n <= 1 else n * factorial(n-1)"},
            {"user_input": "Explain machine learning", "target_prompt": "Machine learning is a subset of AI that enables computers to learn from data without explicit programming."},
            {"user_input": "How to cook pasta?", "target_prompt": "Boil water, add pasta, cook for 8-10 minutes, drain and serve with sauce."}
        ],
        "self-instruct": [
            {"user_input": "What is blockchain?", "target_prompt": "Blockchain is a distributed ledger technology that maintains records in blocks linked by cryptography."},
            {"user_input": "How to learn programming?", "target_prompt": "Start with basics, practice daily, build projects, and learn from online resources."},
            {"user_input": "Explain quantum computing", "target_prompt": "Quantum computing uses quantum mechanical phenomena to process information in ways classical computers cannot."}
        ],
        "alpaca": [
            {"user_input": "Write a poem about AI", "target_prompt": "In circuits deep and algorithms bright, artificial minds take flight. Learning, growing, day by day, in digital dreams they find their way."},
            {"user_input": "How to make coffee?", "target_prompt": "Grind beans, heat water to 200°F, pour over grounds, let steep for 4 minutes, then enjoy."},
            {"user_input": "What is climate change?", "target_prompt": "Climate change refers to long-term shifts in global weather patterns caused by human activities."}
        ]
    }
    
    for name, data in sample_datasets.items():
        out_path = f"data/raw/{name}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"📝 Created sample data for {name}")

def main():
    os.makedirs("data/raw", exist_ok=True)
    
    print("🚀 Starting Dataset Download for Prompt Engineering & Agent Alignment")
    print("=" * 70)
    
    success_count = 0
    total_count = len(DATASETS)
    
    for name, url in DATASETS.items():
        if download_with_fallback(name, url):
            success_count += 1
        else:
            print(f"📝 Creating sample data for {name} instead...")
            create_sample_data()
    
    print("\n" + "=" * 70)
    print(f"✅ Download Summary:")
    print(f"   Successfully downloaded: {success_count}/{total_count} datasets")
    print(f"   Location: data/raw/")
    
    if success_count < total_count:
        print(f"   Note: Some datasets were replaced with sample data")
    
    print("\n📊 Available datasets:")
    for fname in os.listdir("data/raw"):
        if fname.endswith(('.json', '.jsonl')):
            print(f"   - {fname}")

if __name__ == "__main__":
    main()
