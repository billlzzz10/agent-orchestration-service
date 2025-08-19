#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Azure Fine-tuning Orchestrator
จัดการ workflow การ fine-tuning บน Azure OpenAI
"""

import json
import logging
import argparse
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
import requests
import azure.cognitiveservices.speech as speechsdk
from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient
from azure.ai.ml.entities import Data
from azure.storage.blob import BlobServiceClient
import openai

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AzureFineTuningOrchestrator:
    """จัดการ workflow การ fine-tuning บน Azure OpenAI"""
    
    def __init__(self, 
                 subscription_id: str,
                 resource_group: str,
                 workspace_name: str,
                 openai_endpoint: str,
                 openai_api_key: str):
        
        self.subscription_id = subscription_id
        self.resource_group = resource_group
        self.workspace_name = workspace_name
        self.openai_endpoint = openai_endpoint
        self.openai_api_key = openai_api_key
        
        # Initialize clients
        self.credential = DefaultAzureCredential()
        self.ml_client = MLClient(
            credential=self.credential,
            subscription_id=subscription_id,
            resource_group_name=resource_group,
            workspace_name=workspace_name
        )
        
        # Initialize OpenAI client
        self.openai_client = openai.AzureOpenAI(
            azure_endpoint=openai_endpoint,
            api_key=openai_api_key,
            api_version="2024-02-15-preview"
        )
        
        # Storage settings
        self.storage_account = None
        self.container_name = "fine-tuning-data"
        
    def setup_storage(self, storage_account_name: str):
        """ตั้งค่า Azure Storage"""
        logger.info(f"Setting up storage account: {storage_account_name}")
        
        try:
            # สร้าง BlobServiceClient
            account_url = f"https://{storage_account_name}.blob.core.windows.net"
            self.blob_service_client = BlobServiceClient(
                account_url=account_url,
                credential=self.credential
            )
            
            # สร้าง container ถ้ายังไม่มี
            container_client = self.blob_service_client.get_container_client(self.container_name)
            try:
                container_client.get_container_properties()
            except:
                container_client.create_container()
                logger.info(f"Created container: {self.container_name}")
            
            self.storage_account = storage_account_name
            logger.info("Storage setup completed")
            
        except Exception as e:
            logger.error(f"Error setting up storage: {e}")
            raise
    
    def upload_training_data(self, data_file: str) -> str:
        """อัปโหลดข้อมูล training ไปยัง Azure Storage"""
        logger.info(f"Uploading training data: {data_file}")
        
        try:
            # อัปโหลดไฟล์
            blob_name = f"training_data_{int(time.time())}.jsonl"
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=blob_name
            )
            
            with open(data_file, 'rb') as f:
                blob_client.upload_blob(f, overwrite=True)
            
            # สร้าง URL สำหรับ fine-tuning
            blob_url = f"https://{self.storage_account}.blob.core.windows.net/{self.container_name}/{blob_name}"
            
            logger.info(f"Training data uploaded: {blob_url}")
            return blob_url
            
        except Exception as e:
            logger.error(f"Error uploading training data: {e}")
            raise
    
    def create_fine_tuning_job(self, 
                              training_file_url: str,
                              model_name: str = "gpt-35-turbo",
                              hyperparameters: Optional[Dict[str, Any]] = None) -> str:
        """สร้าง fine-tuning job"""
        logger.info(f"Creating fine-tuning job for model: {model_name}")
        
        try:
            # Default hyperparameters
            if hyperparameters is None:
                hyperparameters = {
                    "n_epochs": 3,
                    "batch_size": 1,
                    "learning_rate_multiplier": 1.0
                }
            
            # สร้าง fine-tuning job
            job = self.openai_client.fine_tuning.jobs.create(
                training_file=training_file_url,
                model=model_name,
                hyperparameters=hyperparameters
            )
            
            job_id = job.id
            logger.info(f"Fine-tuning job created: {job_id}")
            
            return job_id
            
        except Exception as e:
            logger.error(f"Error creating fine-tuning job: {e}")
            raise
    
    def monitor_fine_tuning_job(self, job_id: str, check_interval: int = 60) -> Dict[str, Any]:
        """ติดตามสถานะ fine-tuning job"""
        logger.info(f"Monitoring fine-tuning job: {job_id}")
        
        while True:
            try:
                # ตรวจสอบสถานะ
                job = self.openai_client.fine_tuning.jobs.retrieve(job_id)
                
                logger.info(f"Job status: {job.status}")
                
                # บันทึกสถานะ
                status_info = {
                    "job_id": job_id,
                    "status": job.status,
                    "created_at": job.created_at,
                    "finished_at": job.finished_at,
                    "trained_tokens": job.trained_tokens,
                    "error": job.error
                }
                
                # ถ้าเสร็จแล้ว
                if job.status in ["succeeded", "failed", "cancelled"]:
                    logger.info(f"Job {job.status}: {job_id}")
                    
                    if job.status == "succeeded":
                        status_info["fine_tuned_model"] = job.fine_tuned_model
                    
                    return status_info
                
                # รอสักครู่แล้วตรวจสอบใหม่
                time.sleep(check_interval)
                
            except Exception as e:
                logger.error(f"Error monitoring job: {e}")
                raise
    
    def deploy_fine_tuned_model(self, model_name: str, deployment_name: str) -> str:
        """deploy fine-tuned model"""
        logger.info(f"Deploying model: {model_name} as {deployment_name}")
        
        try:
            # สร้าง deployment
            deployment = self.openai_client.deployments.create(
                model=model_name,
                deployment_name=deployment_name
            )
            
            deployment_id = deployment.id
            logger.info(f"Model deployed: {deployment_id}")
            
            return deployment_id
            
        except Exception as e:
            logger.error(f"Error deploying model: {e}")
            raise
    
    def test_fine_tuned_model(self, deployment_name: str, test_prompts: List[str]) -> List[Dict[str, Any]]:
        """ทดสอบ fine-tuned model"""
        logger.info(f"Testing fine-tuned model: {deployment_name}")
        
        results = []
        
        for prompt in test_prompts:
            try:
                # สร้าง response
                response = self.openai_client.chat.completions.create(
                    model=deployment_name,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=150,
                    temperature=0.7
                )
                
                result = {
                    "prompt": prompt,
                    "response": response.choices[0].message.content,
                    "usage": response.usage.dict(),
                    "model": response.model
                }
                
                results.append(result)
                logger.info(f"Test completed for prompt: {prompt[:50]}...")
                
            except Exception as e:
                logger.error(f"Error testing model: {e}")
                results.append({
                    "prompt": prompt,
                    "response": f"Error: {str(e)}",
                    "usage": None,
                    "model": deployment_name
                })
        
        return results
    
    def run_complete_workflow(self, 
                            data_file: str,
                            storage_account: str,
                            model_name: str = "gpt-35-turbo",
                            deployment_name: Optional[str] = None) -> Dict[str, Any]:
        """รัน workflow ครบถ้วน"""
        logger.info("Starting complete fine-tuning workflow...")
        
        workflow_results = {
            "start_time": time.time(),
            "steps": []
        }
        
        try:
            # Step 1: Setup storage
            logger.info("Step 1: Setting up storage...")
            self.setup_storage(storage_account)
            workflow_results["steps"].append({
                "step": "storage_setup",
                "status": "completed",
                "storage_account": storage_account
            })
            
            # Step 2: Upload training data
            logger.info("Step 2: Uploading training data...")
            training_file_url = self.upload_training_data(data_file)
            workflow_results["steps"].append({
                "step": "data_upload",
                "status": "completed",
                "training_file_url": training_file_url
            })
            
            # Step 3: Create fine-tuning job
            logger.info("Step 3: Creating fine-tuning job...")
            job_id = self.create_fine_tuning_job(training_file_url, model_name)
            workflow_results["steps"].append({
                "step": "job_creation",
                "status": "completed",
                "job_id": job_id
            })
            
            # Step 4: Monitor fine-tuning
            logger.info("Step 4: Monitoring fine-tuning...")
            job_status = self.monitor_fine_tuning_job(job_id)
            workflow_results["steps"].append({
                "step": "fine_tuning",
                "status": job_status["status"],
                "job_status": job_status
            })
            
            # Step 5: Deploy model (ถ้า fine-tuning สำเร็จ)
            if job_status["status"] == "succeeded":
                logger.info("Step 5: Deploying fine-tuned model...")
                
                if deployment_name is None:
                    deployment_name = f"ft-{model_name}-{int(time.time())}"
                
                deployment_id = self.deploy_fine_tuned_model(
                    job_status["fine_tuned_model"], 
                    deployment_name
                )
                
                workflow_results["steps"].append({
                    "step": "model_deployment",
                    "status": "completed",
                    "deployment_id": deployment_id,
                    "deployment_name": deployment_name
                })
                
                # Step 6: Test model
                logger.info("Step 6: Testing fine-tuned model...")
                test_prompts = [
                    "Hello! How are you today?",
                    "Can you help me with a coding problem?",
                    "What's your opinion on AI?"
                ]
                
                test_results = self.test_fine_tuned_model(deployment_name, test_prompts)
                workflow_results["steps"].append({
                    "step": "model_testing",
                    "status": "completed",
                    "test_results": test_results
                })
            
            workflow_results["end_time"] = time.time()
            workflow_results["total_duration"] = workflow_results["end_time"] - workflow_results["start_time"]
            workflow_results["status"] = "completed"
            
            logger.info("Fine-tuning workflow completed successfully!")
            return workflow_results
            
        except Exception as e:
            logger.error(f"Error in workflow: {e}")
            workflow_results["end_time"] = time.time()
            workflow_results["total_duration"] = workflow_results["end_time"] - workflow_results["start_time"]
            workflow_results["status"] = "failed"
            workflow_results["error"] = str(e)
            raise

def main():
    parser = argparse.ArgumentParser(description="Azure Fine-tuning Orchestrator")
    parser.add_argument("--subscription-id", required=True,
                       help="Azure subscription ID")
    parser.add_argument("--resource-group", required=True,
                       help="Azure resource group")
    parser.add_argument("--workspace-name", required=True,
                       help="Azure ML workspace name")
    parser.add_argument("--openai-endpoint", required=True,
                       help="Azure OpenAI endpoint")
    parser.add_argument("--openai-api-key", required=True,
                       help="Azure OpenAI API key")
    parser.add_argument("--storage-account", required=True,
                       help="Azure Storage account name")
    parser.add_argument("--data-file", required=True,
                       help="Training data file path")
    parser.add_argument("--model-name", default="gpt-35-turbo",
                       help="Base model name for fine-tuning")
    parser.add_argument("--deployment-name",
                       help="Deployment name for fine-tuned model")
    
    args = parser.parse_args()
    
    orchestrator = AzureFineTuningOrchestrator(
        subscription_id=args.subscription_id,
        resource_group=args.resource_group,
        workspace_name=args.workspace_name,
        openai_endpoint=args.openai_endpoint,
        openai_api_key=args.openai_api_key
    )
    
    try:
        results = orchestrator.run_complete_workflow(
            data_file=args.data_file,
            storage_account=args.storage_account,
            model_name=args.model_name,
            deployment_name=args.deployment_name
        )
        
        print("\n" + "="*50)
        print("🎉 Azure Fine-tuning Workflow Completed!")
        print("="*50)
        print(f"⏱️ Total duration: {results['total_duration']:.2f} seconds")
        print(f"📊 Status: {results['status']}")
        
        print("\n📋 Workflow Steps:")
        for step in results['steps']:
            print(f"✅ {step['step']}: {step['status']}")
        
        if results['status'] == 'completed':
            print("\n🚀 Fine-tuned Model Ready!")
            print("📝 Test Results:")
            test_step = next((s for s in results['steps'] if s['step'] == 'model_testing'), None)
            if test_step:
                for i, test in enumerate(test_step['test_results'][:2]):
                    print(f"\n{i+1}. Prompt: {test['prompt']}")
                    print(f"   Response: {test['response'][:100]}...")
        
    except Exception as e:
        logger.error(f"Error running workflow: {e}")
        raise

if __name__ == "__main__":
    main()
