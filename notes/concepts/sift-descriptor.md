---
title: Scale-Invariant Feature Transform (SIFT)
tags: [dl4cv/concept, local-descriptors]
---
# Scale-Invariant Feature Transform (SIFT)

Published by David Lowe (IJCV 2004), SIFT extracts distinctive local invariant features robust to scale, 2D rotation, affine viewpoint distortion, and illumination changes.

### SIFT 4-Step Pipeline
1. **Scale-Space Extrema Detection:** Detect local extrema across adjacent DoG scale levels in a $3 	imes 3 	imes 3$ volume (26 neighbors).
2. **Keypoint Localization:** Fit 3D quadratic Taylor expansion for sub-pixel localization; reject low-contrast points ($|D| < 0.03$) and edge responses via Hessian trace/determinant ratio $rac{	ext{Tr}(H)^2}{	ext{Det}(H)} < rac{(r+1)^2}{r}$ ($r=10$).
3. **Orientation Assignment:** Compute local gradient magnitudes and orientations, building a 36-bin orientation histogram to assign a canonical dominant orientation $	heta_0$.
4. **Keypoint Descriptor:** Extract a $16 	imes 16$ sample window rotated to canonical orientation, subdivided into a $4 	imes 4$ spatial grid. Accumulate an 8-bin orientation histogram in each sub-region ($4 	imes 4 	imes 8 = 128$ dimensions), normalize to unit length, clip at $0.2$, and re-normalize.
