---
title: Biological Visual Pathway and Cortical Processing
tags: [dl4cv/concept, biological-vision]
---
# The Primate Visual Pathway

The primate visual system processes optical signals through a hierarchical feedforward and recurrent neural architecture:

1. **Retina:** Photoreceptors (rods and cones) transduce photons into electrical potentials. Retinal ganglion cells perform spatial-temporal center-surround Difference of Gaussians (DoG) filtering.
2. **Lateral Geniculate Nucleus (LGN):**
   - **Magnocellular (M) Pathway:** Large receptive fields, high contrast sensitivity, fast temporal response (motion, depth, flickers).
   - **Parvocellular (P) Pathway:** Small receptive fields, wavelength-opponent (red-green, blue-yellow), high spatial resolution (color, fine detail, texture).
3. **Primary Visual Cortex (V1 / Striate Cortex):**
   - **Simple Cells:** Linear spatial summation, receptive fields modeled as oriented Gabor wavelets tuned to edge orientation and spatial frequency.
   - **Complex Cells:** Non-linear pooling over simple cells, maintaining orientation tuning with spatial phase invariance.
   - **Hypercomplex / End-Stopped Cells:** Sensitive to line length, corners, and curvature.
4. **Dual Cortical Streams:**
   - **Ventral Stream ("What" Pathway):** V1 $	o$ V2 $	o$ V4 $	o$ Inferotemporal (IT) Cortex (object recognition, category semantics).
   - **Dorsal Stream ("Where / How" Pathway):** V1 $	o$ V2 $	o$ MT/V5 $	o$ Posterior Parietal Cortex (spatial localization, optic flow, motion, robotic motor interaction).
