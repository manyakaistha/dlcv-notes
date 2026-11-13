---
title: Point Operations
tags: [dl4cv/concept, image-processing]
---
# Point Operations

A point operation is an image transformation where the output pixel intensity at coordinate $(m_0, n_0)$ depends strictly and solely on the input pixel intensity at that identical coordinate:
$$s = T(r)$$
where $r = I(m_0, n_0)$ and $s = \hat{I}(m_0, n_0)$.

- **Computational Complexity:** $\mathcal{O}(1)$ operations per pixel.
- **Key Examples:**
  - Dynamic range stretching: $\hat{I} = (I - I_{\min}) rac{I_{\max} - I_{\min}}{I_{	ext{high}} - I_{	ext{low}}} + I_{\min}$
  - Digital negative / Contrast reversal: $\hat{I} = I_{\max} - I + I_{\min}$
  - Global thresholding and gamma correction ($s = c r^\gamma$)
