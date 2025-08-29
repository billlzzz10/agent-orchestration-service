#!/usr/bin/env python3
import json
import numpy as np
from collections import defaultdict, Counter
import re
import os

class SimpleEmbedding:
    """Simple TF-IDF based embedding for clustering without external dependencies"""
    
    def __init__(self, max_features=1000):
        self.max_features = max_features
        self.vocabulary = {}
        self.idf = {}
    
    def tokenize(self, text):
        """แยกคำและทำความสะอาด"""
        text = text.lower()
        tokens = re.findall(r'\w+', text)
        return [token for token in tokens if len(token) > 2]
    
    def build_vocabulary(self, texts):
        """สร้าง vocabulary จากข้อความทั้งหมด"""
        word_counts = Counter()
        doc_counts = defaultdict(int)
        
        for text in texts:
            tokens = self.tokenize(text)
            unique_tokens = set(tokens)
            
            for token in tokens:
                word_counts[token] += 1
            
            for token in unique_tokens:
                doc_counts[token] += 1
        
        # เลือกคำที่พบบ่อยที่สุด
        most_common = word_counts.most_common(self.max_features)
        self.vocabulary = {word: idx for idx, (word, count) in enumerate(most_common)}
        
        # คำนวณ IDF
        total_docs = len(texts)
        for word in self.vocabulary:
            self.idf[word] = np.log(total_docs / (doc_counts[word] + 1))
    
    def vectorize(self, text):
        """แปลงข้อความเป็น vector"""
        tokens = self.tokenize(text)
        token_counts = Counter(tokens)
        
        vector = np.zeros(len(self.vocabulary))
        
        for token, count in token_counts.items():
            if token in self.vocabulary:
                idx = self.vocabulary[token]
                tf = count / len(tokens)  # Term frequency
                vector[idx] = tf * self.idf[token]  # TF-IDF
        
        # Normalize
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        
        return vector
    
    def fit_transform(self, texts):
        """ฝึกและแปลงข้อความเป็น vectors"""
        self.build_vocabulary(texts)
        
        vectors = []
        for text in texts:
            vectors.append(self.vectorize(text))
        
        return np.array(vectors)

class SimpleKMeans:
    """Simple K-Means implementation without sklearn"""
    
    def __init__(self, n_clusters=5, max_iters=100, random_state=42):
        self.n_clusters = n_clusters
        self.max_iters = max_iters
        self.random_state = random_state
        np.random.seed(random_state)
    
    def cosine_similarity(self, a, b):
        """คำนวณ cosine similarity"""
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        
        if norm_a == 0 or norm_b == 0:
            return 0
        
        return dot_product / (norm_a * norm_b)
    
    def fit(self, X):
        """ฝึก K-Means"""
        n_samples, n_features = X.shape
        
        # Initialize centroids randomly
        self.centroids = np.random.rand(self.n_clusters, n_features)
        
        for iteration in range(self.max_iters):
            # Assign points to clusters
            distances = np.zeros((n_samples, self.n_clusters))
            
            for i, point in enumerate(X):
                for j, centroid in enumerate(self.centroids):
                    # Use cosine distance (1 - cosine similarity)
                    distances[i, j] = 1 - self.cosine_similarity(point, centroid)
            
            labels = np.argmin(distances, axis=1)
            
            # Update centroids
            new_centroids = np.zeros_like(self.centroids)
            for k in range(self.n_clusters):
                cluster_points = X[labels == k]
                if len(cluster_points) > 0:
                    new_centroids[k] = np.mean(cluster_points, axis=0)
                else:
                    new_centroids[k] = self.centroids[k]
            
            # Check convergence
            if np.allclose(self.centroids, new_centroids, rtol=1e-4):
                break
                
            self.centroids = new_centroids
        
        self.labels_ = labels
        return self

class DatasetOverlapAnalyzer:
    def __init__(self):
        self.embedding = SimpleEmbedding()
        self.clustering = SimpleKMeans()
    
    def analyze_overlap(self, dataset_file="enhanced_dataset.jsonl"):
        """วิเคราะห์ overlap ระหว่าง datasets"""
        
        print("🔍 Analyzing Dataset Overlap with Clustering...")
        print("=" * 60)
        
        # โหลดข้อมูล
        records = self.load_dataset(dataset_file)
        if not records:
            print("❌ No data found!")
            return
        
        print(f"📊 Loaded {len(records)} records")
        
        # เตรียมข้อมูลสำหรับ clustering
        texts = []
        sources = []
        intents = []
        
        for record in records:
            combined_text = f"{record['user_input']} {record['target_prompt']}"
            texts.append(combined_text)
            sources.append(record.get('source', 'unknown'))
            intents.append(record.get('intent', 'general'))
        
        print("🔢 Creating embeddings...")
        vectors = self.embedding.fit_transform(texts)
        
        # Clustering
        # ใช้จำนวน cluster ไม่เกินจำนวน record ที่มีอยู่
        n_clusters = min(10, len(set(sources)), len(records))
        self.clustering = SimpleKMeans(n_clusters=n_clusters)
        self.clustering.fit(vectors)
        
        # วิเคราะห์ผลลัพธ์
        self.analyze_clusters(records, self.clustering.labels_, sources, intents)
        
        # คำนวณ similarity matrix ระหว่าง sources
        self.calculate_source_similarity(records, vectors, sources)
        
        return self.clustering.labels_
    
    def load_dataset(self, dataset_file):
        """โหลด dataset จากไฟล์"""
        records = []
        
        if not os.path.exists(dataset_file):
            print(f"⚠️  File not found: {dataset_file}")
            return records
        
        try:
            with open(dataset_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        records.append(json.loads(line))
        except Exception as e:
            print(f"❌ Error loading dataset: {e}")
        
        return records
    
    def analyze_clusters(self, records, labels, sources, intents):
        """วิเคราะห์ clusters"""
        
        print(f"\n📈 Cluster Analysis")
        print("-" * 40)
        
        cluster_info = defaultdict(lambda: {
            'sources': Counter(),
            'intents': Counter(),
            'records': []
        })
        
        for i, (record, label) in enumerate(zip(records, labels)):
            cluster_info[label]['sources'][sources[i]] += 1
            cluster_info[label]['intents'][intents[i]] += 1
            cluster_info[label]['records'].append(record)
        
        overlap_matrix = defaultdict(lambda: defaultdict(int))
        
        for cluster_id, info in cluster_info.items():
            print(f"\n🎯 Cluster {cluster_id} ({len(info['records'])} records):")
            
            # แสดง top sources
            print("  Top sources:")
            for source, count in info['sources'].most_common(3):
                percentage = count / len(info['records']) * 100
                print(f"    {source}: {count} ({percentage:.1f}%)")
            
            # แสดง top intents
            print("  Top intents:")
            for intent, count in info['intents'].most_common(3):
                percentage = count / len(info['records']) * 100
                print(f"    {intent}: {count} ({percentage:.1f}%)")
            
            # คำนวณ overlap
            sources_in_cluster = list(info['sources'].keys())
            for i, source1 in enumerate(sources_in_cluster):
                for source2 in sources_in_cluster[i+1:]:
                    overlap_matrix[source1][source2] += 1
                    overlap_matrix[source2][source1] += 1
            
            # แสดงตัวอย่าง prompts
            if info['records']:
                example = info['records'][0]
                print(f"  Example: {example['user_input'][:50]}...")
        
        # แสดง overlap matrix
        self.print_overlap_matrix(overlap_matrix)
        
        # บันทึกรายงาน
        self.save_cluster_report(cluster_info, overlap_matrix)
    
    def calculate_source_similarity(self, records, vectors, sources):
        """คำนวณ similarity ระหว่าง sources"""
        
        print(f"\n🔗 Source Similarity Analysis")
        print("-" * 40)
        
        # จัดกลุ่ม vectors ตาม source
        source_vectors = defaultdict(list)
        for vector, source in zip(vectors, sources):
            source_vectors[source].append(vector)
        
        # คำนวณ centroid ของแต่ละ source
        source_centroids = {}
        for source, vecs in source_vectors.items():
            source_centroids[source] = np.mean(vecs, axis=0)
        
        # คำนวณ similarity matrix
        sources_list = list(source_centroids.keys())
        similarity_matrix = np.zeros((len(sources_list), len(sources_list)))
        
        for i, source1 in enumerate(sources_list):
            for j, source2 in enumerate(sources_list):
                if i != j:
                    sim = self.clustering.cosine_similarity(
                        source_centroids[source1], 
                        source_centroids[source2]
                    )
                    similarity_matrix[i, j] = sim
                else:
                    similarity_matrix[i, j] = 1.0
        
        # แสดงผลลัพธ์
        print("Source similarity matrix:")
        print("Sources:", sources_list)
        
        for i, source1 in enumerate(sources_list):
            print(f"{source1}:")
            for j, source2 in enumerate(sources_list):
                if i != j:
                    sim = similarity_matrix[i, j]
                    print(f"  vs {source2}: {sim:.3f}")
    
    def print_overlap_matrix(self, overlap_matrix):
        """แสดง overlap matrix"""
        
        print(f"\n📊 Source Overlap Matrix")
        print("-" * 40)
        
        sources = list(overlap_matrix.keys())
        
        for source1 in sources:
            overlaps = []
            for source2 in sources:
                if source1 != source2:
                    overlap_count = overlap_matrix[source1][source2]
                    overlaps.append(f"{source2}: {overlap_count}")
            
            if overlaps:
                print(f"{source1}: {', '.join(overlaps)}")
    
    def save_cluster_report(self, cluster_info, overlap_matrix):
        """บันทึกรายงาน clustering"""
        
        report = {
            "clusters": {},
            "overlap_matrix": {},
            "summary": {
                "total_clusters": len(cluster_info),
                "total_overlaps": sum(sum(overlaps.values()) for overlaps in overlap_matrix.values()) // 2
            }
        }
        
        # แปลง cluster_info
        for cluster_id, info in cluster_info.items():
            report["clusters"][str(cluster_id)] = {
                "size": len(info['records']),
                "sources": dict(info['sources']),
                "intents": dict(info['intents']),
                "top_source": info['sources'].most_common(1)[0][0] if info['sources'] else None,
                "top_intent": info['intents'].most_common(1)[0][0] if info['intents'] else None
            }
        
        # แปลง overlap_matrix
        for source1, overlaps in overlap_matrix.items():
            report["overlap_matrix"][source1] = dict(overlaps)
        
        with open("cluster_analysis.json", "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ Cluster analysis saved to: cluster_analysis.json")

def main():
    analyzer = DatasetOverlapAnalyzer()
    
    # ตรวจสอบว่ามีไฟล์ enhanced_dataset.jsonl หรือไม่
    if os.path.exists("enhanced_dataset.jsonl"):
        analyzer.analyze_overlap("enhanced_dataset.jsonl")
    elif os.path.exists("dataset.jsonl"):
        analyzer.analyze_overlap("dataset.jsonl")
    else:
        print("❌ No dataset file found! Please run data processing first.")

if __name__ == "__main__":
    main()
