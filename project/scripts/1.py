#!/usr/bin/env python3
import argparse
import csv
import json
import os

def main():
    parser = argparse.ArgumentParser(description="Convert raw JSON/CSV files to dataset.jsonl")
    parser.add_argument("input_folder", help="Folder containing .json or .csv files")
    args = parser.parse_args()

    records = []
    for fname in os.listdir(args.input_folder):
        path = os.path.join(args.input_folder, fname)
        if fname.lower().endswith(".json"):
            with open(path, "r", encoding="utf-8") as f:
                items = json.load(f)
                for rec in items:
                    records.append({
                        "user_input": rec["user_input"],
                        "target_prompt": rec["target_prompt"]
                    })
        elif fname.lower().endswith(".csv"):
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    records.append({
                        "user_input": row["user_input"],
                        "target_prompt": row["target_prompt"]
                    })
        elif fname.lower().endswith(".parquet"):
            print(f"⚠️  Parquet files not supported without pandas: {fname}")
            continue

    with open("dataset.jsonl", "w", encoding="utf-8") as out:
        for rec in records:
            out.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print(f"Total pairs: {len(records)}")

if __name__ == "__main__":
    main()
