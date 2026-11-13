---
title: "Generative Models, Variational Inference and Metric Learning"
week: 8
month: 2
status: provisional
date: 2026-11-14
prev: "[[week-7-report|Week 7]]"
next: "[[week-9-report|Week 9]]"
map: "[[Knowledge-Map]]"
tags:
  - dlcv/week-08
  - dlcv/generative-models
  - dlcv/metric-learning
concepts:
  - "[[variational-autoencoder]]"
  - "[[kullback-leibler-divergence]]"
  - "[[generative-adversarial-network]]"
  - "[[triplet-loss]]"
---

# Generative Models, Variational Inference and Metric Learning

> **Week 8 Review Article — Month 2 / Week 8**  
> topics inferred from past papers; replace when the official syllabus is available

**Navigation:** ← [[week-7-report|Week 7]] · [[Knowledge-Map|Knowledge Map]] · [[week-9-report|Week 9]] →  
**Associated Concepts:** [[variational-autoencoder]] · [[kullback-leibler-divergence]] · [[generative-adversarial-network]] · [[triplet-loss]]

## Abstract

Generative modeling describes the distribution of observations rather than only a decision boundary. This review develops likelihood, Bayes' rule, relative entropy, autoencoders, variational autoencoders and adversarial games, and contrasts these with metric learning for face recognition. The evidence lower bound makes approximate latent-variable learning tractable, while pathwise reparameterization connects stochastic sampling to gradient optimization. An ideal adversarial equilibrium yields an indistinguishable generated distribution, but neither finite training nor a single image-quality statistic guarantees that result. Numerical examples distinguish a source key from a mathematically derived result and expose the assumptions behind principal-component equivalence, discriminator equilibrium and triplet loss. Evaluation must separately consider fidelity, diversity, task relevance and the assumptions embedded in the measurement.

## Keywords

Likelihood, Bayes, KL divergence, autoencoder, ELBO, Gaussian latent variable, GAN, Siamese network, triplet loss, FID, mutual information gap.

## 1. Introduction and provisional syllabus

Week 7 sequence models condition outputs on a representation and past context; this week considers how a representation can describe an entire data distribution and how its geometry supports comparisons. The inferred clusters are generative models and KL divergence; autoencoder representations; variational autoencoders; GAN objectives and equilibrium; metric learning and face verification; and generative model evaluation. These are a working organization of past-paper questions, not a claim about the missing official syllabus. The associated [[week-08-questions|question bank]] contains the extracted questions and source-key caveats.

A classifier can estimate $p(y\mid x)$ without supplying a way to draw plausible observations $x$. A generative classifier instead models $p(x\mid y)$ and $p(y)$; the joint factorizes as $p(x,y)=p(x\mid y)p(y)$. A conditional generator can sample $x$ given $y$, while an unconditional generator targets the marginal data distribution. These definitions describe distributions, not a particular network architecture: a neural network may implement either kind of model depending on its objective and outputs. An estimated likelihood is also not automatically a reliable out-of-distribution detector, since likelihood can reflect low-level statistics rather than semantic typicality.

## 2. Probability, likelihood and information

**Mathematical formulation:** Bayes' rule gives

$$p(y\mid x)=\frac{p(x\mid y)p(y)}{\sum_{y'}p(x\mid y')p(y')},$$

where the denominator normalizes over mutually exclusive exhaustive classes. For a dog/cat example, class-conditional values $0.02$ and $0.06$ with priors $0.4$ and $0.6$ give $p(\mathrm{cat}\mid x)=0.036/0.044\approx0.81818$. The likelihoods must be evaluated at the same observation; a density may exceed one, even though a posterior probability cannot.

For independent observations $x_1,\ldots,x_n$, maximum likelihood chooses $\theta$ to maximize $\sum_i\log p_\theta(x_i)$, or equivalently minimize mean negative log likelihood. The product formulation assumes independent samples; dependence requires a joint model or appropriate conditional factorization. An autoregressive model writes $p(x)=\prod_i p(x_i\mid x_{<i})$ and can evaluate this factorization where its conditionals are tractable. A diffusion model instead defines a noise-adding process and learns a reverse process; changing sampling steps can change cost and sample quality. Neither construction should be confused with an ordinary GAN's implicit density.

The KL divergence is

$$D_{KL}(P\|Q)=\mathbb E_{x\sim P}\left[\log\frac{p(x)}{q(x)}\right].$$

For discrete outcomes this is $\sum_i p_i\log(p_i/q_i)$, with zero-probability conventions and infinite divergence if $P$ assigns mass where $Q$ assigns none. Gibbs' inequality proves nonnegativity; equality holds when the distributions coincide almost everywhere. KL is generally asymmetric and need not satisfy the triangle inequality. It is therefore not a metric. For Bernoulli distributions with probabilities $0.9$ and $0.1$, both outcomes matter: $D_{KL}(P\|Q)=0.9\log9+0.1\log(1/9)=0.8\log9$. This complementary pair happens to have equal forward and reverse values, which does not establish symmetry in general.

Maximum likelihood corresponds, up to an additive data entropy, to minimizing $D_{KL}(p_{data}\|p_\theta)$, not generally $D_{KL}(p_\theta\|p_{data})$. The direction controls which distribution weights the log ratio and can change the fitted model. Similarly, mean squared error represents a Gaussian negative log likelihood only after assumptions about observation variance and constants are specified. Claims of equivalence without the direction and likelihood are incomplete. The Week 8 bank records an exam question that reverses this direction, preserving the official key while explaining the issue.

## 3. Autoencoder representations

An autoencoder composes an encoder $z=f_\phi(x)$ with a decoder $\hat x=g_\theta(z)$ and minimizes a reconstruction loss, for example $\|x-\hat x\|_2^2$. The bottleneck can force a lower-dimensional representation, but the input and output typically share the same dimensions; compression concerns the intermediate code and also the cost of representing model parameters. A high-capacity network with no additional constraint may simply learn an identity map. Reconstruction quality alone does not imply that interpolation, random sampling or downstream recognition will be useful.

For centered observations and squared reconstruction error, a globally optimized linear autoencoder with a rank-$k$ bottleneck recovers a principal $k$-dimensional reconstruction subspace under the standard assumptions. Its factors are not uniquely identified: invertible changes of coordinates in the latent space can leave the reconstruction unchanged. With tied or orthonormal constraints the relation to principal axes is more direct. Nonlinear networks, different losses, insufficient optimization, or an unconstrained architecture invalidate a blanket claim that every linear autoencoder is PCA. PCA itself minimizes squared projection error onto a $k$-dimensional linear subspace, with possible nonuniqueness at tied eigenvalues.

A denoising autoencoder corrupts a clean sample $x$ to obtain $\tilde x\sim c(\tilde x\mid x)$, encodes the corrupted sample, and compares the reconstruction against the clean target. Its objective is $\mathbb E_{x,\tilde x}\ell(x,g(f(\tilde x)))$. The corruption distribution determines the invariances encouraged by training. It is incorrect to compare only against $\tilde x$ if the intended task is denoising; that could reward reproducing noise. Denoising is not identical to probabilistic generation, and a reconstruction network does not by itself provide a prior from which plausible latent codes can be sampled.

## 4. Variational autoencoders

A latent-variable model specifies $p_\theta(x,z)=p(z)p_\theta(x\mid z)$ and has marginal likelihood $p_\theta(x)=\int p(z)p_\theta(x\mid z)\,dz$. The integral and exact posterior may be intractable. Introduce an approximate posterior $q_\phi(z\mid x)$. Jensen's inequality yields

$$\log p_\theta(x)\ge\mathbb E_{q_\phi(z\mid x)}[\log p_\theta(x\mid z)]-D_{KL}(q_\phi(z\mid x)\|p(z))\equiv\mathcal L_{ELBO}.$$

More precisely, $\log p_\theta(x)=\mathcal L_{ELBO}+D_{KL}(q_\phi(z\mid x)\|p_\theta(z\mid x))$. The gap is nonnegative, and maximizing the bound jointly improves model and inference parameters but does not prove the true likelihood is maximized. The first term rewards a probabilistic reconstruction; the second regularizes each approximate posterior towards the prior. The reconstruction term is not universally pixelwise MSE: its form depends on the decoder likelihood. An excessively influential KL term may encourage posterior collapse, where $q(z\mid x)$ carries little information about $x$.

For a diagonal Gaussian posterior and a unit normal prior, the analytic regularizer is

$$D_{KL}(q\|p)=\frac12\sum_i(\mu_i^2+\sigma_i^2-1-\log\sigma_i^2).$$

The encoder may output $\log\sigma_i^2$ for numerical convenience, in which case $\sigma_i=\exp(\tfrac12\log\sigma_i^2)$. Confusing log variance with standard deviation changes both samples and KL. The reparameterization trick draws $\epsilon\sim\mathcal N(0,I)$ independently of the encoder and computes $z=\mu+\sigma\odot\epsilon$. Gradients pass through the deterministic transformation for each noise draw. This is a pathwise estimator for suitable continuous distributions; it does not make a hard categorical draw differentiable without further methods. Monte Carlo noise remains, and one sample is not a universal guarantee of low variance.

**Algorithm:** Given a minibatch, obtain $\mu$ and log variance, draw standard Gaussian noise, form $z$, evaluate the decoder likelihood and analytic KL, and update encoder and decoder by gradients of negative ELBO. At generation time sample from the prior and decode. A decoder with an elementary pixelwise likelihood can average multiple plausible outputs, giving blurry reconstructions; this is a common tendency rather than a theorem that all VAE samples must be blurry. A powerful decoder, alternative likelihood, or training choice changes the result. Comparing a single output with a GAN image cannot establish general superiority.

## 5. GAN games and equilibrium

The original GAN uses generator $G(z)$ with $z\sim p_z$ and discriminator $D(x)\in(0,1)$. Its minimax objective is

$$\min_G\max_D\;\mathbb E_{x\sim p_{data}}\log D(x)+\mathbb E_{z\sim p_z}\log(1-D(G(z))).$$

The discriminator distinguishes real and generated observations; the generator changes the distribution of its outputs. With a fixed generator and sufficient discriminator capacity, $D^*(x)=p_{data}(x)/(p_{data}(x)+p_g(x))$ wherever the denominator is positive. If $p_g=p_{data}$ and class priors are equal, $D^*=1/2$ on the common support. This conclusion assumes the ideal equilibrium and an optimal discriminator, not merely that training has run for many iterations. The initial $D(G(z))$ is not determined by the game; it depends on initialization and the state of optimization. A nearly perfect discriminator can assign values near zero to fake samples, but zero is not a general initial condition.

Typical training alternates discriminator and generator updates. The original saturating generator loss may have weak gradients when the discriminator confidently rejects generated images; the widely used non-saturating objective maximizes $\log D(G(z))$ instead while retaining the same intended equilibrium. A conditional GAN introduces additional conditioning information and objectives; a vanilla unconditional GAN need not model a labeled joint distribution. A GAN usually provides a sampling procedure rather than a tractable explicit density. Its discriminator output is a real-versus-generated score under its training setup, not automatically a calibrated likelihood.

Mode collapse occurs when diverse latent inputs produce limited output modes. A generator may achieve convincing individual samples while omitting important regions of the data distribution. Conversely, a diverse but unrealistic sample set has poor fidelity. Oscillating adversarial updates, an overpowering discriminator, limited model capacity and dataset bias can all complicate training. Progress must be assessed with multiple diagnostics and held-out data; an apparently stable loss curve is insufficient evidence of distributional equality.

## 6. Metric learning and verification

A Siamese model applies the same encoder $f_\theta$ to multiple inputs. Shared weights mean that two applications do not double the number of trainable parameters. The loss is chosen to impose geometry on the embeddings: matched examples should be near and mismatched examples sufficiently separated. Verification asks whether a pair belongs to the same identity, usually by thresholding a distance. Identification selects among a gallery of identities; open-set identification additionally needs a reject decision. The gallery, threshold, data distribution and operating point affect error rates.

For anchor $a$, positive $p$ and negative $n$, squared Euclidean triplet loss with margin $\alpha$ is

$$L=\max\{0,\|f(a)-f(p)\|_2^2-\|f(a)-f(n)\|_2^2+\alpha\}.$$

The hinge makes the loss nonnegative. Zero means the specified margin is satisfied for that triplet, not that every possible triplet is correct. A negative must be farther from the anchor than its positive by at least the margin in the chosen distance units. Squared and unsquared distances yield different numerical margins and gradients. Mining determines which examples contribute: easy triplets often have zero loss, while very hard negatives may be mislabeled or destabilize training. A contrastive pair objective instead works with positive and negative pairs, often applying a margin to the latter.

For the source vectors $a=(4,5,3,7,1)$, $p=(8,5,6,7,1)$, $n=(9,1,3,8,0)$, the squared distances are $25$ and $43$. With margin $12$, the unhinged expression is $-6$ and the standard loss is zero. The keyed $-30$ is neither of those values. This discrepancy is explicitly recorded with the source question; it should not be silently corrected in the answer key.

## 7. Comparison and evaluation

| Method | Training signal | Generation or prediction | Principal limitation |
| :--- | :--- | :--- | :--- |
| Discriminative classifier | Label prediction | $p(y\mid x)$ or score | Does not by itself model $p(x)$ |
| Autoencoder | Reconstruction | Encode and reconstruct | A useful prior is not guaranteed |
| VAE | ELBO: likelihood and KL | Prior sample then decode | Bound gap and likelihood assumptions |
| GAN | Adversarial game | Transform prior samples | Instability and missing modes |
| Metric encoder | Pair/triplet distances | Threshold or rank embeddings | Mining and threshold calibration |

FID compares feature distributions of real and generated images using Gaussian approximations. If their feature means and covariances are $(\mu_r,\Sigma_r)$ and $(\mu_g,\Sigma_g)$, its population expression is

$$\|\mu_r-\mu_g\|^2+\operatorname{tr}(\Sigma_r+\Sigma_g-2(\Sigma_r^{1/2}\Sigma_g\Sigma_r^{1/2})^{1/2}).$$

Lower is better under the chosen feature extractor and evaluation protocol. FID is sensitive to preprocessing, finite sample estimation and the features chosen; its Gaussian summary is not a full distributional comparison. It may miss failure modes outside the representation and is computationally nontrivial. Scores obtained with different preprocessing, sample counts or extractors should not be treated as directly comparable. It measures neither semantic correctness nor fairness by itself.

Disentanglement asks whether coordinates capture distinct underlying factors, but requires an operational definition. The mutual information gap computes, for each known factor, the gap between its largest and second-largest mutual information with individual latent coordinates, normalized by the factor entropy, then averages. This requires access to meaningful factor labels and depends on their distributions and estimation. A high score under one metric is not proof of causal or universal disentanglement. Visual quality, distribution coverage, privacy, downstream utility and subgroup performance should be examined separately.

## 8. Applications, pitfalls and handoff

In medical imaging, conditional synthesis may support augmentation, but memorization, missing pathology and distribution shifts can undermine evaluation. In face verification, a learned embedding supports matching; demographic imbalance, threshold calibration and presentation attacks affect practical errors. In industrial inspection, a reconstruction model may highlight deviations, but high reconstruction error is not automatically a calibrated anomaly probability. In image compression, a bottleneck trades rate against distortion; actual compression requires counting quantization, entropy coding and model overhead. These cases need held-out evaluation aligned with their respective operational goals.

**Dangerous misconceptions:** low reconstruction error does not imply a good unconditional generator; KL is not symmetric even when one particular pair has equal values; the ideal GAN discriminator output of one half is conditional on equilibrium; and a negative unhinged triplet expression is not a negative hinge loss. The PCA connection requires a particular loss and optimization setting. When reading a key, preserve what it states and separately identify missing assumptions or contradictory calculations.

The next provisional cluster concerns attention and vision transformers. Its representations can serve as encoders or feature extractors for the same generative and metric objectives, but architecture alone does not determine the statistical model or evaluation protocol.

## 9. References and annotated literature

1. Kingma, D. P. and Welling, M. (2014), “Auto-Encoding Variational Bayes,” *ICLR*. [arXiv:1312.6114](https://arxiv.org/abs/1312.6114). Contribution: derives the variational objective and pathwise stochastic-gradient estimator.
2. Goodfellow, I. et al. (2014), “Generative Adversarial Nets,” *NeurIPS*. [arXiv:1406.2661](https://arxiv.org/abs/1406.2661). Contribution: introduces the adversarial game and ideal discriminator analysis.
3. Vincent, P. et al. (2010), “Stacked Denoising Autoencoders,” *JMLR*, 11, 3371–3408. [JMLR paper](https://www.jmlr.org/papers/v11/vincent10a.html). Contribution: studies learning representations by reconstructing clean inputs from corrupted observations.
4. Schroff, F., Kalenichenko, D. and Philbin, J. (2015), “FaceNet,” *CVPR*. [DOI: 10.1109/CVPR.2015.7298682](https://doi.org/10.1109/CVPR.2015.7298682). Contribution: applies triplet-based embedding learning to face recognition.
5. Heusel, M. et al. (2017), “GANs Trained by a Two Time-Scale Update Rule Converge to a Local Nash Equilibrium,” *NeurIPS*. [arXiv:1706.08500](https://arxiv.org/abs/1706.08500). Contribution: introduces FID and studies different update rates.
6. Chen, R. T. Q. et al. (2018), “Isolating Sources of Disentanglement in Variational Autoencoders,” *NeurIPS*. [arXiv:1802.04942](https://arxiv.org/abs/1802.04942). Contribution: introduces mutual information gap as a factor-based measure.

## Appendix A — Computational reproducibility

Execute the self-contained arithmetic in [[week-8-exam-notes]] with `uv run python` in the repository environment. The source bank retains official answers and identifies calculations that disagree with them.

## Appendix B — Knowledge graph connections

Upstream: [[week-7-report]] · Sibling: [[week-08-questions]] · Downstream: [[week-9-report]] · Concepts: [[variational-autoencoder]], [[kullback-leibler-divergence]], [[generative-adversarial-network]], [[triplet-loss]].
