---
title: "Week 4 in plain language: how CNNs look at pictures"
week: 4
status: complete
tags: [dl4cv/eli12, dl4cv/week-04, deep-learning/cnn]
---

# Week 4 in plain language: how CNNs look at pictures

**Explain-like-I'm-12 version.** This is a gentle first pass through the [full Week 4 report](../month%201/week%204/week-4-report.md). For exam formulas and further examples, read the [exam notes](../month%201/week%204/week-4-exam-notes.md), then try the questions at the end.

> **The big idea.** A convolutional neural network (CNN) learns little pattern detectors, uses them all over a picture, and combines their clues to make a prediction.

## 1. A little window looking for clues

A picture is a grid of **pixels**, or tiny picture elements, each represented by numbers. A **neural network** is a chain of steps with adjustable numbers that learns from examples. A CNN starts by looking at small patches: a nearby group of pixels is often useful for spotting an edge or a corner.

A **filter** (also called a **kernel**) is a small grid of adjustable numbers called **weights**. Put it over a patch, multiply matching numbers and add the results. Slide it to the next position and repeat. This operation is called a **convolution** in CNNs; most libraries actually use the unflipped filter, a calculation also called cross-correlation. The grid of answers is a **feature map**: a map showing where that filter responds strongly.

The same weights are reused at every position: this is **weight sharing**, like using one stamp across a page. It saves stored weights and lets the same detector look anywhere. Moving a pattern can move its response on the map; this is called **translation equivariance**. Edges, padding and larger strides can limit this neat behaviour. It does not mean the final answer is guaranteed to stay the same when an object moves.

**Remember:** One shared filter examines many small patches and produces one feature map.

## 2. Channels: a stack of maps

A **channel** is one layer of numbers in a picture or feature stack. A colour image commonly has three channels: red, green and blue. Think of three transparent sheets stacked together. A standard filter covers a small height and width but reaches through **all** input channels; it adds the matching products across all the sheets to make one number at each position.

One filter makes one output channel. Four different filters make four feature maps, even when the input has three channels. A later layer can combine earlier maps into more complicated clues.

**Remember:** Input channels determine each filter's depth; the number of filters determines output channels.

## 3. Stride, padding and output size

**Stride** is the number of pixels the window moves each step. **Padding** adds a border, often of zeros, around the input. A wider stride usually gives a smaller map; padding lets the filter visit edge pixels more and can preserve map size.

For one direction, with input size $N$, filter size $F$, padding $P$ on **each** side and stride $S$, the output size is $\lfloor(N+2P-F)/S\rfloor+1$. The floor symbols mean round down. The final 1 counts the starting position. This version assumes a normal, undilated filter and a window that fits. Apply it separately to height and width, and again at each layer.

Example: a 7-pixel side, filter size 3, padding 1 and stride 2 gives $\lfloor(7+2-3)/2\rfloor+1=4$. So a `7 × 7` input becomes a `4 × 4` map per filter. For stride 1, a size-3 filter and padding 1 preserve the spatial size.

**Remember:** Subtract the filter from the padded size, divide by stride, round down, and add one.

## 4. Counting the adjustable numbers

A **parameter** is a number the network can learn. Besides weights, a filter often has one **bias**, an adjustable number added to every output it produces. With standard square filters, the count including bias is $(F \times F \times C_{in}+1)\times C_{out}$: filter width times height times input channels, plus one bias, times the number of filters. Leave out the plus one if the question says there is no bias.

For four `3 × 3` filters on a three-channel image, each filter has `3 × 3 × 3 = 27` weights and one bias. Four filters have `4 × 28 = 112` parameters. The same weights are reused across the picture, so making the picture taller does not increase this count.

**Remember:** Count all input channels and one bias per filter, not one bias per output pixel.

## 5. Pooling: keep a smaller summary

**Pooling** summarises each small window of a feature map. **Max pooling** keeps its largest number; **average pooling** keeps its average. Pooling is usually done separately on each channel and has no learned weights. It reduces spatial size and may make the representation less sensitive to small shifts, but it throws away detail and does not promise perfect shift invariance.

Here is one complete hand calculation. Use a `2 × 2` filter of all ones, stride 1, no padding and no bias on this one-channel `4 × 4` patch:

```text
Input                 Filter
 1  2  3  4            1  1
 5  6  7  8            1  1
 9 10 11 12
13 14 15 16
```

The first window adds `1 + 2 + 5 + 6 = 14`. Slide the filter to obtain:

```text
14 18 22
30 34 38
46 50 54
```

Now use `2 × 2` max pooling with stride 2 and no padding. Only one whole window fits: `14, 18, 30, 34`. Its maximum is **34**; the unused last row and column do not fit another complete window.

The following self-contained check was run with `uv run --no-project python`:

```python
x = [[4*i+j+1 for j in range(4)] for i in range(4)]
y = [[sum(x[i+a][j+b] for a in range(2) for b in range(2)) for j in range(3)] for i in range(3)]
p = max(y[i][j] for i in range(2) for j in range(2))
size = (7 - 3 + 2*1)//2 + 1
params = (3*3*3+1)*4
assert (size, params, y, p) == (4, 112, [[14,18,22],[30,34,38],[46,50,54]], 34)
print('output size:', size)
print('parameters:', params)
print('convolution:', y)
print('max pool:', p)
```

```text
output size: 4
parameters: 112
convolution: [[14, 18, 22], [30, 34, 38], [46, 50, 54]]
max pool: 34
```

**Remember:** Convolution makes a map of filter responses; max pooling keeps the largest response in each window.

## 6. How the filters learn: backpropagation

A **loss** is a number measuring how wrong a prediction is. A **gradient** says how a small change in a number would change that loss. **Backpropagation** works backwards from the loss, passing these messages through each step so the network can adjust its weights to reduce the loss.

Think of one shared stamp used in many places: each use contributes to the advice for changing that stamp. The filter weight's gradient adds contributions from every position where it was used. An input pixel can also affect several overlapping windows, so its backward messages add together. In max pooling, the message goes to the winning position of each window; in average pooling it is shared equally. If windows overlap, contributions add. When maxima tie, the implementation chooses how to route the message.

For example, if the `2 × 2` max-pool window above receives a backward message of 6, the position containing 34 receives 6 and the other three receive 0. For average pooling, each receives `6 / 4 = 1.5`.

**Remember:** Add the advice from every use of a shared weight; pooling sends advice back according to its own rule.

## 7. AlexNet and VGG: two famous recipes

An **architecture** is the arrangement of a network's layers. **Image classification** means choosing a category for a whole image, such as cat or dog. AlexNet, a landmark 2012 classifier, used five convolution layers followed by three **fully connected** layers, where each output connects to every input from the preceding layer. It used filters of different sizes, including `11 × 11`, `5 × 5` and `3 × 3`, and overlapping max-pool windows. It also used **ReLU**, a rule that replaces negative values with zero, and **dropout**, which temporarily leaves out some units during training to help reduce memorisation of the training examples.

VGG, introduced in 2014, favoured stacks of small `3 × 3` filters and `2 × 2` max pooling. A **receptive field** is the part of the original input that can affect one output. Three stride-1 `3 × 3` layers have a `7 × 7` receptive field: the widths grow 3, 5, then 7. This is the same span as one `7 × 7` filter, not the same computation. With the same number of channels throughout and ignoring biases, three small layers use `27 × C × C` weights versus `49 × C × C` for one large layer, where $C$ is the channel count. ReLUs between the small layers add extra decision-making steps. VGG-16 has more total parameters than AlexNet, despite this local comparison.

**Remember:** AlexNet mixes filter sizes; VGG builds wider views by stacking small filters.

## Check yourself

1. A `5 × 5` input uses a `3 × 3` filter, stride 1, no padding. What is the output size? **`3 × 3`**, since `(5 − 3)/1 + 1 = 3` per side.
2. How many output maps do six filters make? **Six**, regardless of the number of input channels.
3. Why does a shared weight collect several backward contributions? **It was used at several positions.**
4. Is pooling perfectly shift-invariant? **No**; a small move may still change a window's summary.

**Remember:** Check spatial size, channels, bias and the backward route separately.

## Where this was asked

The links below cover questions classified with Week 4 as their primary week. Groups are ordered by the number of those questions; a question can test more than its assigned topic.

### CNN operations and spatial dimensions (34 questions)

- [da5006_2024T2_ET_AN Q262](../question-bank/week-04-questions.md#da5006_2024t2_et_an--q262--2-marks--id-640653904325)
- [da5006_2024T3_ET_AN Q218](../question-bank/week-04-questions.md#da5006_2024t3_et_an--q218--2-marks--id-6406531046065)
- [da5006_2025T2_ET_AN Q108](../question-bank/week-04-questions.md#da5006_2025t2_et_an--q108--2-marks--id-6406531431371)
- [da5006_2025T2_ET_FN Q184](../question-bank/week-04-questions.md#da5006_2025t2_et_fn--q184--2-marks--id-6406531422573)
- [da5006_2025T3_ET_FN Q2](../question-bank/week-04-questions.md#da5006_2025t3_et_fn--q2--1-marks--id-6406531862816)
- [da5006_2025T3_ET_FN Q14](../question-bank/week-04-questions.md#da5006_2025t3_et_fn--q14--1-marks--id-6406531862828)
- [da5006_2026T1_ET_FN Q11](../question-bank/week-04-questions.md#da5006_2026t1_et_fn--q11--2-marks--id-6406532136826)
- [da5006_2026T1_ET_FN Q21](../question-bank/week-04-questions.md#da5006_2026t1_et_fn--q21--4-marks--id-6406532136836)
- [da5006_2026T2_ET_FN Q10](../question-bank/week-04-questions.md#da5006_2026t2_et_fn--q10--2-marks--id-6406532270049)
- [da5006_2026T2_ET_FN Q30](../question-bank/week-04-questions.md#da5006_2026t2_et_fn--q30--4-marks--id-6406532270069)
- [da5006_2026T2_ET_FN Q33](../question-bank/week-04-questions.md#da5006_2026t2_et_fn--q33--4-marks--id-6406532270072)
- [da5006_2024T2_Q1_NA Q97](../question-bank/week-04-questions.md#da5006_2024t2_q1_na--q97--2-marks--id-640653829674)
- [da5006_2024T2_Q1_NA Q98](../question-bank/week-04-questions.md#da5006_2024t2_q1_na--q98--2-marks--id-640653829675)
- [da5006_2024T3_Q1_NA Q171](../question-bank/week-04-questions.md#da5006_2024t3_q1_na--q171--2-marks--id-640653994507)
- [da5006_2025T1_Q1_NA Q158](../question-bank/week-04-questions.md#da5006_2025t1_q1_na--q158--2-marks--id-6406531130639)
- [da5006_2025T1_Q1_NA Q159](../question-bank/week-04-questions.md#da5006_2025t1_q1_na--q159--2-marks--id-6406531130640)
- [da5006_2025T2_Q1_NA Q180](../question-bank/week-04-questions.md#da5006_2025t2_q1_na--q180--3-marks--id-6406531279531)
- [da5006_2025T2_Q1_NA Q181](../question-bank/week-04-questions.md#da5006_2025t2_q1_na--q181--3-marks--id-6406531279532)
- [da5006_2026T1_Q1_NA Q11](../question-bank/week-04-questions.md#da5006_2026t1_q1_na--q11--1-marks--id-6406531961521)
- [da5006_2026T2_Q1_NA Q10](../question-bank/week-04-questions.md#da5006_2026t2_q1_na--q10--1-marks--id-6406532166257)
- [da5006_2024T1_Q2_NA Q155](../question-bank/week-04-questions.md#da5006_2024t1_q2_na--q155--2-marks--id-640653766145)
- [da5006_2024T1_Q2_NA Q156](../question-bank/week-04-questions.md#da5006_2024t1_q2_na--q156--2-marks--id-640653766146)
- [da5006_2024T3_Q2_NA Q132](../question-bank/week-04-questions.md#da5006_2024t3_q2_na--q132--2-marks--id-6406531031065)
- [da5006_2024T3_Q2_NA Q133](../question-bank/week-04-questions.md#da5006_2024t3_q2_na--q133--2-marks--id-6406531031066)
- [da5006_2025T1_Q2_NA Q268](../question-bank/week-04-questions.md#da5006_2025t1_q2_na--q268--3-marks--id-6406531168244)
- [da5006_2025T1_Q2_NA Q269](../question-bank/week-04-questions.md#da5006_2025t1_q2_na--q269--3-marks--id-6406531168245)
- [da5006_2025T2_Q2_NA Q259](../question-bank/week-04-questions.md#da5006_2025t2_q2_na--q259--2-marks--id-6406531333813)
- [da5006_2025T2_Q2_NA Q260](../question-bank/week-04-questions.md#da5006_2025t2_q2_na--q260--2-marks--id-6406531333814)
- [da5006_2025T3_Q2_NA Q154](../question-bank/week-04-questions.md#da5006_2025t3_q2_na--q154--2-marks--id-6406531815748)
- [da5006_2025T3_Q2_NA Q155](../question-bank/week-04-questions.md#da5006_2025t3_q2_na--q155--2-marks--id-6406531815749)
- [da5006_2026T1_Q2_NA Q19](../question-bank/week-04-questions.md#da5006_2026t1_q2_na--q19--1-marks--id-6406532040106)
- [da5006_2026T1_Q2_NA Q20](../question-bank/week-04-questions.md#da5006_2026t1_q2_na--q20--1-marks--id-6406532040107)
- [da5006_2026T2_Q2_NA Q18](../question-bank/week-04-questions.md#da5006_2026t2_q2_na--q18--4-marks--id-6406532194398)
- [da5006_2026T2_Q2_NA Q19](../question-bank/week-04-questions.md#da5006_2026t2_q2_na--q19--4-marks--id-6406532194399)

**Remember:** Use the question to practise the ideas in this topic.

### CNN backpropagation (7 questions)

- [da5006_2024T1_ET_AN Q167](../question-bank/week-04-questions.md#da5006_2024t1_et_an--q167--2-marks--id-640653821593)
- [da5006_2026T2_ET_FN Q11](../question-bank/week-04-questions.md#da5006_2026t2_et_fn--q11--2-marks--id-6406532270050)
- [da5006_2024T2_Q1_NA Q83](../question-bank/week-04-questions.md#da5006_2024t2_q1_na--q83--2-marks--id-640653829673)
- [da5006_2024T3_Q1_NA Q157](../question-bank/week-04-questions.md#da5006_2024t3_q1_na--q157--2-marks--id-640653994506)
- [da5006_2025T1_Q1_NA Q179](../question-bank/week-04-questions.md#da5006_2025t1_q1_na--q179--2-marks--id-6406531130638)
- [da5006_2025T2_Q1_NA Q172](../question-bank/week-04-questions.md#da5006_2025t2_q1_na--q172--3-marks--id-6406531279514)
- [da5006_2025T2_Q1_NA Q179](../question-bank/week-04-questions.md#da5006_2025t2_q1_na--q179--3-marks--id-6406531279530)

**Remember:** Use the question to practise the ideas in this topic.

### Pooling and receptive fields (5 questions)

- [da5006_2026T1_ET_FN Q12](../question-bank/week-04-questions.md#da5006_2026t1_et_fn--q12--2-marks--id-6406532136827)
- [da5006_2024T2_Q1_NA Q94](../question-bank/week-04-questions.md#da5006_2024t2_q1_na--q94--2-marks--id-640653829676)
- [da5006_2024T3_Q1_NA Q152](../question-bank/week-04-questions.md#da5006_2024t3_q1_na--q152--2-marks--id-640653994509)
- [da5006_2025T1_Q1_NA Q169](../question-bank/week-04-questions.md#da5006_2025t1_q1_na--q169--2-marks--id-6406531130641)
- [da5006_2025T2_Q1_NA Q166](../question-bank/week-04-questions.md#da5006_2025t2_q1_na--q166--2-marks--id-6406531279508)

**Remember:** Use the question to practise the ideas in this topic.

### AlexNet and early CNN classifiers (3 questions)

- [da5006_2025T2_ET_FN Q159](../question-bank/week-04-questions.md#da5006_2025t2_et_fn--q159--2-marks--id-6406531422538)
- [da5006_2025T2_Q2_NA Q239](../question-bank/week-04-questions.md#da5006_2025t2_q2_na--q239--2-marks--id-6406531333790)
- [da5006_2025T3_Q2_NA Q135](../question-bank/week-04-questions.md#da5006_2025t3_q2_na--q135--2-marks--id-6406531815727)

**Remember:** Use the question to practise the ideas in this topic.
