# Variational autoencoder

A variational autoencoder (VAE) is a latent-variable generative model trained with an approximate posterior. It specifies a prior $p(z)$ and decoder likelihood $p_\theta(x\mid z)$, and uses an encoder $q_\phi(z\mid x)$ to approximate the posterior. Its evidence lower bound (ELBO) is the expected log decoder likelihood minus $D_{KL}(q_\phi(z\mid x)\|p(z))$. The difference between the log evidence and this bound is the divergence from the approximate to the true posterior. For a diagonal Gaussian encoder, $z=\mu+\sigma\odot\epsilon$ with independent standard Gaussian noise provides differentiable pathwise samples. The KL has a closed form for a standard normal prior. A decoder likelihood determines the appropriate reconstruction term; squared error is not universal.

## Why it matters here

Week 8 questions require calculating individual sampled coordinates and the Gaussian KL, interpreting the prior regularizer, and contrasting the VAE objective with a GAN. A low reconstruction loss alone is not proof that prior samples are useful.

**Appears in:** [[week-8-report]] · [[week-8-exam-notes]] · [[week-08-questions]]

## Related

[[kullback-leibler-divergence]] · [[generative-adversarial-network]] · [[triplet-loss]]
