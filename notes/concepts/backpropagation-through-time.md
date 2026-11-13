---
title: "Backpropagation Through Time"
status: provisional
---

# Backpropagation Through Time

Backpropagation through time (BPTT) applies reverse-mode differentiation to an unrolled recurrent computation. Each time step uses the same parameter tensors, so their gradient is the sum of contributions from all uses. For hidden states $h_t$, the influence of an earlier state on a later one involves the ordered Jacobian product $\partial h_t/\partial h_s=J_t\cdots J_{s+1}$. Repeated contraction can make long-range gradients vanish, while repeated expansion can make them explode. Nonlinear activation derivatives, changing state-dependent Jacobians and matrix geometry all affect this behavior; the recurrent weight matrix's eigenvalues alone do not fully determine finite-time dynamics.

## Why it matters here

Recurrent captioning and sequence classification rely on credit assignment across time. Global norm clipping limits an excessively large gradient, but cannot restore a vanished one; gated cells and careful initialization can help propagation without guaranteeing it. Truncated BPTT detaches the state at chosen boundaries, reducing memory and gradient horizon. The forward state can still carry information beyond the truncation boundary, even though its gradient history is cut. Padding must be masked when aggregating token losses.

**Appears in:** [[week-7-report]] · [[week-7-exam-notes]]

## Related

[[recurrent-neural-network]] · [[gated-recurrent-unit]] · [[encoder-decoder-attention]]
