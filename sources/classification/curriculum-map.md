# Deep Learning for Computer Vision — Evidence-Based Curriculum Map (Weeks 1–12)

## Evidence boundary

The local course vault documents Weeks 1–5 only. The Knowledge Map marks all five complete and contains no Weeks 6–12 rows or source files. Weeks 6–12 below are therefore explicitly **unmapped**; their topics must not be treated as course content until source notes are found. There are no daily notes or raw weekly exports in this vault. “Detailed” coverage below describes the surviving report and exam-note headings, not a claim that every topic is fully or correctly taught.

## Week spine (1–12)

| Week | Evidence-backed scope / status | Main sources |
|---|---|---|
| 1 | Visual signal foundations: image representation, point operations, linear filtering/correlation/convolution, matching and nonlinear filters, Fourier analysis, sampling and interpolation. **Documented; complete per MOC.** | `Deep Learning for Computer Vision/month 1/week 1/week-1-report.md`; `.../week-1-exam-notes.md` |
| 2 | Classical mid-level primitives: edges/corners, scale space, invariant local descriptors, grouping/segmentation, shape descriptors, biological visual pathway. **Documented; complete per MOC.** | `Deep Learning for Computer Vision/month 1/week 2/week-2-report.md`; `.../week-2-exam-notes.md` |
| 3 | Neural-network foundations: perceptrons/MLPs, activations and gradients, backpropagation, optimization, regularization, initialization and batch normalization. **Documented; complete per MOC.** | `Deep Learning for Computer Vision/month 1/week 3/week-3-report.md`; `.../week-3-exam-notes.md` |
| 4 | CNN fundamentals: inductive biases, convolution tensor/dimension calculus and gradients, pooling, convolution variants, AlexNet/ZFNet/VGG and receptive fields. **Documented; complete per MOC.** | `Deep Learning for Computer Vision/month 1/week 4/week-4-report.md`; `.../week-4-exam-notes.md` |
| 5 | Advanced CNN architectures, transfer learning, interpretation/visualization, and object detection including R-CNN family and YOLO. **Documented; complete per MOC.** | `Deep Learning for Computer Vision/month 2/week 5/week-5-report.md`; `.../week-5-exam-notes.md` |
| 6 | **Unmapped.** No local week-6 report, exam notes, syllabus, or MOC entry. | No evidence located. |
| 7 | **Unmapped.** No local week-7 report, exam notes, syllabus, or MOC entry. | No evidence located. |
| 8 | **Unmapped.** No local week-8 report, exam notes, syllabus, or MOC entry. | No evidence located. |
| 9 | **Unmapped.** No local week-9 report, exam notes, syllabus, or MOC entry. | No evidence located. |
| 10 | **Unmapped.** No local week-10 report, exam notes, syllabus, or MOC entry. | No evidence located. |
| 11 | **Unmapped.** No local week-11 report, exam notes, syllabus, or MOC entry. | No evidence located. |
| 12 | **Unmapped.** No local week-12 report, exam notes, syllabus, or MOC entry. | No evidence located. |

## Detailed coverage: Weeks 1–5

### Week 1 — Visual signal and image-processing foundations

**Evidence / headings:** `month 1/week 1/week-1-report.md`, §§1–7: perception and vision bottlenecks; optional image formation; discrete image representation and point operations; spatial filtering, correlation vs convolution, separability and padding; template matching and nonlinear filtering; DFT, convolution theorem and phase/magnitude; sampling, aliasing, anti-aliasing and interpolation. §8 problem bank and §9 runnable verification suite. Exam condensation in `week-1-exam-notes.md`, §§1–4.

**Boundary:** Starts at image formation/representation and ends at reconstruction after sampling. This establishes signal-processing machinery; it does not cover learned feature extraction or neural-network training.

**Limitations:** Physical image formation is explicitly labeled optional in the report. The vault’s concept directory omits some MOC-linked concepts and this week has no daily notes/export, so the MOC is not proof of day-level sequencing.

### Week 2 — Classical mid-level visual primitives

**Evidence / headings:** `month 1/week 2/week-2-report.md`, §§1–9: abstraction/Marr and part-based representations; derivative edges and Canny; edgelets and PCA; Harris structure tensor; Gaussian scale space/LoG/DoG; SIFT and SIFT/SURF/GLOH/MOPS comparison; grouping and segmentation paradigms; Shape Context/MSER; primate visual hierarchy. §§10–11 problem bank and runnable suite. Exam notes `week-2-exam-notes.md`, §§1–4.

**Boundary:** Builds hand-designed local and mid-level representations on Week 1 signals, reaching biological hierarchy. It precedes learned deep representations; object detection is not yet the focus.

**Limitations:** The report heading promises broad segmentation paradigms but the vault has no concept notes for each listed method. “Complete” is the MOC status, not an independent validation of implementation or coverage.

### Week 3 — General neural-network foundations

**Evidence / headings:** `month 1/week 3/week-3-report.md`, §§1–7: McCulloch–Pitts/perceptron, linear separability and XOR; MLPs/universal approximation; activations/vanishing gradients; matrix-calculus backprop equations; nonconvex optimization including momentum/adaptive methods; L1/L2 and dropout; preprocessing, symmetry breaking, Xavier/He initialization and batch normalization. §§8–9 problem bank and runnable suite. Exam notes `week-3-exam-notes.md`, §§1–4.

**Boundary:** Moves from fixed handcrafted features to trainable neural representations and optimization. It supplies general learning machinery, before convolution-specific spatial structure in Week 4.

**Limitations:** General universal-approximation statements do not guarantee practical learnability, sample efficiency, or good optimization. Listed MOC concepts such as Adam and batch normalization are not all present as atomic files in the concept directory.

### Week 4 — Convolutional neural networks

**Evidence / headings:** `month 1/week 4/week-4-report.md`, Module 1 §§1.1–1.6 (BatchNorm backprop recap; FNN limits; CNN biases; 3D convolution; output dimensions; variants), Module 2 §§2.1–2.3 (filter/input/pooling gradients), Module 3 §§3.1–3.6 (ImageNet, AlexNet, ZFNet, VGG, receptive field equivalence, timeline), terminology, worked problems, executable suite. Exam notes `week-4-exam-notes.md`, §§1–4.

**Boundary:** Specializes Week 3’s learning rules to spatially structured tensors and classic image classifiers. It ends at classification-era CNN architecture progression; Week 5 expands architecture efficiency and detection.

**Limitations:** The MOC mentions LeNet-5 and pooling routing details, but report headings emphasize AlexNet/ZFNet/VGG; do not assume equal depth. The exam note and report are the only instructional artifacts found.

### Week 5 — Advanced architectures, interpretability, transfer, detection

**Evidence / headings:** `month 2/week 5/week-5-report.md`, Modules 1–5: Inception/GoogLeNet and ResNet; pre-activation, WRN, ResNeXt, DenseNet, MobileNet, SENet, ConvNeXt; transfer-learning decision matrix; weights/feature maps, activating patches, t-SNE and occlusion; detection hierarchy, Viola–Jones, R-CNN family, YOLO. Worked numerical problems, executable suite and readings. Exam notes `week-5-exam-notes.md`, §§1–4.

**Boundary:** Broadens CNN classification into compute-efficient families, model inspection, fine-tuning, and object localization/detection. YOLO and R-CNN are the last evidenced subject matter; no segmentation, video, 3D vision, or transformer curriculum is established by these sources.

**Limitations:** Several topics span distinct research eras and variants; headings alone do not establish which exact model versions are implemented. MOC mentions Faster R-CNN/RPN anchors, whereas report heading groups the family without a dedicated subsection for each variant. No course material for later weeks can be inferred from this endpoint.

## Source inventory and provenance

- Hub/spine and stated completion statuses: `Deep Learning for Computer Vision/Knowledge-Map.md` (“Track Curriculum & Weekly Spine”, “Curricular Architecture”, “Core Concept Spine”). Its architecture diagram ends at Week 5.
- Reports and exam notes: exact paths listed above. Reports contain problem banks and executable-suite headings, but no canonical `days/w<N>d<D>.md` notes or `week<N>-export.md` exports were present in the course file inventory.
- Concept notes: `Deep Learning for Computer Vision/notes/concepts/`. The current inventory is strongest for Weeks 1–2; absence of later-week concept files means the MOC’s full concept spine is not fully materialized as atomic notes.
- No `Deep Learning for Computer Vision/AGENTS.md` was found; root `AGENTS.md` governs the vault. This map is an extraction artifact, not a claim that the course vault meets every root quality criterion.
