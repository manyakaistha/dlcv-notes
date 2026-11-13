---
title: Digital Image Representation
tags: [dl4cv/concept, image-processing]
---
# Digital Image Representation

A digital image is mathematically modeled either as a continuous 2D intensity function $f: \mathbb{R}^2 	o \mathbb{R}$ or as a discretized third-order tensor $\mathbf{I} \in \mathbb{R}^{H 	imes W 	imes C}$.
Here, $H$ is image height, $W$ is width, and $C$ represents spectral channels (standardly $C=3$ for RGB or $C=1$ for grayscale).

In uncompressed 8-bit systems, pixel values are quantized to integers $I(x, y) \in \{0, 1, \dots, 255\}$, commonly normalized to $[0.0, 1.0]$ in deep learning pipelines to avoid activation saturation and gradient explosion.
