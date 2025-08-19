# 🤖 Claude Code Setup Guide

คู่มือการตั้งค่าและใช้งาน Claude กับ dataset ที่สร้างขึ้น

## 📋 Prerequisites

- Python 3.11+
- Anthropic API key
- Dataset files (JSONL format)

## 🚀 Quick Start

### 1. ติดตั้ง Dependencies

```bash
# ติดตั้ง Python 3.11 (ถ้ายังไม่มี)
winget install Python.Python.3.11

# ติดตั้ง libraries
py -3.11 -m pip install anthropic datasets pyarrow numpy
```

### 2. ตั้งค่า API Key

```bash
# Windows
set ANTHROPIC_API_KEY=your-api-key-here

# Linux/Mac
export ANTHROPIC_API_KEY=your-api-key-here
```

### 3. รัน Setup Script

```bash
py -3.11 scripts/claude_setup.py
```

## 📁 Project Structure

```
project/
├── config/
│   ├── claude_config.json      # Claude configuration
│   ├── prompt_templates.json   # Prompt templates
│   └── usage_examples.json     # Usage examples
├── data/
│   ├── train.jsonl             # Training data
│   ├── val.jsonl               # Validation data
│   └── test.jsonl              # Test data
├── scripts/
│   ├── build_pairs.py          # Dataset builder
│   ├── claude_setup.py         # Setup script
│   ├── claude_demo.py          # Demo script
│   ├── claude_eval.py          # Evaluation script
│   └── evaluate_dataset.py     # Dataset quality evaluation
└── *.jsonl                     # Generated datasets
```

## 🎯 Usage Examples

### 1. สร้าง Dataset

```bash
# สร้าง dataset ขนาดเล็ก
py -3.11 scripts/build_pairs.py --target 1000 --out my_dataset.jsonl

# สร้าง dataset ขนาดใหญ่
py -3.11 scripts/build_pairs.py --target 5000 --min-len 5 --max-len 256 --out large_dataset.jsonl
```

### 2. ประเมินคุณภาพ Dataset

```bash
py -3.11 scripts/evaluate_dataset.py my_dataset.jsonl
```

### 3. ทดสอบ Claude

```bash
# รัน demo แบบ interactive
py -3.11 scripts/claude_demo.py demo

# สร้าง responses สำหรับ evaluation
py -3.11 scripts/claude_demo.py generate
```

### 4. ประเมิน Claude Responses

```bash
py -3.11 scripts/claude_eval.py data/test.jsonl claude_responses.jsonl
```

## 🔧 Configuration

### Claude Config (`config/claude_config.json`)

```json
{
  "claude_version": "3.5-sonnet",
  "model_settings": {
    "max_tokens": 4096,
    "temperature": 0.7,
    "top_p": 0.9
  },
  "dataset_config": {
    "input_format": "jsonl",
    "output_format": "jsonl",
    "validation_split": 0.1,
    "test_split": 0.1
  }
}
```

### Prompt Templates (`config/prompt_templates.json`)

```json
{
  "system_prompts": {
    "general": "You are Claude, an AI assistant created by Anthropic...",
    "code": "You are Claude, an expert programmer...",
    "analysis": "You are Claude, an expert analyst..."
  },
  "user_prompts": {
    "instruction": "Please follow this instruction: {input}",
    "question": "Please answer this question: {input}"
  }
}
```

## 📊 Evaluation Metrics

### Dataset Quality Metrics

- **Diversity Score**: ความหลากหลายของ intent types
- **Balance Score**: ความสมดุลของการกระจายข้อมูล
- **Coverage Score**: ความครอบคลุมของ sources
- **Cluster Efficiency**: ประสิทธิภาพของ clustering

### Claude Response Metrics

- **Completeness**: ความครบถ้วนของคำตอบ
- **Relevance**: ความเกี่ยวข้องกับคำถาม
- **Coherence**: ความสอดคล้องและโครงสร้าง
- **Helpfulness**: ความช่วยเหลือและประโยชน์

## 🎨 Advanced Usage

### Custom Prompt Engineering

```python
from anthropic import Anthropic
import json

# โหลด prompt templates
with open('config/prompt_templates.json', 'r') as f:
    templates = json.load(f)

client = Anthropic()

# ใช้ custom prompt
system_prompt = templates['system_prompts']['code']
user_prompt = templates['user_prompts']['instruction'].format(input="Write a Python function")

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
)
```

### Batch Processing

```python
import json
import time
from anthropic import Anthropic

def process_batch(dataset, batch_size=10):
    client = Anthropic()
    results = []
    
    for i in range(0, len(dataset), batch_size):
        batch = dataset[i:i+batch_size]
        
        for item in batch:
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[{"role": "user", "content": item['input']}]
            )
            
            results.append({
                'id': item['id'],
                'input': item['input'],
                'response': response.content[0].text
            })
        
        time.sleep(1)  # Rate limiting
    
    return results
```

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**
   ```
   ❌ ANTHROPIC_API_KEY not found!
   ```
   **Solution**: Set your API key environment variable

2. **Import Error**
   ```
   ❌ Anthropic library not installed!
   ```
   **Solution**: Run `pip install anthropic`

3. **Dataset Not Found**
   ```
   ❌ Dataset file not found: data/test.jsonl
   ```
   **Solution**: Run `claude_setup.py` first

4. **Rate Limiting**
   ```
   ❌ Rate limit exceeded
   ```
   **Solution**: Add delays between requests

### Performance Tips

- ใช้ batch processing สำหรับข้อมูลจำนวนมาก
- ตั้งค่า `max_tokens` ให้เหมาะสม
- ใช้ `temperature` ต่ำสำหรับงานที่ต้องการความแม่นยำ
- ใช้ `temperature` สูงสำหรับงานสร้างสรรค์

## 📈 Monitoring & Analytics

### Response Quality Tracking

```python
def track_response_quality(responses):
    metrics = {
        'total_responses': len(responses),
        'avg_length': sum(len(r['response'].split()) for r in responses) / len(responses),
        'success_rate': sum(1 for r in responses if r['response']) / len(responses)
    }
    return metrics
```

### Cost Monitoring

```python
def estimate_cost(responses, model="claude-3-5-sonnet-20241022"):
    # ประมาณการค่าใช้จ่าย (ราคาอาจเปลี่ยนแปลง)
    costs = {
        "claude-3-5-sonnet-20241022": {"input": 0.003, "output": 0.015},  # per 1K tokens
        "claude-3-haiku-20240307": {"input": 0.00025, "output": 0.00125}
    }
    
    total_cost = 0
    for response in responses:
        input_tokens = len(response['input'].split()) * 1.3  # ประมาณการ
        output_tokens = len(response['response'].split()) * 1.3
        
        cost = (input_tokens * costs[model]["input"] + 
                output_tokens * costs[model]["output"]) / 1000
        total_cost += cost
    
    return total_cost
```

## 🔗 Useful Links

- [Anthropic API Documentation](https://docs.anthropic.com/)
- [Claude Models](https://docs.anthropic.com/en/docs/models-overview)
- [Rate Limits](https://docs.anthropic.com/en/api/rate-limits)
- [Best Practices](https://docs.anthropic.com/en/docs/best-practices)

## 📝 License

This project is for educational and research purposes. Please follow Anthropic's usage guidelines and terms of service.
