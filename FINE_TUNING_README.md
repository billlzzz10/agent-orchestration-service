# 🎯 Fine-tuning Pipeline - AI Training Platform

## 📋 Overview

Fine-tuning Pipeline สำหรับ AI Training Platform ที่รองรับทั้ง **Azure OpenAI** และ **OpenSource Models** พร้อม GIF export สำหรับ review

## 🚀 Features

### ✅ **Azure OpenAI Fine-tuning**
- Dataset preparation สำหรับ Azure OpenAI format
- Complete workflow orchestration
- Model deployment และ testing
- Quality evaluation metrics

### ✅ **OpenSource Model Demo**
- Local model inference
- Real-time conversation demo
- GIF export สำหรับ review
- Multiple model support

### ✅ **Quality Assurance**
- Dataset quality filtering
- Train/validation split
- Performance benchmarking
- Comprehensive testing

## 📁 Project Structure

```
project/
├── scripts/
│   ├── azure_fine_tuning_prep.py      # Dataset preparation
│   ├── azure_fine_tuning_orchestrator.py  # Azure workflow
│   ├── opensource_model_demo.py       # OpenSource demo
│   └── test_fine_tuning_pipeline.py   # Testing framework
├── data/
│   ├── azure_fine_tuning/             # Azure format datasets
│   ├── processed/                     # Processed datasets
│   └── enhanced/                      # Enhanced datasets
├── outputs/
│   └── gifs/                          # GIF exports
├── test_outputs/                      # Test results
├── requirements_fine_tuning.txt       # Dependencies
├── test_fine_tuning.sh               # Test script
└── FINE_TUNING_README.md             # This file
```

## 🛠️ Installation

### 1. **Install Dependencies**

```bash
# Install fine-tuning requirements
pip install -r requirements_fine_tuning.txt

# หรือติดตั้งทีละตัว
pip install torch transformers datasets
pip install azure-identity azure-ai-ml azure-storage-blob
pip install openai pillow imageio fastapi uvicorn
```

### 2. **Azure Setup** (สำหรับ Azure Fine-tuning)

```bash
# Login to Azure
az login

# Set subscription
az account set --subscription <your-subscription-id>

# Create resource group
az group create --name <resource-group> --location eastus

# Create Azure OpenAI resource
az cognitiveservices account create \
    --name <openai-resource> \
    --resource-group <resource-group> \
    --kind OpenAI \
    --sku S0 \
    --location eastus
```

### 3. **Environment Variables**

```bash
# Azure OpenAI
export AZURE_OPENAI_ENDPOINT="https://<resource>.openai.azure.com/"
export AZURE_OPENAI_API_KEY="<your-api-key>"
export AZURE_SUBSCRIPTION_ID="<subscription-id>"
export AZURE_RESOURCE_GROUP="<resource-group>"
export AZURE_WORKSPACE_NAME="<workspace-name>"

# Storage
export AZURE_STORAGE_ACCOUNT="<storage-account>"
```

## 🎯 Usage Examples

### 1. **Dataset Preparation**

```bash
# เตรียมข้อมูลสำหรับ Azure fine-tuning
python3 scripts/azure_fine_tuning_prep.py \
    --output-dir data/azure_fine_tuning \
    --test-size 0.2
```

**Output:**
- `train_data.jsonl` - Training data
- `validation_data.jsonl` - Validation data
- `dataset_metadata.json` - Dataset statistics

### 2. **OpenSource Model Demo**

```bash
# สาธิต OpenSource model พร้อม GIF export
python3 scripts/opensource_model_demo.py \
    --model "microsoft/DialoGPT-medium" \
    --prompts "Hello!" "How are you?" "Tell me a joke" \
    --output-gif "demo_conversation.gif"
```

**Output:**
- `demo_conversation.gif` - Animated conversation
- `demo_results.json` - Test results

### 3. **Azure Fine-tuning Workflow**

```bash
# รัน complete Azure fine-tuning workflow
python3 scripts/azure_fine_tuning_orchestrator.py \
    --subscription-id $AZURE_SUBSCRIPTION_ID \
    --resource-group $AZURE_RESOURCE_GROUP \
    --workspace-name $AZURE_WORKSPACE_NAME \
    --openai-endpoint $AZURE_OPENAI_ENDPOINT \
    --openai-api-key $AZURE_OPENAI_API_KEY \
    --storage-account $AZURE_STORAGE_ACCOUNT \
    --data-file data/azure_fine_tuning/train_data.jsonl \
    --model-name "gpt-35-turbo" \
    --deployment-name "my-fine-tuned-model"
```

### 4. **Complete Testing**

```bash
# ทดสอบ pipeline ครบถ้วน
./test_fine_tuning.sh

# หรือใช้ Python script
python3 scripts/test_fine_tuning_pipeline.py --test-dir test_outputs
```

## 📊 Dataset Format

### **Azure OpenAI Format (JSONL)**

```json
{"messages": [{"role": "user", "content": "Hello!"}, {"role": "assistant", "content": "Hi there! How can I help you today?"}]}
{"messages": [{"role": "user", "content": "What's the weather like?"}, {"role": "assistant", "content": "I don't have access to real-time weather data, but I can help you find weather information online!"}]}
```

### **Input Format Support**

- **Conversations**: `{"conversations": [{"from": "human", "value": "..."}, {"from": "gpt", "value": "..."}]}`
- **Instruction-Response**: `{"instruction": "...", "response": "..."}`
- **Prompt-Completion**: `{"prompt": "...", "completion": "..."}`

## 🎬 GIF Export Features

### **OpenSource Model Demo GIF**

- **Real-time Conversation**: แสดงการสนทนาระหว่าง user และ model
- **Generation Time**: แสดงเวลาที่ใช้ในการสร้าง response
- **Quality Metrics**: แสดงคุณภาพของ response
- **Export Options**: บันทึกเป็น GIF สำหรับ review

### **GIF Configuration**

```python
# ปรับแต่ง GIF settings
demo = OpenSourceModelDemo("microsoft/DialoGPT-medium")
demo.frame_delay = 0.5  # ความเร็วของ animation
demo.gif_frames = []    # เก็บ frames

# สร้าง custom frame
demo.add_frame_to_gif("Custom text frame")
demo.save_gif("custom_demo.gif")
```

## 🔧 Configuration

### **Azure Fine-tuning Hyperparameters**

```python
hyperparameters = {
    "n_epochs": 3,                    # จำนวน epochs
    "batch_size": 1,                  # Batch size
    "learning_rate_multiplier": 1.0   # Learning rate multiplier
}
```

### **Quality Filtering Settings**

```python
# Dataset quality thresholds
min_length = 50        # ความยาวขั้นต่ำ
max_length = 4000      # ความยาวสูงสุด
min_response_length = 20  # ความยาว response ขั้นต่ำ
```

### **Model Selection**

```python
# Azure OpenAI Models
azure_models = [
    "gpt-35-turbo",
    "gpt-4",
    "gpt-4-turbo"
]

# OpenSource Models
opensource_models = [
    "microsoft/DialoGPT-small",
    "microsoft/DialoGPT-medium",
    "microsoft/DialoGPT-large",
    "facebook/opt-350m",
    "facebook/opt-1.3b"
]
```

## 📈 Performance Metrics

### **Dataset Quality Metrics**

- **Total Conversations**: จำนวนการสนทนาทั้งหมด
- **Train/Validation Split**: อัตราส่วนข้อมูล training/validation
- **Average Message Length**: ความยาวเฉลี่ยของข้อความ
- **Quality Score**: คะแนนคุณภาพของ dataset

### **Model Performance Metrics**

- **Generation Time**: เวลาที่ใช้ในการสร้าง response
- **Response Quality**: คุณภาพของ response
- **Token Usage**: จำนวน tokens ที่ใช้
- **Cost Analysis**: การวิเคราะห์ค่าใช้จ่าย

## 🧪 Testing Framework

### **Test Coverage**

1. **Dataset Preparation Test**
   - Data loading และ validation
   - Format conversion
   - Quality filtering
   - Train/validation split

2. **OpenSource Model Test**
   - Model loading
   - Response generation
   - GIF creation
   - Performance measurement

3. **Azure Orchestrator Test**
   - Storage setup
   - Data upload
   - Job creation
   - Model deployment

4. **Web Application Test**
   - API endpoints
   - Health checks
   - User interface

### **Running Tests**

```bash
# Run all tests
./test_fine_tuning.sh

# Run specific test
python3 scripts/test_fine_tuning_pipeline.py --test-dir test_outputs

# Check test results
cat test_outputs/test_results.json
```

## 🚀 Production Deployment

### **Azure Production Setup**

1. **Resource Scaling**
   ```bash
   # Scale up Azure resources
   az cognitiveservices account update \
       --name <resource> \
       --resource-group <group> \
       --sku S1
   ```

2. **Monitoring Setup**
   ```bash
   # Enable monitoring
   az monitor diagnostic-settings create \
       --resource <resource-id> \
       --name "fine-tuning-monitoring" \
       --logs '[{"category": "AuditLogs", "enabled": true}]'
   ```

3. **Security Configuration**
   ```bash
   # Enable private endpoints
   az network private-endpoint create \
       --name "openai-private-endpoint" \
       --resource-group <group> \
       --vnet-name <vnet> \
       --subnet <subnet> \
       --private-connection-resource-id <resource-id>
   ```

### **OpenSource Production Setup**

1. **Model Optimization**
   ```python
   # Quantization for production
   from transformers import AutoModelForCausalLM
   
   model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
   model = torch.quantization.quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8)
   ```

2. **Caching Setup**
   ```python
   # Response caching
   import redis
   
   redis_client = redis.Redis(host='localhost', port=6379, db=0)
   
   def get_cached_response(prompt):
       cache_key = f"response:{hash(prompt)}"
       return redis_client.get(cache_key)
   ```

## 📚 Troubleshooting

### **Common Issues**

1. **Azure Authentication Error**
   ```bash
   # Solution: Set up Azure credentials
   az login
   az account set --subscription <subscription-id>
   ```

2. **Model Loading Error**
   ```bash
   # Solution: Install correct dependencies
   pip install torch transformers --index-url https://download.pytorch.org/whl/cu118
   ```

3. **GIF Creation Error**
   ```bash
   # Solution: Install imageio dependencies
   pip install imageio imageio-ffmpeg
   ```

4. **Memory Issues**
   ```python
   # Solution: Use smaller models or enable gradient checkpointing
   model.gradient_checkpointing_enable()
   ```

### **Debug Mode**

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python3 scripts/azure_fine_tuning_prep.py --debug
```

## 🤝 Contributing

### **Development Setup**

1. **Fork Repository**
2. **Create Feature Branch**
3. **Add Tests**
4. **Submit Pull Request**

### **Code Standards**

- Follow PEP 8 style guidelines
- Add type hints to all functions
- Include comprehensive docstrings
- Write unit tests for new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### **Documentation**
- [Azure OpenAI Documentation](https://docs.microsoft.com/en-us/azure/cognitive-services/openai/)
- [Transformers Documentation](https://huggingface.co/docs/transformers/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

### **Community**
- GitHub Issues: [Report bugs](https://github.com/your-repo/issues)
- Discussions: [Ask questions](https://github.com/your-repo/discussions)

---

## 🎉 **Ready to Fine-tune!**

Fine-tuning Pipeline พร้อมใช้งานแล้ว! 

**เริ่มต้นใช้งาน:**
```bash
./test_fine_tuning.sh
```

**หรือดูตัวอย่างเพิ่มเติม:**
```bash
python3 scripts/opensource_model_demo.py --help
python3 scripts/azure_fine_tuning_prep.py --help
```

**Happy Fine-tuning! 🚀**
