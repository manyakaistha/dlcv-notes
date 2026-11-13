---
title: "Recurrent Networks, Attention, and Visual Sequence Generation"
week: 7
month: 2
status: provisional
date: 2026-11-14
prev: "[[week-6-report|Week 6]]"
next: "[[week-8-report|Week 8]]"
map: "[[Knowledge-Map]]"
tags:
  - dlcv/week-07
  - dlcv/sequence-modeling
  - dlcv/attention
concepts:
  - "[[recurrent-neural-network]]"
  - "[[backpropagation-through-time]]"
  - "[[gated-recurrent-unit]]"
  - "[[encoder-decoder-attention]]"
---

# Recurrent Networks, Attention, and Visual Sequence Generation

> **Week 7 Review Article — Month 2 / Week 7**  
> **Provisional: topics inferred from past papers; replace when the official syllabus is available.**  
> Practical method: **Concept → Code → Output → Interpretation**.

**Navigation:** ← [[week-6-report|Week 6]] · [[Knowledge-Map|Knowledge Map]] · [[week-8-report|Week 8]] →  
**Associated Concepts:** [[recurrent-neural-network]] · [[backpropagation-through-time]] · [[gated-recurrent-unit]] · [[encoder-decoder-attention]] · [[week-7-exam-notes|Exam Notes]]

## Abstract

Visual recognition often requires predictions that depend on an ordered history, as in describing image regions with a sequence of words. Recurrent networks represent this history with a shared state transition, while backpropagation through time accumulates gradients across all uses of the shared parameters. Products of transition Jacobians explain both unstable gradients and the difficulty of retaining long-range dependencies; gated cells introduce controlled additive paths but do not guarantee successful learning. Encoder–decoder attention replaces a single fixed visual or sequence summary with a query-dependent weighted combination of feature vectors. Hard attention instead samples or selects discrete locations and requires an appropriate estimator for the selection mechanism. Parameter counts, normalized alignment scores, and caption evaluation are derived with explicit conventions, and numerical examples are reproducible in the companion exam notes.

## Keywords

Recurrent neural network; BPTT; LSTM; GRU; encoder–decoder; additive attention; dot product; image captioning; BLEU; `[time, batch, feature]`.

## 1. Introduction & Week 7 Syllabus

A convolutional image encoder converts pixels into spatial features; detection and segmentation use those features to localize objects and assign labels. A captioning system must additionally choose an ordered sequence whose length need not equal the number of image regions. A recurrent decoder handles variable-length prefixes by repeatedly applying one transition to a hidden state and the previous token. The same transition parameters are reused regardless of sequence length, so a model can process sequences longer than those seen at training, although performance and stability are not guaranteed to extrapolate.

The six clusters below are inferred from the supplied taxonomy and the 133 records assigned primary week 7 in the final classification. These records are exam evidence, not proof of the official lecture sequence. In particular, some mixed questions mention Transformer mechanisms and generative-model evaluation as well as recurrent attention. The section ordering is a conceptual laboratory sequence rather than a claim about dated lectures. The companion [[week-7-exam-notes|exam notes]] contain executed numerical recipes.

| Sequence | Core focus | Practical task |
| :--- | :--- | :--- |
| 1 | Recurrent states and topologies | Count shared parameters in stacked networks |
| 2 | BPTT and gradient dynamics | Trace Jacobian products and apply clipping |
| 3 | LSTM and GRU | Identify gates and count their parameters |
| 4 | Encoder–decoder alignment | Compute scores, softmax weights and context |
| 5 | Hard/soft attention and captioning | Compare estimators, decoding and BLEU |

## 2. Theoretical Foundations

### 2.1 Recurrence and conditional prediction

For input $x_t\in\mathbb{R}^{d}$ and state $h_t\in\mathbb{R}^{h}$, a vanilla recurrent network can be written

$$a_t=W_{xh}x_t+W_{hh}h_{t-1}+b_h,\qquad h_t=\phi(a_t),\qquad o_t=W_{hy}h_t+b_y.$$

Here `W_xh [h,d]`, `W_hh [h,h]`, `b_h [h]`, `W_hy [k,h]` and `b_y [k]` use column-vector convention; $o_t\in\mathbb R^k$ may be logits, subsequently normalized by softmax for classification. $h_0$ may be fixed, learned, or conditioned on an encoder. The state is a deterministic function of the prefix and the initial state; it is a compressed representation, not a literal storage of every past observation. A minibatch adds a batch dimension, and practical libraries may use `[batch, time, feature]` or `[time, batch, feature]`.

**Parameter sharing:** the matrices and biases above are the same at every time step. Unrolling a sequence draws multiple computational uses of one set of parameters, not independent layers with new weights. Sequence length affects computation and intermediate activation storage, but not this cell's parameter count. The cell without an output head has $hd+h^2+h$ scalars with one bias; the output head adds $kh+k$. Some libraries represent two biases per gate or transition, and problems that ask only for weights omit all bias terms. Always specify the convention before counting.

A sequence classifier uses one output after a prefix (many-to-one); frame tagging uses one output per input (aligned many-to-many); image-to-caption generation has one image condition and multiple output tokens (one-to-many); translation can have different input and output lengths (encoder–decoder many-to-many). A single vector can produce many outputs through a recurrent decoder without requiring the image to be repeatedly re-encoded. Conversely, a sequence-to-sequence system need not align output step $t$ with input step $t$.

A bidirectional encoder computes forward states from the left and backward states from the right, often concatenating them to form $h_i=[\overrightarrow h_i;\overleftarrow h_i]$. Each state then summarizes information on both sides of position $i$. A bidirectional model cannot be used naively for strictly causal prediction when future inputs are unavailable. An offline encoder can be bidirectional while its autoregressive decoder remains causal. Two directions normally have separate parameters; output dimension after concatenation is twice the per-direction hidden width.

### 2.2 Loss and backpropagation through time

For labels $y_t$ and logits $o_t$, a typical objective is $L=\sum_{t=1}^{T}\ell(o_t,y_t)$, perhaps averaged over valid tokens. Padding positions must be masked; otherwise padding artificially changes both the loss and the effective weighting of examples. Unrolling creates a directed acyclic computation graph, and reverse-mode differentiation accumulates each parameter's contributions across all its occurrences. In particular, $\partial L/\partial W_{hh}$ is a sum of contributions from all time steps, not the gradient of only the final transition.

The effect of a state $h_s$ on a later state $h_t$ involves the ordered product

$$\frac{\partial h_t}{\partial h_s}=J_tJ_{t-1}\cdots J_{s+1},\qquad J_j=\operatorname{diag}(\phi'(a_j))W_{hh}.$$

When the relevant singular directions contract repeatedly, long-range contributions can vanish; expansion can produce exploding gradients. The spectral radius of $W_{hh}$ alone is not a complete test: nonlinear derivatives, changing states, non-normal matrices, and alignment of singular directions matter. Saturated sigmoid and tanh units have small derivatives, intensifying contraction. Orthogonal recurrent initialization preserves norms for the linear transform at initialization, but nonlinearities and later updates can still contract or expand them.

**Algorithmic implication:** global norm clipping replaces gradient $g$ by $g\min(1,c/\|g\|_2)$ for threshold $c>0$. It limits the norm of the gradient supplied to the optimizer, not necessarily the eventual parameter-update norm under Adam, momentum, or weight decay. It reduces the impact of exploding gradients; it does not recover information already lost to vanishing gradients. Truncated BPTT detaches state periodically, saving memory and computation at the cost of omitting gradient paths beyond the truncation window. The forward state may still carry information across that boundary, but credit assignment through that boundary is cut.

### 2.3 Gated memory

An LSTM maintains a cell state $c_t$ as well as exposed hidden state $h_t$. With $[x_t;h_{t-1}]$ denoting concatenation and $\odot$ elementwise multiplication, one standard formulation is

$$\begin{aligned}
f_t&=\sigma(W_f[x_t;h_{t-1}]+b_f),& i_t&=\sigma(W_i[x_t;h_{t-1}]+b_i),\\
\tilde c_t&=\tanh(W_c[x_t;h_{t-1}]+b_c),& o_t&=\sigma(W_o[x_t;h_{t-1}]+b_o),\\
c_t&=f_t\odot c_{t-1}+i_t\odot\tilde c_t,& h_t&=o_t\odot\tanh(c_t).
\end{aligned}$$

The forget gate controls retention, the input gate controls writing, and the output gate controls exposure of the cell. Holding the gates fixed, the direct cell-to-cell derivative contains $\operatorname{diag}(f_t)$; products of values near one can preserve a direct gradient path. The full derivative also includes dependencies through the gates and hidden state, so this observation is not a guarantee against all vanishing or exploding gradients. For input width $d$ and hidden width $h$, four gates, one bias per gate, and no peepholes or projection, the cell count is $4(hd+h^2+h)$.

A common GRU convention uses update $z_t$, reset $r_t$, candidate $\tilde h_t$, and one state:

$$\begin{aligned}
z_t&=\sigma(W_zx_t+U_zh_{t-1}+b_z),\\
r_t&=\sigma(W_rx_t+U_rh_{t-1}+b_r),\\
\tilde h_t&=\tanh(W_nx_t+U_n(r_t\odot h_{t-1})+b_n),\\
h_t&=(1-z_t)\odot h_{t-1}+z_t\odot\tilde h_t.
\end{aligned}$$

Here a large $z_t$ favors the candidate and a large $r_t$ lets previous-state information enter the candidate. Other sources reverse the update-gate convention, or apply the reset gate after the recurrent affine transform; interpret a diagram from its equations rather than its label alone. For this formulation, three gates and one bias per gate give $3(hd+h^2+h)$ parameters. Frameworks with separate input and recurrent biases count $3(hd+h^2+2h)$; reset placement can also change the computation. An LSTM's separate cell state is not present in the basic GRU, and neither cell makes the state a perfect long-term memory.

## 3. Core Formulation & Algorithmic Machinery

### 3.1 Encoder–decoder alignment

A fixed-vector encoder–decoder maps an input sequence into a summary and conditions a decoder on that summary. Its bottleneck can lose information as inputs grow. Attention gives each decoder step access to encoder annotations $h_1,\ldots,h_S$, which can be word states, temporal states, or CNN region vectors. For decoder query $s_{t-1}$ and encoder annotation $h_i$, compute

$$e_{t,i}=\operatorname{score}(s_{t-1},h_i),\qquad
\alpha_{t,i}=\frac{\exp(e_{t,i})}{\sum_{j=1}^{S}\exp(e_{t,j})},\qquad
c_t=\sum_{i=1}^{S}\alpha_{t,i}h_i.$$

The decoder then conditions its next state or token distribution on $c_t$, alongside the previous state and token. Exact placement of $c_t$ depends on the architecture. $\alpha_{t,i}\ge0$ and $\sum_i\alpha_{t,i}=1$ over **valid encoder positions for that query**. The context has the same dimension as the value vectors. If separate key and value projections are used, scores use keys while the weighted sum uses values; they need not have the same width. Mask padded positions before softmax, typically with negative infinity, and ensure at least one valid position remains.

Common scoring choices include dot product $e_{t,i}=s_{t-1}^{\top}h_i$ when dimensions match; general/bilinear score $s_{t-1}^{\top}Wh_i$; and additive score

$$e_{t,i}=v^\top\tanh(W_ss_{t-1}+W_hh_i+b).$$

Additive attention uses learned projections to a common intermediate width and a learned vector $v$. Dot product is parameter-free only if the input vectors are used directly; projected dot products have learnable matrices. Scaled dot product divides by $\sqrt{d_k}$, where $d_k$ is the key/query dimension, to moderate logit magnitude under common variance assumptions. Do not apply this factor automatically to an unscaled dot-product question.

### 3.2 Numerically stable attention and interpretation

Softmax is invariant to subtracting the same constant from all scores: use $m=\max_i e_{t,i}$ and evaluate $\exp(e_{t,i}-m)/\sum_j\exp(e_{t,j}-m)$. This avoids overflow without changing probabilities. A higher score produces a higher weight, but the final context also depends on all values. A weighted average can lie between value vectors and need not equal any one of them. Distinct score vectors differing only by a constant yield identical weights; identical weights do not prove identical causal importance of input features.

For a query `[1, 0]`, keys `[2, 0]` and `[1, 0]`, and values `[1, 0]` and `[0, 2]`, unscaled dot scores are 2 and 1. The companion executable example obtains weights approximately 0.731059 and 0.268941 and context `[0.731059, 0.537883]`. The second context coordinate is twice the second weight because the value's second coordinate is 2. This demonstrates score, normalization and aggregation separately. Attention maps can be useful diagnostic visualizations, but their weights alone do not establish a faithful causal explanation: downstream processing and alternative attention distributions may yield similar predictions.

### 3.3 Hard versus soft attention

Soft attention computes the full weighted sum and is differentiable with respect to scores and values, so ordinary backpropagation applies. It typically evaluates all candidate features for each query. Hard attention selects a discrete location, for example $z_t\sim p_\theta(z_t\mid s_{t-1},h_{1:S})$, then uses the selected feature. Selection is not ordinarily differentiable through the discrete draw. A score-function estimator for expected reward $R$ is

$$\nabla_\theta\mathbb E_{z\sim p_\theta}[R(z)] = \mathbb E_z[R(z)\nabla_\theta\log p_\theta(z)]$$

when $R$ has no additional direct dependence on $\theta$; otherwise add the expected direct derivative. A baseline independent of the sampled action conditional on the state can reduce variance without changing the expectation. REINFORCE is one estimator, not a synonym for all hard-attention algorithms. Sampling introduces estimator variance, and a deterministic argmax has no useful ordinary derivative almost everywhere. Sparse or local selection can reduce feature-processing cost, but scoring every candidate can still be expensive; cost depends on the actual implementation.

### 3.4 Captioning and autoregressive decoding

A CNN may produce a global vector or a spatial feature map `[H, W, C]`, flattened into $S=HW$ region vectors. An RNN/LSTM decoder conditions on the image and previous tokens to model

$$p(y_{1:T}\mid I)=\prod_{t=1}^{T}p(y_t\mid y_{<t},I),\qquad
L=-\sum_{t=1}^{T}\log p(y_t^{*}\mid y_{<t}^{*},I).$$

Training commonly uses teacher forcing: ground-truth previous tokens are supplied when predicting the next token. At inference the model only has its own generated prefix, starting from a beginning token and stopping on an end token or length limit. This mismatch can compound errors, but teacher forcing remains a valid way to optimize the stated conditional likelihood. A global image vector is simple but may discard spatial detail; attention can condition each word on a different combination of region features. A CNN feature region's receptive field may overlap other regions and can include substantial context, so a single attention weight is not equivalent to isolating an object pixel.

Greedy decoding chooses the highest-probability next token locally. Beam search retains several partial sequences and compares their accumulated log probabilities; its result depends on beam size, termination, and any length normalization. It is not guaranteed to find the globally most probable sequence or the most accurate caption. Sampling enables diversity but can produce implausible outputs. Repeating or hallucinating an object can occur even if the sentence is fluent. A bidirectional encoder may inspect all image or source positions, whereas an autoregressive decoder must not access future target words at inference.

### 3.5 Relation to self-attention and Transformers

In cross-attention, queries come from the decoder and keys/values from encoded source or image features. In self-attention, queries, keys and values are projected from the same input sequence; the source representation is context-dependent and all valid tokens can interact. A Transformer uses attention and position-wise feed-forward layers without recurrence in its standard architecture, and positional information must be supplied to distinguish ordering. A causal mask prevents a decoder token from attending to future target positions. Unlike a recurrent transition, self-attention can process input positions in parallel during training; autoregressive generation still proceeds sequentially across generated tokens. These properties are architectural comparisons, not evidence that Week 9's detailed Transformer syllabus was officially taught in Week 7.

## 4. Numerical Analysis & Comparative Benchmarks

| Mechanism | State or context | Strength | Limitation |
| :--- | :--- | :--- | :--- |
| Vanilla RNN | One recurrent hidden state | Shared transition and variable length | Long products can destabilize gradients |
| LSTM | Hidden plus cell state; four gates | Controlled additive memory path | More gates and parameters; no guarantee of long-term learning |
| GRU | One state; reset and update gates | Simpler gated transition | Gate convention and implementation vary |
| Soft attention | Weighted sum over values | Differentiable end to end | Dense computation; weights are not automatically explanations |
| Hard attention | Selected discrete location | Potentially selective feature access | Discrete selection needs an estimator or other training method |
| Transformer self-attention | Token-to-token interactions | Parallel sequence processing during training | Requires positional information and appropriate masks |

### Caption evaluation

BLEU uses modified $n$-gram precisions with clipping against reference counts. For candidate length $c$, selected reference length $r$, maximum order $N$, and weights $w_n$ summing to one,

$$\operatorname{BLEU}=\operatorname{BP}\exp\left(\sum_{n=1}^{N}w_n\log p_n\right),\qquad
\operatorname{BP}=\begin{cases}1&c>r,\\e^{1-r/c}&c\le r.\end{cases}$$

Modified precision prevents a repeated candidate n-gram from being credited more often than its maximum count in the references. Corpus BLEU aggregates clipped counts and candidate counts before calculating precision; it is not generally the arithmetic mean of sentence BLEU scores. If an unsmoothed precision is zero, the geometric mean is zero. Smoothing, tokenization, reference selection and $N$ must be reported, particularly for short captions. BLEU measures textual n-gram overlap, not visual grounding, factual correctness, or semantic equivalence directly. A sensible paraphrase can receive a low score, and a common generic caption can overlap despite missing an image-specific detail. Human evaluation and complementary measures can therefore supply information BLEU lacks.

## 5. Practical Implementation & Verification

The following complete standard-library program verifies a single-bias recurrent count and an attention calculation. It uses no random sampling and can run from the project root using `uv run python`.

### Concept → Code → Output → Interpretation

The parameters are shared across time; the attention calculation normalizes over the two keys and combines the corresponding values.

```python
import math

d, h = 3, 4
print("RNN:", h*d + h*h + h)
scores = [2.0, 1.0]
maximum = max(scores)
exp_scores = [math.exp(s - maximum) for s in scores]
weights = [x / sum(exp_scores) for x in exp_scores]
values = [(1.0, 0.0), (0.0, 2.0)]
context = [sum(w * v[j] for w, v in zip(weights, values)) for j in range(2)]
print("weights:", *(f"{x:.6f}" for x in weights))
print("context:", *(f"{x:.6f}" for x in context))
```

```text
RNN: 32
weights: 0.731059 0.268941
context: 0.731059 0.537883
```

The cell has 12 input weights, 16 recurrent weights and 4 bias terms; no output head is included. The context is a convex combination of the two values. This checks arithmetic, not model accuracy or empirical convergence. The companion notes verify additional stacked, gated and BLEU examples.

## 6. Real-World Applications & Scientific Formulations

**Image description.** Target: generate a sentence grounded in an image. A CNN provides feature vectors and a conditional decoder models $p(y_t\mid y_{<t},I)$. Failure modes include object hallucination, missed small objects, and language priors overwhelming visual evidence. Region attention can expose where the model reads, but an attention map is not itself a causal proof.

**Video event recognition.** Target: classify a temporal sequence of frame features. A many-to-one RNN forms $h_T$ and a classification distribution $p(y\mid h_T)$. Failure modes include motion ambiguity from sparse frame sampling, vanishing credit assignment for early events, and information leakage when future frames are used in an online task. Masking variable-length batches and checking causal availability are essential.

**Visual question answering.** Target: condition an answer on a question and an image. A question-derived query scores image-region keys and aggregates visual values into a context. Failure modes include reliance on dataset language priors, ambiguous questions, and attention concentrating on a correlated background. A multimodal answer requires both representations to contribute; the existence of attention does not establish this empirically.

**Sequence transcription.** Target: map an image of a text line or video frames to an output sequence whose length differs from the number of visual features. Encoder–decoder attention models position-dependent alignments and an autoregressive decoder produces characters or words. Misalignment, repeated output, early end tokens, and out-of-vocabulary symbols are possible. Alternative alignment objectives can be used; attention should not be conflated with a specific loss such as CTC.

## 7. Critical Challenges, Pathology & Failure Modes

**The dangerous misconception:** unrolling creates new trainable recurrent weights at every time step. **Why this is false:** the same tensors are used repeatedly; their gradient contributions add. A different layer or direction, however, generally has its own tensors. The output projection is counted only if included in the question.

**The dangerous misconception:** clipping solves both exploding and vanishing gradients. **Why this is false:** it rescales large gradients and cannot reconstruct small long-range contributions. Orthogonal initialization and gating can improve propagation under appropriate conditions but do not prove stability for every sequence.

**The dangerous misconception:** gates are binary switches. **Why this is false:** sigmoid gates normally take continuous values in $(0,1)$ for finite inputs and act elementwise. Update-gate interpretation depends on the equation convention; reset can enter the candidate computation at different locations in different implementations.

**The dangerous misconception:** attention weights sum to one across all decoder steps. **Why this is false:** softmax usually normalizes across source positions separately for each query. Padding must be excluded from that denominator. Scores are not probabilities until normalized, and a context is a value-weighted sum, not a sum of keys unless keys and values coincide.

**The dangerous misconception:** soft attention always costs less than hard attention, or hard attention is always cheaper. **Why this is false:** actual cost depends on how locations are scored, selected and processed. Discrete training additionally requires accounting for the selection distribution. Neither method automatically provides faithful explanations.

**The dangerous misconception:** high BLEU proves an image caption is correct. **Why this is false:** reference overlap is sensitive to wording and incomplete reference coverage; it does not directly inspect the image. Equally, a low score alone cannot prove the caption is false.

## 8. Conclusion & Pedagogical Handoff

1. Recurrent transitions reuse parameters across sequence positions; architecture and bias conventions determine counts.
2. BPTT differentiates through the unrolled graph, and products of time-dependent Jacobians govern long-range gradient transmission.
3. LSTM and GRU gates modulate information flow; their additive paths improve the conditions for memory without guaranteeing it.
4. Attention scores, softmax normalization and value aggregation are distinct operations; hard selection changes the gradient-estimation problem.
5. Image captioning joins visual features, autoregressive generation, decoding, and evaluation. [[week-8-report|Week 8]] provisionally moves toward generative representations and probabilistic objectives; the sequence remains subject to the official syllabus.

## 9. Academic References & Annotated Literature

1. Hochreiter, S. and Schmidhuber, J. (1997). “Long Short-Term Memory.” *Neural Computation* 9(8), 1735–1780. [DOI: 10.1162/neco.1997.9.8.1735](https://doi.org/10.1162/neco.1997.9.8.1735). Contribution: introduces a gated memory architecture addressing long-term dependencies.
2. Pascanu, R., Mikolov, T. and Bengio, Y. (2013). “On the Difficulty of Training Recurrent Neural Networks.” *ICML*, PMLR 28, 1310–1318. [arXiv:1211.5063](https://arxiv.org/abs/1211.5063). Contribution: analyzes exploding and vanishing gradients and proposes norm clipping.
3. Cho, K. et al. (2014). “Learning Phrase Representations using RNN Encoder–Decoder for Statistical Machine Translation.” *EMNLP*, 1724–1734. [DOI: 10.3115/v1/D14-1179](https://doi.org/10.3115/v1/D14-1179). Contribution: introduces the GRU in an encoder–decoder framework.
4. Bahdanau, D., Cho, K. and Bengio, Y. (2015). “Neural Machine Translation by Jointly Learning to Align and Translate.” *ICLR*. [arXiv:1409.0473](https://arxiv.org/abs/1409.0473). Contribution: develops learned soft alignment for recurrent encoder–decoders.
5. Luong, M.-T., Pham, H. and Manning, C. D. (2015). “Effective Approaches to Attention-based Neural Machine Translation.” *EMNLP*, 1412–1421. [DOI: 10.18653/v1/D15-1166](https://doi.org/10.18653/v1/D15-1166). Contribution: compares dot, general and other alignment functions.
6. Xu, K. et al. (2015). “Show, Attend and Tell: Neural Image Caption Generation with Visual Attention.” *ICML*, PMLR 37, 2048–2057. [arXiv:1502.03044](https://arxiv.org/abs/1502.03044). Contribution: applies soft and stochastic hard visual attention to captioning.
7. Williams, R. J. (1992). “Simple Statistical Gradient-Following Algorithms for Connectionist Reinforcement Learning.” *Machine Learning* 8, 229–256. [DOI: 10.1007/BF00992696](https://doi.org/10.1007/BF00992696). Contribution: develops score-function policy-gradient estimators.
8. Papineni, K., Roukos, S., Ward, T. and Zhu, W.-J. (2002). “BLEU: a Method for Automatic Evaluation of Machine Translation.” *ACL*, 311–318. [DOI: 10.3115/1073083.1073135](https://doi.org/10.3115/1073083.1073135). Contribution: defines clipped n-gram precision and brevity penalty.
9. Vaswani, A. et al. (2017). “Attention Is All You Need.” *NeurIPS*. [arXiv:1706.03762](https://arxiv.org/abs/1706.03762). Contribution: introduces the Transformer and scaled dot-product attention.

## Appendix A — Computational Reproducibility (UV + Python)

From the repository root, run the complete program in Section 5 with `uv run python <script.py>`. The companion [[week-7-exam-notes|exam notes]] provide a second self-contained program and exact output for all worked examples. The arithmetic uses Python's standard library; no dataset, random initialization, GPU, or trained model is needed. Output precision is explicitly specified.

## Appendix B — Knowledge Graph Connections

**Upstream:** [[week-5-report|CNN features]] · [[week-6-report|Dense visual representations]].  
**Downstream:** [[week-8-report|Generative foundations]] · [[week-9-report|Transformer attention]].  
**Sibling:** [[week-7-exam-notes|Worked exam recipes]] · [[recurrent-neural-network]] · [[backpropagation-through-time]] · [[gated-recurrent-unit]] · [[encoder-decoder-attention]].
