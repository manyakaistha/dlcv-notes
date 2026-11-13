---
title: "Vector quantization"
status: provisional
---

# Vector quantization

Vector quantization maps each continuous encoder vector to an element of a finite codebook, usually by minimizing squared Euclidean distance. In VQ-VAE the chosen entry is passed to a decoder, while the corresponding index provides a discrete latent representation. A reconstruction objective is combined with a codebook update and an encoder commitment penalty. Because the nearest-neighbor choice is discontinuous, the straight-through estimator passes a surrogate reconstruction gradient to the encoder; it is not the true derivative of the selection. A separate prior over discrete indices is generally needed to sample new code grids. Underuse of entries limits effective capacity even if the nominal codebook is large. **Why it matters here:** the past-paper questions identify the codebook as the finite set to which encoder outputs are mapped.

**Appears in:** [[week-10-report]] · [[week-10-exam-notes]] · [[week-10-questions]]

## Related

[[diffusion-process]]
