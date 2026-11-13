---
title: "Diffusion process"
status: provisional
---

# Diffusion process

A denoising diffusion model specifies a forward Markov chain that gradually corrupts a data sample with Gaussian noise and learns reverse transitions for generation. With $lpha_t=1-eta_t$ and $arlpha_t=\prod_{s=1}^tlpha_s$, the forward marginal is $q(x_t\mid x_0)=\mathcal N(\sqrt{arlpha_t}x_0,(1-arlpha_t)I)$. This closed form allows training at an arbitrary timestep without simulating every preceding transition. A neural network commonly predicts the sampled noise and thereby parameterizes a reverse mean. The sum of schedule entries $\sum_teta_t$ is generally not the final marginal noise variance because subsequent transitions attenuate earlier innovations. **Why it matters here:** exam questions test schedule arithmetic, reverse-step assumptions and the square-root coefficients of a forward sample.

**Appears in:** [[week-10-report]] · [[week-10-exam-notes]] · [[week-10-questions]]

## Related

[[classifier-free-guidance]]
