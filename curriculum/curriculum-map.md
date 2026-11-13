---
title: "DL for Computer Vision: Curriculum Topic Map"
status: provisional
map: "[[Knowledge-Map]]"
---

# DL for Computer Vision: Curriculum Topic Map

> **Weeks 6–12 are provisional:** topics inferred from past papers; replace when official syllabus is available.

Weeks 1–4 follow the supplied syllabus and the existing report and exam-note headings; Week 5 follows its existing notes. The remaining sequence is an inference, not a recovered syllabus. Q1 covers weeks 1–4, Q2 covers weeks 5–8 plus earlier material, and ET covers all weeks with emphasis on 9–12. Exams can revisit earlier topics, so an ET occurrence alone does not establish its teaching week.

**Count method.** Each number counts manifest records whose `detected_concepts` contain at least one listed keyword, case-insensitively with punctuation and underscores normalized to spaces and whole-phrase matching. Q1/Q2/ET counts use the same rule; repeated exam questions are separate records, and one record may count in several topics. Broad or incomplete concept tags can overcount or miss matches; counts are screening estimates, not final primary classifications or unique-question totals. Source: [classification manifest](../sources/classification/classification-manifest.json). The JSON file contains the matching keywords and the same counts.

**Placement evidence.** Q2 contains many RNN, GRU and encoder–decoder attention questions and also tests focal loss, KL divergence, VAEs, GANs and metric learning, motivating Weeks 6–8. Transformer fundamentals also occur in Q2; their extension to ViT and DETR is grouped in Week 9, so primary classification must place Q2 questions within its permitted weeks (using Week 7 attention where appropriate). ET-only or ET-heavy diffusion, CLIP/BLIP, SAM and robustness clusters motivate later weeks. No date or exact sequence is established by these counts. The 2024T3 Q1 question 172 has no stem or detected concepts in its truncated source; it cannot support a topic assignment.

**Navigation:** [[Knowledge-Map|Knowledge Map]] · [Machine-readable taxonomy](topics.json)

| Week | Scope | Status |
| :--- | :--- | :--- |
| [[week-1-report\|Week 1]] | Visual signals and sampling | official |
| [[week-2-report\|Week 2]] | Classical features and segmentation | official |
| [[week-3-report\|Week 3]] | Neural networks and training | official |
| [[week-4-report\|Week 4]] | CNN fundamentals and classifiers | official |
| [[week-5-report\|Week 5]] | Advanced CNNs and detection | official |
| Week 6 | Dense detection, segmentation and motion | provisional |
| Week 7 | Recurrent models and attention | provisional |
| Week 8 | Generative and metric foundations | provisional |
| Week 9 | Transformers and vision | provisional |
| Week 10 | Advanced generation and style | provisional |
| Week 11 | Self-supervision and alignment | provisional |
| Week 12 | Multimodal models and robustness | provisional |

## Week 1 — Visual signals and sampling

| Topic ID | Topic | Manifest matches (Q1 / Q2 / ET) |
| :--- | :--- | ---: |
| `w1-vision-formation` | Vision and image formation | 12 (0 / 8 / 4) |
| `w1-representation` | Image representation and point operations | 42 (24 / 2 / 16) |
| `w1-filtering` | Spatial filtering and convolution | 122 (54 / 42 / 26) |
| `w1-frequency` | Frequency-domain images | 13 (8 / 0 / 5) |
| `w1-sampling` | Sampling and reconstruction | 20 (3 / 2 / 15) |

## Week 2 — Classical features and segmentation

| Topic ID | Topic | Manifest matches (Q1 / Q2 / ET) |
| :--- | :--- | ---: |
| `w2-edges` | Edges and differential operators | 114 (54 / 20 / 40) |
| `w2-corners-blobs` | Corners and blobs | 15 (13 / 0 / 2) |
| `w2-scale-space` | Scale space, pyramids and filter banks | 33 (19 / 0 / 14) |
| `w2-features` | Invariant features and geometric descriptors | 47 (29 / 2 / 16) |
| `w2-classical-segmentation` | Classical image segmentation | 29 (8 / 8 / 13) |
| `w2-visual-system` | Human visual system | 6 (4 / 0 / 2) |

## Week 3 — Neural networks and training

| Topic ID | Topic | Manifest matches (Q1 / Q2 / ET) |
| :--- | :--- | ---: |
| `w3-neural-networks` | Perceptrons and feedforward networks | 76 (15 / 34 / 27) |
| `w3-backprop` | Backpropagation and losses | 136 (38 / 45 / 53) |
| `w3-optimization` | Gradient descent and variants | 19 (9 / 1 / 9) |
| `w3-regularization` | Regularization and generalization | 17 (0 / 3 / 14) |
| `w3-training` | Initialization and normalization | 16 (2 / 10 / 4) |

## Week 4 — CNN fundamentals and classifiers

| Topic ID | Topic | Manifest matches (Q1 / Q2 / ET) |
| :--- | :--- | ---: |
| `w4-cnn-fundamentals` | CNN operations and spatial dimensions | 139 (29 / 70 / 40) |
| `w4-pooling-receptive-fields` | Pooling and receptive fields | 31 (8 / 14 / 9) |
| `w4-cnn-backprop` | CNN backpropagation | 3 (2 / 0 / 1) |
| `w4-alexnet` | AlexNet and early CNN classifiers | 55 (10 / 22 / 23) |
| `w4-vgg` | VGG and stacked convolutions | 9 (4 / 3 / 2) |

## Week 5 — Advanced CNNs and detection

| Topic ID | Topic | Manifest matches (Q1 / Q2 / ET) |
| :--- | :--- | ---: |
| `w5-inception` | Inception and bottleneck convolutions | 19 (0 / 18 / 1) |
| `w5-residual-networks` | Residual and connected CNN architectures | 15 (0 / 13 / 2) |
| `w5-efficient-cnns` | Efficient convolutional networks | 36 (0 / 28 / 8) |
| `w5-transfer` | Transfer learning and fine-tuning | 11 (0 / 8 / 3) |
| `w5-interpretability` | CNN visualization and interpretability | 16 (0 / 12 / 4) |
| `w5-two-stage-detection` | Two-stage detection and R-CNN | 33 (0 / 25 / 8) |
| `w5-yolo` | Single-stage detection and YOLO | 70 (6 / 45 / 19) |

## Week 6 — Dense detection, segmentation and motion

> **Provisional:** topics inferred from past papers; replace when official syllabus is available.

| Topic ID | Topic | Manifest matches (Q1 / Q2 / ET) |
| :--- | :--- | ---: |
| `w6-dense-detection` | Dense detectors and focal loss | 12 (0 / 8 / 4) |
| `w6-detector-boxes` | Detection losses, boxes and matching | 26 (0 / 20 / 6) |
| `w6-feature-pyramids` | Multiscale feature pyramids | 6 (0 / 3 / 3) |
| `w6-segmentation` | Semantic and instance segmentation | 14 (0 / 9 / 5) |
| `w6-segnet` | SegNet encoder-decoder segmentation | 59 (0 / 40 / 19) |
| `w6-motion` | Optical flow and image registration | 3 (2 / 0 / 1) |

## Week 7 — Recurrent models and attention

> **Provisional:** topics inferred from past papers; replace when official syllabus is available.

| Topic ID | Topic | Manifest matches (Q1 / Q2 / ET) |
| :--- | :--- | ---: |
| `w7-rnn-basics` | Recurrent networks and sequence architectures | 101 (0 / 86 / 15) |
| `w7-rnn-training` | Recurrent training and gradient dynamics | 16 (2 / 9 / 5) |
| `w7-gated-rnn` | LSTM and GRU gating | 28 (0 / 24 / 4) |
| `w7-sequence-attention` | Encoder-decoder attention | 46 (0 / 42 / 4) |
| `w7-hard-soft-attention` | Soft and hard attention | 14 (0 / 10 / 4) |
| `w7-captioning` | Recurrent image captioning and evaluation | 37 (0 / 13 / 24) |

## Week 8 — Generative and metric foundations

> **Provisional:** topics inferred from past papers; replace when official syllabus is available.

| Topic ID | Topic | Manifest matches (Q1 / Q2 / ET) |
| :--- | :--- | ---: |
| `w8-probabilistic-generative` | Generative models and KL divergence | 17 (0 / 13 / 4) |
| `w8-autoencoders` | Autoencoder representations | 27 (8 / 5 / 14) |
| `w8-vae` | Variational autoencoders | 30 (0 / 8 / 22) |
| `w8-gan-basics` | GAN objectives and equilibrium | 15 (0 / 5 / 10) |
| `w8-metric-learning` | Metric learning and face verification | 10 (0 / 5 / 5) |
| `w8-generative-evaluation` | Generative model evaluation | 6 (0 / 1 / 5) |

## Week 9 — Transformers and vision

> **Provisional:** topics inferred from past papers; replace when official syllabus is available.

| Topic ID | Topic | Manifest matches (Q1 / Q2 / ET) |
| :--- | :--- | ---: |
| `w9-self-attention` | Self-attention and QKV projections | 29 (0 / 5 / 24) |
| `w9-transformer-blocks` | Transformer encoders and decoders | 23 (0 / 2 / 21) |
| `w9-positional-encoding` | Token and positional representations | 8 (0 / 1 / 7) |
| `w9-vit` | Vision transformers | 8 (0 / 0 / 8) |
| `w9-detr` | Transformer object detection | 2 (0 / 0 / 2) |

## Week 10 — Advanced generation and style

> **Provisional:** topics inferred from past papers; replace when official syllabus is available.

| Topic ID | Topic | Manifest matches (Q1 / Q2 / ET) |
| :--- | :--- | ---: |
| `w10-progressive-gan` | Progressive and style-based GANs | 4 (0 / 0 / 4) |
| `w10-gan-pathologies` | GAN diversity and failure modes | 7 (0 / 2 / 5) |
| `w10-vq-vae` | Vector-quantized autoencoders | 11 (5 / 0 / 6) |
| `w10-diffusion-forward` | Forward diffusion and noise schedules | 9 (0 / 0 / 9) |
| `w10-diffusion-reverse` | Reverse diffusion and guidance | 7 (0 / 0 / 7) |
| `w10-style-transfer` | Neural style transfer | 3 (0 / 2 / 1) |

## Week 11 — Self-supervision and alignment

> **Provisional:** topics inferred from past papers; replace when official syllabus is available.

| Topic ID | Topic | Manifest matches (Q1 / Q2 / ET) |
| :--- | :--- | ---: |
| `w11-self-supervised` | Self-supervised objectives and pretext tasks | 17 (0 / 0 / 17) |
| `w11-contrastive` | Contrastive representation learning | 5 (0 / 0 / 5) |
| `w11-few-shot` | Few-shot and low-data adaptation | 2 (0 / 0 / 2) |
| `w11-clip` | CLIP and image-text contrastive alignment | 9 (0 / 0 / 9) |
| `w11-vision-language-tasks` | Vision-language tasks and retrieval | 18 (0 / 2 / 16) |

## Week 12 — Multimodal models and robustness

> **Provisional:** topics inferred from past papers; replace when official syllabus is available.

| Topic ID | Topic | Manifest matches (Q1 / Q2 / ET) |
| :--- | :--- | ---: |
| `w12-blip` | BLIP architecture and objectives | 24 (0 / 0 / 24) |
| `w12-promptable-segmentation` | Promptable segmentation and SAM | 3 (0 / 0 / 3) |
| `w12-adversarial-robustness` | Adversarial examples and attacks | 4 (0 / 0 / 4) |
| `w12-foundation-models` | Multimodal foundation models and conditioning | 6 (0 / 0 / 6) |
| `w12-multimodal-decoding` | Multimodal generation and decoding | 10 (0 / 2 / 8) |
