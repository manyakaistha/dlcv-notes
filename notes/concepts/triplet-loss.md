# Triplet loss

Triplet loss learns an embedding by comparing an anchor with a matched positive and an unmatched negative. With squared Euclidean distances and margin $\alpha$, the conventional hinge form is $\max(0,\|f(a)-f(p)\|^2-\|f(a)-f(n)\|^2+\alpha)$. It is zero when that negative is sufficiently farther from the anchor than the positive. The loss is nonnegative; an unhinged expression can be negative. The scale and units of the margin depend on whether distances are squared, and the choice of sampled or mined triplets determines which comparisons produce gradients. Siamese branches apply shared encoder parameters, so multiple forward passes do not create multiple independent parameter sets.

## Why it matters here

Week 8 uses this geometry for face verification and identification. Numerical questions require computing each distance before the hinge and counting shared parameters only once; a zero loss for one triplet does not establish correct ranking for all examples.

**Appears in:** [[week-8-report]] · [[week-8-exam-notes]] · [[week-08-questions]]

## Related

[[variational-autoencoder]] · [[kullback-leibler-divergence]] · [[generative-adversarial-network]]
