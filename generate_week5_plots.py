import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Polygon
import numpy as np

output_dir = "/Volumes/1700 APFS/PERSONAL_PROGRAMMING_PROJECTS/Notes/Deep Learning for Computer Vision/month 2/week 5/assets"
os.makedirs(output_dir, exist_ok=True)

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#2b2b2b'
plt.rcParams['axes.linewidth'] = 0.8

# -------------------------------------------------------------
# FIGURE 1: Inception Module & 1x1 Bottleneck Dimensionality Reduction
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), facecolor='white')

# (A) Naive Inception Module
ax1.set_title("(A) Naive Inception Module (Compute Explosion)", fontsize=11, fontweight='bold', pad=12)

# Input
ax1.add_patch(FancyBboxPatch((0.5, 0.4), 6.0, 0.7, boxstyle="round,pad=0.1", facecolor='#e2e8f0', edgecolor='#475569', lw=1.5))
ax1.text(3.5, 0.75, "Previous Layer Feature Map (e.g., 28x28x256)", ha='center', va='center', fontsize=9, fontweight='bold')

# 4 Parallel Branches (Naive)
branches_naive = [
    ("1x1 Conv\n(128 filters)", 1.0, "#bae6fd", "#0284c7"),
    ("3x3 Conv\n(192 filters)", 2.6, "#fed7aa", "#ea580c"),
    ("5x5 Conv\n(96 filters)", 4.2, "#fca5a5", "#dc2626"),
    ("3x3 MaxPool\n(stride 1, pad 1)", 5.8, "#bbf7d0", "#16a34a")
]

for name, x, bg, border in branches_naive:
    ax1.annotate("", xy=(x + 0.3, 1.8), xytext=(3.5, 1.1), arrowprops=dict(arrowstyle="->", color='#64748b', lw=1.2))
    ax1.add_patch(FancyBboxPatch((x - 0.4, 1.8), 1.4, 1.1, boxstyle="round,pad=0.1", facecolor=bg, edgecolor=border, lw=1.5))
    ax1.text(x + 0.3, 2.35, name, ha='center', va='center', fontsize=8, fontweight='bold')

# Filter Concatenation
for name, x, bg, border in branches_naive:
    ax1.annotate("", xy=(3.5, 3.6), xytext=(x + 0.3, 2.9), arrowprops=dict(arrowstyle="->", color='#64748b', lw=1.2))

ax1.add_patch(FancyBboxPatch((0.5, 3.6), 6.0, 0.7, boxstyle="round,pad=0.1", facecolor='#fef08a', edgecolor='#ca8a04', lw=1.5))
ax1.text(3.5, 3.95, "Depth Concatenation (128 + 192 + 96 + 256 = 672 channels!)\nTotal FLOPs: ~854 Million Operations per Block!",
         ha='center', va='center', fontsize=8.5, fontweight='bold', color='#854d0e')

ax1.set_xlim(0, 7.0)
ax1.set_ylim(0.1, 4.6)
ax1.axis('off')

# (B) Inception with 1x1 Dimension Reduction
ax2.set_title("(B) Inception Module with 1x1 Bottleneck Reductions", fontsize=11, fontweight='bold', pad=12)

# Input
ax2.add_patch(FancyBboxPatch((0.5, 0.4), 6.0, 0.6, boxstyle="round,pad=0.1", facecolor='#e2e8f0', edgecolor='#475569', lw=1.5))
ax2.text(3.5, 0.7, "Previous Layer Feature Map (28x28x256)", ha='center', va='center', fontsize=9, fontweight='bold')

# Branch 1: 1x1 Conv
ax2.annotate("", xy=(1.0, 2.2), xytext=(3.5, 1.0), arrowprops=dict(arrowstyle="->", color='#64748b', lw=1.2))
ax2.add_patch(FancyBboxPatch((0.4, 2.2), 1.2, 0.8, boxstyle="round,pad=0.1", facecolor='#bae6fd', edgecolor='#0284c7', lw=1.5))
ax2.text(1.0, 2.6, "1x1 Conv\n(64)", ha='center', va='center', fontsize=8, fontweight='bold')

# Branch 2: 1x1 (reduce) -> 3x3
ax2.annotate("", xy=(2.6, 1.4), xytext=(3.5, 1.0), arrowprops=dict(arrowstyle="->", color='#64748b', lw=1.2))
ax2.add_patch(FancyBboxPatch((2.0, 1.4), 1.2, 0.6, boxstyle="round,pad=0.08", facecolor='#fef08a', edgecolor='#ca8a04', lw=1.2))
ax2.text(2.6, 1.7, "1x1 Red (96)", ha='center', va='center', fontsize=7.5, fontweight='bold')
ax2.annotate("", xy=(2.6, 2.4), xytext=(2.6, 2.0), arrowprops=dict(arrowstyle="->", color='#64748b', lw=1.2))
ax2.add_patch(FancyBboxPatch((2.0, 2.4), 1.2, 0.7, boxstyle="round,pad=0.08", facecolor='#fed7aa', edgecolor='#ea580c', lw=1.5))
ax2.text(2.6, 2.75, "3x3 Conv\n(128)", ha='center', va='center', fontsize=8, fontweight='bold')

# Branch 3: 1x1 (reduce) -> 5x5
ax2.annotate("", xy=(4.3, 1.4), xytext=(3.5, 1.0), arrowprops=dict(arrowstyle="->", color='#64748b', lw=1.2))
ax2.add_patch(FancyBboxPatch((3.7, 1.4), 1.2, 0.6, boxstyle="round,pad=0.08", facecolor='#fef08a', edgecolor='#ca8a04', lw=1.2))
ax2.text(4.3, 1.7, "1x1 Red (16)", ha='center', va='center', fontsize=7.5, fontweight='bold')
ax2.annotate("", xy=(4.3, 2.4), xytext=(4.3, 2.0), arrowprops=dict(arrowstyle="->", color='#64748b', lw=1.2))
ax2.add_patch(FancyBboxPatch((3.7, 2.4), 1.2, 0.7, boxstyle="round,pad=0.08", facecolor='#fca5a5', edgecolor='#dc2626', lw=1.5))
ax2.text(4.3, 2.75, "5x5 Conv\n(32)", ha='center', va='center', fontsize=8, fontweight='bold')

# Branch 4: 3x3 MaxPool -> 1x1 Conv
ax2.annotate("", xy=(5.9, 1.4), xytext=(3.5, 1.0), arrowprops=dict(arrowstyle="->", color='#64748b', lw=1.2))
ax2.add_patch(FancyBboxPatch((5.3, 1.4), 1.2, 0.6, boxstyle="round,pad=0.08", facecolor='#bbf7d0', edgecolor='#16a34a', lw=1.2))
ax2.text(5.9, 1.7, "3x3 Pool", ha='center', va='center', fontsize=7.5, fontweight='bold')
ax2.annotate("", xy=(5.9, 2.4), xytext=(5.9, 2.0), arrowprops=dict(arrowstyle="->", color='#64748b', lw=1.2))
ax2.add_patch(FancyBboxPatch((5.3, 2.4), 1.2, 0.7, boxstyle="round,pad=0.08", facecolor='#fef08a', edgecolor='#ca8a04', lw=1.5))
ax2.text(5.9, 2.75, "1x1 Red\n(32)", ha='center', va='center', fontsize=8, fontweight='bold')

# Concatenation
for x_top in [1.0, 2.6, 4.3, 5.9]:
    ax2.annotate("", xy=(3.5, 3.6), xytext=(x_top, 3.1), arrowprops=dict(arrowstyle="->", color='#64748b', lw=1.2))

ax2.add_patch(FancyBboxPatch((0.5, 3.6), 6.0, 0.7, boxstyle="round,pad=0.1", facecolor='#bbf7d0', edgecolor='#16a34a', lw=1.5))
ax2.text(3.5, 3.95, "Depth Concatenation (64 + 128 + 32 + 32 = 256 channels!)\nTotal FLOPs: ~358 Million (Over 2.4x Speedup via 1x1 Projectors!)",
         ha='center', va='center', fontsize=8.5, fontweight='bold', color='#166534')

ax2.set_xlim(0, 7.0)
ax2.set_ylim(0.1, 4.6)
ax2.axis('off')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "fig01_inception_module_and_1x1_bottleneck.png"), dpi=180, facecolor='white')
plt.close()
print("Saved fig01_inception_module_and_1x1_bottleneck.png")

# -------------------------------------------------------------
# FIGURE 2: The Degradation Problem & ResNet Gradient Superhighway
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5.5), facecolor='white')

# (A) Degradation problem plot
epochs = np.linspace(1, 60, 60)
train_err_20 = 28 * np.exp(-epochs/15) + 8.5
test_err_20 = 32 * np.exp(-epochs/15) + 11.2
train_err_56 = 35 * np.exp(-epochs/18) + 13.8  # Higher training error!
test_err_56 = 39 * np.exp(-epochs/18) + 16.5  # Higher test error!

ax1.set_title("(A) The Degradation Problem (Underfitting in Plain Nets)", fontsize=11, fontweight='bold', pad=10)
ax1.plot(epochs, train_err_20, color='#0284c7', linestyle='--', lw=2, label='20-layer Plain (Train Error)')
ax1.plot(epochs, test_err_20, color='#0284c7', lw=2.5, label='20-layer Plain (Test Error)')
ax1.plot(epochs, train_err_56, color='#dc2626', linestyle='--', lw=2, label='56-layer Plain (Train Error - Degraded!)')
ax1.plot(epochs, test_err_56, color='#dc2626', lw=2.5, label='56-layer Plain (Test Error)')

ax1.text(35, 14.5, "56-layer has HIGHER training error\nthan 20-layer! (NOT overfitting,\nbut optimization failure/degradation)",
         fontsize=8.5, color='#991b1b', fontweight='bold', bbox=dict(boxstyle='round,pad=0.5', facecolor='#fee2e2', edgecolor='#f87171'))

ax1.set_xlabel("Training Epochs", fontsize=10, fontweight='bold')
ax1.set_ylabel("Error Rate (%)", fontsize=10, fontweight='bold')
ax1.set_ylim(5, 45)
ax1.legend(fontsize=8.5, loc='upper right')
ax1.grid(True, linestyle='--', alpha=0.5)

# (B) Residual Block & Clean Gradient Flow
ax2.set_title(r"(B) Residual Block Architecture: $H(x) = F(x) + x$", fontsize=11, fontweight='bold', pad=10)

# Input x
ax2.add_patch(Circle((1.5, 4.5), 0.35, facecolor='#e2e8f0', edgecolor='#475569', lw=1.5))
ax2.text(1.5, 4.5, "x", ha='center', va='center', fontsize=11, fontweight='bold')

# Main branch
ax2.annotate("", xy=(1.5, 3.4), xytext=(1.5, 4.15), arrowprops=dict(arrowstyle="->", color='#0284c7', lw=2))
ax2.add_patch(FancyBboxPatch((0.6, 2.7), 1.8, 0.7, boxstyle="round,pad=0.1", facecolor='#bae6fd', edgecolor='#0284c7', lw=1.5))
ax2.text(1.5, 3.05, "Weight / Conv\n(e.g., 3x3)", ha='center', va='center', fontsize=8.5, fontweight='bold')

ax2.annotate("", xy=(1.5, 2.0), xytext=(1.5, 2.7), arrowprops=dict(arrowstyle="->", color='#0284c7', lw=2))
ax2.add_patch(FancyBboxPatch((0.6, 1.3), 1.8, 0.7, boxstyle="round,pad=0.1", facecolor='#bae6fd', edgecolor='#0284c7', lw=1.5))
ax2.text(1.5, 1.65, "Weight / Conv\n(e.g., 3x3)", ha='center', va='center', fontsize=8.5, fontweight='bold')

# Addition node (+)
ax2.annotate("", xy=(1.5, 0.7), xytext=(1.5, 1.3), arrowprops=dict(arrowstyle="->", color='#0284c7', lw=2))
ax2.add_patch(Circle((1.5, 0.45), 0.25, facecolor='#fef08a', edgecolor='#ca8a04', lw=1.5))
ax2.text(1.5, 0.45, "+", ha='center', va='center', fontsize=14, fontweight='bold')

# Identity Shortcut Connection (Skip Connection)
path_pts = [(1.85, 4.5), (3.6, 4.5), (3.6, 0.45), (1.75, 0.45)]
for i in range(len(path_pts)-1):
    ax2.plot([path_pts[i][0], path_pts[i+1][0]], [path_pts[i][1], path_pts[i+1][1]], color='#16a34a', lw=2.5)
ax2.annotate("", xy=(1.75, 0.45), xytext=(2.2, 0.45), arrowprops=dict(arrowstyle="->", color='#16a34a', lw=2.5))
ax2.text(3.7, 2.5, "Identity Shortcut (x)\nClean Gradient Superhighway!", ha='left', va='center', fontsize=9, fontweight='bold', color='#166534')

# Output
ax2.annotate("", xy=(1.5, -0.4), xytext=(1.5, 0.2), arrowprops=dict(arrowstyle="->", color='#0284c7', lw=2))
ax2.text(1.5, -0.55, "Output: H(x) = F(x) + x", ha='center', va='center', fontsize=10, fontweight='bold', color='#0f172a')

# Mathematical Gradient Flow Box
grad_box_text = (
    "Analytical Gradient Flow Through Residual Connection:\n\n"
    r"  $x_L = x_l + \sum_{i=l}^{L-1} F(x_i, W_i)$" + "\n\n"
    r"  $\frac{\partial \mathcal{L}}{\partial x_l} = \frac{\partial \mathcal{L}}{\partial x_L} \cdot \left( 1 + \frac{\partial}{\partial x_l} \sum_{i=l}^{L-1} F(x_i, W_i) \right)$" + "\n\n"
    "Crucial Insight: The '+ 1' term guarantees that\n"
    "gradient signals flow cleanly back to layer l even if\n"
    "the weight gradient term vanishes completely!"
)
ax2.text(4.4, 3.8, grad_box_text, va='top', ha='left', fontsize=8.5, linespacing=1.35,
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#f8fafc', edgecolor='#94a3b8'))

ax2.set_xlim(0, 9.2)
ax2.set_ylim(-0.8, 5.0)
ax2.axis('off')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "fig02_resnet_residual_block_and_gradient_flow.png"), dpi=180, facecolor='white')
plt.close()
print("Saved fig02_resnet_residual_block_and_gradient_flow.png")

# -------------------------------------------------------------
# FIGURE 3: Modern Architecture Variants: ResNeXt, DenseNet, SENet, ConvNeXt
# -------------------------------------------------------------
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 11), facecolor='white')

# (A) ResNeXt: Split-Transform-Merge (Cardinality)
ax1.set_title("(A) ResNeXt: Cardinality via Split-Transform-Merge", fontsize=11, fontweight='bold', pad=10)
ax1.add_patch(FancyBboxPatch((0.5, 4.0), 5.5, 0.6, boxstyle="round,pad=0.08", facecolor='#e2e8f0', edgecolor='#475569'))
ax1.text(3.25, 4.3, "Input X (256 channels)", ha='center', va='center', fontsize=9, fontweight='bold')

# Branches (Cardinality = 32 paths)
for idx, bx in enumerate([1.2, 2.3, 4.2, 5.3]):
    lbl = f"Path {idx+1}" if idx < 3 else "Path 32"
    ax1.annotate("", xy=(bx, 3.3), xytext=(3.25, 4.0), arrowprops=dict(arrowstyle="->", color='#64748b'))
    ax1.add_patch(FancyBboxPatch((bx - 0.45, 1.8), 0.9, 1.5, boxstyle="round,pad=0.08", facecolor='#fed7aa', edgecolor='#ea580c'))
    ax1.text(bx, 2.55, f"1x1(4)\n3x3(4)\n1x1(256)", ha='center', va='center', fontsize=7.5, fontweight='bold')
ax1.text(3.25, 2.55, "• • •", ha='center', va='center', fontsize=14, fontweight='bold', color='#ea580c')

# Aggregate
ax1.add_patch(Circle((3.25, 1.0), 0.25, facecolor='#fef08a', edgecolor='#ca8a04', lw=1.5))
ax1.text(3.25, 1.0, "+", ha='center', va='center', fontsize=12, fontweight='bold')
for bx in [1.2, 2.3, 4.2, 5.3]:
    ax1.annotate("", xy=(3.25, 1.25), xytext=(bx, 1.8), arrowprops=dict(arrowstyle="->", color='#64748b'))

# Skip connection
ax1.plot([6.0, 6.4, 6.4, 3.5], [4.3, 4.3, 1.0, 1.0], color='#16a34a', lw=2)
ax1.annotate("", xy=(3.5, 1.0), xytext=(3.9, 1.0), arrowprops=dict(arrowstyle="->", color='#16a34a', lw=2))

ax1.text(3.25, 0.3, "Cardinality C=32 improves accuracy more effectively\nthan simply increasing Depth or Width!", ha='center', fontsize=8.5, fontweight='bold', color='#c2410c')
ax1.set_xlim(0, 6.8)
ax1.set_ylim(0.0, 4.8)
ax1.axis('off')

# (B) DenseNet: Dense Feature Concatenation
ax2.set_title("(B) DenseNet: Direct Inter-Layer Feature Reuse", fontsize=11, fontweight='bold', pad=10)

layers = [("x_0\n(Input)", 0.8), ("x_1\n(k)", 2.2), ("x_2\n(k)", 3.6), ("x_3\n(k)", 5.0), ("x_4\n(k)", 6.4)]
for name, x in layers:
    ax2.add_patch(FancyBboxPatch((x-0.45, 1.8), 0.9, 1.2, boxstyle="round,pad=0.08", facecolor='#bae6fd', edgecolor='#0284c7', lw=1.5))
    ax2.text(x, 2.4, name, ha='center', va='center', fontsize=8.5, fontweight='bold')

# Sequential connections
for i in range(len(layers)-1):
    ax2.annotate("", xy=(layers[i+1][1]-0.45, 2.4), xytext=(layers[i][1]+0.45, 2.4), arrowprops=dict(arrowstyle="->", color='#0284c7', lw=1.5))

# Skip arcs
arcs = [
    (0.8, 3.6, 3.4), (0.8, 5.0, 3.8), (0.8, 6.4, 4.2),
    (2.2, 5.0, 3.3), (2.2, 6.4, 3.7),
    (3.6, 6.4, 3.2)
]
for x1, x2, arc_h in arcs:
    mid_x = (x1 + x2)/2
    ax2.plot([x1, mid_x, x2], [3.0, arc_h, 3.0], color='#ea580c', lw=1.5, linestyle='-')
    ax2.annotate("", xy=(x2, 3.0), xytext=(x2 - 0.1, 3.1), arrowprops=dict(arrowstyle="->", color='#ea580c', lw=1.5))

ax2.text(3.6, 0.6, "Dense connectivity: l(l+1)/2 = 10 connections for 5 layers!\nConcatenates feature maps [x_0, x_1, ...] instead of adding.\nGrowth rate k controls channel expansion per layer.",
         ha='center', fontsize=8.5, fontweight='bold', color='#0369a1')
ax2.set_xlim(0, 7.2)
ax2.set_ylim(0.2, 4.6)
ax2.axis('off')

# (C) SENet: Squeeze-and-Excitation
ax3.set_title("(C) SENet: Channel Squeeze, Excitation & Scaling", fontsize=11, fontweight='bold', pad=10)

# Input X
ax3.add_patch(Rectangle((0.5, 1.5), 1.0, 2.0, facecolor='#bae6fd', edgecolor='#0284c7', lw=1.5))
ax3.text(1.0, 2.5, "Input X\nHxWxC", ha='center', va='center', fontsize=8.5, fontweight='bold')

# Squeeze: GAP
ax3.annotate("", xy=(2.2, 2.5), xytext=(1.5, 2.5), arrowprops=dict(arrowstyle="->", color='#0284c7', lw=1.5))
ax3.text(1.85, 2.7, "Squeeze\n(GAP)", ha='center', fontsize=7.5, fontweight='bold')
ax3.add_patch(Rectangle((2.2, 1.8), 0.4, 1.4, facecolor='#fef08a', edgecolor='#ca8a04', lw=1.5))
ax3.text(2.4, 2.5, "1x1xC", ha='center', va='center', fontsize=7.5, rotation=90, fontweight='bold')

# Excitation: FC -> ReLU -> FC -> Sigmoid
ax3.annotate("", xy=(3.3, 2.5), xytext=(2.6, 2.5), arrowprops=dict(arrowstyle="->", color='#ea580c', lw=1.5))
ax3.text(2.95, 2.7, "Excitation\n(FC-ReLU-FC)", ha='center', fontsize=7.5, fontweight='bold')
ax3.add_patch(Rectangle((3.3, 1.8), 0.4, 1.4, facecolor='#fca5a5', edgecolor='#dc2626', lw=1.5))
ax3.text(3.5, 2.5, "Weights s", ha='center', va='center', fontsize=7.5, rotation=90, fontweight='bold')

# Scale (Reweight)
ax3.annotate("", xy=(4.6, 2.5), xytext=(3.7, 2.5), arrowprops=dict(arrowstyle="->", color='#16a34a', lw=1.5))
ax3.text(4.15, 2.7, "Scale\n(X * s)", ha='center', fontsize=7.5, fontweight='bold')
ax3.add_patch(Rectangle((4.6, 1.5), 1.0, 2.0, facecolor='#bbf7d0', edgecolor='#16a34a', lw=1.5))
ax3.text(5.1, 2.5, "Output X̃\nReweighted\nChannels", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#166534')

ax3.text(3.0, 0.6, "Squeeze-and-Excitation dynamically re-weights feature channels\nusing global context with tiny parameter overhead (<1%).",
         ha='center', fontsize=8.5, fontweight='bold', color='#991b1b')
ax3.set_xlim(0, 6.2)
ax3.set_ylim(0.2, 3.8)
ax3.axis('off')

# (D) ConvNeXt: Modernized ResNet with ViT Principles
ax4.set_title("(D) ConvNeXt Block: A 2020s CNN with ViT Design", fontsize=11, fontweight='bold', pad=10)

blocks_convnext = [
    ("7x7 Depthwise Conv (Large Kernel)", "#fed7aa", "#ea580c"),
    ("LayerNorm (Replaces BatchNorm)", "#e2e8f0", "#475569"),
    ("1x1 Conv (Inverted Bottleneck 4C)", "#fef08a", "#ca8a04"),
    ("GELU Activation (Replaces ReLU)", "#fca5a5", "#dc2626"),
    ("1x1 Conv (Project back to C)", "#bbf7d0", "#16a34a")
]

y_start = 3.6
for name, bg, border in blocks_convnext:
    ax4.add_patch(FancyBboxPatch((1.2, y_start - 0.25), 4.2, 0.5, boxstyle="round,pad=0.08", facecolor=bg, edgecolor=border, lw=1.2))
    ax4.text(3.3, y_start, name, ha='center', va='center', fontsize=8.5, fontweight='bold')
    if y_start > 1.2:
        ax4.annotate("", xy=(3.3, y_start - 0.35), xytext=(3.3, y_start - 0.25), arrowprops=dict(arrowstyle="->", color='#64748b'))
    y_start -= 0.6

# Skip connection
ax4.plot([0.8, 0.8, 0.8, 3.3], [3.6, 3.6, 0.7, 0.7], color='#16a34a', lw=2)
ax4.annotate("", xy=(3.3, 0.7), xytext=(2.8, 0.7), arrowprops=dict(arrowstyle="->", color='#16a34a', lw=2))
ax4.text(0.7, 2.1, "Identity\nShortcut", ha='right', va='center', fontsize=8, fontweight='bold', color='#166534')

ax4.text(3.3, 0.2, "Key Innovations: Inverted bottleneck (4x), 7x7 depthwise kernels,\nLayerNorm & GELU, fewer activations (ViT parity).",
         ha='center', fontsize=8.5, fontweight='bold', color='#1e293b')
ax4.set_xlim(0, 6.0)
ax4.set_ylim(0.0, 4.2)
ax4.axis('off')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "fig03_modern_architectures_family.png"), dpi=180, facecolor='white')
plt.close()
print("Saved fig03_modern_architectures_family.png")

# -------------------------------------------------------------
# FIGURE 4: MobileNet Depthwise Separable Convolutions
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5.5), facecolor='white')

# (A) Standard Conv vs Depthwise Separable Visual Breakdown
ax1.set_title("(A) Standard Conv vs Depthwise Separable Factorization", fontsize=11, fontweight='bold', pad=10)

# Standard Conv
ax1.add_patch(FancyBboxPatch((0.4, 3.4), 2.8, 1.2, boxstyle="round,pad=0.1", facecolor='#f1f5f9', edgecolor='#64748b', lw=1.5))
ax1.text(1.8, 4.0, "Standard Convolution\nFilter: Dk x Dk x M (Full Depth)\nApplied N times across channels", ha='center', va='center', fontsize=8.5, fontweight='bold')
ax1.text(1.8, 3.55, "Cost = Dk · Dk · M · N · Df · Df", ha='center', va='center', fontsize=8.5, color='#dc2626', fontweight='bold')

# Depthwise Separable (2 steps)
# Step 1: Depthwise
ax1.add_patch(FancyBboxPatch((3.8, 3.4), 2.8, 1.2, boxstyle="round,pad=0.1", facecolor='#fed7aa', edgecolor='#ea580c', lw=1.5))
ax1.text(5.2, 4.0, "Step 1: Depthwise Conv\nFilter: Dk x Dk x 1\n1 filter per channel (M filters total)", ha='center', va='center', fontsize=8.5, fontweight='bold')
ax1.text(5.2, 3.55, "Cost = Dk · Dk · M · Df · Df", ha='center', va='center', fontsize=8.5, color='#c2410c', fontweight='bold')

# Arrow down to Step 2
ax1.annotate("", xy=(5.2, 2.7), xytext=(5.2, 3.3), arrowprops=dict(arrowstyle="->", color='#64748b', lw=2))

# Step 2: Pointwise
ax1.add_patch(FancyBboxPatch((3.8, 1.4), 2.8, 1.2, boxstyle="round,pad=0.1", facecolor='#bae6fd', edgecolor='#0284c7', lw=1.5))
ax1.text(5.2, 2.0, "Step 2: Pointwise Conv\nFilter: 1 x 1 x M\nN filters linear combination", ha='center', va='center', fontsize=8.5, fontweight='bold')
ax1.text(5.2, 1.55, "Cost = M · N · Df · Df", ha='center', va='center', fontsize=8.5, color='#0369a1', fontweight='bold')

ax1.set_xlim(0, 7.0)
ax1.set_ylim(0.8, 4.8)
ax1.axis('off')

# (B) Computational Savings Ratio Derivation
ax2.set_title("(B) Mathematical Computation Reduction Ratio", fontsize=11, fontweight='bold', pad=10)

calc_text = (
    "Mathematical Derivation of Computational Savings:\n\n"
    r"• Standard Convolution Computational Cost:" + "\n"
    r"    $\text{Cost}_{\text{standard}} = D_K \cdot D_K \cdot M \cdot N \cdot D_F \cdot D_F$" + "\n\n"
    r"• Depthwise Separable Convolution Cost:" + "\n"
    r"    $\text{Cost}_{\text{separable}} = (D_K \cdot D_K \cdot M \cdot D_F \cdot D_F) + (M \cdot N \cdot D_F \cdot D_F)$" + "\n\n"
    r"• Ratio of Computational Loads:" + "\n"
    r"    $\text{Ratio} = \frac{D_K \cdot D_K \cdot M \cdot D_F^2 + M \cdot N \cdot D_F^2}{D_K \cdot D_K \cdot M \cdot N \cdot D_F^2} = \frac{1}{N} + \frac{1}{D_K^2}$" + "\n\n"
    "Benchmark Concrete Example (3x3 Filters, D_K = 3):\n"
    r"  For large output depth $N \gg 1$:" + "\n"
    r"  $\text{Ratio} \approx \frac{1}{D_K^2} = \frac{1}{3^2} = \frac{1}{9} \approx \mathbf{11.1\% \text{ of original compute!}}$" + "\n\n"
    r"  $\to \mathbf{8 \times \text{ to } 9 \times \text{ Computation & Parameter Speedup!}}$"
)
ax2.text(0.05, 0.95, calc_text, va='top', ha='left', fontsize=9, linespacing=1.38,
         bbox=dict(boxstyle='round,pad=0.8', facecolor='#f8fafc', edgecolor='#cbd5e1'))
ax2.axis('off')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "fig04_mobilenet_depthwise_separable_convolution.png"), dpi=180, facecolor='white')
plt.close()
print("Saved fig04_mobilenet_depthwise_separable_convolution.png")

# -------------------------------------------------------------
# FIGURE 5: Transfer Learning & Fine-Tuning Decision Matrix
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 8), facecolor='white')
ax.set_title("The Transfer Learning 2x2 Decision Matrix in CNNs", fontsize=12, fontweight='bold', pad=15)

# Dividing lines
ax.axhline(0.5, color='#475569', lw=2)
ax.axvline(0.5, color='#475569', lw=2)

# Quadrant 1: Top-Right (Large Dataset, Similar to Source)
ax.add_patch(Rectangle((0.52, 0.52), 0.46, 0.44, facecolor='#dcfce7', edgecolor='#16a34a', lw=2))
ax.text(0.75, 0.9, "QUADRANT 1: Fine-Tune Most / All Layers", ha='center', fontsize=9.5, fontweight='bold', color='#166534')
ax.text(0.75, 0.72,
        "• Low overfitting risk (large dataset)\n"
        "• High feature transferability (similar data)\n"
        "• Strategy: Fine-tune whole network\n"
        "  with smaller learning rate (e.g., 0.1x η)",
        ha='center', va='center', fontsize=8.5, linespacing=1.3)

# Quadrant 2: Top-Left (Small Dataset, Similar to Source)
ax.add_patch(Rectangle((0.02, 0.52), 0.46, 0.44, facecolor='#bae6fd', edgecolor='#0284c7', lw=2))
ax.text(0.25, 0.9, "QUADRANT 2: Train Linear Classifier on Top", ha='center', fontsize=9.5, fontweight='bold', color='#0369a1')
ax.text(0.25, 0.72,
        "• High overfitting risk on deep layers\n"
        "• Base features already match target\n"
        "• Strategy: Freeze all CNN backbone layers;\n"
        "  train only final linear layer / SVM",
        ha='center', va='center', fontsize=8.5, linespacing=1.3)

# Quadrant 3: Bottom-Right (Large Dataset, Dissimilar to Source)
ax.add_patch(Rectangle((0.52, 0.02), 0.46, 0.44, facecolor='#fef08a', edgecolor='#ca8a04', lw=2))
ax.text(0.75, 0.4, "QUADRANT 3: Fine-Tune Extensively / Train", ha='center', fontsize=9.5, fontweight='bold', color='#854d0e')
ax.text(0.75, 0.22,
        "• Low overfitting risk (sufficient data)\n"
        "• High-level features differ drastically\n"
        "• Strategy: Initialize from ImageNet but\n"
        "  fine-tune through entire depth",
        ha='center', va='center', fontsize=8.5, linespacing=1.3)

# Quadrant 4: Bottom-Left (Small Dataset, Dissimilar to Source)
ax.add_patch(Rectangle((0.02, 0.02), 0.46, 0.44, facecolor='#fee2e2', edgecolor='#dc2626', lw=2))
ax.text(0.25, 0.4, "QUADRANT 4: Train on Mid-Level Features", ha='center', fontsize=9.5, fontweight='bold', color='#991b1b')
ax.text(0.25, 0.22,
        "• WORST CASE: Severe overfitting + domain shift\n"
        "• Top layers are too specialized to source\n"
        "• Strategy: Train linear classifier from\n"
        "  earlier layers (textures/edges), not FC7",
        ha='center', va='center', fontsize=8.5, linespacing=1.3)

# Axis labels
ax.text(0.5, -0.05, "Data Similarity to ImageNet (Dissimilar ← → Similar)", ha='center', fontsize=10, fontweight='bold')
ax.text(-0.05, 0.5, "Target Dataset Size (Small ← → Large)", va='center', rotation=90, fontsize=10, fontweight='bold')

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "fig05_transfer_learning_decision_matrix.png"), dpi=180, facecolor='white')
plt.close()
print("Saved fig05_transfer_learning_decision_matrix.png")

# -------------------------------------------------------------
# FIGURE 6: CNN Interpretability: Layer Hierarchy & Occlusion Experiments
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), facecolor='white')

# (A) Feature Hierarchy in CNNs
ax1.set_title("(A) Hierarchical Feature Representations in Deep CNNs", fontsize=11, fontweight='bold', pad=10)

hierarchy = [
    ("Layer 1 (Low-Level)", "Oriented Edges, Gabor-like filters, Color Blobs\nUniversal across all datasets & visual tasks", "#bae6fd", "#0284c7"),
    ("Layer 3 (Mid-Level)", "Complex Textures, Corners, Circles, Object Parts\n(e.g., eye detectors, wheels, noses)", "#fed7aa", "#ea580c"),
    ("Layer 5 / FC (High-Level)", "Semantic Class Abstractions & Entire Objects\n(e.g., dog faces, car bodies, keyboards)", "#bbf7d0", "#16a34a")
]

for idx, (title, desc, bg, border) in enumerate(hierarchy):
    y = 3.6 - idx * 1.4
    ax1.add_patch(FancyBboxPatch((0.5, y), 6.0, 1.0, boxstyle="round,pad=0.1", facecolor=bg, edgecolor=border, lw=1.5))
    ax1.text(0.8, y + 0.65, title, fontsize=9.5, fontweight='bold', color='#0f172a')
    ax1.text(0.8, y + 0.25, desc, fontsize=8.5, color='#334155', linespacing=1.2)
    if idx < 2:
        ax1.annotate("", xy=(3.5, y - 0.35), xytext=(3.5, y), arrowprops=dict(arrowstyle="->", color='#64748b', lw=2))

ax1.set_xlim(0, 7.0)
ax1.set_ylim(0.2, 5.0)
ax1.axis('off')

# (B) Occlusion Experiment (Zeiler & Fergus)
ax2.set_title("(B) Occlusion Experiment: Diagnosing Spatial Sensitivity", fontsize=11, fontweight='bold', pad=10)

# Input image with dog face
ax2.add_patch(Rectangle((0.5, 1.8), 2.2, 2.2, facecolor='#f1f5f9', edgecolor='#64748b', lw=1.5))
ax2.text(1.6, 3.2, "Dog Face", ha='center', fontsize=9, fontweight='bold')
# Occluder box
ax2.add_patch(Rectangle((1.3, 2.4), 0.7, 0.7, facecolor='#334155', edgecolor='#0f172a', lw=1.5))
ax2.text(1.65, 2.75, "Gray\nPatch", ha='center', va='center', fontsize=7.5, color='white', fontweight='bold')
ax2.text(1.6, 1.4, "Input Image with\nSliding Gray Occluder", ha='center', fontsize=8.5, fontweight='bold')

# Arrow
ax2.annotate("", xy=(3.5, 2.9), xytext=(2.9, 2.9), arrowprops=dict(arrowstyle="->", color='#0284c7', lw=2))
ax2.text(3.2, 3.1, "Feed CNN", ha='center', fontsize=8, fontweight='bold')

# Heatmap output
heatmap = np.array([
    [0.92, 0.90, 0.88, 0.91],
    [0.89, 0.12, 0.18, 0.87],  # Massive drop when occluding face!
    [0.91, 0.15, 0.22, 0.89],
    [0.93, 0.91, 0.90, 0.92]
])
im = ax2.imshow(heatmap, cmap='hot', extent=[3.7, 5.9, 1.8, 4.0], origin='upper')
ax2.text(4.8, 1.4, "Probability Heatmap for 'Pomeranian'\n(Dark red = probability drops to 0.12!)", ha='center', fontsize=8.5, fontweight='bold', color='#991b1b')

ax2.text(3.3, 0.5, "Proof of Localization: When the face is occluded,\nmodel confidence collapses. Confirms CNN looks at the object,\nnot spurious background context!",
         ha='center', fontsize=8.5, fontweight='bold', bbox=dict(boxstyle='round,pad=0.5', facecolor='#f8fafc', edgecolor='#cbd5e1'))

ax2.set_xlim(0, 6.5)
ax2.set_ylim(0.1, 4.4)
ax2.axis('off')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "fig06_cnn_interpretability_and_visualization.png"), dpi=180, facecolor='white')
plt.close()
print("Saved fig06_cnn_interpretability_and_visualization.png")

# -------------------------------------------------------------
# FIGURE 7: Object Detection Taxonomy & RoI Pooling
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5.5), facecolor='white')

# (A) Visual Task Taxonomy
ax1.set_title("(A) Taxonomy of Computer Vision Recognition Tasks", fontsize=11, fontweight='bold', pad=10)

tasks = [
    ("Classification", "Single label for full image\n(e.g., 'Dog')", "#bae6fd", "#0284c7", 0.5),
    ("Classification + Localization", "Single label + 1 bounding box\n(e.g., 'Dog' at [x, y, w, h])", "#fed7aa", "#ea580c", 2.0),
    ("Object Detection", "Multiple classes + multiple boxes\n(e.g., 'Dog', 'Cat', 'Duck')", "#fef08a", "#ca8a04", 3.5),
    ("Instance Segmentation", "Pixel-level semantic mask for\nevery distinct object instance", "#bbf7d0", "#16a34a", 5.0)
]

for title, desc, bg, border, x in tasks:
    ax1.add_patch(FancyBboxPatch((x-0.65, 1.8), 1.3, 1.8, boxstyle="round,pad=0.08", facecolor=bg, edgecolor=border, lw=1.5))
    ax1.text(x, 3.2, title, ha='center', va='center', fontsize=8.5, fontweight='bold')
    ax1.text(x, 2.3, desc, ha='center', va='center', fontsize=7.5, color='#1e293b', linespacing=1.2)
    if x < 5.0:
        ax1.annotate("", xy=(x + 0.95, 2.7), xytext=(x + 0.65, 2.7), arrowprops=dict(arrowstyle="->", color='#64748b', lw=1.5))

ax1.set_xlim(-0.3, 5.9)
ax1.set_ylim(1.0, 4.2)
ax1.axis('off')

# (B) RoI Pooling in Fast R-CNN
ax2.set_title("(B) Region of Interest (RoI) Pooling Mechanism", fontsize=11, fontweight='bold', pad=10)

# Irregular RoI proposal on feature map
ax2.add_patch(Rectangle((0.5, 1.5), 2.4, 2.0, facecolor='#fed7aa', edgecolor='#ea580c', lw=1.5))
ax2.text(1.7, 3.7, "Arbitrary Sized Proposal (h x w)\ne.g., 5 x 7 on Conv Feature Map", ha='center', fontsize=8.5, fontweight='bold', color='#c2410c')

# 2x2 grid subdivisions on irregular RoI
ax2.plot([1.7, 1.7], [1.5, 3.5], color='#c2410c', linestyle='--')
ax2.plot([0.5, 2.9], [2.5, 2.5], color='#c2410c', linestyle='--')
ax2.text(1.1, 3.0, "Sec 1", ha='center', va='center', fontsize=8)
ax2.text(2.3, 3.0, "Sec 2", ha='center', va='center', fontsize=8)
ax2.text(1.1, 2.0, "Sec 3", ha='center', va='center', fontsize=8)
ax2.text(2.3, 2.0, "Sec 4", ha='center', va='center', fontsize=8)

# Arrow to fixed output
ax2.annotate("", xy=(4.0, 2.5), xytext=(3.1, 2.5), arrowprops=dict(arrowstyle="->", color='#0284c7', lw=2))
ax2.text(3.55, 2.8, "Max Pool\nper section", ha='center', fontsize=8, fontweight='bold', color='#0284c7')

# Fixed size output grid (e.g., 2x2 for illustration, standard 7x7)
ax2.add_patch(Rectangle((4.2, 1.7), 1.6, 1.6, facecolor='#bbf7d0', edgecolor='#16a34a', lw=1.5))
ax2.plot([5.0, 5.0], [1.7, 3.3], color='#16a34a', lw=1.5)
ax2.plot([4.2, 5.8], [2.5, 2.5], color='#16a34a', lw=1.5)
ax2.text(5.0, 3.6, "Fixed Size Output (H x W)\n(e.g., 7x7xDepth for FC Layers)", ha='center', fontsize=8.5, fontweight='bold', color='#166534')

ax2.text(3.2, 0.7, "RoI Pooling divides any variable proposed region into\nH x W equal sections and max-pools each section,\nyielding identical vector sizes for fully connected layers.",
         ha='center', fontsize=8.5, fontweight='bold', bbox=dict(boxstyle='round,pad=0.5', facecolor='#f8fafc', edgecolor='#cbd5e1'))

ax2.set_xlim(0, 6.4)
ax2.set_ylim(0.3, 4.4)
ax2.axis('off')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "fig07_object_detection_taxonomy_and_roi_pooling.png"), dpi=180, facecolor='white')
plt.close()
print("Saved fig07_object_detection_taxonomy_and_roi_pooling.png")

# -------------------------------------------------------------
# FIGURE 8: Evolution from R-CNN to Faster R-CNN and YOLO
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(15, 6), facecolor='white')
ax.set_title("Evolution of Object Detection Frameworks (Two-Stage to Single-Stage)", fontsize=12, fontweight='bold', pad=15)

detectors = [
    ("R-CNN (2014)", "Girshick et al.",
     "• Selective Search (~2000 proposals)\n• Warp each proposal to 227x227\n• 2000 independent CNN passes!\n• SVM class + BBox Regressor\n• Inference: ~47 sec / image (Glacial!)",
     "#fee2e2", "#dc2626", 1.2),
    ("Fast R-CNN (2015)", "Girshick",
     "• 1 CNN forward pass on full image\n• Project Selective Search to features\n• RoI Pooling for fixed 7x7 maps\n• Multi-task loss (CrossEntropy + Smooth L1)\n• Inference: ~2 sec / image (25x speedup)",
     "#fed7aa", "#ea580c", 4.3),
    ("Faster R-CNN (2015)", "Ren, He, Girshick, Sun",
     "• In-network Region Proposal Net (RPN)\n• Predefined Anchor Boxes (9 scales/ratios)\n• Eliminates Selective Search entirely!\n• Fully end-to-end differentiable\n• Inference: ~0.2 sec / image (Real-time)",
     "#fef08a", "#ca8a04", 7.4),
    ("YOLO (2016)", "Redmon et al.",
     "• SINGLE-STAGE DETECTOR\n• Reframe detection as direct regression\n• Divides image into S x S grid\n• Predicts boxes + class probs simultaneously\n• Inference: 45 - 155 FPS (Ultra-fast!)",
     "#bbf7d0", "#16a34a", 10.5)
]

for name, author, desc, bg, border, x in detectors:
    ax.add_patch(FancyBboxPatch((x-1.35, 1.0), 2.7, 3.8, boxstyle="round,pad=0.1", facecolor=bg, edgecolor=border, lw=2))
    ax.text(x, 4.4, name, ha='center', va='center', fontsize=10, fontweight='bold', color='#0f172a')
    ax.text(x, 4.05, author, ha='center', va='center', fontsize=8, color='#475569', style='italic')
    ax.text(x, 2.5, desc, ha='center', va='center', fontsize=8, color='#1e293b', linespacing=1.35)
    if x < 10.0:
        ax.annotate("", xy=(x + 1.6, 2.8), xytext=(x + 1.35, 2.8), arrowprops=dict(arrowstyle="->", color='#475569', lw=2))

ax.set_xlim(-0.3, 12.2)
ax.set_ylim(0.5, 5.2)
ax.axis('off')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "fig08_rcnn_evolution_to_yolo.png"), dpi=180, facecolor='white')
plt.close()
print("Saved fig08_rcnn_evolution_to_yolo.png")

print("All 8 Week 5 figures successfully generated!")
