---
title: Gradient Location and Orientation Histogram (GLOH)
tags: [dl4cv/concept, local-descriptors]
---
# Gradient Location and Orientation Histogram (GLOH)

Introduced by Mikolajczyk and Schmid (2005), GLOH extends SIFT by replacing the Cartesian $4 	imes 4$ grid with a **log-polar spatial binning grid**:
- 1 central circular bin + 8 middle annular sectors + 8 outer annular sectors = **17 spatial bins**.
- Local gradient orientations are quantized into 16 bins, yielding a $17 	imes 16 = 272$-dimensional histogram.
- **PCA Dimensionality Reduction:** The 272-D vector is projected onto the top 128 eigenvectors computed from an independent training set, enhancing distinctiveness and robustness.
