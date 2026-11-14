#!/usr/bin/env python3
"""Build deterministic exam routes, question index and topic statistics from the manifest."""
import json
import re
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
topics = json.loads((ROOT / 'curriculum/topics.json').read_text())
questions = json.loads((ROOT / 'classification/final/final-manifest.json').read_text())
by_id = {t['id']: t for t in topics}
assert len(by_id) == len(topics)
assert len(questions) == 728 and len({(q['source_paper'], q['question_id']) for q in questions}) == 728
assert all(q['topic_id'] in by_id and q['primary_week'] == by_id[q['topic_id']]['week'] for q in questions)

def slug(s):
    # GitHub heading IDs: lowercase, strip punctuation, replace each whitespace with '-'.
    return re.sub(r'\s', '-', re.sub(r'[^\w\s-]', '', s.lower()))

def stat(t, exam=None):
    qs = [q for q in questions if q['topic_id'] == t['id'] and (exam is None or q['exam_type'] == exam)]
    total = sum((Decimal(str(q['marks'])) for q in qs), Decimal(0))
    total_value = int(total) if total == total.to_integral_value() else float(total)
    return {'occurrences': len(qs), 'mean_marks': float(total / len(qs)) if qs else None, 'total_marks': total_value}

stats = [{'week': t['week'], 'topic_id': t['id'], 'name': t['name'], 'status': t['status'],
          'all': stat(t), 'by_exam': {e: stat(t, e) for e in ('Q1', 'Q2', 'ET')}} for t in topics]
(ROOT / 'classification/final/topic-stats.json').write_text(json.dumps(stats, indent=2, ensure_ascii=False) + '\n')

def bank_link(t):
    # Banks omit topics with no questions; point to the bank when no topic heading exists.
    bank = ROOT / f"question-bank/week-{t['week']:02}-questions.md"
    heading = '## Topic: ' + t['name']
    anchor = '#' + slug('Topic: ' + t['name']) if bank.exists() and heading in bank.read_text() else ''
    return f"[Questions](question-bank/week-{t['week']:02}-questions.md{anchor})"

def tables(exam, weeks):
    selected = [s for s in stats if s['week'] in weeks]
    maximum = max((s['all' if exam is None else 'by_exam'][exam] if exam else s['all'])['total_marks'] for s in selected)
    out = []
    for week in weeks:
        entries = [s for s in selected if s['week'] == week]
        if not entries:
            continue
        out += [f"### Week {week}" + (' — provisional' if week >= 6 else ''), '', '| Rank | Priority | Topic | Occurrences | Mean marks | Score | Resources |', '| ---: | :--- | :--- | ---: | ---: | ---: | :--- |']
        key = lambda s: s['all'] if exam is None else s['by_exam'][exam]
        ranks = {s['topic_id']: 1 + sum(key(o)['total_marks'] > key(s)['total_marks'] for o in selected) for s in selected}
        for s in sorted(entries, key=lambda x: (-key(x)['total_marks'], x['name'])):
            d = key(s); score = d['total_marks']
            priority = 'P1' if score and score * 2 >= maximum else 'P2' if score and score * 5 >= maximum else 'P3'
            mean = f"{d['mean_marks']:.2f}" if d['mean_marks'] is not None else '—'
            topic = by_id[s['topic_id']]
            out.append(f"| {ranks[s['topic_id']]} | {priority} | {s['name'].replace('|', ' / ')} | {d['occurrences']} | {mean} | {score} | [[week-{week}-report\\|Report]] · [[week-{week}-exam-notes\\|Exam notes]] · {bank_link(topic)} |")
        out.append('')
    return out

lines = ['---', 'title: "Deep Learning for Computer Vision — Exam Study Guide"', 'map: "[[Knowledge-Map]]"', 'tags: [dl4cv/exam-study]', '---', '', '# Exam Study Guide', '', '[[Knowledge-Map|Knowledge Map]] · [[exam-question-index|Question index]]', '', 'Choose the route for your exam. Work P1 first, then P2, then P3; study prerequisite concepts in order and practise the linked questions without looking at their answers.', '', 'Each occurrence is one manifest question assigned to its primary topic. Score = occurrences × mean marks = sum of assigned marks; repeated questions count separately. Mean is undefined for zero occurrences. Rank is competition rank across the applicable route, with tied scores sharing rank. For each route, P1 has a positive score at least 50% of that route’s maximum; P2 has a positive score at least 20% but below 50%; P3 is below 20%, including zero. Cut-offs describe this evidence, not a prediction or the importance of prerequisites.', '', 'Weeks 6–12 are **provisional**: topics inferred from past papers; replace when official syllabus is available. Topic-bank links lead to the topic heading when present, otherwise to the week bank. In-progress banks may not yet contain every question.', '', '## Quiz 1 route', '', 'Weeks 1–4; statistics use Quiz 1 questions only.', '']
lines += tables('Q1', range(1,5))
lines += ['## Quiz 2 route', '', 'Weeks 5–8 are the main route; Weeks 1–4 are included for earlier material. Statistics use Quiz 2 questions only.', ''] + tables('Q2', [5,6,7,8,1,2,3,4])
lines += ['## End-term route', '', 'Begin with Weeks 9–12, then revisit Weeks 1–8. Statistics use end-term questions only.', ''] + tables('ET', [9,10,11,12,1,2,3,4,5,6,7,8])
lines += ['## Overall evidence across all exams', '', 'This complete ranking uses all manifest questions and provides a cross-exam comparison; use the routes above for exam-specific preparation.', ''] + tables(None, range(1,13))
lines += ['## Reproduce', '', 'Run `uv run python scripts/compute_topic_stats.py` from the repository root. The manifest and curriculum are the inputs; the script writes this guide, the question index, and `classification/final/topic-stats.json`.', '']
(ROOT / 'exam-study-guide.md').write_text('\n'.join(lines))

lines = ['---', 'title: "Deep Learning for Computer Vision — Exam Question Index"', 'map: "[[Knowledge-Map]]"', 'tags: [dl4cv/past-papers]', '---', '', '# Exam Question Index', '', '[[Knowledge-Map|Knowledge Map]] · [[exam-study-guide|Exam study guide]]', '', f'All {len(questions)} manifest question occurrences are listed by paper. Week and topic are the primary classification; weeks 6–12 are provisional. Bank links follow the published heading rule; a bank still in progress may not yet contain its target.', '']
for paper in sorted({q['source_paper'] for q in questions}):
    lines += [f'## {paper}', '', '| Term | Exam | Q# | Marks | Week | Topic | Question |', '| :--- | :--- | ---: | ---: | ---: | :--- | :--- |']
    for q in sorted((q for q in questions if q['source_paper'] == paper), key=lambda q: (q['source_number'], str(q['question_id']))):
        week = q['primary_week']; topic = by_id[q['topic_id']]['name'].replace('|', ' / ')
        heading = f"{paper} · Q{q['source_number']} · {q['marks']} marks · ID {q['question_id']}"
        anchor = slug(heading)
        term = paper.split('_')[1]
        lines.append(f"| {term} | {q['exam_type']} | {q['source_number']} | {q['marks']} | {week}{' (provisional)' if week >= 6 else ''} | {topic} | [ID {q['question_id']}](question-bank/week-{week:02}-questions.md#{anchor}) |")
    lines.append('')
(ROOT / 'exam-question-index.md').write_text('\n'.join(lines))
print(f'Generated statistics for {len(topics)} topics and index for {len(questions)} questions.')
