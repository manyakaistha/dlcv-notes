---
title: 2D Spatial Convolution
tags: [dl4cv/concept, filtering]
---
# 2D Spatial Convolution

Discrete 2D convolution flips the kernel by $180^\circ$ horizontally and vertically before sliding and computing inner products:
$$G[i, j] = (H * I)[i, j] = \sum_{u=-k}^k \sum_{v=-k}^k H[u, v] I[i-u, j-v] = \sum_{u=-k}^k \sum_{v=-k}^k H[-u, -v] I[i+u, j+v]$$

### Fundamental Properties
1. **Commutativity:** $a * b = b * a$
2. **Associativity:** $a * (b * c) = (a * b) * c$
3. **Distributivity:** $a * (b + c) = (a * b) + (a * c)$
4. **Shift Invariance:** Shifting the input shifts the output identically.
