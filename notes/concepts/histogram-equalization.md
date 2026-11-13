---
title: Histogram Equalization
tags: [dl4cv/concept, image-processing]
---
# Histogram Equalization

Histogram equalization is a non-linear monotonic point operation that transforms the pixel intensity distribution of an image so that the output histogram approximates a uniform distribution, maximizing image contrast and dynamic range.

### Governing Formula
For an image with $L$ gray levels and normalized probability density $p_r(r_k) = rac{n_k}{MN}$, the discrete transformation is given by the cumulative distribution function (CDF):
$$s_k = T(r_k) = \left\lfloor (L - 1) \sum_{j=0}^k p_r(r_j) ightfloor = \left\lfloor rac{L - 1}{MN} \sum_{j=0}^k n_j ightfloor$$
