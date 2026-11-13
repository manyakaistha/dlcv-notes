---
title: Scale-Space Theory
tags: [dl4cv/concept, multi-scale]
---
# Scale-Space Theory

Natural scenes contain physical objects at multiple physical scales. Scale-space theory (Witkin 1983, Koenderink 1984, Lindeberg 1994) represents an image as a one-parameter continuous family of smoothed images:
$$L(x, y; \sigma) = G(x, y; \sigma) * I(x, y)$$
where $G(x, y; \sigma) = rac{1}{2\pi\sigma^2} e^{-(x^2 + y^2)/(2\sigma^2)}$ is the only linear scale-space kernel guaranteed not to create new spurious extrema as scale $\sigma$ increases.

### Characteristic Scale Selection
Evaluating normalized differential operators across scales (such as scale-normalized Laplacian $\sigma^2 |
abla^2 L|$) attains a local maximum at a **characteristic scale** $\sigma^*$ reflecting the physical radius of the underlying feature.
