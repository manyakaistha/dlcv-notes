# Contrastive learning

Contrastive learning trains a representation by making a designated positive pair score highly relative to a set of alternatives. The positive can be two stochastic views of one image, a synchronized observation, or a paired image and caption. A similarity function, candidate sampling scheme, and loss determine the actual learning problem. In instance discrimination, different source images commonly become negatives even when they share a semantic class. This produces possible false negatives; the name negative describes the training relationship rather than a guarantee of semantic difference. SimCLR uses augmented in-batch views, whereas MoCo maintains a dictionary of keys with a momentum encoder. Both require careful choices about invariances, augmentation, batch composition, and downstream evaluation.

## Why it matters here

Understanding which pairs are positive distinguishes SimCLR and MoCo from arbitrary class grouping, and clarifies why CLIP can use image–text pairs.

**Appears in:** [[week-11-report]] · [[week-11-exam-notes]] · [[week-11-questions]]

## Related

[[infonce-loss]] · [[clip-alignment]]
