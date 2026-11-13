---
title: "Recurrent Neural Network"
status: provisional
---

# Recurrent Neural Network

A recurrent neural network (RNN) applies a shared state transition to successive elements of an ordered sequence. A vanilla cell maps input $x_t\in\mathbb R^d$ and previous state $h_{t-1}\in\mathbb R^h$ to $h_t=\phi(W_{xh}x_t+W_{hh}h_{t-1}+b)$. The hidden state is a learned summary of the prefix, and an output head can map each state, or only the last state, to task predictions. The same cell parameters are reused across time. With one bias and no output head, it has $hd+h^2+h$ parameters, independent of sequence length. Different layers or directions normally use distinct parameters. A bidirectional encoder combines forward and backward states but needs access to future input positions.

## Why it matters here

Recurrent networks connect image features to sequences such as captions and enable sequence classification and alignment. Exam questions distinguish one-to-many, many-to-one and many-to-many mappings and require counting shared weights without multiplying by the number of time steps. The information stored in a fixed-size hidden vector can be incomplete, motivating gated cells and attention.

**Appears in:** [[week-7-report]] · [[week-7-exam-notes]]

## Related

[[backpropagation-through-time]] · [[gated-recurrent-unit]] · [[encoder-decoder-attention]]
