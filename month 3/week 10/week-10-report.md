---
title: "Advanced Image Generation: Adversarial Games, Discrete Latents, Diffusion and Style"
week: 10
month: 3
status: provisional
date: 2026-11-14
prev: "[[week-9-report|Week 9]]"
next: "[[week-11-report|Week 11]]"
map: "[[Knowledge-Map]]"
tags:
  - dlcv/week-10
  - dlcv/generative-models
  - dlcv/style-transfer
concepts:
  - "[[progressive-growing]]"
  - "[[gan-mode-collapse]]"
  - "[[vector-quantization]]"
  - "[[diffusion-process]]"
  - "[[classifier-free-guidance]]"
  - "[[gram-matrix-style]]"
---

# Advanced Image Generation: Adversarial Games, Discrete Latents, Diffusion and Style

> **Week 10 Review Article — Month 3 / Week 10**  
> **Provisional:** topics inferred from past papers; replace when the official syllabus is available.

**Navigation:** [[week-9-report|Week 9]] · [[Knowledge-Map|Knowledge Map]] · [[week-11-report|Week 11]]  
**Associated concepts:** [[progressive-growing]] · [[gan-mode-collapse]] · [[vector-quantization]] · [[diffusion-process]] · [[classifier-free-guidance]] · [[gram-matrix-style]]

## Abstract

Image generation requires learning a distribution over images, not merely predicting a class label. Adversarial networks learn an implicit sampler through a two-player game, while vector-quantized autoencoders compress observations into discrete code indices and diffusion models learn to reverse a specified corruption process. Progressive growing and style-based generation introduce multiscale structure and control into adversarial synthesis, but neither eliminates the need to measure diversity. Gaussian diffusion admits an exact forward marginal and a tractable posterior conditioned on the clean observation; a learned model approximates the reverse transitions at sampling time. Classifier-free guidance interpolates or extrapolates conditional and unconditional model predictions, with a convention-dependent scale. Neural style transfer addresses a related but different problem: synthesizing an image matching the content of one image and feature correlations of another.

**Keywords:** GAN, mode collapse, VQ-VAE, codebook, DDPM, noise schedule, classifier-free guidance, Gram matrix, style transfer.

## 1. Introduction and provisional syllabus

A discriminative model maps a visual input to a label or other target; a generative model represents or samples from a distribution of images, possibly conditional on a label, prompt, or reference. In Week 8, the variational autoencoder and the basic GAN motivate latent variables and adversarial training. This week develops practical alternatives for high-resolution synthesis and exam problems involving discrete latents, diffusion schedules and image style. Week 9's attention architectures can supply components of a generator or a conditioning network but are not required by every generative model.

| Provisional topic | Core question | Study activity |
| :--- | :--- | :--- |
| Progressive and style-based GANs | How does resolution or style control enter synthesis? | Trace a fade-in and distinguish style from noise. |
| GAN diversity and failure modes | Why can plausible samples miss modes? | Compare individual and minibatch evidence. |
| Vector-quantized autoencoders | How is a continuous encoder output mapped to a discrete code? | Compute nearest-neighbor distances and gradients. |
| Forward diffusion and noise schedules | How does $q(x_t\mid x_0)$ arise? | Derive the product schedule and calculate a sample. |
| Reverse diffusion and guidance | How is noise removed and conditioning strengthened? | Derive the posterior mean and interpret guidance scales. |
| Neural style transfer | What does a Gram matrix measure? | Compute a channel Gram matrix and style loss. |

This sequence is an inferred study organization, not an official daily syllabus. The [[week-10-questions|question bank]] preserves the exam wording, marks, source answers and qualification of ambiguous numerical assumptions. A sum of schedule coefficients can exceed one because it is an arithmetic sum; it is not itself a probability or a diffusion marginal variance.

## 2. Theoretical foundations

### 2.1 Adversarial distributions and equilibrium

Let real images follow $p_{\rm data}$, let $z\sim p(z)$, and let $G_\theta(z)$ induce $p_\theta$. The original GAN game is

$$\min_G\max_D V(D,G)=\mathbb E_{x\sim p_{\rm data}}\log D(x)+\mathbb E_{z\sim p(z)}\log(1-D(G(z))).$$

For a fixed generator and densities with respect to a common measure, pointwise optimization gives $D^*(x)=p_{\rm data}(x)/(p_{\rm data}(x)+p_\theta(x))$ wherever the denominator is positive. Inserting it gives $-\log4+2\operatorname{JS}(p_{\rm data}\Vert p_\theta)$. The global distributional optimum is $p_\theta=p_{\rm data}$ and $D^*=1/2$ on their common support. This ideal result assumes sufficient model capacity and optimization; it is not a guarantee for alternating finite-step training. A discriminator loss near a particular scalar is therefore not a certificate that the generator has captured all modes.

The original minimax generator minimizes $\mathbb E\log(1-D(G(z)))$. When a competent discriminator gives generated examples scores near zero, its gradient may be weak. The common non-saturating alternative maximizes $\mathbb E\log D(G(z))$, yielding a stronger early gradient in many settings, but changes the generator objective and does not remove game dynamics. Training alternates updates on real and generated minibatches; gradients must flow through the discriminator to the generator, while discriminator parameters are held fixed during a generator update.

### 2.2 Progressive growing and style-based synthesis

Progressive GAN begins with low-resolution generator and discriminator networks. Higher-resolution blocks are added progressively on both sides, and a fade-in interpolates the old upsampled output and the new block's output, for example $x=(1-\lambda)x_{\rm old}+\lambda x_{\rm new}$ with $\lambda$ increasing from zero to one. The discriminator uses a corresponding transition in reverse. At coarse scales the network models large spatial structures; later stages refine details. This schedule can reduce instability and computational cost early in training, but does not mathematically guarantee stable optimization, all modes, or unlimited image variation.

StyleGAN separates a mapping network, which transforms a sampled latent $z$ into an intermediate latent $w$, from a synthesis network. Styles derived from $w$ modulate synthesis at multiple resolutions, and injected stochastic noise can affect local variation. Early and late layers often influence relatively coarse and fine attributes respectively, but this is a tendency rather than perfect semantic disentanglement. Style mixing, in which different intermediate latents control different layer ranges, probes this organization. StyleGAN's learned styles are distinct from Gram matrices in classical neural style transfer: the former modulate a learned generator; the latter specify feature correlations against a reference image.

### 2.3 Mode collapse and minibatch evidence

Mode collapse means that many latent inputs produce samples from only a small subset of the data distribution. Each sample can look realistic while the generator neglects other plausible identities or structures. The discriminator's per-image objective may fail to detect a lack of variation in a small set if each member looks plausible in isolation. ProGAN appends a minibatch standard-deviation feature to the discriminator, making some batch-level variation available to its decision. It computes variation across examples at feature locations, averages to a summary and broadcasts that summary as a feature map. This can discourage a generator whose minibatch variation differs systematically from real minibatches, but a single statistic cannot identify all discrepancies between distributions and finite batches make the estimate noisy.

**The dangerous misconception:** a large batch standard deviation proves that every mode is represented. **Why this is false:** distinct distributions can share the same mean and variance. Diversity, fidelity, memorization, and coverage should be assessed separately, using samples and suitable quantitative diagnostics. Even a low Fréchet inception distance depends on the feature extractor and sample size and does not establish semantic coverage in every application. Privacy or authenticity claims also require separate evaluation.

### 2.4 Vector quantization and VQ-VAE

An encoder maps $x$ to continuous vectors $z_e(x)$; at each spatial position, a codebook $E=\{e_1,\ldots,e_K\}$ supplies the nearest vector:

$$k^*=\arg\min_{k\in\{1,\ldots,K\}}\|z_e(x)-e_k\|_2^2,\qquad z_q(x)=e_{k^*}.$$

The discrete index $k^*$ selects a learned vector; the decoder reconstructs from the grid of selected vectors. A standard VQ-VAE objective is

$$\mathcal L=-\log p_\theta(x\mid z_q)+\|\operatorname{sg}[z_e]-e\|_2^2+\beta\|z_e-\operatorname{sg}[e]\|_2^2.$$

Here $\operatorname{sg}$ is stop-gradient, $e=e_{k^*}$, and $\beta$ is a commitment weight. The codebook loss moves selected embeddings toward encoder outputs; the commitment term encourages encoder outputs to remain near their selected embeddings. The reconstruction gradient uses a straight-through estimator: during the backward pass the quantizer is treated as an identity for the encoder. This is a biased surrogate gradient, not the exact derivative of the discontinuous nearest-neighbor map. An alternative updates the codebook with exponential moving averages. A separately trained prior over code indices permits unconditional sampling; a reconstruction model alone does not specify an adequate prior over valid grids.

Codebook collapse occurs when only a small subset of entries is used, reducing effective capacity. Usage counts or perplexity reveal underuse, although high perplexity alone does not prove useful representations. Larger $K$ increases the number of possible indices but can make training less efficient and does not guarantee better reconstruction. For a grid with $H\times W$ positions and $K$ symbols, a fixed-length representation uses $HW\lceil\log_2 K\rceil$ bits for the indices, ignoring model and entropy-coding overhead. The representation is discrete even though selected embedding vectors are real-valued.

### 2.5 Forward Gaussian diffusion

The DDPM forward Markov chain uses $0<\beta_t<1$, $\alpha_t=1-\beta_t$, and $\bar\alpha_t=\prod_{s=1}^{t}\alpha_s$:

$$q(x_t\mid x_{t-1})=\mathcal N(\sqrt{\alpha_t}x_{t-1},\beta_t I).$$

Writing $x_t=\sqrt{\alpha_t}x_{t-1}+\sqrt{\beta_t}\epsilon_t$ with independent standard normal noise and substituting recursively, the coefficient of $x_0$ becomes $\sqrt{\bar\alpha_t}$. The independent noise terms combine as a Gaussian whose variance telescopes to $1-\bar\alpha_t$. Hence

$$q(x_t\mid x_0)=\mathcal N(\sqrt{\bar\alpha_t}x_0,(1-\bar\alpha_t)I),\quad x_t=\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\epsilon,\quad\epsilon\sim\mathcal N(0,I).$$

The expression allows direct sampling at an arbitrary timestep during training. The coefficient $\bar\alpha_t$ controls retained signal power, while $1-\bar\alpha_t$ is the marginal noise variance conditional on $x_0$. Each $\beta_t$ is the innovation variance conditional on $x_{t-1}$, not the marginal variance conditional on $x_0$. For a linear schedule with $T$ endpoints $a,b$, $\sum_t\beta_t=T(a+b)/2$; this exam arithmetic is distinct from $1-\prod_t(1-\beta_t)$ because earlier noise is attenuated by later transitions. The approximation $1-\prod_t(1-\beta_t)\approx\sum_t\beta_t$ only applies when the total is sufficiently small.

### 2.6 Reverse posterior and denoising

The exact forward posterior conditioned on both $x_t$ and $x_0$ follows by multiplying Gaussian densities:

$$q(x_{t-1}\mid x_t,x_0)=\mathcal N(\tilde\mu_t(x_t,x_0),\tilde\beta_t I),$$
$$\tilde\beta_t=\frac{1-\bar\alpha_{t-1}}{1-\bar\alpha_t}\beta_t,\qquad
\tilde\mu_t=\frac{\sqrt{\bar\alpha_{t-1}}\beta_t}{1-\bar\alpha_t}x_0+\frac{\sqrt{\alpha_t}(1-\bar\alpha_{t-1})}{1-\bar\alpha_t}x_t.$$

To derive these expressions, collect the quadratic terms in $x_{t-1}$ from $q(x_t\mid x_{t-1})q(x_{t-1}\mid x_0)$ and complete the square. At generation time $x_0$ is unknown. A neural network $\epsilon_\theta(x_t,t)$ estimates the added noise and yields $\hat x_0=(x_t-\sqrt{1-\bar\alpha_t}\epsilon_\theta)/\sqrt{\bar\alpha_t}$. Substitution gives the usual noise-prediction mean

$$\mu_\theta(x_t,t)=\frac{1}{\sqrt{\alpha_t}}\left(x_t-\frac{\beta_t}{\sqrt{1-\bar\alpha_t}}\epsilon_\theta(x_t,t)\right).$$

A reverse step samples $x_{t-1}=\mu_\theta+\sigma_t z$ for an appropriate variance schedule, with special treatment of the final step. The simplified training objective samples $t$, $x_0$, and $\epsilon$, then minimizes $\|\epsilon-\epsilon_\theta(x_t,t)\|^2$. The exact variational bound has timestep-dependent terms and weights; the common unweighted objective is a practical simplification, not an identity for every parameterization. Reverse denoising generates a sample from the learned distribution and does not generally recover a particular original image from pure noise.

### 2.7 Classifier-free guidance

A conditional model can be trained with conditioning information randomly dropped, so the same network predicts $\epsilon_c=\epsilon_\theta(x_t,t,c)$ and $\epsilon_u=\epsilon_\theta(x_t,t,\varnothing)$. One convention combines them as

$$\epsilon_\gamma=\epsilon_u+\gamma(\epsilon_c-\epsilon_u).$$

Here $\gamma=0$ gives the unconditional prediction, $\gamma=1$ gives the ordinary conditional prediction, and $\gamma>1$ extrapolates toward stronger conditioning. Another common convention writes $(1+w)\epsilon_c-w\epsilon_u$, with $w=0$ already conditional; the two scales satisfy $\gamma=1+w$. Always state the equation before interpreting a zero scale. Stronger guidance often improves condition adherence at the expense of diversity or realism; the direction and magnitude depend on model, dataset, scale and sampler. Classifier-free guidance uses no separate classifier at sampling, unlike classifier guidance, which uses a classifier gradient.

### 2.8 Gram matrices and perceptual style

A fixed feature extractor produces activations $F^l(x)\in\mathbb R^{C_l\times M_l}$ at layer $l$, with channels as rows and $M_l$ spatial positions as columns. The unnormalized Gram matrix is

$$G^l(x)=F^l(x)F^l(x)^T,\qquad G^l_{ij}(x)=\sum_{p=1}^{M_l}F^l_{ip}(x)F^l_{jp}(x).$$

These are uncentered channel inner products, not necessarily centered covariances or normalized correlations. Aggregation discards explicit spatial arrangement, so the same Gram matrix can arise from features with different arrangements. A style objective compares the generated image $x$ with a style reference $s$, for example $\mathcal L_{\rm style}=\sum_l w_l\|G^l(x)-G^l(s)\|_F^2$ with explicitly stated normalization. A content objective compares feature activations of $x$ and content reference $c$, $\mathcal L_{\rm content}=\|F^k(x)-F^k(c)\|_F^2$. The total can add total variation regularization and weights $\lambda_c,\lambda_s$. Normalization differs between formulations; a numerical question must specify it before a unique loss is computed.

## 3. Algorithms and practical verification

### 3.1 Training and sampling recipes

**Progressive GAN:** begin with low-resolution images; alternate discriminator and generator updates; introduce corresponding higher-resolution blocks with a smooth blend; stabilize at each resolution. Track held-out fidelity and diversity, not merely the losses. **VQ-VAE:** encode an input; find the closest code at every position; reconstruct using selected embeddings; apply reconstruction, codebook and commitment terms; update the encoder using straight-through gradients; fit a prior to the resulting indices for generation. **Diffusion:** draw an image, timestep and standard normal noise; form $x_t$ in one step using $\bar\alpha_t$; train the noise predictor; generate by starting at a Gaussian and applying learned reverse steps. Conditional sampling may combine two predictions with a stated guidance convention. **Style transfer:** extract target content features and style Gram matrices once, initialize a generated image, repeatedly compute its features and weighted losses, and update the image while holding the extractor fixed.

### 3.2 Concept → Code → Output → Interpretation

**Concept:** schedule sums and marginal DDPM noise variance differ. The following pure Python example also checks the forward-sample arithmetic used in the question bank.

```python
import math

betas = [0.03 + (0.02 - 0.03) * t / 149 for t in range(150)]
bar_alpha = math.prod(1 - beta for beta in betas)
x_t = math.sqrt(0.81) * 2 + math.sqrt(0.19) * -1
print(f"schedule sum: {sum(betas):.6f}")
print(f"marginal variance: {1 - bar_alpha:.6f}")
print(f"forward sample: {x_t:.6f}")
```

```text
schedule sum: 3.750000
marginal variance: 0.977592
forward sample: 1.364110
```

**Interpretation:** the arithmetic sum is 3.75, whereas each earlier innovation is attenuated by subsequent transitions and the resulting marginal variance is below one. The sample calculation uses a standard deviation of $\sqrt{0.19}$ rather than the variance 0.19. Values follow from this illustrative schedule; they are not claims about model quality.

## 4. Numerical analysis and comparison

| Model or method | Learned object | Sampling mechanism | Main limitation |
| :--- | :--- | :--- | :--- |
| GAN / ProGAN | Implicit generator and discriminator | One generator evaluation | Mode collapse and adversarial instability |
| StyleGAN | Modulated synthesis and mapping networks | Latent mapping plus generator | Controls are not perfectly disentangled |
| VQ-VAE plus prior | Encoder, codebook, decoder and index prior | Draw indices, decode selected vectors | Underused codes and prior cost |
| DDPM | Reverse denoising model | Iterative Gaussian transitions | Multiple network evaluations |
| Neural style transfer | Often optimizes image with fixed features | Optimize pixels for one pair | Gram matching omits spatial layout |

This comparison describes canonical forms, not all later variants. GANs can be conditioned and diffusion models can use accelerated samplers; VQ models can also serve as tokenizers for other generative systems. Computational cost depends on architecture, resolution, hardware, and sampler, so a generic table cannot establish actual latency.

When a question gives a constant hypothetical reverse-variance decrement $d$, solve $n=(v_0-v_{\rm target})/d$; if only whole steps are allowed and the question asks to reach *at most* the target, take the ceiling. Exact equality can be impossible. In particular, 0.90 decreased by 0.02 per step yields 0.06 at 42 and 0.04 at 43; 0.05 lies between them. The key of 43 in one source is consistent with a threshold interpretation, but not literal equality. This toy arithmetic should not be mistaken for the DDPM reverse variance formula.

## 5. Applications and scientific formulations

**Image synthesis and augmentation:** sample $G(z)$ or reverse a diffusion chain conditioned on a class. A failure is narrow coverage that reinforces dataset imbalances; augmented samples must be evaluated on real held-out data. **Compression and representation learning:** map an image to a code grid and reconstruct it through a VQ decoder. Distortion and bit rate must be measured together, including prior and coding overhead; unused codes waste representational capacity. **Conditional generation:** use a prompt or label as $c$ and examine the effect of $\gamma$ on both adherence and diversity. Large guidance can amplify artifacts or biases; condition satisfaction should not be assumed from scale alone. **Artistic rendering:** optimize an output against content features and style Gram statistics. Large style weights can destroy semantic layout, and style statistics need not preserve source geometry or confer rights to reuse source material.

## 6. Critical challenges and misconceptions

1. **Sampling versus reconstruction:** decoding a known code grid reconstructs an input, while generation requires a prior over grids. A quantizer does not automatically supply that prior.
2. **Variance versus standard deviation:** in $x_t$, use square roots of the variance coefficients. A direct sum of $\beta_t$ is not the variance of the final state.
3. **Forward versus reverse:** forward noise is a specified transition; reverse denoising is learned. Neither a constant decrement nor exact inversion is implied by DDPM.
4. **Guidance convention:** zero means unconditional only for $\epsilon_u+\gamma(\epsilon_c-\epsilon_u)$; under the alternative $w$ parameterization zero means conditional.
5. **Feature correlation versus geometry:** a Gram matrix matches aggregated channel products and discards spatial arrangement. It does not reconstruct the style image or guarantee local correspondence.
6. **Quality versus coverage:** a plausible image, low training loss, or one diversity statistic cannot establish that a generative model captures the full data distribution.
7. **Straight-through gradients:** the backward identity is an estimator chosen to train a discontinuous operation, not its true derivative.

## 7. Conclusion and handoff

1. Progressive growing organizes adversarial learning from coarse to fine; minibatch features make some diversity evidence visible to the discriminator.
2. VQ-VAE quantizes encoder vectors to learned codebook entries, trains through a surrogate gradient, and needs a prior for sampling.
3. DDPM's accumulated signal is a product of $\alpha_t$; its conditional noise variance is one minus that product, not the sum of $\beta_t$.
4. Reverse transitions use learned noise estimates; classifier-free guidance combines conditional and unconditional predictions with a convention that must be stated.
5. Style transfer matches a generated image's feature Gram matrices to a style reference and feature activations to a content reference.

The next provisional week moves toward representation learning and vision-language alignment, where unlabeled data and paired image-text supervision can supply useful representations without an explicit pixel generator.

## 8. Academic references and annotated literature

- Goodfellow et al. (2014), “Generative Adversarial Nets,” *NeurIPS*. [arXiv:1406.2661](https://arxiv.org/abs/1406.2661). Contribution: adversarial distribution matching and the original minimax objective.
- Karras et al. (2018), “Progressive Growing of GANs for Improved Quality, Stability, and Variation,” *ICLR*. [arXiv:1710.10196](https://arxiv.org/abs/1710.10196). Contribution: progressive resolution and minibatch standard deviation.
- Karras, Laine and Aila (2019), “A Style-Based Generator Architecture for Generative Adversarial Networks,” *CVPR*. [DOI:10.1109/CVPR.2019.00453](https://doi.org/10.1109/CVPR.2019.00453). Contribution: style-based generator and stochastic variation.
- van den Oord, Vinyals and Kavukcuoglu (2017), “Neural Discrete Representation Learning,” *NeurIPS*. [arXiv:1711.00937](https://arxiv.org/abs/1711.00937). Contribution: vector-quantized autoencoder and learned prior.
- Ho, Jain and Abbeel (2020), “Denoising Diffusion Probabilistic Models,” *NeurIPS*. [arXiv:2006.11239](https://arxiv.org/abs/2006.11239). Contribution: Gaussian diffusion and denoising training.
- Ho and Salimans (2022), “Classifier-Free Diffusion Guidance,” *NeurIPS Workshop on Deep Generative Models and Downstream Applications*. [arXiv:2207.12598](https://arxiv.org/abs/2207.12598). Contribution: combining conditional and unconditional score estimates.
- Gatys, Ecker and Bethge (2016), “Image Style Transfer Using Convolutional Neural Networks,” *CVPR*. [DOI:10.1109/CVPR.2016.265](https://doi.org/10.1109/CVPR.2016.265). Contribution: content feature and style Gram losses.

## Appendix A — Computational reproducibility

Run the complete Python block in Section 3.2 using `uv run python` from the repository root. The standard library suffices; no random sampling is used. The question-bank schedule and single-step calculations use the same equations, while the threshold ambiguity is recorded in [[DISCREPANCIES]].

## Appendix B — Knowledge graph connections

**Upstream:** [[week-8-report]], [[week-9-report]]. **Downstream:** [[week-11-report]]. **Siblings:** [[week-10-exam-notes]], [[week-10-questions]], [[Knowledge-Map]].
