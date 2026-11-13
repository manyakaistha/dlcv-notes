---
title: "Week 12 end-term exam notes"
week: 12
month: 3
status: provisional
map: "[[Knowledge-Map]]"
report: "[[week-12-report]]"
---

# Week 12 end-term exam notes

> Topics inferred from past papers; replace when the official syllabus is available.

**Practice:** [[week-12-questions]] · **Theory:** [[week-12-report]]

## One-line recalls

- **BLIP:** a vision–language pretraining framework using contrastive alignment, pair matching and image-conditioned language modeling.
- **Image–text contrastive (ITC):** match separately encoded image and text embeddings against candidate embeddings.
- **Image–text matching (ITM):** classify a jointly encoded image–text pair as matched or mismatched.
- **Language modeling (LM):** predict the next token from image features and the preceding text.
- **Bidirectional self-attention:** each observed text position may attend to both earlier and later input positions.
- **Causal self-attention:** a position cannot attend to later text positions.
- **Cross-attention:** queries from one sequence attend to keys and values from another, such as text attending to image features.
- **Classification token:** a special sequence element whose representation can feed a classification head.
- **Decode token:** a mode/start signal for autoregressive generation, not a complete generated caption.
- **SAM:** an image encoder, prompt encoder and mask decoder provide prompt-conditioned segmentation.
- **Zero-shot transfer:** apply to an evaluation task without task-specific training under the stated protocol; performance is not guaranteed.
- **FGSM:** take one input-gradient sign step to increase the loss within an $\ell_\infty$ budget.
- **PGD:** iteratively increase the loss and project each iterate back into the allowed perturbation set.
- **White-box:** attacker knows the model and generally can compute gradients; standard PGD and C&W are examples.
- **Black-box:** attacker has limited access, such as prediction queries; query-based gradient estimation is possible.

## Formulas to retain

For projected queries $Q$, keys $K$, values $V$ and an additive mask $M$,

$$\operatorname{Attention}(Q,K,V)=\operatorname{softmax}\left(QK^\top/\sqrt{d_k}+M\right)V.$$

If queries are text tokens and keys/values are visual tokens, attention aligns each text query with image information. The softmax is over keys. A causal self-attention mask excludes future text; it does not automatically exclude image features in a separate cross-attention block. For `[B, N, d]` text and `[B, M, d]` image features the per-head score tensor is `[B, N, M]`.

For normalized image and text embeddings $z_i^I,z_i^T$ and temperature $\tau$,

$$\ell_{I\to T}^{(i)}=-\log\frac{\exp((z_i^I)^\top z_i^T/\tau)}{\sum_j\exp((z_i^I)^\top z_j^T/\tau)}.$$

Average the image-to-text and text-to-image directions for a symmetric contrastive objective. Similarity is relative to the other candidates in the batch. ITM instead takes a fused representation and applies a binary classification loss; both objectives can be useful even though their computation differs. When examples have multiple valid captions, a simple single-positive construction may treat a valid alternative as a negative.

Autoregressive factorization and the teacher-forced training loss are

$$p(T\mid I)=\prod_{t=1}^{N}p(t_t\mid t_{<t},I),\qquad
\mathcal L_{LM}=-\sum_t\log p(t_t\mid t_{<t},I).$$

Shift input and target tokens correctly. At inference the prefix contains the model's own earlier outputs; greedy choice is local, beam search is approximate, and sampling can increase diversity. No decoding policy guarantees a factually grounded caption.

For an untargeted attack with budget $\epsilon$,

$$x_{adv}=\operatorname{clip}_{\mathcal X}\{x+\epsilon\operatorname{sign}(\nabla_xL(\theta,x,y))\}.$$

The braces denote the expression being clipped, and $\mathcal X$ is the valid input domain. For $\ell_\infty$ PGD,

$$x^{k+1}=\Pi_{\mathcal X\cap B_\infty(x,\epsilon)}[x^k+\alpha\operatorname{sign}(\nabla_{x^k}L(\theta,x^k,y))].$$

Always center the ball on the clean input $x$. For a targeted attack that minimizes target-label loss, reverse the ascent sign. The scaling of $\epsilon$ must match the scale of $x$. A bound in normalized channels is not automatically the same as a bound in raw pixel values.

For binary masks $A$ and $B$, intersection over union is $|A\cap B|/|A\cup B|$. Define the empty-union convention when needed. IoU compares a predicted region with a reference; a model's own predicted quality score is not a ground-truth IoU.

## Diagram identification recipe

1. Locate the input image and text, then follow the arrows to their separate encoders. Self-attention exchanges information among tokens of the same stream.
2. Locate the text block receiving image features. Its text-to-image attention is cross-attention, with text queries and visual keys and values.
3. Determine whether all words are visible or future words are masked. The former is bidirectional encoding; the latter supports autoregressive decoding.
4. Match the contrastive head to separate embeddings, the matching head to a fused classification representation and the language head to decoder outputs.
5. Identify the role of special encode, classification and decode tokens. Only after that, copy the number assigned in the particular diagram: the same number has no universal meaning across figures.

A frequent exam trap is to infer that the image-grounded encoder has *only* cross-attention. It also has text self-attention; cross-attention adds image conditioning. Conversely, a causal decoder can access the whole image while remaining causal in text. Another trap is to call the image–text matching head contrastive merely because both losses compare image and text. The ITM head scores fused pairs; the contrastive loss compares independently encoded candidates.

## Worked numerical recipes

### 1. FGSM coordinate calculation

Given $x=(3,7,5)$, $g=(0.5,-0.5,1)$ and $\epsilon=0.01$, obtain $\operatorname{sign}(g)=(1,-1,1)$. Multiply by the budget to get $(0.01,-0.01,0.01)$, and add coordinate-wise to obtain $(3.01,6.99,5.01)$. The original problem specifies no valid input interval, so the example does not add an arbitrary pixel clip. If an interval were specified, clip the resulting vector to that interval.

### 2. One-dimensional PGD projection

Take clean $x=0.50$, $\epsilon=0.10$, current iterate $x^k=0.58$, step size $\alpha=0.05$, positive gradient, and valid interval $[0,1]$. The proposed point is $0.63$. The feasible interval is $[0.40,0.60]$, so projection returns $0.60$. Its displacement from the clean point is $0.10$, at the budget boundary. Projecting around $x^k$ instead would permit an invalid drift across repeated steps.

### 3. Intersection over union

If the predicted mask contains 8 pixels, the reference contains 7 pixels, and their intersection contains 5, the union contains $8+7-5=10$ pixels. IoU is therefore $5/10=0.5$. The intersection must not be counted twice in the union. This toy example checks arithmetic, not SAM performance.

### Reproducible verification

Run the following complete script with `uv run python`. It verifies the preceding arithmetic without requiring model weights or external downloads.

```python
x = [3.0, 7.0, 5.0]
g = [0.5, -0.5, 1.0]
sign = lambda v: (v > 0) - (v < 0)
print("FGSM:", [round(a + 0.01 * sign(b), 2) for a, b in zip(x, g)])
clean, epsilon, current, alpha = 0.50, 0.10, 0.58, 0.05
lo, hi = max(0.0, clean - epsilon), min(1.0, clean + epsilon)
print("PGD:", round(min(hi, max(lo, current + alpha)), 2))
intersection, pred, truth = 5, 8, 7
print("IoU:", intersection / (pred + truth - intersection))
```

```text
FGSM: [3.01, 6.99, 5.01]
PGD: 0.6
IoU: 0.5
```

## SAM and robustness traps

SAM can propose masks for unfamiliar objects and help annotators, but it does not guarantee perfect segmentation or automatically assign a semantic class to every mask. A point may refer to an object, part or enclosing region; multiple candidate masks and extra prompts address this ambiguity. Large and diverse training masks help zero-shot transfer, but a new imaging domain can still fail. Reusing image embeddings improves repeated interactive prompting without implying that the full model requires negligible hardware.

An adversarial example must be considered under a specified threat model. Record the norm, budget, scaling, valid domain, attacker knowledge, targeted or untargeted objective, attack iterations, step size and restarts. FGSM uses the gradient sign, not the gradient magnitude, for its $\ell_\infty$ step. PGD is iterative and projects after each step; it is a search procedure, not an exact certificate of robustness. An attack that fails because gradients are unavailable or masked does not prove that the classifier is robust.

C&W is an optimization-based white-box attack in its standard formulation, while ZOO estimates information through queries in a black-box setting. Random input transformation is not by itself a standard white-box attack. Defenses based on transformation require adaptive evaluation: an attacker may need to account for the transformation and its randomness. Finally, evaluate clean accuracy as well as attacked accuracy, since an apparent improvement in robustness can coincide with a change in ordinary predictive accuracy.

## Final self-check

Explain why a matching model can rerank independently retrieved candidates; trace how visual features reach a causal text decoder; derive the sign and valid range of each FGSM coordinate; and distinguish a promptable mask from a semantic label. If any answer relies only on memorizing a figure number or describing a model as “perfect,” return to the corresponding mechanism in [[week-12-report]].
