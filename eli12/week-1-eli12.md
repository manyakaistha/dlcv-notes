---
title: "Week 1 in plain language: how computers see pictures"
week: 1
status: complete
tags: [dl4cv/eli12, dl4cv/week-01]
---

# Week 1 in plain language: how computers see pictures

**Explain-like-I'm-12 version.** A picture looks obvious to you, but a computer starts with numbers. This note follows those numbers from light to pixels, filters and waves. For more detail, read the [full Week 1 report](../month%201/week%201/week-1-report.md) and the [exam notes](../month%201/week%201/week-1-exam-notes.md).

> **The big idea:** A picture is a measurement of light, not a complete description of the world. We can change its numbers or describe their patterns, but missing information cannot simply be wished back.

## 1. What is computer vision?

**Computer vision** means getting useful information from pictures or video. A program might label a picture “cat,” draw a box around the cat, or mark each pixel belonging to it. **Deep learning** uses a network of learned numerical operations to find useful patterns from examples. Training adjusts its numbers using feedback about its mistakes.

This is hard because one picture can have many possible explanations: a dark patch might be a shadow or dark paint. A cat also looks different when it turns around or moves into sunlight. The computer must infer the scene from incomplete clues.

**Remember:** Vision turns measured picture numbers into guesses about the world.

## 2. How light becomes an image

A lamp or the Sun sends light to an object; some light reflects from its surface and enters a camera. A lens focuses it onto a **sensor**, a surface that measures incoming light. The amount measured depends on both the light arriving at the object and what the surface reflects. A simple **pinhole camera** uses a tiny hole instead of a lens: rays crossing at the hole make an upside-down image on the back surface.

Think of a white shirt in a dim room and a grey shirt in a bright room: they can look similarly bright in a photograph. The image alone does not always tell us which cause is responsible.

**Remember:** Illumination, surface and camera together affect the picture.

## 3. Pictures as grids of numbers

A **pixel** is one position in a digital picture's grid. In a grayscale image, its number describes brightness: in a common 8-bit representation, 0 is black and 255 is white. A 2-by-3 grid has 2 rows, 3 columns and 6 pixels. **Quantization** means rounding a measured brightness to one of the allowed levels; 8 bits give 256 possible levels.

A colour image commonly stores three numbers at each position: red, green and blue (**RGB**). These are three **channels**, or separate grids of numbers. On a screen, mixing red and green light gives yellow; this is additive colour mixing. An image with height 2, width 3 and three channels therefore has 18 channel values.

**Remember:** Pixel position tells us where; channel values tell us the measured colour or brightness.

## 4. Changing brightness, one pixel at a time

A **point operation** changes each pixel using its own value. For example, adding 10 to a brightness of 40 gives 50; if the allowed range is 0–255, a result above 255 must be clipped to 255. **Contrast** describes how distinguishable light and dark values are. Stretching a narrow range of values can make differences easier to see, although it cannot recover detail already lost to clipping.

A **histogram** counts how many pixels have each brightness. **Histogram equalization** uses the running fraction of pixels at or below each brightness to spread values across the available range. It can improve contrast, but discrete values and repeated counts mean the resulting histogram need not be perfectly flat.

**Remember:** Point operations use one pixel at a time; a histogram counts brightness values.

## 5. Filters: a small window travels across the image

A **neighbourhood** is a small patch around a pixel. A **filter** makes an output from that patch. A **kernel** is the little grid of weights used by a linear filter: multiply matching entries and add the results. Imagine laying a stencil over a tiled floor and moving it one tile at a time.

For this patch, use a 3-by-3 kernel whose nine weights are each one ninth:

```text
patch             weights
1  2  3           1/9  1/9  1/9
4  5  6           1/9  1/9  1/9
7  8  9           1/9  1/9  1/9
```

The weighted sum is (1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9) / 9 = **5**. This is an average, so it smooths differences between neighbours. A filter is **linear** when scaling inputs scales outputs by the same amount and adding inputs adds their outputs.

The following complete check was run with `uv run python`:

```python
p = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
k = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
print('weighted sum:', sum(p[i][j] * k[i][j] for i in range(3) for j in range(3)))
print('average:', sum(map(sum, p)) / 9)
print('valid output side:', 5 - 3 + 1)
```

```text
weighted sum: 45
average: 5.0
valid output side: 3
```

The sum uses whole-number weights first; dividing by nine gives the stated average. For a 5-by-5 image, a 3-by-3 window moved one pixel at a time fits at 3 positions along each side, giving a 3-by-3 output if no extra border is added. That extra border is called **padding**; the number of pixels moved each step is the **stride**.

**Remember:** A linear filter combines neighbouring values using weights; window size, stride and padding affect the output size.

## 6. Correlation, convolution and useful shortcuts

**Cross-correlation** slides the kernel over the image as written. Mathematical **convolution** rotates the kernel by 180 degrees first, then performs the same multiply-and-add. For a symmetric kernel, such as the averaging kernel above, the rotation changes nothing. For a one-dimensional kernel `[2, -1, 3]`, the flipped kernel is `[3, -1, 2]`, so the distinction matters. Many deep-learning libraries call their correlation operation “convolution.”

Some kernels are **separable**: one horizontal pass followed by one vertical pass gives the same result as the two-dimensional kernel. For example, the rows `[1, 2, 1]`, `[2, 4, 2]`, `[1, 2, 1]` are formed by multiplying `[1, 2, 1]` by 1, 2 and 1. Two short passes can save work.

**Template matching** searches for a small example patch in a larger image. **Normalized cross-correlation** subtracts each patch's average and scales by its variation before comparing; it handles a uniform brightness shift and positive brightness scaling better than a raw weighted sum, provided neither patch is constant.

**Remember:** Convolution flips the kernel; correlation does not, and separable kernels can use two simpler passes.

## 7. Other ways to clean a picture

A **median filter** sorts the values in a neighbourhood and chooses the middle one. For `[1, 2, 100]`, the median is 2, while the average is about 34.3. It can remove isolated bright or dark specks without letting a single extreme value dominate. It is not a linear filter.

A **Gaussian filter** averages nearby pixels with smoothly decreasing weights as distance increases. A **bilateral filter** also gives less weight to pixels whose brightness differs greatly from the centre, so it can smooth within a region while better preserving a strong boundary. It is nonlinear because its weights depend on the image values.

An **integral image** is a table where each entry adds up the original pixels above and to its left, including itself. It helps find a rectangle's sum quickly by adding and subtracting a few table entries, rather than adding every pixel in the rectangle again.

**Remember:** Different filters solve different problems: averages smooth, medians reject isolated extremes, and bilateral weights respect brightness differences.

## 8. Pictures as mixtures of waves

Instead of listing brightness at each location, imagine building a picture by adding striped patterns. **Spatial frequency** says how quickly a pattern changes across distance: wide stripes are low frequency; tightly packed stripes are high frequency. The **Fourier transform** gives a recipe for combining waves of different frequencies and directions to describe the image. The **discrete Fourier transform (DFT)** does this for a finite grid; the **fast Fourier transform (FFT)** is a faster way to compute it.

For a row `[1, 1, 1, 1]`, there is no change across the row: its unscaled DFT has a constant component of 4 and zero at the other frequencies. **Magnitude** says how strong each wave is; **phase** says how it is shifted. Both are needed to reconstruct the picture, and phase strongly affects where structures appear.

The **convolution theorem** connects the two descriptions: convolution in the image grid corresponds to multiplying the matching Fourier values, with suitable padding and conventions for the desired boundaries. Smoothing reduces rapid changes, so it tends to weaken high frequencies.

**Remember:** The Fourier view describes a picture as a mixture of spatial waves; magnitude and phase both matter.

## 9. Sampling, aliasing and resizing

**Sampling** records the image at separate positions, like placing a grid over a painting and measuring at each grid point. If the grid is too coarse, fine stripes can masquerade as wider stripes or a strange **moiré** pattern. This confusion is **aliasing**: different continuous patterns can produce the same samples.

For a signal limited to frequencies below a known maximum, the sampling rate must be at least twice that maximum in the ideal sampling rule; exact recovery at the limiting boundary needs care, so in practice leave a margin. For example, a maximum of 3 cycles per millimetre calls for at least 6 samples per millimetre in that ideal rule. In two dimensions, check the sampling spacing in each direction.

When **downsampling** (keeping fewer pixels), first apply an **anti-aliasing filter**, a smoothing filter that suppresses detail too fine for the new grid. Smoothing after the reduction cannot reliably undo patterns already confused. When enlarging, **interpolation** estimates new values from old ones: nearest-neighbour copies the closest pixel, while bilinear interpolation blends nearby values. Neither can guarantee recovery of detail never recorded.

**Remember:** Smooth before reducing resolution, and sample fine enough to represent the detail you want.

## 10. Check yourself

1. Why can a dark patch be ambiguous? **Answer:** It could come from a dark surface, weak illumination, or another cause.
2. What is the average of the nine values 1 through 9? **Answer:** 5.
3. What happens to `[2, -1, 3]` before mathematical convolution? **Answer:** It is reversed to `[3, -1, 2]`.
4. Which wave component says where a pattern is shifted? **Answer:** Phase.
5. Why smooth before shrinking an image? **Answer:** To suppress detail that the coarser grid would confuse with other patterns.

**Remember:** Work from light to pixels, neighbourhoods, waves and sampling; each step has its own limits.

## Where this was asked

The links below cover the questions assigned **primary week 1** in the final manifest, grouped by the curriculum's topic names and ordered by the number of assigned questions. A flagged assignment may be uncertain; check the note on the question itself. Counts describe this manifest, not every question that could relate to Week 1.

### Spatial filtering and convolution (49 questions)

[da5006_2024T2_ET_AN Q255](../question-bank/week-01-questions.md#da5006_2024t2_et_an--q255--2-marks--id-640653904307) · [da5006_2024T2_ET_AN Q257](../question-bank/week-01-questions.md#da5006_2024t2_et_an--q257--2-marks--id-640653904321) · [da5006_2024T3_ET_AN Q208](../question-bank/week-01-questions.md#da5006_2024t3_et_an--q208--2-marks--id-6406531046071) · [da5006_2025T2_ET_AN Q85](../question-bank/week-01-questions.md#da5006_2025t2_et_an--q85--2-marks--id-6406531431345) · [da5006_2025T2_ET_AN Q92](../question-bank/week-01-questions.md#da5006_2025t2_et_an--q92--2-marks--id-6406531431352) · [da5006_2025T2_ET_FN Q166](../question-bank/week-01-questions.md#da5006_2025t2_et_fn--q166--2-marks--id-6406531422545) · [da5006_2025T2_ET_FN Q180](../question-bank/week-01-questions.md#da5006_2025t2_et_fn--q180--2-marks--id-6406531422559) · [da5006_2025T3_ET_FN Q13](../question-bank/week-01-questions.md#da5006_2025t3_et_fn--q13--1-marks--id-6406531862827) · [da5006_2026T1_ET_FN Q3](../question-bank/week-01-questions.md#da5006_2026t1_et_fn--q3--2-marks--id-6406532136818) · [da5006_2026T1_ET_FN Q4](../question-bank/week-01-questions.md#da5006_2026t1_et_fn--q4--2-marks--id-6406532136819) · [da5006_2026T2_ET_FN Q3](../question-bank/week-01-questions.md#da5006_2026t2_et_fn--q3--2-marks--id-6406532270042) · [da5006_2024T1_Q1_NA Q159](../question-bank/week-01-questions.md#da5006_2024t1_q1_na--q159--2-marks--id-640653739731) · [da5006_2024T1_Q1_NA Q160](../question-bank/week-01-questions.md#da5006_2024t1_q1_na--q160--2-marks--id-640653739735) · [da5006_2024T1_Q1_NA Q167](../question-bank/week-01-questions.md#da5006_2024t1_q1_na--q167--2-marks--id-640653739734) · [da5006_2024T1_Q1_NA Q170](../question-bank/week-01-questions.md#da5006_2024t1_q1_na--q170--2-marks--id-640653739733) · [da5006_2024T1_Q1_NA Q174](../question-bank/week-01-questions.md#da5006_2024t1_q1_na--q174--1-marks--id-640653739729) · [da5006_2024T1_Q1_NA Q175](../question-bank/week-01-questions.md#da5006_2024t1_q1_na--q175--1-marks--id-640653739730) · [da5006_2024T2_Q1_NA Q81](../question-bank/week-01-questions.md#da5006_2024t2_q1_na--q81--2-marks--id-640653829644) · [da5006_2024T2_Q1_NA Q82](../question-bank/week-01-questions.md#da5006_2024t2_q1_na--q82--2-marks--id-640653829647) · [da5006_2024T2_Q1_NA Q84](../question-bank/week-01-questions.md#da5006_2024t2_q1_na--q84--2-marks--id-640653829645) · [da5006_2024T2_Q1_NA Q85](../question-bank/week-01-questions.md#da5006_2024t2_q1_na--q85--2-marks--id-640653829648) · [da5006_2024T2_Q1_NA Q95](../question-bank/week-01-questions.md#da5006_2024t2_q1_na--q95--2-marks--id-640653829646) · [da5006_2024T2_Q1_NA Q99](../question-bank/week-01-questions.md#da5006_2024t2_q1_na--q99--1-marks--id-640653829651) · [da5006_2024T2_Q1_NA Q100](../question-bank/week-01-questions.md#da5006_2024t2_q1_na--q100--1-marks--id-640653829652) · [da5006_2024T3_Q1_NA Q145](../question-bank/week-01-questions.md#da5006_2024t3_q1_na--q145--2-marks--id-640653994483) · [da5006_2024T3_Q1_NA Q154](../question-bank/week-01-questions.md#da5006_2024t3_q1_na--q154--2-marks--id-640653994482) · [da5006_2024T3_Q1_NA Q155](../question-bank/week-01-questions.md#da5006_2024t3_q1_na--q155--2-marks--id-640653994485) · [da5006_2024T3_Q1_NA Q169](../question-bank/week-01-questions.md#da5006_2024t3_q1_na--q169--2-marks--id-640653994484) · [da5006_2025T1_Q1_NA Q156](../question-bank/week-01-questions.md#da5006_2025t1_q1_na--q156--2-marks--id-6406531130617) · [da5006_2025T1_Q1_NA Q162](../question-bank/week-01-questions.md#da5006_2025t1_q1_na--q162--2-marks--id-6406531130616) · [da5006_2025T1_Q1_NA Q170](../question-bank/week-01-questions.md#da5006_2025t1_q1_na--q170--2-marks--id-6406531130642) · [da5006_2025T1_Q1_NA Q171](../question-bank/week-01-questions.md#da5006_2025t1_q1_na--q171--2-marks--id-6406531130643) · [da5006_2025T1_Q1_NA Q176](../question-bank/week-01-questions.md#da5006_2025t1_q1_na--q176--2-marks--id-6406531130615) · [da5006_2025T1_Q1_NA Q177](../question-bank/week-01-questions.md#da5006_2025t1_q1_na--q177--2-marks--id-6406531130618) · [da5006_2025T2_Q1_NA Q159](../question-bank/week-01-questions.md#da5006_2025t2_q1_na--q159--2-marks--id-6406531279501) · [da5006_2025T2_Q1_NA Q160](../question-bank/week-01-questions.md#da5006_2025t2_q1_na--q160--2-marks--id-6406531279502) · [da5006_2025T2_Q1_NA Q173](../question-bank/week-01-questions.md#da5006_2025t2_q1_na--q173--3-marks--id-6406531279515) · [da5006_2025T2_Q1_NA Q174](../question-bank/week-01-questions.md#da5006_2025t2_q1_na--q174--3-marks--id-6406531279516) · [da5006_2025T2_Q1_NA Q176](../question-bank/week-01-questions.md#da5006_2025t2_q1_na--q176--3-marks--id-6406531279518) · [da5006_2026T1_Q1_NA Q5](../question-bank/week-01-questions.md#da5006_2026t1_q1_na--q5--1-marks--id-6406531961524) · [da5006_2026T1_Q1_NA Q7](../question-bank/week-01-questions.md#da5006_2026t1_q1_na--q7--1-marks--id-6406531961517) · [da5006_2026T1_Q1_NA Q13](../question-bank/week-01-questions.md#da5006_2026t1_q1_na--q13--1-marks--id-6406531961526) · [da5006_2026T2_Q1_NA Q5](../question-bank/week-01-questions.md#da5006_2026t2_q1_na--q5--1-marks--id-6406532166260) · [da5006_2026T2_Q1_NA Q7](../question-bank/week-01-questions.md#da5006_2026t2_q1_na--q7--1-marks--id-6406532166254) · [da5006_2026T2_Q1_NA Q12](../question-bank/week-01-questions.md#da5006_2026t2_q1_na--q12--1-marks--id-6406532166262) · [da5006_2024T3_Q2_NA Q138](../question-bank/week-01-questions.md#da5006_2024t3_q2_na--q138--2-marks--id-6406531031072) · [da5006_2025T1_Q2_NA Q242](../question-bank/week-01-questions.md#da5006_2025t1_q2_na--q242--2-marks--id-6406531168216) · [da5006_2025T2_Q2_NA Q234](../question-bank/week-01-questions.md#da5006_2025t2_q2_na--q234--2-marks--id-6406531333785) · [da5006_2025T3_Q2_NA Q130](../question-bank/week-01-questions.md#da5006_2025t3_q2_na--q130--2-marks--id-6406531815722)

### Image representation and point operations (29 questions)

[da5006_2024T1_ET_AN Q187](../question-bank/week-01-questions.md#da5006_2024t1_et_an--q187--2-marks--id-640653821613) · [da5006_2024T2_ET_AN Q261](../question-bank/week-01-questions.md#da5006_2024t2_et_an--q261--2-marks--id-640653904324) · [da5006_2024T3_ET_AN Q217](../question-bank/week-01-questions.md#da5006_2024t3_et_an--q217--2-marks--id-6406531046059) · [da5006_2024T3_ET_AN Q219](../question-bank/week-01-questions.md#da5006_2024t3_et_an--q219--2-marks--id-6406531046075) · [da5006_2025T2_ET_AN Q103](../question-bank/week-01-questions.md#da5006_2025t2_et_an--q103--2-marks--id-6406531431363) · [da5006_2025T2_ET_AN Q107](../question-bank/week-01-questions.md#da5006_2025t2_et_an--q107--2-marks--id-6406531431370) · [da5006_2025T2_ET_FN Q179](../question-bank/week-01-questions.md#da5006_2025t2_et_fn--q179--2-marks--id-6406531422558) · [da5006_2025T3_ET_FN Q3](../question-bank/week-01-questions.md#da5006_2025t3_et_fn--q3--1-marks--id-6406531862817) · [da5006_2026T1_ET_FN Q2](../question-bank/week-01-questions.md#da5006_2026t1_et_fn--q2--2-marks--id-6406532136817) · [da5006_2026T2_ET_FN Q2](../question-bank/week-01-questions.md#da5006_2026t2_et_fn--q2--2-marks--id-6406532270041) · [da5006_2024T1_Q1_NA Q169](../question-bank/week-01-questions.md#da5006_2024t1_q1_na--q169--2-marks--id-640653739732) · [da5006_2024T3_Q1_NA Q143](../question-bank/week-01-questions.md#da5006_2024t3_q1_na--q143--2-marks--id-640653994479) · [da5006_2024T3_Q1_NA Q144](../question-bank/week-01-questions.md#da5006_2024t3_q1_na--q144--2-marks--id-640653994480) · [da5006_2024T3_Q1_NA Q167](../question-bank/week-01-questions.md#da5006_2024t3_q1_na--q167--2-marks--id-640653994477) · [da5006_2024T3_Q1_NA Q168](../question-bank/week-01-questions.md#da5006_2024t3_q1_na--q168--2-marks--id-640653994478) · [da5006_2024T3_Q1_NA Q172](../question-bank/week-01-questions.md#da5006_2024t3_q1_na--q172--2-marks--id-640653994508) · [da5006_2025T1_Q1_NA Q154](../question-bank/week-01-questions.md#da5006_2025t1_q1_na--q154--2-marks--id-6406531130610) · [da5006_2025T1_Q1_NA Q155](../question-bank/week-01-questions.md#da5006_2025t1_q1_na--q155--2-marks--id-6406531130611) · [da5006_2025T1_Q1_NA Q161](../question-bank/week-01-questions.md#da5006_2025t1_q1_na--q161--2-marks--id-6406531130612) · [da5006_2025T1_Q1_NA Q174](../question-bank/week-01-questions.md#da5006_2025t1_q1_na--q174--2-marks--id-6406531130613) · [da5006_2025T2_Q1_NA Q157](../question-bank/week-01-questions.md#da5006_2025t2_q1_na--q157--2-marks--id-6406531279499) · [da5006_2025T2_Q1_NA Q158](../question-bank/week-01-questions.md#da5006_2025t2_q1_na--q158--2-marks--id-6406531279500) · [da5006_2025T2_Q1_NA Q183](../question-bank/week-01-questions.md#da5006_2025t2_q1_na--q183--3-marks--id-6406531279534) · [da5006_2025T2_Q1_NA Q184](../question-bank/week-01-questions.md#da5006_2025t2_q1_na--q184--3-marks--id-6406531279535) · [da5006_2026T1_Q1_NA Q8](../question-bank/week-01-questions.md#da5006_2026t1_q1_na--q8--1-marks--id-6406531961518) · [da5006_2026T1_Q1_NA Q9](../question-bank/week-01-questions.md#da5006_2026t1_q1_na--q9--1-marks--id-6406531961519) · [da5006_2026T1_Q1_NA Q10](../question-bank/week-01-questions.md#da5006_2026t1_q1_na--q10--1-marks--id-6406531961520) · [da5006_2026T2_Q1_NA Q8](../question-bank/week-01-questions.md#da5006_2026t2_q1_na--q8--1-marks--id-6406532166255) · [da5006_2026T2_Q1_NA Q9](../question-bank/week-01-questions.md#da5006_2026t2_q1_na--q9--1-marks--id-6406532166256)

### Frequency-domain images (1 questions)

[da5006_2024T2_Q1_NA Q86](../question-bank/week-01-questions.md#da5006_2024t2_q1_na--q86--2-marks--id-640653829649)

**Remember:** Try the linked questions after learning the idea, and use the worked explanations to check your reasoning.
