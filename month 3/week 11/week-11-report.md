---
title: "Self-Supervised Representation Learning and Vision–Language Alignment"
week: 11
month: 3
status: provisional
date: 2026-11-14
prev: "[[week-10-report|Week 10]]"
next: "[[week-12-report|Week 12]]"
map: "[[Knowledge-Map]]"
tags:
  - dlcv/week-11
  - dlcv/self-supervision
  - dlcv/vision-language
concepts:
  - "[[contrastive-learning]]"
  - "[[infonce-loss]]"
  - "[[few-shot-learning]]"
  - "[[clip-alignment]]"
  - "[[vision-language-retrieval]]"
---

# Self-Supervised Representation Learning and Vision–Language Alignment

> **Week 11 Review Article — Month 3 / Week 11**  
> **Provisional:** topics inferred from past papers; replace when the official syllabus is available.

**Navigation:** ← [[week-10-report|Week 10]] · [[Knowledge-Map|Knowledge Map]] · [[week-12-report|Week 12]] →  
**Associated concepts:** [[contrastive-learning]] · [[infonce-loss]] · [[few-shot-learning]] · [[clip-alignment]] · [[vision-language-retrieval]]

## Abstract

Representation learning uses an auxiliary training signal to organize observations before deployment on a target task. Self-supervision derives that signal from relationships within data, while contrastive objectives turn instance or cross-modal matching into a classification problem. SimCLR uses multiple augmented views and in-batch comparisons, whereas MoCo maintains a queue and a slowly updated key encoder. Few-shot adaptation evaluates how well a learned representation supports new classes with limited labelled examples; CLIP instead can compare an image with natural-language class descriptions without labelled target examples. This review derives the relevant objectives, distinguishes their sampling assumptions, and examines retrieval, visual question answering, temperature, and the limitations of numerical similarity scores. The week and its topic boundaries are provisional, so they should not be mistaken for an official syllabus.

## Keywords

Self-supervision, pretext task, InfoNCE, SimCLR, MoCo, few-shot, CLIP, cross-entropy, cosine similarity, vision–language retrieval.

## 1. Introduction and Week 11 syllabus

Supervised classification asks a model to predict human-provided labels. Its success depends both on the architecture and on whether annotations cover the variation that a later task needs. Large collections of images and paired text are easier to acquire than exhaustive labels for every downstream category. A representation can therefore be trained on a source objective and reused for classification, retrieval, or another task. The central design question is which relationships the source objective preserves and which variations it discards. An image and a crop of that image can provide a positive relationship without a human class label; an image and its caption provide a naturally paired cross-modal relationship.

The previous week's generative material studies how a model can represent or generate data. Here the emphasis shifts to representations useful for transfer, although reconstruction and generation can also supply self-supervised objectives. The end-term questions test whether the student can distinguish a supervision source, calculate a contrastive loss, identify a few-shot setting, and reason about CLIP. They also test image–text retrieval, text-conditioned detection and visual question answering as distinct vision–language tasks. A taxonomy match is not proof of an official teaching sequence.

| Provisional topic | Central question | Examination operation |
| :--- | :--- | :--- |
| Self-supervised objectives and pretext tasks | Where does the target come from? | Identify a task derived from the data |
| Contrastive representation learning | How is a match distinguished from alternatives? | Compute InfoNCE and compare SimCLR with MoCo |
| Few-shot and low-data adaptation | How is a new class learned with few examples? | Count support examples, distinguish zero-shot |
| CLIP and image–text alignment | How do paired modalities share a space? | Interpret cross-entropy, cosine and temperature |
| Vision–language tasks and retrieval | What is the task input and output? | Distinguish retrieval, detection and VQA |

## 2. Theoretical foundations

### 2.1 Pretext objectives and the origin of supervision

Let $x\sim p_{\rm data}$ be an unlabelled observation and let $T$ be a transformation or sampling operation. A self-supervised system constructs a target or relationship $y_T$ from available data and minimizes an expected pretext loss

$$\min_\theta\;\mathbb E_{x,T}\left[\ell(f_\theta(T(x)),y_T(x))\right].$$

The absence of manual category labels does not mean the absence of a target. Predicting the relative temporal order of video frames uses the sequence from the recording as a target. Predicting a masked region uses the hidden content as a target. Contrasting two transformations of an image uses their common source as a relationship. A triplet objective can use synchronized views as positives and temporally separated observations as negatives when that relationship is justified by the data. The target may be noisy: two frames separated in time can still depict the same semantic state, and a crop can remove the object of interest.

**The dangerous misconception:** any objective trained on images is automatically self-supervised. A class-conditional variational autoencoder that requires external class labels for conditioning uses supervised class information, even though its reconstruction loss may otherwise be formed from the input. Conversely, an autoencoder that reconstructs its input without class labels is often described as self-supervised. The correct classification depends on how each training signal is obtained, not on the name of the architecture alone. CLIP's image–text pairs are naturally occurring weak supervision: the text itself is human-authored, but no fixed downstream class label is required.

An encoder $f_\theta$ maps an image $x$ to a feature $h\in\mathbb R^d$. A downstream classifier may operate directly on $h$, on normalized features $h/\|h\|_2$, or after fine-tuning the encoder. In self-supervised pretraining, the pretext task is not the final measure of success. A representation that solves rotation prediction by exploiting border artifacts can achieve low pretext loss while failing semantic classification. Meaningful evaluation holds out downstream labels and tests transfer on an independently specified task. The choice of augmentation encodes desired invariance, so destructive transformations can erase information needed in the downstream task.

### 2.2 Contrastive classification and InfoNCE

For a query $q$, its positive key $k^+$ and a candidate set $\mathcal K$ containing that positive, define a similarity $s(q,k)$ and temperature $\tau>0$. The single-query InfoNCE loss is

$$\ell(q,k^+)=-\log\frac{\exp(s(q,k^+)/\tau)}{\sum_{k\in\mathcal K}\exp(s(q,k)/\tau)}.$$

This is cross-entropy for the index of the positive key among candidates. It is nonnegative because its argument is a probability in $(0,1]$. The positive must occur exactly once in this denominator under this definition; conventions with multiple positives use a different aggregation and must be stated. When logits already include temperature scaling, dividing again by $\tau$ is an error. For numerical stability, evaluate $-z_+ + \operatorname{logsumexp}(z_1,\ldots,z_K)$, subtracting the largest logit before exponentiation if implementing the operation directly.

Writing $p_j=\exp(z_j)/\sum_k\exp(z_k)$, differentiation gives $\partial\ell/\partial z_j=p_j-\mathbf1[j=+]$. For $z_j=s_j/\tau$ the derivative with respect to similarity is $(p_j-\mathbf1[j=+])/\tau$. A lower temperature increases logit separation for fixed unequal scores and sharpens the distribution, giving a high-scoring negative a greater share relative to easier negatives. The overall gradient magnitude is not guaranteed to increase monotonically: saturation and the actual scores also matter. Equal logits remain equal after temperature scaling.

For L2-normalized embeddings, $s(q,k)=q^\top k$ is cosine similarity. For arbitrary nonzero vectors $a,b$ in the same dimension, cosine is $a^\top b/(\|a\|_2\|b\|_2)$. A dot product alone equals cosine only when both norms are one, and a dot product of different-dimensional vectors is undefined. A scaled and rectified metric such as CLIPScore must specify its scale and its clipping convention; the cosine itself is not automatically a percentage or the full metric. These conditions are important because two supplied examination questions violate their stated normalization or dimensional assumptions.

The interpretation of negatives is conditional on the sampling process. A negative is a candidate declared nonmatching for the pretext task, not necessarily an example of a different semantic class. Two photographs of the same breed can be treated as negatives in instance discrimination, creating a false negative for a class-level task. Increasing the number of candidates makes the classification problem more discriminative but can increase false negatives and computational cost. InfoNCE has a mutual-information lower-bound interpretation only under specific sampling and density-ratio assumptions; a low finite-batch training loss alone does not prove a useful or calibrated representation.

### 2.3 Few-shot and low-data adaptation

In an $N$-way, $K$-shot episode, the support set $S=\{(x_i,y_i)\}$ contains $K$ labelled examples for each of $N$ target classes, while a separate query set assesses prediction. Support and query examples must be disjoint. Source-training classes and novel evaluation classes are often disjoint as well; the exact split and whether unlabelled query data may influence adaptation must be reported. A model trained on many examples of source classes but given 20 labelled examples per unseen target class is operating in a 20-shot setting, regardless of the larger source dataset.

A prototypical classifier embeds support samples and computes a class centroid

$$c_k=\frac{1}{|S_k|}\sum_{(x_i,y_i)\in S_k}f_\theta(x_i),\qquad p(y=k\mid x,S)=\frac{e^{-d(f_\theta(x),c_k)}}{\sum_j e^{-d(f_\theta(x),c_j)}}.$$

The distance $d$ and the feature normalization are choices, not universal constants. Episodic meta-training simulates tasks by repeatedly sampling support and query subsets and optimizes query performance after a task-specific adaptation step. Other few-shot methods use a frozen encoder and fit a linear classifier, perform nearest-neighbour matching, or fine-tune selected weights. All may be few-shot without being meta-learning. In contrast, zero-shot classification uses no labelled target-class examples, although it can use text descriptions or other side information. Neither term specifies that pretraining uses no labelled or paired data.

### 2.4 CLIP: a symmetric cross-modal loss

Given $B$ observed pairs $(I_i,T_i)$, image and text encoders followed by projections yield vectors in a common $d$-dimensional space. Normalize each vector to obtain $u_i$ and $v_j$ and construct the similarity matrix $S\in\mathbb R^{B\times B}$ with

$$S_{ij}=\frac{u_i^\top v_j}{\tau},\quad
L_{I\to T}=-\frac1B\sum_i\log\frac{e^{S_{ii}}}{\sum_j e^{S_{ij}}},\quad
L_{T\to I}=-\frac1B\sum_j\log\frac{e^{S_{jj}}}{\sum_i e^{S_{ij}}},\quad L=\tfrac12(L_{I\to T}+L_{T\to I}).$$

Each row treats the matching caption as the class for its image; each column treats the matching image as the class for its caption. Thus CLIP uses contrastive learning *and* cross-entropy: these describe the construction and the classification loss, respectively. The shared space permits comparison between independently computed image and text vectors. Matching pair scores are encouraged to exceed alternatives, rather than forcing every positive cosine to a particular numerical value in isolation. A batch may contain multiple semantically valid captions or near-duplicate images that are treated as negatives by this basic diagonal objective.

At zero-shot inference, choose a prompt template, encode candidate class descriptions, encode the image, and rank similarities. For instance, descriptions of a cat and a dog can be compared to an image; no target-class examples are needed to train a new classifier. Prompt wording, candidate set, distribution shift and the text encoder affect the prediction. The softmax over a chosen set of labels yields relative scores for that set, not an unconditional guarantee of calibrated probabilities. Class descriptions are side information; saying zero-shot does not imply that the pretraining corpus contained no related images or text.

## 3. Algorithms and computational machinery

### 3.1 SimCLR

1. Sample $N$ source images and independently draw two stochastic augmentations for each, producing $2N$ views.
2. Apply a shared encoder $f$ and projection head $g$ to each view; normalize the projected vectors.
3. For each view, treat the other view of the same image as the positive. Compare it against the other $2N-2$ views, excluding the anchor itself but including the positive in the denominator.
4. Average the $2N$ directed losses and backpropagate through the shared encoder and projection head. For downstream evaluation, the representation before the projection head is commonly used.

The resulting normalized temperature-scaled cross-entropy is often called NT-Xent. Two different augmentations define the desired invariance. Random cropping encourages some spatial invariance, and colour distortion reduces reliance on colour alone, but the correct invariances depend on the task. A medical application in which colour indicates a diagnosis may be harmed by aggressive colour changes. The projection head allows the contrastive objective and transferable feature to occupy different representational spaces; removing it changes the optimization, not merely the notation. The original SimCLR experiments emphasize augmentation composition, nonlinear projection, larger batches and longer training, but those empirical findings do not guarantee that maximal batch size is always optimal.

### 3.2 MoCo

MoCo treats contrastive learning as a dynamic dictionary. A query encoder produces $q$ for one view; a key encoder produces the positive key for another. A first-in-first-out queue stores keys from prior minibatches, providing many candidate negatives without retaining all their computation graphs. At each step, new keys are enqueued and the oldest are removed. The key encoder is updated with an exponential moving average of query-encoder parameters:

$$\theta_k\leftarrow m\theta_k+(1-m)\theta_q,\qquad 0\le m<1.$$

The slow update makes queued keys more consistent with current keys than if the encoder changed abruptly. The queue nevertheless contains stale representations, and choosing momentum and queue size trades diversity against staleness. Gradients update the query encoder via the loss; the momentum rule updates the key encoder in the standard construction. The queue is a computational and sampling mechanism, not a list of guaranteed different semantic classes. MoCo and SimCLR both use augmented views and contrastive objectives, but their principal negative dictionaries and encoder update strategies differ.

### 3.3 Image–text inference pipeline

A dual encoder can precompute vectors for a large image or text collection. For text-to-image retrieval, encode the query once and rank all candidate image vectors by similarity; approximate nearest-neighbour indexing can reduce search cost at the expense of potentially missing exact neighbours. Image-to-text retrieval reverses the query and candidate modalities. Retrieval ranks existing candidates, while visual question answering produces or selects an answer conditioned on an image and a question. Text-conditioned object detection additionally localizes entities, commonly requiring box predictions and a mechanism that associates a text query with image regions. A single global CLIP vector does not by itself define a detector or a generative VQA decoder.

## 4. Numerical analysis and comparative benchmarks

| Method | Positive | Alternatives | Encoder / memory | Typical use |
| :--- | :--- | :--- | :--- | :--- |
| SimCLR | Two views of one image | Other batch views | Shared encoder; large in-batch set | Transferable visual features |
| MoCo | Two views of one image | Queued keys | Query and momentum key encoders | Visual pretraining with a dictionary |
| CLIP | Paired image and text | Other batch images or captions | Separate image and text encoders | Cross-modal retrieval and zero-shot classification |
| Prototypical few-shot | Labelled support examples of a class | Other class prototypes | Feature encoder plus support centroids | Adaptation to novel classes |

The table describes the characteristic construction, not an exhaustive list of variants. SimCLR and MoCo can be used to initialize a few-shot learner, and CLIP can also be adapted using labelled examples. Their labels refer to objectives or training regimes rather than mutually exclusive application domains. Dataset quality, compute, architecture and evaluation protocol must be matched before claiming an empirical winner. In particular, a larger contrastive batch increases the candidate set but does not independently establish better downstream accuracy.

For logits $2,1,0$ with the first positive and unit temperature, the exact loss is $\log(e^2+e+1)-2\approx0.407606$. If the exam supplies rounded exponentials $7.39,2.72,1$, the corresponding result is approximately $0.407718$, which rounds to $0.408$. The difference is rounding of the intermediate exponentials. The answer range starts at $0.408$, so the rounded result lies at its boundary; treating the supplied decimal approximations as exact yields a value slightly below the bound. A logarithm to base ten would instead solve a different objective. The dimension of every similarity must be compatible before calculating a score.

A source question supplies $I=(0.2,0.5,0.3,0.4)$ and $T=(0.1,0.6,0.3,0.7)$ and calls them normalized. Their dot product is $0.69$, but their norms are approximately $0.734847$ and $0.974679$. Their cosine is therefore approximately $0.963364$, not $0.69$. The source's 69% corresponds to its raw dot product. Another question supplies vectors with four and three entries; it has no defined ordinary cosine. The source key is retained in the question bank with an explicit warning instead of silently fixing the data.

## 5. Practical implementation and verification

The following complete standard-library program checks both InfoNCE arithmetic and the cosine distinction. It uses no random sampling. Execute from the repository with `uv run python <file.py>` after saving the block.

```python
import math

logits = [2.0, 1.0, 0.0]
m = max(logits)
loss = m + math.log(sum(math.exp(x - m) for x in logits)) - logits[0]
rounded_loss = -math.log(7.39 / (7.39 + 2.72 + 1.0))
a = [0.2, 0.5, 0.3, 0.4]
b = [0.1, 0.6, 0.3, 0.7]
dot = sum(x * y for x, y in zip(a, b))
norm_a = math.sqrt(sum(x * x for x in a))
norm_b = math.sqrt(sum(x * x for x in b))
print(f"exact InfoNCE: {loss:.6f}")
print(f"rounded-input InfoNCE: {rounded_loss:.6f}")
print(f"dot: {dot:.6f}; norms: {norm_a:.6f}, {norm_b:.6f}")
print(f"cosine: {dot / (norm_a * norm_b):.6f}")
```

**Output and interpretation:** the first two values differ because the second calculation uses the rounded values explicitly supplied by the question. The dot product is not the cosine unless both input vectors have unit norm. The program's paired vectors have equal length; production code should explicitly validate matching dimensions and nonzero norms before division. Never infer a CLIPScore scaling factor from an unlabeled percentage option.

## 6. Applications and scientific formulations

**Medical image retrieval.** A text query such as a radiological finding can retrieve similar images by cross-modal similarity. The target is ranking relevant studies, measured against a labelled retrieval benchmark. A generic representation can miss rare findings, confound acquisition artifacts with disease, or expose training-set biases; clinical deployment requires separate validation and appropriate data controls.

**Wildlife monitoring.** Self-supervised views of camera-trap images can pretrain a visual encoder, followed by a few-shot classifier for a newly encountered species. The target is accuracy on held-out cameras and species. Augmentations that remove a small animal or treat temporally close but distinct animals as equivalent can invalidate the positive-pair assumption. Evaluation must separate camera sites or recording sessions when background leakage is a risk.

**Text-guided object localization.** A detector receives both an image and a phrase and predicts boxes or regions that correspond to the phrase. Correct evaluation requires localization as well as semantic matching, for example a specified intersection-over-union threshold. Global image–text alignment alone may associate an image with a phrase without identifying where the object lies. Multiple objects, relational phrases and small regions create ambiguity.

**Visual question answering.** A system maps image $I$ and question $q$ to an answer $a$, modelling $p(a\mid I,q)$ or ranking candidate answers. Question-only biases can yield superficially good scores without visual grounding. Dataset splits and counterfactual or balanced tests help establish whether the model uses the image. A retrieval model may supply representations, but the answer head or decoder and evaluation protocol remain separate design decisions.

## 7. Critical challenges, pathologies and misconceptions

1. **Label leakage:** selecting a model or tuning prompts on the target test set invalidates the estimate of generalization. Separate training, validation and test sets by the unit relevant to deployment.
2. **Shortcut features:** a pretext label can be inferred from borders, compression or timestamps rather than the intended semantic content. Inspect transformations and evaluate downstream transfer.
3. **False negatives:** images or captions that share a real semantic match can appear in the negative set. Batch construction and multi-positive losses may mitigate, but do not automatically remove, this problem.
4. **Collapse and trivial solutions:** an objective that only pulls positive pairs together can map all inputs to a constant. Contrastive negatives oppose this particular collapse; other non-contrastive systems require their own asymmetries or constraints.
5. **Temperature:** smaller $\tau$ sharpens fixed logits; it is not a guarantee that every gradient norm increases or that embeddings become orthogonal.
6. **Evaluation mismatch:** retrieval, classification, detection and VQA have different outputs and metrics. Strong image-level retrieval alone does not establish grounding or reasoning.
7. **Few-shot ambiguity:** report way, shot, support/query split and adaptation procedure. Few-shot need not mean a model was trained from scratch on only a few images.
8. **Numerical assumptions:** verify vector dimensions, norms, candidate set, temperature and logarithm base before calculating a contrastive loss or cosine. Source keys may contain inconsistencies.
9. **Representation bias:** internet image–text pairs reflect coverage gaps and social biases; correlations and inappropriate descriptions can transfer to downstream outputs. Benchmark performance is not a guarantee of fairness or safe deployment.

## 8. Conclusion and pedagogical handoff

1. A self-supervised target is derived from data relationships; the training procedure may still contain other forms of supervision.
2. InfoNCE is cross-entropy over a positive and alternatives, and its interpretation depends on the candidate sampling scheme.
3. SimCLR uses views and in-batch comparisons; MoCo uses a momentum key encoder and a queue.
4. Few-shot classification uses a small labelled support set for new classes, whereas CLIP can classify zero-shot using text prompts.
5. CLIP learns a shared image–text space through symmetric cross-entropy, enabling retrieval but not automatically solving localization or question answering.
6. Week 12 extends cross-modal representations to multimodal pretraining, prompting and generation; the provisional taxonomy should be replaced once official material is available.

## 9. Academic references and annotated literature

- Chen, T., Kornblith, S., Norouzi, M., and Hinton, G. (2020). “A Simple Framework for Contrastive Learning of Visual Representations.” *ICML*. [arXiv:2002.05709](https://arxiv.org/abs/2002.05709). Contribution: SimCLR augmentation, projection, and contrastive training framework.
- He, K., Fan, H., Wu, Y., Xie, S., and Girshick, R. (2020). “Momentum Contrast for Unsupervised Visual Representation Learning.” *CVPR*. [DOI:10.1109/CVPR42600.2020.00975](https://doi.org/10.1109/CVPR42600.2020.00975). Contribution: a momentum encoder and queue form a dynamic contrastive dictionary.
- van den Oord, A., Li, Y., and Vinyals, O. (2018). “Representation Learning with Contrastive Predictive Coding.” [arXiv:1807.03748](https://arxiv.org/abs/1807.03748). Contribution: predictive contrastive representation learning and InfoNCE.
- Radford, A., et al. (2021). “Learning Transferable Visual Models From Natural Language Supervision.” *ICML*. [arXiv:2103.00020](https://arxiv.org/abs/2103.00020). Contribution: symmetric image–text contrastive pretraining and zero-shot transfer.
- Snell, J., Swersky, K., and Zemel, R. (2017). “Prototypical Networks for Few-shot Learning.” *NeurIPS*. [arXiv:1703.05175](https://arxiv.org/abs/1703.05175). Contribution: class prototypes in a learned metric space.
- Hessel, J., Holtzman, A., Forbes, M., Le Bras, R., and Choi, Y. (2021). “CLIPScore: A Reference-free Evaluation Metric for Image Captioning.” *EMNLP*. [DOI:10.18653/v1/2021.emnlp-main.595](https://doi.org/10.18653/v1/2021.emnlp-main.595). Contribution: an image–caption evaluation metric built on CLIP embeddings.

## Appendix A — Computational reproducibility

Save the complete Python block in Section 5 to a local file and run `uv run python <file.py>`. Its standard-library operations need no network access or random seed. Source question wording and keys are preserved in [[week-11-questions]]; the bank identifies defective premises and key disagreements.

## Appendix B — Knowledge graph connections

**Upstream:** [[week-10-report]]; **downstream:** [[week-12-report]]; **siblings:** [[week-11-exam-notes]], [[week-11-questions]], [[contrastive-learning]], [[infonce-loss]], [[few-shot-learning]], [[clip-alignment]], [[vision-language-retrieval]].
