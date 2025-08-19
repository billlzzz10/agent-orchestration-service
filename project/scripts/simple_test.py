#!/usr/bin/env python3
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# 1) โหลด dataset
with open("dataset.jsonl", "r", encoding="utf-8") as f:
    data = [json.loads(line) for line in f]
queries = [rec["user_input"] for rec in data]
targets = [rec["target_prompt"] for rec in data]

# 2) สร้าง TF-IDF embeddings
vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
all_texts = queries + targets
vectorizer.fit(all_texts)

query_vectors = vectorizer.transform(queries)
target_vectors = vectorizer.transform(targets)

# 3) คำนวณ similarity
similarities = cosine_similarity(query_vectors, target_vectors)
best_matches = np.argmax(similarities, axis=1)
best_scores = np.max(similarities, axis=1)

# 4) สรุปผลลัพธ์
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

# 5) บันทึกผลลัพธ์
with open("results.json", "w", encoding="utf-8") as f:
    json.dump({
        "total_pairs": total_pairs,
        "avg_similarity": avg_similarity,
        "worst_matches": [
            {
                "query": queries[wi],
                "answer": targets[best_matches[wi]],
                "similarity": float(best_scores[wi])
            }
            for wi in worst_idxs
        ]
    }, f, ensure_ascii=False, indent=2)

print("✅ Results saved to results.json")
