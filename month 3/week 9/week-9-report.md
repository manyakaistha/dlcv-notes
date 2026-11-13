---
title: "Transformers for Vision: Attention, Representation and Set Prediction"
week: 9
month: 3
status: provisional
date: 2026-11-14
prev: "[[week-8-report|Week 8]]"
next: "[[week-10-report|Week 10]]"
map: "[[Knowledge-Map]]"
tags:
  - dlcv/week-09
  - dlcv/transformers
concepts:
  - "[[scaled-dot-product-attention]]"
  - "[[multi-head-attention]]"
  - "[[position-encoding]]"
  - "[[vision-transformer-patches]]"
  - "[[detr-set-prediction]]"
---

# Transformers for Vision: Attention, Representation and Set Prediction

> **Week 9 Review Article — Month 3 / Week 9**  
> Topics inferred from past papers; replace when the official syllabus is available.  
> Practical method: **Concept → Code → Output → Interpretation**.

**Navigation:** ← [[week-8-report|Week 8]] · [[Knowledge-Map|Knowledge Map]] · [[week-10-report|Week 10]] →  
**Associated concepts:** [[scaled-dot-product-attention]] · [[multi-head-attention]] · [[position-encoding]] · [[vision-transformer-patches]] · [[detr-set-prediction]]

## Abstract

Transformers replace a fixed sequence-processing recurrence with data-dependent interactions between vector representations. This review derives scaled dot-product attention, multi-head projections, positional representations and the encoder–decoder architecture, then applies the same principles to image patches and object detection. Shape accounting distinguishes the number of tokens, the number of attention scores and the number of learned parameters, quantities that are frequently confused in examination questions. Vision Transformers (ViTs) turn an image into a sequence of embedded patches, whereas DETR treats object detection as a set prediction problem with bipartite matching. Worked calculations expose the assumptions needed for numerical answers and distinguish keyed exam answers from mathematical identities. The classification of these topics into this week is provisional, not evidence of an official syllabus.

**Keywords:** self-attention; `Q [N, d_k]`; positional encoding; ViT; DETR; matching; decoder masking.

## 1. Introduction and syllabus

A convolution applies shared local filters across an image. A recurrent network updates a state sequentially. A Transformer instead constructs interactions between positions using learned query, key and value projections. All positions in an unmasked encoder layer can exchange information directly, although the representation learned at a position is still constrained by training data, depth, width and the available image features. The change in computational organization is especially useful for combining visual and textual representations and for handling inputs with varying numbers of tokens. It does not imply that all tokens are treated as spatially indistinguishable: position information must enter the architecture somehow.

The provisional topic taxonomy comprises self-attention and QKV projections; Transformer encoders and decoders; token and positional representations; Vision Transformers; and Transformer object detection. The associated [[week-09-questions|question bank]] contains the 30 records classified to this week. Several test architecture labels or short numerical subparts, so an answer should be justified from the computation and diagram, not from a memorized label alone. The bank retains source keys and explicitly records imprecise questions.

| Topic | Central question | Examination operation |
| :--- | :--- | :--- |
| Self-attention | How does one token aggregate other values? | Project, score, scale, normalize, sum |
| Encoder and decoder | Which information can each block access? | Identify masked self-attention and cross-attention |
| Position and tokens | How can a set-like operation represent order? | Distinguish embeddings, positions and output logits |
| ViT | How is an image represented as vectors? | Count patches and trace the pipeline |
| DETR | How can a fixed set of queries predict objects? | Explain matching and small-object limitations |

## 2. Theoretical foundations

### 2.1 Queries, keys and values

Let $X\in\mathbb R^{N\times d}$ contain $N$ row vectors of width $d$. Learned projections yield $Q=XW_Q$, $K=XW_K$, and $V=XW_V$, where $W_Q,W_K\in\mathbb R^{d\times d_k}$ and $W_V\in\mathbb R^{d\times d_v}$. Thus $Q,K$ have shape `[N, d_k]`, while $V$ has shape `[N, d_v]`. A query encodes what a position seeks, a key provides a representation against which it is compared, and a value supplies the information combined after comparison. These are functional roles in the computation, not intrinsic semantic types.

The score matrix and output are

$$S=\frac{QK^\top}{\sqrt{d_k}},\qquad A_{ij}=\frac{e^{S_{ij}}}{\sum_{\ell=1}^{N}e^{S_{i\ell}}},\qquad Z=AV.$$

Here `S` and `A` are `[N, N]`, and `Z` is `[N, d_v]`. Row $i$ of $A$ gives the distribution over key positions used for query $i$; each row sums to one when at least one key is unmasked. The output $z_i=\sum_j A_{ij}v_j$ is a weighted combination of values, not a weighted combination of keys. Altering one query with keys and values fixed changes its score row and may change its attention distribution and output. It does not change the number or dimension of tokens. If all scores in the row shift by the same constant, softmax is unchanged; hence a changed query does not necessarily change the output in every degenerate case.

**Scaling.** Under a simplified model with independent, zero-mean, unit-variance query and key coordinates, the dot product has variance $d_k$. Dividing by $\sqrt{d_k}$ makes its variance approximately one. This prevents dimension alone from pushing logits into saturated regions of softmax. The assumptions need not hold exactly after training, so scaling is a design choice rather than a guarantee of unsaturated gradients. Numerically stable implementations subtract the row maximum before exponentiation; this leaves softmax unchanged.

### 2.2 Permutations, order and positions

If $P$ is a permutation matrix and the same permutation is applied to all rows of $X$, unmasked self-attention with shared projections obeys

$$\operatorname{Attn}(PX)=P\operatorname{Attn}(X).$$

This is **equivariance**: outputs move with inputs. It is not invariance, which would mean the output is unchanged. A symmetric pooling operation can subsequently produce a permutation-invariant global output. To represent order or image location, a model may add learned absolute positional vectors $p_i$ to token embeddings $x_i$, or introduce relative position terms into attention scores. A standard sinusoidal construction uses

$$p_{i,2j}=\sin(i/10000^{2j/d}),\qquad p_{i,2j+1}=\cos(i/10000^{2j/d}).$$

Absolute and relative methods encode different inductive biases; neither makes attention intrinsically aware of geometry without a defined mapping between tokens and positions. An exam key describing self-attention as invariant is therefore imprecise when referring to its sequence output. A fixed positional assignment also means that permuting content while keeping position vectors fixed changes the input representation.

A token embedding maps discrete token IDs or continuous patch contents into vectors in a common model space. It is distinct from a positional embedding, which indicates location or order. An input embedding represents the source sequence, and an output embedding represents target tokens supplied to the decoder. The final linear map instead produces logits over an output vocabulary; the following softmax gives a probability distribution. These components have different roles even if a particular model ties some weights.

### 2.3 Multi-head attention

For $h$ heads, head $i$ uses its own $W_Q^{(i)},W_K^{(i)},W_V^{(i)}$ and computes $H_i=\operatorname{Attention}(Q_i,K_i,V_i)$. The concatenated outputs are projected back to the model width:

$$\operatorname{MHA}(X)=\operatorname{Concat}(H_1,\ldots,H_h)W_O.$$

Often $d_k=d_v=d/h$, so concatenation has width $d$. Each head can learn different similarity and value subspaces, but independence or unique interpretable roles are not guaranteed. With equal model input and output widths and no biases, the three combined projections and output projection contain $4d^2$ weights. This count assumes the sum of head widths is $d$; specifying only a token count is insufficient. Biases add $4d$ in the common implementation. Parameters are shared across positions, whereas attention scores depend on every input example and are activations, not learned model parameters.

## 3. Core formulation and algorithms

### 3.1 Encoder and decoder

A canonical encoder layer has self-attention, residual connections, normalization and a position-wise feed-forward network. In the original post-normalization convention, one sublayer is $\operatorname{LN}(X+\operatorname{Sublayer}(X))$. Pre-normalization reverses the location of normalization relative to the sublayer, so diagrams and training behavior should not be conflated. The feed-forward network applies the same two affine maps and nonlinearity at every token:

$$\operatorname{FFN}(x)=W_2\,\phi(W_1x+b_1)+b_2.$$

It mixes channels within a token; attention mixes information across positions. Residual additions require matching feature dimensions. Layer normalization normally normalizes features within each token rather than aggregating statistics across the batch. Dropout can be used in training, but its presence is not a defining property of attention.

A standard autoregressive decoder contains causal masked self-attention, encoder–decoder cross-attention and a feed-forward network. In masked self-attention, query position $i$ can attend only to allowed target positions, conventionally $j\leq i$. A mask adds negative infinity to forbidden logits before softmax, giving them zero probability. The decoder inputs are shifted target tokens during teacher-forced training; at inference, previously generated tokens are fed back. This feedback is an autoregressive generation procedure, not a recurrent connection inside the vanilla Transformer layer. Cross-attention uses decoder states for queries and encoder outputs for keys and values. Source and target lengths may differ, producing an attention matrix `[N_target, N_source]`.

| Component | Queries | Keys and values | Access |
| :--- | :--- | :--- | :--- |
| Encoder self-attention | Source | Source | All valid source positions |
| Decoder masked self-attention | Target prefix | Target prefix | Current and earlier allowed positions |
| Decoder cross-attention | Decoder | Encoder output | Valid source positions |
| Position-wise feed-forward | Not applicable | Not applicable | Each position independently |

The final decoder state is mapped to vocabulary logits, and softmax turns those logits into probabilities. Cross-entropy compares the predicted next-token distribution with the target. Padding masks are separate from causal masks: they prevent attention to invalid padding rather than enforcing temporal order. An all-masked row needs explicit handling because a naive softmax over only negative infinities is undefined.

### 3.2 Concept → code → output → interpretation

**Concept.** Two row embeddings select rows of the projection matrices. Calculate the first query's scaled dot products, apply a stable softmax and combine the values. This reproduces the numerical structure in the first paper's attention questions.

**Code** (run with `uv run python`):

```python
import math
q = [2, 0, 2]
keys = [[2, 2, 2], [0, 2, 1]]
values = [[1, 1, 0], [0, 1, 1]]
scores = [sum(a*b for a, b in zip(q, k))/math.sqrt(3) for k in keys]
e = [math.exp(s-max(scores)) for s in scores]
w = [v/sum(e) for v in e]
z = [sum(w[i]*values[i][j] for i in range(2)) for j in range(3)]
print('scores:', *(f'{v:.6f}' for v in scores))
print('weights:', *(f'{v:.6f}' for v in w))
print('output:', *(f'{v:.6f}' for v in z))
```

**Output**

```text
scores: 4.618802 1.154701
weights: 0.969649 0.030351
output: 0.969649 1.000000 0.030351
```

**Interpretation.** The query matches the first key more strongly. The second output coordinate is exactly one because both values have that coordinate equal to one and the weights sum to one. The result depends on using row-vector projections and $d_k=3$; omitting scaling changes the weights.

### 3.3 Images as tokens

For image height $H$, width $W$, channels $C$, and non-overlapping square patches of side $P$ that divide both dimensions, the patch count is $N=(H/P)(W/P)$. Each flattened patch has $P^2C$ entries. A shared affine projection from `[P²C]` to `[D]` uses $P^2CD$ weights plus $D$ biases, if a bias is used. The resulting sequence has shape `[N, D]`; a class token, if used, makes its length $N+1$. Add positional vectors of matching width, process the sequence through encoder blocks, and apply the appropriate task head. Some ViT variants pool patch tokens rather than using a class token.

The original ViT is isotropic: encoder blocks preserve token count and embedding width. This distinguishes it from common pyramidal CNNs and hierarchical vision Transformers. It does not mean every model called a ViT maintains one resolution. Patch projection supplies local structure, but global attention has a weaker built-in locality bias than a CNN. Pretraining and data augmentation can therefore be consequential; architectural properties alone do not establish performance on a new dataset.

For a `64 × 64 × 3` image and `8 × 8` patches, there are $8\times8=64$ patch tokens and 192 scalars per patch. With one-pixel patches there are 4096 tokens, not 12288 tokens; 12288 counts input scalar values. Neither scalar count nor token count is the number of learned attention weights. If the raw 192-dimensional patch vector is used directly as model width, the Q/K/V weight matrices contain $3\times192^2=110592$ weights before biases and output projection; if patches are first projected to another width, use that width instead. This explicitly chosen assumption is essential because the exam statement does not specify it.

### 3.4 DETR and set prediction

DETR starts with a CNN feature map, flattens spatial locations into visual tokens, adds positional information and uses a Transformer encoder to build contextual features. A fixed set of learned object queries enters the decoder. Decoder self-attention lets query slots interact; cross-attention conditions each slot on encoded image features. Each output predicts a class, including a no-object category, and a box. These slots do not correspond to a fixed ordering of objects.

A one-to-one bipartite matching selects the assignment of ground-truth objects to prediction slots minimizing a cost based on class and box quality. The corresponding training loss supervises matched pairs and marks unmatched predictions as no-object. This set formulation discourages duplicate predictions through matching and avoids a separate hand-designed non-maximum suppression stage in the original inference pipeline. Matching is an optimization over assignments, not a differentiable attention distribution; gradients flow through the losses for the selected pairs. A fixed query budget caps the number of predictions in that configuration.

Small objects can be difficult because downsampled backbone features may allocate few spatial locations to them; attention and optimization can also make weak signals difficult to recover. The paper's multiple-choice answer describes signal dilution through global attention as the best listed explanation, but it is an oversimplification rather than proof that global attention always dilutes small objects. Multiscale representations and more focused attention can address aspects of the issue. Losses do not universally discard objects below a hard-coded pixel size, and object queries are not programmed to ignore small objects.

## 4. Numerical analysis and comparisons

The `[N, N]` attention matrix contains $N^2$ scores per head for self-attention. Constructing dense scores costs $O(N^2d_k)$ and combining values costs $O(N^2d_v)$, in addition to projections. Full attention-score storage is quadratic in sequence length, although memory-efficient exact implementations can avoid materializing the whole matrix. Patch size affects both $N$ and spatial detail. Halving patch side on a fixed image quadruples $N$ and increases the dense score count sixteenfold, ignoring special tokens. It does not automatically change the number of parameters in a fixed-width attention block.

| Quantity | Formula | Changes with sequence length? |
| :--- | :--- | :--- |
| Q/K/V weights, common width | $3D^2$ without bias | No |
| Output projection weights | $D^2$ without bias | No |
| One head's score entries | $N^2$ | Yes, quadratically |
| Patch projection weights | $P^2CD$ without bias | Depends on patch size, not patch count |
| Absolute learned positions | typically $ND$ | Yes, for a fixed position table |

These counts describe different objects. A positional table may need interpolation or another adaptation for an unseen image resolution. The model may share, tie or omit biases; always state the convention. A score entry is input-dependent and computed anew for each example, not a parameter merely because it is a scalar in the calculation.

## 5. Practical implementation and verification

A robust attention implementation first checks compatible tensor dimensions, multiplies queries by transposed keys, divides by $\sqrt{d_k}$ and applies additive padding or causal masks. It then uses a stable row-wise softmax and multiplies the result by values. Unit checks should verify output shape, row sums over allowed entries, zero mass on forbidden positions and agreement with a manually calculated small example. For batched multi-head input, a common shape is `[B, h, N, d_k]`; the score shape is `[B, h, N, N]`. For cross-attention, the last two dimensions are `[N_target, N_source]`. Head concatenation and output projection return `[B, N_target, D]` when configured conventionally.

For image classification, verify image divisibility or define padding, flatten each patch in a consistent channel order, apply the projection and insert positional vectors with the correct token count. An additional class token requires one more position vector. For detection, image padding must be masked, boxes must have a documented coordinate convention, and the matching cost must be distinguished from the final loss. These checks detect shape errors, but correct shapes do not establish statistical generalization.

## 6. Applications and scientific formulations

**Image classification.** A class token or pooled token representation is mapped to class logits. A failure mode is distribution shift in image statistics or object scale; validation must use an independent test set.

**Image captioning.** An image encoder supplies visual features, while a causal language decoder predicts the next word conditional on previous words and image features. Cross-attention can connect the modalities, but attention weights alone do not prove causal explanations of a caption.

**Object detection.** DETR predicts a set of class and box pairs using learned queries and assignment-based supervision. Occlusion, small objects and feature downsampling can impair localization, so evaluate by object scale and intersection-over-union threshold.

**Semantic segmentation.** Token features can be decoded to per-pixel or per-region labels. A Transformer does not restrict the output to one image-level class: the task head and spatial reconstruction determine the output resolution. Coarse patch grids can lose boundary detail unless the decoder recovers or fuses spatial information.

## 7. Critical challenges and misconceptions

1. **Scores are not parameters.** $N^2$ attention scores vary per input; projection matrices are learned parameters. The original exam's 12288 and 64 answers are respectively input scalar count and patch count under natural interpretations.
2. **Equivariance is not invariance.** Permuting token rows permutes self-attention outputs. Position signals, masks, and pooling change the symmetry of the complete model.
3. **Softmax is directional.** Normalize across keys for each query. Normalizing across queries changes the computation and generally changes the answer.
4. **A decoder's mask is not recurrence.** Parallel training uses a causal mask, while generation is sequential because future target tokens are unknown.
5. **Heads are not guaranteed explanations.** Separate projections allow different relations, but head semantics and attention maps require independent validation.
6. **Position does not come from token order alone.** A bare permutation-equivariant layer has no access to an externally assumed sequence order unless it is encoded in inputs or architecture.
7. **Small-object explanations are conditional.** Global interactions can help or hinder depending on representation and training; low-resolution features and scale variation also matter.
8. **Test data are not a tuning set.** Use validation data for architectural decisions and reserve the test set for final evaluation.

## 8. Conclusion and handoff

Attention computes a normalized, query-dependent mixture of values; its shape and normalization axis are essential for correct calculations. Multi-head encoder and decoder blocks provide distinct ways to mix source, target and cross-modal information, while position representations introduce order. ViT maps image patches to a vector sequence and DETR maps visual features to a set of object predictions. Count token activations separately from learned weights, and qualify statements about model invariance and small-object detection. The next provisional week extends generative modeling, including discrete latents and diffusion, connecting representations to image synthesis.

## 9. Academic references and annotated literature

- Vaswani, A. et al. (2017), “Attention Is All You Need,” *NeurIPS*. [arXiv:1706.03762](https://arxiv.org/abs/1706.03762). Contribution: scaled attention, multi-head Transformer and encoder–decoder design.
- Dosovitskiy, A. et al. (2021), “An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale,” *ICLR*. [arXiv:2010.11929](https://arxiv.org/abs/2010.11929). Contribution: patch-token ViT and large-scale image classification.
- Carion, N. et al. (2020), “End-to-End Object Detection with Transformers,” *ECCV*. [DOI:10.1007/978-3-030-58452-8_13](https://doi.org/10.1007/978-3-030-58452-8_13). Contribution: query-based set prediction and bipartite matching for detection.
- Zhu, X. et al. (2021), “Deformable DETR: Deformable Transformers for End-to-End Object Detection,” *ICLR*. [arXiv:2010.04159](https://arxiv.org/abs/2010.04159). Contribution: sparse, multiscale sampling for improved detection efficiency and small-object performance.

## Appendix A — Reproducibility

Run the complete code in Section 3.2 using `uv run python` from the repository root. It uses Python's standard library and no random state. The question bank records source-specific figures and keys; numerical assumptions should be checked against the original question.

## Appendix B — Knowledge graph

**Upstream:** [[week-8-report]] · **Downstream:** [[week-10-report]] · **Sibling:** [[week-9-exam-notes]] · [[week-09-questions]].
