# InfoNCE loss

InfoNCE is a contrastive classification objective that identifies a positive candidate among a set containing that positive and sampled alternatives. For logits $z_j=s(q,k_j)/\tau$, the loss is $-z_+ + \log\sum_j e^{z_j}$, the cross-entropy of the positive index. Temperature $\tau>0$ controls the scale of similarities before softmax. A smaller temperature sharpens a fixed set of unequal logits, but its effect on gradient magnitude depends on the scores. Implementations should use log-sum-exp for numerical stability and state whether the positive is included in the denominator. Mutual-information interpretations require assumptions about the sampling distribution and should not be inferred from the formula alone.

## Why it matters here

The end-term calculation requires including the positive in the denominator and using the natural logarithm, while respecting any rounding given in the question.

**Appears in:** [[week-11-report]] · [[week-11-exam-notes]] · [[week-11-questions]]

## Related

[[contrastive-learning]] · [[clip-alignment]]
