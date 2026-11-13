---
title: Hysteresis Dual-Thresholding
tags: [dl4cv/concept, edge-detection]
---
# Hysteresis Dual-Thresholding

Single-threshold edge binarization suffers from an unavoidable trade-off: a high threshold fragments genuine faint contours, while a low threshold introduces noisy false-positive clutter.

Hysteresis resolves this dilemma using two distinct thresholds:
- **Strong Edge Pixels:** $M(x, y) \ge 	au_{	ext{high}}$ (immediately accepted).
- **Weak Edge Pixels:** $	au_{	ext{low}} \le M(x, y) < 	au_{	ext{high}}$ (conditionally retained).
- **Suppressed Non-Edges:** $M(x, y) < 	au_{	ext{low}}$ (discarded).

### Edge Linking Rule
A weak edge pixel is retained if and only if it is connected to at least one strong edge pixel directly or through an unbroken connected component of contiguous weak edge pixels.
