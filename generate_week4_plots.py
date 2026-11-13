import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, ArrowStyle
import numpy as np

# Ensure assets directory exists
output_dir = "/Volumes/1700 APFS/PERSONAL_PROGRAMMING_PROJECTS/Notes/Deep Learning for Computer Vision/month 1/week 4/assets"
os.makedirs(output_dir, exist_ok=True)

# Set base aesthetics
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#2b2b2b'
plt.rcParams['axes.linewidth'] = 0.8

# -------------------------------------------------------------
# FIGURE 1: FNN vs CNN Locality & Parameter Explosion
# -------------------------------------------------------------
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5), facecolor='white')

# Subplot 1: FNN Flattening destruction
ax1.set_title("(A) FNN: Flattening Destroys Spatial Locality", fontsize=11, fontweight='bold', pad=10)
# 2D Grid
for r in range(4):
    for c in range(4):
        color = '#38bdf8' if (r in [1, 2] and c in [1, 2]) else '#e2e8f0'
        ax1.add_patch(Rectangle((c, 3 - r), 0.8, 0.8, facecolor=color, edgecolor='#64748b'))
ax1.text(2, -0.4, "2D Image Matrix (Adjacent Pixels)", ha='center', fontsize=9, fontweight='bold')

# Arrow pointing to 1D vector
ax1.annotate("", xy=(5.2, 2.0), xytext=(4.1, 2.0),
             arrowprops=dict(arrowstyle="->", color='#ef4444', lw=2))
ax1.text(4.65, 2.2, "Flatten", ha='center', fontsize=9, color='#ef4444', fontweight='bold')

# 1D Vector
for i in range(16):
    color = '#38bdf8' if i in [5, 6, 9, 10] else '#e2e8f0'
    ax1.add_patch(Rectangle((5.5, 3.8 - i * 0.25), 0.6, 0.22, facecolor=color, edgecolor='#64748b'))
ax1.text(5.8, -0.4, "1D Vector (Locality Lost)", ha='center', fontsize=9, fontweight='bold')

ax1.set_xlim(-0.5, 6.8)
ax1.set_ylim(-0.8, 4.2)
ax1.axis('off')

# Subplot 2: CNN Local Receptive Field & Weight Sharing
ax2.set_title("(B) CNN: Local Receptive Field & Weight Sharing", fontsize=11, fontweight='bold', pad=10)
# 2D Input Grid
for r in range(5):
    for c in range(5):
        ax2.add_patch(Rectangle((c*0.8, 4 - r*0.8), 0.75, 0.75, facecolor='#f1f5f9', edgecolor='#94a3b8'))

# Highlighted receptive field
for r in range(1, 4):
    for c in range(1, 4):
        ax2.add_patch(Rectangle((c*0.8, 4 - r*0.8), 0.75, 0.75, facecolor='#fed7aa', edgecolor='#ea580c', lw=1.5))
ax2.text(2.0, 0.5, "Receptive Field (3x3 Kernel)", ha='center', fontsize=9, color='#c2410c', fontweight='bold')

# Convolution arrow
ax2.annotate("", xy=(5.0, 2.4), xytext=(4.3, 2.4),
             arrowprops=dict(arrowstyle="->", color='#0284c7', lw=2))
ax2.text(4.65, 2.6, "Conv * W", ha='center', fontsize=9, color='#0284c7', fontweight='bold')

# Output Feature Map single cell
for r in range(3):
    for c in range(3):
        color = '#38bdf8' if (r == 1 and c == 1) else '#e2e8f0'
        ax2.add_patch(Rectangle((5.3 + c*0.7, 3.2 - r*0.7), 0.65, 0.65, facecolor=color, edgecolor='#0284c7'))
ax2.text(6.3, 0.5, "Output Activation Y[i, j]", ha='center', fontsize=9, color='#0369a1', fontweight='bold')

ax2.set_xlim(-0.2, 7.8)
ax2.set_ylim(0.2, 4.8)
ax2.axis('off')

# Subplot 3: Parameter Comparison Bar Chart
ax3.set_title("(C) Parameter Explosion: FNN vs CNN", fontsize=11, fontweight='bold', pad=10)
models = ['FNN (10^6 px x 20 units)', 'CNN (96 filters, 11x11x3)']
params = [60.0, 0.0348]  # Millions
colors = ['#ef4444', '#10b981']

bars = ax3.bar(models, params, color=colors, width=0.55, edgecolor='#1e293b')
ax3.set_ylabel("Parameters (Millions)", fontsize=10, fontweight='bold')
ax3.set_yscale('log')
ax3.set_ylim(0.01, 100)
ax3.grid(axis='y', linestyle='--', alpha=0.5)

for bar in bars:
    height = bar.get_height()
    if height > 1:
        ax3.text(bar.get_x() + bar.get_width()/2., height * 1.2, f"{height:.1f} M", ha='center', va='bottom', fontsize=9, fontweight='bold')
    else:
        ax3.text(bar.get_x() + bar.get_width()/2., height * 1.3, f"{int(height*1000000):,} weights", ha='center', va='bottom', fontsize=9, fontweight='bold')

ax3.set_xticklabels(['FNN (Dense)', 'CNN (Conv)'], fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "fig01_fnn_vs_cnn_locality.png"), dpi=180, facecolor='white')
plt.close()
print("Saved fig01_fnn_vs_cnn_locality.png")

# -------------------------------------------------------------
# FIGURE 2: 3D Convolution & Dimension Calculus
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), facecolor='white')

# Subplot 1: 3D Tensor Convolution Mechanics
ax1.set_title("(A) 3D Convolution Volume Mechanics (K Filters)", fontsize=11, fontweight='bold', pad=10)

# Input Volume (W1 x H1 x D1)
ax1.add_patch(Rectangle((0.5, 1.0), 2.5, 3.0, facecolor='#bae6fd', edgecolor='#0284c7', lw=1.5, label='Input Volume'))
ax1.add_patch(Rectangle((0.8, 1.3), 2.5, 3.0, facecolor='#e0f2fe', edgecolor='#0284c7', lw=1.0, alpha=0.7))
ax1.text(1.75, 2.5, "Input X\n$W_1 \\times H_1 \\times D_1$\n(e.g., 227x227x3)", ha='center', va='center', fontsize=9, fontweight='bold')

# 3D Filter Volume (F x F x D1)
ax1.add_patch(Rectangle((3.8, 2.2), 1.2, 1.2, facecolor='#fde047', edgecolor='#ca8a04', lw=1.5))
ax1.add_patch(Rectangle((4.0, 2.4), 1.2, 1.2, facecolor='#fef08a', edgecolor='#ca8a04', lw=1.0, alpha=0.7))
ax1.text(4.4, 2.8, "Filter\n$F \\times F \\times D_1$", ha='center', va='center', fontsize=8, fontweight='bold', color='#854d0e')

ax1.annotate("", xy=(5.8, 2.8), xytext=(5.1, 2.8), arrowprops=dict(arrowstyle="->", color='#0f172a', lw=2))
ax1.text(5.45, 3.0, "Slide S", ha='center', fontsize=8, fontweight='bold')

# Output Volume (W2 x H2 x K)
ax1.add_patch(Rectangle((6.2, 1.2), 2.0, 2.5, facecolor='#bbf7d0', edgecolor='#16a34a', lw=1.5))
ax1.add_patch(Rectangle((6.5, 1.5), 2.0, 2.5, facecolor='#dcfce7', edgecolor='#16a34a', lw=1.0, alpha=0.7))
ax1.text(7.2, 2.45, "Output Y\n$W_2 \\times H_2 \\times K$\n(K slices)", ha='center', va='center', fontsize=9, fontweight='bold', color='#166534')

ax1.set_xlim(0, 9.2)
ax1.set_ylim(0.5, 5.0)
ax1.axis('off')

# Subplot 2: Spatial Formula Geometry & Step Derivation
ax2.set_title("(B) Mathematical Dimension Formula Derivation", fontsize=11, fontweight='bold', pad=10)

formula_text = (
    "Output Spatial Dimension Formula:\n\n"
    r"  $W_2 = \lfloor \frac{W_1 - F + 2P}{S} \rfloor + 1$" + "\n"
    r"  $H_2 = \lfloor \frac{H_1 - F + 2P}{S} \rfloor + 1$" + "\n"
    r"  $D_2 = K \quad \text{(Number of Filters)}$" + "\n\n"
    "Step-by-Step Rationale:\n"
    r"1. Effective input span with zero-padding: $W_1 + 2P$" + "\n"
    r"2. Subtract filter extent: $(W_1 + 2P) - F$" + "\n"
    r"3. Divide by stride step $S$: jumps between kernel placements" + "\n"
    r"4. Add 1 for the initial starting placement position" + "\n\n"
    "AlexNet Layer 1 Benchmark Example:\n"
    r"  Input: $227 \times 227 \times 3$, $F = 11$, $P = 0$, $S = 4$, $K = 96$" + "\n"
    r"  $W_2 = \frac{227 - 11 + 0}{4} + 1 = \frac{216}{4} + 1 = 54 + 1 = 55$" + "\n"
    r"  Output Shape: $55 \times 55 \times 96$"
)

ax2.text(0.05, 0.95, formula_text, va='top', ha='left', fontsize=9.5, linespacing=1.45,
         bbox=dict(boxstyle='round,pad=0.8', facecolor='#f8fafc', edgecolor='#cbd5e1'))
ax2.axis('off')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "fig02_convolution_dimension_calculus.png"), dpi=180, facecolor='white')
plt.close()
print("Saved fig02_convolution_dimension_calculus.png")

# -------------------------------------------------------------
# FIGURE 3: Convolution Variants: Dilated and Transposed
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), facecolor='white')

# Subplot 1: Dilated Convolution
ax1.set_title("(A) Dilated Convolution (Atrous): Expanding Receptive Field", fontsize=11, fontweight='bold', pad=10)

# 7x7 Grid
grid_size = 7
for r in range(grid_size):
    for c in range(grid_size):
        ax1.add_patch(Rectangle((c, grid_size - 1 - r), 0.9, 0.9, facecolor='#f1f5f9', edgecolor='#cbd5e1'))

# Highlight kernel positions for rate = 2 (centered at (3, 3))
dilated_pts = [(1, 1), (1, 3), (1, 5), (3, 1), (3, 3), (3, 5), (5, 1), (5, 3), (5, 5)]
for r, c in dilated_pts:
    ax1.add_patch(Rectangle((c, grid_size - 1 - r), 0.9, 0.9, facecolor='#ef4444', edgecolor='#b91c1c', lw=1.5))

ax1.text(3.45, -0.6, "3x3 Kernel with Dilation Rate d=2 (Effective Receptive Field = 5x5)\nFormula: F' = d(F - 1) + 1 = 2(3 - 1) + 1 = 5", 
         ha='center', fontsize=9, fontweight='bold', color='#991b1b')

ax1.set_xlim(-0.5, 7.5)
ax1.set_ylim(-1.0, 7.5)
ax1.axis('off')

# Subplot 2: Transposed Convolution
ax2.set_title("(B) Transposed Convolution: Learnable Upsampling (2x2 to 4x4)", fontsize=11, fontweight='bold', pad=10)

# Input 2x2
for r in range(2):
    for c in range(2):
        colors_in = ['#38bdf8', '#34d399', '#fbbf24', '#f87171']
        ax2.add_patch(Rectangle((0.5 + c*1.1, 3.8 - r*1.1), 0.95, 0.95, facecolor=colors_in[r*2 + c], edgecolor='#334155', lw=1.5))
ax2.text(1.5, 2.3, "Input (2x2)", ha='center', fontsize=9, fontweight='bold')

# Arrow
ax2.annotate("", xy=(3.8, 3.2), xytext=(2.9, 3.2), arrowprops=dict(arrowstyle="->", color='#0f172a', lw=2))
ax2.text(3.35, 3.5, "Learnable\nKernel * W", ha='center', fontsize=8, fontweight='bold')

# Output 4x4 with overlapping sums
for r in range(4):
    for c in range(4):
        ax2.add_patch(Rectangle((4.2 + c*0.8, 4.4 - r*0.8), 0.72, 0.72, facecolor='#f8fafc', edgecolor='#64748b'))

# Highlight overlapping patches from top-left and top-right
ax2.add_patch(Rectangle((4.2, 3.6), 1.52, 1.52, facecolor='#38bdf8', alpha=0.3, edgecolor='#0284c7', lw=1.5))
ax2.add_patch(Rectangle((5.0, 3.6), 1.52, 1.52, facecolor='#34d399', alpha=0.3, edgecolor='#059669', lw=1.5))
ax2.text(5.8, 0.8, "Output (4x4)\nOverlapping regions accumulate weighted kernel values", ha='center', fontsize=9, fontweight='bold', color='#0f172a')

ax2.set_xlim(0, 8.0)
ax2.set_ylim(0.4, 5.5)
ax2.axis('off')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "fig03_convolution_variants_dilated_transposed.png"), dpi=180, facecolor='white')
plt.close()
print("Saved fig03_convolution_variants_dilated_transposed.png")

# -------------------------------------------------------------
# FIGURE 4: Backpropagation in CNNs (Weights, Inputs, Pooling)
# -------------------------------------------------------------
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10), facecolor='white')

# (A) dL/dW derivation
ax1.set_title(r"(A) Gradient w.r.t Weights: $\frac{\partial L}{\partial W} = X * \frac{\partial L}{\partial Y}$", fontsize=11, fontweight='bold', pad=10)
text_dw = (
    "Weight Gradient Derivation:\n\n"
    r"• A single weight $W[a', b']$ participates in EVERY output pixel $Y[i, j]$." + "\n"
    r"• Applying the multivariable chain rule:" + "\n"
    r"    $\frac{\partial L}{\partial W[a', b']} = \sum_{i} \sum_{j} \frac{\partial L}{\partial Y[i, j]} \frac{\partial Y[i, j]}{\partial W[a', b']}$" + "\n\n"
    r"• From discrete convolution: $Y[i, j] = \sum_{a, b} X[i-a, j-b] W[a, b]$" + "\n"
    r"    $\frac{\partial Y[i, j]}{\partial W[a', b']} = X[i-a', j-b']$" + "\n\n"
    r"• Substituting back:" + "\n"
    r"    $\frac{\partial L}{\partial W[a', b']} = \sum_{i} \sum_{j} \frac{\partial L}{\partial Y[i, j]} X[i-a', j-b']$" + "\n\n"
    r"CONCLUSION: This is the cross-correlation / convolution of" + "\n"
    r"input $X$ with the upstream gradient $\frac{\partial L}{\partial Y}$!"
)
ax1.text(0.05, 0.95, text_dw, va='top', ha='left', fontsize=9, linespacing=1.35,
         bbox=dict(boxstyle='round,pad=0.7', facecolor='#eff6ff', edgecolor='#93c5fd'))
ax1.axis('off')

# (B) dL/dX derivation
ax2.set_title(r"(B) Gradient w.r.t Input: $\frac{\partial L}{\partial X} = \frac{\partial L}{\partial Y} * \text{flip}_{180^\circ}(W)$", fontsize=11, fontweight='bold', pad=10)
text_dx = (
    "Input Gradient Derivation (Backprop to Previous Layer):\n\n"
    r"• An input pixel $X[i', j']$ affects a bounded neighborhood $P$ in $Y$:" + "\n"
    r"    $\frac{\partial L}{\partial X[i', j']} = \sum_{p \in P} \frac{\partial L}{\partial Y[p]} \frac{\partial Y[p]}{\partial X[i', j']}$" + "\n\n"
    r"• Since $Y[i'+a, j'+b] = \sum_{a, b} X[i', j'] W[a, b]$:" + "\n"
    r"    $\frac{\partial Y[i'+a, j'+b]}{\partial X[i', j']} = W[a, b]$" + "\n\n"
    r"• Substituting into the chain rule:" + "\n"
    r"    $\frac{\partial L}{\partial X[i', j']} = \sum_{a} \sum_{b} \frac{\partial L}{\partial Y[i'+a, j'+b]} W[a, b]$" + "\n\n"
    r"CONCLUSION: Summing with shifted indices equates to convolving" + "\n"
    r"upstream gradient $\frac{\partial L}{\partial Y}$ with filter $W$ rotated by $180^\circ$!"
)
ax2.text(0.05, 0.95, text_dx, va='top', ha='left', fontsize=9, linespacing=1.35,
         bbox=dict(boxstyle='round,pad=0.7', facecolor='#fefce8', edgecolor='#fde047'))
ax2.axis('off')

# (C) Max Pooling Backprop
ax3.set_title("(C) Backprop Through Max Pooling (Router Mechanism)", fontsize=11, fontweight='bold', pad=10)

# 2x2 forward
ax3.add_patch(Rectangle((0.5, 2.5), 1.0, 1.0, facecolor='#f1f5f9', edgecolor='#64748b'))
ax3.add_patch(Rectangle((1.5, 2.5), 1.0, 1.0, facecolor='#f87171', edgecolor='#b91c1c', lw=2))  # Max = 9
ax3.add_patch(Rectangle((0.5, 1.5), 1.0, 1.0, facecolor='#f1f5f9', edgecolor='#64748b'))
ax3.add_patch(Rectangle((1.5, 1.5), 1.0, 1.0, facecolor='#f1f5f9', edgecolor='#64748b'))
ax3.text(1.0, 3.0, "2", ha='center', va='center', fontsize=11, fontweight='bold')
ax3.text(2.0, 3.0, "9", ha='center', va='center', fontsize=12, fontweight='bold', color='#b91c1c')
ax3.text(1.0, 2.0, "1", ha='center', va='center', fontsize=11, fontweight='bold')
ax3.text(2.0, 2.0, "5", ha='center', va='center', fontsize=11, fontweight='bold')
ax3.text(1.5, 0.9, "Forward Pass\n(Max = 9 selected)", ha='center', fontsize=9, fontweight='bold')

# Arrow
ax3.annotate("", xy=(3.8, 2.5), xytext=(2.8, 2.5), arrowprops=dict(arrowstyle="<-", color='#ef4444', lw=2))
ax3.text(3.3, 2.7, "Backprop\ndL/dY = 4.0", ha='center', fontsize=8, fontweight='bold', color='#ef4444')

# 2x2 backward
ax3.add_patch(Rectangle((4.2, 2.5), 1.0, 1.0, facecolor='#f1f5f9', edgecolor='#64748b'))
ax3.add_patch(Rectangle((5.2, 2.5), 1.0, 1.0, facecolor='#fca5a5', edgecolor='#b91c1c', lw=2))  # Receives full 4.0
ax3.add_patch(Rectangle((4.2, 1.5), 1.0, 1.0, facecolor='#f1f5f9', edgecolor='#64748b'))
ax3.add_patch(Rectangle((5.2, 1.5), 1.0, 1.0, facecolor='#f1f5f9', edgecolor='#64748b'))
ax3.text(4.7, 3.0, "0", ha='center', va='center', fontsize=11, fontweight='bold')
ax3.text(5.7, 3.0, "+4.0", ha='center', va='center', fontsize=11, fontweight='bold', color='#b91c1c')
ax3.text(4.7, 2.0, "0", ha='center', va='center', fontsize=11, fontweight='bold')
ax3.text(5.7, 2.0, "0", ha='center', va='center', fontsize=11, fontweight='bold')
ax3.text(5.2, 0.9, "Gradient Route: 100% to Winner\nAll other elements receive 0", ha='center', fontsize=9, fontweight='bold', color='#b91c1c')

ax3.set_xlim(0, 6.8)
ax3.set_ylim(0.4, 4.0)
ax3.axis('off')

# (D) Average Pooling Backprop
ax4.set_title("(D) Backprop Through Average Pooling (Uniform Distributor)", fontsize=11, fontweight='bold', pad=10)

# Forward
ax4.add_patch(Rectangle((0.5, 2.0), 2.0, 2.0, facecolor='#e0f2fe', edgecolor='#0284c7', lw=1.5))
ax4.text(1.5, 3.0, "2x2 Block\nMean", ha='center', va='center', fontsize=10, fontweight='bold', color='#0369a1')
ax4.text(1.5, 1.2, "Forward Pass:\nOutput = Mean(Block)", ha='center', fontsize=9, fontweight='bold')

# Arrow
ax4.annotate("", xy=(3.8, 3.0), xytext=(2.8, 3.0), arrowprops=dict(arrowstyle="<-", color='#0284c7', lw=2))
ax4.text(3.3, 3.2, "Backprop\ndL/dY = 4.0", ha='center', fontsize=8, fontweight='bold', color='#0284c7')

# Backward
ax4.add_patch(Rectangle((4.2, 3.0), 1.0, 1.0, facecolor='#bae6fd', edgecolor='#0284c7'))
ax4.add_patch(Rectangle((5.2, 3.0), 1.0, 1.0, facecolor='#bae6fd', edgecolor='#0284c7'))
ax4.add_patch(Rectangle((4.2, 2.0), 1.0, 1.0, facecolor='#bae6fd', edgecolor='#0284c7'))
ax4.add_patch(Rectangle((5.2, 2.0), 1.0, 1.0, facecolor='#bae6fd', edgecolor='#0284c7'))
ax4.text(4.7, 3.5, "+1.0", ha='center', va='center', fontsize=10, fontweight='bold', color='#0369a1')
ax4.text(5.7, 3.5, "+1.0", ha='center', va='center', fontsize=10, fontweight='bold', color='#0369a1')
ax4.text(4.7, 2.5, "+1.0", ha='center', va='center', fontsize=10, fontweight='bold', color='#0369a1')
ax4.text(5.7, 2.5, "+1.0", ha='center', va='center', fontsize=10, fontweight='bold', color='#0369a1')
ax4.text(5.2, 1.2, "Gradient Distributed Uniformly:\nGrad = Upstream / (K * K) = 4.0 / 4 = 1.0", ha='center', fontsize=9, fontweight='bold', color='#0369a1')

ax4.set_xlim(0, 6.8)
ax4.set_ylim(0.4, 4.4)
ax4.axis('off')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "fig04_cnn_backpropagation_math.png"), dpi=180, facecolor='white')
plt.close()
print("Saved fig04_cnn_backpropagation_math.png")

# -------------------------------------------------------------
# FIGURE 5: Batch Normalization Backprop Computational DAG
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(14, 6.5), facecolor='white')
ax.set_title("Batch Normalization Forward & Backward Computational Graph", fontsize=12, fontweight='bold', pad=15)

# Boxes
nodes = [
    ("x_i", 0.5, 2.5, "#e2e8f0"),
    ("mu", 2.2, 3.8, "#fef08a"),
    ("sigma^2", 4.0, 3.8, "#fed7aa"),
    ("x_hat", 4.0, 1.5, "#bae6fd"),
    ("y_i", 6.5, 2.5, "#bbf7d0"),
    ("Loss L", 8.5, 2.5, "#fca5a5"),
    ("gamma, beta", 6.5, 4.0, "#e9d5ff")
]

for name, x, y, col in nodes:
    ax.add_patch(FancyBboxPatch((x-0.5, y-0.4), 1.0, 0.8, boxstyle="round,pad=0.1", facecolor=col, edgecolor='#1e293b', lw=1.5))
    ax.text(x, y, name, ha='center', va='center', fontsize=10, fontweight='bold')

# Forward arrows (blue)
fwd_arrows = [
    ((0.5, 2.9), (1.7, 3.8)),
    ((2.7, 3.8), (3.5, 3.8)),
    ((0.5, 2.1), (3.5, 1.5)),
    ((2.2, 3.4), (3.7, 1.9)),
    ((4.5, 3.6), (4.3, 1.9)),
    ((4.5, 1.5), (6.0, 2.3)),
    ((6.5, 3.6), (6.5, 2.9)),
    ((7.0, 2.5), (8.0, 2.5))
]
for p1, p2 in fwd_arrows:
    ax.annotate("", xy=p2, xytext=p1, arrowprops=dict(arrowstyle="->", color='#0284c7', lw=1.8))

# Backward equations box
eqs_text = (
    "Batch Normalization Backpropagation Chain Rule Sequence:\n"
    r"1. $\frac{\partial L}{\partial \gamma} = \sum_{i=1}^m \frac{\partial L}{\partial y_i} \hat{x}_i \quad \text{and} \quad \frac{\partial L}{\partial \beta} = \sum_{i=1}^m \frac{\partial L}{\partial y_i}$" + "\n"
    r"2. $\frac{\partial L}{\partial \hat{x}_i} = \frac{\partial L}{\partial y_i} \gamma$" + "\n"
    r"3. $\frac{\partial L}{\partial \sigma^2} = \sum_{i=1}^m \frac{\partial L}{\partial \hat{x}_i} (x_i - \mu) \cdot \left( -\frac{1}{2}(\sigma^2 + \epsilon)^{-3/2} \right)$" + "\n"
    r"4. $\frac{\partial L}{\partial \mu} = \left( \sum_{i=1}^m \frac{\partial L}{\partial \hat{x}_i} \frac{-1}{\sqrt{\sigma^2 + \epsilon}} \right) + \frac{\partial L}{\partial \sigma^2} \frac{\sum_{i=1}^m -2(x_i - \mu)}{m}$" + "\n"
    r"5. $\frac{\partial L}{\partial x_i} = \frac{\partial L}{\partial \hat{x}_i} \frac{1}{\sqrt{\sigma^2 + \epsilon}} + \frac{\partial L}{\partial \sigma^2} \frac{2(x_i - \mu)}{m} + \frac{\partial L}{\partial \mu} \frac{1}{m}$"
)
ax.text(4.5, 0.4, eqs_text, ha='center', va='bottom', fontsize=9.5, linespacing=1.35,
        bbox=dict(boxstyle="round,pad=0.7", facecolor='#f8fafc', edgecolor='#94a3b8'))

ax.text(1.2, 4.6, "Forward Pass (Blue arrows)", color='#0284c7', fontsize=9, fontweight='bold')
ax.text(7.5, 4.6, "Backward Gradients (Chain rule)", color='#dc2626', fontsize=9, fontweight='bold')

ax.set_xlim(-0.2, 9.5)
ax.set_ylim(0.0, 5.2)
ax.axis('off')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "fig05_batchnorm_backprop_computational_graph.png"), dpi=180, facecolor='white')
plt.close()
print("Saved fig05_batchnorm_backprop_computational_graph.png")

# -------------------------------------------------------------
# FIGURE 6: AlexNet Architecture & Computation Bottleneck
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), facecolor='white')

# Subplot 1: AlexNet Layer by Layer
ax1.set_title("(A) AlexNet (2012) Architecture Pipeline", fontsize=11, fontweight='bold', pad=10)

layers = [
    ("Input", "227x227x3", 0.0, "#94a3b8"),
    ("Conv1", "11x11, S=4\n96 filters", 0.035, "#38bdf8"),
    ("Pool1", "3x3, S=2", 0.0, "#bae6fd"),
    ("Conv2", "5x5, pad 2\n256 filters", 0.307, "#38bdf8"),
    ("Pool2", "3x3, S=2", 0.0, "#bae6fd"),
    ("Conv3", "3x3, pad 1\n384 filters", 0.885, "#38bdf8"),
    ("Conv4", "3x3, pad 1\n384 filters", 0.663, "#38bdf8"),
    ("Conv5", "3x3, pad 1\n256 filters", 0.442, "#38bdf8"),
    ("Pool5", "3x3, S=2", 0.0, "#bae6fd"),
    ("FC6", "4096 units\n(6x6x256 in)", 37.75, "#fb923c"),
    ("FC7", "4096 units", 16.78, "#fb923c"),
    ("FC8", "1000 Softmax", 4.10, "#f87171")
]

y_pos = np.arange(len(layers))
layer_names = [l[0] for l in layers]
ax1.barh(y_pos, [1]*len(layers), color=[l[3] for l in layers], edgecolor='#1e293b', height=0.7)
ax1.set_yticks(y_pos)
ax1.set_yticklabels(layer_names, fontsize=9, fontweight='bold')
ax1.invert_yaxis()

for idx, (name, spec, params, col) in enumerate(layers):
    param_str = f"Params: {params:.2f}M" if params > 0 else "No weights"
    ax1.text(0.5, idx, f"{spec} | {param_str}", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#0f172a')

ax1.set_xlim(0, 1.0)
ax1.axis('off')

# Subplot 2: Parameter vs FLOPs Distribution (The Asymmetry)
ax2.set_title("(B) Parameter vs Computation Distribution Bottleneck", fontsize=11, fontweight='bold', pad=10)

labels = ['Conv Layers (1-5)', 'FC Layers (6-8)']
params_pct = [6.2, 93.8]    # ~3.7M vs ~58M
flops_pct = [90.5, 9.5]     # Convolutional operations dominate FLOPs

x = np.arange(2)
width = 0.35

rects1 = ax2.bar(x - width/2, params_pct, width, label='Parameters (%)', color='#fb923c', edgecolor='#1e293b')
rects2 = ax2.bar(x + width/2, flops_pct, width, label='Computation FLOPs (%)', color='#38bdf8', edgecolor='#1e293b')

ax2.set_ylabel('Percentage of Total (%)', fontsize=10, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(labels, fontsize=10, fontweight='bold')
ax2.set_ylim(0, 115)
ax2.legend(fontsize=9, loc='upper center')
ax2.grid(axis='y', linestyle='--', alpha=0.5)

for rect in rects1:
    h = rect.get_height()
    ax2.text(rect.get_x() + rect.get_width()/2., h + 2, f"{h:.1f}%", ha='center', va='bottom', fontsize=9, fontweight='bold', color='#c2410c')
for rect in rects2:
    h = rect.get_height()
    ax2.text(rect.get_x() + rect.get_width()/2., h + 2, f"{h:.1f}%", ha='center', va='bottom', fontsize=9, fontweight='bold', color='#0369a1')

ax2.text(0.5, 80, "THE ASYMMETRY:\n• FC layers store 94% of weights (Memory Bottleneck)\n• Conv layers perform 90% of arithmetic (Compute Bottleneck)",
         ha='center', fontsize=9, fontweight='bold', bbox=dict(boxstyle='round,pad=0.5', facecolor='#f8fafc', edgecolor='#cbd5e1'))

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "fig06_alexnet_architecture_and_bottleneck.png"), dpi=180, facecolor='white')
plt.close()
print("Saved fig06_alexnet_architecture_and_bottleneck.png")

# -------------------------------------------------------------
# FIGURE 7: Receptive Field Equivalency: VGG Stacked 3x3 vs 7x7
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), facecolor='white')

# Subplot 1: Geometric Stacking
ax1.set_title("(A) Receptive Field: 3 Stacked 3x3 Convs = 1 Single 7x7 Conv", fontsize=11, fontweight='bold', pad=10)

# Input Layer (7 units)
for i in range(7):
    ax1.add_patch(Rectangle((i*0.9, 0.5), 0.8, 0.6, facecolor='#bae6fd', edgecolor='#0284c7'))
    ax1.text(i*0.9 + 0.4, 0.8, f"x_{i}", ha='center', va='center', fontsize=8)
ax1.text(3.1, 0.1, "Layer 0: Input Image (7 units span)", ha='center', fontsize=9, fontweight='bold')

# Layer 1: Conv 3x3 (5 units)
for i in range(5):
    ax1.add_patch(Rectangle((0.45 + i*0.9, 1.8), 0.8, 0.6, facecolor='#fed7aa', edgecolor='#ea580c'))
ax1.text(3.1, 1.5, "Layer 1: 3x3 Conv (Receptive Field = 3x3)", ha='center', fontsize=9, fontweight='bold', color='#c2410c')

# Layer 2: Conv 3x3 (3 units)
for i in range(3):
    ax1.add_patch(Rectangle((0.9 + i*0.9, 3.1), 0.8, 0.6, facecolor='#fde047', edgecolor='#ca8a04'))
ax1.text(3.1, 2.8, "Layer 2: 3x3 Conv (Receptive Field = 5x5)", ha='center', fontsize=9, fontweight='bold', color='#854d0e')

# Layer 3: Conv 3x3 (1 unit)
ax1.add_patch(Rectangle((1.8, 4.4), 0.8, 0.6, facecolor='#bbf7d0', edgecolor='#16a34a', lw=2))
ax1.text(2.2, 4.7, "y", ha='center', va='center', fontsize=10, fontweight='bold', color='#166534')
ax1.text(3.1, 4.1, "Layer 3: 3x3 Conv (Effective Receptive Field = 7x7!)", ha='center', fontsize=9, fontweight='bold', color='#166534')

# Connective lines
ax1.plot([0.4, 1.8], [1.1, 4.4], color='#64748b', linestyle='--', alpha=0.6)
ax1.plot([5.8, 2.6], [1.1, 4.4], color='#64748b', linestyle='--', alpha=0.6)

ax1.set_xlim(-0.2, 6.5)
ax1.set_ylim(-0.2, 5.3)
ax1.axis('off')

# Subplot 2: Parameter and Non-linearity Comparison
ax2.set_title("(B) VGG Design Advantage: Parameters & Non-Linearities", fontsize=11, fontweight='bold', pad=10)

comparison_text = (
    "Theoretical Comparison (C Input & Output Channels):\n\n"
    r"1. Single $7 \times 7$ Convolution Layer:" + "\n"
    r"   • Weights: $7 \times 7 \times C^2 = 49 C^2$" + "\n"
    r"   • Activation Functions: 1 non-linear ReLU" + "\n\n"
    r"2. Stack of Three $3 \times 3$ Convolution Layers:" + "\n"
    r"   • Weights: $3 \times (3 \times 3 \times C^2) = 27 C^2$" + "\n"
    r"   • Activation Functions: 3 non-linear ReLUs!" + "\n\n"
    "Key Advantages of VGG Stacking Philosophy:\n"
    r"• Parameter Reduction: $\frac{49 - 27}{49} \approx 45\%$ fewer parameters!" + "\n"
    r"• Discriminative Power: 3 successive ReLUs allow the network" + "\n"
    r"  to learn significantly richer non-linear feature representations." + "\n"
    r"• Architectural Simplicity: Only $3 \times 3$ convs (stride 1, pad 1)" + "\n"
    r"  and $2 \times 2$ max pooling (stride 2) throughout the entire network."
)

ax2.text(0.05, 0.95, comparison_text, va='top', ha='left', fontsize=9.5, linespacing=1.45,
         bbox=dict(boxstyle='round,pad=0.8', facecolor='#f8fafc', edgecolor='#cbd5e1'))
ax2.axis('off')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "fig07_receptive_field_vgg_vs_alexnet.png"), dpi=180, facecolor='white')
plt.close()
print("Saved fig07_receptive_field_vgg_vs_alexnet.png")

# -------------------------------------------------------------
# FIGURE 8: Evolution of Classic CNN Architectures
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(15, 6), facecolor='white')
ax.set_title("Evolution of Foundational CNN Architectures (1980 - 2014)", fontsize=12, fontweight='bold', pad=15)

timeline = [
    ("Neocognitron\n(1980)", "Fukushima", "First hierarchical\nS-cells & C-cells", "#e2e8f0", 0.5),
    ("LeNet-5\n(1998)", "Y. LeCun et al.", "Conv-Pool-Conv-Pool-FC\nDigit recognition (MNIST)", "#bae6fd", 2.5),
    ("AlexNet\n(2012)", "Krizhevsky et al.", "ILSVRC 2012 Winner (16.4% err)\nReLU, Dropout, GPU, LRN", "#fed7aa", 5.0),
    ("ZFNet\n(2013)", "Zeiler & Fergus", "ILSVRC 2013 Winner (11.7% err)\nDeconv visualization, 7x7 S=2", "#fde047", 7.5),
    ("VGGNet\n(2014)", "Simonyan & Zisserman", "ILSVRC 2014 Runner-up (7.3% err)\nHomogeneous 3x3 stacks, depth", "#bbf7d0", 10.0)
]

# Baseline arrow
ax.annotate("", xy=(11.5, 3.0), xytext=(0.0, 3.0), arrowprops=dict(arrowstyle="->", color='#475569', lw=3))

for name, author, desc, col, x_pos in timeline:
    # Circle marker on timeline
    ax.add_patch(Circle((x_pos, 3.0), 0.15, facecolor='#0f172a', edgecolor='white', lw=2))
    # Top card (Title & Author)
    ax.add_patch(FancyBboxPatch((x_pos - 0.95, 3.5), 1.9, 1.2, boxstyle="round,pad=0.1", facecolor=col, edgecolor='#1e293b', lw=1.5))
    ax.text(x_pos, 4.25, name, ha='center', va='center', fontsize=9.5, fontweight='bold', color='#0f172a')
    ax.text(x_pos, 3.75, author, ha='center', va='center', fontsize=8, color='#475569', style='italic')

    # Bottom card (Description)
    ax.add_patch(FancyBboxPatch((x_pos - 0.95, 1.3), 1.9, 1.2, boxstyle="round,pad=0.1", facecolor='#f8fafc', edgecolor='#94a3b8', lw=1.2))
    ax.text(x_pos, 1.9, desc, ha='center', va='center', fontsize=8, color='#1e293b', linespacing=1.25)

ax.set_xlim(-0.5, 12.0)
ax.set_ylim(0.5, 5.2)
ax.axis('off')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "fig08_cnn_evolution_timeline.png"), dpi=180, facecolor='white')
plt.close()
print("Saved fig08_cnn_evolution_timeline.png")

print("All 8 Week 4 figures successfully generated!")
