#!/usr/bin/env python3
"""Merge available classification shards and validate the resulting manifest."""
import argparse
import json
import sys
from pathlib import Path

from validate_classification import validate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1], help="repository root")
    args = parser.parse_args()
    root = args.root.resolve()
    shard_dir = root / "classification/final"
    rows = []
    for path in sorted(shard_dir.glob("shard-*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            print(f"ERROR: cannot read {path.name}: {exc}", file=sys.stderr)
            return 1
        if isinstance(data, dict):
            data = data.get("questions", data.get("records"))
        if not isinstance(data, list) or any(not isinstance(row, dict) for row in data):
            print(f"ERROR: {path.name} must contain a list of question objects", file=sys.stderr)
            return 1
        rows.extend(data)
    rows.sort(key=lambda r: (str(r.get("exam_type", "")), str(r.get("source_paper", "")), int(r.get("source_number", -1)) if isinstance(r.get("source_number"), int) else -1))
    output = shard_dir / "final-manifest.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Merged {len(rows)} records from {len(list(shard_dir.glob('shard-*.json')))} shard(s) into {output.relative_to(root)}")
    return validate(root, output)

if __name__ == "__main__":
    main()
