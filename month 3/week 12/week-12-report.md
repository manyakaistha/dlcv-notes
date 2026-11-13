---
title: "Vision–Language Foundation Models, Promptable Segmentation, and Adversarial Robustness"
week: 12
month: 3
status: provisional
date: 2026-11-14
prev: "[[week-11-report|Week 11]]"
map: "[[Knowledge-Map]]"
tags:
  - dlcv/week-12
  - dlcv/multimodal
  - dlcv/robustness
concepts:
  - "[[blip-pretraining]]"
  - "[[promptable-segmentation]]"
  - "[[adversarial-examples]]"
  - "[[multimodal-decoding]]"
---

# Vision–Language Foundation Models, Promptable Segmentation, and Adversarial Robustness

> **Week 12 Review Article — Month 3 / Week 12**  
> Topics inferred from past papers; replace when the official syllabus is available.

**Navigation:** ← [[week-11-report|Week 11]] · [[Knowledge-Map|Knowledge Map]] · [[week-12-questions|Question bank]] · [[week-12-exam-notes|Exam notes]]

## Abstract

Visual foundation models reuse learned representations across tasks by conditioning computation on language, prompts, or previous output. BLIP combines contrastive alignment, image–text matching, and image-conditioned language modeling in a multimodal mixture of encoder and decoder configurations. Segment Anything separates image encoding from prompt encoding and mask decoding to make interactive segmentation reusable across object categories. Adversarial attacks probe a different property: local sensitivity of predictions to bounded input perturbations. FGSM follows the sign of the loss gradient once, whereas projected gradient descent iterates bounded updates. Together these methods distinguish transfer, generation, localization, and worst-case robustness; none alone establishes the others.

## Keywords

BLIP, image–text contrastive learning, image–text matching, causal attention, SAM, adversarial perturbations, FGSM, PGD

## 1. Introduction and syllabus

The provisional taxonomy contains five clusters: BLIP architecture and objectives; promptable segmentation and SAM; adversarial examples and attacks; multimodal foundation models and conditioning; and multimodal generation and decoding. The question bank emphasizes the relationships among attention modules, special tokens, and losses in a BLIP architecture diagram, the generalization and annotation benefits of SAM, and the calculation and classification of attacks. Understanding the task interface is more useful than memorizing diagram numbers: numbers identify a particular figure, while functions generalize across diagrams.

A foundation model is broadly pretrained and then adapted or prompted for multiple downstream tasks. This is a description of a training and reuse strategy, not a theorem that every task or domain will work. A visual backbone produces image representations; a text backbone represents language; a fusion mechanism allows language to refer to image content. The correct evaluation depends on the requested task. Retrieval measures ranking, matching measures compatibility, generation measures a conditional sequence distribution, and segmentation measures a spatial mask. A model can succeed at one without having a guaranteed capability at another.

## 2. Theoretical foundations

### 2.1 Image–text representation and attention

Let an image encoder map image $I$ to a sequence $V=(v_1,\dots,v_M)$, and let a tokenizer map text to $T=(t_1,\dots,t_N)$. Given hidden states $H$, attention creates queries, keys and values through learned projections. For a single head,

$$Q=HW_Q,\quad K=HW_K,\quad V'=HW_V,\qquad
\operatorname{Attn}(Q,K,V')=\operatorname{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}+M\right)V'.$$

The additive mask $M$ excludes forbidden attention links by assigning them negative infinity before softmax. In self-attention, queries, keys and values originate from the same sequence; in cross-attention they can originate from different modalities. Image-grounded text commonly uses text queries and visual keys and values. The resulting update is a weighted combination of visual information whose weights vary with the text query. Cross-attention is not the same thing as concatenating an image feature to every token: it provides a learned, token-specific selection over image features.

Bidirectional self-attention permits each non-padding text token to attend to the entire provided text. A causal mask permits a position to use only the current and previous positions. The language-modeling shift matters: the state based on a prefix predicts the next token; a causal mask alone does not excuse feeding the target token unshifted as an input to its own prediction. Image tokens are normally all available when generating a caption; restricting future *text* does not imply hiding the image.

### 2.2 BLIP and its three objectives

BLIP's multimodal mixture of encoder–decoder architecture uses an image encoder together with a text transformer in different modes. The unimodal text encoder and image encoder provide independently computed embeddings for contrastive alignment. The image-grounded text encoder inserts cross-attention to fuse text and image representations for matching. The image-grounded text decoder uses causal self-attention together with image cross-attention for language generation. Some parameters are shared between the text configurations; their attention masks and special tokens specify the mode. A special token such as `[ENC]`, `[DEC]`, or `[CLS]` is a learned input symbol whose meaning comes from the architecture and training convention, rather than an ordinary English word.

For a minibatch of $B$ matched pairs, denote normalized representations by $z_i^I,z_i^T$ and temperature by $\tau>0$. One image-to-text contrastive term is

$$\mathcal L_{I\to T}=-\frac1B\sum_i\log\frac{\exp((z_i^I)^\top z_i^T/\tau)}{\sum_j\exp((z_i^I)^\top z_j^T/\tau)}.$$

A symmetric text-to-image term exchanges modalities; their mean is a common image–text contrastive loss, $\mathcal L_{ITC}$. The denominator contains candidate texts for an image, so reducing the loss improves the relative score of the paired text. Temperature changes the sharpness of the distribution and gradient scale. A batch can include false negatives: two semantically valid captions for the same visual content can be treated as mismatches by a simple one-positive construction. Contrastive similarity is not itself an image-grounded token-by-token explanation.

Image–text matching (ITM) uses a joint encoder and a binary classification head. With match label $m\in\{0,1\}$ and predicted probability $p_\theta(m=1\mid I,T)$, the binary cross-entropy is

$$\mathcal L_{ITM}=-m\log p_\theta-(1-m)\log(1-p_\theta).$$

The classifier must decide whether the *pair* matches after cross-modal interaction. Hard negative pairs can make this decision informative, but errors and semantically valid alternatives mean that a negative sampling rule must be interpreted carefully. An ITC score and an ITM score answer related but distinct questions: the first compares separately encoded embeddings; the second scores a fused pair. In retrieval, a practical division is fast dual-encoder candidate search followed by more expensive pairwise reranking.

The image-conditioned language-modeling objective is

$$p_\theta(T\mid I)=\prod_{t=1}^{N}p_\theta(t_t\mid t_{<t},I),\qquad
\mathcal L_{LM}=-\sum_{t=1}^{N}\log p_\theta(t_t\mid t_{<t},I).$$

Training often uses teacher forcing, supplying the reference prefix. At inference the model supplies its own previously generated tokens; an early mistake can affect later predictions. The total pretraining loss combines ITC, ITM, and LM terms; relative weights and training details are implementation-specific. The original BLIP also introduces captioning and filtering of noisy web image–text data (CapFilt): a captioner generates synthetic captions and a filter removes noisy pairs. This is data bootstrapping, not an assurance that synthetic captions are true.

### 2.3 Multimodal decoding and conditioning

For decoding, begin with an appropriate start or task prompt and compute a distribution over the next token. Greedy decoding repeatedly selects the locally most probable token. Beam search retains a fixed number of candidate prefixes under an accumulated score, often with length normalization. Sampling draws from a distribution, potentially modified by temperature, top-$k$, or nucleus truncation. These choices trade determinism, search cost, diversity, and potential degeneration. Beam search is approximate and a wider beam does not guarantee a better human judgment of captions. A stopping token, maximum length, and consistent text preprocessing are part of a reproducible decoding specification.

The distinction between attention visibility and modality access is central. A decoder's masked self-attention sees a prefix, while its cross-attention can see the image. A bidirectional encoder can see all input words because it is encoding observed text, not predicting each unseen next word. A `[CLS]` representation is useful for classification; a decode prompt initializes generation; an encode prompt indicates the joint encoding mode. Special token names and exact sharing vary across implementations, so the actual model's documentation takes priority over a generic mnemonic.

### 2.4 Promptable segmentation and SAM

A segmentation mask is a spatial prediction $m\in\{0,1\}^{H\times W}$, or a real-valued probability map before thresholding. SAM formulates segmentation as predicting a valid mask conditioned on an image and prompt. Prompts may include foreground or background points, bounding boxes, and mask inputs. Sparse and dense prompts have different representations. An image encoder computes a reusable image embedding; a prompt encoder represents the interaction; a lightweight mask decoder combines them and predicts masks and quality estimates. Reusing an image embedding makes multiple prompt interactions cheaper than rerunning the large image encoder for each click, but overall resource requirements still depend on implementation and hardware.

A point can be ambiguous: it might lie on a part, an object, or a larger containing object. SAM addresses this ambiguity by producing multiple masks and predicting their quality. Additional clicks or a box can disambiguate the intended region. Its training data engine used model-assisted annotation to build SA-1B, a large and diverse dataset of images and masks. Prompt-based training and dataset diversity support zero-shot transfer to new images and tasks, but they do not establish perfect masks, automatic semantic labeling, or universal transfer under domain shift. SAM can also be used in automatic mask generation via a grid of prompts, a specific inference procedure distinct from claiming that it always labels every object semantically.

### 2.5 Adversarial examples and threat models

Given a classifier $f_\theta$, input $x$, true label $y$, loss $L(\theta,x,y)$ and perturbation budget $\epsilon$, an untargeted attacker seeks a perturbation that increases loss subject to a norm constraint:

$$\max_{\|\delta\|_p\leq\epsilon,\;x+\delta\in\mathcal X} L(\theta,x+\delta,y).$$

The input domain $\mathcal X$ imposes valid value bounds, such as $[0,1]^d$ for appropriately scaled pixels. A small $\ell_p$ norm is a mathematical constraint; its perceptual meaning depends on scale, representation and data. Attacks are assessed relative to a threat model: norm and budget, target or untargeted goal, knowledge of the model and preprocessing, query access, and permissible input domain all matter. An incorrect prediction on a naturally difficult example is not by itself evidence of an adversarial perturbation.

FGSM follows a first-order linear approximation $L(x+\delta,y)\approx L(x,y)+\nabla_x L(x,y)^\top\delta$. Under the $\ell_\infty$ constraint, each coordinate independently maximizes this linear term by taking the sign of its gradient:

$$x_{adv}=\operatorname{clip}_{\mathcal X}\bigl(x+\epsilon\operatorname{sign}(\nabla_xL(\theta,x,y))\bigr).$$

If a gradient component is zero, the usual numerical sign convention yields zero for that component. Clipping changes the update near input boundaries. FGSM uses one gradient step and maximizes the local linear surrogate; it is not guaranteed to find the true worst case for a nonlinear model. For a targeted attack toward label $y_t$, the corresponding simple update minimizes target loss, reversing the sign when $L$ is the target-label loss.

Projected gradient descent (PGD) repeatedly takes gradient steps and projects into the permitted set:

$$x^{k+1}=\Pi_{\mathcal X\cap B_\infty(x,\epsilon)}\left(x^k+\alpha\operatorname{sign}(\nabla_{x^k}L(\theta,x^k,y))\right).$$

The projection is onto the intersection of the original input's perturbation ball and the valid data range. For an $\ell_\infty$ ball and box domain this reduces to coordinate-wise clipping to the intersection of the respective intervals. Random initializations and multiple restarts can help explore a nonconvex loss landscape. Increasing the number of steps without checking step size or gradient reliability is not a proof of optimality. A gradient-obfuscated model may appear resistant to an ineffective attack while remaining vulnerable to adaptive alternatives.

White-box attacks have access to the model and typically its gradients; standard gradient-based PGD and Carlini–Wagner are white-box examples. Black-box attacks use a restricted interface such as prediction scores or labels and can estimate gradients or exploit transfer from a surrogate. Zeroth-order optimization uses queries to estimate derivative information and is usually discussed as black-box. Random input transformation may be a defense or augmentation operation; its presence alone does not specify a white-box attack. Access assumptions, not whether the attacker uses mathematics or optimization, distinguish the settings.

## 3. Algorithms and practical reasoning

### 3.1 Reading an architecture diagram

1. Identify each input and trace the source of queries, keys, and values. An image-to-image attention block is visual self-attention; text-to-image attention is cross-attention.
2. Determine whether the text self-attention mask is bidirectional or causal. A bidirectional block encodes an observed sequence; a causal block supports next-token generation.
3. Follow the outputs to their heads. Separate image and text embeddings feed contrastive learning, a fused classification token feeds matching, and decoder logits feed language modeling.
4. Locate special tokens by their role, and only then map them to the diagram's numbered labels. Diagram labels are local to the paper and should not be treated as universal constants.
5. Verify dimensions. With text states `[B, N, d]` and image states `[B, M, d]`, text-to-image attention weights have shape `[B, N, M]` per head after suitable projections. Softmax normalizes across the image-key dimension.

### 3.2 Prompted mask workflow

Encode the image, encode a point or box, then run the mask decoder. Inspect proposed masks, choose the one matching the intended object, and correct it with additional positive or negative points. Store the selected mask and annotation metadata; a separate semantic labeling step may be necessary. Evaluate with task-specific ground truth and metrics such as intersection over union, $|A\cap B|/|A\cup B|$, including the chosen convention for empty masks. A high predicted mask-quality score is an estimate and should not substitute for independent ground truth.

### 3.3 Attack workflow

Choose the model, loss, input scaling and allowed perturbation before attacking. Compute the gradient with respect to the input, not model parameters, then construct the signed step and enforce both the budget and input range. Evaluate both clean and attacked inputs. For iterative attacks, use the original $x$ as the center of every projection, not the previous iterate; otherwise accumulated steps can escape the budget. If preprocessing normalizes channels, transform the perturbation budget consistently, or attack in unnormalized pixel space through the differentiable preprocessing pipeline. Record all hyperparameters and report attack success conditional on the evaluation population.

## 4. Comparisons and examination benchmarks

| Mechanism | Inputs and information flow | Main output | Typical use |
| :--- | :--- | :--- | :--- |
| ITC | Separate image and text encoders | Embedding similarity | Efficient retrieval and alignment |
| ITM | Joint image-grounded text encoder | Pair match probability | Pair scoring and reranking |
| LM | Causal text decoder cross-attending to image | Next-token distribution | Caption or answer generation |
| SAM | Image embedding plus spatial prompt | Prompt-conditioned masks | Interactive annotation and segmentation |
| FGSM | Input-loss gradient and one signed step | Perturbed input | Fast first-order attack |
| PGD | Repeated gradient steps and projection | Budget-constrained perturbed input | Stronger iterative attack evaluation |

The 27 primary-week records in the question bank carry 20.9 total marks, all from end-term papers. This is an accounting of the selected manifest, not an estimate of future exam probability. Three FGSM subquestions use $x=(3,7,5)$, gradient $(0.5,-0.5,1)$ and $\epsilon=0.01$. The signed perturbation is $(0.01,-0.01,0.01)$ and the attacked vector is $(3.01,6.99,5.01)$. The exercise contains no input clipping interval; imposing a pixel interval such as $[0,1]$ would change its stipulated mathematical problem.

## 5. Verification and interpretation

The following complete calculation checks the examination's three coordinate answers without additional dependencies. Run it with `uv run python` from the repository root.

```python
x = [3.0, 7.0, 5.0]
grad = [0.5, -0.5, 1.0]
epsilon = 0.01
sign = lambda value: (value > 0) - (value < 0)
adversarial = [a + epsilon * sign(g) for a, g in zip(x, grad)]
print([round(value, 2) for value in adversarial])
```

```text
[3.01, 6.99, 5.01]
```

The gradient magnitudes affect neither coordinate's FGSM step size when they are nonzero; their signs determine its direction. PGD, unlike this calculation, recomputes a gradient after each update. Neither operation changes the model's parameters. A test that evaluates only the clean input cannot establish adversarial robustness.

## 6. Applications and limitations

**Image retrieval:** Encode a corpus of images once and rank them for a text query using contrastive similarity. Cross-modal matching can rerank shortlisted results. Failure modes include ambiguous text, biases in web data and false negatives in training.

**Visual question answering and captioning:** A decoder conditions on an image and a text prefix to generate an answer or description. Plausible language may hallucinate objects or attributes; generation quality and visual grounding need separate evaluation.

**Medical or scientific annotation:** A promptable model can propose spatial masks for review, but unusual image statistics, fine structures and domain-specific definitions can cause mistakes. Specialist verification and domain-specific validation are essential.

**Robustness testing:** Use bounded attacks to probe a deployed classifier under a stated perturbation model. Performance under one attack and budget does not certify performance against all attacks, physical changes, or distribution shifts.

## 7. Pitfalls and misconceptions

- **Contrastive versus matching:** ITC aligns separately encoded representations; ITM classifies a fused pair. Their negatives and computational costs differ.
- **Encoder versus decoder:** Bidirectional text encoding and autoregressive decoding use different attention masks even if some weights are shared.
- **Prompt versus label:** A SAM point specifies spatial evidence for a mask, not necessarily a semantic class name. A proposed mask can still be wrong.
- **Zero-shot versus guaranteed:** Zero-shot means a target task is attempted without task-specific training in the evaluation setup; it does not mean universal success or absence of related pretraining data.
- **Attack versus defense:** FGSM and PGD generate adversarial inputs; training against them is a separate defense procedure. Robustness depends on the attack and its assumptions.
- **Gradient sign versus gradient magnitude:** FGSM uses the sign for an $\ell_\infty$ step. For a different norm constraint, the optimal linearized direction can differ.
- **Projection center:** PGD projects relative to the clean input. Clipping each individual step alone does not bound the final accumulated perturbation.
- **Apparent safety:** Failed optimization does not imply no adversarial example exists. Test attack strength, restarts, numerical gradients and preprocessing.

## 8. Conclusion and handoff

The week integrates three forms of conditioning: multimodal fusion conditions text representations on visual features; a decoder conditions future text on the image and generated prefix; and SAM conditions masks on spatial prompts. Contrastive alignment, pairwise matching and language modeling have distinct loss functions and inference costs. Robustness requires an explicit threat model and evaluation against perturbations that respect the same data scale and domain. The question bank supplies the source-keyed end-term exercises; the exam notes provide compact formula and calculation practice. The next study step is to revisit Weeks 9–11 for transformer attention, representation learning and image–text alignment before integrating these ideas in a complete end-term review.

## 9. Academic references and annotated literature

1. Li, J., Li, D., Xiong, C., and Hoi, S. (2022). “BLIP: Bootstrapping Language-Image Pre-training for Unified Vision-Language Understanding and Generation.” *ICML*. [arXiv:2201.12086](https://arxiv.org/abs/2201.12086). Contribution: unified pretraining objectives and captioning/filtering of noisy data.
2. Kirillov, A., et al. (2023). “Segment Anything.” *ICCV*. [arXiv:2304.02643](https://arxiv.org/abs/2304.02643). Contribution: promptable segmentation model and large-scale data engine.
3. Goodfellow, I. J., Shlens, J., and Szegedy, C. (2015). “Explaining and Harnessing Adversarial Examples.” *ICLR*. [arXiv:1412.6572](https://arxiv.org/abs/1412.6572). Contribution: linear explanation and fast gradient sign method.
4. Madry, A., Makelov, A., Schmidt, L., Tsipras, D., and Vladu, A. (2018). “Towards Deep Learning Models Resistant to Adversarial Attacks.” *ICLR*. [arXiv:1706.06083](https://arxiv.org/abs/1706.06083). Contribution: robust optimization and iterative first-order attacks.
5. Carlini, N., and Wagner, D. (2017). “Towards Evaluating the Robustness of Neural Networks.” *IEEE Symposium on Security and Privacy*. [DOI:10.1109/SP.2017.49](https://doi.org/10.1109/SP.2017.49). Contribution: optimization-based attacks and robustness evaluation.
6. Vaswani, A., et al. (2017). “Attention Is All You Need.” *NeurIPS*. [arXiv:1706.03762](https://arxiv.org/abs/1706.03762). Contribution: scaled dot-product attention and transformer encoder–decoder architecture.

## Appendix A — Computational reproducibility

Run the complete code in Section 5 with `uv run python` and compare the printed vector with the source-keyed FGSM questions. No empirical performance claims in this report are inferred from that arithmetic check.

## Appendix B — Knowledge graph connections

**Upstream:** [[week-11-report]] and [[Knowledge-Map]]. **Sibling concepts:** [[blip-pretraining]], [[promptable-segmentation]], [[adversarial-examples]], [[multimodal-decoding]]. **Practice:** [[week-12-questions]] and [[week-12-exam-notes]].
