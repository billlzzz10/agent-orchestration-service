# Dataset Processing Pipeline

Pipeline สำหรับประมวลผล dataset และสร้าง FAISS index สำหรับ semantic search

## 📋 Prerequisites

```bash
pip install -r requirements.txt
```

## 🚀 วิธีใช้งาน

### วิธีที่ 1: Enhanced Pipeline (แนะนำ)

```bash
# รัน enhanced pipeline ทั้งหมด
./test.sh
```

### วิธีที่ 2: รันทีละขั้นตอน

```bash
# 0. ดาวน์โหลด enhanced datasets
python scripts/enhanced_download.py

# 1. ประมวลผลขั้นสูงพร้อม filtering และ intent classification
python scripts/advanced_processor.py

# 2. วิเคราะห์ overlap ด้วย embedding clustering
python scripts/embedding_analyzer.py

# 3. ประเมินคุณภาพขั้นสุดท้าย
python scripts/basic_test.py enhanced_dataset.jsonl
```

### วิธีที่ 3: Legacy Pipeline

```bash
# 0. ดาวน์โหลด datasets (ถ้ายังไม่มี)
python scripts/download_datasets.py

# 1. รวมไฟล์ raw เป็น dataset.jsonl
python scripts/1.py data/raw

# 2. ประเมินคุณภาพด้วย similarity
python scripts/basic_test.py
```

## 📁 โครงสร้างไฟล์

```
project/
├── scripts/
│   ├── enhanced_download.py    # Enhanced dataset downloader
│   ├── advanced_processor.py   # Advanced filtering & intent classification
│   ├── embedding_analyzer.py   # Embedding-based clustering analysis
│   ├── basic_test.py          # Quality evaluation
│   ├── download_datasets.py   # Legacy downloader
│   ├── 1.py                   # Legacy processor
│   ├── 2.py                   # Legacy FAISS indexer
│   └── 3.py                   # Legacy evaluator
├── data/
│   ├── raw/                   # Raw dataset files
│   └── dataset_manifest.json  # Dataset tracking metadata
├── enhanced_dataset.jsonl     # Enhanced processed dataset
├── processing_report.json     # Processing statistics
├── cluster_analysis.json      # Clustering results
├── results.json              # Quality evaluation results
├── requirements.txt          # Dependencies
├── test.sh                  # Enhanced pipeline script
└── README.md                # ไฟล์นี้
```

## 📊 ผลลัพธ์

### Enhanced Pipeline Outputs:
- `enhanced_dataset.jsonl` - Dataset ที่ผ่าน filtering และ intent classification
- `data/dataset_manifest.json` - Metadata สำหรับ tracking datasets
- `processing_report.json` - สถิติการประมวลผล
- `cluster_analysis.json` - ผลการวิเคราะห์ overlap ด้วย clustering
- `results.json` - ผลการประเมินคุณภาพ

### Legacy Pipeline Outputs:
- `dataset.jsonl` - ไฟล์ dataset รวม
- `results.json` - ผลการประเมินคุณภาพ

## 🔧 การตั้งค่า

### วิธีที่ 1: Enhanced Pipeline (แนะนำ)
1. รัน `./test.sh` เพื่อรัน enhanced pipeline ทั้งหมด
2. ระบบจะดาวน์โหลด datasets, filter, classify, และ analyze อัตโนมัติ

### วิธีที่ 2: ใช้ข้อมูลของตัวเอง
1. สร้างโฟลเดอร์ `data/raw/`
2. ใส่ไฟล์ JSON/CSV ที่มีคอลัมน์ `user_input` และ `target_prompt`
3. รัน `python scripts/advanced_processor.py` เพื่อประมวลผล

### วิธีที่ 3: Legacy Pipeline
1. รัน `python scripts/download_datasets.py` เพื่อดาวน์โหลด datasets
2. รัน `python scripts/1.py data/raw` เพื่อรวมข้อมูล
3. รัน `python scripts/basic_test.py` เพื่อประเมินคุณภาพ

## 📝 หมายเหตุ

### Enhanced Features:
- **Length Filtering**: กรอง prompts ที่มีความยาวเหมาะสม (10-1000 chars, 3-300 tokens)
- **Intent Classification**: จำแนก intent เป็น instruction, question, roleplay, code, conversation
- **Embedding Clustering**: วิเคราะห์ overlap ระหว่าง datasets ด้วย TF-IDF + K-Means
- **Dataset Tracking**: ระบบ manifest สำหรับ track source, version, metadata
- **Quality Control**: ตรวจสอบคุณภาพและสร้างรายงานสถิติ

### Technical Details:
- ใช้ Python built-in libraries (ไม่ต้องติดตั้ง dependencies เพิ่ม)
- รองรับไฟล์ JSON, JSONL, CSV
- รองรับ datasets หลากหลายรูปแบบ
- Fallback system สำหรับ datasets ที่ดาวน์โหลดไม่ได้

## 📊 Datasets สำหรับ Prompt Engineering & Agent Alignment

### 🧠 Prompt Engineering
- **PromptSet**: High-quality prompt engineering dataset
- **Self-Instruct**: Self-instruction dataset for instruction tuning
- **Alpaca**: Stanford Alpaca instruction-following dataset

### 🤖 Agent/Role Prompt
- **Open-Orca**: Open Orca dataset for agent conversations
- **Vicuna**: Vicuna dataset for role-based prompts
- **Chatbot-Arena**: LMSYS Chatbot Arena conversations

### 🧰 Code & Tools
- **Magicoder-Evol**: Code generation and evolution instructions
- **Code-Instruct**: Code instruction dataset

### 🧪 LLM Benchmark
- **FLAN-DialogSum**: Dialog summarization dataset
- **Agent-Instruct**: Agent instruction dataset

### 🔍 Use Cases
- **Prompt Engineering**: ฝึกฝนการเขียน prompts ที่มีประสิทธิภาพ
- **Agent Alignment**: ปรับแต่ง AI agents ให้ทำงานตามที่ต้องการ
- **Embedding Retrieval**: สร้าง embeddings สำหรับ semantic search
- **Instruction Tuning**: ปรับแต่งโมเดลให้ทำตามคำสั่ง
