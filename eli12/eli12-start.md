---
title: "ELI12: Deep Learning for Computer Vision in plain language"
tags: [dlcv/eli12, dlcv/start]
---

# ELI12: Deep Learning for Computer Vision in plain language

**ELI12 means “explain it like I’m 12.”** These notes introduce the first four weeks of Deep Learning for Computer Vision through familiar pictures, small examples, and explanations that define the technical words as they appear. They are a first pass for building intuition before tackling the full mathematics and implementation details.

> [!TIP]
> **Suggested route.** Read a week’s ELI12 note first, then read that week’s full report and exam notes. Use the report to study the complete theory and derivations; use the exam notes to practise recognizing what a question asks and how to construct a complete answer.

## The four notes

| Week | Plain-language note | Starting idea | Then go deeper |
| :-- | :-- | :-- | :-- |
| 1 | [Images become numbers](week-1-eli12.md) | Represent an image as a grid of pixel values, then describe how simple filters detect patterns. | [Full report](../month%201/week%201/week-1-report.md) · [Exam notes](../month%201/week%201/week-1-exam-notes.md) |
| 2 | [Finding structure in images](week-2-eli12.md) | Use edges, corners, and descriptors to summarize visual structure. | [Full report](../month%201/week%202/week-2-report.md) · [Exam notes](../month%201/week%202/week-2-exam-notes.md) |
| 3 | [Learning visual representations](week-3-eli12.md) | Train a network by adjusting its internal settings to reduce prediction errors. | [Full report](../month%201/week%203/week-3-report.md) · [Exam notes](../month%201/week%203/week-3-exam-notes.md) |
| 4 | [Convolutions build visual features](week-4-eli12.md) | Reuse small filters across an image to build useful feature maps. | [Full report](../month%201/week%204/week-4-report.md) · [Exam notes](../month%201/week%204/week-4-exam-notes.md) |

## How to read an exam question

An exam question is a set of instructions with a target. Before calculating, identify what the question wants you to produce.

1. **Find the command word.** “Define” asks for a precise meaning; “derive” asks for connected mathematical steps; “compare” requires a shared basis and relevant differences; “calculate” requires a result and enough working to verify it; “explain” asks for the mechanism and why it matters.
2. **Name the object.** Identify the image, model, algorithm, or quantity being discussed. Copy down the given values, assumptions, and constraints.
3. **Mark the target.** Write down the exact requested output: a tensor shape, numerical value, diagram, equation, advantage, limitation, or sequence of steps. Do not answer a nearby but different question.
4. **Choose the matching tool.** State the relevant definition or equation, explain its symbols, and check units, dimensions, or shape before substituting values.
5. **Show the reasoning.** Keep intermediate steps visible. For comparisons, use the same criteria for each method; for calculations, show the substitution and final result; for explanations, connect cause to effect.
6. **Check completeness.** Address every part, label the final answer, and include a limitation or assumption when the question asks for one.

**A useful habit:** turn the prompt into a short checklist. If it asks for a definition, derivation, example, and limitation, make sure the final answer contains all four.

## What is authoritative?

The ELI12 notes simplify the language and choose small examples to make the ideas easier to approach. They may omit qualifications, edge cases, or derivation steps. The full weekly reports and exam notes are authoritative for complete definitions, mathematical statements, assumptions, and exam-ready detail; use them whenever precision matters or a simplified explanation seems incomplete.
