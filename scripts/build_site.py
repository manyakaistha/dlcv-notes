# /// script
# requires-python = ">=3.10"
# dependencies = ["markdown>=3.6", "pymdown-extensions>=10.8", "beautifulsoup4>=4.12", "pyyaml>=6"]
# ///
"""Build the Speech Technology study site (notes + past-year questions) into static HTML.

Usage:  uv run scripts/build_site.py --output _site

Reads Markdown from content/, resolves Obsidian wikilinks, renders math for MathJax,
copies every non-Markdown file (figures, scanned papers, PDFs) and then verifies that
every local link, image and #anchor resolves. The build fails if any link is broken.
"""
from __future__ import annotations

import argparse
import html
import json
import os
import posixpath
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

import markdown
import yaml
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
ASSETS = ROOT / "site-assets"
SITE_NAME = "Speech Technology"
COURSE = "BSEE4001 · IIT Madras BS Degree"
REPO_URL = "https://github.com/manyakaistha/SpeechTechnology-Notes"

WEEK_HERO = {
    1: ("Waves become<br>numbers.", "Sample. Filter. Spectrum."),
    2: ("How we hear,<br>how we measure.", "Mel. Cepstrum. MFCC."),
    3: ("Gaussians, clusters<br>and Markov paths.", "Gaussian. GMM. EM."),
    4: ("Hidden states,<br>best paths.", "HMM. Forward. Viterbi."),
    5: ("From phones<br>to sentences.", "Lexicon. Acoustic. N-gram."),
}
THEMES = [
    ("paper", "Paper", "#f3eee4", "#e7462b"),
    ("midnight", "Midnight", "#101b38", "#ff7568"),
    ("scope", "Scope", "#06130e", "#5dffa1"),
    ("spectro", "Spectro", "#150b2b", "#ff4f9a"),
    ("butter", "Butter", "#ffe9a8", "#d72d43"),
    ("mono", "Mono", "#141414", "#f2f2f2"),
]

warnings: list[str] = []
errors: list[str] = []


# ----------------------------------------------------------------------------- pages
class Page:
    def __init__(self, rel: str, text: str, virtual: bool = False):
        self.rel = rel  # posix path relative to content/, ending in .md
        self.virtual = virtual
        self.fm, self.body = split_frontmatter(text)
        self.stem = posixpath.basename(rel)[:-3]
        self.out = rel[:-3] + ".html"
        self.title = self._title()
        self.ids: set[str] = set()
        self.html = ""
        self.toc: list[dict] = []

    def _title(self) -> str:
        t = self.fm.get("title")
        if isinstance(t, str) and t.strip():
            return t.strip()
        m = re.search(r"^#\s+(.+)$", self.body, re.M)
        return m.group(1).strip() if m else self.stem


def split_frontmatter(text: str) -> tuple[dict, str]:
    m = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        return {}, text
    try:
        fm = yaml.safe_load(m.group(1)) or {}
        if not isinstance(fm, dict):
            fm = {}
    except yaml.YAMLError:
        fm = {}
        t = re.search(r"^title:\s*(.+)$", m.group(1), re.M)
        if t:
            fm["title"] = t.group(1).strip().strip('"')
    return fm, text[m.end():]


def load_pages() -> dict[str, Page]:
    pages: dict[str, Page] = {}
    for p in sorted(CONTENT.rglob("*.md")):
        rel = p.relative_to(CONTENT).as_posix()
        pages[rel] = Page(rel, p.read_text(encoding="utf-8"))
    return pages


# ----------------------------------------------------------------------------- markdown prep
CODE_SPLIT = re.compile(r"(^```.*?^```[ \t]*$|^~~~.*?^~~~[ \t]*$|`[^`\n]+`)", re.S | re.M)
WIKILINK = re.compile(r"\[\[([^\]\|\\#]+?)(#[^\]\|\\]*)?(?:\\?\|([^\]]*))?\]\]")
LIST_ITEM = re.compile(r"^(\s{0,3})([-*+]|\d{1,3}[.)])\s+\S")


def outside_code(text: str, fn) -> str:
    parts = CODE_SPLIT.split(text)
    return "".join(p if i % 2 else fn(p) for i, p in enumerate(parts))


def fix_lists(text: str) -> str:
    """Python-Markdown needs a blank line before a list; Obsidian/Docsify do not."""
    out: list[str] = []
    in_fence = False
    for line in text.split("\n"):
        if re.match(r"^\s*(```|~~~)", line):
            in_fence = not in_fence
            out.append(line)
            continue
        if not in_fence and LIST_ITEM.match(line) and out:
            prev = out[-1]
            if (
                prev.strip()
                and not LIST_ITEM.match(prev)
                and not re.match(r"^\s+\S", prev)
                and not prev.lstrip().startswith((">", "|", "#", "$$", "<"))
            ):
                out.append("")
        out.append(line)
    return "\n".join(out)


def make_wikilinks(pages: dict[str, Page], by_stem: dict[str, Page], src: Page):
    def sub(m: re.Match) -> str:
        target, anchor, alias = m.group(1).strip(), m.group(2) or "", m.group(3)
        stem = posixpath.basename(target.rstrip("/"))
        stem = stem[:-3] if stem.endswith(".md") else stem
        dest = by_stem.get(stem.lower())
        if dest is None:
            warnings.append(f"{src.rel}: unresolved wikilink [[{m.group(1)}]]")
            return alias or stem
        label = (alias or dest.title).replace("[", "(").replace("]", ")")
        href = posixpath.relpath(dest.rel, posixpath.dirname(src.rel) or ".")
        return f"[{label}]({quote(href)}{anchor})"

    return sub


INLINE_MATH = re.compile(r"(?<![\\$])\$(?!\$)([^$\n]+?)(?<!\\)\$(?!\$)")


def protect_table_math(text: str) -> str:
    """A bare | inside $...$ on a table row would split the cell; use \\vert instead."""
    out = []
    for line in text.split("\n"):
        if line.lstrip().startswith("|") and "$" in line:
            line = INLINE_MATH.sub(lambda m: "$" + re.sub(r"(?<!\\)\|", r"\\vert ", m.group(1)) + "$", line)
        out.append(line)
    return "\n".join(out)


def prepare(text: str, pages, by_stem, src: Page) -> str:
    text = re.sub(r"%%.*?%%", "", text, flags=re.S)
    text = outside_code(text, lambda t: WIKILINK.sub(make_wikilinks(pages, by_stem, src), t))
    return fix_lists(protect_table_math(text))


def render_markdown(text: str) -> tuple[str, list[dict]]:
    md = markdown.Markdown(
        extensions=["tables", "fenced_code", "toc", "attr_list", "md_in_html", "sane_lists", "nl2br", "pymdownx.arithmatex"],
        extension_configs={
            "pymdownx.arithmatex": {"generic": True},
            "toc": {"toc_depth": "2-3", "permalink": False},
        },
    )
    out = md.convert(text)
    return out, getattr(md, "toc_tokens", [])


# ----------------------------------------------------------------------------- links
class Resolver:
    def __init__(self, pages: dict[str, Page]):
        self.pages = pages
        self.files: set[str] = {p.relative_to(CONTENT).as_posix() for p in CONTENT.rglob("*") if p.is_file()}
        self.by_base: dict[str, list[str]] = {}
        for f in self.files:
            self.by_base.setdefault(posixpath.basename(f), []).append(f)

    def target(self, href_path: str, src_rel: str) -> str | None:
        cand = posixpath.normpath(posixpath.join(posixpath.dirname(src_rel), unquote(href_path)))
        if cand in self.files or cand in self.pages:
            return cand
        base = posixpath.basename(unquote(href_path))
        hits = self.by_base.get(base, [])
        if len(hits) == 1:
            return hits[0]
        return None


def rewrite_links(soup: BeautifulSoup, page: Page, resolver: Resolver, internal: list[tuple[str, str, str]]):
    here = posixpath.dirname(page.out) or "."

    def fix(tag, attr):
        href = tag.get(attr)
        if not href:
            return
        parts = urlsplit(href)
        if parts.scheme or parts.netloc:
            if parts.scheme in ("http", "https"):
                tag["rel"] = "noopener"
                tag["target"] = "_blank"
            return
        if not parts.path:  # same-page anchor
            internal.append((page.out, page.out, parts.fragment))
            return
        tgt = resolver.target(parts.path, page.rel)
        if tgt is None:
            if tag.name == "a":
                # Course slide decks are intentionally not republished; keep the citation text.
                warnings.append(f"{page.rel}: dropped link to unpublished file {href}")
                tag.replace_with(*tag.contents) if tag.contents else tag.decompose()
            else:
                errors.append(f"{page.rel}: missing resource {href}")
            return
        new = tgt[:-3] + ".html" if tgt.endswith(".md") else tgt
        rel = posixpath.relpath(new, here)
        frag = ("#" + parts.fragment) if parts.fragment else ""
        tag[attr] = quote(rel) + frag
        if tgt.endswith(".md") and parts.fragment:
            internal.append((page.out, new, parts.fragment))

    for a in soup.find_all("a", href=True):
        fix(a, "href")
    for img in soup.find_all("img", src=True):
        fix(img, "src")
        img["loading"] = "lazy"


def convert_callouts(soup: BeautifulSoup):
    for bq in soup.find_all("blockquote"):
        first = bq.find("p")
        if not first:
            continue
        m = re.match(r"\s*\[!(\w+)\][+-]?\s*(.*)", first.get_text("\n"), re.S)
        if not m:
            continue
        kind = m.group(1).lower()
        bq.name = "div"
        bq["class"] = ["callout", f"callout-{kind}"]
        label = soup.new_tag("span", attrs={"class": "callout-title"})
        label.string = kind.title()
        first_html = first.decode_contents()
        first_html = re.sub(r"^\s*\[![^\]]+\][+-]?\s*(<br\s*/?>)?\s*", "", first_html)
        first.clear()
        first.append(BeautifulSoup(first_html, "html.parser"))
        bq.insert(0, label)


# ----------------------------------------------------------------------------- navigation
def short_week_title(title: str) -> str:
    return re.sub(r"^Week\s+\d+\s*[:—-]\s*", "", title)


def nav_title(p: Page) -> str:
    m = re.match(r"eli12/week-(\d)-eli12\.md", p.rel)
    if m:
        return f"Week {m.group(1)} ELI12"
    if p.rel == "eli12/eli12-start.md":
        return "ELI12 start"
    m = re.match(r"week-(\d)/week-\d-(notes|exam-focused-notes|exam-questions)\.md", p.rel)
    if m:
        kind = {"notes": "Notes", "exam-focused-notes": "Exam guide", "exam-questions": "Past papers"}[m.group(2)]
        return f"Week {m.group(1)} {kind}"
    return p.title


def week_of(page: Page) -> int | None:
    m = re.match(r"week-(\d)/", page.rel) or re.match(r"eli12/week-(\d)-eli12", page.rel)
    return int(m.group(1)) if m else None


def nav_model(pages: dict[str, Page]):
    def has(rel):
        return rel in pages

    groups = []
    start = [("START HERE", "Home", "index.html"),
             ("STUDY ROUTE", "Exam study route", "exam-study-guide.html"),
             ("QUESTIONS BY TOPIC", "Past-paper topics", "past-paper-topics.html"),
             ("ALL PAPERS", "Paper &amp; question index", "exam-question-index.html"),
             ("MAP", "Knowledge map", "Knowledge-Map.html"),
             ("SCOPE", "Curriculum &amp; sources", "source-catalog.html")]
    groups.append(("Start", None, start))
    eli = [("ELI12", "Start here: plain language", "eli12/eli12-start.html")]
    for n in range(1, 6):
        rel = f"eli12/week-{n}-eli12.md"
        if has(rel):
            eli.append((f"WEEK {n}", html.escape(pages[rel].title.split(": ", 1)[-1][:1].upper() + pages[rel].title.split(": ", 1)[-1][1:]), rel[:-3] + ".html"))
    if len(eli) > 1:
        groups.append(("ELI12 · plain language", None, eli))
    for n in range(1, 6):
        items = []
        for label, rel in (("NOTES", f"week-{n}/week-{n}-notes.md"),
                           ("EXAM GUIDE", f"week-{n}/week-{n}-exam-focused-notes.md"),
                           ("PAST PAPERS", f"week-{n}/week-{n}-exam-questions.md")):
            if has(rel):
                items.append((label, short_week_title(pages[rel].title) if label == "NOTES" else
                              ("Learn &amp; prepare" if label == "EXAM GUIDE" else "Questions &amp; worked answers"),
                              rel[:-3] + ".html"))
        if items:
            groups.append((f"Week {n}", n, items))
    concepts = sorted((p for p in pages.values() if p.rel.startswith("notes/concepts/")), key=lambda p: p.title.lower())
    groups.append(("Concepts", None, [("CONCEPT", html.escape(p.title), p.out) for p in concepts]))
    extr = sorted((p for p in pages.values() if p.rel.startswith("sources/exam-papers/extractions/")), key=lambda p: p.rel)
    arch = [("AUDIT", "Question routing audit", "sources/exam-papers/question-routing.html")]
    arch += [("PAPER", html.escape(p.stem.replace("ee4001_", "")), p.out) for p in extr]
    groups.append(("Paper archive", None, arch))
    return groups


def render_nav(groups, current_out: str) -> str:
    here = posixpath.dirname(current_out) or "."

    def href(target):
        return quote(posixpath.relpath(target, here))

    out = []
    for title, _n, items in groups:
        is_open = any(t == current_out for _l, _x, t in items) or title == "Start"
        cur = ' aria-current="page"'
        links = "".join(
            f'<a href="{href(t)}"{cur if t == current_out else ""}>'
            f'<span class="num">{l}</span>{x}</a>' for l, x, t in items)
        out.append(f'<details class="nav-group"{" open" if is_open else ""}><summary>{title}</summary>'
                   f'<nav class="nav" aria-label="{title}">{links}</nav></details>')
    return "".join(out)


def reading_sequence(pages: dict[str, Page]) -> list[str]:
    seq = ["index.html", "exam-study-guide.html", "past-paper-topics.html", "exam-question-index.html",
           "Knowledge-Map.html", "source-catalog.html"]
    seq += ["eli12/eli12-start.html"] + [f"eli12/week-{n}-eli12.html" for n in range(1, 6) if f"eli12/week-{n}-eli12.md" in pages]
    for n in range(1, 6):
        for kind in ("notes", "exam-focused-notes", "exam-questions"):
            rel = f"week-{n}/week-{n}-{kind}.md"
            if rel in pages:
                seq.append(rel[:-3] + ".html")
    seq += [p.out for p in sorted((p for p in pages.values() if p.rel.startswith("notes/concepts/")), key=lambda p: p.title.lower())]
    return seq


# ----------------------------------------------------------------------------- page shell
CREDIT_WAVE = ('<svg class="credit-wave" viewBox="0 0 44 20" aria-hidden="true" focusable="false">'
               '<path d="M1 10h5l3-7 4 14 4-12 3 9 3-4h4l3-5 3 10 3-5h4"/></svg>')


def theme_buttons() -> str:
    return "".join(
        f'<button class="theme-option" data-palette="{k}" aria-pressed="{str(k == "paper").lower()}" '
        f'style="--swatch:{sw};--dot:{dot}"><span aria-hidden="true"></span>{name}</button>'
        for k, name, sw, dot in THEMES)


def shell(*, page_out: str, title: str, description: str, article: str, nav_html: str, kicker: str,
          hero_title: str, hero_caption: str, topline: str, toc: list[dict], overview: bool,
          pagination: str, section_label: str = "") -> str:
    root = "../" * (page_out.count("/")) if "/" in page_out else ""
    assets = root + "assets/"
    toc_html = ""
    if toc:
        def walk(items):
            s = "<ul>"
            for t in items:
                s += f'<li><a href="#{t["id"]}">{t["name"]}</a>'
                if t.get("children"):
                    s += walk(t["children"])
                s += "</li>"
            return s + "</ul>"
        flat = []
        for t in toc:  # skip the page's H1 wrapper, keep H2/H3
            flat.extend(t["children"] if t["level"] == 1 and t.get("children") else [t])
        if flat:
            toc_html = f'<details class="toc"><summary>On this page</summary><div class="toc">{walk(flat)}</div></details>'
    theme_ids = json.dumps([t[0] for t in THEMES])
    return f"""<!doctype html>
<html lang="en" data-theme="paper"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} · {SITE_NAME}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='6' fill='%23f3eee4'/%3E%3Cpath d='M4 16h4l3-8 4 16 4-12 3 8 2-4h4' fill='none' stroke='%23e7462b' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,700;1,700&display=swap" rel="stylesheet">
<script>try {{ const t=localStorage.getItem('speech-lab-theme'); if({theme_ids}.includes(t)) document.documentElement.dataset.theme=t; }} catch {{}}</script>
<link rel="stylesheet" href="{assets}site.css"><link rel="stylesheet" href="{assets}theme.css"><link rel="stylesheet" href="{assets}navigation.css"><link rel="stylesheet" href="{assets}speech.css">
<script>window.MathJax={{tex:{{inlineMath:[['\\\\(','\\\\)']],displayMath:[['\\\\[','\\\\]']]}},options:{{ignoreHtmlClass:'tex2jax_ignore',processHtmlClass:'arithmatex'}}}};</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-mml-chtml.js"></script>
<script defer src="{assets}site.js"></script><script defer src="{assets}theme.js"></script></head>
<body data-overview="{str(overview).lower()}" data-root="{root}">
<div class="reading-progress" aria-hidden="true"></div>
<a class="skip" href="#main">Skip to content</a><div class="layout">
<aside class="sidebar"><span class="eyebrow">{COURSE}</span><a class="brand" href="{root}index.html">Speech Technology<br>Notes &amp; Past Papers</a>
<p>Weekly notes, exam-focused guides and every past-year question with a worked answer.</p>
<details class="palette-panel"><summary>Choose your palette</summary><div class="theme-options">{theme_buttons()}</div><button class="motion-toggle" aria-pressed="true">Pause header motion</button></details>
<div class="desktop-nav"><input class="search" aria-label="Search notes and questions" placeholder="Search notes &amp; questions…" type="search"><div class="results" aria-live="polite"></div>{nav_html}</div>
<details class="mobile-menu"><summary>Browse &amp; search</summary><input class="search" aria-label="Search notes and questions" placeholder="Search notes &amp; questions…" type="search"><div class="results" aria-live="polite"></div>{nav_html}</details>
<footer><span>Speech Technology · {COURSE}</span><br><a href="{REPO_URL}">Source on GitHub ↗</a></footer></aside>
<main id="main"><div class="content"><div class="topline">{topline}</div>
<div class="speech-hero"><canvas aria-hidden="true"></canvas><div class="hero-copy"><span class="hero-kicker">{kicker}</span><p class="hero-title">{hero_title}</p><p class="hero-caption">{hero_caption}</p></div></div>
{('<span class="section-label">' + section_label + '</span>') if section_label else ''}{toc_html}
<article>{article}</article>{pagination}
<footer class="endnote"><span class="author-credit">{CREDIT_WAVE}<span>Created by manaykaistha.</span>{CREDIT_WAVE}</span><br>Worked answers are independently derived study aids, not official answer keys. Past-paper scans are reproduced for revision.</footer></div></main></div></body></html>
"""


def pagination_html(seq: list[str], titles: dict[str, str], current: str) -> str:
    if current not in seq:
        return ""
    i = seq.index(current)
    here = posixpath.dirname(current) or "."
    link = lambda t, arrow: (f'<a href="{quote(posixpath.relpath(t, here))}">' +
                             (f"← {html.escape(titles[t])}" if arrow == "prev" else f"{html.escape(titles[t])} →") + "</a>")
    prev_ = link(seq[i - 1], "prev") if i > 0 else "<span></span>"
    next_ = link(seq[i + 1], "next") if i + 1 < len(seq) else "<span></span>"
    return f'<nav class="pagination" aria-label="Previous and next page">{prev_}{next_}</nav>'


# ----------------------------------------------------------------------------- generated pages
def topic_rows(body: str) -> list[list[str]]:
    """Rows of [topic, evidence-markdown] from a week's 'Topic checklist and evidence' table."""
    m = re.search(r"## Topic checklist and evidence\s*\n(.*?)(?=\n## )", body, re.S)
    rows: list[list[str]] = []
    if not m:
        return rows
    cur = None
    for ln in m.group(1).splitlines():
        if not ln.startswith("|") or re.match(r"^\|\s*:?-", ln):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < 2 or cells[0] == "Topic":
            continue
        if cells[0]:
            cur = [cells[0], cells[1]]
            rows.append(cur)
        elif cur:
            cur[1] += ", " + cells[1]
    return rows


def anchor_topics(pages: dict[str, Page]) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for rel, pg in pages.items():
        if re.fullmatch(r"week-\d/week-\d-exam-questions\.md", rel):
            for topic, ev in topic_rows(pg.body):
                for a in re.findall(r"\(#(ee4001_[^)]+)\)", ev):
                    out.setdefault(a, [])
                    if topic not in out[a]:
                        out[a].append(topic)
    return out


def norm_stem(text: str) -> str:
    t = text.lower()
    t = re.sub(r"\(\s*\d+(\.\d+)?\s*points?\s*\)", " ", t)
    t = re.sub(r"\b(for|in)\b", " ", t)
    t = re.sub(r"[^a-z0-9.+*/=<>^$ -]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def group_duplicates(items: list[dict]) -> None:
    """Assign item['group'] by near-identical stem text (same numbers, high similarity)."""
    import difflib
    groups: list[list[dict]] = []
    for it in items:
        key = it["stem"]
        nums = tuple(sorted(re.findall(r"\d+(?:\.\d+)?", key)))
        for g in groups:
            ref = g[0]
            if not key or not ref["stem"]:
                continue
            if nums == ref["nums"] and difflib.SequenceMatcher(None, key, ref["stem"]).ratio() >= 0.9:
                g.append(it)
                it["nums"] = nums
                break
        else:
            it["nums"] = nums
            groups.append([it])
    for i, g in enumerate(groups):
        for it in g:
            it["group"] = i


def annotate_questions(soup: BeautifulSoup, page: Page, a2t: dict[str, list[str]], report: list[dict]) -> None:
    """Wrap each question (anchor + h3 + body up to its worked answer) so the page can filter it."""
    art_children = list(soup.children)
    heading_re = re.compile(r"^(\d{4}) Term (\d) · (Quiz 1|Quiz 2|End Term) · (\w+) — Question (.+)$")
    starts = []
    for i, el in enumerate(art_children):
        if getattr(el, "name", None) == "h3" and heading_re.match(el.get_text(" ", strip=True)):
            j = i
            prev = art_children[i - 1] if i else None
            k = i - 1
            while k >= 0 and isinstance(art_children[k], str) and not art_children[k].strip():
                k -= 1
            prev = art_children[k] if k >= 0 else None
            if prev is not None and getattr(prev, "name", None) == "p" and prev.find("a", id=True) and not prev.get_text(strip=True):
                j = k
            starts.append((j, i))
    items = []
    for n, (j, i) in enumerate(starts):
        end = starts[n + 1][0] if n + 1 < len(starts) else len(art_children)
        nodes = [x for x in art_children[j:end]]
        # trim trailing non-question material (hr, next h2 sections)
        cut = len(nodes)
        for idx, x in enumerate(nodes):
            if getattr(x, "name", None) in ("hr", "h2") and idx > 1:
                cut = idx
                break
        nodes = nodes[:cut]
        h3 = art_children[i]
        m = heading_re.match(h3.get_text(" ", strip=True))
        year, term, kind, session, qrest = m.groups()
        anchor = (art_children[j].find("a", id=True) or {}).get("id", "") if j != i else ""
        stem_parts = []
        for x in nodes:
            name = getattr(x, "name", None)
            if x is h3 or name is None:
                continue
            if name == "h4" and "Worked answer" in x.get_text():
                break
            txt = x.get_text(" ", strip=True)
            if txt.startswith(("Source:", "Topics:", "Figure ")) or x.find("img"):
                continue
            stem_parts.append(txt)
        items.append({"anchor": anchor, "year": int(year), "term": f"{year} T{term}", "kind": kind,
                      "session": session, "q": qrest, "stem": norm_stem(" ".join(stem_parts)),
                      "topics": a2t.get(anchor, ["Other"]), "nodes": nodes})
    if not items:
        return
    group_duplicates(items)
    # Manual corrections from a reviewed pass (scripts/dup_overrides.json): merge notation-only variants.
    ov = ROOT / "scripts" / "dup_overrides.json"
    if ov.exists():
        by_anchor = {it["anchor"]: it for it in items}
        for m in json.loads(ov.read_text(encoding="utf-8")).get("merge", []):
            members = [by_anchor[a] for a in m["anchors"] if a in by_anchor]
            if len(members) > 1:
                target = members[0]["group"]
                for it in members[1:]:
                    old = it["group"]
                    for other in items:
                        if other["group"] == old:
                            other["group"] = target
        for sp in json.loads(ov.read_text(encoding="utf-8")).get("split", []):
            if sp["anchor"] in by_anchor:
                by_anchor[sp["anchor"]]["group"] = 10_000 + len(items)
    for it in items:
        wrap = soup.new_tag("div", attrs={"class": "qitem", "data-year": str(it["year"]),
                                          "data-topics": "|".join(it["topics"]), "data-group": str(it["group"]),
                                          "data-label": f'{it["term"]} {it["kind"]} {it["session"]} Q{it["q"].split(" ")[0]}',
                                          "data-qid": it["anchor"]})
        it["nodes"][0].insert_before(wrap)
        for x in it["nodes"]:
            wrap.append(x.extract())
        report.append({"page": page.rel, "anchor": it["anchor"], "label": wrap["data-label"], "group": it["group"],
                       "topics": it["topics"], "stem": it["stem"][:200]})
    # drop decorative rules between items
    for hr in soup.find_all("hr"):
        if hr.find_previous_sibling("div", class_="qitem") is not None and (hr.find_next_sibling() is None or hr.find_next_sibling().name in ("div", "h2")):
            hr.decompose()
    # filter bar before the first h2
    topics = sorted({t for it in items for t in it["topics"]})
    years = sorted({it["year"] for it in items})
    opts_t = "".join(f'<option value="{html.escape(t)}">{html.escape(t)}</option>' for t in topics)
    opts_y = "".join(f'<option value="{y}">{y}</option>' for y in years)
    bar = BeautifulSoup(f"""<div class="qfilter" role="search" aria-label="Filter questions"><div class="qf-row">
<label>Topic <select id="qf-topic"><option value="">All topics</option>{opts_t}</select></label>
<label>Year <select id="qf-year"><option value="">All years</option>{opts_y}</select></label>
<label class="qf-check"><input type="checkbox" id="qf-dedup"> Remove duplicates</label>
<button type="button" id="qf-reset">Reset</button></div>
<p class="qf-count" id="qf-count" role="status" aria-live="polite"></p></div>""", "html.parser")
    first_item = soup.find("div", class_="qitem")
    lead = first_item.find_previous_sibling("h2") if first_item else None
    (lead.insert_before(bar) if lead else first_item.insert_before(bar))
    soup.append(BeautifulSoup('<script defer src="__ASSETS__qfilter.js"></script>', "html.parser"))


def build_topics_page(pages: dict[str, Page]) -> Page:
    lines = ["---", 'title: "Past-paper topics: find every question by topic"', "---", "",
             "# Past-paper topics", "",
             "Pick a topic to jump straight to every past-year question that tests it. Each link opens the question, its scanned "
             "stem and a worked answer. The number in brackets counts the matching paper occurrences; repeated questions are kept "
             "once per paper because the same template often returns in later terms.", ""]
    for n in range(1, 5):
        rel = f"week-{n}/week-{n}-exam-questions.md"
        if rel not in pages:
            continue
        rows = topic_rows(pages[rel].body)
        if not rows:
            continue
        notes = f"week-{n}/week-{n}-notes.md"
        lines += [f"## Week {n} — {short_week_title(pages[notes].title)}", "",
                  f"[Study notes](week-{n}/week-{n}-notes.md) · [Exam-focused guide](week-{n}/week-{n}-exam-focused-notes.md) · "
                  f"[All Week {n} questions](week-{n}/week-{n}-exam-questions.md)", "",
                  "| Topic | Where it was asked |", "| :-- | :-- |"]
        for topic, ev in rows:
            ev = ev.replace("](#", f"](week-{n}/week-{n}-exam-questions.md#")
            count = ev.count("](week-")
            label = f"{topic} ({count})" if count else topic
            lines.append(f"| **{label}** | {ev} |")
        lines.append("")
    pg = Page("past-paper-topics.md", "\n".join(lines), virtual=True)
    return pg


def stats(pages: dict[str, Page]) -> dict:
    occ = 0
    for n in range(1, 5):
        rel = f"week-{n}/week-{n}-exam-questions.md"
        if rel in pages:
            m = re.search(r"Coverage:\*\*\s*(\d+)\s+source question", pages[rel].body)
            occ += int(m.group(1)) if m else 0
    return {
        "occ": occ,
        "papers": len([p for p in pages if p.startswith("sources/exam-papers/extractions/")]),
        "concepts": len([p for p in pages if p.startswith("notes/concepts/")]),
        "figures": len(list(CONTENT.glob("week-*/assets/*.png"))),
    }


def home_article(pages: dict[str, Page]) -> str:
    s = stats(pages)
    cards = []
    for n in range(1, 6):
        notes = f"week-{n}/week-{n}-notes.md"
        if notes not in pages:
            continue
        li = []
        if f"eli12/week-{n}-eli12.md" in pages:
            li.append(f'<li><a href="eli12/week-{n}-eli12.html">Plain language (ELI12)</a></li>')
        li.append(f'<li><a href="week-{n}/week-{n}-notes.html">Study notes</a></li>')
        stat = "Notes only (no past-paper bank yet)"
        g = f"week-{n}/week-{n}-exam-focused-notes.md"
        q = f"week-{n}/week-{n}-exam-questions.md"
        if g in pages:
            li.append(f'<li><a href="week-{n}/week-{n}-exam-focused-notes.html">Exam-focused guide</a></li>')
        if q in pages:
            m = re.search(r"Coverage:\*\*\s*(\d+)\s+source question", pages[q].body)
            stat = f"{m.group(1)} past-paper questions" if m else "Past-paper questions"
            li.append(f'<li><a href="week-{n}/week-{n}-exam-questions.html">Past papers &amp; worked answers</a></li>')
        cards.append(f'<div class="week-card"><span class="resource-meta">Week {n}</span>'
                     f'<h3>{html.escape(short_week_title(pages[notes].title))}</h3>'
                     f'<span class="stat">{stat}</span><ul>{"".join(li)}</ul></div>')
    return f"""
<h1>Speech Technology: Notes &amp; Past Papers</h1>
<p>Everything for BSEE4001 Speech Technology in one place: five weeks of rigorous notes with runnable code and figures, beginner-friendly exam guides, and the past-year questions with scanned stems and worked answers. Use <strong>Ask AI</strong> on any page, section or selected passage to get an ELI15 explanation.</p>
<div class="hero-stats"><div><b>5</b><span>weeks of notes</span></div><div><b>{s['occ']}</b><span>past-paper questions</span></div><div><b>{s['papers']}</b><span>exam papers archived</span></div><div><b>{s['concepts']}</b><span>concept notes</span></div><div><b>{s['figures']}</b><span>figures</span></div></div>
<h2>Start with a question you want to answer</h2>
<div class="resource-list">
<a class="resource-card" href="past-paper-topics.html"><span class="resource-meta">Questions by topic</span><h2>Find every question on a topic</h2><p>Sampling and aliasing, linearity and time-invariance, MFCC steps, GMM calculations, Viterbi tables and more. Each topic links to every paper that tested it, with the worked answer.</p><span class="resource-action">Browse past-paper topics →</span></a>
<a class="resource-card" href="exam-study-guide.html"><span class="resource-meta">Study route</span><h2>What to learn first, and why</h2><p>Priorities P1 to P3 for Weeks 1 to 4, derived from how often and how directly each mechanism was tested.</p><span class="resource-action">Open the exam study route →</span></a>
</div>
<h2>New here? Start in plain language</h2>
<div class="resource-list">
<a class="resource-card" href="eli12/eli12-start.html"><span class="resource-meta">ELI12 · all five weeks</span><h2>Speech Technology, explained like you're 12</h2><p>Flipbooks for sampling, trumpets for the voice, weather for HMMs. The same ideas as the weekly notes, with tiny numbers you can check by hand, and links to the exact exam questions each note prepares you for.</p><span class="resource-action">Open the ELI12 notes →</span></a>
</div>
<h2>Weekly notes, exam guides and past papers</h2>
<div class="resource-grid">{''.join(cards)}</div>
<h2>Reference</h2>
<ul>
<li><a href="exam-question-index.html">Paper and question index</a>: inventory of all {s['papers']} exam papers and how every question was routed.</li>
<li><a href="Knowledge-Map.html">Knowledge map</a>: how the concepts connect.</li>
<li><a href="source-catalog.html">Curriculum scope and sources</a>.</li>
</ul>
<div class="callout callout-note"><span class="callout-title">Note</span><p>Worked answers are independently derived by working through each question, not official answer keys. Where a source was ambiguous or its OCR looked wrong, the page says so beside the question.</p></div>
"""


# ----------------------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="_site")
    args = ap.parse_args()
    out = Path(args.output).resolve()
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    pages = load_pages()
    pages["past-paper-topics.md"] = build_topics_page(pages)
    by_stem = {p.stem.lower(): p for p in pages.values()}
    resolver = Resolver(pages)
    groups = nav_model(pages)
    seq = reading_sequence(pages)
    titles = {p.out: nav_title(p) for p in pages.values()}
    titles["index.html"] = "Home"
    internal: list[tuple[str, str, str]] = []
    search: list[dict] = []
    all_ids: dict[str, set[str]] = {}

    a2t = anchor_topics(pages)
    dup_report: list[dict] = []
    for p in pages.values():
        text = prepare(p.body, pages, by_stem, p)
        body, toc = render_markdown(text)
        soup = BeautifulSoup(body, "html.parser")
        rewrite_links(soup, p, resolver, internal)
        convert_callouts(soup)
        if re.fullmatch(r"week-\d/week-\d-exam-questions\.md", p.rel):
            annotate_questions(soup, p, a2t, dup_report)
        # Metadata chips from front matter.
        chips = []
        for t in (p.fm.get("tags") or []):
            chips.append(str(t).replace("speech/", ""))
        if p.fm.get("date"):
            chips.append(str(p.fm["date"]))
        if chips:
            chip = BeautifulSoup('<div class="meta-chips">' + "".join(f"<span>{html.escape(c)}</span>" for c in chips) + "</div>", "html.parser")
            h1 = soup.find("h1")
            (h1.insert_after(chip) if h1 else soup.insert(0, chip))
        wk = re.match(r"week-(\d)/", p.rel)
        if wk and f"eli12/week-{wk.group(1)}-eli12.md" in pages:
            rel_eli = quote(posixpath.relpath(f"eli12/week-{wk.group(1)}-eli12.html", posixpath.dirname(p.out) or "."))
            tip = BeautifulSoup(f'<div class="callout callout-tip"><span class="callout-title">New to this?</span>'
                                f'<p>Read the <a href="{rel_eli}">Week {wk.group(1)} plain-language (ELI12) note</a> first, then come back here.</p></div>', "html.parser")
            anchor = soup.find("div", class_="meta-chips") or soup.find("h1")
            (anchor.insert_after(tip) if anchor else soup.insert(0, tip))
        p.html = str(soup).replace("__ASSETS__", ("../" * p.out.count("/")) + "assets/")
        p.ids = {t["id"] for t in soup.find_all(attrs={"id": True})}
        all_ids[p.out] = p.ids
        p.toc = toc
        w = week_of(p)
        if p.rel.startswith("notes/concepts/"):
            kicker, (ht, hc) = "Concept note", ("One idea,<br>stated precisely.", "Definition. Why it matters. Related.")
        elif p.rel.startswith("eli12/"):
            kicker = f"ELI12 · Week {w}" if w else "ELI12 · Plain language"
            ht, hc = ("Same ideas,<br>plain words.", "Picture it. Count it. Try it.")
        elif w and p.rel.endswith("exam-questions.md"):
            kicker, (ht, hc) = f"Week {w} · Past papers", ("Every question,<br>with the working.", "Scan. Solve. Check.")
        elif w and p.rel.endswith("exam-focused-notes.md"):
            kicker, (ht, hc) = f"Week {w} · Exam guide", WEEK_HERO[w]
        elif w:
            kicker, (ht, hc) = f"Week {w} · Notes", WEEK_HERO[w]
        elif p.rel.startswith("sources/"):
            kicker, (ht, hc) = "Paper archive", ("Source papers,<br>kept intact.", "Extraction. Audit. Trace.")
        else:
            kicker, (ht, hc) = COURSE, ("From sound waves<br>to words.", "Sample. Transform. Decode.")
        desc = re.sub(r"\s+", " ", BeautifulSoup(body, "html.parser").find("p").get_text(" ") if soup.find("p") else p.title)[:200]
        nav = render_nav(groups, p.out)
        topline = f'<span>{html.escape(kicker)}</span><a href="{quote(posixpath.relpath("index.html", posixpath.dirname(p.out) or "."))}">All resources ↗</a>'
        page_html = shell(page_out=p.out, title=p.title, description=desc, article=p.html, nav_html=nav, kicker=kicker,
                          hero_title=ht, hero_caption=hc, topline=topline, toc=toc, overview=False,
                          pagination=pagination_html(seq, titles, p.out))
        dest = out / p.out
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(page_html, encoding="utf-8")
        text_only = re.sub(r"\s+", " ", soup.get_text(" "))
        limit = 4000 if p.rel.startswith("sources/exam-papers/extractions") else 30000
        search.append({"title": p.title, "url": p.out, "text": text_only[:limit]})

    if os.environ.get("DUP_REPORT"):  # review aid; not published
        Path(os.environ["DUP_REPORT"]).write_text(json.dumps(dup_report, indent=1), encoding="utf-8")
    # Home page.
    home = home_article(pages)
    soup = BeautifulSoup(home, "html.parser")
    home_page = Page("index.md", "# Home", virtual=True)
    toc_home = [{"level": 2, "id": h["id"], "name": h.get_text(), "children": []} for h in soup.find_all("h2") if h.get("id")]
    for i, h in enumerate(soup.find_all("h2")):
        h["id"] = re.sub(r"[^a-z0-9]+", "-", h.get_text().lower()).strip("-")
    toc_home = [{"level": 2, "id": h["id"], "name": html.escape(h.get_text()), "children": []} for h in soup.find_all("h2")]
    all_ids["index.html"] = {h["id"] for h in soup.find_all(attrs={"id": True})}
    # Validate home links with the same resolver.
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if urlsplit(href).scheme:
            continue
        if href.endswith(".html") and href[:-5] + ".md" not in pages and href != "index.html":
            errors.append(f"home: broken link {href}")
    (out / "index.html").write_text(
        shell(page_out="index.html", title="Speech Technology: Notes & Past Papers",
              description="BSEE4001 Speech Technology notes, exam-focused guides and every past-year question with a worked answer.",
              article=str(soup), nav_html=render_nav(groups, "index.html"), kicker=COURSE,
              hero_title="From sound waves<br>to words.", hero_caption="Sample. Transform. Decode.",
              topline='<span>Speech Technology · Student resources</span><a href="past-paper-topics.html">Questions by topic ↗</a>',
              toc=toc_home, overview=True, pagination=pagination_html(seq, titles, "index.html"),
              section_label="Course overview"), encoding="utf-8")
    search.append({"title": "Home", "url": "index.html", "text": "Speech Technology notes and past papers"})

    # Static files: everything that is not Markdown, plus the site assets.
    for f in CONTENT.rglob("*"):
        if f.is_file() and f.suffix != ".md":
            d = out / f.relative_to(CONTENT)
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, d)
    shutil.copytree(ASSETS, out / "assets")
    (out / ".nojekyll").write_text("")
    (out / "search.json").write_text(json.dumps(search, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    # Anchor verification (links into other pages and within a page).
    for src, dst, frag in internal:
        frag = unquote(frag)
        if frag and dst in all_ids and frag not in all_ids[dst] and not frag.startswith("fn"):
            errors.append(f"{src}: anchor #{frag} not found in {dst}")
        elif dst not in all_ids:
            errors.append(f"{src}: link target page {dst} missing")

    for w in sorted(set(warnings)):
        print("warning:", w)
    for e in sorted(set(errors)):
        print("ERROR:", e)
    print(f"built {len(pages) + 1} pages, {len(internal)} anchored links checked, "
          f"{len(set(warnings))} warnings, {len(set(errors))} errors -> {out}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
