#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dataset Quality Evaluation
ประเมินคุณภาพ dataset ที่สร้างจาก build_pairs.py โดยใช้การวิเคราะห์แบบออฟไลน์
"""

import json
import sys
from typing import List, Dict, Any
# from google.cloud import aiplatform
# from google.cloud.aiplatform import evaluation

def load_dataset(file_path: str) -> List[Dict[str, Any]]:
    """โหลด dataset จาก JSONL file"""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line.strip()))
    return data

def analyze_dataset_quality(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """วิเคราะห์คุณภาพ dataset"""
    analysis = {
        'total_pairs': len(data),
        'sources': {},
        'intents': {},
        'clusters': {},
        'length_stats': {
            'input': {'min': float('inf'), 'max': 0, 'avg': 0},
            'output': {'min': float('inf'), 'max': 0, 'avg': 0}
        },
        'quality_metrics': {}
    }
    
    total_input_len = 0
    total_output_len = 0
    
    for item in data:
        # Count sources
        source = item.get('source', 'unknown')
        analysis['sources'][source] = analysis['sources'].get(source, 0) + 1
        
        # Count intents
        intent = item.get('intent', 'unknown')
        analysis['intents'][intent] = analysis['intents'].get(intent, 0) + 1
        
        # Count clusters
        cluster = item.get('cluster', -1)
        analysis['clusters'][cluster] = analysis['clusters'].get(cluster, 0) + 1
        
        # Length analysis
        input_text = item.get('input', '')
        output_text = item.get('output', '')
        
        input_len = len(input_text.split())
        output_len = len(output_text.split())
        
        total_input_len += input_len
        total_output_len += output_len
        
        analysis['length_stats']['input']['min'] = min(analysis['length_stats']['input']['min'], input_len)
        analysis['length_stats']['input']['max'] = max(analysis['length_stats']['input']['max'], input_len)
        analysis['length_stats']['output']['min'] = min(analysis['length_stats']['output']['min'], output_len)
        analysis['length_stats']['output']['max'] = max(analysis['length_stats']['output']['max'], output_len)
    
    # Calculate averages
    if data:
        analysis['length_stats']['input']['avg'] = total_input_len / len(data)
        analysis['length_stats']['output']['avg'] = total_output_len / len(data)
    
    # Quality metrics
    analysis['quality_metrics'] = {
        'diversity_score': len(analysis['intents']) / 10.0,  # Normalized by expected intents
        'balance_score': min(analysis['intents'].values()) / max(analysis['intents'].values()) if analysis['intents'] else 0,
        'coverage_score': len(analysis['sources']) / 10.0,  # Normalized by expected sources
        'cluster_efficiency': len(analysis['clusters']) / len(data) if data else 0
    }
    
    return analysis

def print_analysis(analysis: Dict[str, Any]):
    """พิมพ์ผลการวิเคราะห์"""
    print("=" * 60)
    print("📊 DATASET QUALITY ANALYSIS")
    print("=" * 60)
    
    print(f"\n📈 Basic Statistics:")
    print(f"  Total pairs: {analysis['total_pairs']:,}")
    print(f"  Unique sources: {len(analysis['sources'])}")
    print(f"  Unique intents: {len(analysis['intents'])}")
    print(f"  Unique clusters: {len(analysis['clusters'])}")
    
    print(f"\n📝 Length Statistics:")
    input_stats = analysis['length_stats']['input']
    output_stats = analysis['length_stats']['output']
    print(f"  Input:  {input_stats['min']}-{input_stats['max']} tokens (avg: {input_stats['avg']:.1f})")
    print(f"  Output: {output_stats['min']}-{output_stats['max']} tokens (avg: {output_stats['avg']:.1f})")
    
    print(f"\n🏷️  Intent Distribution:")
    for intent, count in sorted(analysis['intents'].items(), key=lambda x: x[1], reverse=True):
        percentage = (count / analysis['total_pairs']) * 100
        print(f"  {intent:12}: {count:4d} ({percentage:5.1f}%)")
    
    print(f"\n📚 Source Distribution:")
    for source, count in sorted(analysis['sources'].items(), key=lambda x: x[1], reverse=True):
        percentage = (count / analysis['total_pairs']) * 100
        print(f"  {source:12}: {count:4d} ({percentage:5.1f}%)")
    
    print(f"\n🎯 Quality Metrics:")
    metrics = analysis['quality_metrics']
    print(f"  Diversity Score:    {metrics['diversity_score']:.3f}")
    print(f"  Balance Score:      {metrics['balance_score']:.3f}")
    print(f"  Coverage Score:     {metrics['coverage_score']:.3f}")
    print(f"  Cluster Efficiency: {metrics['cluster_efficiency']:.3f}")
    
    # Overall score
    overall_score = sum(metrics.values()) / len(metrics)
    print(f"\n⭐ Overall Quality Score: {overall_score:.3f}/1.0")
    
    if overall_score >= 0.8:
        print("🎉 Excellent dataset quality!")
    elif overall_score >= 0.6:
        print("👍 Good dataset quality")
    elif overall_score >= 0.4:
        print("⚠️  Fair dataset quality - consider improvements")
    else:
        print("❌ Poor dataset quality - needs significant improvements")

def main():
    if len(sys.argv) != 2:
        print("Usage: python evaluate_dataset.py <dataset.jsonl>")
        print("Example: python evaluate_dataset.py test_pairs.jsonl")
        sys.exit(1)
    
    dataset_file = sys.argv[1]
    
    try:
        print(f"🔍 Loading dataset from {dataset_file}...")
        data = load_dataset(dataset_file)
        
        print(f"📊 Analyzing {len(data)} pairs...")
        analysis = analyze_dataset_quality(data)
        
        print_analysis(analysis)
        
        # Save analysis to file
        output_file = dataset_file.replace('.jsonl', '_analysis.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, ensure_ascii=False, indent=2)
        print(f"\n💾 Analysis saved to {output_file}")
        
    except FileNotFoundError:
        print(f"❌ Error: File {dataset_file} not found")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
