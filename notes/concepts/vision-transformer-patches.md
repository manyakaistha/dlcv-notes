---
title: "Vision Transformer patches"
status: provisional
---

# Vision Transformer patches

A Vision Transformer commonly converts an image into non-overlapping patches, flattens each patch and applies a shared learned linear projection to produce a sequence of model-width vectors. For an image of height $H$, width $W$, $C$ channels and patch side $P$ dividing both dimensions, there are $(H/P)(W/P)$ patches, each containing $P^2C$ scalars. Positional embeddings identify patch locations; an optional class token can collect image-level information. Transformer encoder layers then exchange information among the tokens. The original isotropic design preserves token-grid resolution and embedding width in its encoder, but hierarchical variants may change them. Patch count, scalar count and learned projection parameter count are different quantities.

## Why it matters here

This concept connects the shape calculations and architectural distinctions tested in the provisional Week 9 end-term questions. Explicit assumptions about token dimensions and information flow prevent confusing an implementation detail with a general property.

**Appears in:** [[week-9-report]] · [[week-9-exam-notes]] · [[week-09-questions]]

## Related

[[position-encoding]] · [[multi-head-attention]]
