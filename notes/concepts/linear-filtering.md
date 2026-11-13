---
title: Linear Filtering
tags: [dl4cv/concept, filtering]
---
# Linear Filtering

A spatial filter is linear if the operator satisfies the principle of superposition:
$$\mathcal{L}[lpha f_1 + eta f_2] = lpha \mathcal{L}[f_1] + eta \mathcal{L}[f_2]$$

In discrete image processing, a linear spatial filter computes each output pixel as an affine linear combination (weighted inner product) of pixels in a local $(2k+1) 	imes (2k+1)$ neighborhood:
$$G[i, j] = \sum_{u=-k}^k \sum_{v=-k}^k H[u, v] I[i+u, j+v]$$
