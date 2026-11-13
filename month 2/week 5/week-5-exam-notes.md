---
title: "Week 5 Exam Revision Notes: Inception, ResNet, Modern Architectures, Visualization & Object Detection"
week: 5
month: 2
status: complete
tags:
  - dl4cv/week-05
  - dl4cv/exam-notes
  - deep-learning/inception
  - deep-learning/resnet
  - deep-learning/mobilenet
  - deep-learning/transfer-learning
  - computer-vision/object-detection
concepts:
  - "[[inception-googlenet]]"
  - "[[bottleneck-1x1-convolutions]]"
  - "[[resnet-residual-learning]]"
  - "[[degradation-problem]]"
  - "[[identity-shortcut-gradient-flow]]"
  - "[[resnext-cardinality]]"
  - "[[densenet-feature-reuse]]"
  - "[[depthwise-separable-convolutions]]"
  - "[[efficientnet-compound-scaling]]"
  - "[[senet-squeeze-and-excitation]]"
  - "[[convnext-modern-cnn]]"
  - "[[transfer-learning-decision-matrix]]"
  - "[[cnn-visualization-techniques]]"
  - "[[occlusion-experiments]]"
  - "[[tsne-representation-space]]"
  - "[[object-detection-taxonomy]]"
  - "[[viola-jones-algorithm]]"
  - "[[rcnn-framework]]"
  - "[[fast-rcnn-roi-pooling]]"
  - "[[faster-rcnn-rpn-anchors]]"
  - "[[yolo-single-stage-detector]]"
prev: "[[week-5-report|Week 5 Academic Report]]"
next: "[[../../Knowledge-Map|DL4CV Knowledge Map]]"
map: "[[../../Knowledge-Map|DL4CV Knowledge Map]]"
---

# Week 5 Exam Revision Notes: Advanced CNNs, Interpretability & Object Detection

> **Purpose:** Ultra-condensed, high-yield exam revision guide for Week 5 of Deep Learning for Computer Vision (Prof. Vineeth N Balasubramanian, IIT Hyderabad). Contains all essential mathematical derivations, governing formulas, complexity benchmarks, visual anchors, common exam traps, and model solutions.

---

## 1. High-Yield Master Formula & Concept Cheat Sheet

| Topic / Architecture | Governing Equation / Mathematical Formula | Computational Complexity / FLOPs | Core Architectural Innovation | High-Yield Exam Trap |
| :--- | :--- | :--- | :--- | :--- |
| **GoogLeNet / Inception** | 4 parallel paths: $1 \times 1$, $3 \times 3$, $5 \times 5$, $3 \times 3$ Pool | $\sim 5\text{M}$ weights ($12\times$ fewer than AlexNet) | Multi-scale filters without manual guessing; Global Avg Pool | **Naive module explodes FLOPs**; requires $1 \times 1$ bottleneck before $3\times3, 5\times5$. |
| **$1 \times 1$ Bottleneck Conv** | FLOPs: $H W \cdot (1 \cdot 1 \cdot C_{\text{in}}) \cdot C_{\text{red}}$ | $\mathcal{O}(H W C_{\text{in}} C_{\text{red}})$ | Low-dimensional channel subspace projection | Preserves spatial $H \times W$; only collapses/expands channel depth. |
| **Auxiliary Classifiers** | $\mathcal{L} = \mathcal{L}_{\text{main}} + 0.3 \mathcal{L}_{\text{aux1}} + 0.3 \mathcal{L}_{\text{aux2}}$ | Discarded during inference | Combats vanishing gradients in 22-layer deep net | Only used during **training**; discounted by $0.3\times$. |
| **The Degradation Problem** | Plain-56 error > Plain-20 error | Underfitting (NOT overfitting!) | Optimization failure in deep plain CNNs | Both **training AND test error increase**; gradients fail to propagate. |
| **ResNet Formulation** | $\mathbf{y} = \mathcal{F}(\mathbf{x}) + \mathbf{x} \implies \mathcal{F}(\mathbf{x}) = \mathcal{H}(\mathbf{x}) - \mathbf{x}$ | $\mathcal{O}(1)$ parameter overhead | Forces layers to learn residual perturbations | Identity shortcut (+x) is **element-wise addition**, not concatenation. |
| **ResNet Gradient Flow** | $\frac{\partial \mathcal{L}}{\partial \mathbf{x}_l} = \frac{\partial \mathcal{L}}{\partial \mathbf{x}_L} \left( \mathbf{I} + \frac{\partial}{\partial \mathbf{x}_l}\sum \mathcal{F} \right)$ | Non-vanishing gradient path | The persistent **$+\mathbf{I}$ identity term** | Gradients flow cleanly back to layer $l$ even if weight gradients vanish! |
| **ResNeXt Cardinality** | Aggregated split-transform-merge ($C=32$) | Same FLOP budget as ResNet | Cardinality as 3rd dimension (Depth, Width, Cardinality) | Increasing **cardinality $C$ outperforms** increasing depth or width. |
| **DenseNet Connectivity** | $\mathbf{x}_l = H_l([\mathbf{x}_0, \mathbf{x}_1, \dots, \mathbf{x}_{l-1}])$ | $\frac{L(L+1)}{2}$ direct connections | Feature reuse via depth concatenation | Uses **concatenation**, not addition; channels grow by growth rate $k$. |
| **MobileNet Factorization** | Ratio: $\frac{\text{Cost}_{\text{sep}}}{\text{Cost}_{\text{std}}} = \frac{1}{N} + \frac{1}{D_K^2}$ | $\approx \frac{1}{9} \implies \mathbf{8\times \text{ to } 9\times \text{ speedup}}$ | Depthwise ($D_K \times D_K \times 1$) + Pointwise ($1 \times 1 \times M$) | For $3 \times 3$, computation collapses to $\approx 11\%$ of standard conv! |
| **EfficientNet Scaling** | Depth $d=\alpha^\phi$, Width $w=\beta^\phi$, Res $r=\gamma^\phi$ | Subject to $\alpha \cdot \beta^2 \cdot \gamma^2 \approx 2$ | Compound Scaling | Scaling only one dimension saturates; must balance all three. |
| **SENet (Squeeze-Excite)** | $\mathbf{s} = \sigma\left( W_2 \cdot \operatorname{ReLU}(W_1 \mathbf{z}) \right), \; \tilde{X} = s \cdot X$ | $<1\%$ parameter overhead | Squeeze (GAP) + Excitation (MLP) channel attention | Dynamically re-weights channels based on global image context. |
| **ConvNeXt Block** | $7 \times 7$ depthwise, inverted bottleneck, LN, GELU | ViT parity with pure CNN | Macro/micro modernization of ResNet-50 | Replaces BatchNorm with **LayerNorm**; replaces ReLU with **GELU**. |
| **Occlusion Experiment** | Map softmax drop $\Delta P$ vs occluder $(x, y)$ | $\mathcal{O}(H W / \text{stride}^2)$ | Perturbation-based causal visual attribution | Proves network localizes the object, not background correlation. |
| **Fast R-CNN RoI Pool** | Maps variable $h \times w$ proposal to fixed $H \times W$ | Quantized sub-bin max-pooling | Single forward pass on full image | Eliminates running 2,000 independent CNN passes per image. |
| **Faster R-CNN RPN** | $k$ Anchor Boxes (3 scales $\times$ 3 aspect ratios) | Real-time ($\sim 0.2\text{s}$ / image) | In-network proposal network | Eliminates slow external **Selective Search** algorithm entirely. |
| **YOLO Single-Stage** | Output Tensor: $S \times S \times (5B + C)$ | 45 - 155 FPS (Ultra-fast) | Direct bounding box regression over spatial grid | Reframes detection as single-pass regression; lower precision on tiny objects. |

---

## 2. Core Mathematical Derivations to Memorize

### 2.1 Derivation: Inception $1 \times 1$ Bottleneck FLOP Reduction
**Objective**: Show why inserting a $1 \times 1$ conv before a $5 \times 5$ conv saves $>90\%$ of arithmetic operations.
1. Given input volume $H \times W \times C_{\text{in}}$, target output channels $C_{\text{out}}$, and filter size $F \times F$.
2. **Direct Standard Convolution FLOPs**:
   $$\text{FLOPs}_{\text{direct}} = H \cdot W \cdot (F \cdot F \cdot C_{\text{in}}) \cdot C_{\text{out}}$$
3. **Bottlenecked Pipeline (Project to $C_{\text{red}}$ via $1 \times 1$, then apply $F \times F$)**:
   $$\text{FLOPs}_{\text{step1}} = H \cdot W \cdot (1 \cdot 1 \cdot C_{\text{in}}) \cdot C_{\text{red}}$$
   $$\text{FLOPs}_{\text{step2}} = H \cdot W \cdot (F \cdot F \cdot C_{\text{red}}) \cdot C_{\text{out}}$$
   $$\text{FLOPs}_{\text{bottleneck}} = H \cdot W \cdot C_{\text{red}} \left( C_{\text{in}} + F^2 \cdot C_{\text{out}} \right)$$
4. **Concrete Ratio** (for $C_{\text{in}}=256, F=5, C_{\text{out}}=32, C_{\text{red}}=16$):
   $$\text{FLOPs}_{\text{direct}} \propto 5^2 \times 256 \times 32 = 204,800$$
   $$\text{FLOPs}_{\text{bottleneck}} \propto (1 \times 256 \times 16) + (5^2 \times 16 \times 32) = 4,096 + 12,800 = 16,896$$
   $$\text{Savings} = \frac{204,800 - 16,896}{204,800} = \mathbf{91.75\% \text{ reduction!}} \quad \blacksquare$$

---

### 2.2 Derivation: ResNet Non-Vanishing Gradient Proof
**Objective**: Prove that gradients backpropagating through a chain of residual blocks never vanish.
1. Forward recurrence from shallow layer $l$ to deeper layer $L$:
   $$\mathbf{x}_{l+1} = \mathbf{x}_l + \mathcal{F}(\mathbf{x}_l, W_l) \implies \mathbf{x}_L = \mathbf{x}_l + \sum_{i=l}^{L-1} \mathcal{F}(\mathbf{x}_i, W_i)$$
2. Applying the chain rule to compute gradient w.r.t. activation $\mathbf{x}_l$:
   $$\frac{\partial \mathcal{L}}{\partial \mathbf{x}_l} = \frac{\partial \mathcal{L}}{\partial \mathbf{x}_L} \frac{\partial \mathbf{x}_L}{\partial \mathbf{x}_l} = \frac{\partial \mathcal{L}}{\partial \mathbf{x}_L} \left( \frac{\partial}{\partial \mathbf{x}_l} \left( \mathbf{x}_l + \sum_{i=l}^{L-1} \mathcal{F}(\mathbf{x}_i, W_i) \right) \right)$$
3. Differentiating the sum:
   $$\frac{\partial \mathcal{L}}{\partial \mathbf{x}_l} = \frac{\partial \mathcal{L}}{\partial \mathbf{x}_L} \left( \mathbf{I} + \frac{\partial}{\partial \mathbf{x}_l} \sum_{i=l}^{L-1} \mathcal{F}(\mathbf{x}_i, W_i) \right)$$
4. Expanding the terms:
   $$\frac{\partial \mathcal{L}}{\partial \mathbf{x}_l} = \underbrace{\frac{\partial \mathcal{L}}{\partial \mathbf{x}_L}}_{\text{Unattenuated Clean Gradient}} + \underbrace{\frac{\partial \mathcal{L}}{\partial \mathbf{x}_L} \left( \frac{\partial}{\partial \mathbf{x}_l} \sum_{i=l}^{L-1} \mathcal{F}(\mathbf{x}_i, W_i) \right)}_{\text{Weight Modulated Gradient}}$$
5. Even if the weights $\mathcal{F}$ are very small (or zero), the identity term $\mathbf{I}$ ensures that $\frac{\partial \mathcal{L}}{\partial \mathbf{x}_l} \approx \frac{\partial \mathcal{L}}{\partial \mathbf{x}_L}$. Gradients never vanish, ensuring stable optimization across arbitrary depths. $\blacksquare$

---

### 2.3 Derivation: MobileNet Depthwise Separable Computation Ratio
**Objective**: Prove that depthwise separable convolution achieves an $\sim \frac{1}{D_K^2}$ computation reduction.
1. Let input be $D_F \times D_F \times M$, filter spatial size $D_K \times D_K$, and output channels $N$.
2. **Standard Conv Cost**:
   $$\text{Cost}_{\text{standard}} = D_K \cdot D_K \cdot M \cdot N \cdot D_F \cdot D_F$$
3. **Depthwise Separable Cost**:
   - Depthwise step (apply $D_K \times D_K \times 1$ to each of $M$ channels):
     $$\text{Cost}_{\text{depthwise}} = D_K \cdot D_K \cdot M \cdot D_F \cdot D_F$$
   - Pointwise step (apply $1 \times 1 \times M$ with $N$ filters):
     $$\text{Cost}_{\text{pointwise}} = M \cdot N \cdot D_F \cdot D_F$$
   - Combined Cost:
     $$\text{Cost}_{\text{separable}} = D_K^2 M D_F^2 + M N D_F^2$$
4. **Ratio of Costs**:
   $$\text{Ratio} = \frac{D_K^2 M D_F^2 + M N D_F^2}{D_K^2 M N D_F^2} = \frac{D_K^2 + N}{D_K^2 \cdot N} = \mathbf{\frac{1}{N} + \frac{1}{D_K^2}}$$
5. For $D_K = 3$ and $N \gg 1$:
   $$\text{Ratio} \approx \frac{1}{3^2} = \frac{1}{9} \implies \mathbf{\approx 88.9\% \text{ reduction in compute!}} \quad \blacksquare$$

---

## 3. High-Frequency Exam Traps & Pitfalls

> [!CAUTION]
> **Trap 1: The Degradation Problem is NOT Overfitting!**  
> When asked why a 56-layer plain network has worse error than a 20-layer plain network, many students answer "Overfitting because it has more parameters." **WRONG!**  
> In overfitting, training error decreases while test error increases. In the degradation problem, **training error itself increases**, proving it is an **optimization failure / vanishing gradient problem**, not overfitting.

> [!WARNING]
> **Trap 2: Addition in ResNet vs. Concatenation in DenseNet**  
> - **ResNet**: Performs **element-wise addition** ($\mathbf{y} = \mathcal{F}(\mathbf{x}) + \mathbf{x}$). Feature dimensions MUST match identically ($H, W, C$).  
> - **DenseNet**: Performs **depth-wise concatenation** ($\mathbf{y} = [\mathbf{x}_0, \mathbf{x}_1, \dots]$). Channel depth grows monotonically by growth rate $k$.

> [!IMPORTANT]
> **Trap 3: Fine-Tuning Small Datasets on Dissimilar Domains (Quadrant 4)**  
> If your target dataset is very small (e.g., 200 medical X-rays) and completely dissimilar to ImageNet, **DO NOT train a linear classifier on top of the last layer (FC7 or final pool)**. Deep layers encode domain-specific ImageNet semantic concepts (dogs, trucks). Instead, train your classifier on **mid-level convolutional activations (edges, textures)**.

> [!NOTE]
> **Trap 4: Smooth $L_1$ Loss vs. Standard $L_2$ Loss in Bounding Box Regression**  
> Fast R-CNN replaces $L_2$ loss ($0.5(y - \hat{y})^2$) with **Smooth $L_1$ loss**. Why? Because $L_2$ squared penalties explode on large outlier errors ($\nabla \to \infty$). Smooth $L_1$ transitions to linear $|x| - 0.5$ for $|x| \ge 1$, bounding gradients to $\pm 1$ and stabilizing regression.

---

## 4. Solved Review & Self-Assessment Questions (Q1 - Q9)

### Q1: The Degradation Problem
**Question**: Explain why simply stacking more layers in a plain CNN architecture eventually leads to higher training error, and name this phenomenon.  
**Model Answer**:  
This phenomenon is known as the **degradation problem**. As network depth increases in a plain CNN, repeated multiplications during backpropagation cause loss gradients to vanish (or explode) before reaching early layers. Because the early layers cannot update effectively, the deeper network cannot even learn the identity mapping of a shallower model, resulting in higher training error (underfitting). It is an optimization failure, not overfitting.

---

### Q2: 1x1 Convolutions in the Inception Module
**Question**: Mathematically, how does a $1 \times 1$ convolution reduce the computational load in the Inception Module?  
**Model Answer**:  
If an incoming feature map has shape $H \times W \times C_{\text{in}}$ (e.g., $56 \times 56 \times 64$), directly applying $C_{\text{out}} = 64$ filters of size $5 \times 5$ requires $(H \cdot W) \cdot (5 \times 5 \times 64) \cdot 64 \approx 102.7\text{M FLOPs}$. By first applying a $1 \times 1$ convolution with $C_{\text{red}} = 32$ filters, the volume collapses depth-wise to $56 \times 56 \times 32$ using only $H \cdot W \cdot 64 \cdot 32 \approx 6.4\text{M FLOPs}$. The subsequent $5 \times 5$ convolution now only processes depth 32, requiring $H \cdot W \cdot (5 \times 5 \times 32) \cdot 64 \approx 51.4\text{M FLOPs}$. Total computation drops from $102.7\text{M}$ to $57.8\text{M FLOPs}$, cutting compute by nearly $44\%$ without altering spatial dimensions.

---

### Q3: Residual Mapping vs. Plain Mapping
**Question**: Describe the structural difference between $H(x)$ in a standard plain network versus a ResNet block.  
**Model Answer**:  
In a standard plain network, the stacked convolutional layers are parameterized to learn the complete desired output mapping directly: $\mathcal{H}(\mathbf{x})$. In a ResNet block, an identity shortcut adds the input $\mathbf{x}$ directly to the layer transformation, forcing the layers to model only the residual difference: $\mathcal{F}(\mathbf{x}) \triangleq \mathcal{H}(\mathbf{x}) - \mathbf{x}$. The final output is $\mathcal{F}(\mathbf{x}) + \mathbf{x}$. If an identity mapping is optimal, driving residual weights to zero ($\mathcal{F} \to \mathbf{0}$) is substantially easier than learning an identity transformation from scratch.

---

### Q4: Auxiliary Classifiers in GoogLeNet
**Question**: What is the purpose of auxiliary classifiers in GoogLeNet?  
**Model Answer**:  
GoogLeNet is 22 layers deep. During backpropagation, gradients originating from the final softmax classification layer can attenuate significantly before reaching the earliest convolutional layers. GoogLeNet injected two auxiliary classification heads at intermediate layers during training. Their discounted losses ($0.3 \times \mathcal{L}_{\text{aux}}$) injected strong, fresh loss gradients directly into intermediate layers, mitigating vanishing gradients and regularizing the network. They are discarded during inference.

---

### Q5: Low-Level vs. Deep CNN Features
**Question**: Contrast the features learned by Layer 1 of a CNN versus those learned by deeper layers.  
**Model Answer**:  
- **Layer 1 (Low-Level)**: Filters consistently learn universal primitive visual features, specifically oriented Gabor-like edges (horizontal, vertical, diagonal) and opposing color blobs. These look identical across different vision datasets ("Gabor fatigue").  
- **Deeper Layers (High-Level)**: Intermediate layers combine edges into corners, geometric shapes, and mid-level textures (object parts like eyes, wheels, noses). The deepest layers assemble these parts into high-level semantic abstractions representing complete object classes (faces, dogs, cars).

---

### Q6: Occlusion Experiments
**Question**: How do Occlusion Experiments help in visualizing CNN decisions?  
**Model Answer**:  
An occlusion experiment (Zeiler & Fergus) systematically slides an opaque gray patch across every coordinate of an input image and records the resulting classification probability for the target class. Plotting these probabilities as a 2D heatmap localizes exactly which spatial pixels are causally responsible for the model's decision: when the occluder covers non-essential background context, probability remains high; when it occludes the actual object (e.g., dog face), probability sharply collapses. This confirms that the CNN has learned true object localization rather than background bias.

---

### Q7: R-CNN Bottleneck & Fast R-CNN Solution
**Question**: What was the major bottleneck in the original R-CNN framework, and how did Fast R-CNN resolve it?  
**Model Answer**:  
The original R-CNN ran Selective Search to generate $\sim 2,000$ region proposals per image, warped each proposal, and executed **2,000 separate forward passes through the CNN** for every single image, making inference glacial ($\sim 47$ seconds/image). Fast R-CNN resolved this by passing the entire input image through the CNN **only once** to produce a global convolutional feature map. Region proposals were projected onto this map, and **Region of Interest (RoI) Pooling** extracted fixed $7 \times 7$ feature vectors for each proposal, accelerating inference by $25\times$.

---

### Q8: Multi-Task Loss in Object Detectors
**Question**: Explain the Multi-task Loss in modern object detectors.  
**Model Answer**:  
Object detectors must perform two distinct tasks simultaneously: discrete categorical classification and continuous spatial bounding box localization. The multi-task loss combines both objectives into a single joint objective function:
$$\mathcal{L} = \mathcal{L}_{\text{cls}}(p, u) + \lambda [u \ge 1] \mathcal{L}_{\text{loc}}(t^u, v)$$
where $\mathcal{L}_{\text{cls}}$ is log cross-entropy loss over predicted class probabilities $p$ for true class $u$, $[u \ge 1]$ is an Iverson bracket that activates localization loss only for non-background foreground objects, and $\mathcal{L}_{\text{loc}}$ is Smooth $L_1$ loss between predicted box offsets $t^u$ and ground truth coordinates $v$.

---

### Q9: YOLO vs. The R-CNN Family
**Question**: How does YOLO differ fundamentally from the R-CNN family in its approach to Object Detection?  
**Model Answer**:  
The R-CNN family (R-CNN, Fast R-CNN, Faster R-CNN) uses a **two-stage pipeline**: first proposing candidate regions of interest (via Selective Search or an RPN), and then classifying and refining those proposals. In contrast, **YOLO (You Only Look Once)** is a **single-stage detector** that completely eliminates region proposals. It reframes detection as a **single unified regression problem**: the image is divided into an $S \times S$ grid, and in a single forward pass, each grid cell directly predicts bounding box coordinates, confidence scores, and class probabilities simultaneously. This yields ultra-fast real-time inference (45–155 FPS) with a slight trade-off in small object localization precision.


## High-frequency exam traps (from PYQs)

> [!WARNING]
> **Depthwise stage versus complete separable convolution:** For input channels $M$, output channels $N$, kernel width $k$, and feature-map width $D$, depthwise quantities are $k^2M$ parameters and $D^2k^2M$ MACs. Pointwise quantities are $MN$ parameters and $D^2MN$ MACs. A question asking for the *separable convolution total* requires summing both stages; several source keys in the PYQs report only the depthwise component despite asking for the total.

> [!CAUTION]
> **CAM versus Grad-CAM assumptions:** Original CAM requires a compatible classifier architecture with global average pooling before the linear class layer. Grad-CAM uses gradients of a target score with respect to convolutional feature maps and can be applied to a wider range of CNN architectures. Do not transfer CAM's architectural restriction to Grad-CAM or claim that Grad-CAM needs retraining.
