---
title: "Week 3 in plain language: how a neural network learns"
week: 3
status: complete
tags: [dl4cv/eli12, dl4cv/week-03]
---

# Week 3 in plain language: how a neural network learns

**Explain-like-I'm-12 version.** A network learns to turn picture numbers into a useful answer by adjusting its own settings. This is a first pass through the [full Week 3 report](../month%201/week%203/week-3-report.md); use the [exam notes](../month%201/week%203/week-3-exam-notes.md) for the detailed mathematics.

> [!NOTE]
> **The big idea:** Make a prediction, measure its mistake, trace the mistake backwards, and adjust the settings. Repeat on many examples, then check on pictures the network has not practised on.

## 1. A neuron is a tiny voting machine

A picture is a grid of **pixels**, each represented by numbers such as brightness. A neuron receives numbers, multiplies each by a **weight** (how strongly to listen to that input), adds them, and adds a **bias** (a starting offset). Its **activation function** then changes that total into its output.

For inputs 2 and 3, weights 0.5 and -0.25, and bias 0.1, the total is $2(0.5)+3(-0.25)+0.1=0.35$. With **ReLU** (short for rectified linear unit), which keeps a positive total and replaces a negative one with zero, the output is 0.35. A negative weight is a vote against a larger total.

**Remember:** Multiply, add the bias, then apply the activation.

## 2. From one neuron to a network

An early McCulloch–Pitts neuron makes a yes/no decision from binary inputs and a threshold; it has no learned continuous weights. A **perceptron** learns weights for a yes/no decision. Its **decision boundary** is the line (or higher-dimensional flat surface) separating its two answers. If no straight line separates the examples, a single perceptron cannot solve them: XOR says “yes” for exactly one of two switches being on, and its yes and no cases cannot be separated by one line.

A **feedforward network** passes numbers from an input layer through one or more **hidden layers** (intermediate groups of neurons) to an output layer, without sending them backwards during prediction. Hidden neurons can combine simple decisions into more complicated ones, including XOR. With suitable nonlinear activations and enough hidden neurons, a network can approximate a continuous function on a bounded region as closely as desired; this does not promise easy training or a small network.

**Remember:** Layers and nonlinear activations let networks make decisions a single straight boundary cannot.

## 3. Why activations matter

Without nonlinear activations, stacking ordinary weighted sums is still just one weighted sum. **Sigmoid** squeezes any number between 0 and 1; **tanh** squeezes it between -1 and 1. ReLU keeps positive numbers and clips negative ones to zero. Sigmoid and tanh can become nearly flat at their extremes: the learning signal then gets tiny, called a **vanishing gradient**. ReLU avoids that flat region on its positive side, but a neuron stuck on the negative side can stop receiving a useful learning signal, called a **dying ReLU**.

**Remember:** Nonlinearity gives layers expressive power, but activation choice also affects learning.

## 4. How wrong was the answer?

A **label** is the known answer for a training example. A **loss** is a number measuring the prediction's mistake: lower is better. For a predicted number 0.35 and target 1, use half the squared difference: $L=\frac12(0.35-1)^2=0.21125$. The half makes the next calculation tidy.

For choosing among picture categories, **softmax** converts a set of scores into probabilities that add to one. **Cross-entropy** is a loss that penalizes assigning a low probability to the correct category. A confident wrong answer is expensive.

**Remember:** The loss turns “how wrong?” into a number the network can reduce.

## 5. Backpropagation: passing the blame backwards

A **derivative** tells how quickly one number changes when another changes a little. A **gradient** is the collection of those slopes for the network's adjustable settings. **Backpropagation** uses the **chain rule**—multiply the slopes along a chain of calculations—to work out each setting's share of the loss. It computes gradients; a separate update rule changes the weights.

Use the neuron above, target 1 and loss $L=\frac12(\text{output}-1)^2$. Since its total is positive, ReLU passes changes through with slope 1. The loss slope with respect to the output is $0.35-1=-0.65$. The first weight affects the total by the first input, 2, so its loss slope is $-0.65\times1\times2=-1.3$. With **learning rate** (step size) 0.1, subtract 0.1 times that slope: the first weight becomes $0.5-0.1(-1.3)=0.63$. If only this weight changes, the output becomes 0.61 and the loss becomes 0.07605. The negative slope told us increasing this weight would locally reduce the loss.

**Remember:** Backpropagation finds which direction each setting should move; the update takes the step.

## 6. Walking downhill: gradient descent and its relatives

Imagine the loss as height on a foggy hill. **Gradient descent** takes a step opposite the uphill slope. Too large a learning rate can overshoot; too small can make progress slow. **Batch** gradient descent uses the whole training set for each step; **stochastic gradient descent** (SGD) uses one example; **mini-batch** training uses a small group. Small batches give noisier but cheaper steps.

Compare one update from weight 1, gradient 0.2 and learning rate 0.1. The gradient is the slope of the chosen batch's loss at the current weight.

| Method | Calculation | New weight |
| :-- | :-- | :-- |
| SGD | $1-0.1(0.2)$ | 0.98 |
| Momentum | Previous velocity 0.01, memory 0.9: new velocity $0.9(0.01)+0.1(0.2)=0.029$; subtract it | 0.971 |
| Adam | First step, zero initial memories, memory rates 0.9 and 0.999: corrected average gradient 0.2 and corrected average squared gradient 0.04; divide by $\sqrt{0.04}+10^{-8}$, multiply by 0.1, then subtract | approximately 0.900000005 |

**Momentum** carries some previous motion forward, like a rolling ball. **Adam** keeps moving averages of gradients and their squares, corrects their initial bias towards zero, and scales each setting's step separately; the tiny $10^{-8}$ prevents division by zero. **Nesterov momentum** measures the slope after looking ahead along the stored motion. None guarantees finding the best possible answer.

**Remember:** Optimizers decide how to use the gradient; their history and step sizes can change the journey.

## 7. Studying without memorising: regularization

**Generalization** means doing well on new examples, not just training examples. **Overfitting** is memorising quirks of the training set so new examples suffer. **Regularization** adds a restraint or variation to help generalization.

- **L2 regularization** adds a penalty for squared weights to the loss. For weight 2 and penalty strength 0.1, the extra loss is $0.1(2^2)=0.4$. It encourages smaller weights; the data loss still matters. **L1** instead adds a penalty based on absolute weight size and can encourage exact zeros.
- **Dropout** randomly switches off some hidden outputs during training. With outputs 2 and 4, keep probability 0.5, and a particular mask that keeps the first and drops the second, *inverted dropout* scales the survivor by $1/0.5$: the passed values are 4 and 0. Other masks are possible. At prediction time dropout is off; the unmasked outputs are 2 and 4. The scaling preserves each output's average over masks, not each individual outcome.
- **Early stopping** stops training when performance on a separate **validation set** (held-out examples used for choices) stops improving. A final **test set** is kept aside for assessment after choices are made.

**Remember:** A low training loss alone does not prove the network will work on new pictures.

## 8. Helping training start and stay healthy

If all hidden neurons start with identical weights and biases, they can receive identical updates and keep doing the same job. Random **initialization** (choosing starting weights) breaks this symmetry. Values that are too large or too small can make signals or gradients explode or fade across layers. Xavier initialization uses a scale suited to common symmetric activations; He initialization uses a scale designed for ReLU. Neither is a guarantee for every network.

**Normalization** puts numbers on a more manageable scale. Input normalization makes input features comparable. **Batch normalization** uses the mean and spread of a mini-batch to standardize intermediate values, then applies a learned scale and shift. At prediction time it ordinarily uses running estimates collected during training. It can make training easier, but does not replace checking performance on unseen data.

**Remember:** Different sensible starting weights and well-scaled signals help information travel through the network.

## Check yourself

1. Inputs 1 and 2 have weights 2 and -1, with bias 0.5. What is the ReLU output? *(0.5: the total is 2 - 2 + 0.5.)*
2. Does backpropagation itself update the weights? *(No; it computes gradients for an update rule.)*
3. Why use a validation set? *(To choose training settings using examples outside the training set.)*
4. What happens to dropout at prediction time? *(It is switched off.)*

**Remember:** Predict, measure, trace the slopes backwards, update, and check on unseen examples.

## Where this was asked

These are all questions assigned primary Week 3 in the final manifest, grouped by curriculum topic and ordered by question count. Paper codes identify the original exam; question numbers link to their exact entries in the bank.

### Perceptrons and feedforward networks (28 questions)

[da5006_2024T3_ET_AN Q209](../question-bank/week-03-questions.md#da5006_2024t3_et_an--q209--2-marks--id-6406531046072) · [da5006_2025T2_ET_AN Q84](../question-bank/week-03-questions.md#da5006_2025t2_et_an--q84--2-marks--id-6406531431344) · [da5006_2025T2_ET_AN Q126](../question-bank/week-03-questions.md#da5006_2025t2_et_an--q126--1-marks--id-6406531431390) · [da5006_2025T2_ET_AN Q127](../question-bank/week-03-questions.md#da5006_2025t2_et_an--q127--1-marks--id-6406531431391) · [da5006_2025T2_ET_AN Q128](../question-bank/week-03-questions.md#da5006_2025t2_et_an--q128--1-marks--id-6406531431392) · [da5006_2025T2_ET_AN Q129](../question-bank/week-03-questions.md#da5006_2025t2_et_an--q129--1-marks--id-6406531431393) · [da5006_2025T2_ET_AN Q130](../question-bank/week-03-questions.md#da5006_2025t2_et_an--q130--1-marks--id-6406531431394) · [da5006_2025T2_ET_AN Q131](../question-bank/week-03-questions.md#da5006_2025t2_et_an--q131--1-marks--id-6406531431395) · [da5006_2025T2_ET_FN Q177](../question-bank/week-03-questions.md#da5006_2025t2_et_fn--q177--2-marks--id-6406531422556) · [da5006_2025T2_ET_FN Q191](../question-bank/week-03-questions.md#da5006_2025t2_et_fn--q191--1-marks--id-6406531422567) · [da5006_2025T2_ET_FN Q192](../question-bank/week-03-questions.md#da5006_2025t2_et_fn--q192--1-marks--id-6406531422568) · [da5006_2025T2_ET_FN Q193](../question-bank/week-03-questions.md#da5006_2025t2_et_fn--q193--1-marks--id-6406531422569) · [da5006_2025T2_ET_FN Q194](../question-bank/week-03-questions.md#da5006_2025t2_et_fn--q194--1-marks--id-6406531422570) · [da5006_2025T2_ET_FN Q195](../question-bank/week-03-questions.md#da5006_2025t2_et_fn--q195--1-marks--id-6406531422571) · [da5006_2025T2_ET_FN Q196](../question-bank/week-03-questions.md#da5006_2025t2_et_fn--q196--1-marks--id-6406531422572) · [da5006_2026T1_ET_FN Q22](../question-bank/week-03-questions.md#da5006_2026t1_et_fn--q22--4-marks--id-6406532136837) · [da5006_2024T3_Q1_NA Q146](../question-bank/week-03-questions.md#da5006_2024t3_q1_na--q146--2-marks--id-640653994486) · [da5006_2024T3_Q1_NA Q156](../question-bank/week-03-questions.md#da5006_2024t3_q1_na--q156--2-marks--id-640653994488) · [da5006_2025T1_Q1_NA Q163](../question-bank/week-03-questions.md#da5006_2025t1_q1_na--q163--2-marks--id-6406531130619) · [da5006_2025T1_Q1_NA Q178](../question-bank/week-03-questions.md#da5006_2025t1_q1_na--q178--2-marks--id-6406531130621) · [da5006_2025T2_Q1_NA Q161](../question-bank/week-03-questions.md#da5006_2025t2_q1_na--q161--2-marks--id-6406531279503) · [da5006_2025T2_Q1_NA Q171](../question-bank/week-03-questions.md#da5006_2025t2_q1_na--q171--3-marks--id-6406531279513) · [da5006_2024T1_Q2_NA Q149](../question-bank/week-03-questions.md#da5006_2024t1_q2_na--q149--2-marks--id-640653766144) · [da5006_2024T1_Q2_NA Q157](../question-bank/week-03-questions.md#da5006_2024t1_q2_na--q157--2-marks--id-640653766147) · [da5006_2024T1_Q2_NA Q168](../question-bank/week-03-questions.md#da5006_2024t1_q2_na--q168--2-marks--id-640653766149) · [da5006_2024T1_Q2_NA Q169](../question-bank/week-03-questions.md#da5006_2024t1_q2_na--q169--2-marks--id-640653766150) · [da5006_2024T1_Q2_NA Q170](../question-bank/week-03-questions.md#da5006_2024t1_q2_na--q170--1-marks--id-640653766151) · [da5006_2024T2_Q2_NA Q129](../question-bank/week-03-questions.md#da5006_2024t2_q2_na--q129--2-marks--id-640653856604)

### Backpropagation and losses (26 questions)

[da5006_2024T1_ET_AN Q197](../question-bank/week-03-questions.md#da5006_2024t1_et_an--q197--07-marks--id-640653821610) · [da5006_2024T1_ET_AN Q198](../question-bank/week-03-questions.md#da5006_2024t1_et_an--q198--07-marks--id-640653821611) · [da5006_2024T1_ET_AN Q199](../question-bank/week-03-questions.md#da5006_2024t1_et_an--q199--06-marks--id-640653821612) · [da5006_2024T3_ET_AN Q212](../question-bank/week-03-questions.md#da5006_2024t3_et_an--q212--2-marks--id-6406531046076) · [da5006_2024T3_ET_AN Q215](../question-bank/week-03-questions.md#da5006_2024t3_et_an--q215--2-marks--id-6406531046057) · [da5006_2024T3_ET_AN Q216](../question-bank/week-03-questions.md#da5006_2024t3_et_an--q216--2-marks--id-6406531046058) · [da5006_2025T2_ET_AN Q109](../question-bank/week-03-questions.md#da5006_2025t2_et_an--q109--1-marks--id-6406531431368) · [da5006_2025T2_ET_AN Q110](../question-bank/week-03-questions.md#da5006_2025t2_et_an--q110--1-marks--id-6406531431369) · [da5006_2025T2_ET_FN Q160](../question-bank/week-03-questions.md#da5006_2025t2_et_fn--q160--2-marks--id-6406531422539) · [da5006_2025T2_ET_FN Q185](../question-bank/week-03-questions.md#da5006_2025t2_et_fn--q185--1-marks--id-6406531422564) · [da5006_2025T2_ET_FN Q186](../question-bank/week-03-questions.md#da5006_2025t2_et_fn--q186--1-marks--id-6406531422565) · [da5006_2025T3_ET_FN Q7](../question-bank/week-03-questions.md#da5006_2025t3_et_fn--q7--1-marks--id-6406531862821) · [da5006_2025T3_ET_FN Q17](../question-bank/week-03-questions.md#da5006_2025t3_et_fn--q17--1-marks--id-6406531862831) · [da5006_2025T3_ET_FN Q20](../question-bank/week-03-questions.md#da5006_2025t3_et_fn--q20--1-marks--id-6406531862834) · [da5006_2026T1_ET_FN Q8](../question-bank/week-03-questions.md#da5006_2026t1_et_fn--q8--2-marks--id-6406532136823) · [da5006_2026T2_ET_FN Q7](../question-bank/week-03-questions.md#da5006_2026t2_et_fn--q7--2-marks--id-6406532270046) · [da5006_2026T2_ET_FN Q23](../question-bank/week-03-questions.md#da5006_2026t2_et_fn--q23--3-marks--id-6406532270062) · [da5006_2026T2_ET_FN Q32](../question-bank/week-03-questions.md#da5006_2026t2_et_fn--q32--4-marks--id-6406532270071) · [da5006_2024T2_Q1_NA Q93](../question-bank/week-03-questions.md#da5006_2024t2_q1_na--q93--2-marks--id-640653829672) · [da5006_2024T3_Q1_NA Q151](../question-bank/week-03-questions.md#da5006_2024t3_q1_na--q151--2-marks--id-640653994505) · [da5006_2025T1_Q1_NA Q168](../question-bank/week-03-questions.md#da5006_2025t1_q1_na--q168--2-marks--id-6406531130637) · [da5006_2025T1_Q1_NA Q188](../question-bank/week-03-questions.md#da5006_2025t1_q1_na--q188--1-marks--id-6406531130647) · [da5006_2025T1_Q1_NA Q189](../question-bank/week-03-questions.md#da5006_2025t1_q1_na--q189--1-marks--id-6406531130648) · [da5006_2025T2_Q1_NA Q165](../question-bank/week-03-questions.md#da5006_2025t2_q1_na--q165--2-marks--id-6406531279507) · [da5006_2026T1_Q1_NA Q6](../question-bank/week-03-questions.md#da5006_2026t1_q1_na--q6--1-marks--id-6406531961529) · [da5006_2026T2_Q1_NA Q6](../question-bank/week-03-questions.md#da5006_2026t2_q1_na--q6--1-marks--id-6406532166265)

### Gradient descent and variants (14 questions)

[da5006_2025T2_ET_AN Q104](../question-bank/week-03-questions.md#da5006_2025t2_et_an--q104--2-marks--id-6406531431364) · [da5006_2025T2_ET_FN Q181](../question-bank/week-03-questions.md#da5006_2025t2_et_fn--q181--2-marks--id-6406531422560) · [da5006_2025T3_ET_FN Q15](../question-bank/week-03-questions.md#da5006_2025t3_et_fn--q15--1-marks--id-6406531862829) · [da5006_2026T1_ET_FN Q9](../question-bank/week-03-questions.md#da5006_2026t1_et_fn--q9--2-marks--id-6406532136824) · [da5006_2026T2_ET_FN Q8](../question-bank/week-03-questions.md#da5006_2026t2_et_fn--q8--2-marks--id-6406532270047) · [da5006_2024T3_Q1_NA Q153](../question-bank/week-03-questions.md#da5006_2024t3_q1_na--q153--2-marks--id-640653994481) · [da5006_2025T1_Q1_NA Q160](../question-bank/week-03-questions.md#da5006_2025t1_q1_na--q160--2-marks--id-6406531130645) · [da5006_2025T1_Q1_NA Q172](../question-bank/week-03-questions.md#da5006_2025t1_q1_na--q172--2-marks--id-6406531130644) · [da5006_2025T1_Q1_NA Q175](../question-bank/week-03-questions.md#da5006_2025t1_q1_na--q175--2-marks--id-6406531130614) · [da5006_2025T2_Q1_NA Q167](../question-bank/week-03-questions.md#da5006_2025t2_q1_na--q167--2-marks--id-6406531279509) · [da5006_2025T2_Q1_NA Q175](../question-bank/week-03-questions.md#da5006_2025t2_q1_na--q175--3-marks--id-6406531279517) · [da5006_2025T2_Q1_NA Q182](../question-bank/week-03-questions.md#da5006_2025t2_q1_na--q182--3-marks--id-6406531279533) · [da5006_2026T1_Q1_NA Q3](../question-bank/week-03-questions.md#da5006_2026t1_q1_na--q3--1-marks--id-6406531961522) · [da5006_2026T2_Q1_NA Q3](../question-bank/week-03-questions.md#da5006_2026t2_q1_na--q3--1-marks--id-6406532166258)

### Regularization and generalization (11 questions)

[da5006_2024T1_ET_AN Q169](../question-bank/week-03-questions.md#da5006_2024t1_et_an--q169--2-marks--id-640653821595) · [da5006_2024T2_ET_AN Q253](../question-bank/week-03-questions.md#da5006_2024t2_et_an--q253--2-marks--id-640653904305) · [da5006_2025T2_ET_AN Q89](../question-bank/week-03-questions.md#da5006_2025t2_et_an--q89--2-marks--id-6406531431349) · [da5006_2025T2_ET_AN Q101](../question-bank/week-03-questions.md#da5006_2025t2_et_an--q101--2-marks--id-6406531431361) · [da5006_2025T2_ET_FN Q165](../question-bank/week-03-questions.md#da5006_2025t2_et_fn--q165--2-marks--id-6406531422544) · [da5006_2025T2_ET_FN Q175](../question-bank/week-03-questions.md#da5006_2025t2_et_fn--q175--2-marks--id-6406531422554) · [da5006_2025T3_ET_FN Q8](../question-bank/week-03-questions.md#da5006_2025t3_et_fn--q8--1-marks--id-6406531862822) · [da5006_2025T3_ET_FN Q16](../question-bank/week-03-questions.md#da5006_2025t3_et_fn--q16--1-marks--id-6406531862830) · [da5006_2026T1_ET_FN Q10](../question-bank/week-03-questions.md#da5006_2026t1_et_fn--q10--2-marks--id-6406532136825) · [da5006_2026T1_ET_FN Q17](../question-bank/week-03-questions.md#da5006_2026t1_et_fn--q17--3-marks--id-6406532136832) · [da5006_2026T2_ET_FN Q9](../question-bank/week-03-questions.md#da5006_2026t2_et_fn--q9--2-marks--id-6406532270048)

### Initialization and normalization (1 questions)

[da5006_2025T3_ET_FN Q18](../question-bank/week-03-questions.md#da5006_2025t3_et_fn--q18--1-marks--id-6406531862832)

**Remember:** Practise the exact question, then use the full notes to check the reasoning.
