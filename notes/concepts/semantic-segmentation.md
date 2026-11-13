---
title: "Semantic segmentation"
status: provisional
---

# Semantic segmentation

Semantic segmentation assigns a category to each image location. A model commonly outputs logits with shape `[B, C, H, W]` for a batch of images and $C$ classes; softmax and an argmax over the class dimension yield a class map. The spatial resolution may require upsampling to match the target. Pixelwise cross-entropy can supervise labeled pixels, while class-wise intersection over union provides a complementary evaluation measure. Ignore masks and absent-class conventions must be specified when computing a metric.

## Why it matters here

Semantic labels identify where a category appears but do not intrinsically separate two objects of that category. Instance segmentation supplies per-object identities and masks, while box detection supplies coarser localization. Encoder–decoder networks such as SegNet reconstruct spatial predictions from lower-resolution features.

**Appears in:** [[week-6-report]] · [[week-6-exam-notes]] · [[week-06-questions]]

## Related

[[focal-loss]] · [[intersection-over-union]] · [[feature-pyramid-network]]
