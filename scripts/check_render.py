# /// script
# requires-python = ">=3.10"
# dependencies = ["beautifulsoup4>=4.12"]
# ///
"""Heuristic render check: leftover Markdown/TeX syntax or unparsed lists in the built site."""
import glob, re, sys
from bs4 import BeautifulSoup

bad = 0
for f in sorted(glob.glob('_site/**/*.html', recursive=True)):
    if '/extractions/' in f:
        continue
    s = BeautifulSoup(open(f, encoding='utf-8').read(), 'html.parser')
    art = s.find('article')
    if not art:
        continue
    math = len(art.find_all(class_='arithmatex'))
    for t in art.find_all(['pre', 'code']):
        t.decompose()
    for t in art.find_all(class_='arithmatex'):
        t.decompose()
    txt = art.get_text('\n')
    probs = {'dollar': len(re.findall(r'\$[^\s$]', txt)), 'bold': txt.count('**'), 'wiki': txt.count('[['), 'pseudo_list_p': 0}
    for p in art.find_all('p'):
        t = p.get_text('\n')
        if len(re.findall(r'(?:^|\n)\s*(?:[-*]|\d+\.)\s+\S', t)) >= 2:
            probs['pseudo_list_p'] += 1
    if any(probs.values()):
        bad += 1
        print(f.replace('_site/', ''), probs, 'math=', math)
print('pages with render issues:', bad)
sys.exit(1 if bad else 0)
