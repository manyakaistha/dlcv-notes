# CLIP alignment

CLIP learns a shared image–text embedding space from paired images and captions. Separate image and text encoders project each modality into a common dimension, and normalized embeddings produce a matrix of pairwise cosine similarities. The training objective averages row-wise image-to-text and column-wise text-to-image cross-entropies, using the paired diagonal entry as the target in each direction. This is simultaneously a contrastive objective and a cross-entropy objective. At inference, encoded text prompts can act as candidate class descriptions, allowing zero-shot image classification without labelled target-class examples. Text–image retrieval instead ranks candidate items in the other modality. Similarity is sensitive to data, prompt wording, and candidate selection; it is not automatically a calibrated probability or proof of localization.

## Why it matters here

The week tests zero-shot classification, the symmetric objective, temperature, and the distinction between a dot product and cosine.

**Appears in:** [[week-11-report]] · [[week-11-exam-notes]] · [[week-11-questions]]

## Related

[[infonce-loss]] · [[vision-language-retrieval]]
