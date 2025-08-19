#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenSource Model Demo with GIF Export
สาธิตการใช้ OpenSource models พร้อม export เป็น GIF
"""

import json
import logging
import argparse
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
import requests
from PIL import Image, ImageDraw, ImageFont
import imageio
import numpy as np
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OpenSourceModelDemo:
    """สาธิตการใช้ OpenSource models พร้อม GIF export"""
    
    def __init__(self, model_name: str = "microsoft/DialoGPT-medium"):
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.generator = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # GIF settings
        self.gif_frames = []
        self.frame_delay = 0.5  # seconds
        
    def load_model(self):
        """โหลด OpenSource model"""
        logger.info(f"Loading model: {self.model_name}")
        
        try:
            # โหลด tokenizer และ model
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            
            # ย้ายไป GPU ถ้ามี
            self.model.to(self.device)
            
            # สร้าง pipeline
            self.generator = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if self.device == "cuda" else -1
            )
            
            logger.info(f"Model loaded successfully on {self.device}")
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def generate_response(self, prompt: str, max_length: int = 100) -> str:
        """สร้าง response จาก model"""
        try:
            # Encode input
            inputs = self.tokenizer.encode(prompt, return_tensors="pt")
            inputs = inputs.to(self.device)
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=max_length,
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # ตัดเอาเฉพาะส่วนใหม่
            response = response[len(prompt):].strip()
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "Sorry, I couldn't generate a response."
    
    def create_text_frame(self, text: str, width: int = 800, height: int = 400) -> Image.Image:
        """สร้าง frame สำหรับ GIF"""
        # สร้างภาพ
        img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(img)
        
        # ใช้ font
        try:
            font = ImageFont.truetype("arial.ttf", 16)
        except:
            font = ImageFont.load_default()
        
        # แบ่งข้อความเป็นบรรทัด
        lines = []
        words = text.split()
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            bbox = draw.textbbox((0, 0), test_line, font=font)
            text_width = bbox[2] - bbox[0]
            
            if text_width <= width - 40:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        # วาดข้อความ
        y_position = 20
        for line in lines:
            draw.text((20, y_position), line, fill='black', font=font)
            y_position += 25
        
        return img
    
    def add_frame_to_gif(self, text: str):
        """เพิ่ม frame ลงใน GIF"""
        frame = self.create_text_frame(text)
        self.gif_frames.append(frame)
    
    def save_gif(self, filename: str = "model_demo.gif"):
        """บันทึก GIF"""
        if not self.gif_frames:
            logger.warning("No frames to save")
            return
        
        # สร้าง output directory
        output_dir = Path("outputs/gifs")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filepath = output_dir / filename
        
        # บันทึก GIF
        imageio.mimsave(
            filepath,
            self.gif_frames,
            duration=self.frame_delay,
            loop=0
        )
        
        logger.info(f"GIF saved to: {filepath}")
    
    def demo_conversation(self, prompts: List[str]) -> List[Dict[str, str]]:
        """สาธิตการสนทนากับ model"""
        if not self.generator:
            self.load_model()
        
        conversation = []
        
        # เพิ่ม frame เริ่มต้น
        self.add_frame_to_gif("🤖 OpenSource Model Demo\n\nStarting conversation...")
        
        for i, prompt in enumerate(prompts):
            logger.info(f"Processing prompt {i+1}/{len(prompts)}: {prompt[:50]}...")
            
            # แสดง prompt
            prompt_frame = f"👤 User: {prompt}"
            self.add_frame_to_gif(prompt_frame)
            
            # สร้าง response
            start_time = time.time()
            response = self.generate_response(prompt)
            generation_time = time.time() - start_time
            
            # แสดง response
            response_frame = f"👤 User: {prompt}\n\n🤖 Assistant: {response}\n\n⏱️ Generated in {generation_time:.2f}s"
            self.add_frame_to_gif(response_frame)
            
            # บันทึกการสนทนา
            conversation.append({
                "prompt": prompt,
                "response": response,
                "generation_time": generation_time
            })
            
            # รอสักครู่
            time.sleep(0.5)
        
        return conversation
    
    def load_demo_prompts(self) -> List[str]:
        """โหลด prompts สำหรับ demo"""
        demo_prompts = [
            "Hello! How are you today?",
            "Can you help me with a coding problem?",
            "What's the weather like?",
            "Tell me a joke",
            "Explain quantum computing in simple terms",
            "Write a short poem about AI",
            "What are the benefits of renewable energy?",
            "How can I improve my productivity?",
            "Recommend a good book to read",
            "What's your opinion on artificial intelligence?"
        ]
        
        return demo_prompts
    
    def run_demo(self, custom_prompts: Optional[List[str]] = None) -> Dict[str, Any]:
        """รัน demo หลัก"""
        logger.info("Starting OpenSource Model Demo...")
        
        # โหลด prompts
        if custom_prompts:
            prompts = custom_prompts
        else:
            prompts = self.load_demo_prompts()
        
        # รันการสนทนา
        conversation = self.demo_conversation(prompts)
        
        # บันทึก GIF
        self.save_gif()
        
        # สร้างผลลัพธ์
        results = {
            "model_name": self.model_name,
            "total_prompts": len(prompts),
            "conversation": conversation,
            "avg_generation_time": np.mean([conv["generation_time"] for conv in conversation]),
            "total_generation_time": sum([conv["generation_time"] for conv in conversation]),
            "gif_frames": len(self.gif_frames)
        }
        
        # บันทึกผลลัพธ์
        output_dir = Path("outputs")
        output_dir.mkdir(exist_ok=True)
        
        with open(output_dir / "demo_results.json", 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        logger.info("Demo completed successfully!")
        return results

def main():
    parser = argparse.ArgumentParser(description="OpenSource Model Demo with GIF Export")
    parser.add_argument("--model", default="microsoft/DialoGPT-medium",
                       help="Model name to use for demo")
    parser.add_argument("--prompts", nargs="+",
                       help="Custom prompts for demo")
    parser.add_argument("--output-gif", default="model_demo.gif",
                       help="Output GIF filename")
    
    args = parser.parse_args()
    
    demo = OpenSourceModelDemo(args.model)
    
    try:
        results = demo.run_demo(args.prompts)
        
        print("\n" + "="*50)
        print("🎉 OpenSource Model Demo Completed!")
        print("="*50)
        print(f"🤖 Model: {results['model_name']}")
        print(f"📝 Total prompts: {results['total_prompts']}")
        print(f"⏱️ Avg generation time: {results['avg_generation_time']:.2f}s")
        print(f"🎬 GIF frames: {results['gif_frames']}")
        print(f"📁 Output files:")
        print(f"   - GIF: outputs/gifs/{args.output_gif}")
        print(f"   - Results: outputs/demo_results.json")
        
        print("\n📋 Sample conversation:")
        for i, conv in enumerate(results['conversation'][:3]):
            print(f"\n{i+1}. User: {conv['prompt']}")
            print(f"   Assistant: {conv['response'][:100]}...")
        
    except Exception as e:
        logger.error(f"Error running demo: {e}")
        raise

if __name__ == "__main__":
    main()
