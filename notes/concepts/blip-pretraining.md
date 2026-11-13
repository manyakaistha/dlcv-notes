# BLIP pretraining

BLIP is a vision–language pretraining framework combining an image encoder and text transformer configured for unimodal encoding, image-grounded encoding, and image-grounded generation. Image–text contrastive learning aligns separately computed image and text embeddings, while image–text matching classifies a fused pair. A language-modeling objective trains a causal decoder to predict text conditioned on visual features and the preceding tokens. BLIP also uses a captioner and filter to improve noisy web image–text training data. Shared weights do not make the modes identical: their attention masks, conditioning paths, and task tokens differ.

**Why it matters here:** Past-paper questions ask which diagram components implement self-attention, cross-attention, classification prompts and the different objectives. Trace information flow before matching a component to a diagram number.

**Appears in:** [[week-12-report]] · [[week-12-exam-notes]] · [[week-12-questions]]

## Related

[[promptable-segmentation]] · [[adversarial-examples]] · [[multimodal-decoding]]
