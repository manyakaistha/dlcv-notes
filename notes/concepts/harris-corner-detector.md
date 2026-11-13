---
title: Harris Corner Detector
tags: [dl4cv/concept, feature-detection]
---
# Harris Corner Detector

Introduced by Chris Harris and Mike Stephens (1988), the Harris Corner Detector identifies 2D interest points where image intensity varies substantially across multiple spatial directions, overcoming the aperture problem.

### Autocorrelation Matrix (Structure Tensor)
For a small shift $(\Delta x, \Delta y)$, the change in intensity over a window $w(u, v)$ is approximated via first-order Taylor expansion:
$$E(\Delta x, \Delta y) pprox [\Delta x, \Delta y] \, \mathbf{A} \, egin{bmatrix} \Delta x \ \Delta y \end{bmatrix}$$
where the structure tensor $\mathbf{A}$ is:
$$\mathbf{A} = \sum_{u, v} w(u, v) egin{bmatrix} I_x^2 & I_x I_y \ I_x I_y & I_y^2 \end{bmatrix}$$

### Harris Cornerness Response
To avoid computing explicit matrix eigenvalues $\lambda_1, \lambda_2$, Harris proposed the scalar metric:
$$R = \det(\mathbf{A}) - \kappa \, 	ext{trace}^2(\mathbf{A}) = \lambda_1 \lambda_2 - \kappa (\lambda_1 + \lambda_2)^2$$
(standardly $\kappa \in [0.04, 0.06]$).
- **Corner:** $R > 0$ (both $\lambda_1, \lambda_2$ are large).
- **Edge:** $R < 0$ (one eigenvalue dominates, $\lambda_1 \gg \lambda_2$).
- **Flat:** $R pprox 0$ ($\lambda_1, \lambda_2 pprox 0$).
