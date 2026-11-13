---
title: Normalized Cross-Correlation (NCC)
tags: [dl4cv/concept, template-matching]
---
# Normalized Cross-Correlation (NCC)

Normalized Cross-Correlation computes the zero-mean, unit-variance normalized cosine similarity between a template $T$ and local image patches:
$$	ext{NCC}(x, y) = rac{\sum_{u, v} (T[u, v] - ar{T})(I[x+u, y+v] - ar{I}_{x, y})}{\sqrt{\sum_{u, v} (T[u, v] - ar{T})^2 \sum_{u, v} (I[x+u, y+v] - ar{I}_{x, y})^2}}$$

### Invariance Property
NCC is strictly invariant to affine transformations of image brightness and contrast ($I 	o lpha I + eta$ for $lpha > 0$).
