---
title: "Encoder–Decoder Attention"
status: provisional
---

# Encoder–Decoder Attention

Encoder–decoder attention constructs a query-dependent context from a collection of encoded source representations. For decoder query $q_t$, source keys $k_i$ and values $v_i$, an alignment function produces scores $e_{t,i}=\operatorname{score}(q_t,k_i)$. A softmax over valid source positions gives $\alpha_{t,i}=e^{e_{t,i}}/\sum_j e^{e_{t,j}}$, and the context is $c_t=\sum_i\alpha_{t,i}v_i$. Dot-product scoring requires compatible query and key dimensions; additive scoring learns projections and a nonlinear compatibility function. The weights sum to one for each query, and padding must be masked before normalization. Keys and values may be the same vectors, but are distinct roles in the general formulation.

## Why it matters here

A caption decoder can attend to CNN image regions differently for each generated word, avoiding exclusive reliance on a single fixed image summary. Soft attention computes a differentiable weighted sum; stochastic hard attention selects a discrete location and requires a suitable gradient estimator for the selection policy. Exam calculations must distinguish scores, normalized weights and the final value-weighted context. Attention weights can help diagnose behavior but are not by themselves proof of causal explanation.

**Appears in:** [[week-7-report]] · [[week-7-exam-notes]]

## Related

[[recurrent-neural-network]] · [[gated-recurrent-unit]] · [[backpropagation-through-time]]
