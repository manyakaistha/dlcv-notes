---
title: Canny Edge Detector
tags: [dl4cv/concept, edge-detection]
---
# Canny Edge Detector

Formulated by John Canny in 1986, the Canny Edge Detector is an optimal differential edge detection pipeline designed around three mathematical criteria:
1. **Low Error Rate:** Low probability of false positives (marking non-edges) and false negatives (missing real edges).
2. **Localization:** Minimal Euclidean distance between detected edge pixels and true physical edges.
3. **Single Response:** Eliminating multiple responses to a single edge (thin 1-pixel ridges).

### Four-Stage Algorithmic Pipeline
1. **Gaussian Smoothing:** Convolve image $I$ with a 2D Gaussian filter $G_\sigma$ to suppress high-frequency sensor noise.
2. **Directional Derivative Computation:** Compute spatial partial derivatives $I_x = rac{\partial (G * I)}{\partial x}$ and $I_y = rac{\partial (G * I)}{\partial y}$, obtaining gradient magnitude $M(x, y) = \sqrt{I_x^2 + I_y^2}$ and orientation $	heta(x, y) = 	an^{-1}(I_y / I_x)$.
3. **Non-Maximum Suppression (NMS):** Thin wide gradient ridges into 1-pixel contours by suppressing any pixel whose magnitude is not a local maximum along its gradient normal vector.
4. **Hysteresis Dual-Thresholding & Edge Linking:** Classify pixels using two thresholds ($	au_{	ext{high}}, 	au_{	ext{low}}$), retaining weak edges only if they connect via an unbroken chain to a strong edge.
