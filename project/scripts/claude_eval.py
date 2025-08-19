#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Claude Response Evaluation Script
ประเมินคุณภาพการตอบกลับของ Claude
"""

import json
import sys
from typing import Dict, List, Any
import re

def evaluate_response(instruction: str, expected: str, actual: str) -> Dict[str, float]:
    """ประเมินคุณภาพการตอบกลับ"""
    scores = {}
    
    # 1. Completeness (ความครบถ้วน)
    expected_words = len(expected.split())
    actual_words = len(actual.split())
    if expected_words > 0:
        completeness = min(actual_words / expected_words, 1.0)
    else:
        completeness = 1.0 if actual_words > 0 else 0.0
    scores['completeness'] = completeness
    
    # 2. Relevance (ความเกี่ยวข้อง)
    # ตรวจสอบคำสำคัญใน instruction ที่ควรปรากฏใน response
    instruction_keywords = set(re.findall(r'\b\w+\b', instruction.lower()))
    response_keywords = set(re.findall(r'\b\w+\b', actual.lower()))
    if instruction_keywords:
        relevance = len(instruction_keywords & response_keywords) / len(instruction_keywords)
    else:
        relevance = 1.0
    scores['relevance'] = relevance
    
    # 3. Coherence (ความสอดคล้อง)
    # ตรวจสอบความยาวและโครงสร้าง
    if actual_words >= 10 and '.' in actual:
        coherence = 1.0
    elif actual_words >= 5:
        coherence = 0.7
    else:
        coherence = 0.3
    scores['coherence'] = coherence
    
    # 4. Helpfulness (ความช่วยเหลือ)
    # ตรวจสอบว่ามีคำที่แสดงความช่วยเหลือ
    helpful_words = ['help', 'assist', 'guide', 'explain', 'show', 'provide', 'suggest']
    helpful_count = sum(1 for word in helpful_words if word in actual.lower())
    helpfulness = min(helpful_count / 2, 1.0)
    scores['helpfulness'] = helpfulness
    
    # 5. Overall score
    scores['overall'] = sum(scores.values()) / len(scores)
    
    return scores

def main():
    if len(sys.argv) != 3:
        print("Usage: python claude_eval.py <test_data.jsonl> <claude_responses.jsonl>")
        sys.exit(1)
    
    test_file = sys.argv[1]
    responses_file = sys.argv[2]
    
    # โหลดข้อมูล
    test_data = []
    with open(test_file, 'r', encoding='utf-8') as f:
        for line in f:
            test_data.append(json.loads(line.strip()))
    
    responses = []
    with open(responses_file, 'r', encoding='utf-8') as f:
        for line in f:
            responses.append(json.loads(line.strip()))
    
    # ประเมิน
    total_scores = {'completeness': 0, 'relevance': 0, 'coherence': 0, 'helpfulness': 0, 'overall': 0}
    
    for i, (test_item, response_item) in enumerate(zip(test_data, responses)):
        instruction = test_item.get('input', '')
        expected = test_item.get('output', '')
        actual = response_item.get('response', '')
        
        scores = evaluate_response(instruction, expected, actual)
        
        for metric, score in scores.items():
            total_scores[metric] += score
        
        if i < 5:  # แสดงตัวอย่าง 5 อันแรก
            print(f"Sample {i+1}: {scores['overall']:.3f}")
    
    # คำนวณค่าเฉลี่ย
    n = len(test_data)
    avg_scores = {metric: score/n for metric, score in total_scores.items()}
    
    print("\n📊 EVALUATION RESULTS:")
    print("=" * 40)
    for metric, score in avg_scores.items():
        print(f"{metric:12}: {score:.3f}")
    
    # บันทึกผลลัพธ์
    results = {
        'total_samples': n,
        'average_scores': avg_scores,
        'evaluation_timestamp': str(datetime.now())
    }
    
    with open('evaluation_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Results saved to evaluation_results.json")

if __name__ == "__main__":
    from datetime import datetime
    main()
