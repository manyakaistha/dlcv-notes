---
title: "DETR set prediction"
status: provisional
---

# DETR set prediction

DETR formulates object detection as direct prediction of a set of class and bounding-box pairs. A backbone creates visual features, a Transformer encodes them, and a decoder uses learned object queries to produce a fixed number of candidate slots. Bipartite matching assigns each ground-truth object to a distinct predicted slot using a cost involving classification and localization. Matched outputs are supervised by corresponding object and box losses; unmatched slots are supervised as no-object. This formulation removes the need for a separate non-maximum suppression stage in the original detector. The fixed slot budget caps the output set size, and downsampled features can make small objects difficult to represent. Matching is an assignment operation rather than an attention probability.

## Why it matters here

This concept connects the shape calculations and architectural distinctions tested in the provisional Week 9 end-term questions. Explicit assumptions about token dimensions and information flow prevent confusing an implementation detail with a general property.

**Appears in:** [[week-9-report]] · [[week-9-exam-notes]] · [[week-09-questions]]

## Related

[[vision-transformer-patches]] · [[multi-head-attention]]
