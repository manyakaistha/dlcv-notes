---
title: "Focal loss"
status: provisional
---

# Focal loss

Focal loss modifies binary cross-entropy so that easily classified examples contribute less to dense detector training. With target-conditioned probability $p_t$, it is $-\alpha_t(1-p_t)^\gamma\log p_t$, where the focusing parameter $\gamma$ is nonnegative and $\alpha_t$ optionally weights classes. When $\gamma=0$, the expression reduces to weighted cross-entropy. When $p_t$ approaches one and $\gamma>0$, the modulating factor approaches zero. The loss changes classification weighting; it is not itself a geometric box regression loss.

## Why it matters here

Dense detectors encounter many easy background locations. RetinaNet uses focal loss to reduce their dominance, while retaining a separate localization objective for positive examples. A low focal loss does not imply accurate object boundaries.

**Appears in:** [[week-6-report]] · [[week-6-exam-notes]] · [[week-06-questions]]

## Related

[[intersection-over-union]] · [[feature-pyramid-network]] · [[semantic-segmentation]]
