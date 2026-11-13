# Promptable segmentation

Promptable segmentation predicts a spatial mask from an image and a task prompt, such as a foreground point, a negative point, a box, or a previous mask. Segment Anything (SAM) uses an image encoder, a prompt encoder, and a mask decoder; the image embedding can be reused across interactions. An ambiguous prompt can admit several valid masks, so multiple proposals and a predicted quality score help the user select and refine the intended region. The training data engine used model-assisted annotation to build a large, diverse mask dataset.

**Why it matters here:** SAM's transfer to unfamiliar objects can accelerate annotation, but zero-shot generalization is empirical rather than a guarantee. A spatial mask is not automatically a semantic category label and still needs task-specific evaluation.

**Appears in:** [[week-12-report]] · [[week-12-exam-notes]] · [[week-12-questions]]

## Related

[[blip-pretraining]] · [[adversarial-examples]] · [[multimodal-decoding]]
