---
title: Deep Learning for Computer Vision Knowledge Map
tags: [dl4cv/moc]
---

# Deep Learning for Computer Vision — Master Knowledge Map

## Track Curriculum & Weekly Spine

| Week | Comprehensive Report | Fast Exam Revision Notes | Core Theoretical & Computational Focus | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Week 1** | [[month 1/week 1/week-1-report\|Week 1 Academic Report]] | [[month 1/week 1/week-1-exam-notes\|Week 1 Exam Notes]] | Foundations of Visual Signals, Linear Filtering, Frequency Analysis, and Discrete Sampling | **Complete** |
| **Week 2** | [[month 1/week 2/week-2-report\|Week 2 Academic Report]] | [[month 1/week 2/week-2-exam-notes\|Week 2 Exam Notes]] | Mid-Level Visual Primitives: Differential Edges, Scale-Space Blobs, Invariant Descriptors, and Primate Vision | **Complete** |
| **Week 3** | [[month 1/week 3/week-3-report\|Week 3 Academic Report]] | [[month 1/week 3/week-3-exam-notes\|Week 3 Exam Notes]] | Foundations of Deep Neural Networks: Perceptrons, Backpropagation, Optimization, Regularization & Normalization | **Complete** |
| **Week 4** | [[month 1/week 4/week-4-report\|Week 4 Academic Report]] | [[month 1/week 4/week-4-exam-notes\|Week 4 Exam Notes]] | Deep Convolutional Neural Networks: Tensor Calculus, Backprop Equations, Variants & Classic Architectures | **Complete** |
| **Week 5** | [[month 2/week 5/week-5-report\|Week 5 Academic Report]] | [[month 2/week 5/week-5-exam-notes\|Week 5 Exam Notes]] | Advanced CNNs (Inception, ResNet, MobileNet), Visual Interpretability, Transfer Learning & Object Detection | **Complete** |

---

## Curricular Architecture: Foundations to Deep Visual Learning

```mermaid
flowchart TD
    subgraph Week 1: Low-Level Signal Foundations
        M1["Course Intro & Perceptual Paradox"] --> M4["Image Representation & Point Ops"]
        M4 --> M5["Spatial Linear Filtering & Convolution"]
        M5 --> M6["Frequency Domain & Non-Linear Filters"]
        M6 --> M7["Sampling, Aliasing & Interpolation"]
    end

    subgraph Week 2: Mid-Level Invariant Primitives
        M7 --> W2_1["Differential Edge Detection & Canny Optimization"]
        W2_1 --> W2_2["Edgelets PCA & Second-Moment Eigendecomposition"]
        W2_2 --> W2_3["2D Interest Points & Harris Structure Tensor"]
        W2_3 --> W2_4["Scale-Space Theory, LoG, DoG & Image Pyramids"]
        W2_4 --> W2_5["Scale-Invariant Feature Transform (SIFT, SURF, GLOH)"]
        W2_5 --> W2_6["Visual Grouping & Segmentation (Watershed, Mean Shift, Graph Cuts)"]
        W2_6 --> W2_7["Geometric Shape Matching (Shape Context, MSER)"]
        W2_7 --> W2_8["Primate Visual Hierarchy (Retina, LGN, V1, Dual Streams)"]
    end

    subgraph Week 3: Deep Neural Foundations
        W2_8 --> W3_1["Early Neurons (MP, Perceptron & XOR Conundrum)"]
        W3_1 --> W3_2["Feedforward MLPs & Universal Approximation"]
        W3_2 --> W3_3["Activation Dynamics & Vanishing Gradients"]
        W3_3 --> W3_4["Multivariate Backpropagation Calculus"]
        W3_4 --> W3_5["Non-Convex Optimization (Momentum, NAG, Adam)"]
        W3_5 --> W3_6["Regularization (L1 vs L2 Unit Balls, Dropout Ensemble)"]
        W3_6 --> W3_7["Training Stabilization (He/Xavier Init & Batch Normalization)"]
    end

    subgraph Week 4: Convolutional Neural Networks
        W3_7 --> W4_1["Batch Normalization Backprop Calculus"]
        W4_1 --> W4_2["Spatial Inductive Biases (Receptive Fields, Weight Sharing)"]
        W4_2 --> W4_3["3D Tensor Convolution & Dimension Calculus"]
        W4_3 --> W4_4["CNN Backprop Calculus (dL/dW as Cross-Correlation, dL/dX as Flipped Conv)"]
        W4_4 --> W4_5["Pooling Routing Mechanics (Max Argmax Router vs Avg Uniform Distributor)"]
        W4_5 --> W4_6["Convolution Variants (Dilated Atrous & Transposed Upsampling)"]
        W4_6 --> W4_7["Classic Landmark Architectures (LeNet-5, AlexNet, ZFNet)"]
        W4_7 --> W4_8["VGGNet Uniformity & Receptive Field Stacking Equivalency"]
    end

    subgraph Week 5: Advanced Architectures, Interpretability & Detection
        W4_8 --> W5_1["Inception & 1x1 Bottleneck Dimensionality Reduction"]
        W5_1 --> W5_2["ResNet & Identity Shortcut Clean Gradient Superhighways"]
        W5_2 --> W5_3["Modern Paradigms (ResNeXt, DenseNet, MobileNet, SENet, ConvNeXt)"]
        W5_3 --> W5_4["Transfer Learning & 2x2 Decision Matrix"]
        W5_4 --> W5_5["Interpretability: Weights, Activations, t-SNE & Occlusion"]
        W5_5 --> W5_6["Object Detection: Viola-Jones to Two-Stage (R-CNN, Fast, Faster)"]
        W5_6 --> W5_7["Single-Stage Real-Time Detection: YOLO Grid Regression"]
    end
```

---

## Core Concept Spine

- **Week 1 Foundations:**
  - [[image-representation]] · [[point-operations]] · [[histogram-equalization]] · [[linear-filtering]] · [[cross-correlation]] · [[convolution]] · [[kernel-separability]] · [[normalized-cross-correlation]] · [[median-filter]] · [[bilateral-filter]] · [[fourier-transform]] · [[convolution-theorem]] · [[nyquist-shannon-sampling]] · [[image-aliasing]] · [[image-interpolation]]
- **Week 2 Mid-Level Primitives:**
  - [[canny-edge-detector]] · [[non-maximum-suppression]] · [[hysteresis-thresholding]] · [[edgelet-representation]] · [[harris-corner-detector]] · [[structure-tensor]] · [[scale-space-theory]] · [[difference-of-gaussians]] · [[sift-descriptor]] · [[surf-descriptor]] · [[gloh-descriptor]] · [[shape-context]] · [[mser-regions]] · [[gestalt-grouping]] · [[biological-visual-pathway]]
- **Week 3 Deep Neural Foundations:**
  - [[mcculloch-pitts-neuron]] · [[rosenblatt-perceptron]] · [[universal-approximation-theorem]] · [[activation-functions]] · [[backpropagation-algorithm]] · [[gradient-descent-variants]] · [[momentum-and-nesterov]] · [[adam-optimizer]] · [[l1-l2-regularization]] · [[dropout-regularization]] · [[symmetry-breaking]] · [[xavier-he-initialization]] · [[internal-covariate-shift]] · [[batch-normalization]]
- **Week 4 Convolutional Neural Networks:**
  - [[batchnorm-backprop]] · [[local-receptive-fields]] · [[weight-sharing]] · [[translation-equivariance]] · [[translation-invariance]] · [[3d-convolution-volume]] · [[dimension-calculus]] · [[dilated-convolution]] · [[transposed-convolution]] · [[cnn-backprop-weights]] · [[cnn-backprop-inputs]] · [[max-pooling-router]] · [[average-pooling-distributor]] · [[lenet-5]] · [[alexnet-architecture]] · [[local-response-normalization]] · [[zfnet-visualization]] · [[vggnet-architecture]] · [[receptive-field-stacking]]
- **Week 5 Advanced CNNs, Interpretability & Detection:**
  - [[inception-googlenet]] · [[bottleneck-1x1-convolutions]] · [[resnet-residual-learning]] · [[degradation-problem]] · [[identity-shortcut-gradient-flow]] · [[resnext-cardinality]] · [[densenet-feature-reuse]] · [[depthwise-separable-convolutions]] · [[efficientnet-compound-scaling]] · [[senet-squeeze-and-excitation]] · [[convnext-modern-cnn]] · [[transfer-learning-decision-matrix]] · [[cnn-visualization-techniques]] · [[occlusion-experiments]] · [[tsne-representation-space]] · [[object-detection-taxonomy]] · [[viola-jones-algorithm]] · [[rcnn-framework]] · [[fast-rcnn-roi-pooling]] · [[faster-rcnn-rpn-anchors]] · [[yolo-single-stage-detector]]

---

## Central Governing Paradigm

$$\mathbf{y} = \mathcal{F}(\mathbf{x}, \{W_i\}) + \mathbf{x} \implies \frac{\partial \mathcal{L}}{\partial \mathbf{x}_l} = \frac{\partial \mathcal{L}}{\partial \mathbf{x}_L} \left( \mathbf{I} + \frac{\partial}{\partial \mathbf{x}_l} \sum_{i=l}^{L-1} \mathcal{F}(\mathbf{x}_i, W_i) \right)$$

$$\text{Depthwise Separable Factorization}: \quad \frac{\text{Cost}_{\text{separable}}}{\text{Cost}_{\text{standard}}} = \frac{1}{N} + \frac{1}{D_K^2} \approx \frac{1}{9}$$

$$\text{Two-Stage Detection}: \quad \text{Image} \xrightarrow{\text{Backbone}} \text{Conv Features} \xrightarrow{\text{RPN}} \text{RoIs} \xrightarrow{\text{RoI Pooling}} \text{FCs} \to (\text{Softmax}, \operatorname{Smooth}_{L_1})$$

$$\text{Single-Stage Detection (YOLO)}: \quad \text{Image} \xrightarrow{\text{Single CNN}} S \times S \times (B \times 5 + C) \text{ Tensor}$$

Week 5 expands deep vision from rigid sequential classifiers to scalable, interpretable, and spatially grounded detection architectures. Residual learning resolves optimization degradation by establishing clean identity superhighways. Depthwise separable convolutions democratize deep vision for mobile hardware. Finally, region-based (R-CNN family) and single-shot (YOLO) detectors bridge high-level semantic representation with precise spatial localization.
