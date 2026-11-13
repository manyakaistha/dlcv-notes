---
title: Cross-Correlation
tags: [dl4cv/concept, filtering]
---
# 2D Cross-Correlation

2D discrete cross-correlation slides a filter kernel $H$ across an image $I$ without spatial flipping:
$$G[i, j] = (H \otimes I)[i, j] = \sum_{u=-k}^k \sum_{v=-k}^k H[u, v] I[i+u, j+v]$$

Cross-correlation measures the localized sliding dot product similarity between the template kernel and sub-patches of the image. Unlike convolution, cross-correlation is generally **not commutative** ($H \otimes I 
e I \otimes H$).
