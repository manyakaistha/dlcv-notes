---
title: "Week 6 Exam Notes: Dense Detection and Segmentation"
week: 6
status: provisional
map: "[[Knowledge-Map]]"
---

# Week 6 Exam Notes: Dense Detection and Segmentation

> Topics inferred from past papers; replace when the official syllabus is available.

**Navigation:** [[week-6-report|Review]] · [[week-06-questions|Question bank]] · [[Knowledge-Map|Knowledge Map]]

## Prediction tasks: one-line recalls

- **Classification:** assign an image-level class or class probabilities; a class alone does not locate an object.
- **Object detection:** output object classes and boxes; multiple boxes represent multiple instances, though boxes are not detailed masks.
- **Semantic segmentation:** output a class label per pixel, without necessarily separating individual same-class objects.
- **Instance segmentation:** output a separate mask and class for each detected object instance.
- **Panoptic segmentation:** combine instance identities for countable objects with semantic labels for other regions.
- **Optical flow:** predict apparent image-plane displacement, not a categorical mask or automatically the full 3D velocity.
- **Per-pixel logits:** for $C$ classes, an output can have shape `[B, C, H, W]`; apply a class decision over $C$ at each pixel.

## Boxes, intersection and union

For box $A=(x_1,y_1,x_2,y_2)$ with continuous coordinates, area is $(x_2-x_1)(y_2-y_1)$. For boxes $A$ and $B$ compute:

$$w_I=\max(0,\min(x_2^A,x_2^B)-\max(x_1^A,x_1^B)),\quad h_I=\max(0,\min(y_2^A,y_2^B)-\max(y_1^A,y_1^B)),$$

$$I=w_Ih_I,\qquad U=|A|+|B|-I,\qquad \operatorname{IoU}=I/U.$$

**Recipe:** compute both areas, clamp each overlap dimension to zero, multiply them, subtract intersection once from the area sum, then divide. Compare the numerical answer with the available choices only after computing it. An inclusive integer-pixel convention differs from the continuous convention: state the convention and use it consistently. A disjoint pair has zero intersection. IoU is undefined if both areas and the union are zero, so valid boxes should have positive area.

**Worked example:** $A=(2,2,10,12)$ has area $8\cdot10=80$; $B=(6,5,14,15)$ also has area $80$. Intersection has width $10-6=4$ and height $12-5=7$, so $I=28$ and $U=132$. Thus IoU is $28/132=0.212121\ldots$, or $0.212$ to three decimals. This is not $28/160$: the latter neglects to subtract the overlap from the union.

**Worked example:** two $12\times12$ boxes sharing an $8\times8$ region have IoU $64/(144+144-64)=64/224\approx0.2857$, approximately 28.6%. If the question offers 28% as the nearest answer, choose the nearest listed option; do not silently treat 28% as the exact value.

## Positive examples and regression

An RPN predicts objectness and box offsets for anchors. Matching determines positive, negative and possibly ignored anchors. A positive corresponds to a ground-truth object and can carry a localization target. A background example has no foreground box target and typically contributes classification rather than localization loss. The complete training procedure may subsample positives, so use the stated count of sampled positive proposals if available.

**Recipe:** add positive proposal counts across images; count one proposal-level regression loss per positive. If a question instead asks for scalar residual components, four parameters per box usually give four times that number. Do not multiply by the number of images a second time, and do not mistake all 512 proposals for foreground.

**Worked example:** 10 foreground proposals in one image and 12 in the other give $10+12=22$ proposal-level terms. If each term separately sums four coordinate losses, this corresponds to 88 scalar coordinate contributions, before any averaging. The two counts answer different questions.

A common offset parameterization is $t_x=(x-x_a)/w_a$, $t_y=(y-y_a)/h_a$, $t_w=\log(w/w_a)$, $t_h=\log(h/h_a)$. The reference anchor has center $(x_a,y_a)$ and positive size $(w_a,h_a)$. Offset normalization makes the regression targets relative to anchor geometry. Smooth L1 behaves quadratically near zero and linearly in its tails, limiting the influence of large errors compared with squared error. IoU and its extensions can also serve as box regression objectives; the statement that IoU loss is impossible is false.

## Focal loss and class imbalance

For target $y$ and positive probability $p$, let $p_t=p$ if $y=1$ and $p_t=1-p$ if $y=0$. Then

$$\operatorname{FL}(p_t)=-\alpha_t(1-p_t)^\gamma\log p_t.$$

The factor $(1-p_t)^\gamma$ is small for an easy correctly classified example and larger for a difficult example. Setting $\gamma=0$ gives weighted cross-entropy. RetinaNet uses focal loss to address the dominance of easy background examples in dense one-stage detection. It is a classification loss, not a regression distance. Binary cross-entropy can also train an objectness score; focal loss is a modified cross-entropy and the best answer depends on the precise wording.

**Worked example:** for $p_t=0.9$ and $\gamma=2$, the modulating factor is $(0.1)^2=0.01$. For $p_t=0.2$ it is $(0.8)^2=0.64$. These are multiplicative weights on cross-entropy before the optional $\alpha_t$ factor, not the final loss values. Focal loss reduces easy-example influence; it does not remove hard negatives or guarantee a balanced minibatch.

## Feature pyramids and anchors

The top-down FPN path propagates semantically strong deep features toward higher-resolution maps. Lateral connections combine these with shallower features after channel alignment. Multiple pyramid levels allow heads to work at several spatial scales; the resulting maps do not themselves perform non-maximum suppression.

**Anchor recipe:** if level $l$ has $H_lW_l$ locations and $A_l$ anchors at each, total anchors are $\sum_l H_lW_lA_l$. Multiplying scales by aspect ratios is valid when the full Cartesian product is used. This is the number of candidates before thresholding or matching, not the number of detections.

**Worked example:** three levels $80\times80$, $40\times40$, $20\times20$ contain $6400+1600+400=8400$ locations. With three scales and three aspect ratios, there are nine anchors per location and $8400\cdot9=75600$ anchors per image. A batch of two would contain twice this many candidate anchors, but the exam question specifies per image.

## SegNet and unpooling

Max pooling outputs the maximum in each window and can record its position. SegNet reuses the corresponding encoder indices to place decoder values in an upsampled sparse map. Other positions are zero before later learned convolutions. The indices encode where a maximum was selected, not the nonmaximal input values. Unpooling is therefore not a mathematical inverse of pooling.

**Recipe for diagrams:** partition the output into pooling windows, locate the nonzero value in each window, translate that position using the diagram's bit convention, and write the indices in spatial order. Do not assume a universal `00`–`11` orientation. A $2\times2$ pooling window has four possible locations, so two bits suffice in principle. Ties require the implementation's selection rule. U-Net-style feature skips send richer feature maps and should not be conflated with saved pooling indices.

## Optical flow and registration

Brightness constancy plus a first-order expansion gives $I_xu+I_yv+I_t\approx0$ for flow $(u,v)$. One scalar equation cannot determine both unknown components at a single pixel: this is the aperture problem. Regularization or neighborhood assumptions supply additional constraints. A common dense registration objective minimizes a weighted sum of squared intensity differences between an image and the warped second image. It is one objective among several, not a universal law. Illumination changes, occlusion and large motion violate or complicate the simplest model.

## Code verification

The following deterministic calculation checks the numerical examples above. Execute it from the repository root with `uv run python`.

```python
print(f"IoU: {28 / (80 + 80 - 28):.3f}")
print(f"Second IoU: {64 / (144 + 144 - 64):.6f}")
print(f"Positive proposals: {10 + 12}")
print(f"Focal factors: {(1 - 0.9)**2:.2f}, {(1 - 0.2)**2:.2f}")
print(f"Anchors: {(80**2 + 40**2 + 20**2) * 9}")
```

```text
IoU: 0.212
Second IoU: 0.285714
Positive proposals: 22
Focal factors: 0.01, 0.64
Anchors: 75600
```
