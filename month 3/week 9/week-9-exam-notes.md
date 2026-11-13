---
title: "Week 9 Transformer examination notes"
week: 9
month: 3
status: provisional
map: "[[Knowledge-Map]]"
report: "[[week-9-report]]"
tags:
  - dlcv/week-09
---

# Week 9 examination notes

> Topics inferred from past papers; replace when the official syllabus is available.

**Navigation:** [[week-9-report|Review article]] · [[week-09-questions|Question bank]] · [[Knowledge-Map|Knowledge Map]]

## One-line recalls

- A Transformer receives a sequence of vectors; raw word IDs and image patches must be embedded.
- Query selects information, key supplies a match representation, and value supplies the vector being aggregated.
- Each query forms a score with each key; softmax runs over the key positions for that query.
- The denominator $\sqrt{d_k}$ is based on the key/query width, not the number of tokens.
- Each attention output is a weighted sum of value vectors; its width is $d_v$.
- Self-attention is permutation-equivariant without positions or asymmetric masks, not generally permutation-invariant.
- Positional information specifies order or location; the token embedding identifies content.
- Multiple heads have separate projections and can represent different relations; interpretation is not guaranteed.
- The encoder has unmasked source self-attention and a position-wise feed-forward network.
- The autoregressive decoder uses masked target self-attention, source cross-attention and a feed-forward network.
- Cross-attention takes queries from the decoder and keys and values from encoder outputs.
- Causal masking prevents a training position from accessing later target tokens.
- Autoregressive generation is sequential, but a vanilla Transformer does not require recurrent connections.
- A ViT projects flattened image patches to model-width tokens, adds positional information and applies encoder blocks.
- A standard isotropic ViT preserves its token-grid resolution and embedding width across encoder blocks.
- DETR uses object queries and one-to-one matching to predict a set of boxes and classes.
- Small objects can suffer from coarse backbone resolution and limited multiscale features; no universal pixel cutoff follows.
- Segmentation is a dense output task and can use Transformer features; it is not limited to one label per image.

## Formula sheet and shape recipe

Let $X\in\mathbb R^{N\times D}$. With $W_Q,W_K\in\mathbb R^{D\times d_k}$ and $W_V\in\mathbb R^{D\times d_v}$,

$$Q=XW_Q,\quad K=XW_K,\quad V=XW_V,\quad Z=\operatorname{softmax}_{\mathrm{keys}}\left(\frac{QK^\top}{\sqrt{d_k}}+M\right)V.$$

For self-attention, `[N, d_k] × [d_k, N]` produces `[N, N]`, and `[N, N] × [N, d_v]` produces `[N, d_v]`. For cross-attention, replace the score shape by `[N_target, N_source]`. $M_{ij}$ is zero for an allowed entry and negative infinity for a forbidden one; it is applied before softmax. A row with no allowed key requires special treatment. Numerically, subtract the largest finite score in each row before exponentiation.

For $h$ heads with $d_k=d_v=D/h$, concatenation yields `[N, D]`, followed by an output projection. With separate Q, K, V and output maps, each `[D, D]`, the total is $4D^2$ weights, or $4D^2+4D$ parameters with four bias vectors. The count assumes these precise dimensions. Changing the number of heads at fixed $D$ does not change this standard total, though per-head widths and computation organization change.

For an image `[H, W, C]` and patch side $P$ dividing both spatial dimensions,

$$N=\frac HP\frac WP,\quad F=P^2C,\quad \text{patch-projection parameters}=FD+D\quad\text{(with bias)}.$$

A class token adds one to the sequence length and typically has $D$ learned entries. A learned absolute position table has $(N+1)D$ entries if it includes that token; check the actual implementation. Dense attention score entries per head are $(N+1)^2$ with a class token. These entries are activations, not model parameters. Projection weights are shared across tokens.

## Numerical recipe 1: two-token attention

For $q_1=[2,0,2]$, $k_1=[2,2,2]$, $k_2=[0,2,1]$, $v_1=[1,1,0]$, $v_2=[0,1,1]$, and $d_k=3$, the raw scores are $8$ and $2$. Divide each by $\sqrt 3$, producing $4.618802$ and $1.154701$. The resulting softmax weights are $0.969649$ and $0.030351$. The weighted sum is $[0.969649,1.000000,0.030351]$. The second coordinate is one because both values have a one there. Scores must be computed from keys; do not use the values for this dot product. These results are reproduced by the executable example in [[week-9-report]].

## Numerical recipe 2: pixels, patches and weights

For a `64 × 64 × 3` image with `8 × 8 × 3` patches, the grid has `8 × 8` positions, so $N=64$. Flattened patch width is $8\cdot8\cdot3=192$. The original image has $64\cdot64\cdot3=12288$ scalar entries; individual-pixel tokenization instead produces $4096$ tokens of width 3. These are three different quantities. With an assumed model width $D=128$, the patch projection has $192\cdot128+128=24704$ parameters including bias; the four standard attention maps have $4\cdot128^2+4\cdot128=66048$ parameters. The attention score matrix has $64^2=4096$ entries per head without a class token, or $65^2=4225$ with one. Scores are not weights trained in the model.

The following complete standard-library calculation checks the counts:

```python
H, W, C, P, D = 64, 64, 3, 8, 128
n = (H // P) * (W // P)
f = P * P * C
print('input scalars:', H * W * C)
print('patches and patch width:', n, f)
print('patch projection:', f * D + D)
print('attention parameters:', 4 * D * D + 4 * D)
print('score entries:', n * n, (n + 1) * (n + 1))
```

```text
input scalars: 12288
patches and patch width: 64 192
patch projection: 24704
attention parameters: 66048
score entries: 4096 4225
```

**Exam trap.** A past paper calls 12288 and 64 “parameters.” The source key is preserved, but the former is the input scalar count and the latter is the patch count. Attention parameter counts cannot be uniquely determined without the projection dimensions and bias convention. If $D$ is fixed, changing the number of patches changes the score matrix, not the attention projection weights.

## Numerical recipe 3: mask and positional symmetry

With three tokens and a standard causal mask, row one can access key 1, row two keys 1 and 2, and row three keys 1, 2 and 3. That is six allowed score positions out of nine, before considering padding. The mask is triangular because rows correspond to queries and columns to keys. A transpose reverses the allowed direction: write down the index rule $j\le i$ instead of guessing from a drawn triangle. If an encoder is bidirectional, its valid source tokens may attend in both directions, subject to padding.

For a permutation matrix $P$, self-attention without position and masks satisfies $f(PX)=Pf(X)$. If one subsequently sums token outputs, the sum is unchanged under permutation. Adding fixed position vectors makes content swaps distinguishable, because the positions stay attached to slots. A learned position vector and a token vector may be added only if their widths agree. The exam key that calls self-attention invariant is an imprecise description of the sequence-to-sequence operation.

## Architecture identification

Read an encoder–decoder diagram by tracing information flow. Source tokens enter the input embedding and position module, then encoder self-attention and feed-forward layers. The target prefix enters an output embedding followed by masked decoder self-attention. Cross-attention connects the decoder query stream to encoder keys and values. The decoder feed-forward layer produces hidden vectors; a linear projection maps these vectors to vocabulary logits and a softmax normalizes each vocabulary row. Encoder and decoder feed-forward layers are separate learned modules, even though their structural role is similar.

For a vision encoder, patching precedes linear projection, which precedes adding position vectors; encoder blocks and the task head follow. A class token may be inserted between projection and positional addition, so a claim about the immediately preceding operation depends on the implementation. A query in DETR is an object slot, not an image patch and not an explicitly preassigned class. One-to-one matching assigns ground-truth objects to distinct output slots for training; unmatched slots receive no-object supervision.

## Final traps and checks

- Write all tensor shapes before multiplying; $QK^\top$ compares queries to keys and $AV$ mixes values.
- Softmax of each valid row sums to one; scores do not need to sum to one.
- If every value coordinate equals the same constant, its attention output equals that constant for any valid softmax row.
- Scaling controls score magnitude under a variance model; it does not guarantee a uniform distribution.
- A soft attention weighted sum is differentiable under ordinary finite logits; discrete hard selection needs a different gradient estimator or approximation.
- Fixed head count does not prove heads attend to different semantic concepts.
- A position-wise feed-forward layer mixes feature channels, not tokens directly.
- A class token is an optional task design, not a universal requirement for every visual Transformer.
- Isotropic ViT statements apply to the standard architecture, not necessarily hierarchical derivatives.
- Attention alone does not prove causal explanation, robustness, or strong small-object accuracy.
- DETR matching, object queries and the no-object class should be distinguished from non-maximum suppression and anchor-box heuristics.
- Prefer a held-out validation set for tuning; a test set measures final generalization rather than selecting hyperparameters.
