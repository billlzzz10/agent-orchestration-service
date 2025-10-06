#!/usr/bin/env python3
"""Lightweight similarity analysis for prompt pairs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import List


def _load_dataset(dataset_path: Path) -> List[dict]:
    with dataset_path.open("r", encoding="utf-8") as file:
        return [json.loads(line) for line in file]


def main() -> int:
    try:
        import numpy as np
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
    except ModuleNotFoundError:
        print("⚠️ scikit-learn not installed; skipping similarity analysis.")
    dataset_path = Path("dataset.jsonl")
    if not dataset_path.exists():
        # Try alternative locations
        alt_paths = [
            Path(__file__).resolve().parent / "dataset.jsonl",
            Path(__file__).resolve().parent.parent / "dataset.jsonl"
        ]
        for alt_path in alt_paths:
            if alt_path.exists():
                dataset_path = alt_path
                break
        else:
            print(f"⚠️ Dataset not found at {dataset_path} or alternative locations")
            return 0

    data = _load_dataset(dataset_path)
    data = _load_dataset(dataset_path)
    queries = []
    targets = []
    for record in data:
        user_input = record.get("user_input", "")
        target_prompt = record.get("target_prompt", "")
        if not user_input or not target_prompt:
            print(f"⚠️ Skipping record with missing fields: {record}")
            continue
        queries.append(user_input)
        targets.append(target_prompt)
    all_texts = queries + targets
    vectorizer.fit(all_texts)

    query_vectors = vectorizer.transform(queries)
    target_vectors = vectorizer.transform(targets)

    similarities = cosine_similarity(query_vectors, target_vectors)
    best_matches = np.argmax(similarities, axis=1)
    best_scores = np.max(similarities, axis=1)

    total_pairs = len(queries)
    avg_similarity = float(np.mean(best_scores))
    worst_idxs = np.argsort(best_scores)[:10]

    print(f"\nTotal pairs      : {total_pairs}")
    print(f"Average similarity: {avg_similarity:.3f}\n")

    print("10 worst matches:")
    for idx in worst_idxs:
        print(f"- Q: {queries[idx]}")
        print(f"  A: {targets[best_matches[idx]]}")
        print(f"  Similarity: {best_scores[idx]:.3f}\n")

    results_path = Path(__file__).resolve().parent.parent / "results.json"
    with results_path.open("w", encoding="utf-8") as file:
        json.dump(
            {
                "total_pairs": total_pairs,
                "avg_similarity": avg_similarity,
                "worst_matches": [
                    {
                        "query": queries[idx],
                        "answer": targets[best_matches[idx]],
                        "similarity": float(best_scores[idx]),
                    }
                    for idx in worst_idxs
                ],
            },
            file,
            ensure_ascii=False,
            indent=2,
        )

    print(f"✅ Results saved to {results_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
