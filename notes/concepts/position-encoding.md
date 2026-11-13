---
title: "Position encoding"
status: provisional
---

# Position encoding

Position encoding supplies information about token order or location to an architecture whose basic self-attention operation otherwise commutes with a simultaneous permutation of input rows. Absolute encodings associate a vector with each sequence position and are commonly added to token embeddings of equal width. They may be learned or constructed from sinusoidal functions. Relative position methods instead incorporate pairwise positional relationships, often through attention scores. The token embedding represents content, whereas the positional representation identifies its slot or relation to other slots. Without an appropriate positional signal or asymmetric structural constraint, a sequence model cannot distinguish permutations merely from the order in which rows are presented. Pooling can make a whole-model output invariant even when its tokenwise layers are equivariant.

## Why it matters here

This concept connects the shape calculations and architectural distinctions tested in the provisional Week 9 end-term questions. Explicit assumptions about token dimensions and information flow prevent confusing an implementation detail with a general property.

**Appears in:** [[week-9-report]] · [[week-9-exam-notes]] · [[week-09-questions]]

## Related

[[scaled-dot-product-attention]] · [[vision-transformer-patches]]
