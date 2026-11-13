# Kullback–Leibler divergence

Kullback–Leibler (KL) divergence measures the expected log density ratio of two probability distributions, $D_{KL}(P\|Q)=\mathbb E_P[\log(p/q)]$. For a discrete distribution it is $\sum_i p_i\log(p_i/q_i)$, with infinite divergence when $P$ puts positive mass where $Q$ has none. Gibbs' inequality establishes nonnegativity, with equality for equal distributions almost everywhere. KL generally changes when its arguments are reversed and is not a metric. A natural logarithm expresses its value in nats. Minimizing data-to-model KL corresponds to maximum likelihood up to data entropy; the reverse direction does not generally have this equivalence.

## Why it matters here

The week tests Bernoulli sums, Gaussian posterior regularization and likelihood equivalence. Each Bernoulli outcome contributes to the sum, and equal forward and reverse KL for one special pair does not imply symmetry. Source-key discrepancies should be kept distinct from the derived result.

**Appears in:** [[week-8-report]] · [[week-8-exam-notes]] · [[week-08-questions]]

## Related

[[variational-autoencoder]] · [[generative-adversarial-network]] · [[triplet-loss]]
