---
title: 2D Discrete Fourier Transform
tags: [dl4cv/concept, frequency-domain]
---
# 2D Discrete Fourier Transform (DFT)

The 2D DFT decomposes a spatial digital image $f(x, y)$ of size $M 	imes N$ into a linear combination of complex orthogonal sinusoids:
$$F(u, v) = \sum_{x=0}^{M-1} \sum_{y=0}^{N-1} f(x, y) e^{-j 2\pi \left(rac{ux}{M} + rac{vy}{N}ight)}$$

- **Magnitude Spectrum:** $|F(u, v)| = \sqrt{R^2(u, v) + I^2(u, v)}$ encodes frequency amplitude and luminance contrast.
- **Phase Spectrum:** $\phi(u, v) = 	ext{atan2}(I(u, v), R(u, v))$ encodes spatial geometric structure and edge alignment.
