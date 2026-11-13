---
title: "Feature pyramid network"
status: provisional
---

# Feature pyramid network

A feature pyramid network constructs semantically rich feature maps at multiple spatial resolutions from a backbone hierarchy. A top-down pathway upsamples deep, coarse features; lateral projections bring shallower features to compatible channel dimensions before combination. Subsequent convolutions produce maps on which prediction heads can operate. The hierarchy helps reuse features across object scales without independently running a backbone on every image scale. The exact level assignment and interpolation method are implementation choices, and the spatial and channel dimensions must agree at each addition.

## Why it matters here

Detection questions test why high-resolution features need deeper semantic information and how many anchors exist over multiple levels. The total candidate anchors equal $\sum_l H_lW_lA_l$ when level $l$ has $A_l$ anchors per location. FPN itself does not perform non-maximum suppression.

**Appears in:** [[week-6-report]] · [[week-6-exam-notes]] · [[week-06-questions]]

## Related

[[focal-loss]] · [[intersection-over-union]] · [[semantic-segmentation]]
