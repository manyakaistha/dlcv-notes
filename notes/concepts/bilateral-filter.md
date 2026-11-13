---
title: Bilateral Filter
tags: [dl4cv/concept, filtering, non-linear]
---
# Bilateral Filter

The bilateral filter is a non-linear, edge-preserving smoothing filter that weights neighboring pixels by combining spatial geometric proximity and radiometric intensity similarity:
$$I^{	ext{filtered}}(p) = rac{1}{W_p} \sum_{q \in \Omega} I(q) \exp\left(-rac{\|p - q\|^2}{2\sigma_s^2}ight) \exp\left(-rac{|I(p) - I(q)|^2}{2\sigma_r^2}ight)$$
where $W_p$ is a normalization constant ensuring filter weights sum to 1.
