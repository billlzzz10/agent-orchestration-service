#!/usr/bin/env python3
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# 1) โหลด dataset
with open("dataset.jsonl", "r", encoding="utf-8") as f:
    data = [json.loads(line) for line in f]
targets = [rec["target_prompt"] for rec in data]

# 2) สร้าง embedding
model = SentenceTransformer("all-MiniLM-L6-v2")
embs = model.encode(targets, convert_to_numpy=True, show_progress_bar=True)

# 3) บันทึก embeddings และ targets
np.save("embeddings.npy", embs)
with open("targets.pkl", "wb") as f:
    pickle.dump(targets, f)

print(f"Built embeddings with {len(targets)} vectors")
print(f"Embedding dimension: {embs.shape[1]}")
