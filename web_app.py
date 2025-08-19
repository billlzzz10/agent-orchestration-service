#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Training Platform Web Application
เว็บแอปพลิเคชันสำหรับ AI Training Platform Demo
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import uvicorn
from fastapi import FastAPI, HTTPException, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Training Platform",
    description="Fine-tuning Pipeline Demo Platform",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Pydantic models
class Conversation(BaseModel):
    user_message: str
    assistant_message: str

class DatasetInfo(BaseModel):
    total_conversations: int
    quality_score: float
    avg_message_length: float

class ModelInfo(BaseModel):
    model_name: str
    version: str
    status: str
    quality_score: float

# Global variables
DEMO_DATA = {
    "conversations": [],
    "model_info": None,
    "test_results": None
}

def load_demo_data():
    """โหลดข้อมูล demo จากไฟล์"""
    try:
        # Load conversations
        conversations_file = Path("data/raw/sample_conversations.json")
        if conversations_file.exists():
            with open(conversations_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                DEMO_DATA["conversations"] = data
        
        # Load model info
        model_file = Path("outputs/models/ai-training-platform-model-metadata.json")
        if model_file.exists():
            with open(model_file, 'r', encoding='utf-8') as f:
                DEMO_DATA["model_info"] = json.load(f)
        
        # Load test results
        test_file = Path("outputs/results/test_results.json")
        if test_file.exists():
            with open(test_file, 'r', encoding='utf-8') as f:
                DEMO_DATA["test_results"] = json.load(f)
        
        logger.info("Demo data loaded successfully")
    except Exception as e:
        logger.error(f"Error loading demo data: {e}")

# Load data on startup
load_demo_data()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """หน้าแรกของแอปพลิเคชัน"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "model_info": DEMO_DATA["model_info"],
        "test_results": DEMO_DATA["test_results"]
    })

@app.get("/dataset", response_class=HTMLResponse)
async def dataset_page(request: Request):
    """หน้าจัดการ dataset"""
    return templates.TemplateResponse("dataset.html", {
        "request": request,
        "conversations": DEMO_DATA["conversations"]
    })

@app.get("/model", response_class=HTMLResponse)
async def model_page(request: Request):
    """หน้าข้อมูลโมเดล"""
    return templates.TemplateResponse("model.html", {
        "request": request,
        "model_info": DEMO_DATA["model_info"],
        "test_results": DEMO_DATA["test_results"]
    })

@app.get("/deploy", response_class=HTMLResponse)
async def deploy_page(request: Request):
    """หน้าจัดการ deployment"""
    return templates.TemplateResponse("deploy.html", {
        "request": request,
        "model_info": DEMO_DATA["model_info"]
    })

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/api/dataset")
async def get_dataset():
    """API สำหรับดึงข้อมูล dataset"""
    return {
        "conversations": DEMO_DATA["conversations"],
        "total_count": len(DEMO_DATA["conversations"]),
        "quality_score": 8.5
    }

@app.get("/api/model")
async def get_model_info():
    """API สำหรับดึงข้อมูลโมเดล"""
    return DEMO_DATA["model_info"]

@app.get("/api/test-results")
async def get_test_results():
    """API สำหรับดึงผลการทดสอบ"""
    return DEMO_DATA["test_results"]

@app.post("/api/conversation")
async def add_conversation(conversation: Conversation):
    """API สำหรับเพิ่มการสนทนาใหม่"""
    try:
        new_conv = {
            "conversations": [
                {"from": "human", "value": conversation.user_message},
                {"from": "gpt", "value": conversation.assistant_message}
            ]
        }
        
        DEMO_DATA["conversations"].append(new_conv)
        
        # Save to file
        with open("data/raw/sample_conversations.json", 'w', encoding='utf-8') as f:
            json.dump(DEMO_DATA["conversations"], f, ensure_ascii=False, indent=2)
        
        return {"status": "success", "message": "Conversation added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/deploy")
async def deploy_model():
    """API สำหรับ deploy โมเดล"""
    try:
        # Simulate deployment process
        deployment_result = {
            "status": "deploying",
            "deployment_id": f"deploy-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "steps": [
                {"step": "validation", "status": "completed"},
                {"step": "upload", "status": "completed"},
                {"step": "deployment", "status": "in_progress"},
                {"step": "testing", "status": "pending"}
            ]
        }
        
        return deployment_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/deployment-status/{deployment_id}")
async def get_deployment_status(deployment_id: str):
    """API สำหรับตรวจสอบสถานะ deployment"""
    # Simulate deployment status
    return {
        "deployment_id": deployment_id,
        "status": "completed",
        "endpoint": "https://ai-training-platform.openai.azure.com/",
        "model_name": "ai-training-platform-model-v1",
        "created_at": datetime.now().isoformat()
    }

@app.post("/api/upload-dataset")
async def upload_dataset(file: UploadFile = File(...)):
    """API สำหรับอัปโหลด dataset"""
    try:
        if not file.filename.endswith('.json'):
            raise HTTPException(status_code=400, detail="Only JSON files are allowed")
        
        # Read and validate file
        content = await file.read()
        data = json.loads(content.decode('utf-8'))
        
        # Validate format
        if not isinstance(data, list):
            raise HTTPException(status_code=400, detail="Invalid dataset format")
        
        # Save file
        file_path = f"data/raw/{file.filename}"
        with open(file_path, 'wb') as f:
            f.write(content)
        
        # Update demo data
        DEMO_DATA["conversations"] = data
        
        return {
            "status": "success",
            "message": f"Dataset uploaded successfully: {len(data)} conversations",
            "file_path": file_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/export-azure-format")
async def export_azure_format():
    """API สำหรับ export ข้อมูลเป็น Azure format"""
    try:
        azure_format = []
        for conv in DEMO_DATA["conversations"]:
            messages = []
            for msg in conv["conversations"]:
                role = "assistant" if msg["from"] == "gpt" else "user"
                messages.append({
                    "role": role,
                    "content": msg["value"]
                })
            azure_format.append({"messages": messages})
        
        # Save to file
        output_path = "outputs/datasets/azure_fine_tuning_data.jsonl"
        with open(output_path, 'w', encoding='utf-8') as f:
            for item in azure_format:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
        
        return {
            "status": "success",
            "message": f"Azure format exported: {len(azure_format)} conversations",
            "file_path": output_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Create necessary directories
    os.makedirs("templates", exist_ok=True)
    os.makedirs("static", exist_ok=True)
    os.makedirs("static/css", exist_ok=True)
    os.makedirs("static/js", exist_ok=True)
    
    # Run the application
    uvicorn.run(
        "web_app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
