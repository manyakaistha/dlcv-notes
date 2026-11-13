---
title: "Dense Object Detection, Segmentation, and Motion Estimation"
week: 6
month: 2
status: provisional
date: 2026-11-14
prev: "[[week-5-report|Week 5]]"
map: "[[Knowledge-Map]]"
tags:
  - dlcv/week-06
  - dlcv/detection
  - dlcv/segmentation
concepts:
  - "[[focal-loss]]"
  - "[[intersection-over-union]]"
  - "[[feature-pyramid-network]]"
  - "[[semantic-segmentation]]"
---

# Dense Object Detection, Segmentation, and Motion Estimation

> **Week 6 Review Article — Month 2 / Week 6**  
> Topics inferred from past papers; replace when the official syllabus is available.

**Navigation:** [[week-5-report|Week 5]] · [[Knowledge-Map|Knowledge Map]] · [[week-06-questions|Week 6 questions]]

## Abstract

Dense prediction assigns outputs to many spatial locations and must reconcile recognition, localization, and computational cost. Object detectors estimate class and location, while semantic and instance segmentation distinguish categories and object identities at pixel resolution. This review develops intersection over union, positive-sample box regression, focal loss, and feature pyramids as complementary parts of the detection pipeline. It then examines encoder–decoder segmentation, max-pooling indices in SegNet, and optical-flow registration. Mathematical objectives clarify what each prediction is supervised to do and what cannot be inferred from a single score. The scope and sequence are provisional because they are reconstructed from past examination questions.

## Keywords

Dense detection, focal loss, intersection over union, anchor matching, FPN, semantic segmentation, SegNet, optical flow.

## 1. Introduction and provisional syllabus

Week 5 introduced CNN backbones and detection families. A classification backbone alone returns a global category and does not specify the spatial extent of each object. Detection augments a feature extractor with candidate locations, classification, and localization; segmentation asks for a much more detailed spatial labeling. Exam questions also connect dense prediction to image registration. The following clusters are inferred from the taxonomy and are not a claim about the official teaching order.

| Topic | Central question |
| :--- | :--- |
| Dense detection and focal loss | How can many easy background examples avoid overwhelming training? |
| Detection losses, boxes and matching | How do we compare boxes and count localization terms? |
| Multiscale feature pyramids | How can semantically strong features be available at multiple resolutions? |
| Semantic and instance segmentation | What is predicted for each pixel and each object? |
| SegNet encoder-decoder segmentation | How are pooling locations reused during decoding? |
| Optical flow and image registration | How are corresponding points aligned between images? |

## 2. Theoretical foundations

### 2.1 Prediction tasks and supervision

An image classifier maps an image $I$ to a vector of class scores. A detector instead produces a set of candidate boxes $b_j$, class scores $s_{jc}$, and possibly a background or objectness score. In ordinary supervised detection, annotated boxes provide the localization targets. An RPN proposes candidate regions but does not make the need for box supervision disappear. A box is a coarse rectangular approximation; it does not provide the exact object silhouette.

Semantic segmentation predicts a class at each pixel: $y_{ij}\in\{1,\ldots,C\}$. Before the class decision the logits form an array with shape `[H, W, C]`; a batched channels-first implementation typically uses `[B, C, H, W]`. The per-pixel softmax yields class probabilities and argmax selects a label. Two adjacent cars can receive the same semantic label without being separated. Instance segmentation additionally assigns distinct object identities and masks, so each car has its own foreground region. Panoptic segmentation combines semantic labels for amorphous regions with instance identities for countable objects. Classification, detection and segmentation solve different output problems, even when their backbones are similar.

For labeled pixels $\Omega$ the usual pixelwise cross-entropy is

$$
L_{\rm seg}=-\frac{1}{|\Omega|}\sum_{(i,j)\in\Omega}\log p_{ij,y_{ij}}.
$$

Ignored or unlabeled pixels must be excluded from both numerator and normalizer. Class imbalance, annotation uncertainty and boundary errors can make pixel accuracy misleading: predicting background everywhere may score well when foreground is rare. Per-class IoU and mean IoU provide complementary views, but their handling of absent classes should be stated explicitly.

### 2.2 Intersection over union

For measurable boxes or masks $A$ and $B$,

$$\operatorname{IoU}(A,B)=\frac{|A\cap B|}{|A\cup B|}=\frac{|A\cap B|}{|A|+|B|-|A\cap B|}.$$

Under continuous coordinates, a box $(x_1,y_1,x_2,y_2)$ has area $(x_2-x_1)(y_2-y_1)$ for valid ordered endpoints. The overlap width is $\max(0,\min(x_2^A,x_2^B)-\max(x_1^A,x_1^B))$; height is analogous. The max prevents a negative intersection when boxes do not overlap. Inclusive integer pixel conventions can instead use a $+1$ in widths and heights: a solution must state which convention is used and never mix them.

IoU ranges from zero for disjoint positive-area boxes to one for identical boxes. It is scale-normalized and symmetric, but has no useful ordinary overlap gradient for strictly disjoint boxes. Generalized IoU and other geometric extensions address aspects of this limitation. IoU is also a matching or evaluation criterion, and its use there should not be confused with a specific differentiable training loss. For example, $1-\operatorname{IoU}$ is a possible regression loss, contrary to the misconception that IoU cannot enter a loss function.

### 2.3 Anchors and box regression

An anchor is a reference box, usually specified by a location, scale and aspect ratio. Matching assigns anchors to ground-truth objects according to a chosen rule, often with IoU thresholds and additional forced matches. Negative anchors supply background classification examples; ambiguous anchors may be ignored. The exact thresholds and sampling policy are design choices, not properties of IoU itself. A positive anchor receives target offsets such as

$$t_x=(x-x_a)/w_a,\quad t_y=(y-y_a)/h_a,\quad t_w=\log(w/w_a),\quad t_h=\log(h/h_a).$$

Here $(x,y,w,h)$ describes the ground-truth box and the subscript $a$ describes the anchor. Regression predicts offsets rather than absolute coordinates, allowing the same head to operate across positions and scales. Widths and heights must be positive. At inference the transform is inverted and clipping to the image may be needed.

A standard two-stage objective combines classification and localization. For an anchor or proposal $i$ with label $p_i^*\in\{0,1\}$ and target $t_i^*$, a schematic form is

$$L=\frac{1}{N_{\rm cls}}\sum_i L_{\rm cls}(p_i,p_i^*)+\lambda\frac{1}{N_{\rm reg}}\sum_i p_i^* L_{\rm reg}(t_i,t_i^*).$$

The positive indicator excludes background examples from box regression. The per-positive loss is commonly summed over four box coordinates, so distinguish the number of proposal-level regression terms from the number of scalar coordinate residuals. Positive counts are summed across the images actually sampled for the minibatch, not multiplied again by batch size. Real systems may subsample or normalize differently, so the stated question assumptions matter.

Smooth L1 is quadratic near zero and linear outside a threshold. In one common parameterization,

$$\operatorname{smoothL1}_{\beta}(r)=\begin{cases}r^2/(2\beta),&|r|<\beta,\\ |r|-\beta/2,&\text{otherwise}.\end{cases}$$

Compared with squared error its linear tails limit the influence of very large residuals. Some software calls a related but differently scaled function Huber loss; inspect the chosen convention before comparing numerical values. RPN objectness and offsets are separate from the later detector head's classification and box regression, though both use related principles.

## 3. Core algorithms

### 3.1 Dense detection and focal loss

A dense detector predicts across many spatial positions and often multiple anchors per position. Most candidates are background, so an enormous number of easy negatives can dominate a summed cross-entropy objective. Binary cross-entropy for target $y\in\{0,1\}$ and predicted positive probability $p$ is $-y\log p-(1-y)\log(1-p)$. Define $p_t=p$ when $y=1$ and $p_t=1-p$ when $y=0$. Focal loss modifies this to

$$\operatorname{FL}(p_t)=-\alpha_t(1-p_t)^\gamma\log p_t.$$

When $\gamma=0$, this is weighted cross-entropy. For $\gamma>0$, easy correct examples with $p_t$ near one are downweighted more strongly than difficult examples. The coefficient $\alpha_t$ can also rebalance classes. The loss is not a box-distance loss and does not guarantee good localization. RetinaNet combines this classification loss with a multiscale detection architecture. The classification loss and the regression loss solve distinct subproblems and may be combined in one overall objective.

### 3.2 Feature pyramid networks

Backbone features become spatially coarser and usually more semantically abstract as depth increases. A feature pyramid network uses a top-down pathway and lateral projections to join deep semantic features with shallower, higher-resolution features. A schematic recursion is

$$P_l=\operatorname{Conv}_{3\times3}\left(\operatorname{Lat}(C_l)+\operatorname{Upsample}(P_{l+1})\right).$$

Actual implementations distinguish intermediate top-down maps from final smoothed pyramid outputs; spatial sizes must match before addition. Lateral $1\times1$ convolutions align channels. A detector head can be applied at several pyramid levels, letting high-resolution levels represent small objects and coarser levels cover larger receptive fields. Multiscale maps do not guarantee small-object success: limited image evidence, stride, matching rules and annotations still matter.

If level $l$ has spatial size $H_l\times W_l$ and $A_l$ anchors per location, the total number is $\sum_l H_l W_l A_l$. This count describes candidate anchors before filtering and matching, not the number of objects or positive regression examples. A scale–aspect-ratio product gives anchors per location only when every combination is actually used.

### 3.3 SegNet encoder and decoder

SegNet uses an encoder that repeatedly convolves and max-pools, and a decoder that upsamples using the encoder's stored max-pooling indices. For each pooling window, max pooling records the location of the selected maximum. Max-unpooling places the corresponding activation at this location in a larger sparse map, with other positions set to zero. Subsequent learned convolutions densify and refine that map. This saves the need to retain full encoder feature maps for those pooling locations but cannot recover the discarded nonmaximal values. Pooling indices convey spatial placement, not full image content.

For a $2\times2$ window, four locations need two bits in principle. The bit convention in a question must be read from the diagram: treating `00`, `01`, `10`, and `11` as a universal ordering without a stated convention can reverse an answer. A value appearing in an output location determines the corresponding pooling index only under the specified unpooling setup. Ties in the original maximum need a defined implementation rule. SegNet's index reuse differs from U-Net-style skip concatenation, which forwards richer encoder features and costs additional feature storage.

### 3.4 Optical flow and registration

Optical flow is an apparent image-plane displacement field $\mathbf u(x,y)=(u,v)$ between frames. It is related to, but not identical to, the projection of physical 3D motion: illumination changes, occlusion, reflections and textureless surfaces break a simple correspondence. Registration estimates a warp aligning two images. A weighted squared-difference objective is

$$E(\mathbf u)=\sum_{\mathbf x}w(\mathbf x)\left[I_1(\mathbf x)-I_2(\mathbf x+\mathbf u(\mathbf x))\right]^2+\lambda R(\mathbf u).$$

The regularizer $R$ encodes an assumption such as spatial smoothness, and $w$ can suppress invalid or unreliable pixels. This is one possible objective, not the only valid registration distance. For small displacements and brightness constancy, Taylor expansion gives $I_xu+I_yv+I_t\approx0$. This single equation has two unknown flow components at each pixel; the aperture problem requires additional spatial or motion assumptions. Large motion often motivates coarse-to-fine estimation, but repeated texture and occlusion can still defeat correspondence.

## 4. Comparisons and numerical reasoning

| Method | Output | Main training signal | Limitation |
| :--- | :--- | :--- | :--- |
| Classification | Image labels | Image-level class | No explicit localization |
| Detection | Boxes and classes | Box and class annotations | Boxes do not describe exact masks |
| Semantic segmentation | Per-pixel class | Pixel labels | Same-class instances not separated |
| Instance segmentation | Object masks and classes | Instance masks | Overlap and fine boundaries are difficult |
| Optical flow | Pixel displacement vectors | Correspondence or photometric objective | Occlusion and illumination changes |

For two $10\times10$ boxes with $6\times6$ overlap, intersection is $36$, union is $100+100-36=164$, and IoU is $36/164\approx0.2195$. The closest of the stated options can be 21% even though the value is approximately 22%; rounding must follow the actual choices. For boxes $(2,2,10,12)$ and $(6,5,14,15)$, each area is $80$, the intersection is $4\times7=28$, and IoU is $28/132\approx0.212$. These calculations use continuous coordinates.

## 5. Practical implementation and verification

The following standard-library calculation verifies the examples and the three-level anchor count. Run it with `uv run python` from the project root.

```python

def iou(a, b):
    intersection = max(0, min(a[2], b[2]) - max(a[0], b[0])) * max(0, min(a[3], b[3]) - max(a[1], b[1]))
    area = lambda q: (q[2] - q[0]) * (q[3] - q[1])
    return intersection / (area(a) + area(b) - intersection)

print(f"IoU: {iou((2, 2, 10, 12), (6, 5, 14, 15)):.3f}")
print(f"Anchors: {9 * (80**2 + 40**2 + 20**2)}")
```

```text
IoU: 0.212
Anchors: 75600
```

The result checks arithmetic and conventions, not detector accuracy. A full detector must additionally specify matching, minibatch sampling, class and regression normalization, decoding and post-processing. In particular, non-maximum suppression removes redundant overlapping detections according to a score and threshold; it does not create the feature pyramid and is not a training loss.

## 6. Applications and limitations

Autonomous driving benefits from detecting vehicles and segmenting drivable regions, but small distant objects and weather changes challenge feature resolution and domain transfer. Medical imaging can use semantic masks to identify tissue regions and instance masks to distinguish adjacent cells; ambiguity in boundaries makes annotation and metric conventions critical. Aerial imagery contains objects at varied scales and orientations, for which pyramids and appropriate box parameterization are useful, but a standard axis-aligned box may include much background. Motion estimation can align frames for tracking or reconstruction; nonrigid motion, occlusions and brightness variation undermine simple squared-difference objectives.

A practical evaluation protocol should keep the training and test distributions distinct, specify the IoU threshold used to declare a detection correct, and report the treatment of unmatched predictions. A high score at a permissive threshold can coexist with poor boundary alignment. Classwise reporting helps expose rare-category failures that an aggregate score can conceal. The chosen annotation policy also shapes the target: overlapping instances, uncertain borders, and unlabeled objects may be handled differently across datasets. Reproducibility therefore depends on the data split and metric implementation as well as the neural architecture.

## 7. Pitfalls and misconceptions

**The dangerous misconception:** A high semantic-segmentation score implies distinct objects have been separated. **Why this is false:** the semantic output contains class labels, not necessarily instance identities. A detector may count separate objects but still fail to give their masks.

**The dangerous misconception:** Every RPN proposal contributes a box regression term. **Why this is false:** a standard regression target is defined for matched positive proposals; background supplies classification supervision. Count after any sampling specified by the problem.

**The dangerous misconception:** Focal loss changes the localization geometry. **Why this is false:** it modifies classification weighting; a separate box loss supplies localization supervision. Similarly, a feature pyramid mixes features at scales but does not automatically eliminate anchors or perform NMS.

**The dangerous misconception:** Max-unpooling is the inverse of max pooling. **Why this is false:** indices recover selected positions but not discarded values. The decoder must infer missing detail from learned parameters and available features.

## 8. Conclusion and handoff

Dense prediction uses spatial features for several different output structures. Box overlap, positive matching and focal loss address distinct detection decisions, while pyramids combine resolution and semantics. Segmentation adds pixel-level detail and SegNet uses stored pooling indices to guide decoding. Optical flow illustrates a different dense target: displacement rather than category. The provisional next cluster concerns recurrent sequence models and attention; its placement, like this week's, awaits an official syllabus.

## 9. Academic references and annotated literature

1. Lin, T.-Y. et al. (2017). Focal Loss for Dense Object Detection. *ICCV*. [DOI: 10.1109/ICCV.2017.324](https://doi.org/10.1109/ICCV.2017.324). Introduces focal loss and RetinaNet.
2. Lin, T.-Y. et al. (2017). Feature Pyramid Networks for Object Detection. *CVPR*. [DOI: 10.1109/CVPR.2017.106](https://doi.org/10.1109/CVPR.2017.106). Describes top-down pyramids with lateral connections.
3. Badrinarayanan, V., Kendall, A. and Cipolla, R. (2017). SegNet: A Deep Convolutional Encoder-Decoder Architecture for Image Segmentation. *IEEE TPAMI*. [DOI: 10.1109/TPAMI.2016.2644615](https://doi.org/10.1109/TPAMI.2016.2644615). Develops pooling-index-guided decoding.
4. Ren, S., He, K., Girshick, R. and Sun, J. (2015). Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks. *NeurIPS*. [arXiv:1506.01497](https://arxiv.org/abs/1506.01497). Introduces jointly trained proposal networks.
5. Horn, B. K. P. and Schunck, B. G. (1981). Determining Optical Flow. *Artificial Intelligence*. [DOI: 10.1016/0004-3702(81)90024-2](https://doi.org/10.1016/0004-3702(81)90024-2). Formulates optical flow with a smoothness constraint.

## Appendix A — Computational reproducibility

Run the code in Section 5 via `uv run python` from the repository root. Inputs are deterministic and no external data or random sampling is involved.

## Appendix B — Knowledge graph connections

Upstream: [[week-5-report]]. Siblings: [[focal-loss]], [[intersection-over-union]], [[feature-pyramid-network]], [[semantic-segmentation]]. Assessment: [[week-06-questions]].
