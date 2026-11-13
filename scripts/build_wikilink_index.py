#!/usr/bin/env python3
"""Build a case-insensitive Obsidian wikilink target to site path index."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {".git", ".venv", "_site", "screenshots", "__pycache__"}

def main():
    index = {}
    for path in sorted(ROOT.rglob("*.md")):
        rel = path.relative_to(ROOT)
        if any(part in EXCLUDED for part in rel.parts):
            continue
        url = "/".join(part.replace(" ", "%20") for part in rel.parts)
        keys = {path.stem.lower(), path.name.lower(), str(rel.with_suffix("")).lower(), str(rel).lower()}
        for key in keys:
            index.setdefault(key, url)
    out = ROOT / "wikilinks.json"
    out.write_text(json.dumps(index, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Indexed {len(index)} wikilink keys from {len(list(ROOT.rglob('*.md')))} Markdown paths into {out.name}.")

if __name__ == "__main__":
    main()
