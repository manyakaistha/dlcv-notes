---
title: Shape Context Descriptor
tags: [dl4cv/concept, shape-matching]
---
# Shape Context

Developed by Serge Belongie, Jitendra Malik, and Jan Puzicha (PAMI 2002), Shape Context describes the global spatial distribution of a shape relative to a reference contour point $p_i$.

### Log-Polar Histogram
A log-polar coordinate grid with 5 radial bins (logarithmic spacing) and 12 angular bins (60 bins total) is centered at point $p_i$:
$$h_i(k) = \#\{q 
e p_i \mid (q - p_i) \in 	ext{bin}(k)\}$$

### Matching Cost
The matching cost between two points $p_i$ and $q_j$ across two shapes is evaluated via the $\chi^2$ test statistic:
$$C_{ij} = C(p_i, q_j) = rac{1}{2} \sum_{k=1}^K rac{(h_i(k) - h_j(k))^2}{h_i(k) + h_j(k)}$$
Optimal one-to-one point correspondences are solved using the Hungarian bipartite matching algorithm.
