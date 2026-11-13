---
title: "Gram matrix for style"
status: provisional
---

# Gram matrix for style

For feature activations $F\in\mathbb R^{C	imes M}$, the Gram matrix $G=FF^T$ contains pairwise channel inner products summed across spatial positions. It is an uncentered second-order statistic, not necessarily a normalized correlation or centered covariance. Neural style transfer compares Gram matrices of a synthesized image with those of a style reference at selected feature layers; a separate content loss compares spatial feature activations with a content image. Because a common permutation of spatial positions leaves $FF^T$ unchanged, the statistic captures some texture-like co-activation while discarding explicit arrangement. Different normalizations change the numerical loss. **Why it matters here:** an exam question asks about the Gram matrix’s role, and its keyed option should be read with the generated-versus-style distinction in mind.

**Appears in:** [[week-10-report]] · [[week-10-exam-notes]] · [[week-10-questions]]

## Related

[[vector-quantization]]
