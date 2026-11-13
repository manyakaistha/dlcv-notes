#!/usr/bin/env python3
"""Validate classification/final/final-manifest.json against extracted papers."""
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

QUESTION_RE = re.compile(
    r"^###\s+Question\s+(\d+)\s*\n\s*\n"
    r"\*\*Question ID:\*\*\s*`([^`]+)`\s*·\s*"
    r"\*\*Type:\*\*\s*([^·\n]+?)\s*·\s*"
    r"\*\*Marks:\*\*\s*(\d+(?:\.\d+)?)\s*$", re.M
)
REQUIRED = {
    "source_paper": str, "question_id": str, "source_number": int,
    "marks": (int, float), "exam_type": str, "primary_week": int,
    "related_weeks": list, "topic_id": str, "confidence": str,
    "rationale": str, "flag_for_review": bool,
}


def extract_universe(root):
    papers = {}
    declared_total = None
    index = root / "sources/extraction-meta/EXTRACTION_INDEX.md"
    if index.exists():
        text = index.read_text(encoding="utf-8")
        match = re.search(r"(\d+) papers\s*·\s*(\d+) academic question entries", text)
        if match:
            declared_total = int(match.group(2))
    for path in sorted((root / "sources/exam-papers").glob("da5006_*.md")):
        exam = re.search(r"_(Q1|Q2|ET)_", path.name)
        if not exam:
            continue
        text = path.read_text(encoding="utf-8")
        for m in QUESTION_RE.finditer(text):
            number, qid, qtype, marks = m.groups()
            key = (path.stem, qid)
            if key in papers:
                raise ValueError(f"duplicate source question key: {key}")
            papers[key] = {"source_paper": path.stem, "question_id": qid,
                           "source_number": int(number), "marks": float(marks),
                           "exam_type": exam.group(1), "source_type": qtype.strip()}
    return papers, declared_total


def load_topics(root):
    path = root / "curriculum/topics.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return {item["id"]: item["week"] for item in data}
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return None, f"cannot load curriculum/topics.json: {exc}"


def validate(root, manifest_path):
    errors, warnings = [], []
    try:
        universe, declared = extract_universe(root)
    except (OSError, ValueError) as exc:
        print(f"HARD FAILURE: cannot build question universe: {exc}")
        return 1
    if declared is not None and declared != len(universe):
        errors.append(f"extraction index declares {declared} questions, parsed {len(universe)}")
    try:
        records = json.loads(manifest_path.read_text(encoding="utf-8"))
        if not isinstance(records, list):
            raise ValueError("manifest root must be a JSON list")
    except (OSError, ValueError) as exc:
        print(f"HARD FAILURE: cannot load manifest: {exc}")
        return 1
    topic_data = load_topics(root)
    if isinstance(topic_data, tuple):
        topics, message = topic_data
        errors.append(message)
    else:
        topics = topic_data

    seen = Counter()
    q2_total = q2_early = 0
    counts = defaultdict(Counter)
    flagged = []
    for i, row in enumerate(records):
        if not isinstance(row, dict):
            errors.append(f"record[{i}] must be an object")
            continue
        bad = False
        for field, typ in REQUIRED.items():
            if field not in row or not isinstance(row[field], typ) or (typ is int and isinstance(row[field], bool)):
                errors.append(f"record[{i}] missing/invalid {field}")
                bad = True
        for f, value in (("related_weeks", row.get("related_weeks")),):
            if isinstance(value, list) and any(not isinstance(w, int) or isinstance(w, bool) for w in value):
                errors.append(f"record[{i}] {f} must contain integers")
                bad = True
        key = (row.get("source_paper"), row.get("question_id"))
        seen[key] += 1
        source = universe.get(key)
        if source is None:
            errors.append(f"record[{i}] extra/unknown question: {key}")
            continue
        if row.get("exam_type") != source["exam_type"]:
            errors.append(f"{key}: exam_type {row.get('exam_type')!r} != {source['exam_type']}")
        if row.get("source_number") != source["source_number"]:
            errors.append(f"{key}: source_number does not match paper")
        if isinstance(row.get("marks"), (int, float)) and row["marks"] != source["marks"]:
            errors.append(f"{key}: marks {row['marks']} != paper marks {source['marks']:g}")
        wk, et = row.get("primary_week"), source["exam_type"]
        bounds = {"Q1": (1, 4), "Q2": (1, 8), "ET": (1, 12)}[et]
        if isinstance(wk, int) and not isinstance(wk, bool):
            if not bounds[0] <= wk <= bounds[1]:
                errors.append(f"{key}: {et} primary_week {wk} outside {bounds[0]}..{bounds[1]}")
            counts[et][wk] += 1
            if et == "Q2":
                q2_total += 1
                q2_early += wk <= 4
        tid = row.get("topic_id")
        if topics is not None and isinstance(tid, str):
            if tid not in topics:
                errors.append(f"{key}: unknown topic_id {tid!r}")
            elif topics[tid] != wk:
                errors.append(f"{key}: topic {tid!r} is week {topics[tid]}, primary_week is {wk}")
        if row.get("flag_for_review") is True:
            flagged.append(row)
    for key in universe:
        if seen[key] == 0:
            errors.append(f"missing question: {key}")
        elif seen[key] > 1:
            errors.append(f"question appears {seen[key]} times: {key}")
    if q2_total and q2_early / q2_total > 0.40:
        warnings.append(f"Q2 weeks 1–4: {q2_early}/{q2_total} ({q2_early/q2_total:.1%}), exceeds 40% threshold")
    print(f"Question universe: {len(universe)} parsed" + (f" (index declares {declared})" if declared is not None else ""))
    print("Counts[exam_type][week]")
    print("exam_type | " + " | ".join(f"W{w}" for w in range(1, 13)))
    print("--- | " + " | ".join("---:" for _ in range(12)))
    for et in ("Q1", "Q2", "ET"):
        print(et + " | " + " | ".join(str(counts[et][w]) for w in range(1, 13)))
    print(f"\nFlagged for review ({len(flagged)}):")
    for row in flagged:
        print(f"- {row.get('source_paper')} #{row.get('source_number')} ({row.get('question_id')}): {row.get('rationale', '')}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"HARD FAILURE: {error}")
    print(f"\nValidation: {'FAILED' if errors else 'PASSED'} ({len(errors)} hard failures, {len(warnings)} warnings)")
    return 1 if errors else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1], help="repository root (for isolated validation/testing)")
    parser.add_argument("--manifest", type=Path, help="manifest path; defaults to classification/final/final-manifest.json under root")
    args = parser.parse_args()
    manifest = args.manifest or args.root / "classification/final/final-manifest.json"
    raise SystemExit(validate(args.root.resolve(), manifest.resolve()))

if __name__ == "__main__":
    main()
