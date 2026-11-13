---
title: "Intersection over union"
status: provisional
---

# Intersection over union

Intersection over union (IoU) measures overlap between two nonempty sets as $|A\cap B|/|A\cup B|$. For boxes with continuous coordinates, compute each overlap dimension by subtracting the larger lower coordinate from the smaller upper coordinate and clamping at zero. Their product is the intersection area; union is the sum of individual areas minus the intersection. IoU is symmetric, bounded between zero and one for positive-area boxes, and invariant to a common uniform scale. Coordinate conventions matter: inclusive integer pixels and continuous coordinates yield different widths.

## Why it matters here

IoU supports anchor matching, detection evaluation, and overlap-based localization losses. These uses have different purposes and may use different thresholds. Ordinary IoU has a flat zero-overlap region, motivating alternative box losses for disjoint predictions.

**Appears in:** [[week-6-report]] · [[week-6-exam-notes]] · [[week-06-questions]]

## Related

[[focal-loss]] · [[feature-pyramid-network]] · [[semantic-segmentation]]
