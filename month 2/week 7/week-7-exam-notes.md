---
title: "Week 7 Exam Notes: Recurrence and Attention"
week: 7
month: 2
status: provisional
date: 2026-11-14
report: "[[week-7-report]]"
map: "[[Knowledge-Map]]"
tags:
  - dlcv/week-07
  - dlcv/exam
---

# Week 7 Exam Notes: Recurrence and Attention

> **Provisional: topics inferred from past papers; replace when the official syllabus is available.**

**Navigation:** [[week-7-report|Week 7 Report]] · [[Knowledge-Map|Knowledge Map]] · [[recurrent-neural-network]] · [[gated-recurrent-unit]] · [[encoder-decoder-attention]]

## Fast recall: sequence models

- A recurrent hidden state $h_t=\phi(W_{xh}x_t+W_{hh}h_{t-1}+b)$ summarizes a prefix; parameters are shared over time.
- One-to-many: image to caption. Many-to-one: sequence to class. Aligned many-to-many: per-frame tagging. Encoder–decoder many-to-many: translation with potentially different lengths.
- A bidirectional encoder concatenates forward and backward context. Future context makes it unsuitable for strictly causal online inputs unless latency permits it.
- Unrolling increases computation with sequence length, but does not multiply recurrent parameter count by time steps.
- Output logits require an output head if the task demands a vocabulary or class distribution. Count that head separately.
- Mask padded time steps in both the objective and any attention normalization.

## Parameter-count recipes

For input width $d$, hidden width $h$, output width $k$, and column-vector weights, a vanilla cell with one bias has $hd+h^2+h$ parameters. The input matrix has shape `[h,d]`, recurrent matrix `[h,h]`, and bias `[h]`. Add $kh+k$ for a biased output head. Without biases, omit the corresponding terms. With two stored biases per transition, count both. A question that asks for weights only excludes biases.

For a stacked network, the input width to layer one is the data width; each later unidirectional layer receives the previous layer's hidden width. Add the separate count of each layer and the head. A bidirectional layer with separate parameters has two directions, and a subsequent layer normally receives twice the per-direction output width. For variable-length sequences, none of these counts depends on how many tokens are unrolled.

**Worked example:** $d=3$, $h=4$ gives $4\cdot3+4\cdot4+4=32$ parameters in a single-bias RNN cell. Add a second RNN layer of width 5, receiving width 4: $5\cdot4+5\cdot5+5=50$. A biased two-class head contributes $2\cdot5+2=12$. The total is $32+50+12=94$. The first cell's weights are not counted again for every time step.

**Gated cells:** with the same $d,h$ and one combined bias per gate, a standard LSTM without peepholes or projection has $4(hd+h^2+h)$, and a GRU has $3(hd+h^2+h)$. For $d=3,h=4$ these are 128 and 96. A GRU implementation storing both input and recurrent biases has $3(hd+h^2+2h)$ instead; LSTM analogously has $4(hd+h^2+2h)$. Separate output projections and learned initial states are additional parameters. LSTM projections, peepholes and framework-specific gate layouts change the formula.

## Gradients, BPTT and stability

- The loss can sum or average token losses. BPTT adds derivatives from every use of a shared parameter.
- $\partial h_t/\partial h_s=J_t\cdots J_{s+1}$, where $J_j=\operatorname{diag}(\phi'(a_j))W_{hh}$. Small repeated effects can vanish; large ones can explode.
- Matrix eigenvalues alone do not determine finite-time gradient norms in a nonlinear, time-dependent system. Saturation of sigmoid or tanh can shrink derivatives.
- Global norm clipping uses $g' = g\min(1,c/\|g\|_2)$ and addresses a large gradient, not a vanished one. Optimizer state can make the actual parameter update differ from the clipped gradient.
- Orthogonal recurrent initialization preserves linear norms at initialization, but nonlinear derivatives and subsequent updates can change propagation.
- Truncated BPTT detaches the forward state at a boundary: the state can carry history forward, but gradients do not propagate across that boundary.
- Gating can help preserve an additive path; it does not mathematically guarantee that every relevant gradient survives.

**Clipping example:** a gradient `(3, 4)` has Euclidean norm 5. With threshold 2, multiply by $2/5$ to obtain `(1.2, 1.6)`; its norm is 2. If the threshold is at least 5, no scaling occurs. Clipping each coordinate independently is a different operation and generally changes the direction.

## LSTM and GRU: formulas and traps

An LSTM uses forget $f_t$, input $i_t$, candidate $\tilde c_t$, and output $o_t$:

$$c_t=f_t\odot c_{t-1}+i_t\odot\tilde c_t,\qquad h_t=o_t\odot\tanh(c_t).$$

Each gate normally applies a sigmoid to an affine function of current input and previous hidden state, while the candidate uses tanh. Forget retains old cell content; input admits candidate content; output exposes cell content. A sigmoid gate is a continuous vector, not an all-or-nothing Boolean switch. The cell state and hidden state have distinct roles. Holding gate values fixed isolates a direct cell path with derivative $f_t$; full derivatives include the gates' dependence on past states.

For one GRU convention,

$$\begin{aligned}
z_t&=\sigma(W_zx_t+U_zh_{t-1}+b_z),\quad r_t=\sigma(W_rx_t+U_rh_{t-1}+b_r),\\
\tilde h_t&=\tanh(W_nx_t+U_n(r_t\odot h_{t-1})+b_n),\\
h_t&=(1-z_t)\odot h_{t-1}+z_t\odot\tilde h_t.
\end{aligned}$$

Under this convention $z_t=0$ retains the previous state and $z_t=1$ selects the candidate; these are limiting interpretations of sigmoid gates. Some sources define the complementary update convention. Reset controls the contribution of old state to the candidate, and some implementations place reset after the recurrent affine transform. Read the supplied diagram or formula before labeling gates. GRU has one exposed state; a conventional LSTM has a separate cell state.

## Attention: score → normalize → aggregate

For decoder query $s$ and encoder key $k_i$, compute scores $e_i$, then $\alpha_i=\exp(e_i)/\sum_j\exp(e_j)$, then context $c=\sum_i\alpha_i v_i$. Keys determine matching; values are what is aggregated. If a problem uses encoder hidden states as both keys and values, they coincide, but this is not a general rule. Attention weights are nonnegative and sum to one across valid source positions **for each query**. Mask padding before softmax.

- **Dot:** $e_i=s^\top k_i$; dimensions must match.
- **Scaled dot:** $e_i=s^\top k_i/\sqrt{d_k}$; use scaling only when specified.
- **General/bilinear:** $e_i=s^\top Wk_i$.
- **Additive:** $e_i=v_a^\top\tanh(W_ss+W_kk_i+b)$, with learned projections and vector.

**Worked dot-product example:** query `(1,0)`, keys `(2,0)` and `(1,0)`, values `(1,0)` and `(0,2)`. Scores are `(2,1)`. Subtract the maximum before exponentiating: softmax is approximately `(0.731059,0.268941)`. The context is approximately `(0.731059,0.537883)`. Taking the weighted sum of scores or keys instead of the specified values answers a different question. Equal shifts of all scores do not change softmax.

**Additive recipe:** evaluate the query projection and each key projection, add the bias, apply tanh elementwise, then take the dot product with $v_a$; only then normalize across positions. Keep the intermediate width consistent. For scalar $s=k_1=1$, $k_2=0$, $W_s=W_k=v_a=1$ and zero bias, the scores are $\tanh(2)$ and $\tanh(1)$. Their softmax weights are verified below. A large score indicates greater relative weight for the same query; it does not establish causal explanatory importance.

## Soft, hard and self-attention

Soft attention takes a differentiable weighted sum over candidate values. Hard attention selects or samples a discrete location; the sample operation does not have an ordinary useful pathwise derivative. REINFORCE estimates a gradient of an expected reward using $R\nabla\log p(z)$, with an appropriate action-independent baseline for variance reduction. Direct parameter dependence of the reward requires an additional derivative. Hard selection can reduce processing of values but may still require scoring every location; actual inference cost depends on the implementation.

Cross-attention uses decoder queries and source/image keys and values. Self-attention derives all three from the same sequence. Standard Transformers replace recurrent transitions with attention and feed-forward blocks, and need positional information; causal masks block access to future target tokens. Parallel training over tokens does not make autoregressive generation parallel across generated steps. Attention is not identical to recurrence, and a large attention weight is not necessarily a faithful explanation.

## Captioning and BLEU

A CNN can produce a global image vector or a spatial grid of feature vectors. A decoder models $p(y_{1:T}\mid I)=\prod_t p(y_t\mid y_{<t},I)$. Teacher forcing uses the reference prefix during training; inference uses generated words. Start and end tokens delimit generation. Greedy decoding selects one locally best token; beam search keeps multiple prefixes and is sensitive to length normalization. Neither guarantees a correct or visually grounded caption.

BLEU uses clipped modified $n$-gram precisions $p_n$ and a brevity penalty:

$$\operatorname{BLEU}=\operatorname{BP}\exp\left(\sum_{n=1}^N w_n\log p_n\right),\quad
\operatorname{BP}=1\; (c>r),\quad \operatorname{BP}=e^{1-r/c}\; (c\le r).$$

Clipping limits the credit for a repeated candidate n-gram to its maximum count in the references. Corpus BLEU aggregates counts first; it is not the mean of sentence scores. With unsmoothed precision zero, BLEU is zero. Tokenization, reference choice, $N$, and smoothing affect results. BLEU measures text overlap rather than visual truth; an accurate paraphrase can score poorly and a generic caption can score well.

**Worked BLEU-2 arithmetic:** if $p_1=3/4$, $p_2=1/3$, equal weights, candidate length $c=4$ and selected reference length $r=5$, the penalty is $e^{-1/4}$ and BLEU is $e^{-1/4}\sqrt{(3/4)(1/3)}=0.389400$ to six decimals. These are stipulated precision counts for an arithmetic example, not a reported model result.

## Executable verification

Run this complete program with `uv run python <script.py>` from the repository root. It verifies the numerical examples above, including the scalar additive attention and clipping calculation.

```python
import math

d, h = 3, 4
cell = h * d + h * h + h
second = 5 * 4 + 5 * 5 + 5
head = 2 * 5 + 2
print("RNN:", cell)
print("two-layer:", cell + second + head)
print("LSTM:", 4 * cell)
print("GRU:", 3 * cell)

def softmax(scores):
    m = max(scores)
    exps = [math.exp(s - m) for s in scores]
    return [x / sum(exps) for x in exps]

weights = softmax([2.0, 1.0])
values = [(1.0, 0.0), (0.0, 2.0)]
context = [sum(w * v[j] for w, v in zip(weights, values)) for j in range(2)]
print("attention:", *(f"{x:.6f}" for x in weights),
      "context:", *(f"{x:.6f}" for x in context))
additive = softmax([math.tanh(2), math.tanh(1)])
print("additive:", *(f"{x:.6f}" for x in additive))
gradient = [3.0, 4.0]
scale = min(1.0, 2.0 / math.hypot(*gradient))
print("clipped:", *(f"{scale*x:.1f}" for x in gradient))
bleu = math.exp(1 - 5 / 4) * math.sqrt((3 / 4) * (1 / 3))
print("BLEU:", f"{bleu:.6f}")
```

```text
RNN: 32
two-layer: 94
LSTM: 128
GRU: 96
attention: 0.731059 0.268941 context: 0.731059 0.537883
additive: 0.550436 0.449564
clipped: 1.2 1.6
BLEU: 0.389400
```

The printed quantities verify arithmetic for explicitly stated conventions; they are not measured accuracy, performance, or claims about trained models. See [[week-7-report|the report]] for derivations, limitations, and references.
