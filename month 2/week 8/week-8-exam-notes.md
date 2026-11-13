---
title: "Week 8 Exam Notes: Generative Models and Metric Learning"
week: 8
month: 2
status: provisional
map: "[[Knowledge-Map]]"
report: "[[week-8-report]]"
---

# Week 8 exam notes

> topics inferred from past papers; replace when the official syllabus is available

Use these notes with [[week-8-report]] and [[week-08-questions]]. The source key is reported as given in the bank; warning blocks distinguish incorrect or underspecified answers from the mathematical derivation. The concepts [[variational-autoencoder]], [[kullback-leibler-divergence]], [[generative-adversarial-network]] and [[triplet-loss]] provide the definitions behind the formulas.

## One-line recalls

- A discriminative classifier models or scores $p(y\mid x)$; a generative classifier can factor $p(x,y)$ into a likelihood and a class prior.
- Bayes' denominator sums the joint probability or density of the observation over all classes.
- Maximum likelihood minimizes negative log likelihood, and corresponds to forward data-to-model KL up to data entropy.
- KL divergence is nonnegative but generally asymmetric; it is not a distance metric.
- An autoencoder reconstructs inputs through a latent representation; a bottleneck does not automatically define a generative prior.
- Denoising training reconstructs the clean target from its corrupted input.
- A centered, squared-error linear bottleneck autoencoder at a global optimum recovers a principal reconstruction subspace under standard assumptions.
- A VAE combines an expected log likelihood with a KL regularizer in an evidence lower bound.
- Reparameterization uses independent noise and a differentiable transformation, rather than differentiating through a random draw directly.
- A vanilla GAN has a generator and discriminator; its learned sample distribution need not have a tractable likelihood.
- At ideal matching with equal class priors, an optimal GAN discriminator returns one half on the common support.
- Siamese branches share weights; repeated use of the same encoder does not multiply its parameter count.
- Verification tests a claimed identity; identification searches for an identity among candidates.
- FID compares feature statistics, while mutual information gap evaluates a specified notion of factor separation using known factors.

## Formulas to reproduce

Bayes for classes $c$:

$$p(c\mid x)=\frac{p(x\mid c)p(c)}{\sum_j p(x\mid j)p(j)}.$$

For discrete distributions, $D_{KL}(P\|Q)=\sum_i p_i\log(p_i/q_i)$. The index includes every possible outcome. If the logarithm is natural the unit is nats; base two gives bits. A zero $p_i$ contributes zero by continuity, whereas positive $p_i$ with zero $q_i$ gives an infinite divergence. KL equality under argument reversal for one particular pair is not a proof of symmetry. The Bernoulli expansion is $p\log(p/q)+(1-p)\log((1-p)/(1-q))$.

The VAE evidence lower bound is

$$\mathcal L=\mathbb E_{q_\phi(z\mid x)}\log p_\theta(x\mid z)-D_{KL}(q_\phi(z\mid x)\|p(z)).$$

For $q=\mathcal N(\mu,\mathrm{diag}(\sigma^2))$ and $p=\mathcal N(0,I)$, use $\tfrac12\sum_i(\mu_i^2+\sigma_i^2-1-\log\sigma_i^2)$. If the network returns log variance $s$, take $\sigma=\exp(s/2)$ before forming $z=\mu+\sigma\odot\epsilon$, with $\epsilon\sim\mathcal N(0,I)$. Keep batch and latent dimensions aligned; multiplication is elementwise. The KL is a regularizer in the ELBO, not a standalone replacement for its reconstruction term.

The GAN discriminator objective is $\mathbb E_{data}\log D(x)+\mathbb E_z\log(1-D(G(z)))$. The generator minimizes this in the original minimax formulation, while a common non-saturating alternative maximizes $\mathbb E_z\log D(G(z))$. Holding the generator fixed, $D^*(x)=p_{data}(x)/(p_{data}(x)+p_g(x))$ where defined. Do not infer that a real discriminator is optimal, or that a value of one half proves distributional matching without the other assumptions.

For squared Euclidean triplets, $L=\max(0,d(a,p)^2-d(a,n)^2+\alpha)$. The margin is measured in the units of the chosen distance expression. A pairwise contrastive loss convention may differ in which binary label denotes positive; read the definition before substitution. Ranking compares relative distances rather than requiring a fixed class label for each possible person.

## Numerical recipes and worked examples

**Bayes.** Multiply each likelihood by its class prior, sum these products, then divide the desired product by the sum. For cat likelihood $0.06$, dog likelihood $0.02$, and corresponding priors $0.6$ and $0.4$, the numerator is $0.036$ and the denominator $0.044$; the cat posterior is approximately $0.81818$. Normalize only after including all classes.

**Gaussian sample.** For $\mu=(0.2,0.3,0.1)$, $\sigma=(0.1,0.2,0.1)$ and $\epsilon=(0.5,0.2,0.8)$, the components are $0.2+0.1(0.5)$, $0.3+0.2(0.2)$, and $0.1+0.1(0.8)$, yielding $(0.25,0.34,0.18)$. A specified noise sample is used as given; it is not replaced by its mean zero. Round only after computing the requested component.

**Gaussian KL.** With $\mu=(0,1)$ and $\sigma=(1,0.5)$, the first coordinate contributes zero. The second contributes $\tfrac12(1+0.25-1-\log0.25)=0.818147\ldots$. The logarithm is of the variance $0.25$, not the standard deviation $0.5$. This calculation uses natural logarithms.

**Bernoulli KL.** For $P=\operatorname{Bernoulli}(0.9)$ and $Q=\operatorname{Bernoulli}(0.1)$, use both the success and failure terms: $0.9\ln9+0.1\ln(1/9)=0.8\ln9\approx1.75778$. An expression $c\ln d$ does not uniquely identify both $c$ and $d$ without further restrictions. In particular, the source pair $c=0.9,d=8$ does not equal this KL value.

**Triplet.** For $a=(4,5,3,7,1)$, $p=(8,5,6,7,1)$ and $n=(9,1,3,8,0)$, calculate $d^2(a,p)=16+9=25$ and $d^2(a,n)=25+16+1+1=43$. With margin 12, the hinge argument is $25-43+12=-6$, so the standard loss is zero. The source's negative answer is retained with a warning in the bank. If a question defines a different sign or omits the hinge, follow the explicit definition while stating it.

**Shared parameter count.** Two branches each execute an encoder containing 73,286 trainable parameters. If the branches share the same parameter objects and there are no additional modules, the total is 73,286, not twice that value. If the branches merely have identical architectures but independent weights, the count doubles: architecture equality alone does not prove weight sharing.

The following executable check reproduces the numerical results. Run it with `uv run python` from the repository environment; the code has no random sampling.

```python
import math

mu = [0.2, 0.3, 0.1]
sigma = [0.1, 0.2, 0.1]
eps = [0.5, 0.2, 0.8]
z = [m + s * e for m, s, e in zip(mu, sigma, eps)]
a, p, n = [4, 5, 3, 7, 1], [8, 5, 6, 7, 1], [9, 1, 3, 8, 0]
dap = sum((x-y)**2 for x, y in zip(a, p))
dan = sum((x-y)**2 for x, y in zip(a, n))
print('Bayes:', round(.06*.6/(.06*.6+.02*.4), 6))
print('z:', [round(x, 2) for x in z])
print('Gaussian KL:', round(.5*(1+.25-1-math.log(.25)), 6))
print('Bernoulli KL:', round(.8*math.log(9), 6))
print('Triplet distances and loss:', dap, dan, max(0, dap-dan+12))
```

```text
Bayes: 0.818182
z: [0.25, 0.34, 0.18]
Gaussian KL: 0.818147
Bernoulli KL: 1.75778
Triplet distances and loss: 25 43 0
```

## Common traps

- A Gaussian decoder with fixed variance makes MSE proportional to negative log likelihood; a different likelihood or learned variance changes the objective.
- Forward and reverse KL are not interchangeable. A question that prints one but invokes a property of the other is underspecified or erroneous.
- An initial discriminator probability of zero is a possible approximation for a strong discriminator, not a consequence of random initialization.
- A $D(G(z))$ of one half is an ideal-equilibrium result under equal priors, not a practical certificate of a successful GAN.
- A source may call a score “triplet loss” but supply an unhinged expression. Check the stated definition and the arithmetic separately.
- A VAE's location-scale trick is not an exact ordinary pathwise derivative for hard discrete samples; special estimators or relaxations are needed.
- A low FID is conditional on feature extraction and sample protocol; it cannot prove diversity, semantic correctness, privacy or absence of bias.
- Global attention covers all encoder states, while position encoding conveys order; these ideas can appear in mixed-topic multiple-select questions.
