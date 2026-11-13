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

OUT_DIR = "/Volumes/1700 APFS/PERSONAL_PROGRAMMING_PROJECTS/Notes/Deep Learning for Computer Vision/month 1/week 2/assets"
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

# -------------------------------------------------------------------------
# Figure 1: Canny Edge Pipeline & Sub-Pixel NMS (2x2 Grid)
# -------------------------------------------------------------------------
def fig01_canny_pipeline():
    fig, axes = plt.subplots(2, 2, figsize=(11, 9.5))
    
    # 1. Base image with shapes & noise
    img = np.zeros((64, 64))
    img[12:52, 12:32] = 180 # rectangle
    y, x = np.mgrid[-32:32, -32:32]
    circle_mask = ((x - 8)**2 + (y - 4)**2) < 14**2
    img[circle_mask] = 220
    noisy = np.clip(img + np.random.normal(0, 15, img.shape), 0, 255)
    
    axes[0, 0].set_title("1. Noisy Input Image", fontsize=13, fontweight="bold")
    axes[0, 0].imshow(noisy, cmap="gray")
    axes[0, 0].axis("off")
    
    # 2. Gaussian smoothed & Sobel gradient magnitude
    pil_img = Image.fromarray(noisy.astype(np.uint8))
    smoothed = np.array(pil_img.filter(ImageFilter.GaussianBlur(radius=1.5))).astype(float)
    
    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=float)
    sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=float)
    gx = conv2d_numpy(smoothed, sobel_x)
    gy = conv2d_numpy(smoothed, sobel_y)
    mag = np.sqrt(gx**2 + gy**2)
    theta = np.arctan2(gy, gx) * 180.0 / np.pi
    theta[theta < 0] += 180.0
    
    axes[0, 1].set_title(r"2. Gradient Magnitude $\|\nabla \mathbf{I}\|$", fontsize=13, fontweight="bold")
    im1 = axes[0, 1].imshow(mag, cmap="viridis")
    axes[0, 1].axis("off")
    cbar1 = plt.colorbar(im1, ax=axes[0, 1], fraction=0.046, pad=0.04)
    cbar1.ax.tick_params(labelsize=10)
    
    # 3. NMS Concept Diagram
    ax_nms = axes[1, 0]
    ax_nms.set_title(r"3. Sub-Pixel NMS along Gradient $\theta$", fontsize=13, fontweight="bold")
    # Draw 3x3 pixel grid
    for i in range(4):
        ax_nms.axhline(i, color="#888888", lw=1.5, ls=":")
        ax_nms.axvline(i, color="#888888", lw=1.5, ls=":")
    # Center pixel q at (1.5, 1.5)
    ax_nms.plot(1.5, 1.5, 'ro', markersize=14, label="Center Pixel $q$")
    # Gradient vector at 35 degrees
    dx = 1.05 * np.cos(np.radians(35))
    dy = 1.05 * np.sin(np.radians(35))
    ax_nms.arrow(1.5, 1.5, dx, dy, color="red", width=0.05, head_width=0.18, length_includes_head=True)
    ax_nms.arrow(1.5, 1.5, -dx, -dy, color="red", width=0.05, head_width=0.18, length_includes_head=True)
    # Interpolated points p and r
    ax_nms.plot(1.5 + dx, 1.5 + dy, 'bs', markersize=11, label="Interpolated $p$")
    ax_nms.plot(1.5 - dx, 1.5 - dy, 'bs', markersize=11, label="Interpolated $r$")
    ax_nms.text(1.5, 0.45, "$M(q) \\geq \\max(M(p), M(r))$", ha="center", fontsize=12, fontweight="bold", color="darkred",
                bbox=dict(boxstyle="round,pad=0.3", fc="#fff2f2", ec="red", lw=1.2))
    ax_nms.set_xlim(-0.1, 3.1)
    ax_nms.set_ylim(-0.1, 3.1)
    ax_nms.axis("off")
    ax_nms.legend(loc="upper left", fontsize=10, frameon=True, framealpha=0.9, edgecolor="gray")
    
    # 4. Thin edges after Hysteresis
    nms = np.zeros_like(mag)
    h, w = mag.shape
    for y in range(1, h-1):
        for x in range(1, w-1):
            angle = theta[y, x]
            if (0 <= angle < 22.5) or (157.5 <= angle <= 180):
                q1, q2 = mag[y, x+1], mag[y, x-1]
            elif 22.5 <= angle < 67.5:
                q1, q2 = mag[y+1, x+1], mag[y-1, x-1]
            elif 67.5 <= angle < 112.5:
                q1, q2 = mag[y+1, x], mag[y-1, x]
            else:
                q1, q2 = mag[y+1, x-1], mag[y-1, x+1]
            if mag[y, x] >= q1 and mag[y, x] >= q2:
                nms[y, x] = mag[y, x]
                
    t_high = 120
    t_low = 40
    edges = np.zeros_like(nms)
    strong_y, strong_x = np.where(nms >= t_high)
    edges[strong_y, strong_x] = 255
    for y in range(1, h-1):
        for x in range(1, w-1):
            if t_low <= nms[y, x] < t_high:
                if np.any(edges[y-1:y+2, x-1:x+2] == 255):
                    edges[y, x] = 255
                    
    axes[1, 1].set_title("4. Canny 1-Pixel Edges (Hysteresis)", fontsize=13, fontweight="bold")
    axes[1, 1].imshow(edges, cmap="gray")
    axes[1, 1].axis("off")
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig01_canny_edge_pipeline_and_nms.png"), 
                dpi=180, facecolor="white")
    plt.close()

# -------------------------------------------------------------------------
# Figure 2: Edgelet Second Moment & PCA Linearity Metrics
# -------------------------------------------------------------------------
def fig02_edgelet_second_moment_pca():
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))
    
    # 1. Edgelet Points in 2D
    x = np.array([1.0, 1.8, 2.2, 3.1, 4.0, 4.9, 5.8, 6.2])
    y = 2.0 * x + np.array([0.1, -0.2, 0.3, -0.1, 0.2, -0.3, 0.1, 0.2])
    mu_x, mu_y = np.mean(x), np.mean(y)
    
    axes[0].set_title("1. Edgelet Connected Pixels", fontsize=13, fontweight="bold", pad=10)
    axes[0].plot(x, y, 'ro', markersize=11, label="Edge Pixels")
    axes[0].plot(mu_x, mu_y, 'kX', markersize=14, label=r"Centroid $(\mu_x, \mu_y)$")
    axes[0].set_xlabel("x (column coordinate)", fontsize=12, fontweight="bold")
    axes[0].set_ylabel("y (row coordinate)", fontsize=12, fontweight="bold")
    axes[0].legend(frameon=True, fontsize=11, loc="upper left", framealpha=0.9, edgecolor="gray")
    axes[0].grid(True, linestyle=":", alpha=0.6)
    
    # 2. Covariance Matrix & Eigendecomposition
    dx = x - mu_x
    dy = y - mu_y
    C = np.array([
        [np.sum(dx**2), np.sum(dx*dy)],
        [np.sum(dx*dy), np.sum(dy**2)]
    ]) / len(x)
    
    eigenvals, eigenvecs = np.linalg.eigh(C)
    idx = np.argsort(eigenvals)[::-1]
    eigenvals = eigenvals[idx]
    eigenvecs = eigenvecs[:, idx]
    
    v1 = eigenvecs[:, 0]
    v2 = eigenvecs[:, 1]
    theta_edgelet = np.degrees(np.arctan2(v1[1], v1[0]))
    
    axes[1].set_title(r"2. PCA Orientation & Covariance Ellipse", fontsize=13, fontweight="bold", pad=10)
    axes[1].scatter(dx, dy, color="royalblue", s=70, label="Mean-Centered Pixels")
    s1 = 2 * np.sqrt(eigenvals[0])
    s2 = 2 * np.sqrt(eigenvals[1])
    axes[1].arrow(0, 0, v1[0]*s1, v1[1]*s1, color="red", width=0.10, head_width=0.35, 
                  length_includes_head=True, label=r"Principal $\mathbf{v}_1$ ($\lambda_1$)")
    axes[1].arrow(0, 0, v2[0]*s2, v2[1]*s2, color="green", width=0.10, head_width=0.35, 
                  length_includes_head=True, label=r"Orthogonal $\mathbf{v}_2$ ($\lambda_2$)")
    axes[1].set_xlabel("$x - \\mu_x$", fontsize=12, fontweight="bold")
    axes[1].set_ylabel("$y - \\mu_y$", fontsize=12, fontweight="bold")
    axes[1].text(0, -3.2, f"Orientation $\\theta = {theta_edgelet:.1f}^\\circ$\n$\\lambda_1 / \\lambda_2 = {eigenvals[0]/eigenvals[1]:.1f}$ (High Linearity)", 
                 ha="center", fontsize=11, fontweight="bold", 
                 bbox=dict(boxstyle="round,pad=0.3", fc="#fffde8", ec="orange", lw=1.2))
    axes[1].legend(frameon=True, fontsize=10, loc="upper left", framealpha=0.9, edgecolor="gray")
    axes[1].grid(True, linestyle=":", alpha=0.6)
    axes[1].set_aspect("equal")
    axes[1].set_ylim(-4.2, 4.2)
    
    # 3. Straightness Ratio across curvatures
    curvatures = np.linspace(0, 1.0, 50)
    straightness_ratio = 100.0 / (1.0 + 99.0 * (curvatures**2))
    
    axes[2].set_title(r"3. Straightness Metric $\lambda_1 / \lambda_2$", fontsize=13, fontweight="bold", pad=10)
    axes[2].plot(curvatures, straightness_ratio, 'purple', lw=3.2)
    axes[2].set_xlabel("Edgelet Curvature $\\kappa$", fontsize=12, fontweight="bold")
    axes[2].set_ylabel(r"Eigenvalue Ratio $\lambda_1 / \lambda_2$", fontsize=12, fontweight="bold")
    axes[2].axhline(10, color="red", ls="--", lw=2, label=r"Straight Line Threshold ($\geq 10$)")
    axes[2].legend(frameon=True, fontsize=11, loc="upper right", framealpha=0.9, edgecolor="gray")
    axes[2].grid(True, linestyle=":", alpha=0.6)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig02_edgelet_second_moment_pca.png"), 
                dpi=180, facecolor="white")
    plt.close()

# -------------------------------------------------------------------------
# Figure 3: Harris Corner Structure Tensor Dynamics
# -------------------------------------------------------------------------
def fig03_harris_corner_structure_tensor():
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))
    
    # 1. Aperture Problem Illustration
    ax0 = axes[0]
    ax0.set_title("1. The Aperture Problem", fontsize=13, fontweight="bold", pad=10)
    
    # Flat patch
    rect_flat = plt.Rectangle((0.08, 0.58), 0.36, 0.36, facecolor="#e6e6e6", edgecolor="black", lw=2)
    ax0.add_patch(rect_flat)
    ax0.text(0.26, 0.76, "Flat Region\n$\\Delta I \\approx 0$\nin all directions", 
             ha="center", va="center", fontsize=11, fontweight="bold", color="#222222")
    
    # Edge patch
    rect_edge = plt.Rectangle((0.56, 0.58), 0.36, 0.36, facecolor="white", edgecolor="black", lw=2)
    ax0.add_patch(rect_edge)
    ax0.axvspan(0.56, 0.74, ymin=0.58, ymax=0.94, facecolor="#666666", alpha=0.85)
    ax0.text(0.74, 0.76, "Edge Region\n$\\Delta I = 0$ along\n$\\Delta I > 0$ normal", 
             ha="center", va="center", fontsize=11, fontweight="bold", color="darkred",
             bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="darkred", lw=1))
    
    # Corner patch
    rect_corner = plt.Rectangle((0.32, 0.10), 0.36, 0.36, facecolor="white", edgecolor="black", lw=2)
    ax0.add_patch(rect_corner)
    corner_poly = plt.Polygon([[0.32, 0.10], [0.50, 0.10], [0.50, 0.28], [0.68, 0.28], [0.68, 0.46], [0.32, 0.46]], 
                              facecolor="#444444")
    ax0.add_patch(corner_poly)
    ax0.text(0.50, 0.28, "Corner Region\n$\\Delta I > 0$\nin ALL directions", 
             ha="center", va="center", fontsize=11, fontweight="bold", color="yellow",
             bbox=dict(boxstyle="round,pad=0.2", fc="black", ec="yellow", lw=1))
    
    ax0.set_xlim(0, 1.0)
    ax0.set_ylim(0.04, 1.0)
    ax0.axis("off")
    
    # 2. Eigenvalue Plane lambda_1 vs lambda_2
    ax1 = axes[1]
    ax1.set_title(r"2. Structure Tensor Plane ($\lambda_1, \lambda_2$)", fontsize=13, fontweight="bold", pad=10)
    l_max = 50
    ax1.fill_between([0, 10], [0, 0], [10, 10], color="#e8e8e8", label=r"Flat ($\lambda_1, \lambda_2 \approx 0$)")
    ax1.fill_between([15, l_max], [0, 0], [10, 10], color="#ffcccc", label=r"Edge ($\lambda_1 \gg \lambda_2$)")
    ax1.fill_between([0, 10], [15, 15], [l_max, l_max], color="#ffcccc")
    ax1.fill_between([15, l_max], [15, 15], [l_max, l_max], color="#cce5ff", label=r"Corner ($\lambda_1, \lambda_2 \gg 0$)")
    ax1.plot([0, l_max], [0, l_max], 'k--', alpha=0.5, lw=1.5)
    ax1.set_xlabel(r"$\lambda_1$ (Major Eigenvalue)", fontsize=12, fontweight="bold")
    ax1.set_ylabel(r"$\lambda_2$ (Minor Eigenvalue)", fontsize=12, fontweight="bold")
    ax1.set_xlim(0, l_max)
    ax1.set_ylim(0, l_max)
    ax1.legend(frameon=True, fontsize=10, loc="upper left", framealpha=0.9, edgecolor="gray")
    ax1.grid(True, linestyle=":", alpha=0.6)
    
    # 3. Harris Response Surface R = det(A) - kappa * trace^2(A)
    ax2 = axes[2]
    ax2.set_title(r"3. Harris Response $R = \det(\mathbf{A}) - \kappa \operatorname{tr}^2(\mathbf{A})$", 
                  fontsize=13, fontweight="bold", pad=10)
    l1 = np.linspace(0, 50, 120)
    l2 = np.linspace(0, 50, 120)
    L1, L2 = np.meshgrid(l1, l2)
    kappa = 0.05
    R = (L1 * L2) - kappa * ((L1 + L2)**2)
    
    im_r = ax2.contourf(L1, L2, R, levels=20, cmap="coolwarm")
    cbar = plt.colorbar(im_r, ax=ax2, fraction=0.046, pad=0.04)
    cbar.set_label("Cornerness Score $R$", fontsize=11, fontweight="bold")
    ax2.contour(L1, L2, R, levels=[0], colors="black", linewidths=2.5)
    ax2.text(35, 35, "$R > 0$\n(Corner)", color="darkblue", fontweight="bold", ha="center", fontsize=11,
             bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="darkblue", lw=1))
    ax2.text(36, 6, "$R < 0$\n(Edge)", color="darkred", fontweight="bold", ha="center", fontsize=11,
             bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="darkred", lw=1))
    ax2.text(6, 6, "$R \\approx 0$\n(Flat)", color="black", fontweight="bold", ha="center", fontsize=11,
             bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="black", lw=1))
    ax2.set_xlabel(r"$\lambda_1$", fontsize=12, fontweight="bold")
    ax2.set_ylabel(r"$\lambda_2$", fontsize=12, fontweight="bold")
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig03_harris_corner_structure_tensor.png"), 
                dpi=180, facecolor="white")
    plt.close()

# -------------------------------------------------------------------------
# Figure 4: Scale Space Representation & DoG Extrema Selection
# -------------------------------------------------------------------------
def fig04_scale_space_log_dog():
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))
    
    # 1. 1D LoG Mexican Hat vs DoG Comparison
    x = np.linspace(-5, 5, 200)
    sigma = 1.0
    k = 1.6
    log_1d = (1.0 / (np.sqrt(2 * np.pi) * sigma**3)) * (1.0 - (x**2 / sigma**2)) * np.exp(-x**2 / (2 * sigma**2))
    g1 = (1.0 / (np.sqrt(2 * np.pi) * sigma)) * np.exp(-x**2 / (2 * sigma**2))
    g2 = (1.0 / (np.sqrt(2 * np.pi) * (k * sigma))) * np.exp(-x**2 / (2 * (k * sigma)**2))
    dog_1d = (g2 - g1) * (1.0 / (k - 1.0))
    
    axes[0].set_title(r"1. LoG ($\sigma^2 \nabla^2 G$) vs DoG Profile", fontsize=13, fontweight="bold", pad=10)
    axes[0].plot(x, log_1d, 'b-', lw=3.2, label="LoG (Mexican Hat)")
    axes[0].plot(x, -dog_1d * 1.5, 'r--', lw=2.8, label=f"DoG ($G_{{k\\sigma}} - G_{{\\sigma}}, k={k}$)")
    axes[0].axhline(0, color="gray", ls=":", lw=1.5)
    axes[0].set_xlabel("Spatial Coordinate $x$", fontsize=12, fontweight="bold")
    axes[0].set_ylabel("Kernel Amplitude", fontsize=12, fontweight="bold")
    axes[0].legend(frameon=True, fontsize=11, loc="upper right", framealpha=0.9, edgecolor="gray")
    axes[0].grid(True, linestyle=":", alpha=0.6)
    
    # 2. Scale-space pyramid (octaves)
    ax_pyr = axes[1]
    ax_pyr.set_title("2. Gaussian Scale-Space Pyramid", fontsize=13, fontweight="bold", pad=10)
    levels = [1.0, 0.75, 0.55, 0.40]
    labels = ["Octave 1 (Original)", "Octave 2 (Subsample 2×)", "Octave 3 (Subsample 4×)", "Octave 4 (Subsample 8×)"]
    scale_sigmas = ["$\\sigma_0$", "$2\\sigma_0$", "$4\\sigma_0$", "$8\\sigma_0$"]
    colors = ["#4c72b0", "#55a868", "#c44e52", "#8172b3"]
    for idx, (lev, lbl, col, sig) in enumerate(zip(levels, labels, colors, scale_sigmas)):
        rect = plt.Rectangle((0.45 - lev/2, idx*0.25), lev, 0.20, facecolor=col, alpha=0.85, edgecolor="black", lw=1.8)
        ax_pyr.add_patch(rect)
        ax_pyr.text(0.45, idx*0.25 + 0.10, lbl, ha="center", va="center", color="white", fontweight="bold", fontsize=11)
        ax_pyr.text(0.92, idx*0.25 + 0.10, sig, ha="left", va="center", color=col, fontweight="bold", fontsize=12)
    ax_pyr.set_xlim(-0.1, 1.15)
    ax_pyr.set_ylim(-0.05, 1.05)
    ax_pyr.axis("off")
    
    # 3. Characteristic Scale Selection Curve
    ax_scale = axes[2]
    ax_scale.set_title("3. Characteristic Scale Selection Peak", fontsize=13, fontweight="bold", pad=10)
    blob_radius = 6.0
    sigmas = np.linspace(1.0, 15.0, 120)
    true_peak_sigma = blob_radius / np.sqrt(2.0)
    response = (sigmas**2) * np.exp(- (sigmas - true_peak_sigma)**2 / 6.0)
    response /= response.max()
    
    ax_scale.plot(sigmas, response, 'purple', lw=3.2, label=r"Scale Response $\sigma^2 |\nabla^2 G * I|$")
    ax_scale.axvline(true_peak_sigma, color="red", ls="--", lw=2.2, label=f"Peak $\\sigma^* = {true_peak_sigma:.2f}$")
    ax_scale.set_xlabel(r"Scale Parameter $\sigma$ (pixels)", fontsize=12, fontweight="bold")
    ax_scale.set_ylabel("Normalized Response", fontsize=12, fontweight="bold")
    ax_scale.text(true_peak_sigma + 0.6, 0.82, f"Peak Scale $\\sigma^* = r / \\sqrt{{2}}$\nRadius $r = {blob_radius:.1f}$ px", 
                  color="darkred", fontweight="bold", fontsize=11,
                  bbox=dict(boxstyle="round,pad=0.2", fc="#fff2f2", ec="red", lw=1))
    ax_scale.legend(frameon=True, fontsize=11, loc="lower right", framealpha=0.9, edgecolor="gray")
    ax_scale.grid(True, linestyle=":", alpha=0.6)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig04_scale_space_log_and_dog.png"), 
                dpi=180, facecolor="white")
    plt.close()

# -------------------------------------------------------------------------
# Figure 5: SIFT Descriptor Pipeline
# -------------------------------------------------------------------------
def fig05_sift_descriptor_pipeline():
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))
    
    # 1. 3D DoG Extrema Search (26 Neighbors)
    ax0 = axes[0]
    ax0.set_title("1. Scale-Space Extrema (26 Neighbors)", fontsize=13, fontweight="bold", pad=10)
    scales = [r"Scale $k^2\sigma_0$ (Upper 9)", r"Scale $k\sigma_0$ (Candidate + 8)", r"Scale $\sigma_0$ (Lower 9)"]
    offsets = [0.66, 0.36, 0.06]
    for sc, off in zip(scales, offsets):
        rect = plt.Rectangle((0.10, off), 0.80, 0.22, facecolor="#eef6fb", edgecolor="#555555", lw=1.5)
        ax0.add_patch(rect)
        ax0.text(0.12, off + 0.17, sc, fontsize=10, fontweight="bold", color="navy")
        for r in range(3):
            for c in range(3):
                px = 0.38 + c * 0.16
                py = off + 0.04 + r * 0.06
                if off == 0.36 and r == 1 and c == 1:
                    ax0.plot(px, py, 'r*', markersize=14, label="Keypoint Candidate $X$")
                else:
                    ax0.plot(px, py, 'ks', markersize=7, alpha=0.6)
    ax0.set_xlim(0, 1.0)
    ax0.set_ylim(0, 0.96)
    ax0.axis("off")
    ax0.legend(loc="upper right", fontsize=10, frameon=True, framealpha=0.9, edgecolor="gray")
    
    # 2. Keypoint Orientation Histogram
    ax1 = axes[1]
    ax1.set_title("2. Keypoint Canonical Orientation", fontsize=13, fontweight="bold", pad=10)
    angles = np.linspace(0, 350, 36)
    hist_weights = 10 + 90 * np.exp(-(angles - 70)**2 / (2 * 25**2)) + 45 * np.exp(-(angles - 250)**2 / (2 * 20**2))
    ax1.bar(angles, hist_weights, width=8.5, color="teal", edgecolor="black", alpha=0.85)
    ax1.axvline(70, color="red", ls="--", lw=2.5, label="Dominant $\\theta_0 = 70^\\circ$")
    ax1.set_xlabel("Gradient Orientation (degrees, 36 bins)", fontsize=12, fontweight="bold")
    ax1.set_ylabel("Weighted Gradient Magnitude", fontsize=12, fontweight="bold")
    ax1.legend(frameon=True, fontsize=11, loc="upper right", framealpha=0.9, edgecolor="gray")
    ax1.grid(True, linestyle=":", alpha=0.6)
    
    # 3. 128-D SIFT Feature Vector Pooling
    ax2 = axes[2]
    ax2.set_title("3. SIFT 128-D Descriptor Grid", fontsize=13, fontweight="bold", pad=10)
    for i in range(5):
        ax2.axhline(i, color="black", lw=2)
        ax2.axvline(i, color="black", lw=2)
    angles_8 = np.arange(0, 360, 45)
    for r in range(4):
        for c in range(4):
            cx, cy = c + 0.5, r + 0.5
            for ang in angles_8:
                length = 0.16 + 0.22 * np.random.rand()
                rad = np.radians(ang)
                ax2.arrow(cx, cy, length * np.cos(rad), length * np.sin(rad), 
                          color="darkblue", width=0.02, head_width=0.08, length_includes_head=True)
    ax2.set_xlim(-0.2, 4.2)
    ax2.set_ylim(-0.4, 4.4)
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.text(2.0, -0.25, "16 Spatial Cells × 8 Orientation Bins = 128 Dimensions", 
             ha="center", fontsize=11, fontweight="bold",
             bbox=dict(boxstyle="round,pad=0.3", fc="#f2f2f2", ec="gray", lw=1))
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig05_sift_descriptor_pipeline.png"), 
                dpi=180, facecolor="white")
    plt.close()

# -------------------------------------------------------------------------
# Figure 6: SURF, GLOH, SIFT & MOPS Comparison
# -------------------------------------------------------------------------
def fig06_surf_gloh_mops_comparison():
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))
    
    # 1. GLOH Grid Geometry
    ax0 = axes[0]
    ax0.set_title("1. GLOH Log-Polar Spatial Grid", fontsize=13, fontweight="bold", pad=10)
    radii = [0.3, 0.6, 1.0]
    for r in radii:
        circle = plt.Circle((0, 0), r, fill=False, color="navy", lw=2.2)
        ax0.add_patch(circle)
    for angle in np.linspace(0, 360, 9)[:-1]:
        rad = np.radians(angle)
        ax0.plot([0.3 * np.cos(rad), 1.0 * np.cos(rad)], [0.3 * np.sin(rad), 1.0 * np.sin(rad)], 'b--', lw=1.5)
    ax0.set_xlim(-1.25, 1.25)
    ax0.set_ylim(-1.35, 1.25)
    ax0.set_aspect("equal")
    ax0.axis("off")
    ax0.text(0, 0, "Inner (1)", ha="center", va="center", fontsize=10, fontweight="bold", color="darkred")
    ax0.text(0, 0.45, "Middle (8)", ha="center", va="center", fontsize=10, fontweight="bold")
    ax0.text(0, 0.80, "Outer (8)", ha="center", va="center", fontsize=10, fontweight="bold")
    ax0.text(0, -1.20, "17 Spatial Bins × 16 Orientations = 272-D → PCA 128-D", 
             ha="center", fontsize=10, fontweight="bold",
             bbox=dict(boxstyle="round,pad=0.2", fc="#f6f6f6", ec="navy", lw=1))
    
    # 2. SURF Box Filter Approximations (Integral Image)
    ax1 = axes[1]
    ax1.set_title("2. SURF Haar Box Approximations", fontsize=13, fontweight="bold", pad=10)
    # Dxx
    rect_bg = plt.Rectangle((0.1, 0.56), 0.8, 0.38, facecolor="#d0d0d0", edgecolor="black", lw=1.5)
    ax1.add_patch(rect_bg)
    ax1.add_patch(plt.Rectangle((0.10, 0.56), 0.25, 0.38, facecolor="white", edgecolor="black", lw=1.5))
    ax1.add_patch(plt.Rectangle((0.65, 0.56), 0.25, 0.38, facecolor="white", edgecolor="black", lw=1.5))
    ax1.add_patch(plt.Rectangle((0.35, 0.56), 0.30, 0.38, facecolor="black", edgecolor="black", lw=1.5))
    ax1.text(0.50, 0.75, "-2", color="white", ha="center", va="center", fontweight="bold", fontsize=12)
    ax1.text(0.22, 0.75, "+1", color="black", ha="center", va="center", fontweight="bold", fontsize=12)
    ax1.text(0.78, 0.75, "+1", color="black", ha="center", va="center", fontweight="bold", fontsize=12)
    ax1.text(0.50, 0.49, "$D_{xx}$ Filter (Constant $\\mathcal{O}(1)$ via Integral Image)", 
             ha="center", fontsize=10, fontweight="bold")
    
    # Dxy
    ax1.add_patch(plt.Rectangle((0.2, 0.08), 0.6, 0.36, facecolor="gray", edgecolor="black", lw=1.5))
    ax1.add_patch(plt.Rectangle((0.2, 0.26), 0.3, 0.18, facecolor="white", edgecolor="black", lw=1.5))
    ax1.add_patch(plt.Rectangle((0.5, 0.08), 0.3, 0.18, facecolor="white", edgecolor="black", lw=1.5))
    ax1.add_patch(plt.Rectangle((0.5, 0.26), 0.3, 0.18, facecolor="black", edgecolor="black", lw=1.5))
    ax1.add_patch(plt.Rectangle((0.2, 0.08), 0.3, 0.18, facecolor="black", edgecolor="black", lw=1.5))
    ax1.text(0.5, 0.01, "$D_{xy}$ Filter (Evaluated via 4 Corner Lookups)", 
             ha="center", fontsize=10, fontweight="bold")
    ax1.set_xlim(0, 1.0)
    ax1.set_ylim(-0.06, 1.05)
    ax1.axis("off")
    
    # 3. Computational Benchmark: SIFT vs SURF vs GLOH vs MOPS
    ax2 = axes[2]
    ax2.set_title("3. Speed vs Matching Accuracy", fontsize=13, fontweight="bold", pad=10)
    methods = ["SURF", "SIFT", "GLOH", "MOPS"]
    speed_ms = [14.0, 48.0, 62.0, 18.0]
    accuracy_pct = [86.5, 88.0, 91.2, 74.0]
    
    ax2.scatter(speed_ms, accuracy_pct, s=[240, 260, 280, 220], color=["#2ca02c", "#1f77b4", "#9467bd", "#ff7f0e"], zorder=5)
    for m, s, a in zip(methods, speed_ms, accuracy_pct):
        offset_y = 0.8 if m != "SIFT" else -1.8
        offset_x = 2.0
        ax2.text(s + offset_x, a + offset_y, m, fontsize=12, fontweight="bold")
    ax2.set_xlabel("Computation Time per Image (ms)", fontsize=12, fontweight="bold")
    ax2.set_ylabel("Matching Recall (%)", fontsize=12, fontweight="bold")
    ax2.grid(True, linestyle=":", alpha=0.6)
    ax2.set_xlim(5, 75)
    ax2.set_ylim(70, 96)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig06_surf_gloh_mops_comparison.png"), 
                dpi=180, facecolor="white")
    plt.close()

# -------------------------------------------------------------------------
# Figure 7: Gestalt Laws & Segmentation Paradigms (2x2 Grid)
# -------------------------------------------------------------------------
def fig07_gestalt_and_segmentation():
    fig, axes = plt.subplots(2, 2, figsize=(11, 9.5))
    
    # 1. Gestalt Grouping Laws
    ax0 = axes[0, 0]
    ax0.set_title("1. Gestalt Grouping Laws", fontsize=13, fontweight="bold")
    # Proximity
    for c in [0.12, 0.22, 0.52, 0.62]:
        for r in [0.72, 0.86]:
            ax0.plot(c, r, 'bo', markersize=9)
    ax0.text(0.37, 0.92, "Proximity", ha="center", fontsize=11, fontweight="bold")
    # Similarity
    for idx, c in enumerate(np.linspace(0.12, 0.66, 6)):
        marker = 'ro' if idx % 2 == 0 else 'bs'
        ax0.plot(c, 0.50, marker, markersize=9)
    ax0.text(0.37, 0.58, "Similarity", ha="center", fontsize=11, fontweight="bold")
    # Closure
    ax0.plot([0.15, 0.55], [0.18, 0.18], 'k-', lw=3)
    ax0.plot([0.15, 0.15], [0.18, 0.36], 'k-', lw=3)
    ax0.plot([0.55, 0.55], [0.18, 0.36], 'k-', lw=3)
    ax0.plot([0.15, 0.30], [0.36, 0.36], 'k--', lw=2.5)
    ax0.plot([0.40, 0.55], [0.36, 0.36], 'k--', lw=2.5)
    ax0.text(0.35, 0.25, "Closure", ha="center", fontsize=11, fontweight="bold")
    ax0.set_xlim(0, 0.8)
    ax0.set_ylim(0.08, 1.0)
    ax0.axis("off")
    
    # 2. Watershed Flooding
    ax1 = axes[0, 1]
    ax1.set_title("2. Watershed Flooding Paradigm", fontsize=13, fontweight="bold")
    x = np.linspace(0, 10, 200)
    topo = 2.0 + 1.5 * np.cos(x * 1.2) + 0.8 * np.sin(x * 0.6)
    water_level = 2.4
    ax1.plot(x, topo, 'k-', lw=3.0, label="Topographic Gradient Surface")
    ax1.axhline(water_level, color="blue", ls="--", lw=2, label=f"Water Level $h = {water_level}$")
    ax1.fill_between(x, topo, water_level, where=(topo < water_level), color="skyblue", alpha=0.6, label="Catchment Basins")
    ax1.set_xlabel("Spatial Coordinate", fontsize=12, fontweight="bold")
    ax1.set_ylabel("Gradient Elevation", fontsize=12, fontweight="bold")
    ax1.legend(loc="upper right", fontsize=10, frameon=True, framealpha=0.9, edgecolor="gray")
    ax1.grid(True, linestyle=":", alpha=0.5)
    
    # 3. Mean Shift Mode Seeking
    ax2 = axes[1, 0]
    ax2.set_title("3. Mean Shift Mode Seeking", fontsize=13, fontweight="bold")
    c1 = np.random.normal(loc=[-1.5, -1.0], scale=0.55, size=(60, 2))
    c2 = np.random.normal(loc=[1.5, 1.2], scale=0.65, size=(80, 2))
    ax2.scatter(c1[:, 0], c1[:, 1], color="teal", alpha=0.55, s=35)
    ax2.scatter(c2[:, 0], c2[:, 1], color="coral", alpha=0.55, s=35)
    traj = np.array([[0.0, -2.5], [-0.5, -2.0], [-1.0, -1.5], [-1.5, -1.0]])
    ax2.plot(traj[:, 0], traj[:, 1], 'r-o', lw=3.0, markersize=7, label="Mode Trajectory")
    ax2.plot(traj[-1, 0], traj[-1, 1], 'k*', markersize=16, label="Stationary Mode")
    ax2.set_xlabel("Feature Space $x_1$", fontsize=12, fontweight="bold")
    ax2.set_ylabel("Feature Space $x_2$", fontsize=12, fontweight="bold")
    ax2.legend(loc="upper left", fontsize=10, frameon=True, framealpha=0.9, edgecolor="gray")
    ax2.grid(True, linestyle=":", alpha=0.5)
    
    # 4. Graph Cut Minimum Energy Cut
    ax3 = axes[1, 1]
    ax3.set_title("4. Graph Cut (Min s-t Cut)", fontsize=13, fontweight="bold")
    ax3.plot(0.2, 0.5, 'go', markersize=18, label="Source $S$ (Foreground)")
    ax3.plot(0.8, 0.5, 'ro', markersize=18, label="Sink $T$ (Background)")
    for py in [0.25, 0.5, 0.75]:
        ax3.plot(0.4, py, 'ks', markersize=12)
        ax3.plot(0.6, py, 'ks', markersize=12)
        ax3.plot([0.4, 0.6], [py, py], 'k-', lw=2)
        ax3.plot([0.2, 0.4], [0.5, py], 'g:', lw=1.5)
        ax3.plot([0.6, 0.8], [py, 0.5], 'r:', lw=1.5)
    ax3.axvline(0.5, color="red", ls="--", lw=3.2, label="Min Cut Boundary")
    ax3.set_xlim(0.05, 0.95)
    ax3.set_ylim(0.1, 0.9)
    ax3.axis("off")
    ax3.legend(loc="upper center", fontsize=10, frameon=True, framealpha=0.9, edgecolor="gray")
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig07_gestalt_and_segmentation_paradigms.png"), 
                dpi=180, facecolor="white")
    plt.close()

# -------------------------------------------------------------------------
# Figure 8: Shape Context Log-Polar Matching
# -------------------------------------------------------------------------
def fig08_shape_context_log_polar():
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))
    
    # 1. Silhouette Contour with Sample Points
    t = np.linspace(0, 2*np.pi, 30, endpoint=False)
    x = 1.5 * np.cos(t) + 0.2 * np.cos(3*t)
    y = 1.0 * np.sin(t) - 0.3 * np.sin(2*t)
    
    axes[0].set_title("1. Shape Contour & Sample Points", fontsize=13, fontweight="bold", pad=10)
    axes[0].plot(x, y, 'k-', lw=2.5)
    axes[0].plot(x, y, 'bo', markersize=8, label="Sampled Points")
    ref_idx = 5
    axes[0].plot(x[ref_idx], y[ref_idx], 'r*', markersize=18, label=r"Reference $p_i$")
    axes[0].set_aspect("equal")
    axes[0].legend(frameon=True, fontsize=11, loc="upper right", framealpha=0.9, edgecolor="gray")
    axes[0].axis("off")
    
    # 2. Log-Polar Bins centered at p_i
    axes[1].set_title(r"2. Log-Polar Spatial Bins ($5 \times 12$)", fontsize=13, fontweight="bold", pad=10)
    radii = [0.2, 0.45, 0.9, 1.6, 2.5]
    for r in radii:
        axes[1].add_patch(plt.Circle((0, 0), r, fill=False, color="purple", lw=1.8))
    for ang in np.linspace(0, 360, 13)[:-1]:
        rad = np.radians(ang)
        axes[1].plot([0, 2.5*np.cos(rad)], [0, 2.5*np.sin(rad)], 'm:', lw=1.2)
    rel_x = x - x[ref_idx]
    rel_y = y - y[ref_idx]
    axes[1].plot(rel_x, rel_y, 'bo', markersize=8)
    axes[1].plot(0, 0, 'r*', markersize=18)
    axes[1].set_xlim(-2.8, 2.8)
    axes[1].set_ylim(-3.0, 2.8)
    axes[1].set_aspect("equal")
    axes[1].axis("off")
    axes[1].text(0, -2.85, "Log-radial distance + angular quantization", ha="center", fontsize=11, fontweight="bold",
                 bbox=dict(boxstyle="round,pad=0.2", fc="#fbf5ff", ec="purple", lw=1))
    
    # 3. Shape Context Histogram Matrix
    hist_matrix = np.zeros((5, 12))
    hist_matrix[1:4, 2:8] = np.random.poisson(lam=4, size=(3, 6))
    hist_matrix[0, 1:4] = np.random.poisson(lam=6, size=3)
    
    sns.heatmap(hist_matrix, cmap="magma", annot=True, fmt=".0f", ax=axes[2], cbar=False,
                annot_kws={"size": 12, "weight": "bold"})
    axes[2].set_title(r"3. Shape Context Histogram $h_i(k)$", fontsize=13, fontweight="bold", pad=10)
    axes[2].set_xlabel(r"Angular Bins $\theta \in [0, 2\pi)$ (12 bins)", fontsize=12, fontweight="bold")
    axes[2].set_ylabel(r"Log-Radial Bins $\log(r)$ (5 bins)", fontsize=12, fontweight="bold")
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig08_shape_context_log_polar_matching.png"), 
                dpi=180, facecolor="white")
    plt.close()

# -------------------------------------------------------------------------
# Figure 9: MSER Component Tree & Area Stability Function
# -------------------------------------------------------------------------
def fig09_mser_component_tree():
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))
    
    # 1. Grayscale Landscape with Threshold Sweeps
    x = np.linspace(0, 10, 200)
    intensity = 180 - 120 * np.exp(-(x - 3)**2 / 1.5) - 90 * np.exp(-(x - 7.5)**2 / 2.0)
    
    axes[0].set_title("1. Threshold Sweep Across Intensity", fontsize=13, fontweight="bold", pad=10)
    axes[0].plot(x, intensity, 'k-', lw=3.0)
    axes[0].axhline(80, color="green", ls="--", lw=2, label="Threshold $g_1 = 80$ (2 blobs)")
    axes[0].axhline(120, color="orange", ls="--", lw=2, label="Threshold $g_2 = 120$ (Expanded)")
    axes[0].axhline(155, color="red", ls="--", lw=2, label="Threshold $g_3 = 155$ (Merged)")
    axes[0].fill_between(x, intensity, 80, where=(intensity < 80), color="green", alpha=0.3)
    axes[0].fill_between(x, intensity, 120, where=(intensity < 120), color="orange", alpha=0.2)
    axes[0].set_xlabel("Spatial Coordinate", fontsize=12, fontweight="bold")
    axes[0].set_ylabel("Grayscale Intensity $g$", fontsize=12, fontweight="bold")
    axes[0].legend(frameon=True, fontsize=10, loc="lower right", framealpha=0.9, edgecolor="gray")
    axes[0].grid(True, linestyle=":", alpha=0.6)
    
    # 2. Extremal Region Component Tree
    ax1 = axes[1]
    ax1.set_title("2. Extremal Region Component Tree", fontsize=13, fontweight="bold", pad=10)
    ax1.plot([2, 5], [0.8, 0.5], 'k-', lw=2.5)
    ax1.plot([8, 5], [0.8, 0.5], 'k-', lw=2.5)
    ax1.plot([5, 5], [0.5, 0.15], 'k-', lw=2.5)
    
    ax1.plot(2, 0.8, 'go', markersize=16, label="$Q_1$ (Left Basin)")
    ax1.plot(8, 0.8, 'go', markersize=16, label="$Q_2$ (Right Basin)")
    ax1.plot(5, 0.5, 'yo', markersize=20, label="$Q_{\\text{merge}}$ (Combined)")
    ax1.plot(5, 0.15, 'ro', markersize=24, label="$Q_{\\text{root}}$ (Entire Frame)")
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 1.0)
    ax1.axis("off")
    ax1.legend(loc="upper center", fontsize=11, frameon=True, framealpha=0.9, edgecolor="gray")
    
    # 3. MSER Stability Rate Curve
    thresholds = np.arange(40, 200, 2)
    area = 200 / (1.0 + np.exp(-(thresholds - 60)/5.0)) + 400 / (1.0 + np.exp(-(thresholds - 140)/6.0))
    delta = 4
    q_rate = np.zeros(len(thresholds))
    for i in range(delta, len(thresholds) - delta):
        q_rate[i] = (area[i+delta] - area[i-delta]) / area[i]
    q_rate[:delta] = q_rate[delta]
    q_rate[-delta:] = q_rate[-delta-1]
    
    axes[2].set_title(r"3. Stability Rate $q(g) = \frac{|Q_{g+\Delta} \setminus Q_{g-\Delta}|}{|Q_g|}$", 
                      fontsize=13, fontweight="bold", pad=10)
    axes[2].plot(thresholds, q_rate, 'crimson', lw=3.0, label="Area Growth Rate $q(g)$")
    min_idx = np.argmin(q_rate[20:45]) + 20
    axes[2].plot(thresholds[min_idx], q_rate[min_idx], 'g*', markersize=18, 
                 label=f"MSER Local Min ($g={thresholds[min_idx]}$)")
    axes[2].set_xlabel("Threshold Intensity $g$", fontsize=12, fontweight="bold")
    axes[2].set_ylabel("Stability Rate $q(g)$", fontsize=12, fontweight="bold")
    axes[2].legend(frameon=True, fontsize=11, loc="upper right", framealpha=0.9, edgecolor="gray")
    axes[2].grid(True, linestyle=":", alpha=0.6)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig09_mser_component_tree_stability.png"), 
                dpi=180, facecolor="white")
    plt.close()

# -------------------------------------------------------------------------
# Figure 10: Biological Visual Pathway & Cortical Streams
# -------------------------------------------------------------------------
def fig10_biological_visual_pathway():
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))
    
    # 1. Retinal Ganglion Cell Receptive Field (DoG)
    ax0 = axes[0]
    ax0.set_title("1. Retinal Ganglion On-Center DoG", fontsize=13, fontweight="bold", pad=10)
    r = np.linspace(-4, 4, 100)
    R_x, R_y = np.meshgrid(r, r)
    rad_sq = R_x**2 + R_y**2
    dog_retina = np.exp(-rad_sq / (2 * 0.8**2)) - 0.5 * np.exp(-rad_sq / (2 * 2.0**2))
    ax0.contourf(R_x, R_y, dog_retina, levels=20, cmap="coolwarm")
    ax0.set_aspect("equal")
    ax0.axis("off")
    ax0.text(0, 0, "+", color="white", ha="center", va="center", fontsize=20, fontweight="bold")
    ax0.text(0, 2.5, "−", color="navy", ha="center", va="center", fontsize=24, fontweight="bold")
    ax0.text(0, -3.5, "Center Excitation (+) / Surround Inhibition (−)", ha="center", fontsize=11, fontweight="bold",
             bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="navy", lw=1))
    
    # 2. V1 Simple Cell Oriented Receptive Field (Gabor)
    ax1 = axes[1]
    ax1.set_title("2. V1 Simple Cell (Hubel & Wiesel Gabor)", fontsize=13, fontweight="bold", pad=10)
    x_rot = R_x * np.cos(np.pi/4) + R_y * np.sin(np.pi/4)
    y_rot = -R_x * np.sin(np.pi/4) + R_y * np.cos(np.pi/4)
    gabor_v1 = np.exp(-(x_rot**2 + 0.5*y_rot**2) / (2 * 1.5**2)) * np.cos(2*np.pi*x_rot / 1.5)
    ax1.contourf(R_x, R_y, gabor_v1, levels=20, cmap="coolwarm")
    ax1.set_aspect("equal")
    ax1.axis("off")
    ax1.text(0, -3.5, "Oriented Excitatory & Inhibitory Bands (45°)", ha="center", fontsize=11, fontweight="bold",
             bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="darkred", lw=1))
    
    # 3. Dual Cortical Processing Streams
    ax2 = axes[2]
    ax2.set_title("3. Dual Cortical Visual Streams", fontsize=13, fontweight="bold", pad=10)
    
    rect_v1 = plt.Rectangle((0.04, 0.38), 0.22, 0.24, facecolor="#4c72b0", edgecolor="black", lw=2)
    rect_dorsal = plt.Rectangle((0.52, 0.64), 0.44, 0.28, facecolor="#c44e52", edgecolor="black", lw=2)
    rect_ventral = plt.Rectangle((0.52, 0.08), 0.44, 0.28, facecolor="#55a868", edgecolor="black", lw=2)
    
    ax2.add_patch(rect_v1)
    ax2.add_patch(rect_dorsal)
    ax2.add_patch(rect_ventral)
    
    ax2.text(0.15, 0.50, "Primary\nVisual\nCortex\n(V1)", color="white", ha="center", va="center", fontweight="bold", fontsize=11)
    ax2.text(0.74, 0.78, "Dorsal Stream ('Where / How')\nV1 → V2 → MT/V5 → Parietal\n(Motion, Spatial Localization)", 
             color="white", ha="center", va="center", fontweight="bold", fontsize=10)
    ax2.text(0.74, 0.22, "Ventral Stream ('What')\nV1 → V2 → V4 → IT Cortex\n(Object Identity, Shape, Color)", 
             color="white", ha="center", va="center", fontweight="bold", fontsize=10)
    
    ax2.arrow(0.26, 0.54, 0.24, 0.18, color="black", width=0.018, head_width=0.05, length_includes_head=True)
    ax2.arrow(0.26, 0.46, 0.24, -0.18, color="black", width=0.018, head_width=0.05, length_includes_head=True)
    ax2.set_xlim(0, 1.0)
    ax2.set_ylim(0, 1.0)
    ax2.axis("off")
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig10_biological_visual_pathway_and_v1.png"), 
                dpi=180, facecolor="white")
    plt.close()

if __name__ == "__main__":
    print("Generating Figure 1: Canny Edge Pipeline & NMS...")
    fig01_canny_pipeline()
    print("Generating Figure 2: Edgelet Second Moment & PCA...")
    fig02_edgelet_second_moment_pca()
    print("Generating Figure 3: Harris Corner Structure Tensor...")
    fig03_harris_corner_structure_tensor()
    print("Generating Figure 4: Scale Space LoG & DoG...")
    fig04_scale_space_log_dog()
    print("Generating Figure 5: SIFT Descriptor Pipeline...")
    fig05_sift_descriptor_pipeline()
    print("Generating Figure 6: SURF, GLOH, SIFT & MOPS Comparison...")
    fig06_surf_gloh_mops_comparison()
    print("Generating Figure 7: Gestalt Laws & Segmentation...")
    fig07_gestalt_and_segmentation()
    print("Generating Figure 8: Shape Context Log-Polar...")
    fig08_shape_context_log_polar()
    print("Generating Figure 9: MSER Component Tree...")
    fig09_mser_component_tree()
    print("Generating Figure 10: Biological Visual Pathway...")
    fig10_biological_visual_pathway()
    print(f"All 10 figures successfully generated in {OUT_DIR}!")
