---
title: Convolution Theorem
tags: [dl4cv/concept, frequency-domain, mathematics]
---
# The Convolution Theorem

The Convolution Theorem states that spatial convolution between two functions is mathematically equivalent to point-wise multiplication in the frequency domain:
$$\mathcal{F}[g * h] = \mathcal{F}[g] \cdot \mathcal{F}[h] \iff g * h = \mathcal{F}^{-1}[\mathcal{F}[g] \cdot \mathcal{F}[h]]$$

### Computational Complexity
- **Spatial 2D Convolution:** $\mathcal{O}(N^2 k^2)$ operations.
- **FFT-Based Convolution:** $\mathcal{O}(N^2 \log N)$ operations.
FFT-based filtering becomes dramatically faster when the kernel size $k$ exceeds approximately $15 	imes 15$ to $21 	imes 21$ pixels.
