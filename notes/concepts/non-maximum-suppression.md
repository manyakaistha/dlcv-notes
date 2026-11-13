---
title: Non-Maximum Suppression (NMS)
tags: [dl4cv/concept, edge-detection]
---
# Non-Maximum Suppression (NMS)

Non-Maximum Suppression is a spatial thinning algorithm that suppresses non-peak gradient responses along the direction perpendicular to an edge contour.

For a pixel $q$ with gradient angle $	heta = 	an^{-1}(I_y / I_x)$:
1. Cast a ray along direction $	heta$ and $-	heta$ passing through $q$.
2. Interpolate gradient magnitudes at the intersection points $p$ and $r$ with the adjacent 8-connected grid lines.
3. If $M(q) \ge M(p)$ and $M(q) \ge M(r)$, retain $M(q)$; otherwise, set $M(q) = 0$.
