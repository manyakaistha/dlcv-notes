---
title: Kernel Separability
tags: [dl4cv/concept, filtering, linear-algebra]
---
# Kernel Separability

A 2D convolution kernel $\mathbf{K} \in \mathbb{R}^{k 	imes k}$ is separable if it can be decomposed into the outer product of two 1D kernels:
$$\mathbf{K} = \mathbf{v} \mathbf{h}^T$$

- **Computational Speedup:** Reduces cost from $k^2$ multiplications per pixel to $2k$, yielding an acceleration factor of $rac{k}{2}$.
- **SVD Rank-1 Condition:** A kernel is separable if and only if its Singular Value Decomposition (SVD) has exactly one non-zero singular value ($	ext{rank}(\mathbf{K}) = 1$):
  $$\mathbf{K} = \sigma_1 \mathbf{u}_1 \mathbf{v}_1^T \implies \mathbf{v} = \sqrt{\sigma_1} \mathbf{u}_1, \quad \mathbf{h} = \sqrt{\sigma_1} \mathbf{v}_1$$
