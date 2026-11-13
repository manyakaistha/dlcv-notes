---
title: Difference of Gaussians (DoG)
tags: [dl4cv/concept, multi-scale]
---
# Difference of Gaussians (DoG)

The Difference of Gaussians is an efficient bandpass approximation to the scale-normalized Laplacian of Gaussian (LoG):
$$D(x, y; \sigma) = (G(x, y; k\sigma) - G(x, y; \sigma)) * I(x, y) = L(x, y; k\sigma) - L(x, y; \sigma)$$

By the heat diffusion equation $rac{\partial L}{\partial \sigma} = \sigma 
abla^2 L$:
$$rac{\partial L}{\partial \sigma} = \lim_{k 	o 1} rac{L(k\sigma) - L(\sigma)}{k\sigma - \sigma} \implies L(k\sigma) - L(\sigma) pprox (k - 1) \sigma^2 
abla^2 L$$
DoG requires only subtracting adjacent blurred images in a Gaussian pyramid, eliminating direct computation of second spatial derivatives.
