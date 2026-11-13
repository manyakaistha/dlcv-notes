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
