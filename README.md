# Deep Learning for Computer Vision: Notes & Past Papers

Notes and past-year questions for **DA5006 Deep Learning for Computer Vision** (IIT Madras BS Degree), published as a searchable website with an **Ask AI** button on every page.

- **[Open the website](https://manyakaistha.github.io/dlcv-notes/)**
- [Past-paper topics](https://manyakaistha.github.io/dlcv-notes/past-paper-topics.html): find questions by curriculum topic and jump to the relevant question.
- [Curriculum map](https://manyakaistha.github.io/dlcv-notes/curriculum/curriculum-map.html): explore the course scope and topic taxonomy.

## What is inside

| Part | Where | Contents |
| :-- | :-- | :-- |
| Weekly notes | `month N/week M/week-M-report.md` | Theory, derivations, figures and runnable code for Weeks 1–12 |
| Exam-focused guides | `month N/week M/week-M-exam-notes.md` | Week-by-week exam preparation |
| Past papers | `question-bank/week-NN-questions.md` | Questions and worked answers grouped by week |
| Concept notes | `notes/concepts/` | Atomic definitions connecting the weeks |
| Paper archive | `sources/exam-papers/` | Available paper transcriptions and figures |
| Classification | `classification/final/final-manifest.json` | Question-to-topic mapping, with review flags |
| Curriculum | `curriculum/` | Curriculum map and topic names |

Weeks 6–12 are provisional where marked. Worked answers are independently derived study aids, not official answer keys.

## Ask AI

Every page has an **Ask AI** stamp and a button beside each heading. Select text to ask about a passage. The helper constructs a prompt in your browser for the provider you choose or copies it; it does not call an API.

## Build the website locally

```bash
uv run scripts/build_site.py --output _site     # fails on broken links or anchors
uv run scripts/build_site.py --output _site --warn-only  # build while missing notes are landing
uv run scripts/check_render.py                  # report leftover Markdown or TeX syntax
uv run scripts/check_links.py _site             # independently crawl built HTML
uv run --no-project python -m http.server 8765 --directory _site
```

The builder records missing references in `scripts/broken-links.txt`. GitHub Actions runs the build and both independent checks, temporarily using warning mode for existing source issues, and publishes to GitHub Pages on `main`. MathJax is served from jsDelivr.

## Layout

```text
month N/week M/     Weekly Markdown notes and figures
question-bank/      Questions and worked answers
notes/concepts/     Atomic concept notes
sources/exam-papers/ Paper transcriptions and assets
curriculum/         Course map and topic taxonomy
classification/     Question classifications
scripts/            Site builder and checks
site-assets/        CSS and JavaScript for themes, search and Ask AI
.github/workflows/  GitHub Pages deployment
```
