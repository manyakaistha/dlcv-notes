---
title: Image Aliasing and Anti-Aliasing
tags: [dl4cv/concept, signal-processing]
---
# Image Aliasing

When a continuous or discrete visual signal is sampled at a rate below the Nyquist limit ($f_s < 2 f_{\max}$), high-frequency spectral components fold across the Nyquist boundary into low-frequency bins. This creates illusory low-frequency artifacts such as **Moiré patterns**, jagged staircasing, and false textures.

### Anti-Aliasing
To downsample an image by a factor of $r$ without aliasing, one must apply a low-pass anti-aliasing pre-filter (e.g. Gaussian blur) with cutoff $\omega_c \le rac{\pi}{r}$ prior to decimation.
