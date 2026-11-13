# PLAN.md — DL for Computer Vision exam-prep site (shared contract for all agents)

Goal: a docsify study site (same style as the LLM / Speech Technology sites in github.com/manyakaistha/Notes) for IITM "Deep Learning for Computer Vision" (paper code `da5006`): week notes, exam notes, week-wise PYQ question banks with worked answers, a frequency/marks study guide, concept notes.

Read `AGENTS.md` (vault standards) first. Key rules: Obsidian wikilinks, quoted frontmatter links, no invented numbers, any Python via `uv run` only, deterministic. Do not waste tokens: read only what your task needs.

## Exam scope rules (set by the student — authoritative)
- Paper name `..._Q1_...` = Quiz 1: covers **weeks 1–4 only**. Every Q1 question MUST map to a week in 1–4 (never 5+).
- `..._Q2_...` = Quiz 2: covers **weeks 5–8**, plus some weeks 1–4.
- `..._ET_...` = End term: weeks 1–12, **focus on weeks 9–12**.
- A question's `primary_week` must respect these ranges. Terms: 2024T1 … 2026T2.

## Syllabus (screenshots in `screenshots/syllabus-week{1..4}.png`)
- W1: Course Intro; History (opt); Image Formation (opt); Image Representation; Linear Filtering; Image in Frequency Domain; Image Sampling.
- W2: Edge Detection; Edges→Blobs and Corners; Scale Space, Image Pyramids, Filter Banks; Feature Detectors SIFT & variants; Image Segmentation; Other Feature Spaces; Human Visual System.
- W3: NN review (2 parts); Feedforward NN & Backprop (2); Gradient Descent & Variants (2); Regularization (2); Improving Training of NNs (2).
- W4: CNN intro (2 parts); Backprop in CNNs; CNN architectures for classification: AlexNet, VGG.
- W5: documented in `month 2/week 5/` (Inception, ResNet, MobileNet, interpretability/visualization, transfer learning, object detection R-CNN family/YOLO).
- W6–W12: **syllabus not supplied → PROVISIONAL.** Derive topic clusters from Q2/ET questions that fall outside W1–5, ordered in the most plausible course sequence; mark every W6–12 page `status: provisional` with a banner "topics inferred from past papers; replace when official syllabus is available".

## Data
- Extracted papers: `sources/exam-papers/da5006_<term>_<Q1|Q2|ET>_<NA|AN|FN>.md` (+ `assets/`). 728 questions, each has Question ID, type, marks, options, correct answer, source evidence. 3 answers are unavailable (truncated PDFs) — keep flagged, never guess.
- Prior classification (partly WRONG; use as hints only): `sources/classification/classification-manifest.json`, `needs-review.csv`, `week-{1..5}-pyqs.md`. Known defects: 11 Q1 questions were placed in week 5/unassigned; ~290 Q2/ET questions unassigned; weeks 6–12 absent.
- Existing notes: `month 1/week 1..4/`, `month 2/week 5/` (`week-N-report.md`, `week-N-exam-notes.md`), `notes/concepts/*.md`, `Knowledge-Map.md`.

## Target artifacts / owners (disjoint files per agent)
1. `curriculum/topics.json` + `curriculum/curriculum-map.md`: topic taxonomy W1–12: `[{"week":N,"id":"w3-backprop","name":"…","keywords":[…],"syllabus_item":"…","status":"official|provisional"}]` (4–8 topics/week).
2. `classification/final/` : `final-manifest.json` — one record per question (source_paper, question_id, source_number, marks, exam_type, primary_week 1–12, related_weeks, topic_id, confidence, rationale ≤25 words, flag_for_review bool). Valid for all 728. Validator `scripts/validate_classification.py` (run with `uv run`) enforcing the scope rules above and 728 unique (paper, question_id).
3. `question-bank/week-NN-questions.md` (NN=01..12): per week, grouped by topic (`## Topic: …`), each question: full stem (copy source wording; images via relative path to `../sources/exam-papers/assets/...`), options, **correct answer**, and a 2–5 line worked explanation (derive numerics yourself and check with `uv run python`; if the source key disagrees with your derivation, report in `question-bank/DISCREPANCIES.md`, keep the source key as primary). Header: counts by exam type and marks.
4. Notes for weeks 6–12: `month M/week N/week-N-report.md` (shorter than W1–5 reports is fine, ≥2000 words, with equations, figures optional) and `week-N-exam-notes.md` (formulas, traps, 1-line recalls) + any new `notes/concepts/*.md`. Weeks 1–5: audit existing notes against the question bank and add missing high-frequency points only.
5. `exam-study-guide.md` (topic ranking: occurrences × mean marks, per week, like the LLM guide), `exam-question-index.md`, updated `Knowledge-Map.md`, `_sidebar.md`, `README.md`, `index.html`, `.github/workflows/pages.yml`, `scripts/check_links.py`.

## Git protocol
Each agent works in its own worktree, commits only its owned files, then `git pull --rebase origin main && git push origin HEAD:main`. Never force-push. Never edit another agent's files. Report in ≤10 lines: files written, counts, anything unresolved.
