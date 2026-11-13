---
title: Edgelet Representation and Second Moment PCA
tags: [dl4cv/concept, shape-analysis]
---
# Edgelet Representation & Eigendecomposition

An **edgelet** is a short, approximately linear segment of connected edge pixels sharing similar gradient orientations.

### Extraction & PCA Orientation
1. **Quantization:** Discretize Canny gradient orientations into 8 directional bins ($45^\circ$ each).
2. **Grouping:** For reference bin $d$, extract connected components whose pixel orientations lie within adjacent bins $\{d-1, d, d+1\}$.
3. **Second Moment Covariance Matrix:** For $N$ edgelet coordinates $\{(x_i, y_i)\}_{i=1}^N$:
   $$C_{	ext{edgelet}} = rac{1}{N} egin{bmatrix} \sum (x_i - \mu_x)^2 & \sum (x_i - \mu_x)(y_i - \mu_y) \ \sum (x_i - \mu_x)(y_i - \mu_y) & \sum (y_i - \mu_y)^2 \end{bmatrix}$$
4. **Orientation via Eigendecomposition:** The principal eigenvector $\mathbf{v}_1 = [v_{1, x}, v_{1, y}]^T$ associated with largest eigenvalue $\lambda_1$ defines the edgelet orientation:
   $$	heta_{	ext{edgelet}} = 	an^{-1}\left(rac{v_{1, y}}{v_{1, x}}ight)$$
   The eigenvalue ratio $\lambda_1 / \lambda_2$ quantifies structural straightness.
