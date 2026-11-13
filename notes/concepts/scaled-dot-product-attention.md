---
title: "Scaled dot-product attention"
status: provisional
---

# Scaled dot-product attention

Scaled dot-product attention maps a query matrix $Q$, key matrix $K$ and value matrix $V$ to $\operatorname{softmax}(QK^\top/\sqrt{d_k})V$, with softmax taken across keys for each query. The output at a query position is a convex combination of value vectors when the logits are finite and at least one key is allowed. The scaling reduces the growth of score variance with key dimension under independent unit-variance coordinate assumptions. An additive mask can exclude invalid or future positions before normalization. The queries and keys must share their inner dimension, while values may have a different feature width. In self-attention all three derive from the same sequence; cross-attention obtains them from different streams.

## Why it matters here

This concept connects the shape calculations and architectural distinctions tested in the provisional Week 9 end-term questions. Explicit assumptions about token dimensions and information flow prevent confusing an implementation detail with a general property.

**Appears in:** [[week-9-report]] · [[week-9-exam-notes]] · [[week-09-questions]]

## Related

[[multi-head-attention]] · [[position-encoding]]
