---
title: "Week 11 End-Term Exam Notes"
week: 11
month: 3
status: provisional
report: "[[week-11-report]]"
map: "[[Knowledge-Map]]"
tags:
  - dlcv/week-11
  - dlcv/exam
---

# Week 11 End-Term Exam Notes

> **Provisional:** topics inferred from past papers; replace when the official syllabus is available.

**Navigation:** [[week-11-report|Review article]] · [[week-11-questions|Question bank]] · [[Knowledge-Map|Knowledge map]]

## Fast recalls

- **Self-supervision:** derive a prediction target or a relation from the data rather than using a manually assigned target-class label for that objective.
- **Pretext task:** an auxiliary task used to train a representation before evaluating a downstream task; high pretext accuracy does not prove transfer.
- **Temporal ordering:** frame sequence labels can come from the original video; temporal sampling assumptions may be violated by repeated or static content.
- **Conditional VAE:** class conditioning uses class information, so a class-labelled conditional VAE is not purely self-supervised under the exam's intended distinction.
- **Contrastive learning:** make a designated positive score well relative to candidate alternatives; negatives need not be different semantic classes.
- **SimCLR:** independently augment each image twice; use the companion view as positive and other batch views as alternatives.
- **MoCo:** compare a query against a positive key and a queue of keys; update the key encoder by momentum.
- **Few-shot:** adapt to target classes with a small labelled support set; $N$-way $K$-shot means $N$ classes and $K$ support examples per class.
- **Zero-shot:** make predictions for target classes without their labelled target examples, commonly using class names or descriptions as side information.
- **CLIP:** learn a common image–text space using paired data and symmetric contrastive cross-entropy; fixed downstream class labels are unnecessary.
- **Retrieval:** rank existing items from one modality using a query from the other. VQA returns an answer; text-conditioned detection returns localization as well as semantic matching.

## Formulas and symbols

For query $q$, positive $k^+$, candidate set $\mathcal K$ and temperature $\tau>0$, write

$$\ell=-\log\frac{\exp(s(q,k^+)/\tau)}{\sum_{k\in\mathcal K}\exp(s(q,k)/\tau)}.$$

The positive is included in this denominator. The loss is cross-entropy with the positive's index as the target. For logits $z_j=s_j/\tau$ and softmax $p_j$, $\partial\ell/\partial s_j=(p_j-\mathbf1[j=+])/\tau$. Lower temperature sharpens fixed unequal logits, emphasizing high-scoring alternatives relative to easier ones. It does not always increase every gradient norm, and it does not force orthogonality. Use natural logarithms unless a question explicitly defines another base.

For $N$ source images, SimCLR has $2N$ views. Each anchor has one positive, $2N-2$ negatives, and $2N-1$ terms in its denominator after the anchor is excluded. This count assumes one positive per anchor and no additional masking. A different multi-positive convention changes it. With $N=4$, eight views yield one positive and six negatives per anchor; seven candidates occur in the denominator. Augmentations define what the model is encouraged to ignore, so they must preserve task-relevant content.

For MoCo the update is

$$\theta_k\leftarrow m\theta_k+(1-m)\theta_q.$$

Here $\theta_q$ denotes query-encoder parameters and $\theta_k$ the key encoder. A high $m$ changes the key encoder slowly; queued keys originate from earlier iterations and may be stale. The key encoder is updated by this rule in the standard method rather than directly by the query loss. A queue supplies many candidate negatives without requiring one enormous current batch.

CLIP normalizes projected image vectors $u_i$ and text vectors $v_j$, then uses $S_{ij}=u_i^\top v_j/\tau$. The image-to-text term is row-wise cross-entropy with target $i$, and the text-to-image term is column-wise cross-entropy with target $j$:

$$L=\frac12\left[-\frac1B\sum_i\log\frac{e^{S_{ii}}}{\sum_j e^{S_{ij}}}-\frac1B\sum_j\log\frac{e^{S_{jj}}}{\sum_i e^{S_{ij}}}\right].$$

Thus “contrastive loss” and “cross-entropy loss” are compatible descriptions. Matching image–text pairs supply supervision; separate human class labels are not required. The model can classify without fine-tuning by embedding class prompts and ranking their similarities to the image. Candidate choice and prompt wording affect the result, and a softmax over candidate labels is not necessarily calibrated.

For few-shot prototypes, $c_k=|S_k|^{-1}\sum_{(x_i,y_i)\in S_k}f(x_i)$ and the prediction is the class whose prototype has smallest chosen distance from the query embedding. Some models instead fit a classifier or perform gradient-based adaptation. Meta-learning is one possible training approach, not a synonym for all few-shot learning. Keep query examples separate from support examples when measuring performance.

For nonzero equal-length vectors, $\cos(a,b)=a^\top b/(\|a\|_2\|b\|_2)$. The dot product equals cosine when both norms equal one. If lengths differ, the dot product is undefined; do not silently truncate a vector. CLIPScore is a specific metric with scaling and rectification conventions, so a bare cosine is not automatically the full CLIPScore. State the formula supplied in the question before converting to a percentage.

## Numerical recipes and worked examples

**InfoNCE from supplied exponentials.** A positive similarity of 2 and negatives 1 and 0 with unit temperature give $p_+=e^2/(e^2+e+1)$. Using the exam's rounded numbers gives $7.39/(7.39+2.72+1)=0.665167$ and $-\ln p_+=0.407718$, which rounds to $0.408$. Using full exponentials gives $0.407606$. Keep the positive in the denominator, and do not apply temperature a second time to logits already scaled by it. Intermediate rounding explains the small difference; the supplied-key interval begins at 0.408 and agrees after rounding to three decimals.

**Cosine versus dot product.** For $a=(0.2,0.5,0.3,0.4)$ and $b=(0.1,0.6,0.3,0.7)$, the dot product is $0.02+0.30+0.09+0.28=0.69$. Their norms are approximately $0.734847$ and $0.974679$, giving cosine $0.963364$. The source key of 69% corresponds to the raw dot product, although the vectors were called normalized. Report the source key while warning that the premise and true cosine disagree. A separate source question has one four-component and one three-component vector, so its cosine is not defined.

**Few-shot count.** For a five-way, two-shot episode, the support set contains $5\times2=10$ labelled examples. The number of query examples is not fixed by the way and shot alone. If a network previously trained on thousands of examples per source class adapts to unseen classes with 20 labelled examples each, that is 20-shot target adaptation. Do not count the source examples as target shots.

**Prototype calculation.** In a one-dimensional example, support embeddings for class A are 0 and 2, and for class B are 4 and 6. Their prototypes are 1 and 5. A query at 2 has distances 1 and 3, so nearest-prototype classification selects A. If a query is equally distant, the tie-breaking rule must be specified. In multiple dimensions, apply the selected distance to the vector prototypes rather than comparing individual coordinates independently.

**Symmetric CLIP probability.** For two pairs with similarity logits $[[2,0],[0,2]]$, each row and column assigns the paired item probability $e^2/(e^2+1)=0.880797$; the two direction losses agree at $0.126928$. The loss averages directions, so it remains $0.126928$, not twice that number. For an asymmetric matrix, compute row and column cross-entropies separately before averaging. The diagonal corresponds to the intended pairs only when the batch is arranged accordingly.

## Common traps and decision procedure

1. Identify whether the data supply a target, a human class label, or paired text. “Unlabelled” is relative to the target task, not a claim that the data have no structure.
2. Identify the anchor, positive, alternatives and denominator before substituting numbers. A designated negative may be semantically related to the anchor.
3. Check whether numbers are similarities or already temperature-scaled logits. Apply $\tau$ exactly once.
4. Check dimension and both norms before using a dot product as a cosine. A claimed normalization can be false.
5. Recognize that CLIP's symmetric cross-entropies implement a contrastive objective. Its original training does not rely on rotation prediction as the central pretext task.
6. Separate zero-shot from few-shot using labelled target examples, not the size of pretraining. A prompt provides side information, not necessarily a labelled target image.
7. Distinguish image-to-text and text-to-image directions. Detection requires spatial outputs, and VQA requires an answer conditioned on the question and image.
8. Treat source answer keys as evidence, not mathematical proof. Retain the key, derive independently and flag any disagreement.
9. Avoid assuming that a smaller temperature always improves retrieval, that more negatives are always beneficial, or that all correct captions are unique within a batch.
10. For test-set validity, avoid tuning prompts or adaptation choices on the final held-out examples; state any use of unlabelled query data.

## Verification

The arithmetic above was checked with the following deterministic standard-library code, runnable as `uv run python <file.py>`:

```python
import math
p = 7.39 / (7.39 + 2.72 + 1)
exact = math.log(sum(math.exp(x) for x in (2, 1, 0))) - 2
x, y = (0.2, 0.5, 0.3, 0.4), (0.1, 0.6, 0.3, 0.7)
dot = sum(a*b for a, b in zip(x, y))
nx = math.sqrt(sum(a*a for a in x))
ny = math.sqrt(sum(b*b for b in y))
print(f"rounded probability={p:.6f}, loss={-math.log(p):.6f}, exact={exact:.6f}")
print(f"dot={dot:.6f}, norms={nx:.6f},{ny:.6f}, cosine={dot/(nx*ny):.6f}")
print(f"support={5*2}, prototypes={(0+2)/2:.0f},{(4+6)/2:.0f}")
print(f"symmetric CLIP probability={math.exp(2)/(math.exp(2)+1):.6f}, loss={math.log1p(math.exp(-2)):.6f}")
```

The code verifies the displayed examples, including the distinction between rounded intermediate values and full exponentials. For more theory, method assumptions, application limitations and references, see [[week-11-report]].
