---
title: "Gated Recurrent Unit"
status: provisional
---

# Gated Recurrent Unit

A gated recurrent unit (GRU) is a recurrent cell that uses update and reset gates to control how a hidden state incorporates a candidate state. In one convention, $z_t=\sigma(W_zx_t+U_zh_{t-1}+b_z)$, $r_t=\sigma(W_rx_t+U_rh_{t-1}+b_r)$, $\tilde h_t=\tanh(W_nx_t+U_n(r_t\odot h_{t-1})+b_n)$, and $h_t=(1-z_t)\odot h_{t-1}+z_t\odot\tilde h_t$. The update gate interpolates elementwise between old and candidate states; the reset gate modulates the old state's role in constructing the candidate. Some texts reverse the update convention, and implementations can place the reset operation differently.

## Why it matters here

The additive interpolation provides a direct route for state and gradient propagation, although it does not guarantee long-range learning. Unlike a standard LSTM, the GRU has no separate cell state. With input width $d$, hidden width $h$, and one bias per gate, its three gates have $3(hd+h^2+h)$ parameters. Frameworks storing separate input and recurrent biases have additional bias parameters. Exam diagrams must be interpreted using their actual equations rather than gate names alone.

**Appears in:** [[week-7-report]] · [[week-7-exam-notes]]

## Related

[[recurrent-neural-network]] · [[backpropagation-through-time]] · [[encoder-decoder-attention]]
