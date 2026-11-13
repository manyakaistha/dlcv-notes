---
title: "Classifier-free guidance"
status: provisional
---

# Classifier-free guidance

Classifier-free guidance combines conditional and unconditional predictions from a diffusion model trained with occasional dropped conditioning. Under the convention $\epsilon_\gamma=\epsilon_u+\gamma(\epsilon_c-\epsilon_u)$, zero returns the unconditional prediction, one returns the conditional prediction, and values above one extrapolate toward the condition. Another convention uses $w=\gamma-1$, so its zero denotes ordinary conditional prediction. Stronger guidance often improves prompt or class adherence while reducing diversity or creating artifacts, but these are empirical tendencies rather than universal guarantees. No separate external classifier is required at sampling time. **Why it matters here:** multiple-select questions test the zero-scale convention and the tradeoff between conditioning strength and sample diversity.

**Appears in:** [[week-10-report]] · [[week-10-exam-notes]] · [[week-10-questions]]

## Related

[[diffusion-process]]
