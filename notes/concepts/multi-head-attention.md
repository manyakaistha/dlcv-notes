---
title: "Multi-head attention"
status: provisional
---

# Multi-head attention

Multi-head attention computes several attention operations using separately learned query, key and value projections, concatenates their outputs, and applies a learned output projection. In the common configuration with model width $D$ and $h$ heads, each head has width $D/h$, and the concatenated representation returns to width $D$. Each head can learn a different comparison and value transformation, although neither distinct semantics nor causal interpretability is guaranteed. With three combined $D\times D$ input projections and a $D\times D$ output projection, the block has $4D^2$ weights before biases. Its score activations scale quadratically with token length under dense attention, independently of the number of learned projection weights.

## Why it matters here

This concept connects the shape calculations and architectural distinctions tested in the provisional Week 9 end-term questions. Explicit assumptions about token dimensions and information flow prevent confusing an implementation detail with a general property.

**Appears in:** [[week-9-report]] · [[week-9-exam-notes]] · [[week-09-questions]]

## Related

[[scaled-dot-product-attention]] · [[vision-transformer-patches]]
