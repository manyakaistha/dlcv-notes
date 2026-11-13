import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image, ImageFilter

# Professional Academic Styling optimized for readability in Obsidian / Markdown notes
sns.set_theme(style="white", palette="deep")
plt.rcParams["figure.dpi"] = 180
plt.rcParams["savefig.dpi"] = 180
plt.rcParams["savefig.bbox"] = "tight"
plt.rcParams["figure.facecolor"] = "white"
plt.rcParams["axes.facecolor"] = "white"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Helvetica Neue", "Arial"]
plt.rcParams["axes.edgecolor"] = "#222222"
plt.rcParams["axes.linewidth"] = 1.2
plt.rcParams["font.size"] = 12
plt.rcParams["axes.titlesize"] = 14
plt.rcParams["axes.titleweight"] = "bold"
plt.rcParams["axes.labelsize"] = 13
plt.rcParams["axes.labelweight"] = "bold"
plt.rcParams["xtick.labelsize"] = 11
plt.rcParams["ytick.labelsize"] = 11
plt.rcParams["legend.fontsize"] = 11

OUT_DIR = "/Volumes/1700 APFS/PERSONAL_PROGRAMMING_PROJECTS/Notes/Deep Learning for Computer Vision/month 1/week 1/assets"
os.makedirs(OUT_DIR, exist_ok=True)
np.random.seed(42)

def conv2d_numpy(image, kernel):
    """Zero-padded 2D convolution using numpy"""
    ih, iw = image.shape
    kh, kw = kernel.shape
    pad_h, pad_w = kh // 2, kw // 2
    padded = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant')
    out = np.zeros_like(image, dtype=float)
    k_flipped = np.flip(np.flip(kernel, 0), 1)
    for y in range(ih):
        for x in range(iw):
            patch = padded[y:y+kh, x:x+kw]
            out[y, x] = np.sum(patch * k_flipped)
    return out

def median2d_numpy(image, size=3):
    """2D median filter using numpy"""
    ih, iw = image.shape
    pad = size // 2
    padded = np.pad(image, pad, mode='edge')
    out = np.zeros_like(image, dtype=float)
    for y in range(ih):
        for x in range(iw):
            patch = padded[y:y+size, x:x+size]
            out[y, x] = np.median(patch)
    return out

# -------------------------------------------------------------------------
# Figure 1: Perceptual Illusions & Computational Bottlenecks
# -------------------------------------------------------------------------
def fig01_illusions_and_challenges():
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))
    
    # 1. Muller-Lyer Illusion
    ax = axes[0]
    ax.set_title("Müller-Lyer Illusion\n(3D Depth Prior Inversion)", fontsize=14, fontweight="bold", pad=12)
    # Top line with outward fins (appears shorter)
    ax.plot([0.2, 0.8], [0.7, 0.7], 'k-', lw=4)
    ax.plot([0.2, 0.08], [0.7, 0.82], 'k-', lw=4)
    ax.plot([0.2, 0.08], [0.7, 0.58], 'k-', lw=4)
    ax.plot([0.8, 0.92], [0.7, 0.82], 'k-', lw=4)
    ax.plot([0.8, 0.92], [0.7, 0.58], 'k-', lw=4)
    ax.text(0.5, 0.76, "Identical Length L = 0.6\n(Perceived as Shorter / Closer Convex)", 
            ha="center", fontsize=11, color="navy", fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", fc="#eef3ff", ec="navy", lw=1))
    
    # Bottom line with inward fins (appears longer)
    ax.plot([0.2, 0.8], [0.28, 0.28], 'k-', lw=4)
    ax.plot([0.2, 0.32], [0.28, 0.40], 'k-', lw=4)
    ax.plot([0.2, 0.32], [0.28, 0.16], 'k-', lw=4)
    ax.plot([0.8, 0.68], [0.28, 0.40], 'k-', lw=4)
    ax.plot([0.8, 0.68], [0.28, 0.16], 'k-', lw=4)
    ax.text(0.5, 0.16, "Identical Length L = 0.6\n(Perceived as Longer / Distant Concave)", 
            ha="center", fontsize=11, color="darkred", fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", fc="#ffeeee", ec="darkred", lw=1))
    
    ax.axvline(0.2, color="gray", linestyle="--", alpha=0.7, lw=1.5)
    ax.axvline(0.8, color="gray", linestyle="--", alpha=0.7, lw=1.5)
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(0.06, 0.96)
    ax.axis("off")
    
    # 2. Adelson's Checkerboard Shadow
    ax = axes[1]
    ax.set_title("Adelson's Checkerboard Shadow\n(Illumination Discounting $I = R \\cdot L$)", 
                 fontsize=14, fontweight="bold", pad=12)
    checker = np.zeros((6, 6))
    for r in range(6):
        for c in range(6):
            checker[r, c] = 108 if (r + c) % 2 == 1 else 200
    yy, xx = np.mgrid[0:6, 0:6]
    shadow = np.clip(1.0 - 0.14 * (xx + yy - 3), 0.48, 1.0)
    img_shadowed = checker * shadow
    val_A = 108.0
    img_shadowed[1, 2] = val_A # force exact match
    img_shadowed[4, 3] = val_A
    
    ax.imshow(img_shadowed, cmap="gray", vmin=0, vmax=255)
    ax.plot(2, 1, 's', markersize=20, fillstyle='none', markeredgecolor="yellow", markeredgewidth=3.5)
    ax.text(2, 0.4, f"Tile A: I = {int(val_A)}\n(Direct Light)", color="yellow", ha="center", fontsize=11, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.2", fc="black", ec="yellow", lw=1.5))
    ax.plot(3, 4, 's', markersize=20, fillstyle='none', markeredgecolor="cyan", markeredgewidth=3.5)
    ax.text(3, 4.8, f"Tile B: I = {int(val_A)}\n(In Shadow)", color="cyan", ha="center", fontsize=11, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.2", fc="black", ec="cyan", lw=1.5))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("Identical Physical Pixel Irradiance (I = 108)\nDivergent Perceived Reflectance", 
                  fontsize=12, fontweight="bold", labelpad=8)
    
    # 3. Visual Search: Pop-Out vs Conjunction
    ax = axes[2]
    ax.set_title("Visual Search Reaction Scaling\n(Feature Integration Theory)", fontsize=14, fontweight="bold", pad=12)
    set_sizes = np.array([4, 8, 16, 32, 64])
    rt_popout = 400 + 0.3 * set_sizes + np.random.normal(0, 3, len(set_sizes))
    rt_conjunction = 400 + 26.0 * set_sizes + np.random.normal(0, 10, len(set_sizes))
    
    ax.plot(set_sizes, rt_popout, 'o-', color="#2ca02c", lw=3.2, markersize=8, label=r"Pop-out: Color ($\mathcal{O}(1)$)")
    ax.plot(set_sizes, rt_conjunction, 's--', color="#d62728", lw=3.2, markersize=8, label=r"Conjunction: Color+Shape ($\mathcal{O}(N)$)")
    ax.set_xlabel("Distractor Set Size ($N$ items)", fontsize=12, fontweight="bold")
    ax.set_ylabel("Reaction Time (ms)", fontsize=12, fontweight="bold")
    ax.legend(frameon=True, fontsize=11, loc="upper left", framealpha=0.9, edgecolor="gray")
    ax.grid(True, linestyle=":", alpha=0.6)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig01_perceptual_illusions_and_cv_bottlenecks.png"), 
                dpi=180, facecolor="white")
    plt.close()

# -------------------------------------------------------------------------
# Figure 2: Image Representations & Point Operations
# -------------------------------------------------------------------------
def fig02_point_ops_and_averaging():
    fig = plt.figure(figsize=(16, 5.5))
    gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 1.2])
    
    # 1. 3D Surface representation of image f(x, y)
    ax0 = fig.add_subplot(gs[0], projection='3d')
    x = np.linspace(-3, 3, 32)
    y = np.linspace(-3, 3, 32)
    X, Y = np.meshgrid(x, y)
    Z = np.exp(-(X**2 + Y**2)/3.5) * 200 + 25
    surf = ax0.plot_surface(X, Y, Z, cmap="viridis", edgecolor='none', alpha=0.9)
    ax0.set_title(r"Continuous Surface $z = f(x, y)$", fontsize=13, fontweight="bold", pad=10)
    ax0.set_xlabel("x (col)", fontsize=11, labelpad=4)
    ax0.set_ylabel("y (row)", fontsize=11, labelpad=4)
    ax0.set_zlabel("Intensity $I$", fontsize=11, labelpad=4)
    ax0.view_init(elev=32, azim=225)
    
    # 2. Point Transfer Functions: Inversion & Stretching
    ax1 = fig.add_subplot(gs[1])
    ax1.set_title("Point Operations $s = T(r)$", fontsize=13, fontweight="bold", pad=10)
    r = np.linspace(0, 255, 256)
    identity = r
    inversion = 255 - r
    r_min, r_max = 50, 180
    stretching = np.clip((r - r_min) * (255.0 / (r_max - r_min)), 0, 255)
    
    ax1.plot(r, identity, 'k--', lw=2, label="Identity: $s = r$")
    ax1.plot(r, inversion, 'crimson', lw=3, label="Negative: $s = 255 - r$")
    ax1.plot(r, stretching, 'royalblue', lw=3, label=f"Stretch: $[{r_min},{r_max}] \\to [0, 255]$")
    ax1.set_xlabel("Input Intensity $r \\in [0, 255]$", fontsize=12, fontweight="bold")
    ax1.set_ylabel("Output Intensity $s \\in [0, 255]$", fontsize=12, fontweight="bold")
    ax1.legend(frameon=True, fontsize=11, loc="center left", framealpha=0.9, edgecolor="gray")
    ax1.grid(True, linestyle=":", alpha=0.6)
    
    # 3. Multi-Image Averaging Noise Reduction
    ax2 = fig.add_subplot(gs[2])
    ax2.set_title(r"Noise Reduction via Averaging ($\sigma / \sqrt{N}$)", fontsize=13, fontweight="bold", pad=10)
    true_intensity = 128
    sigma_noise = 40
    frame_counts = [1, 4, 16, 64]
    x_vals = np.linspace(true_intensity - 3.2*sigma_noise, true_intensity + 3.2*sigma_noise, 400)
    colors = ["#d62728", "#ff7f0e", "#1f77b4", "#2ca02c"]
    for N, col in zip(frame_counts, colors):
        sigma_N = sigma_noise / np.sqrt(N)
        pdf = (1.0 / (sigma_N * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_vals - true_intensity)/sigma_N)**2)
        ax2.plot(x_vals, pdf, label=f"$N={N}$ frames ($\\sigma={sigma_N:.1f}$)", color=col, lw=2.8)
        
    ax2.axvline(true_intensity, color="black", linestyle=":", alpha=0.8, lw=2)
    ax2.set_xlabel("Sampled Pixel Value (Ground Truth = 128)", fontsize=12, fontweight="bold")
    ax2.set_ylabel("Probability Density $p(I)$", fontsize=12, fontweight="bold")
    ax2.legend(frameon=True, fontsize=11, loc="upper right", framealpha=0.9, edgecolor="gray")
    ax2.grid(True, linestyle=":", alpha=0.6)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig02_image_representations_point_ops.png"), 
                dpi=180, facecolor="white")
    plt.close()

# -------------------------------------------------------------------------
# Figure 3: Histogram Equalization Derivation & Dynamics
# -------------------------------------------------------------------------
def fig03_histogram_equalization():
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    np.random.seed(101)
    low_contrast_data = np.clip(np.random.normal(loc=75, scale=20, size=30000), 0, 255).astype(np.uint8)
    
    # 1. Original Histogram
    counts, _ = np.histogram(low_contrast_data, bins=256, range=[0, 256], density=True)
    axes[0, 0].set_title("1. Input Histogram $p_r(r_k)$ (Low Dynamic Range)", fontsize=13, fontweight="bold")
    axes[0, 0].bar(np.arange(256), counts, color="#4c72b0", width=1.0)
    axes[0, 0].set_xlim(0, 255)
    axes[0, 0].set_xlabel("Input Gray Level $r_k$", fontsize=12, fontweight="bold")
    axes[0, 0].set_ylabel("Probability $p_r(r_k)$", fontsize=12, fontweight="bold")
    axes[0, 0].grid(True, linestyle=":", alpha=0.5)
    
    # 2. Cumulative Distribution Function (CDF) Transfer Function
    cdf = counts.cumsum()
    cdf_normalized = cdf / cdf[-1]
    T_map = np.floor(255 * cdf_normalized).astype(np.uint8)
    
    axes[0, 1].set_title(r"2. CDF Transfer $s_k = (L-1)\sum_{j=0}^k p_r(r_j)$", fontsize=13, fontweight="bold")
    axes[0, 1].plot(np.arange(256), T_map, color="#c44e52", lw=3.2, label="CDF Mapping $T(r)$")
    axes[0, 1].plot([0, 255], [0, 255], 'k--', alpha=0.6, lw=1.8, label="Linear Reference")
    axes[0, 1].set_xlim(0, 255)
    axes[0, 1].set_ylim(0, 255)
    axes[0, 1].set_xlabel("Input Gray Level $r_k$", fontsize=12, fontweight="bold")
    axes[0, 1].set_ylabel("Transformed Gray Level $s_k$", fontsize=12, fontweight="bold")
    axes[0, 1].legend(frameon=True, fontsize=11, loc="lower right", framealpha=0.9, edgecolor="gray")
    axes[0, 1].grid(True, linestyle=":", alpha=0.5)
    
    # 3. Equalized Data & Histogram
    equalized_data = T_map[low_contrast_data]
    eq_counts, _ = np.histogram(equalized_data, bins=256, range=[0, 256], density=True)
    
    axes[1, 0].set_title("3. Equalized Histogram $p_s(s_k)$ (Full Dynamic Span)", fontsize=13, fontweight="bold")
    axes[1, 0].bar(np.arange(256), eq_counts, color="#55a868", width=1.0)
    axes[1, 0].set_xlim(0, 255)
    axes[1, 0].set_xlabel("Equalized Gray Level $s \\in [0, 255]$", fontsize=12, fontweight="bold")
    axes[1, 0].set_ylabel("Probability $p_s(s_k)$", fontsize=12, fontweight="bold")
    axes[1, 0].grid(True, linestyle=":", alpha=0.5)
    
    # 4. Cumulative Distribution of Equalized Data
    eq_cdf = eq_counts.cumsum()
    axes[1, 1].set_title("4. Linearized Cumulative Distribution $\\sum p_s(s)$", fontsize=13, fontweight="bold")
    axes[1, 1].plot(np.arange(256), eq_cdf, color="#8172b3", lw=3.2, label="Empirical Uniform CDF")
    axes[1, 1].plot([0, 255], [0, 1.0], 'k--', lw=1.8, alpha=0.7, label="Ideal Uniform Linearity")
    axes[1, 1].set_xlim(0, 255)
    axes[1, 1].set_ylim(0, 1.05)
    axes[1, 1].set_xlabel("Equalized Gray Level $s$", fontsize=12, fontweight="bold")
    axes[1, 1].set_ylabel("Cumulative Sum", fontsize=12, fontweight="bold")
    axes[1, 1].legend(frameon=True, fontsize=11, loc="lower right", framealpha=0.9, edgecolor="gray")
    axes[1, 1].grid(True, linestyle=":", alpha=0.5)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig03_histogram_equalization_derivation.png"), 
                dpi=180, facecolor="white")
    plt.close()

# -------------------------------------------------------------------------
# Figure 4: Spatial Convolution Mechanics & Directional Gradients (2x2 Grid)
# -------------------------------------------------------------------------
def fig04_convolution_mechanics_and_padding():
    fig, axes = plt.subplots(2, 2, figsize=(11, 9.5))
    img = np.zeros((48, 48))
    img[12:36, 12:36] = 200
    
    # Sobel kernels
    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=float)
    sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=float)
    
    # 1. Input image
    axes[0, 0].set_title("1. Input Image $\\mathbf{I}$ (Box Step)", fontsize=13, fontweight="bold")
    im0 = axes[0, 0].imshow(img, cmap="gray", vmin=0, vmax=255)
    axes[0, 0].set_xticks([])
    axes[0, 0].set_yticks([])
    plt.colorbar(im0, ax=axes[0, 0], fraction=0.046, pad=0.04)
    
    # 2. Horizontal gradient
    gx = conv2d_numpy(img, sobel_x)
    axes[0, 1].set_title("2. Horizontal Gradient $\\partial \\mathbf{I} / \\partial x$", fontsize=13, fontweight="bold")
    im1 = axes[0, 1].imshow(gx, cmap="coolwarm", vmin=-400, vmax=400)
    axes[0, 1].set_xticks([])
    axes[0, 1].set_yticks([])
    cbar1 = plt.colorbar(im1, ax=axes[0, 1], fraction=0.046, pad=0.04)
    cbar1.ax.tick_params(labelsize=10)
    
    # 3. Vertical gradient
    gy = conv2d_numpy(img, sobel_y)
    axes[1, 0].set_title("3. Vertical Gradient $\\partial \\mathbf{I} / \\partial y$", fontsize=13, fontweight="bold")
    im2 = axes[1, 0].imshow(gy, cmap="coolwarm", vmin=-400, vmax=400)
    axes[1, 0].set_xticks([])
    axes[1, 0].set_yticks([])
    cbar2 = plt.colorbar(im2, ax=axes[1, 0], fraction=0.046, pad=0.04)
    cbar2.ax.tick_params(labelsize=10)
    
    # 4. Gradient magnitude
    g_mag = np.sqrt(gx**2 + gy**2)
    axes[1, 1].set_title(r"4. Gradient Magnitude $\|\nabla \mathbf{I}\| = \sqrt{I_x^2 + I_y^2}$", fontsize=13, fontweight="bold")
    im3 = axes[1, 1].imshow(g_mag, cmap="magma")
    axes[1, 1].set_xticks([])
    axes[1, 1].set_yticks([])
    cbar3 = plt.colorbar(im3, ax=axes[1, 1], fraction=0.046, pad=0.04)
    cbar3.ax.tick_params(labelsize=10)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig04_spatial_convolution_vs_correlation.png"), 
                dpi=180, facecolor="white")
    plt.close()

# -------------------------------------------------------------------------
# Figure 5: Kernel Separability & SVD Rank-1 Decomposition
# -------------------------------------------------------------------------
def fig05_separability_and_svd():
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))
    
    # 1. 2D Gaussian Kernel (5x5)
    k_size = 5
    sigma = 1.0
    ax_coord = np.arange(-k_size//2 + 1., k_size//2 + 1.)
    xx, yy = np.meshgrid(ax_coord, ax_coord)
    kernel_2d = np.exp(-(xx**2 + yy**2) / (2. * sigma**2))
    kernel_2d /= kernel_2d.sum()
    
    sns.heatmap(kernel_2d, annot=True, fmt=".3f", cmap="Blues", cbar=False, ax=axes[0],
                annot_kws={"size": 12, "weight": "bold"})
    axes[0].set_title("2D Gaussian Kernel $\\mathbf{K}$ (5×5)", fontsize=13, fontweight="bold", pad=10)
    axes[0].set_xticks([])
    axes[0].set_yticks([])
    
    # 2. SVD decomposition singular values
    U, S, Vt = np.linalg.svd(kernel_2d)
    axes[1].set_title("SVD Singular Value Spectrum $\\sigma_i$", fontsize=13, fontweight="bold", pad=10)
    axes[1].stem(np.arange(1, len(S)+1), S, linefmt="b-", markerfmt="bo", basefmt="k-")
    axes[1].text(1, S[0]*1.06, f"$\\sigma_1 = {S[0]:.4f}$\n(Rank = 1)", ha="center", fontsize=12, color="navy", fontweight="bold",
                 bbox=dict(boxstyle="round,pad=0.2", fc="#eef3ff", ec="navy", lw=1))
    for i in range(1, len(S)):
        axes[1].text(i+1, S[i]+0.04, f"$\\sigma_{i+1} \\approx 0$", ha="center", fontsize=10, color="gray")
    axes[1].set_ylim(-0.05, 1.25)
    axes[1].set_xlabel("Singular Value Index $i$", fontsize=12, fontweight="bold")
    axes[1].set_ylabel("Singular Value $\\sigma_i$", fontsize=12, fontweight="bold")
    axes[1].grid(True, linestyle=":", alpha=0.5)
    
    # 3. Computational Scaling: k^2 vs 2k operations
    k_vals = np.arange(3, 33, 2)
    ops_2d = k_vals ** 2
    ops_separable = 2 * k_vals
    speedup = ops_2d / ops_separable
    
    ax_scale = axes[2]
    ax_scale.set_title(r"Complexity: $\mathcal{O}(k^2)$ vs $\mathcal{O}(2k)$", fontsize=13, fontweight="bold", pad=10)
    ax_scale.plot(k_vals, ops_2d, 'r-o', lw=3.0, markersize=7, label="2D Standard: $k^2$ ops/pixel")
    ax_scale.plot(k_vals, ops_separable, 'g-s', lw=3.0, markersize=7, label="Separable: $2k$ ops/pixel")
    ax_scale.set_xlabel("Kernel Size $k$ (pixels)", fontsize=12, fontweight="bold")
    ax_scale.set_ylabel("Multiplications per Pixel", fontsize=12, fontweight="bold")
    ax_scale.legend(frameon=True, fontsize=11, loc="upper left", framealpha=0.9, edgecolor="gray")
    ax_scale.grid(True, linestyle=":", alpha=0.5)
    
    ax_twin = ax_scale.twinx()
    ax_twin.plot(k_vals, speedup, 'b--', lw=2.2, alpha=0.8)
    ax_twin.set_ylabel("Speedup Factor ($k / 2$)", color="navy", fontsize=12, fontweight="bold")
    ax_twin.tick_params(axis='y', labelcolor='navy')
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig05_kernel_separability_and_svd.png"), 
                dpi=180, facecolor="white")
    plt.close()

# -------------------------------------------------------------------------
# Figure 6: Template Matching & NCC vs Raw Correlation
# -------------------------------------------------------------------------
def fig06_ncc_template_matching():
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))
    h, w = 80, 120
    scene = np.zeros((h, w))
    tx, ty = 25, 30
    tw, th = 16, 16
    template = np.zeros((th, tw))
    template[3:13, 6:10] = 180
    template[3:6, 3:13] = 180
    scene[ty:ty+th, tx:tx+tw] = template
    
    # Heavy illumination ramp
    ramp = np.linspace(20, 220, w)
    scene_lit = scene + ramp[np.newaxis, :]
    
    axes[0].set_title("1. Scene with Illumination Ramp", fontsize=13, fontweight="bold", pad=10)
    axes[0].imshow(scene_lit, cmap="gray")
    rect = plt.Rectangle((tx, ty), tw, th, edgecolor='red', facecolor='none', lw=3)
    axes[0].add_patch(rect)
    axes[0].text(tx, ty-5, "Target Template", color="red", fontsize=11, fontweight="bold",
                 bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="red", lw=1.2))
    axes[0].set_xticks([])
    axes[0].set_yticks([])
    
    # Raw correlation
    raw_corr = np.zeros((h - th + 1, w - tw + 1))
    for y in range(h - th + 1):
        for x in range(w - tw + 1):
            patch = scene_lit[y:y+th, x:x+tw]
            raw_corr[y, x] = np.sum(patch * template)
            
    axes[1].set_title("2. Raw Correlation\n(False Peak at Bright Margin)", fontsize=13, fontweight="bold", pad=10)
    im1 = axes[1].imshow(raw_corr, cmap="inferno")
    my, mx = np.unravel_index(np.argmax(raw_corr), raw_corr.shape)
    axes[1].plot(mx, my, 'gx', markersize=14, markeredgewidth=3.5)
    axes[1].text(mx - 15, my - 6, "False Peak", color="darkgreen", fontsize=11, fontweight="bold",
                 bbox=dict(boxstyle="round,pad=0.2", fc="#d4ffd4", ec="green", lw=1.2))
    axes[1].set_xticks([])
    axes[1].set_yticks([])
    plt.colorbar(im1, ax=axes[1], fraction=0.046, pad=0.04)
    
    # NCC
    t_zero = template - template.mean()
    ncc = np.zeros((h - th + 1, w - tw + 1))
    t_norm = np.linalg.norm(t_zero)
    for y in range(h - th + 1):
        for x in range(w - tw + 1):
            patch = scene_lit[y:y+th, x:x+tw]
            p_zero = patch - patch.mean()
            p_norm = np.linalg.norm(p_zero)
            if p_norm > 1e-5 and t_norm > 1e-5:
                ncc[y, x] = np.sum(t_zero * p_zero) / (t_norm * p_norm)
                
    axes[2].set_title("3. Normalized Cross-Correlation (NCC)\n(Peak Exact at Ground Truth)", fontsize=13, fontweight="bold", pad=10)
    im2 = axes[2].imshow(ncc, cmap="viridis", vmin=-0.2, vmax=1.0)
    nmy, nmx = np.unravel_index(np.argmax(ncc), ncc.shape)
    axes[2].plot(nmx, nmy, 'ro', markersize=12, fillstyle='none', markeredgewidth=3.5)
    axes[2].text(nmx, nmy - 6, f"True Target\nNCC={ncc[nmy, nmx]:.2f}", color="darkred", fontsize=11, fontweight="bold",
                 bbox=dict(boxstyle="round,pad=0.2", fc="#ffefef", ec="red", lw=1.2))
    axes[2].set_xticks([])
    axes[2].set_yticks([])
    plt.colorbar(im2, ax=axes[2], fraction=0.046, pad=0.04)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig06_template_matching_and_ncc.png"), 
                dpi=180, facecolor="white")
    plt.close()

# -------------------------------------------------------------------------
# Figure 7: Non-Linear Filters & Noise Removal (2x2 Grid)
# -------------------------------------------------------------------------
def fig07_nonlinear_filters():
    fig, axes = plt.subplots(2, 2, figsize=(11, 9.5))
    clean = np.zeros((48, 48))
    clean[:, 24:] = 200
    
    noisy = clean.copy()
    sp_prob = 0.15
    rnd = np.random.rand(*clean.shape)
    noisy[rnd < (sp_prob / 2)] = 0
    noisy[(rnd >= (sp_prob / 2)) & (rnd < sp_prob)] = 255
    
    # 1. Salt and Pepper
    axes[0, 0].set_title("1. Salt-and-Pepper Impulse Noise (15%)", fontsize=13, fontweight="bold")
    axes[0, 0].imshow(noisy, cmap="gray", vmin=0, vmax=255)
    axes[0, 0].set_xticks([])
    axes[0, 0].set_yticks([])
    
    # 2. Gaussian filter
    pil_noisy = Image.fromarray(noisy.astype(np.uint8))
    pil_gauss = pil_noisy.filter(ImageFilter.GaussianBlur(radius=1.8))
    gauss_res = np.array(pil_gauss)
    
    axes[0, 1].set_title("2. Gaussian (Linear Blurs Spikes & Edge)", fontsize=13, fontweight="bold")
    axes[0, 1].imshow(gauss_res, cmap="gray", vmin=0, vmax=255)
    axes[0, 1].set_xticks([])
    axes[0, 1].set_yticks([])
    
    # 3. Median filter
    med_res = median2d_numpy(noisy, size=3)
    axes[1, 0].set_title("3. Median (Non-Linear Sharp Edge Preserved)", fontsize=13, fontweight="bold")
    axes[1, 0].imshow(med_res, cmap="gray", vmin=0, vmax=255)
    axes[1, 0].set_xticks([])
    axes[1, 0].set_yticks([])
    
    # 4. Bilateral weighting concept
    ax_bf = axes[1, 1]
    ax_bf.set_title("4. Bilateral Weighting Mechanisms", fontsize=13, fontweight="bold")
    dist = np.linspace(-4, 4, 100)
    spatial_w = np.exp(-dist**2 / (2 * 1.5**2))
    range_w = np.exp(-(dist*2.2)**2 / 2)
    
    ax_bf.plot(dist, spatial_w, 'b-', lw=3.0, label=r"Spatial $g_{\sigma_s}(\|p-q\|)$")
    ax_bf.plot(dist, range_w, 'r--', lw=3.0, label=r"Range $g_{\sigma_r}(|I_p - I_q|)$")
    ax_bf.set_xlabel("Relative Spatial / Radiometric Distance", fontsize=12, fontweight="bold")
    ax_bf.set_ylabel("Kernel Weight $W$", fontsize=12, fontweight="bold")
    ax_bf.legend(frameon=True, fontsize=11, loc="upper right", framealpha=0.9, edgecolor="gray")
    ax_bf.grid(True, linestyle=":", alpha=0.5)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig07_nonlinear_filters_noise_removal.png"), 
                dpi=180, facecolor="white")
    plt.close()

# -------------------------------------------------------------------------
# Figure 8: Fourier Spectrum & Oppenheim Phase-Swap Duality (2x4)
# -------------------------------------------------------------------------
def fig08_fourier_analysis_and_swap():
    fig, axes = plt.subplots(2, 4, figsize=(16, 8.5))
    
    # Image 1: Cross / Rectangles
    img1 = np.zeros((128, 128))
    img1[30:98, 48:80] = 255
    img1[48:80, 20:108] = 255
    
    # Image 2: Concentric Sinusoids
    y, x = np.mgrid[-64:64, -64:64]
    r = np.sqrt(x**2 + y**2)
    img2 = np.clip(128 + 127 * np.cos(r / 4.0), 0, 255)
    
    F1 = np.fft.fftshift(np.fft.fft2(img1))
    mag1 = np.abs(F1)
    phase1 = np.angle(F1)
    
    F2 = np.fft.fftshift(np.fft.fft2(img2))
    mag2 = np.abs(F2)
    phase2 = np.angle(F2)
    
    # Row 1
    axes[0, 0].set_title("1. Image A (Cross)", fontsize=13, fontweight="bold")
    axes[0, 0].imshow(img1, cmap="gray")
    axes[0, 0].axis("off")
    
    axes[0, 1].set_title(r"2. Mag A: $\log(1+|F_A|)$", fontsize=13, fontweight="bold")
    axes[0, 1].imshow(np.log1p(mag1), cmap="magma")
    axes[0, 1].axis("off")
    
    axes[0, 2].set_title("3. Image B (Rings)", fontsize=13, fontweight="bold")
    axes[0, 2].imshow(img2, cmap="gray")
    axes[0, 2].axis("off")
    
    axes[0, 3].set_title(r"4. Mag B: $\log(1+|F_B|)$", fontsize=13, fontweight="bold")
    axes[0, 3].imshow(np.log1p(mag2), cmap="magma")
    axes[0, 3].axis("off")
    
    # Reconstructions with swapped phase
    F_synth1 = mag2 * np.exp(1j * phase1)
    recon1 = np.real(np.fft.ifft2(np.fft.ifftshift(F_synth1)))
    
    F_synth2 = mag1 * np.exp(1j * phase2)
    recon2 = np.real(np.fft.ifft2(np.fft.ifftshift(F_synth2)))
    
    # Row 2
    axes[1, 0].set_title(r"5. Phase A: $\angle F_A$", fontsize=13, fontweight="bold")
    axes[1, 0].imshow(phase1, cmap="twilight")
    axes[1, 0].axis("off")
    
    axes[1, 1].set_title("6. Mag B + Phase A\n(Shape of A Preserved!)", fontsize=13, fontweight="bold", color="darkred")
    axes[1, 1].imshow(recon1, cmap="gray")
    axes[1, 1].axis("off")
    
    axes[1, 2].set_title(r"7. Phase B: $\angle F_B$", fontsize=13, fontweight="bold")
    axes[1, 2].imshow(phase2, cmap="twilight")
    axes[1, 2].axis("off")
    
    axes[1, 3].set_title("8. Mag A + Phase B\n(Shape of B Preserved!)", fontsize=13, fontweight="bold", color="navy")
    axes[1, 3].imshow(recon2, cmap="gray")
    axes[1, 3].axis("off")
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig08_fourier_spectrum_magnitude_phase.png"), 
                dpi=180, facecolor="white")
    plt.close()

# -------------------------------------------------------------------------
# Figure 9: Convolution Theorem & Frequency Filtering (2x2 Grid)
# -------------------------------------------------------------------------
def fig09_frequency_filtering_and_convolution_theorem():
    fig, axes = plt.subplots(2, 2, figsize=(11, 9.5))
    base = np.zeros((128, 128))
    base[40:88, 40:88] = 180
    base[55:73, 55:73] = 60
    base += np.random.normal(0, 10, base.shape)
    base = np.clip(base, 0, 255)
    
    # 1. Spatial image
    axes[0, 0].set_title("1. Input Spatial Image $g(x, y)$", fontsize=13, fontweight="bold")
    axes[0, 0].imshow(base, cmap="gray")
    axes[0, 0].axis("off")
    
    # 2. Low-pass
    F = np.fft.fftshift(np.fft.fft2(base))
    u = np.linspace(-64, 64, 128)
    U, V = np.meshgrid(u, u)
    D = np.sqrt(U**2 + V**2)
    
    sigma_lp = 16.0
    H_lp = np.exp(- (D**2) / (2 * sigma_lp**2))
    G_lp = F * H_lp
    img_lp = np.real(np.fft.ifft2(np.fft.ifftshift(G_lp)))
    
    axes[0, 1].set_title("2. Low-Pass Filtered (Smoothed)\n$\\mathcal{F}^{-1}\\{\\mathcal{F}[g] \\cdot H_{LP}\\}$", 
                         fontsize=13, fontweight="bold")
    axes[0, 1].imshow(img_lp, cmap="gray")
    axes[0, 1].axis("off")
    
    # 3. High-pass
    H_hp = 1.0 - H_lp
    G_hp = F * H_hp
    img_hp = np.real(np.fft.ifft2(np.fft.ifftshift(G_hp)))
    
    axes[1, 0].set_title("3. High-Pass Filtered (Edges)\n$\\mathcal{F}^{-1}\\{\\mathcal{F}[g] \\cdot H_{HP}\\}$", 
                         fontsize=13, fontweight="bold")
    axes[1, 0].imshow(img_hp, cmap="gray")
    axes[1, 0].axis("off")
    
    # 4. Complexity curve
    ax_comp = axes[1, 1]
    ax_comp.set_title("4. FFT vs Spatial Complexity", fontsize=13, fontweight="bold")
    N = 512
    k_range = np.arange(3, 45, 2)
    spatial_cost = (N**2) * (k_range**2)
    fft_cost = np.full_like(k_range, 3 * (N**2) * 2 * np.log2(N) + (N**2))
    
    ax_comp.plot(k_range, spatial_cost / 1e6, 'r-o', lw=2.8, markersize=6, label=r"Spatial $\mathcal{O}(N^2 k^2)$")
    ax_comp.plot(k_range, fft_cost / 1e6, 'b--', lw=3.0, label=r"FFT Domain $\mathcal{O}(N^2 \log N)$")
    ax_comp.set_xlabel("Kernel Size $k$ (Image $512\\times512$)", fontsize=12, fontweight="bold")
    ax_comp.set_ylabel("FLOPs ($10^6$ operations)", fontsize=12, fontweight="bold")
    ax_comp.legend(frameon=True, fontsize=11, loc="upper left", framealpha=0.9, edgecolor="gray")
    ax_comp.grid(True, linestyle=":", alpha=0.5)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig09_convolution_theorem_and_frequency_filtering.png"), 
                dpi=180, facecolor="white")
    plt.close()

# -------------------------------------------------------------------------
# Figure 10: Sampling, Aliasing & Interpolation (2x3 Grid)
# -------------------------------------------------------------------------
def fig10_sampling_aliasing_interpolation():
    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    
    # 1. 1D Signal Sampling & Aliasing Demonstration
    ax1 = axes[0, 0]
    ax1.set_title("1. Nyquist: $f_s \\geq 2 f_{\\max}$", fontsize=13, fontweight="bold")
    t_cont = np.linspace(0, 1, 1000)
    f_sig = 4.0
    y_cont = np.sin(2 * np.pi * f_sig * t_cont)
    
    t_samp1 = np.linspace(0, 1, 17)
    y_samp1 = np.sin(2 * np.pi * f_sig * t_samp1)
    
    ax1.plot(t_cont, y_cont, 'k-', alpha=0.5, lw=1.8, label="True 4 Hz Signal")
    ax1.stem(t_samp1, y_samp1, linefmt="g-", markerfmt="go", basefmt="k-", label="Adequate $f_s = 16\\text{ Hz}$")
    ax1.set_xlabel("Time $t$ (s)", fontsize=12, fontweight="bold")
    ax1.set_ylabel("Amplitude", fontsize=12, fontweight="bold")
    ax1.legend(frameon=True, fontsize=10, loc="lower left", framealpha=0.9, edgecolor="gray")
    ax1.grid(True, linestyle=":", alpha=0.5)
    
    # 2. Sub-Nyquist Sampling
    ax2 = axes[0, 1]
    ax2.set_title("2. Sub-Nyquist: Aliasing Fold", fontsize=13, fontweight="bold")
    t_samp2 = np.linspace(0, 1, 6)
    y_samp2 = np.sin(2 * np.pi * f_sig * t_samp2)
    y_alias = np.sin(2 * np.pi * 1.0 * t_cont)
    
    ax2.plot(t_cont, y_cont, 'k--', alpha=0.4, lw=1.5, label="True 4 Hz Signal")
    ax2.plot(t_cont, -y_alias, 'r-', lw=2.8, label="Illusory Alias (1 Hz)")
    ax2.stem(t_samp2, y_samp2, linefmt="r-", markerfmt="ro", basefmt="k-", label="Undersampled $f_s = 5\\text{ Hz}$")
    ax2.set_xlabel("Time $t$ (s)", fontsize=12, fontweight="bold")
    ax2.legend(frameon=True, fontsize=10, loc="lower left", framealpha=0.9, edgecolor="gray")
    ax2.grid(True, linestyle=":", alpha=0.5)
    
    # 3. 2D Zone Plate
    x, y = np.mgrid[-2:2:256j, -2:2:256j]
    r_sq = x**2 + y**2
    zone_plate = 0.5 + 0.5 * np.cos(35.0 * r_sq)
    
    axes[0, 2].set_title("3. Continuous Chirp Zone Plate", fontsize=13, fontweight="bold")
    axes[0, 2].imshow(zone_plate, cmap="gray")
    axes[0, 2].axis("off")
    
    # 4. Decimation without anti-aliasing (Moiré)
    decimated_aliased = zone_plate[::4, ::4]
    axes[1, 0].set_title("4. Decimated 4× (NO Pre-filter)\nSevere False Moiré Rings", 
                         fontsize=13, fontweight="bold", color="darkred")
    axes[1, 0].imshow(decimated_aliased, cmap="gray")
    axes[1, 0].axis("off")
    
    # 5. Decimation with Gaussian anti-aliasing
    zp_pil = Image.fromarray((zone_plate * 255).astype(np.uint8))
    zp_filtered = np.array(zp_pil.filter(ImageFilter.GaussianBlur(radius=2.0))) / 255.0
    decimated_filtered = zp_filtered[::4, ::4]
    axes[1, 1].set_title("5. Decimated 4× (WITH Anti-Aliasing)\nClean Bandlimited Attenuation", 
                         fontsize=13, fontweight="bold", color="darkgreen")
    axes[1, 1].imshow(decimated_filtered, cmap="gray")
    axes[1, 1].axis("off")
    
    # 6. Interpolation comparison
    crop_small = (decimated_filtered[16:32, 16:32] * 255).astype(np.uint8)
    crop_pil = Image.fromarray(crop_small)
    nn_up = np.array(crop_pil.resize((64, 64), Image.NEAREST))
    bicubic_up = np.array(crop_pil.resize((64, 64), Image.BICUBIC))
    
    comp_img = np.zeros_like(nn_up)
    comp_img[:, :32] = nn_up[:, :32]
    comp_img[:, 32:] = bicubic_up[:, 32:]
    axes[1, 2].set_title("6. Reconstruction Interpolation\nNearest (Left) vs Bicubic (Right)", 
                         fontsize=13, fontweight="bold")
    axes[1, 2].imshow(comp_img, cmap="gray")
    axes[1, 2].axvline(32, color="yellow", linestyle="--", lw=2.5)
    axes[1, 2].text(16, 12, "Nearest", color="yellow", ha="center", fontsize=11, fontweight="bold",
                    bbox=dict(boxstyle="round,pad=0.2", fc="black", ec="yellow", lw=1))
    axes[1, 2].text(48, 12, "Bicubic", color="yellow", ha="center", fontsize=11, fontweight="bold",
                    bbox=dict(boxstyle="round,pad=0.2", fc="black", ec="yellow", lw=1))
    axes[1, 2].axis("off")
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig10_sampling_aliasing_and_interpolation.png"), 
                dpi=180, facecolor="white")
    plt.close()

if __name__ == "__main__":
    print("Generating Figure 1: Perceptual Illusions & Bottlenecks...")
    fig01_illusions_and_challenges()
    print("Generating Figure 2: Point Operations & Noise Averaging...")
    fig02_point_ops_and_averaging()
    print("Generating Figure 3: Histogram Equalization...")
    fig03_histogram_equalization()
    print("Generating Figure 4: Spatial Convolution & Sobel...")
    fig04_convolution_mechanics_and_padding()
    print("Generating Figure 5: Separability & SVD...")
    fig05_separability_and_svd()
    print("Generating Figure 6: Template Matching & NCC...")
    fig06_ncc_template_matching()
    print("Generating Figure 7: Non-Linear Filters & Bilateral...")
    fig07_nonlinear_filters()
    print("Generating Figure 8: Fourier Spectrum & Oppenheim Phase Swap...")
    fig08_fourier_analysis_and_swap()
    print("Generating Figure 9: Convolution Theorem & Frequency Filtering...")
    fig09_frequency_filtering_and_convolution_theorem()
    print("Generating Figure 10: Sampling, Aliasing & Interpolation...")
    fig10_sampling_aliasing_interpolation()
    print(f"All 10 figures successfully generated in {OUT_DIR}!")
