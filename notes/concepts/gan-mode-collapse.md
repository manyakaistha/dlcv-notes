---
title: "GAN mode collapse"
status: provisional
---

# GAN mode collapse

Mode collapse is a failure of a generative adversarial network in which many latent inputs produce samples concentrated on a limited subset of the data distribution. Individual samples may appear realistic even while the generator omits important modes. A discriminator operating on individual images can miss batch-level lack of variety. Minibatch standard-deviation features provide one summary of variation to the discriminator and can discourage some collapsed solutions, but matching one statistic is not sufficient to match distributions. Diversity depends on the evaluation set and feature representation; fidelity, coverage and memorization require separate assessment. **Why it matters here:** the progressive GAN questions ask why batch-level variation can help detect generated samples with insufficient diversity.

**Appears in:** [[week-10-report]] · [[week-10-exam-notes]] · [[week-10-questions]]

## Related

[[progressive-growing]]
