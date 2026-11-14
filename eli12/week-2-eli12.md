---
title: "Week 2 in plain language: finding useful clues in pictures"
week: 2
status: complete
tags: [dl4cv/eli12, dl4cv/week-02]
---

# Week 2 in plain language: finding useful clues in pictures

A picture is a grid of numbers, but a useful description might say “there is a corner here” or “this patch looks like a wheel.” This note builds those clues step by step. Read the [full Week 2 report](../month%201/week%202/week-2-report.md) for the mathematics and the [exam notes](../month%201/week%202/week-2-exam-notes.md) for revision.

> **The big idea:** Find changes, distinctive points and groups at several sizes, then describe them in ways that survive common changes in a picture.

## 1. Edges: where a picture changes

Imagine running a finger over a map from dark sea to bright land. An **edge** is a place where brightness changes sharply. A **gradient** records how quickly brightness changes in each direction; its direction points towards the fastest increase, and its size measures the strength of that change. It points across an edge, not along it.

For a tiny patch with rows `[1, 2, 3]`, `[2, 3, 4]`, `[3, 4, 5]`, estimate each change at the middle by subtracting opposite neighbours and dividing by two. The horizontal change is `(4 − 2)/2 = 1`, and the vertical change is also `(4 − 2)/2 = 1`. The gradient's size is $\sqrt{1^2+1^2}=\sqrt2$; it points diagonally towards increasing numbers. This is one particular **finite difference**, an estimate from nearby pixels.

A **filter** is a small set of weights slid across an image to calculate a new value at each position. Derivative filters estimate changes; Sobel filters combine a difference in one direction with some smoothing in the other. A **second derivative** measures how the first change itself changes. The **Laplacian** adds second derivatives in both image directions, and its sign changes can help locate edges. Random pixel fluctuations (**noise**) also cause changes, so differentiation can amplify them.

**Remember:** An edge is a sharp brightness change; the gradient points across it towards brighter pixels.

## 2. Canny: clean, thin, and connect

The Canny detector makes an edge map in stages:

1. Smooth with a **Gaussian** filter, a weighted average giving nearby pixels more influence. Its width, called sigma, controls the blur: more blur suppresses more noise but can hide fine edges.
2. Find gradient strength and direction using derivatives of the smoothed image.
3. Thin the wide responses using **non-maximum suppression**: keep a pixel only if it is a local peak compared with neighbours along the gradient direction.
4. Use two cutoffs (**hysteresis**): keep strong responses, also keep weak ones connected to strong ones, and discard weak isolated responses. Responses below the lower cutoff are discarded.

Think of the last step as keeping faint pencil marks only when they join a convincing line. A detected edge can still be a shadow or a texture change, not necessarily an object boundary.

**Remember:** Canny smooths, measures, thins, then connects using two thresholds.

## 3. From edges to corners

An **edgelet** is a short piece of an edge, summarized by its position, direction and length. It is like replacing a long dotted outline with little straight sticks. A method called **principal component analysis** (PCA) can find the dominant direction of the edgelet's pixel positions: the direction along which those positions spread most.

A straight edge is tricky to match: through a small window it can slide along itself and still look much the same. This is the **aperture problem**. A **corner**, where brightness changes in two directions, is more distinctive: sliding the window in either direction changes its contents.

The Harris detector collects horizontal and vertical gradients in a neighbourhood into a 2-by-2 **structure tensor** (a table of sums). For each pixel with horizontal change $I_x$ and vertical change $I_y$, add $I_x^2$ to the top left, $I_y^2$ to the bottom right, and $I_xI_y$ to each off-diagonal entry. Weights can give nearby pixels more influence. Its two **eigenvalues** describe the amounts of change in two special perpendicular directions: both small suggests flat, one large suggests an edge, and both large suggests a corner.

For a simple unweighted example, gradients `(2, 0)` and `(0, 2)` give the table `[[4, 0], [0, 4]]`. Harris uses $R=\det(A)-k\operatorname{tr}(A)^2$: $A$ is the table, determinant is `4×4 − 0×0 = 16`, trace is the diagonal sum `8`, and $k=0.04$ is a chosen sensitivity. Thus $R=16-0.04(8^2)=13.44$, a positive corner response. An edge-like table `[[4, 0], [0, 0]]` gives `−0.64`. In practice compare responses with a threshold and nearby positions; the sign alone is not a complete detector.

Rotating the image preserves the ideal Harris response, but changing image scale can change what fits inside the neighbourhood. Adding a constant brightness leaves gradients unchanged; multiplying brightness changes the response size, so a fixed threshold need not select the same points.

**Remember:** An edge changes strongly in one direction; a corner changes strongly in two.

## 4. Blobs, scale space and pyramids

A **blob** is a patch that differs from its surroundings, such as a dark dot on light paper. A tiny dot and a large dot need different-sized measuring windows. **Scale** means the size of the detail being examined. A **scale space** is a family of increasingly Gaussian-blurred versions of the same picture: fine detail fades as the blur grows.

The **Laplacian of Gaussian** (LoG) smooths and then measures the Laplacian. Comparing its suitably scale-normalized response across positions and blur sizes can find a blob's **characteristic scale**, the size at which its response is strongest. A **difference of Gaussians** (DoG) subtracts two nearby blur levels and approximates that normalized LoG up to a scale-step factor. For example, if one location is `0.8` after the first blur and `0.5` after the next, the second minus the first is `−0.3`. Reversing the subtraction reverses the sign.

An **image pyramid** stores images at successively smaller resolutions, often after smoothing before shrinking to reduce **aliasing**: false patterns caused by sampling fine detail too coarsely. An **octave** is a doubling of scale, commonly paired with halving image width and height. A **filter bank** applies several filters at different directions or sizes; their responses describe patterns such as stripes and textures. A Gaussian blur stack, a resized pyramid and a filter bank are related tools with different jobs.

**Remember:** Search at several scales because a feature's useful size changes with viewing distance.

## 5. SIFT: find a landmark, then describe it

A **keypoint** is a selected, repeatable location; a **descriptor** is a list of numbers describing its neighbourhood. Think of a keypoint as a landmark on a treasure map and its descriptor as the landmark's fingerprint. **SIFT** means Scale-Invariant Feature Transform. Its main steps are:

1. Build a Gaussian scale space and compare DoG values with neighbours in position and scale to find candidate peaks and dips.
2. Refine their location and scale; discard low-contrast points and unstable edge-like responses. A **Hessian** is a table of second derivatives used here to identify strongly uneven curvature.
3. Assign a main orientation from local gradient directions. Turn the local coordinate frame to that direction so a rotated picture can produce a similar description. Multiple strong directions can produce multiple orientations.
4. Divide the neighbourhood into a `4 × 4` grid. For each cell count gradient strengths into eight direction bins: `4 × 4 × 8 = 128` numbers. Normalize the list to reduce sensitivity to overall brightness contrast, with clipping and renormalization to limit very large entries.

Compare descriptors from two images to propose matches. Similar fingerprints can still be wrong on repeated windows or blank walls; a later geometric consistency check can reject mismatches. SIFT is designed to be robust to scale and rotation, and somewhat robust to illumination and viewpoint changes, not magically immune to every transformation.

**Remember:** SIFT locates repeatable points at a chosen scale and records a rotation-aligned local fingerprint.

## 6. SIFT's relatives and other ways to describe shape

**SURF** (Speeded-Up Robust Features) uses approximations and sums over rectangular image areas to speed feature calculations. **GLOH** (Gradient Location and Orientation Histogram) gathers gradient directions in a layout based on distance and angle around the point, then typically reduces the number of values with PCA. **MOPS** (Multi-Scale Oriented Patches) aligns and samples a normalized image patch as its descriptor. They trade detail, speed and resilience differently.

**Shape context** describes a point on an outline by counting other outline points in bins of direction and distance; nearby distances get finer divisions than faraway distances. Similar descriptions can suggest which points correspond across shapes. Missing outlines and clutter can confuse it.

**MSER** means Maximally Stable Extremal Regions. Imagine raising a brightness cutoff and watching connected dark regions grow. A region whose area changes unusually little over a range of cutoffs is a stable candidate. It describes a region, not simply a corner, and can fail if contrast or visibility changes too much.

**Remember:** Different descriptors keep different clues: gradient directions, patch brightness, outline relationships or stable regions.

## 7. Segmentation: dividing the picture into regions

**Segmentation** assigns pixels to groups, like cutting a picture into pieces. It does not automatically tell us an object's name. **Thresholding** separates pixels using a brightness cutoff; for `[2, 3, 8, 9]`, a cutoff of `5` puts the first two in one group and the last two in another. **Otsu's method** chooses a cutoff by looking for a strong separation between brightness groups. Uneven lighting can make one cutoff unreliable.

**Watershed** treats a suitably chosen image as a landscape: basins fill until they meet, forming boundaries. Noise can produce too many basins. **Mean shift** repeatedly moves a point towards nearby dense crowds of similar pixels in a chosen feature space; the space can include colour and position. A **graph cut** treats pixels as nodes joined by weighted links and divides them by optimizing a chosen grouping cost. Each method depends on the clues and settings it is given.

The **Gestalt** grouping ideas describe tendencies in perception: nearby or similar things tend to group together; smooth continuation and closure can make broken contours look connected. These are useful clues, not guarantees that a group is a real object.

**Remember:** Segmentation groups pixels using a rule; the quality of the groups depends on the rule and the image.

## 8. Human vision: a layered journey

Light reaches the **retina**, the light-sensitive layer at the back of the eye. **Rods** work well in dim light; **cones** support colour and detailed vision in brighter conditions. Retinal circuits compare neighbouring areas, helping emphasize changes in brightness. Signals travel through the optic nerve to the **lateral geniculate nucleus** (LGN), a relay in the thalamus, then to **V1**, the primary visual cortex at the back of the brain. Many V1 cells respond to edges at particular orientations.

Later visual processing has two broad, interacting routes: the **ventral** stream is strongly involved in recognizing what an object is, while the **dorsal** stream helps locate things and guide actions. Real vision involves feedback and interaction, so this is a useful simplified map, not two isolated wires. Computer vision borrows the idea of building complex descriptions from simpler clues, without reproducing the whole brain.

**Remember:** Visual processing builds from local signals toward richer information about objects and actions.

## 9. Check yourself

1. A gradient is `(3, 4)`. What is its strength? **5**, because $\sqrt{3^2+4^2}=5$.
2. Can a weak Canny response survive? **Yes**, if it passes the lower threshold and connects to a strong edge.
3. Why is a corner often easier to match than a straight edge? **It changes in two directions**, so its position is better constrained.
4. Why blur before shrinking? **To reduce fine detail that would otherwise alias** into false patterns.
5. Is segmentation the same as recognizing a cat? **No**: grouping pixels and naming the object are different jobs.

**Remember:** Explain the reason behind each answer, not just the vocabulary.

## Where this was asked

These links cover every question classified with primary Week 2 in the final manifest. Counts are questions, not marks; topic names follow the curriculum. The manifest assigns no primary Week 2 questions to Classical image segmentation or Human visual system.

### Edges and differential operators (54 questions)

- [da5006_2024T1_ET_AN Q161 (2 marks; ID 640653821587)](../question-bank/week-02-questions.md#da5006_2024t1_et_an--q161--2-marks--id-640653821587)
- [da5006_2024T2_ET_AN Q249 (2 marks; ID 640653904300)](../question-bank/week-02-questions.md#da5006_2024t2_et_an--q249--2-marks--id-640653904300)
- [da5006_2024T2_ET_AN Q250 (2 marks; ID 640653904302)](../question-bank/week-02-questions.md#da5006_2024t2_et_an--q250--2-marks--id-640653904302)
- [da5006_2024T2_ET_AN Q251 (2 marks; ID 640653904303)](../question-bank/week-02-questions.md#da5006_2024t2_et_an--q251--2-marks--id-640653904303)
- [da5006_2024T3_ET_AN Q206 (2 marks; ID 6406531046064)](../question-bank/week-02-questions.md#da5006_2024t3_et_an--q206--2-marks--id-6406531046064)
- [da5006_2024T3_ET_AN Q210 (2 marks; ID 6406531046073)](../question-bank/week-02-questions.md#da5006_2024t3_et_an--q210--2-marks--id-6406531046073)
- [da5006_2025T2_ET_AN Q91 (2 marks; ID 6406531431351)](../question-bank/week-02-questions.md#da5006_2025t2_et_an--q91--2-marks--id-6406531431351)
- [da5006_2025T2_ET_AN Q102 (2 marks; ID 6406531431362)](../question-bank/week-02-questions.md#da5006_2025t2_et_an--q102--2-marks--id-6406531431362)
- [da5006_2025T2_ET_FN Q156 (2 marks; ID 6406531422535)](../question-bank/week-02-questions.md#da5006_2025t2_et_fn--q156--2-marks--id-6406531422535)
- [da5006_2025T2_ET_FN Q157 (2 marks; ID 6406531422536)](../question-bank/week-02-questions.md#da5006_2025t2_et_fn--q157--2-marks--id-6406531422536)
- [da5006_2025T2_ET_FN Q158 (2 marks; ID 6406531422537)](../question-bank/week-02-questions.md#da5006_2025t2_et_fn--q158--2-marks--id-6406531422537)
- [da5006_2025T2_ET_FN Q176 (2 marks; ID 6406531422555)](../question-bank/week-02-questions.md#da5006_2025t2_et_fn--q176--2-marks--id-6406531422555)
- [da5006_2026T1_ET_FN Q5 (2 marks; ID 6406532136820)](../question-bank/week-02-questions.md#da5006_2026t1_et_fn--q5--2-marks--id-6406532136820)
- [da5006_2026T2_ET_FN Q4 (2 marks; ID 6406532270043)](../question-bank/week-02-questions.md#da5006_2026t2_et_fn--q4--2-marks--id-6406532270043)
- [da5006_2024T1_Q1_NA Q162 (2 marks; ID 640653739737)](../question-bank/week-02-questions.md#da5006_2024t1_q1_na--q162--2-marks--id-640653739737)
- [da5006_2024T1_Q1_NA Q168 (2 marks; ID 640653739741)](../question-bank/week-02-questions.md#da5006_2024t1_q1_na--q168--2-marks--id-640653739741)
- [da5006_2024T1_Q1_NA Q172 (2 marks; ID 640653739739)](../question-bank/week-02-questions.md#da5006_2024t1_q1_na--q172--2-marks--id-640653739739)
- [da5006_2024T1_Q1_NA Q173 (2 marks; ID 640653739740)](../question-bank/week-02-questions.md#da5006_2024t1_q1_na--q173--2-marks--id-640653739740)
- [da5006_2024T2_Q1_NA Q96 (2 marks; ID 640653829653)](../question-bank/week-02-questions.md#da5006_2024t2_q1_na--q96--2-marks--id-640653829653)
- [da5006_2024T2_Q1_NA Q101 (2 marks; ID 640653829657)](../question-bank/week-02-questions.md#da5006_2024t2_q1_na--q101--2-marks--id-640653829657)
- [da5006_2024T2_Q1_NA Q102 (1 marks; ID 640653829658)](../question-bank/week-02-questions.md#da5006_2024t2_q1_na--q102--1-marks--id-640653829658)
- [da5006_2024T2_Q1_NA Q103 (1 marks; ID 640653829659)](../question-bank/week-02-questions.md#da5006_2024t2_q1_na--q103--1-marks--id-640653829659)
- [da5006_2024T2_Q1_NA Q104 (2 marks; ID 640653829661)](../question-bank/week-02-questions.md#da5006_2024t2_q1_na--q104--2-marks--id-640653829661)
- [da5006_2024T2_Q1_NA Q105 (2 marks; ID 640653829662)](../question-bank/week-02-questions.md#da5006_2024t2_q1_na--q105--2-marks--id-640653829662)
- [da5006_2024T3_Q1_NA Q147 (2 marks; ID 640653994487)](../question-bank/week-02-questions.md#da5006_2024t3_q1_na--q147--2-marks--id-640653994487)
- [da5006_2024T3_Q1_NA Q158 (0.5 marks; ID 640653994492)](../question-bank/week-02-questions.md#da5006_2024t3_q1_na--q158--05-marks--id-640653994492)
- [da5006_2024T3_Q1_NA Q159 (0.5 marks; ID 640653994493)](../question-bank/week-02-questions.md#da5006_2024t3_q1_na--q159--05-marks--id-640653994493)
- [da5006_2024T3_Q1_NA Q160 (1 marks; ID 640653994494)](../question-bank/week-02-questions.md#da5006_2024t3_q1_na--q160--1-marks--id-640653994494)
- [da5006_2024T3_Q1_NA Q161 (1 marks; ID 640653994496)](../question-bank/week-02-questions.md#da5006_2024t3_q1_na--q161--1-marks--id-640653994496)
- [da5006_2024T3_Q1_NA Q162 (1 marks; ID 640653994497)](../question-bank/week-02-questions.md#da5006_2024t3_q1_na--q162--1-marks--id-640653994497)
- [da5006_2024T3_Q1_NA Q170 (2 marks; ID 640653994489)](../question-bank/week-02-questions.md#da5006_2024t3_q1_na--q170--2-marks--id-640653994489)
- [da5006_2025T1_Q1_NA Q157 (2 marks; ID 6406531130622)](../question-bank/week-02-questions.md#da5006_2025t1_q1_na--q157--2-marks--id-6406531130622)
- [da5006_2025T1_Q1_NA Q164 (2 marks; ID 6406531130620)](../question-bank/week-02-questions.md#da5006_2025t1_q1_na--q164--2-marks--id-6406531130620)
- [da5006_2025T1_Q1_NA Q173 (2 marks; ID 6406531130649)](../question-bank/week-02-questions.md#da5006_2025t1_q1_na--q173--2-marks--id-6406531130649)
- [da5006_2025T1_Q1_NA Q180 (1 marks; ID 6406531130625)](../question-bank/week-02-questions.md#da5006_2025t1_q1_na--q180--1-marks--id-6406531130625)
- [da5006_2025T1_Q1_NA Q181 (1 marks; ID 6406531130626)](../question-bank/week-02-questions.md#da5006_2025t1_q1_na--q181--1-marks--id-6406531130626)
- [da5006_2025T1_Q1_NA Q182 (1 marks; ID 6406531130628)](../question-bank/week-02-questions.md#da5006_2025t1_q1_na--q182--1-marks--id-6406531130628)
- [da5006_2025T1_Q1_NA Q183 (1 marks; ID 6406531130629)](../question-bank/week-02-questions.md#da5006_2025t1_q1_na--q183--1-marks--id-6406531130629)
- [da5006_2025T2_Q1_NA Q162 (2 marks; ID 6406531279504)](../question-bank/week-02-questions.md#da5006_2025t2_q1_na--q162--2-marks--id-6406531279504)
- [da5006_2025T2_Q1_NA Q164 (2 marks; ID 6406531279506)](../question-bank/week-02-questions.md#da5006_2025t2_q1_na--q164--2-marks--id-6406531279506)
- [da5006_2025T2_Q1_NA Q168 (2 marks; ID 6406531279510)](../question-bank/week-02-questions.md#da5006_2025t2_q1_na--q168--2-marks--id-6406531279510)
- [da5006_2025T2_Q1_NA Q169 (2 marks; ID 6406531279511)](../question-bank/week-02-questions.md#da5006_2025t2_q1_na--q169--2-marks--id-6406531279511)
- [da5006_2025T2_Q1_NA Q177 (3 marks; ID 6406531279519)](../question-bank/week-02-questions.md#da5006_2025t2_q1_na--q177--3-marks--id-6406531279519)
- [da5006_2025T2_Q1_NA Q178 (3 marks; ID 6406531279520)](../question-bank/week-02-questions.md#da5006_2025t2_q1_na--q178--3-marks--id-6406531279520)
- [da5006_2025T2_Q1_NA Q185 (1.5 marks; ID 6406531279522)](../question-bank/week-02-questions.md#da5006_2025t2_q1_na--q185--15-marks--id-6406531279522)
- [da5006_2025T2_Q1_NA Q186 (1.5 marks; ID 6406531279523)](../question-bank/week-02-questions.md#da5006_2025t2_q1_na--q186--15-marks--id-6406531279523)
- [da5006_2025T2_Q1_NA Q187 (1.5 marks; ID 6406531279525)](../question-bank/week-02-questions.md#da5006_2025t2_q1_na--q187--15-marks--id-6406531279525)
- [da5006_2025T2_Q1_NA Q188 (1.5 marks; ID 6406531279526)](../question-bank/week-02-questions.md#da5006_2025t2_q1_na--q188--15-marks--id-6406531279526)
- [da5006_2026T1_Q1_NA Q2 (1 marks; ID 6406531961516)](../question-bank/week-02-questions.md#da5006_2026t1_q1_na--q2--1-marks--id-6406531961516)
- [da5006_2026T1_Q1_NA Q14 (1 marks; ID 6406531961527)](../question-bank/week-02-questions.md#da5006_2026t1_q1_na--q14--1-marks--id-6406531961527)
- [da5006_2026T1_Q1_NA Q15 (1 marks; ID 6406531961528)](../question-bank/week-02-questions.md#da5006_2026t1_q1_na--q15--1-marks--id-6406531961528)
- [da5006_2026T2_Q1_NA Q2 (1 marks; ID 6406532166253)](../question-bank/week-02-questions.md#da5006_2026t2_q1_na--q2--1-marks--id-6406532166253)
- [da5006_2026T2_Q1_NA Q13 (1 marks; ID 6406532166263)](../question-bank/week-02-questions.md#da5006_2026t2_q1_na--q13--1-marks--id-6406532166263)
- [da5006_2026T2_Q1_NA Q14 (1 marks; ID 6406532166264)](../question-bank/week-02-questions.md#da5006_2026t2_q1_na--q14--1-marks--id-6406532166264)

**Remember:** Follow a link to read the full question and its context.

### Invariant features and geometric descriptors (49 questions)

- [da5006_2024T1_ET_AN Q162 (2 marks; ID 640653821588)](../question-bank/week-02-questions.md#da5006_2024t1_et_an--q162--2-marks--id-640653821588)
- [da5006_2024T1_ET_AN Q163 (2 marks; ID 640653821589)](../question-bank/week-02-questions.md#da5006_2024t1_et_an--q163--2-marks--id-640653821589)
- [da5006_2024T1_ET_AN Q164 (2 marks; ID 640653821590)](../question-bank/week-02-questions.md#da5006_2024t1_et_an--q164--2-marks--id-640653821590)
- [da5006_2024T1_ET_AN Q165 (2 marks; ID 640653821591)](../question-bank/week-02-questions.md#da5006_2024t1_et_an--q165--2-marks--id-640653821591)
- [da5006_2024T1_ET_AN Q166 (2 marks; ID 640653821592)](../question-bank/week-02-questions.md#da5006_2024t1_et_an--q166--2-marks--id-640653821592)
- [da5006_2024T2_ET_AN Q254 (2 marks; ID 640653904306)](../question-bank/week-02-questions.md#da5006_2024t2_et_an--q254--2-marks--id-640653904306)
- [da5006_2025T2_ET_FN Q161 (2 marks; ID 6406531422540)](../question-bank/week-02-questions.md#da5006_2025t2_et_fn--q161--2-marks--id-6406531422540)
- [da5006_2026T1_ET_FN Q6 (2 marks; ID 6406532136821)](../question-bank/week-02-questions.md#da5006_2026t1_et_fn--q6--2-marks--id-6406532136821)
- [da5006_2026T2_ET_FN Q6 (2 marks; ID 6406532270045)](../question-bank/week-02-questions.md#da5006_2026t2_et_fn--q6--2-marks--id-6406532270045)
- [da5006_2024T1_Q1_NA Q161 (2 marks; ID 640653739736)](../question-bank/week-02-questions.md#da5006_2024t1_q1_na--q161--2-marks--id-640653739736)
- [da5006_2024T1_Q1_NA Q164 (2 marks; ID 640653739748)](../question-bank/week-02-questions.md#da5006_2024t1_q1_na--q164--2-marks--id-640653739748)
- [da5006_2024T1_Q1_NA Q165 (2 marks; ID 640653739749)](../question-bank/week-02-questions.md#da5006_2024t1_q1_na--q165--2-marks--id-640653739749)
- [da5006_2024T1_Q1_NA Q166 (2 marks; ID 640653739750)](../question-bank/week-02-questions.md#da5006_2024t1_q1_na--q166--2-marks--id-640653739750)
- [da5006_2024T1_Q1_NA Q171 (2 marks; ID 640653739738)](../question-bank/week-02-questions.md#da5006_2024t1_q1_na--q171--2-marks--id-640653739738)
- [da5006_2024T1_Q1_NA Q176 (0.5 marks; ID 640653739744)](../question-bank/week-02-questions.md#da5006_2024t1_q1_na--q176--05-marks--id-640653739744)
- [da5006_2024T1_Q1_NA Q177 (0.5 marks; ID 640653739745)](../question-bank/week-02-questions.md#da5006_2024t1_q1_na--q177--05-marks--id-640653739745)
- [da5006_2024T1_Q1_NA Q178 (0.5 marks; ID 640653739746)](../question-bank/week-02-questions.md#da5006_2024t1_q1_na--q178--05-marks--id-640653739746)
- [da5006_2024T1_Q1_NA Q179 (0.5 marks; ID 640653739747)](../question-bank/week-02-questions.md#da5006_2024t1_q1_na--q179--05-marks--id-640653739747)
- [da5006_2024T1_Q1_NA Q180 (1 marks; ID 640653739752)](../question-bank/week-02-questions.md#da5006_2024t1_q1_na--q180--1-marks--id-640653739752)
- [da5006_2024T1_Q1_NA Q181 (1 marks; ID 640653739753)](../question-bank/week-02-questions.md#da5006_2024t1_q1_na--q181--1-marks--id-640653739753)
- [da5006_2024T2_Q1_NA Q87 (2 marks; ID 640653829654)](../question-bank/week-02-questions.md#da5006_2024t2_q1_na--q87--2-marks--id-640653829654)
- [da5006_2024T2_Q1_NA Q88 (2 marks; ID 640653829655)](../question-bank/week-02-questions.md#da5006_2024t2_q1_na--q88--2-marks--id-640653829655)
- [da5006_2024T2_Q1_NA Q90 (2 marks; ID 640653829669)](../question-bank/week-02-questions.md#da5006_2024t2_q1_na--q90--2-marks--id-640653829669)
- [da5006_2024T2_Q1_NA Q91 (2 marks; ID 640653829670)](../question-bank/week-02-questions.md#da5006_2024t2_q1_na--q91--2-marks--id-640653829670)
- [da5006_2024T2_Q1_NA Q92 (2 marks; ID 640653829671)](../question-bank/week-02-questions.md#da5006_2024t2_q1_na--q92--2-marks--id-640653829671)
- [da5006_2024T2_Q1_NA Q106 (1 marks; ID 640653829665)](../question-bank/week-02-questions.md#da5006_2024t2_q1_na--q106--1-marks--id-640653829665)
- [da5006_2024T2_Q1_NA Q107 (1 marks; ID 640653829666)](../question-bank/week-02-questions.md#da5006_2024t2_q1_na--q107--1-marks--id-640653829666)
- [da5006_2024T2_Q1_NA Q108 (1 marks; ID 640653829667)](../question-bank/week-02-questions.md#da5006_2024t2_q1_na--q108--1-marks--id-640653829667)
- [da5006_2024T2_Q1_NA Q109 (1 marks; ID 640653829668)](../question-bank/week-02-questions.md#da5006_2024t2_q1_na--q109--1-marks--id-640653829668)
- [da5006_2024T3_Q1_NA Q148 (2 marks; ID 640653994490)](../question-bank/week-02-questions.md#da5006_2024t3_q1_na--q148--2-marks--id-640653994490)
- [da5006_2024T3_Q1_NA Q150 (2 marks; ID 640653994504)](../question-bank/week-02-questions.md#da5006_2024t3_q1_na--q150--2-marks--id-640653994504)
- [da5006_2024T3_Q1_NA Q163 (0.5 marks; ID 640653994500)](../question-bank/week-02-questions.md#da5006_2024t3_q1_na--q163--05-marks--id-640653994500)
- [da5006_2024T3_Q1_NA Q164 (0.5 marks; ID 640653994501)](../question-bank/week-02-questions.md#da5006_2024t3_q1_na--q164--05-marks--id-640653994501)
- [da5006_2024T3_Q1_NA Q165 (0.5 marks; ID 640653994502)](../question-bank/week-02-questions.md#da5006_2024t3_q1_na--q165--05-marks--id-640653994502)
- [da5006_2024T3_Q1_NA Q166 (0.5 marks; ID 640653994503)](../question-bank/week-02-questions.md#da5006_2024t3_q1_na--q166--05-marks--id-640653994503)
- [da5006_2025T1_Q1_NA Q165 (2 marks; ID 6406531130623)](../question-bank/week-02-questions.md#da5006_2025t1_q1_na--q165--2-marks--id-6406531130623)
- [da5006_2025T1_Q1_NA Q167 (2 marks; ID 6406531130636)](../question-bank/week-02-questions.md#da5006_2025t1_q1_na--q167--2-marks--id-6406531130636)
- [da5006_2025T1_Q1_NA Q184 (0.5 marks; ID 6406531130632)](../question-bank/week-02-questions.md#da5006_2025t1_q1_na--q184--05-marks--id-6406531130632)
- [da5006_2025T1_Q1_NA Q185 (0.5 marks; ID 6406531130633)](../question-bank/week-02-questions.md#da5006_2025t1_q1_na--q185--05-marks--id-6406531130633)
- [da5006_2025T1_Q1_NA Q186 (0.5 marks; ID 6406531130634)](../question-bank/week-02-questions.md#da5006_2025t1_q1_na--q186--05-marks--id-6406531130634)
- [da5006_2025T1_Q1_NA Q187 (0.5 marks; ID 6406531130635)](../question-bank/week-02-questions.md#da5006_2025t1_q1_na--q187--05-marks--id-6406531130635)
- [da5006_2025T2_Q1_NA Q163 (2 marks; ID 6406531279505)](../question-bank/week-02-questions.md#da5006_2025t2_q1_na--q163--2-marks--id-6406531279505)
- [da5006_2025T2_Q1_NA Q189 (1.5 marks; ID 6406531279528)](../question-bank/week-02-questions.md#da5006_2025t2_q1_na--q189--15-marks--id-6406531279528)
- [da5006_2025T2_Q1_NA Q190 (1.5 marks; ID 6406531279529)](../question-bank/week-02-questions.md#da5006_2025t2_q1_na--q190--15-marks--id-6406531279529)
- [da5006_2026T1_Q1_NA Q4 (1 marks; ID 6406531961523)](../question-bank/week-02-questions.md#da5006_2026t1_q1_na--q4--1-marks--id-6406531961523)
- [da5006_2026T1_Q1_NA Q12 (1 marks; ID 6406531961525)](../question-bank/week-02-questions.md#da5006_2026t1_q1_na--q12--1-marks--id-6406531961525)
- [da5006_2026T2_Q1_NA Q4 (1 marks; ID 6406532166259)](../question-bank/week-02-questions.md#da5006_2026t2_q1_na--q4--1-marks--id-6406532166259)
- [da5006_2026T2_Q1_NA Q11 (1 marks; ID 6406532166261)](../question-bank/week-02-questions.md#da5006_2026t2_q1_na--q11--1-marks--id-6406532166261)
- [da5006_2024T1_Q2_NA Q162 (2 marks; ID 640653766158)](../question-bank/week-02-questions.md#da5006_2024t1_q2_na--q162--2-marks--id-640653766158)

**Remember:** Follow a link to read the full question and its context.

### Scale space, pyramids and filter banks (8 questions)

- [da5006_2024T1_ET_AN Q188 (2 marks; ID 640653821614)](../question-bank/week-02-questions.md#da5006_2024t1_et_an--q188--2-marks--id-640653821614)
- [da5006_2024T2_ET_AN Q260 (2 marks; ID 640653904301)](../question-bank/week-02-questions.md#da5006_2024t2_et_an--q260--2-marks--id-640653904301)
- [da5006_2025T2_ET_AN Q93 (2 marks; ID 6406531431353)](../question-bank/week-02-questions.md#da5006_2025t2_et_an--q93--2-marks--id-6406531431353)
- [da5006_2025T2_ET_FN Q167 (2 marks; ID 6406531422546)](../question-bank/week-02-questions.md#da5006_2025t2_et_fn--q167--2-marks--id-6406531422546)
- [da5006_2026T1_ET_FN Q7 (2 marks; ID 6406532136822)](../question-bank/week-02-questions.md#da5006_2026t1_et_fn--q7--2-marks--id-6406532136822)
- [da5006_2026T2_ET_FN Q5 (2 marks; ID 6406532270044)](../question-bank/week-02-questions.md#da5006_2026t2_et_fn--q5--2-marks--id-6406532270044)
- [da5006_2026T2_ET_FN Q22 (3 marks; ID 6406532270061)](../question-bank/week-02-questions.md#da5006_2026t2_et_fn--q22--3-marks--id-6406532270061)
- [da5006_2026T2_ET_FN Q31 (4 marks; ID 6406532270070)](../question-bank/week-02-questions.md#da5006_2026t2_et_fn--q31--4-marks--id-6406532270070)

**Remember:** Follow a link to read the full question and its context.

### Corners and blobs (7 questions)

- [da5006_2024T1_ET_AN Q186 (2 marks; ID 640653821608)](../question-bank/week-02-questions.md#da5006_2024t1_et_an--q186--2-marks--id-640653821608)
- [da5006_2026T1_ET_FN Q16 (3 marks; ID 6406532136831)](../question-bank/week-02-questions.md#da5006_2026t1_et_fn--q16--3-marks--id-6406532136831)
- [da5006_2024T1_Q1_NA Q163 (2 marks; ID 640653739742)](../question-bank/week-02-questions.md#da5006_2024t1_q1_na--q163--2-marks--id-640653739742)
- [da5006_2024T2_Q1_NA Q89 (2 marks; ID 640653829663)](../question-bank/week-02-questions.md#da5006_2024t2_q1_na--q89--2-marks--id-640653829663)
- [da5006_2024T3_Q1_NA Q149 (2 marks; ID 640653994498)](../question-bank/week-02-questions.md#da5006_2024t3_q1_na--q149--2-marks--id-640653994498)
- [da5006_2025T1_Q1_NA Q166 (2 marks; ID 6406531130630)](../question-bank/week-02-questions.md#da5006_2025t1_q1_na--q166--2-marks--id-6406531130630)
- [da5006_2025T2_Q1_NA Q170 (2 marks; ID 6406531279512)](../question-bank/week-02-questions.md#da5006_2025t2_q1_na--q170--2-marks--id-6406531279512)

**Remember:** Follow a link to read the full question and its context.
