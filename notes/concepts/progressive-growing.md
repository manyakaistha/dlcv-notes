---
title: "Progressive growing"
status: provisional
---

# Progressive growing

Progressive growing is a GAN training schedule that starts generator and discriminator at low image resolution and introduces higher-resolution blocks as learning proceeds. During each transition, a blending coefficient interpolates the previous path with the new path, reducing abrupt changes in the networks’ inputs and outputs. Coarse spatial structure can be learned before fine detail, and early iterations need not process the final resolution. Both networks must be adapted consistently; it is not simply a post-processing upsampler. The schedule is a practical optimization technique, not a theorem that training will converge or that the generator will cover every mode. **Why it matters here:** end-term questions distinguish increasing resolution and discovering global structure from freezing layers or guaranteeing unlimited diversity.

**Appears in:** [[week-10-report]] · [[week-10-exam-notes]] · [[week-10-questions]]

## Related

[[gan-mode-collapse]]
