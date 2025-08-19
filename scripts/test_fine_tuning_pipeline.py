#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Fine-tuning Pipeline
ทดสอบ pipeline การ fine-tuning ครบถ้วน
"""

import json
import logging
import argparse
import time
from pathlib import Path
from typing import List, Dict, Any
import subprocess
import sys

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FineTuningPipelineTester:
    """ทดสอบ Fine-tuning Pipeline ครบถ้วน"""
    
    def __init__(self, test_dir: str = "test_outputs"):
        self.test_dir = Path(test_dir)
        self.test_dir.mkdir(parents=True, exist_ok=True)
        
        # Test results
        self.test_results = {
            "start_time": time.time(),
            "tests": [],
            "overall_status": "pending"
        }
    
    def run_test(self, test_name: str, command: List[str], timeout: int = 300) -> Dict[str, Any]:
        """รัน test command"""
        logger.info(f"Running test: {test_name}")
        
        test_result = {
            "test_name": test_name,
            "command": " ".join(command),
            "status": "running",
            "start_time": time.time()
        }
        
        try:
            # รัน command
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            test_result["end_time"] = time.time()
            test_result["duration"] = test_result["end_time"] - test_result["start_time"]
            test_result["return_code"] = result.returncode
            test_result["stdout"] = result.stdout
            test_result["stderr"] = result.stderr
            
            if result.returncode == 0:
                test_result["status"] = "passed"
                logger.info(f"✅ Test passed: {test_name}")
            else:
                test_result["status"] = "failed"
                logger.error(f"❌ Test failed: {test_name}")
                logger.error(f"Error: {result.stderr}")
            
        except subprocess.TimeoutExpired:
            test_result["status"] = "timeout"
            test_result["error"] = f"Test timed out after {timeout} seconds"
            logger.error(f"⏰ Test timeout: {test_name}")
            
        except Exception as e:
            test_result["status"] = "error"
            test_result["error"] = str(e)
            logger.error(f"💥 Test error: {test_name} - {e}")
        
        return test_result
    
    def test_dataset_preparation(self) -> Dict[str, Any]:
        """ทดสอบการเตรียม dataset"""
        logger.info("Testing dataset preparation...")
        
        # สร้าง test data
        test_data = [
            {
                "conversations": [
                    {"from": "human", "value": "Hello! How are you today?"},
                    {"from": "gpt", "value": "Hello! I'm doing great, thank you for asking. How about you?"}
                ]
            },
            {
                "conversations": [
                    {"from": "human", "value": "Can you help me with Python programming?"},
                    {"from": "gpt", "value": "Of course! I'd be happy to help you with Python programming. What specific question do you have?"}
                ]
            }
        ]
        
        # บันทึก test data
        test_data_file = self.test_dir / "test_data.json"
        with open(test_data_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)
        
        # รัน dataset preparation
        command = [
            sys.executable, "scripts/azure_fine_tuning_prep.py",
            "--output-dir", str(self.test_dir / "azure_fine_tuning")
        ]
        
        return self.run_test("Dataset Preparation", command)
    
    def test_opensource_model_demo(self) -> Dict[str, Any]:
        """ทดสอบ OpenSource model demo"""
        logger.info("Testing OpenSource model demo...")
        
        # รัน demo ด้วย prompts สั้นๆ
        command = [
            sys.executable, "scripts/opensource_model_demo.py",
            "--model", "microsoft/DialoGPT-small",  # ใช้ model เล็กเพื่อความเร็ว
            "--prompts", "Hello!", "How are you?",
            "--output-gif", "test_demo.gif"
        ]
        
        return self.run_test("OpenSource Model Demo", command, timeout=600)
    
    def test_azure_orchestrator_simulation(self) -> Dict[str, Any]:
        """จำลองการทดสอบ Azure orchestrator (ไม่ต้องใช้ Azure จริง)"""
        logger.info("Testing Azure orchestrator simulation...")
        
        # สร้าง simulation script
        simulation_script = self.test_dir / "azure_simulation.py"
        
        simulation_code = '''
#!/usr/bin/env python3
import json
import time
import sys
from pathlib import Path

def simulate_azure_workflow():
    """จำลอง Azure workflow"""
    print("🚀 Starting Azure Fine-tuning Simulation...")
    
    # Simulate steps
    steps = [
        ("Storage Setup", 2),
        ("Data Upload", 3),
        ("Job Creation", 2),
        ("Fine-tuning", 5),
        ("Model Deployment", 2),
        ("Testing", 3)
    ]
    
    results = {"steps": []}
    
    for step_name, duration in steps:
        print(f"⏳ {step_name}...")
        time.sleep(duration)
        print(f"✅ {step_name} completed")
        
        results["steps"].append({
            "step": step_name,
            "status": "completed",
            "duration": duration
        })
    
    print("🎉 Azure simulation completed successfully!")
    
    # Save results
    output_file = Path("test_outputs/azure_simulation_results.json")
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    return results

if __name__ == "__main__":
    simulate_azure_workflow()
'''
        
        with open(simulation_script, 'w') as f:
            f.write(simulation_code)
        
        # รัน simulation
        command = [sys.executable, str(simulation_script)]
        return self.run_test("Azure Orchestrator Simulation", command)
    
    def test_web_application(self) -> Dict[str, Any]:
        """ทดสอบ web application"""
        logger.info("Testing web application...")
        
        # สร้าง simple web app test
        web_test_script = self.test_dir / "web_app_test.py"
        
        web_test_code = '''
#!/usr/bin/env python3
import requests
import time
import subprocess
import sys
from pathlib import Path

def test_web_app():
    """ทดสอบ web application"""
    print("🌐 Testing Web Application...")
    
    # Start web app in background
    web_app_process = subprocess.Popen([
        sys.executable, "-m", "uvicorn", "web_app:app", 
        "--host", "127.0.0.1", "--port", "8000"
    ])
    
    try:
        # Wait for app to start
        time.sleep(5)
        
        # Test endpoints
        base_url = "http://127.0.0.1:8000"
        
        # Test health check
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print(f"❌ Health check failed: {response.status_code}")
        
        # Test main page
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print("✅ Main page loaded")
        else:
            print(f"❌ Main page failed: {response.status_code}")
        
        print("🎉 Web application test completed!")
        
    finally:
        # Stop web app
        web_app_process.terminate()
        web_app_process.wait()

if __name__ == "__main__":
    test_web_app()
'''
        
        with open(web_test_script, 'w') as f:
            f.write(web_test_code)
        
        # รัน web app test
        command = [sys.executable, str(web_test_script)]
        return self.run_test("Web Application", command, timeout=120)
    
    def run_all_tests(self) -> Dict[str, Any]:
        """รัน test ทั้งหมด"""
        logger.info("Starting comprehensive fine-tuning pipeline tests...")
        
        # รัน tests
        tests = [
            self.test_dataset_preparation(),
            self.test_opensource_model_demo(),
            self.test_azure_orchestrator_simulation(),
            self.test_web_application()
        ]
        
        self.test_results["tests"] = tests
        self.test_results["end_time"] = time.time()
        self.test_results["total_duration"] = self.test_results["end_time"] - self.test_results["start_time"]
        
        # ตรวจสอบ overall status
        passed_tests = sum(1 for test in tests if test["status"] == "passed")
        total_tests = len(tests)
        
        if passed_tests == total_tests:
            self.test_results["overall_status"] = "passed"
        elif passed_tests > 0:
            self.test_results["overall_status"] = "partial"
        else:
            self.test_results["overall_status"] = "failed"
        
        # บันทึกผลลัพธ์
        results_file = self.test_dir / "test_results.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, ensure_ascii=False, indent=2)
        
        return self.test_results
    
    def print_summary(self):
        """พิมพ์สรุปผลการทดสอบ"""
        print("\n" + "="*60)
        print("🎯 Fine-tuning Pipeline Test Summary")
        print("="*60)
        
        print(f"📊 Overall Status: {self.test_results['overall_status'].upper()}")
        print(f"⏱️ Total Duration: {self.test_results['total_duration']:.2f} seconds")
        print(f"🧪 Total Tests: {len(self.test_results['tests'])}")
        
        passed = sum(1 for test in self.test_results['tests'] if test['status'] == 'passed')
        failed = sum(1 for test in self.test_results['tests'] if test['status'] == 'failed')
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        
        print("\n📋 Test Details:")
        for test in self.test_results['tests']:
            status_icon = "✅" if test['status'] == 'passed' else "❌"
            print(f"{status_icon} {test['test_name']}: {test['status']} ({test.get('duration', 0):.2f}s)")
        
        print(f"\n📁 Results saved to: {self.test_dir}/test_results.json")

def main():
    parser = argparse.ArgumentParser(description="Test Fine-tuning Pipeline")
    parser.add_argument("--test-dir", default="test_outputs",
                       help="Test output directory")
    parser.add_argument("--skip-web", action="store_true",
                       help="Skip web application test")
    
    args = parser.parse_args()
    
    tester = FineTuningPipelineTester(args.test_dir)
    
    try:
        results = tester.run_all_tests()
        tester.print_summary()
        
        # Exit with appropriate code
        if results['overall_status'] == 'passed':
            sys.exit(0)
        elif results['overall_status'] == 'partial':
            sys.exit(1)
        else:
            sys.exit(2)
            
    except Exception as e:
        logger.error(f"Error running tests: {e}")
        sys.exit(3)

if __name__ == "__main__":
    main()
