# Question Bank Discrepancies

- **Week 3 — `da5006_2025T2_ET_FN`, Q192, ID `6406531422568`:** The source key gives `3` for the linear activation. From the stated $x=[5,3,1,2]$, $w=[0.4,0.6,0.8,-0.2]$, and $b=0.4$, the affine output is $w^Tx+b=2+1.8+0.8-0.4+0.4=4.6$. The bank retains the source key and flags the arithmetic conflict.

## Week 5 — separable-convolution totals

The source keys for Q261 (2025T2 Q2, ID `6406531333816`) and Q156 (2025T3 Q2, ID `6406531815751`) give 12,544 parameters, which is the depthwise stage only ($7^2\cdot256$); the stem asks for depthwise-separable convolution, whose depthwise-plus-pointwise total is 143,616. The source keys for Q262 (ID `6406531333817`) and Q157 (ID `6406531815752`) give 1,254,400 MACs, also the depthwise stage only; total depthwise-plus-pointwise cost is 14,361,600 MACs. The question bank retains every source key and marks each mismatch. Values independently evaluated with `uv run python` using $P_{dw}=k^2M$, $P_{pw}=MN$, $C_{dw}=D_f^2k^2M$, and $C_{pw}=D_f^2MN$.

## da5006_2025T2_Q2_NA · Q240 · ID 6406531333791

The source key gives 28%. Both boxes have area 144, their intersection is 64, and the union is 224; IoU is 64/224 × 100 = 28.571428...%, which rounds to 29% to the nearest whole percent. The source states 28 without a tolerance.

## Week 11 — CLIP source questions

- `da5006_2024T3_ET_AN` Q202 (ID `6406531046055`): The source key cannot be verified: the supplied embeddings have different dimensions and are not normalized. Source key retained.
- `da5006_2025T2_ET_AN` Q88 (ID `6406531431348`): The keyed 69% is the raw dot product, whereas cosine similarity for the displayed vectors is approximately 96.34%; the vectors are not normalized. Source key retained.
- `da5006_2025T2_ET_AN` Q100 (ID `6406531431360`): The source key omits A: CLIP uses symmetric cross-entropy on contrastive similarity logits, so A and C are true. Source key retained.
## Week 9 — source wording and keys

- `da5006_2024T1_ET_AN` Q200–201: keyed 12288 and 64 are respectively input scalar count and patch count, not specified learned self-attention parameter counts. Projection widths are missing.
- `da5006_2026T1_ET_FN` Q18: key includes B, but self-attention on token sequences is permutation-equivariant, not invariant; positional information breaks that equivariance.

## Week 8

- **da5006_2024T1_ET_AN Q185 (ID 640653821621)**: The printed KL direction does not imply the maximum-likelihood equivalence used by the key. Maximum likelihood follows from minimizing $D_{KL}(p_{data}\|p_\theta)$, not generally the reverse order printed in the question. Squared-error equivalence also needs a fixed-variance Gaussian likelihood.

- **da5006_2024T1_Q2_NA Q154 (ID 640653766164)**: The key includes $p(x,y)$, which is not modeled by the vanilla unconditional GAN. A vanilla unconditional GAN learns a distribution over $x$ through samples; it does not, without a label-conditioned formulation or joint samples, model $p(x,y)$.

- **da5006_2024T1_Q2_NA Q173 (ID 640653766169)**: The keyed coefficient and the companion keyed value do not yield the stated KL divergence; infinitely many coefficient/base pairs are possible. Both outcomes contribute: $0.9\log 9+0.1\log(1/9)=0.8\log 9$. The requested pair $(c,d)$ is not uniquely determined without a convention.

- **da5006_2024T1_Q2_NA Q174 (ID 640653766170)**: With the companion key $c=0.9$, the required base is approximately 7.0504, not 8. The Bernoulli sum is $0.8\log 9$, not $0.9\log 8$. If the keyed $c=0.9$ is fixed, $d=9^{8/9}\approx7.0504$.

- **da5006_2024T1_Q2_NA Q175 (ID 640653766173)**: The initial output is not determined by the premise; zero is only a possible limiting case. No initial discriminator output is fixed by the GAN objective: it depends on initialization and updates. A strong discriminator may assign fakes probabilities near zero.

- **da5006_2024T2_Q2_NA Q134 (ID 640653856582)**: The conventional hinge triplet loss is 0, not the keyed -30. Squared distances are $d(a,p)^2=25$ and $d(a,n)^2=43$. The conventional hinge triplet loss is $\max(0,25-43+12)=0$; even the unhinged expression is $-6$.


## Week 2

- `da5006_2024T1_ET_AN`, Q165, ID `640653821591`: source key A says VLAD captures spatial relationships. Standard VLAD aggregates descriptor residuals by visual word without spatial layout, so D is the better answer.
- `da5006_2026T1_Q1_NA`, Q12, ID `6406531961525`: source key 12 conflicts with the requested sum: 3D translation has 3 degrees of freedom and a 3D affine map has 12, summing to 15.
- `da5006_2026T1_Q1_NA`, Q15, ID `6406531961528`: source range −6 to −5 conflicts with the eigenvalue calculation, whose normalized difference has magnitude $\sqrt{13}/7 \approx 0.5151$.
