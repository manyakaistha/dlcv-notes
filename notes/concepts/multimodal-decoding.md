# Multimodal decoding

Multimodal decoding generates a sequence while conditioning on nontextual context, such as image features. An image-grounded autoregressive decoder factorizes the conditional probability of a caption as the product of next-token probabilities given the image and previous tokens. Causal self-attention prevents access to future text; cross-attention can provide access to all encoded image tokens. During teacher-forced training the prefix comes from the reference; during inference it comes from previous predictions. Greedy decoding, beam search, and sampling select outputs differently and have different cost and diversity properties.

**Why it matters here:** BLIP diagram questions distinguish a decode token, causal self-attention, and visual cross-attention. A fluent caption can still hallucinate visual content, so sequence likelihood alone does not establish grounding.

**Appears in:** [[week-12-report]] · [[week-12-exam-notes]] · [[week-12-questions]]

## Related

[[blip-pretraining]] · [[promptable-segmentation]] · [[adversarial-examples]]
