# Adversarial examples

An adversarial example is an input deliberately perturbed to induce a model error under a specified threat model. The threat model states the attacker's objective and information, the permissible input domain, and the perturbation norm and budget. Under an $\ell_\infty$ constraint, FGSM adds the budget times the sign of the input-loss gradient; projected gradient descent repeats gradient steps and projects back onto the feasible set centered on the original input. A targeted attack can instead minimize loss for a chosen target. Standard PGD and Carlini–Wagner attacks are white-box; query-based zeroth-order attacks are black-box.

**Why it matters here:** Examination calculations require signs, coordinate-wise addition, and any stated clipping. A failed attack is not a proof of robustness, and input normalization changes the interpretation of the budget.

**Appears in:** [[week-12-report]] · [[week-12-exam-notes]] · [[week-12-questions]]

## Related

[[blip-pretraining]] · [[promptable-segmentation]] · [[multimodal-decoding]]
