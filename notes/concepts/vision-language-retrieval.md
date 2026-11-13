# Vision–language retrieval

Vision–language retrieval ranks items in one modality in response to a query in another. In text-to-image retrieval a text encoder maps a query into an embedding and candidate image embeddings are ranked by a compatible similarity; image-to-text retrieval reverses these roles. Dual encoders permit candidate vectors to be computed in advance, making large-scale search practical, though approximate indexes may miss exact neighbours. Evaluation must specify the candidate pool and relevance labels, since several captions or images can be valid matches. Retrieval differs from visual question answering, which returns an answer conditioned on an image and question, and from text-conditioned object detection, which must also localize objects. A global similarity score alone does not establish spatial grounding.

## Why it matters here

The examination groups retrieval, visual question answering and text-conditioned detection as vision–language tasks while requiring their different outputs to be understood.

**Appears in:** [[week-11-report]] · [[week-11-exam-notes]] · [[week-11-questions]]

## Related

[[clip-alignment]] · [[contrastive-learning]]
