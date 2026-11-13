---
title: Maximally Stable Extremal Regions (MSER)
tags: [dl4cv/concept, blob-detection]
---
# Maximally Stable Extremal Regions (MSER)

Formulated by Jiri Matas et al. (BMVC 2002), MSER is an affine-invariant blob detector based on monotonic intensity threshold sweeping.

### Algorithmic Mechanics
1. **Threshold Sweep:** Sweep a threshold $g$ across $[0, 255]$, binarizing the image and tracking the growth of connected components (extremal regions $Q_g$).
2. **Stability Evaluation:** Measure the area growth rate of region $Q_i$ across step $\Delta$:
   $$q(i) = rac{|Q_{i+\Delta} \setminus Q_{i-\Delta}|}{|Q_i|}$$
3. **Extremal Selection:** Select regions that attain a local minimum of $q(i)$ as Maximally Stable Extremal Regions.
- **Invariance:** MSER is strictly invariant to monotonic continuous transformations of image intensity ($I 	o g(I)$) and continuous affine spatial warps.
