# DL(CV) extraction verification report

Completed extraction and independent review of all 23 discovered PDFs, matching the expected inventory. Every PDF has one same-basename Markdown file beside it. All 356 physical source pages were personally inspected by the coordinator; separate Gemini extraction and audit workers report their page and asset inspection registers.

| Result | Total |
| :--- | ---: |
| Papers / verified papers | 23 / 23 |
| Academic question entries | 728 |
| Unique asset files | 546 |
| Embedded image references | 549 |
| Unresolved extraction errors | 0 |
| Answers unavailable in original PDFs | 3 |
| Additional declared question absent from original | 1 |

“Verified” means reviewed against the available source, with retained limitations. It does not repair missing original content or certify academically correct source keys. Two of the 728 entries have only a surviving question header; their missing stems are explicitly identified.

## Source limitations

| Paper | Source question | Limitation |
| :--- | :--- | :--- |
| [da5006_2024T3_Q1_NA](<da5006_2024T3_Q1_NA.md>) | 172 / `640653994508` | Source PDF terminates at page 13 immediately after Question 172 header; stem body and answer key are truncated in the source. |
| [da5006_2024T3_Q2_NA](<da5006_2024T3_Q2_NA.md>) | 157 / `6406531031092` | Source export truncated at bottom of page 12; question stem query and possible answers missing from original document. Marked as "Answer not verifiable from the source PDF". |
| [da5006_2025T3_Q2_NA](<da5006_2025T3_Q2_NA.md>) | 179 / `6406531815777` | Answer text is truncated in the source PDF: page 21 terminates immediately after 'Possible Answers :' at y=808.97 with no numerical range provided. |

2025T3_Q2_NA also declares Question 180 in its final passage, but provides no Q180 header or content. It was not invented. Its available questions total 62.5 marks versus the declared 63; the absent 0.5-mark child explains the discrepancy.

Source keys are preserved even when questionable. Examples include 2024T2_Q2 Q134 = −30, 2025T2_ET_FN Q184 = 100, and 2026T1_Q1 Q15 accepted range −6 to −5. Paper notes distinguish source-key concerns from extraction corrections.

## Independent review and corrections

All extraction, correction, and audit child tasks used Gemini 3.8 Flash through Antigravity, exact model ID `gemini-3.8-flash-high`. Actual provider instances: `antigravity`, `antigravity_stu`, `antigravity_paid_acc`. The queue targeted three simultaneous tasks per account and ran nine tasks concurrently when work was available. No alternate model/provider was substituted.

Each paper received a newly delegated independent audit, with original-PDF page inspection, asset inspection and per-question results. Additional audits followed substantial corrections. The coordinator also corrected and rechecked findings directly against the source, retaining precise evidence. Audit proposals were checked because several were themselves wrong. Corrections included fabricated options/matrices, reversed negations, derivative symbols, truncated accepted sets, shifted answers, and evidence bounding boxes. Backups and correction logs are retained.

Two early workers ended after starting OCR without producing final deliverables; these were recorded as incomplete and recovered through distinct round-2 extraction tasks. They were not counted as successful extractions. There were no active children or pending child runs at completion.

[Task registry](.extraction/tasks.json) retains all task IDs, actual assignments, terminal results and recovery history. [Verification decisions](.extraction/verification-decisions.json) maps each paper to its audits and correction evidence. [Coordinator inspection](.extraction/coordinator-inspection.json) records personally inspected pages. Per-paper audit files contain independent question-by-question pass/fail findings.

## Validation actually executed

The following were run through the shared uv environment after final corrections:

```sh
uv run --directory '/Users/manyakaistha/Downloads/DL for Computer Vision/.extraction' python '/Users/manyakaistha/Downloads/DL for Computer Vision/.extraction/validate.py'
uv run --directory '/Users/manyakaistha/Downloads/DL for Computer Vision/.extraction' python '/Users/manyakaistha/Downloads/DL for Computer Vision/.extraction/validate_consistency.py'
uv run --directory '/Users/manyakaistha/Downloads/DL for Computer Vision/.extraction' python '/Users/manyakaistha/Downloads/DL for Computer Vision/.extraction/validate_extended.py'
uv run --directory '/Users/manyakaistha/Downloads/DL for Computer Vision/.extraction' python '/Users/manyakaistha/Downloads/DL for Computer Vision/.extraction/check_source_metadata.py'
uv run --directory '/Users/manyakaistha/Downloads/DL for Computer Vision/.extraction' python '/Users/manyakaistha/Downloads/DL for Computer Vision/.extraction/check_option_fidelity.py'
uv run --directory '/Users/manyakaistha/Downloads/DL for Computer Vision/.extraction' python '/Users/manyakaistha/Downloads/DL for Computer Vision/.extraction/check_stem_fidelity.py'
uv run --directory '/Users/manyakaistha/Downloads/DL for Computer Vision/.extraction' python '/Users/manyakaistha/Downloads/DL for Computer Vision/.extraction/check_answer_fidelity.py'
uv run --directory '/Users/manyakaistha/Downloads/DL for Computer Vision/.extraction' python '/Users/manyakaistha/Downloads/DL for Computer Vision/.extraction/reconcile_exclusions.py'
```

Results: 23/23 structural checks passed; 23/23 cross-file consistency checks passed; 23/23 extended checks passed; zero source-marks mismatches; 1,214 plain options and 261 plain stems checked mechanically; 725 answer fields/option-ID mappings checked mechanically. Three source-truncated answers require the recorded limitation rather than an inferred answer. Residual diagnostic matches were reviewed and classified in [diagnostic dispositions](.extraction/diagnostic-dispositions.json). These automated checks supplement visual audits and do not independently prove fidelity.

Validation covers same-basename inventory, first H1, corresponding source links, YAML, decodable nonempty assets, sequential immediate captions, question identities, option order/IDs, answer labels/key/record agreement, answer evidence page/bounds, math environments/control characters, confirmation exclusion, completed audit tasks and coordinator page coverage. [Exclusion reconciliation](.extraction/exclusion-reconciliation.json) records 33 omitted source headers with semantic/positional reasons and zero unexplained omissions inside scope. Full outputs and console captures are under `.extraction/`.

All 23 PDF SHA-256 hashes were recomputed and match the initial manifest. Original PDFs remained unchanged. All final source documents use relative asset links; diagnostic full-page renders remain private under `.extraction/`.

## Reproducibility and evidence

The shared uv-managed project contains `pyproject.toml`, `uv.lock` and `.venv`; workers reused it. Python dependencies: PyMuPDF 2.1, Pillow 13.0.0, PyYAML 6.0.3. Native utilities used include uv 0.8.2, Poppler 25.10.0 and Tesseract 5.5.3. [Dependency versions](.extraction/versions.json) and retained scripts provide the actual environment record. Initial preparation used `uv init --bare`, `uv add ... pymupdf pillow pyyaml`, then uv-run preparation/rendering/OCR scripts.

Coordinates use PDF points with a top-left origin, `[x0,y0,x1,y1]`, and 1-based physical pages. Historical alternate coordinate encodings were normalized where found and documented in retained corrections. Structured records, image placements, source text/layout, native image assets, zoom crops, all-page renders, audit findings and backups are retained under `.extraction/`.

[Extraction index](EXTRACTION_INDEX.md) · [Final machine summary](.extraction/final-summary.json)
