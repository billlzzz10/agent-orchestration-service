#!/usr/bin/env python3
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# 1) โหลด dataset
with open("dataset.jsonl", "r", encoding="utf-8") as f:
    data = [json.loads(line) for line in f]
queries = [rec["user_input"] for rec in data]
targets = [rec["target_prompt"] for rec in data]

# 2) สร้าง embedding ของ queries
model = SentenceTransformer("all-MiniLM-L6-v2")
query_embs = model.encode(queries, convert_to_numpy=True, show_progress_bar=True)

# 3) โหลด embeddings และ targets
target_embs = np.load("embeddings.npy")

# 4) คำนวณ similarity
similarities = cosine_similarity(query_embs, target_embs)
best_matches = np.argmax(similarities, axis=1)
best_scores = np.max(similarities, axis=1)

# 5) สรุปผลลัพธ์
total_pairs = len(queries)
avg_similarity = float(np.mean(best_scores))
worst_idxs = np.argsort(best_scores)[:10]

print(f"\nTotal pairs      : {total_pairs}")
print(f"Average similarity: {avg_similarity:.3f}\n")

print("10 worst matches:")
for wi in worst_idxs:
    print(f"- Q: {queries[wi]}")
    print(f"  A: {targets[best_matches[wi]]}")
    print(f"  Similarity: {best_scores[wi]:.3f}\n")

# 6) ตรวจสอบกับ gold_metrics.json (ถ้ามี)
try:
    with open("data/gold_metrics.json", "r", encoding="utf-8") as f:
        gold = json.load(f)
    delta = abs(avg_similarity - gold["avg_similarity"])
    assert total_pairs == gold["total"], "Mismatch in total pair count"
    assert delta < 0.001, f"Average similarity mismatch: Δ={delta:.5f}"
    print("✅ Metrics match gold standard.")
except Exception as e:
    print(f"⚠️  Gold metrics check failed: {e}")
