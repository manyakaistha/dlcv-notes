# Generative adversarial network

A generative adversarial network (GAN) trains a generator and discriminator through an adversarial objective. The generator transforms noise into samples, while the discriminator estimates whether an input came from the data or generator under the training mixture. In the original minimax game, the discriminator maximizes expected log real and log fake classification scores and the generator minimizes the same objective. With fixed generator and adequate capacity, the optimal discriminator is $p_{data}/(p_{data}+p_g)$. At matching distributions and equal real/fake priors this is one half on their common support. Practical optimization typically alternates updates and need not reach this ideal equilibrium. Standard GAN sampling is implicit: a tractable density is not required.

## Why it matters here

The questions test equilibrium, alternating updates, and the distinction from variational autoencoders. A discriminator score alone cannot prove convergence, and plausible individual images do not guarantee that every data mode is represented.

**Appears in:** [[week-8-report]] · [[week-8-exam-notes]] · [[week-08-questions]]

## Related

[[variational-autoencoder]] · [[kullback-leibler-divergence]] · [[triplet-loss]]
