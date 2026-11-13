---
title: "Week 10 exam notes: generative models and style"
week: 10
month: 3
status: provisional
report: "[[week-10-report]]"
map: "[[Knowledge-Map]]"
tags:
  - dlcv/week-10
  - dlcv/exam-preparation
---

# Week 10 exam notes

> **Provisional:** topics inferred from past papers; replace when the official syllabus is available.

**Navigation:** [[week-10-report|Week 10 report]] · [[week-10-questions|Question bank]] · [[Knowledge-Map|Knowledge Map]]

## One-line recall

- **GAN:** the generator transforms random latents into samples; the discriminator distinguishes real samples from generated samples during training.
- **Equilibrium:** in the ideal original GAN game, matching data and generator distributions yields an optimal discriminator of one half on their common support.
- **Progressive growing:** add higher-resolution generator and discriminator blocks over training, generally learning coarse structure before fine detail.
- **Fade-in:** interpolate the old low-resolution path and new high-resolution path to avoid an abrupt architectural transition.
- **Minibatch standard deviation:** supplies a discriminator with an aggregate batch variation feature, helping it notice some forms of low diversity.
- **Mode collapse:** realistic-looking samples can cover only a small fraction of the data distribution.
- **StyleGAN:** a mapping network creates intermediate latents that modulate synthesis at different scales; stochastic noise controls additional local variation.
- **VQ-VAE:** encoder outputs are replaced by nearest learned code vectors; a decoder reconstructs from those vectors.
- **Straight-through:** copy the decoder-side gradient to the encoder as a surrogate through the discontinuous quantizer.
- **Codebook loss:** pulls selected code vectors toward encoder outputs; the commitment term encourages the encoder to stay near selected codes.
- **Prior:** a trained probability model over index grids is needed to generate new VQ-VAE examples.
- **Forward diffusion:** a fixed Markov chain adds Gaussian noise according to a variance schedule.
- **Reverse diffusion:** a learned denoiser approximates the transitions needed to sample from noise toward the data distribution.
- **Classifier-free guidance:** combine conditional and unconditional predictions; stronger conditioning may trade diversity for alignment.
- **Gram matrix:** channel-by-channel uncentered products summed over spatial positions represent feature statistics useful for style.
- **Content loss:** compares feature activations of generated and content images; style loss compares generated and style Gram matrices.

## Formula sheet

For the original GAN,

$$\min_G\max_D\; \mathbb E_{x\sim p_{data}}\log D(x)+\mathbb E_z\log(1-D(G(z))).$$

The fixed-generator optimum is $D^*(x)=p_{data}(x)/(p_{data}(x)+p_g(x))$ where defined. At matched distributions the discriminator is $1/2$. The non-saturating generator objective maximizes $\log D(G(z))$ rather than minimizing the potentially saturating $\log(1-D(G(z)))$. These expressions describe objectives; practical optimization is not guaranteed to reach the ideal equilibrium.

For a codebook $\{e_k\}_{k=1}^K$ and encoder vector $z_e$,

$$k^*=\arg\min_k\|z_e-e_k\|_2^2,\qquad z_q=e_{k^*}.$$

One conventional objective is reconstruction plus $\|\operatorname{sg}[z_e]-e_{k^*}\|^2+\beta\|z_e-\operatorname{sg}[e_{k^*}]\|^2$. Stop-gradient means the argument is held constant for differentiation. For a spatial index grid of size $H\times W$, a fixed-length representation has $HW\lceil\log_2K\rceil$ index bits, excluding model and other overhead. Ties in nearest-neighbor selection require a specified tie rule; training may alternatively use exponential moving averages for the embeddings.

For diffusion set $\alpha_t=1-\beta_t$, $\bar\alpha_t=\prod_{s=1}^t\alpha_s$, and $\bar\alpha_0=1$. Then

$$q(x_t\mid x_{t-1})=\mathcal N(\sqrt{\alpha_t}x_{t-1},\beta_t I),\qquad x_t=\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\epsilon.$$

The forward conditional marginal is Gaussian with mean $\sqrt{\bar\alpha_t}x_0$ and variance $(1-\bar\alpha_t)I$. Its noise variance is not generally $\sum_t\beta_t$. The exact posterior conditional on $x_0$ has variance $\tilde\beta_t=\beta_t(1-\bar\alpha_{t-1})/(1-\bar\alpha_t)$. A common reverse mean based on predicted noise is

$$\mu_\theta=\frac{1}{\sqrt{\alpha_t}}\left(x_t-\frac{\beta_t}{\sqrt{1-\bar\alpha_t}}\epsilon_\theta(x_t,t)\right).$$

The network is often trained with $\|\epsilon-\epsilon_\theta(x_t,t)\|_2^2$, with $t$ and noise sampled during training. The reverse sampler's variance and final-step treatment are implementation choices, and the simplified loss does not reproduce every weighted term of the variational bound.

For classifier-free guidance under the convention used here,

$$\epsilon_\gamma=\epsilon_u+\gamma(\epsilon_c-\epsilon_u).$$

At $\gamma=0$ this is unconditional; at $\gamma=1$ it is conditional; larger values extrapolate. A different convention $(1+w)\epsilon_c-w\epsilon_u$ has $w=0$ at the ordinary conditional prediction, with $\gamma=1+w$. Read the definition rather than assuming all guidance scales have the same zero point.

For features $F\in\mathbb R^{C\times M}$, $G=FF^T$ is `C × C`, with $G_{ij}=\sum_pF_{ip}F_{jp}$. A style loss compares $G$ for generated and style images, often over several layers; a content loss compares their activations to those of the content image. State normalization when computing numeric losses, because definitions differ.

## Worked numerical recipes

### 1. Forward sample

Given $\bar\alpha_t=0.81$, $x_0=2$, and $\epsilon=-1$, compute $\sqrt{0.81}(2)+\sqrt{0.19}(-1)=1.364110\ldots$. To three decimals the sample is **1.364**. The square roots are essential: the coefficients inside the roots are variances, not standard deviations. This agrees with the accepted range in Q38 of the 2026T2 end-term paper.

### 2. Linear schedule

For 150 linearly spaced values starting at 0.03 and ending at 0.02, the average is $(0.03+0.02)/2=0.025$ and the sum is **3.75**. This is the sum requested in the exam, not the final DDPM marginal variance. Multiplying the factors $1-\beta_t$ gives the actual conditional marginal variance $1-\bar\alpha_T\approx0.977592$ for this particular schedule. Neither quantity should be substituted for the other merely because both involve noise.

### 3. Reverse-step toy problem

If a hypothetical variance falls by 0.02 from 1.0 each step, reaching 0.1 requires $(1.0-0.1)/0.02=45$ steps. For a starting variance of 0.90 and a target of 0.05, the real-valued solution is 42.5 steps. Forty-two whole steps yield 0.06 and 43 yield 0.04. The source key gives 43; this is valid for crossing to at most 0.05, while exact equality is impossible under the stipulated fixed decrement. Do not generalize this toy linear decrement to the DDPM posterior.

### 4. Nearest code and rate

Let $z_e=(1,2)$ and code vectors be $e_1=(0,0)$, $e_2=(1,1)$ and $e_3=(3,2)$. The squared distances are 5, 1 and 4, so the quantizer selects $e_2$. If a grid has $4\times4$ positions and a codebook has eight entries, each index requires three fixed-length bits and the grid requires $16\times3=48$ bits before overhead. This does not measure the full compressed file size or the distortion.

### 5. Gram matrix

For $F=\begin{bmatrix}1&2\\3&4\end{bmatrix}$, the channel Gram matrix is $FF^T=\begin{bmatrix}5&11\\11&25\end{bmatrix}$. The diagonal terms are sums of squared activations and the off-diagonal term is the cross-channel dot product. Permuting both spatial columns leaves the Gram matrix unchanged, illustrating why it loses explicit spatial location. Dividing by $M$ would yield a normalized Gram matrix; never mix definitions across the generated and style images.

### 6. Guidance interpolation

Suppose scalar noise predictions are $\epsilon_u=0.4$ and $\epsilon_c=0.1$. For $\gamma=2$, the guided prediction is $0.4+2(0.1-0.4)=-0.2$. This is extrapolation rather than a convex average, so it can lie outside the range of the two predictions. At zero it is 0.4; at one it is 0.1. These numbers illustrate the formula and do not establish a universal best scale.

The following self-contained standard-library code verifies all numbers above. Run from the project root with `uv run python` and compare the output.

```python
import math

betas = [0.03 + (0.02 - 0.03) * t / 149 for t in range(150)]
print(f"forward: {2 * math.sqrt(0.81) - math.sqrt(0.19):.6f}")
print(f"schedule: {sum(betas):.6f}, marginal: {1 - math.prod(1-b for b in betas):.6f}")
print(f"steps: {(1.0-0.1)/0.02:.1f}, crossing: {(0.9-0.05)/0.02:.1f}")
z = (1, 2)
codes = [(0, 0), (1, 1), (3, 2)]
print("distances:", [sum((a-b)**2 for a, b in zip(z, e)) for e in codes])
print("bits:", 4 * 4 * math.ceil(math.log2(8)))
f = [[1, 2], [3, 4]]
print("Gram:", [[sum(a*b for a, b in zip(row, col)) for col in f] for row in f])
print(f"guidance: {0.4 + 2 * (0.1 - 0.4):.1f}")
```

```text
forward: 1.364110
schedule: 3.750000, marginal: 0.977592
steps: 45.0, crossing: 42.5
distances: [5, 1, 4]
bits: 48
Gram: [[5, 11], [11, 25]]
guidance: -0.2
```

## Exam traps and checks

1. Do not equate the schedule sum with accumulated marginal variance. Compute the product of $\alpha$ values.
2. Do not confuse a variance with its square root in the forward sample. Check coefficients and signs before rounding.
3. A reverse process does not guarantee the original input is recovered from an independent noise sample. It samples a learned distribution.
4. A fixed decrement problem needs a precise stopping rule. If exact equality is impossible, explain whether the accepted integer is a threshold crossing.
5. A guidance scale of zero is meaningful only after the formula and convention are given. Classifier-free guidance does not require a separate classifier.
6. Higher guidance does not guarantee better every-sample quality or zero mode collapse. Fidelity and diversity are different axes of evaluation.
7. A codebook is a finite set of learned vectors, not a decoder, classifier, or probability prior. The index is discrete while the vector components are continuous.
8. Straight-through differentiation is an approximation. Stop-gradient determines which loss term updates the encoder or the embeddings.
9. Minibatch statistics reveal only some diversity differences; matching a single statistic does not prove matching distributions.
10. Gram matrices compare generated-image and style-image feature statistics. The content image supplies a separate feature target, even if an exam option describes this imprecisely.
11. Progressive growing increases resolution gradually. It does not freeze every network layer or guarantee unlimited variation.
12. For any multiple-select question assess each statement independently. A plausible tendency such as lower diversity with high guidance is not an unconditional theorem.

## Last-minute retrieval

From memory, write $\bar\alpha_t$ as a product and derive the direct forward sample; explain why the variance contains one minus that product. Sketch the quantize–decode path and identify the gradient each VQ-VAE loss term supplies. State the two guidance conventions and identify their zero points. Compute a two-channel Gram matrix and explain why its spatial invariance helps represent texture but loses layout. Finally distinguish progressive resolution, StyleGAN modulation, minibatch diversity, and ordinary neural style transfer: these are related tools with different objectives.
