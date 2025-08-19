#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HF multi-dataset normalizer + filter + intent grouping + embedding clustering (numpy-only).
- Sources: UltraChat, OpenOrca, WizardLM Evol-Instruct, OpenHermes (best-effort), ShareGPT Vicuna unfiltered.
- Dependencies: datasets, pyarrow, numpy (and Python stdlib).
- Output: JSONL to stdout by default (safe: no files created). Use --out to write a file.

Example:
  python build_pairs.py --min-len 5 --max-len 512 --target 5000 --dim 4096 --k auto > pairs.jsonl
"""

import sys, os, re, json, math, argparse, hashlib, random, time
from typing import List, Dict, Iterable, Tuple, Optional
import numpy as np

try:
    from datasets import load_dataset, IterableDataset
except Exception as e:
    print(f"ERROR: 'datasets' is required. Install: pip install datasets pyarrow numpy\n{e}", file=sys.stderr)
    sys.exit(1)

# ----------------------------
# Utility
# ----------------------------

WORD_RE = re.compile(r"[A-Za-z0-9_]+", re.UNICODE)

def tokenize(text: str) -> List[str]:
    if not text:
        return []
    return [t.lower() for t in WORD_RE.findall(text)]

def count_tokens(text: str) -> int:
    return len(text.split())

def stable_hash(s: str) -> int:
    # 64-bit stable hash via blake2b
    return int.from_bytes(hashlib.blake2b(s.encode('utf-8'), digest_size=8).digest(), 'big', signed=False)

def hash_token(tok: str, dim: int) -> int:
    h = hashlib.blake2b(tok.encode('utf-8'), digest_size=8).digest()
    return int.from_bytes(h, 'big') % dim

def l2_normalize_rows(X: np.ndarray, eps: float = 1e-12) -> np.ndarray:
    norms = np.linalg.norm(X, axis=1, keepdims=True)
    norms = np.maximum(norms, eps)
    return X / norms

# ----------------------------
# Loading and normalization
# ----------------------------

def gen_ultrachat(max_take: int) -> Iterable[Dict]:
    # HuggingFaceH4/ultrachat_200k
    for split in ("train", "test"):
        try:
            ds = load_dataset("HuggingFaceH4/ultrachat_200k", split=split, streaming=True)
        except Exception:
            continue
        cnt = 0
        for ex in ds:
            msgs = ex.get("messages") or []
            # extract consecutive user->assistant pairs
            for i in range(len(msgs) - 1):
                a, b = msgs[i], msgs[i+1]
                if not a or not b:
                    continue
                if a.get("role") == "user" and b.get("role") in ("assistant", "system"):
                    instr = a.get("content") or ""
                    resp  = b.get("content") or ""
                    if instr and resp:
                        yield {
                            "source": "ultrachat",
                            "instruction": instr.strip(),
                            "context": None,
                            "response": resp.strip(),
                        }
                        cnt += 1
                        if cnt >= max_take:
                            break
            if cnt >= max_take:
                break

def gen_openorca(max_take: int) -> Iterable[Dict]:
    # Open-Orca/OpenOrca
    try:
        ds = load_dataset("Open-Orca/OpenOrca", split="train", streaming=True)
    except Exception:
        return
    cnt = 0
    for ex in ds:
        q = (ex.get("question") or "").strip()
        r = (ex.get("response") or "").strip()
        sys_prompt = (ex.get("system_prompt") or "").strip()
        if r and (q or sys_prompt):
            instr = q if q else ""
            ctx = sys_prompt if sys_prompt else None
            yield {
                "source": "openorca",
                "instruction": instr,
                "context": ctx,
                "response": r,
            }
            cnt += 1
            if cnt >= max_take:
                break

def gen_wizardlm(max_take: int) -> Iterable[Dict]:
    # WizardLM/WizardLM_evol_instruct_V2_196k
    try:
        ds = load_dataset("WizardLM/WizardLM_evol_instruct_V2_196k", split="train", streaming=True)
    except Exception:
        return
    cnt = 0
    for ex in ds:
        instr = (ex.get("instruction") or "").strip()
        resp  = (ex.get("output") or "").strip()
        if instr and resp:
            yield {
                "source": "wizardlm",
                "instruction": instr,
                "context": None,
                "response": resp,
            }
            cnt += 1
            if cnt >= max_take:
                break

def gen_sharegpt(max_take: int) -> Iterable[Dict]:
    # anon8231489123/ShareGPT_Vicuna_unfiltered
    try:
        ds = load_dataset("anon8231489123/ShareGPT_Vicuna_unfiltered", split="train", streaming=True)
    except Exception:
        return
    cnt = 0
    for ex in ds:
        conv = ex.get("conversations") or []
        for i in range(len(conv) - 1):
            a, b = conv[i], conv[i+1]
            if not a or not b:
                continue
            if (a.get("from") or "").lower() in ("human", "user") and (b.get("from") or "").lower() in ("gpt", "assistant", "chatgpt"):
                instr = (a.get("value") or "").strip()
                resp  = (b.get("value") or "").strip()
                if instr and resp:
                    yield {
                        "source": "sharegpt",
                        "instruction": instr,
                        "context": None,
                        "response": resp,
                    }
                    cnt += 1
                    if cnt >= max_take:
                        break
        if cnt >= max_take:
            break

def gen_openhermes(max_take: int) -> Iterable[Dict]:
    # Try multiple candidate IDs; skip silently if unavailable
    candidates = [
        "teknium/OpenHermes-2.5",
        "teknium/OpenHermes",
        "teknium/OpenHermes-2.5-ShareGPT",
    ]
    cnt_total = 0
    for dsid in candidates:
        if cnt_total >= max_take:
            break
        try:
            ds = load_dataset(dsid, split="train", streaming=True)
        except Exception:
            continue
        cnt = 0
        for ex in ds:
            # Handle either convo style or instruct style
            if "conversations" in ex:
                conv = ex["conversations"] or []
                for i in range(len(conv) - 1):
                    a, b = conv[i], conv[i+1]
                    if not a or not b:
                        continue
                    if (a.get("role") or a.get("from", "")).lower() in ("user", "human") and (b.get("role") or b.get("from", "")).lower() in ("assistant", "gpt", "chatgpt"):
                        instr = (a.get("content") or a.get("value") or "").strip()
                        resp  = (b.get("content") or b.get("value") or "").strip()
                        if instr and resp:
                            yield {"source": "openhermes", "instruction": instr, "context": None, "response": resp}
                            cnt += 1; cnt_total += 1
                            if cnt_total >= max_take or cnt >= max_take:
                                break
            else:
                instr = (ex.get("instruction") or "").strip()
                resp  = (ex.get("output") or ex.get("response") or "").strip()
                if instr and resp:
                    yield {"source": "openhermes", "instruction": instr, "context": None, "response": resp}
                    cnt += 1; cnt_total += 1
                    if cnt_total >= max_take or cnt >= max_take:
                        break

def gen_alpaca(max_take: int) -> Iterable[Dict]:
    # tatsu-lab/alpaca
    try:
        ds = load_dataset("tatsu-lab/alpaca", split="train", streaming=True)
    except Exception:
        return
    cnt = 0
    for ex in ds:
        instr = (ex.get("instruction") or "").strip()
        resp  = (ex.get("output") or "").strip()
        if instr and resp:
            yield {
                "source": "alpaca",
                "instruction": instr,
                "context": None,
                "response": resp,
            }
            cnt += 1
            if cnt >= max_take:
                break

def gen_dolly(max_take: int) -> Iterable[Dict]:
    # databricks/databricks-dolly-15k
    try:
        ds = load_dataset("databricks/databricks-dolly-15k", split="train", streaming=True)
    except Exception:
        return
    cnt = 0
    for ex in ds:
        instr = (ex.get("instruction") or "").strip()
        resp  = (ex.get("response") or "").strip()
        if instr and resp:
            yield {
                "source": "dolly",
                "instruction": instr,
                "context": None,
                "response": resp,
            }
            cnt += 1
            if cnt >= max_take:
                break

def gen_self_instruct(max_take: int) -> Iterable[Dict]:
    # yizhongw/self_instruct
    try:
        ds = load_dataset("yizhongw/self_instruct", split="train", streaming=True)
    except Exception:
        return
    cnt = 0
    for ex in ds:
        instr = (ex.get("instruction") or "").strip()
        resp  = (ex.get("output") or "").strip()
        if instr and resp:
            yield {
                "source": "self_instruct",
                "instruction": instr,
                "context": None,
                "response": resp,
            }
            cnt += 1
            if cnt >= max_take:
                break

def gen_code_alpaca(max_take: int) -> Iterable[Dict]:
    # sahil280114/codealpaca
    try:
        ds = load_dataset("sahil280114/codealpaca", split="train", streaming=True)
    except Exception:
        return
    cnt = 0
    for ex in ds:
        instr = (ex.get("instruction") or "").strip()
        resp  = (ex.get("output") or "").strip()
        if instr and resp:
            yield {
                "source": "code_alpaca",
                "instruction": instr,
                "context": None,
                "response": resp,
            }
            cnt += 1
            if cnt >= max_take:
                break

def gen_tulu(max_take: int) -> Iterable[Dict]:
    # allenai/tulu-v2-sft-mixture
    try:
        ds = load_dataset("allenai/tulu-v2-sft-mixture", split="train", streaming=True)
    except Exception:
        return
    cnt = 0
    for ex in ds:
        instr = (ex.get("instruction") or "").strip()
        resp  = (ex.get("output") or "").strip()
        if instr and resp:
            yield {
                "source": "tulu",
                "instruction": instr,
                "context": None,
                "response": resp,
            }
            cnt += 1
            if cnt >= max_take:
                break

# ----------------------------
# Filtering, grouping, dedup
# ----------------------------

INTENT_RULES = [
    ("code",      r"\b(code|python|javascript|function|class|api|regex|sql|pandas|numpy|bug|error|compile|algorithm)\b"),
    ("math",      r"\b(prove|theorem|equation|integral|derivative|algebra|geometry|probability|statistics|matrix|vector)\b"),
    ("reasoning", r"\b(riddle|logic|reason|puzzle|deduce|explain why|chain of thought|step by step)\b"),
    ("qa",        r"\b(who|what|when|where|why|how|compare|define|summarize|explain)\b"),
    ("creative",  r"\b(poem|story|lyrics|song|novel|character|creative|narrative)\b"),
    ("roleplay",  r"\b(roleplay|act as|simulate|persona|character)\b"),
    ("writing",   r"\b(rewrite|edit|improve|paraphrase|grammar|style|tone|email|essay)\b"),
    ("data",      r"\b(extract|table|csv|json|xml|schema|map fields|normalize)\b"),
    ("assistant", r"\b(schedule|remind|organize|plan|checklist|itinerary|steps)\b"),
]

INTENT_REGEX = [(label, re.compile(pat, re.IGNORECASE)) for label, pat in INTENT_RULES]

def detect_intent(text: str) -> str:
    if not text:
        return "other"
    for label, rx in INTENT_REGEX:
        if rx.search(text):
            return label
    return "other"

def passes_filters(instr: str, resp: str, ctx: Optional[str], min_len: int, max_len: int) -> bool:
    li = count_tokens(instr)
    lr = count_tokens(resp)
    if li < min_len or lr < min_len:
        return False
    if li > max_len or lr > max_len:
        return False
    # basic sanity: avoid extremely long lines (characters)
    if len(instr) > 8000 or len(resp) > 8000:
        return False
    return True

# ----------------------------
# Embedding (hashing TF-IDF) + KMeans
# ----------------------------

def build_hashing_tfidf(texts: List[str], dim: int = 4096) -> np.ndarray:
    n = len(texts)
    df = np.zeros(dim, dtype=np.int32)
    # First pass: DF buckets
    for t in texts:
        toks = tokenize(t)
        if not toks:
            continue
        buckets = set(hash_token(tok, dim) for tok in toks)
        for b in buckets:
            df[b] += 1
    idf = np.log((1.0 + n) / (1.0 + df)) + 1.0  # shape (dim,)
    # Second pass: TF buckets per doc
    X = np.zeros((n, dim), dtype=np.float32)
    for i, t in enumerate(texts):
        toks = tokenize(t)
        if not toks:
            continue
        tf_local = {}
        for tok in toks:
            b = hash_token(tok, dim)
            tf_local[b] = tf_local.get(b, 0) + 1
        if not tf_local:
            continue
        # log-tf
        for b, c in tf_local.items():
            X[i, b] = math.log1p(c) * idf[b]
    X = l2_normalize_rows(X)
    return X

def kmeans_pp_init(X: np.ndarray, k: int, rng: np.random.Generator) -> np.ndarray:
    n = X.shape[0]
    centroids = np.empty((k, X.shape[1]), dtype=X.dtype)
    # pick first centroid
    idx = rng.integers(0, n)
    centroids[0] = X[idx]
    # distances to nearest centroid
    d2 = np.sum((X - centroids[0])**2, axis=1)
    for c in range(1, k):
        probs = d2 / (d2.sum() + 1e-12)
        idx = rng.choice(n, p=probs)
        centroids[c] = X[idx]
        d2 = np.minimum(d2, np.sum((X - centroids[c])**2, axis=1))
    return centroids

def kmeans(X: np.ndarray, k: int, iters: int = 20, seed: int = 42) -> np.ndarray:
    rng = np.random.default_rng(seed)
    n = X.shape[0]
    if k <= 1:
        return np.zeros(n, dtype=np.int32)
    k = min(k, n)
    C = kmeans_pp_init(X, k, rng)
    labels = np.zeros(n, dtype=np.int32)
    for _ in range(iters):
        # assign
        # use cosine similarity since rows are L2-normalized
        sims = X @ C.T  # (n,k)
        labels = np.argmax(sims, axis=1)
        # update
        newC = np.zeros_like(C)
        counts = np.zeros(k, dtype=np.int32)
        for i in range(n):
            lab = labels[i]
            newC[lab] += X[i]
            counts[lab] += 1
        for j in range(k):
            if counts[j] > 0:
                newC[j] /= counts[j]
        # re-normalize centroids
        C = l2_normalize_rows(newC)
    return labels

# ----------------------------
# Main pipeline
# ----------------------------

def collect_pairs(target: int, per_source_cap: int, min_len: int, max_len: int) -> List[Dict]:
    gens = [
        gen_ultrachat,
        gen_openorca,
        gen_wizardlm,
        gen_openhermes,
        gen_sharegpt,
        gen_alpaca,
        gen_dolly,
        gen_self_instruct,
        gen_code_alpaca,
        gen_tulu,
    ]
    pairs: List[Dict] = []
    seen = set()
    successful_sources = 0
    
    print(f"🔍 Searching for datasets...", file=sys.stderr)
    
    for g in gens:
        if len(pairs) >= target:
            break
        take = min(per_source_cap, max(0, target - len(pairs)))
        
        source_name = g.__name__.replace('gen_', '')
        print(f"  Trying {source_name}...", file=sys.stderr)
        
        collected = 0
        for ex in g(take):
            instr = (ex["instruction"] or "").strip()
            resp  = (ex["response"] or "").strip()
            ctx   = (ex.get("context") or None)
            if not passes_filters(instr, resp, ctx, min_len, max_len):
                continue
            key = stable_hash(instr + "\n###\n" + resp)
            if key in seen:
                continue
            seen.add(key)
            pairs.append({
                "source": ex["source"],
                "instruction": instr,
                "context": ctx,
                "response": resp,
            })
            collected += 1
            if len(pairs) >= target:
                break
        
        if collected > 0:
            successful_sources += 1
            print(f"  ✅ {source_name}: {collected} pairs", file=sys.stderr)
        else:
            print(f"  ❌ {source_name}: failed", file=sys.stderr)
    
    print(f"📊 Found {successful_sources} successful sources, {len(pairs)} total pairs", file=sys.stderr)
    return pairs

def decide_k(n: int) -> int:
    # heuristic: sqrt(n/2), clipped to [8, 64]
    return int(np.clip(int(math.sqrt(max(2, n) / 2.0)), 8, 64))

def main():
    ap = argparse.ArgumentParser(description="Normalize, filter, group intents, and cluster HF instruct data.")
    ap.add_argument("--min-len", type=int, default=5, help="Minimum token length for both input and output.")
    ap.add_argument("--max-len", type=int, default=512, help="Maximum token length for both input and output.")
    ap.add_argument("--target", type=int, default=5000, help="Target number of pairs to collect (>=1000 recommended).")
    ap.add_argument("--per-source-cap", type=int, default=20000, help="Max examples to consider per source.")
    ap.add_argument("--dim", type=int, default=4096, help="Hashing TF-IDF dimension.")
    ap.add_argument("--k", type=str, default="auto", help="Cluster count: integer or 'auto'.")
    ap.add_argument("--seed", type=int, default=42, help="Random seed.")
    ap.add_argument("--out", type=str, default="", help="Output JSONL path (default: stdout).")
    args = ap.parse_args()

    start = time.time()
    pairs = collect_pairs(target=args.target, per_source_cap=args.per_source_cap, min_len=args.min_len, max_len=args.max_len)

    # Guarantee >=1000 if sources available: if not reached, try relaxing filters once
    if len(pairs) < 1000:
        print(f"⚠️  Only got {len(pairs)} pairs, trying with relaxed filters...", file=sys.stderr)
        # Relax and try again (add more per-source and wider length bounds)
        more = collect_pairs(
            target=max(1000, args.target),
            per_source_cap=max(args.per_source_cap, 50000),
            min_len=max(1, args.min_len // 2),
            max_len=max(args.max_len, 1024),
        )
        # Merge unique
        seen = set(stable_hash(p["instruction"] + "\n###\n" + p["response"]) for p in pairs)
        for p in more:
            key = stable_hash(p["instruction"] + "\n###\n" + p["response"])
            if key not in seen:
                pairs.append(p)
                seen.add(key)

    n = len(pairs)
    if n < 1000:
        print(f"WARNING: Collected only {n} pairs (<1000). Sources may be unavailable or blocked.", file=sys.stderr)

    # Intent grouping
    for p in pairs:
        text_for_intent = (p["instruction"] + " " + (p["context"] or "")).strip()
        p["intent"] = detect_intent(text_for_intent)

    # Embeddings + clustering
    texts = [(p["instruction"] + "\n" + (p["context"] or "") + "\n" + p["response"]).strip() for p in pairs]
    X = build_hashing_tfidf(texts, dim=args.dim)
    k = decide_k(n) if args.k == "auto" else max(1, int(args.k))
    labels = kmeans(X, k=k, iters=20, seed=args.seed)
    for p, lab in zip(pairs, labels):
        p["cluster"] = int(lab)

    # Output
    outfh = open(args.out, "w", encoding="utf-8") if args.out else sys.stdout
    for i, p in enumerate(pairs):
        rec = {
            "id": f"{p['source']}::{i}",
            "source": p["source"],
            "input": p["instruction"] if p["context"] is None else (p["instruction"] + "\n\n[CONTEXT]\n" + p["context"]),
            "output": p["response"],
            "intent": p["intent"],
            "cluster": p["cluster"],
        }
        outfh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    if args.out:
        outfh.close()

    # Stats to stderr only (won't pollute JSONL)
    elapsed = time.time() - start
    intents = {}
    for p in pairs:
        intents[p["intent"]] = intents.get(p["intent"], 0) + 1
    print(f"Done: {n} pairs | k={k} | dim={args.dim} | time={elapsed:.1f}s", file=sys.stderr)
    print("Intent distribution: " + ", ".join(f"{k}:{v}" for k, v in sorted(intents.items(), key=lambda x: -x[1])), file=sys.stderr)

if __name__ == "__main__":
    main()
