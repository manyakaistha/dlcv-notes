---
title: Median Filter
tags: [dl4cv/concept, filtering, non-linear]
---
# Median Filter

The median filter is a non-linear order-statistic spatial filter that replaces each central pixel with the median value of all pixels in its local neighborhood:
$$\hat{I}(x, y) = 	ext{median}\left(\{I(x+u, y+v) \mid (u, v) \in \mathcal{N}\}ight)$$

- **Primary Strength:** Completely eliminates impulse, spike, and salt-and-pepper noise without blurring sharp step edges or spreading outlier values.
