---
title: Image Interpolation Kernels
tags: [dl4cv/concept, signal-processing]
---
# Image Interpolation

Image interpolation reconstructs a continuous approximation $\hat{f}(x, y)$ from discrete pixel lattice points via continuous convolution:
$$\hat{f}(x, y) = \sum_{k, l} F[k, l] h(x - k, y - l)$$

### Common Interpolation Kernels
1. **Nearest Neighbor:** Box kernel ($h(x) = 1$ for $|x| < 0.5$). Discontinuous, causes pixelated blocking artifacts.
2. **Bilinear Interpolation:** Triangular tent kernel ($h(x) = \max(0, 1 - |x|)$). $C^0$ continuous, linear interpolation across 4 nearest neighbors.
3. **Bicubic Interpolation:** Cubic spline kernel spanning 16 nearest neighbors. $C^1$ continuous, sharper gradient reproduction and edge retention.
