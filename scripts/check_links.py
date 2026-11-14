# /// script
# requires-python = ">=3.10"
# dependencies = ["beautifulsoup4>=4.12"]
# ///
"""Independent crawl of the BUILT site: every local href/src must exist and every #fragment must resolve."""
import posixpath, sys
from pathlib import Path
from urllib.parse import unquote, urlsplit
from bs4 import BeautifulSoup

site = Path(sys.argv[1] if len(sys.argv) > 1 else "_site").resolve()
ids: dict[Path, set[str]] = {}
bad, checked = [], 0
pages = sorted(site.rglob("*.html"))
for f in pages:
    s = BeautifulSoup(f.read_text(encoding="utf-8"), "html.parser")
    ids[f] = {t["id"] for t in s.find_all(attrs={"id": True})} | {t["name"] for t in s.find_all("a", attrs={"name": True})}
for f in pages:
    s = BeautifulSoup(f.read_text(encoding="utf-8"), "html.parser")
    for tag, attr in [(t, "href") for t in s.find_all("a", href=True)] + [(t, "src") for t in s.find_all(["img", "script"], src=True)]:
        u = urlsplit(tag[attr])
        if u.scheme or u.netloc:
            continue
        checked += 1
        dest = f if not u.path else (f.parent / unquote(u.path)).resolve()
        if not dest.exists():
            bad.append(f"{f.relative_to(site)}: {tag[attr]} -> missing file")
        elif u.fragment and dest.suffix == ".html" and unquote(u.fragment) not in ids.get(dest, set()):
            bad.append(f"{f.relative_to(site)}: {tag[attr]} -> missing anchor")
print(f"crawled {len(pages)} pages, {checked} local links/images; broken: {len(bad)}")
for b in bad[:40]:
    print("  ", b)
sys.exit(1 if bad else 0)
