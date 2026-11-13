#!/usr/bin/env python3
"""Check relative Markdown links, image paths, sidebar links, and Obsidian links."""
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", ".venv", "_site", "screenshots", "__pycache__", "AGENTS.md", "PLAN.md"}
LINK_RE = re.compile(r"!?\[[^\]]*\]\((?:<([^>]+)>|([^\s)]+))(?:\s+[^)]*)?\)")
WIKI_RE = re.compile(r"(?<!\[)\[\[([^\]|\[\]]+)(?:\\?\|[^\]]+)?\]\](?!\])")

def files():
    return [p for p in ROOT.rglob("*.md") if not any(x in SKIP for x in p.relative_to(ROOT).parts)
            and (p.parts[len(ROOT.parts)] in {"month 1", "month 2", "month 3", "notes", "question-bank", "sources"}
                 or p.parent == ROOT)]

def exists_target(source, raw):
    raw = unquote(raw.strip())
    if not raw or raw.startswith(("#", "//", "/")):
        return True
    parts = urlsplit(raw)
    if parts.scheme or parts.netloc:
        return True
    target = (source.parent / parts.path).resolve() if not parts.path.startswith("/") else (ROOT / parts.path.lstrip("/")).resolve()
    if target.is_file():
        return True
    if target.is_dir():
        return any((target / name).is_file() for name in ("README.md", "_sidebar.md", "index.md"))
    return False

def main():
    md_files = files()
    by_name = {}
    for p in md_files:
        rel = p.relative_to(ROOT)
        by_name.setdefault(p.stem.lower(), p)
        by_name.setdefault(p.name.lower(), p)
        by_name.setdefault(str(rel.with_suffix("")).lower(), p)
    errors = []
    link_count = wiki_count = 0
    for source in md_files:
        text = source.read_text(encoding="utf-8", errors="replace")
        text = re.sub(r"```.*?```|`[^`]*`", "", text, flags=re.S)
        for match in LINK_RE.finditer(text):
            target = match.group(1) or match.group(2)
            link_count += 1
            if not exists_target(source, target):
                errors.append(f"{source.relative_to(ROOT)}: dangling link {target}")
        for target in WIKI_RE.findall(text):
            wiki_count += 1
            key = target.strip().replace("\\|", "|").rstrip("\\").replace("\\", "/").removesuffix(".md").lower()
            if key not in by_name and key.split("/")[-1] not in by_name:
                errors.append(f"{source.relative_to(ROOT)}: dangling wikilink [[{target}]]")
    sidebar = ROOT / "_sidebar.md"
    if sidebar.exists():
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", sidebar.read_text(encoding="utf-8")):
            link_count += 1
            if not exists_target(sidebar, target):
                errors.append(f"_sidebar.md: dangling entry {target}")
    print(f"Checked {len(md_files)} Markdown files, {link_count} relative links/sidebar entries, and {wiki_count} wikilinks.")
    if errors:
        print(f"Found {len(errors)} dangling reference(s):")
        print("\n".join(f"- {e}" for e in errors))
        return 1
    print("All checked links resolve.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
