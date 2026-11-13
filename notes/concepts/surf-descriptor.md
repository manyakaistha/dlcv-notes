---
title: Speeded-Up Robust Features (SURF)
tags: [dl4cv/concept, local-descriptors]
---
# Speeded-Up Robust Features (SURF)

Developed by Herbert Bay et al. (ECCV 2006), SURF accelerates scale- and rotation-invariant feature detection and description:
- **Detector:** Approximates continuous Gaussian second derivatives ($rac{\partial^2 G}{\partial x^2}, rac{\partial^2 G}{\partial x \partial y}$) using piecewise constant rectangular box filters evaluated in $\mathcal{O}(1)$ time via **Integral Images**.
- **Descriptor:** Extracts Haar wavelet responses $d_x, d_y$ over a $4 	imes 4$ sub-region grid, accumulating a 64-dimensional feature vector:
  $$\mathbf{v}_{	ext{sub}} = \left[\sum d_x, \sum d_y, \sum |d_x|, \sum |d_y|ight]^T$$
