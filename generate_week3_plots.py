import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Professional Academic Styling matching Weeks 1 & 2
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

OUT_DIR = "/Volumes/1700 APFS/PERSONAL_PROGRAMMING_PROJECTS/Notes/Deep Learning for Computer Vision/month 1/week 3/assets"
os.makedirs(OUT_DIR, exist_ok=True)
np.random.seed(42)

# =========================================================================
# Figure 1: Early Neurons & The XOR Linear Separability Crisis
# =========================================================================
def fig01_early_neurons_and_xor():
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))

    # 1. McCulloch-Pitts Neuron Logic (AND / OR)
    ax0 = axes[0]
    ax0.set_title("1. McCulloch-Pitts & Perceptron\nLinear Boundary ($w^T x \\geq 0$)", fontsize=13, fontweight="bold", pad=10)
    # AND function
    ax0.scatter([0, 0, 1], [0, 1, 0], color="crimson", s=100, marker="o", label="Class 0 (Off)")
    ax0.scatter([1], [1], color="forestgreen", s=130, marker="^", label="Class 1 (On)")
    # Line x1 + x2 = 1.5 -> x2 = 1.5 - x1
    x_vals = np.linspace(-0.2, 1.4, 100)
    ax0.plot(x_vals, 1.5 - x_vals, 'b--', lw=2.5, label="Boundary $x_1 + x_2 = 1.5$")
    ax0.fill_between(x_vals, 1.5 - x_vals, 1.5, color="green", alpha=0.1)
    ax0.fill_between(x_vals, -0.3, 1.5 - x_vals, color="red", alpha=0.08)
    ax0.set_xlim(-0.2, 1.3)
    ax0.set_ylim(-0.2, 1.3)
    ax0.set_xlabel("$x_1$", fontsize=12, fontweight="bold")
    ax0.set_ylabel("$x_2$", fontsize=12, fontweight="bold")
    ax0.legend(frameon=True, fontsize=10, loc="lower left", framealpha=0.9, edgecolor="gray")
    ax0.grid(True, linestyle=":", alpha=0.6)

    # 2. The XOR Conundrum (Linear Inseparability)
    ax1 = axes[1]
    ax1.set_title("2. The XOR Conundrum\n(Minsky & Papert 1969 Impossibility)", fontsize=13, fontweight="bold", pad=10)
    ax1.scatter([0, 1], [0, 1], color="crimson", s=110, marker="o", label="Class 0: (0,0), (1,1)")
    ax1.scatter([0, 1], [1, 0], color="forestgreen", s=140, marker="^", label="Class 1: (0,1), (1,0)")
    # Draw attempt lines
    ax1.plot(x_vals, 0.5 - x_vals, 'k:', lw=1.8, label="Candidate Line 1")
    ax1.plot(x_vals, 1.5 - x_vals, 'k-.', lw=1.8, label="Candidate Line 2")
    ax1.text(0.5, 0.5, "NO single linear hyperplane\ncan separate classes!", ha="center", va="center",
             fontsize=11, fontweight="bold", color="darkred",
             bbox=dict(boxstyle="round,pad=0.3", fc="#ffeeee", ec="darkred", lw=1.2))
    ax1.set_xlim(-0.2, 1.3)
    ax1.set_ylim(-0.2, 1.3)
    ax1.set_xlabel("$x_1$", fontsize=12, fontweight="bold")
    ax1.set_ylabel("$x_2$", fontsize=12, fontweight="bold")
    ax1.legend(frameon=True, fontsize=10, loc="upper right", framealpha=0.9, edgecolor="gray")
    ax1.grid(True, linestyle=":", alpha=0.6)

    # 3. 2-Layer MLP Solving XOR via Feature Space Transformation
    ax2 = axes[2]
    ax2.set_title("3. MLP Solution via Latent Space\n$h_1 = \\operatorname{OR}(x), h_2 = \\operatorname{NAND}(x)$", fontsize=13, fontweight="bold", pad=10)
    # Latent space: (h1, h2) for inputs:
    # (0,0) -> h1=0, h2=1 (XOR=0)
    # (1,1) -> h1=1, h2=0 (XOR=0)
    # (0,1) -> h1=1, h2=1 (XOR=1)
    # (1,0) -> h1=1, h2=1 (XOR=1)
    ax2.scatter([0, 1], [1, 0], color="crimson", s=110, marker="o", label="Class 0 in Hidden Space")
    ax2.scatter([1], [1], color="forestgreen", s=160, marker="^", label="Class 1: (0,1) & (1,0) Coincide")
    # Separation line h1 + h2 = 1.5
    h_vals = np.linspace(-0.2, 1.4, 100)
    ax2.plot(h_vals, 1.5 - h_vals, 'g-', lw=2.8, label="Output Layer Boundary\n$h_1 + h_2 = 1.5$")
    ax2.text(0.5, 0.4, "Linearly Separable in\nHidden Space $\\mathbf{h}$!", ha="center", fontsize=11, fontweight="bold",
             color="darkgreen", bbox=dict(boxstyle="round,pad=0.3", fc="#eef9ee", ec="green", lw=1.2))
    ax2.set_xlim(-0.2, 1.3)
    ax2.set_ylim(-0.2, 1.3)
    ax2.set_xlabel("Hidden Unit $h_1$ (OR)", fontsize=12, fontweight="bold")
    ax2.set_ylabel("Hidden Unit $h_2$ (NAND)", fontsize=12, fontweight="bold")
    ax2.legend(frameon=True, fontsize=10, loc="lower left", framealpha=0.9, edgecolor="gray")
    ax2.grid(True, linestyle=":", alpha=0.6)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig01_early_neurons_and_xor.png"), dpi=180, facecolor="white")
    plt.close()

# =========================================================================
# Figure 2: Activation Functions & Vanishing Gradient Profiles
# =========================================================================
def fig02_activations_and_gradients():
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))
    z = np.linspace(-5, 5, 300)

    # 1. Activation Output Curves
    ax0 = axes[0]
    ax0.set_title("1. Activation Functions $f(z)$", fontsize=13, fontweight="bold", pad=10)
    sig = 1.0 / (1.0 + np.exp(-z))
    tanh = np.tanh(z)
    relu = np.maximum(0, z)
    lrelu = np.where(z > 0, z, 0.1 * z)

    ax0.plot(z, sig, 'r-', lw=2.5, label=r"Sigmoid $\sigma(z) \in [0, 1]$")
    ax0.plot(z, tanh, 'b-', lw=2.5, label=r"Tanh $\tanh(z) \in [-1, 1]$")
    ax0.plot(z, relu, 'g-', lw=2.8, label=r"ReLU $\max(0, z)$")
    ax0.plot(z, lrelu, 'm--', lw=2.0, label=r"Leaky ReLU ($\alpha=0.1$)")
    ax0.axhline(0, color="gray", ls=":", lw=1)
    ax0.axvline(0, color="gray", ls=":", lw=1)
    ax0.set_ylim(-1.2, 3.5)
    ax0.set_xlabel("Input Pre-activation $z$", fontsize=12, fontweight="bold")
    ax0.set_ylabel("Activation $f(z)$", fontsize=12, fontweight="bold")
    ax0.legend(frameon=True, fontsize=10, loc="upper left", framealpha=0.9, edgecolor="gray")
    ax0.grid(True, linestyle=":", alpha=0.5)

    # 2. Derivative Profiles & Gradient Saturation
    ax1 = axes[1]
    ax1.set_title("2. Derivative Profiles $f'(z)$\n(Vanishing Gradient Trigger)", fontsize=13, fontweight="bold", pad=10)
    sig_grad = sig * (1.0 - sig)
    tanh_grad = 1.0 - tanh**2
    relu_grad = np.where(z > 0, 1.0, 0.0)
    lrelu_grad = np.where(z > 0, 1.0, 0.1)

    ax1.plot(z, sig_grad, 'r-', lw=2.5, label=r"$\sigma'(z) \leq 0.25$ (Severe Decay)")
    ax1.plot(z, tanh_grad, 'b-', lw=2.5, label=r"$\tanh'(z) \leq 1.0$ (Saturates)")
    ax1.plot(z, relu_grad, 'g-', lw=2.8, label="ReLU $f'(z) = 1$ ($z>0$)")
    ax1.plot(z, lrelu_grad, 'm--', lw=2.0, label="Leaky ReLU $f'(z) = 0.1$ ($z<0$)")
    ax1.axhline(0.25, color="red", ls=":", alpha=0.6, label="Max Sigmoid Grad (0.25)")
    ax1.set_ylim(-0.1, 1.15)
    ax1.set_xlabel("Input Pre-activation $z$", fontsize=12, fontweight="bold")
    ax1.set_ylabel("First Derivative $f'(z)$", fontsize=12, fontweight="bold")
    ax1.legend(frameon=True, fontsize=10, loc="upper right", framealpha=0.9, edgecolor="gray")
    ax1.grid(True, linestyle=":", alpha=0.5)

    # 3. Vanishing Gradient Across Network Depth (Cumulative Multiplications)
    ax2 = axes[2]
    ax2.set_title(r"3. Gradient Magnitude Decay Across Depth\n$\prod_{l=1}^L \frac{\partial a^{(l)}}{\partial z^{(l)}}$", fontsize=13, fontweight="bold", pad=10)
    depths = np.arange(1, 13)
    # Max gradient for sigmoid is 0.25, tanh is 1.0 (mean ~ 0.5 under normal init), ReLU is 1.0
    grad_decay_sig = (0.25) ** depths
    grad_decay_tanh = (0.50) ** depths
    grad_decay_relu = np.ones_like(depths, dtype=float)

    ax2.semilogy(depths, grad_decay_sig, 'r-o', lw=2.5, markersize=6, label="Sigmoid: Vanishes $\\to 10^{-7}$")
    ax2.semilogy(depths, grad_decay_tanh, 'b-s', lw=2.5, markersize=6, label="Tanh: Rapid Attenuation")
    ax2.semilogy(depths, grad_decay_relu, 'g-^', lw=2.8, markersize=7, label="ReLU: Constant Gradient Flow (1.0)")
    ax2.set_xlabel("Layer Depth (Backprop Steps)", fontsize=12, fontweight="bold")
    ax2.set_ylabel("Backpropagated Gradient Scale", fontsize=12, fontweight="bold")
    ax2.legend(frameon=True, fontsize=10, loc="lower left", framealpha=0.9, edgecolor="gray")
    ax2.grid(True, which="both", linestyle=":", alpha=0.5)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig02_activations_and_gradients.png"), dpi=180, facecolor="white")
    plt.close()

# =========================================================================
# Figure 3: Backpropagation Computational Graph & Chain Rule Flow
# =========================================================================
def fig03_backpropagation_computational_graph():
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # 1. Forward Pass Pipeline Diagram
    ax0 = axes[0]
    ax0.set_title("1. Forward Propagation (Graph Flow)", fontsize=13, fontweight="bold", pad=10)
    # Draw boxes
    boxes_fwd = [
        ("Input\n$a^{(l-1)}$", 0.1, 0.5),
        ("Affine Layer\n$z^{(l)} = W^{(l)} a^{(l-1)} + b^{(l)}$", 0.45, 0.5),
        ("Activation\n$a^{(l)} = f(z^{(l)})$", 0.82, 0.5)
    ]
    for text, cx, cy in boxes_fwd:
        rect = plt.Rectangle((cx-0.12, cy-0.18), 0.24, 0.36, facecolor="#eef3ff", edgecolor="#224488", lw=2, zorder=2)
        ax0.add_patch(rect)
        ax0.text(cx, cy, text, ha="center", va="center", fontsize=11, fontweight="bold", color="#112255", zorder=3)

    # Forward arrows
    ax0.annotate("", xy=(0.33, 0.5), xytext=(0.22, 0.5),
                 arrowprops=dict(arrowstyle="->", color="darkblue", lw=3.0))
    ax0.annotate("", xy=(0.70, 0.5), xytext=(0.57, 0.5),
                 arrowprops=dict(arrowstyle="->", color="darkblue", lw=3.0))
    ax0.annotate("", xy=(1.05, 0.5), xytext=(0.94, 0.5),
                 arrowprops=dict(arrowstyle="->", color="darkblue", lw=3.0))
    ax0.text(0.275, 0.55, "$a^{(l-1)}$", ha="center", fontsize=11, color="navy", fontweight="bold")
    ax0.text(0.635, 0.55, "$z^{(l)}$", ha="center", fontsize=11, color="navy", fontweight="bold")
    ax0.text(1.0, 0.55, "$a^{(l)}$", ha="center", fontsize=11, color="navy", fontweight="bold")
    ax0.set_xlim(-0.05, 1.1)
    ax0.set_ylim(0.1, 0.9)
    ax0.axis("off")

    # 2. Backward Pass Pipeline & Error Redistribution
    ax1 = axes[1]
    ax1.set_title("2. Backward Pass & Multivariate Chain Rule", fontsize=13, fontweight="bold", pad=10)
    boxes_bwd = [
        ("Output Error\n$\\delta^{(l+1)} = \\frac{\\partial \\mathcal{L}}{\\partial z^{(l+1)}}$", 0.85, 0.5),
        ("Linear Projection\n$(W^{(l)})^T \\delta^{(l+1)}$", 0.50, 0.5),
        ("Current Error\n$\\delta^{(l)} = (W^{(l)})^T \\delta^{(l+1)} \\odot f'(z^{(l)})$", 0.15, 0.5)
    ]
    for text, cx, cy in boxes_bwd:
        rect = plt.Rectangle((cx-0.14, cy-0.18), 0.28, 0.36, facecolor="#fff2f2", edgecolor="#aa2222", lw=2, zorder=2)
        ax1.add_patch(rect)
        ax1.text(cx, cy, text, ha="center", va="center", fontsize=10.5, fontweight="bold", color="#661111", zorder=3)

    # Backward arrows
    ax1.annotate("", xy=(0.64, 0.5), xytext=(0.71, 0.5),
                 arrowprops=dict(arrowstyle="->", color="darkred", lw=3.0))
    ax1.annotate("", xy=(0.29, 0.5), xytext=(0.36, 0.5),
                 arrowprops=dict(arrowstyle="->", color="darkred", lw=3.0))
    ax1.text(0.675, 0.56, "$(W^{(l)})^T$", ha="center", fontsize=11, color="darkred", fontweight="bold")
    ax1.text(0.325, 0.56, "$\\odot f'(z^{(l)})$", ha="center", fontsize=11, color="darkred", fontweight="bold")

    # Weight and bias gradients callout
    grad_box = ("Weight Gradient: $\\nabla_{W^{(l)}} \\mathcal{L} = \\delta^{(l+1)} (a^{(l)})^T$\n"
                "Bias Gradient:   $\\nabla_{b^{(l)}} \\mathcal{L} = \\delta^{(l+1)}$")
    ax1.text(0.50, 0.18, grad_box, ha="center", va="center", fontsize=11, fontweight="bold", color="#331111",
             bbox=dict(boxstyle="round,pad=0.4", fc="#fff9e6", ec="#cc9900", lw=1.5))

    ax1.set_xlim(-0.02, 1.02)
    ax1.set_ylim(0.05, 0.95)
    ax1.axis("off")

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig03_backpropagation_computational_graph.png"), dpi=180, facecolor="white")
    plt.close()

# =========================================================================
# Figure 4: Optimization Landscape & Gradient Descent Trajectories (2x2 Grid)
# =========================================================================
def fig04_optimization_and_momentum():
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Pathological Ravine Function: f(x, y) = 0.5 * x^2 + 10 * y^2
    x = np.linspace(-4, 4, 200)
    y = np.linspace(-2, 2, 200)
    X, Y = np.meshgrid(x, y)
    Z = 0.5 * X**2 + 10.0 * Y**2

    # 1. Standard Gradient Descent in Ravine (Oscillations)
    ax0 = axes[0, 0]
    ax0.set_title("1. Standard Gradient Descent\n(Severe Transverse Oscillation)", fontsize=13, fontweight="bold")
    ax0.contour(X, Y, Z, levels=np.logspace(-1, 2.5, 12), cmap="Blues_r", alpha=0.7)
    # Simulate SGD path
    x_curr, y_curr = -3.5, 1.6
    lr = 0.09
    path_x, path_y = [x_curr], [y_curr]
    for _ in range(16):
        gx = x_curr
        gy = 20.0 * y_curr
        x_curr -= lr * gx
        y_curr -= lr * gy
        path_x.append(x_curr)
        path_y.append(y_curr)
    ax0.plot(path_x, path_y, 'r-o', lw=2.2, markersize=5, label="GD Trajectory")
    ax0.plot(0, 0, 'g*', markersize=14, label="Optimum (0, 0)")
    ax0.set_xlabel("$w_1$ (Flat Curvature)", fontsize=11, fontweight="bold")
    ax0.set_ylabel("$w_2$ (Steep Curvature)", fontsize=11, fontweight="bold")
    ax0.legend(frameon=True, fontsize=10, loc="lower right", framealpha=0.9, edgecolor="gray")
    ax0.grid(True, linestyle=":", alpha=0.5)

    # 2. Classical Momentum (Damped Oscillations, Faster Longitudinal Travel)
    ax1 = axes[0, 1]
    ax1.set_title("2. Classical Polyak Momentum\n(Damped Lateral Jitter, Accelerated Axis)", fontsize=13, fontweight="bold")
    ax1.contour(X, Y, Z, levels=np.logspace(-1, 2.5, 12), cmap="Blues_r", alpha=0.7)
    x_curr, y_curr = -3.5, 1.6
    vx, vy = 0.0, 0.0
    gamma = 0.75
    lr = 0.04
    path_x_m, path_y_m = [x_curr], [y_curr]
    for _ in range(16):
        gx = x_curr
        gy = 20.0 * y_curr
        vx = gamma * vx + lr * gx
        vy = gamma * vy + lr * gy
        x_curr -= vx
        y_curr -= vy
        path_x_m.append(x_curr)
        path_y_m.append(y_curr)
    ax1.plot(path_x_m, path_y_m, 'b-s', lw=2.2, markersize=5, label="Momentum Trajectory")
    ax1.plot(0, 0, 'g*', markersize=14, label="Optimum (0, 0)")
    ax1.set_xlabel("$w_1$", fontsize=11, fontweight="bold")
    ax1.set_ylabel("$w_2$", fontsize=11, fontweight="bold")
    ax1.legend(frameon=True, fontsize=10, loc="lower right", framealpha=0.9, edgecolor="gray")
    ax1.grid(True, linestyle=":", alpha=0.5)

    # 3. Nesterov Accelerated Gradient (NAG) Look-Ahead
    ax2 = axes[1, 0]
    ax2.set_title("3. Nesterov Accelerated Gradient (NAG)\n('Look Before You Leap' Step)", fontsize=13, fontweight="bold")
    # Vector illustration
    ax2.plot([0, 2], [0, 1], 'b-', lw=3, label=r"Momentum Step $\gamma v_{t-1}$")
    ax2.plot([2, 2.5], [1, 0.2], 'r--', lw=3, label=r"Grad at Look-ahead $\nabla \mathcal{L}(\theta - \gamma v)$")
    ax2.plot([0, 2.5], [0, 0.2], 'g-', lw=3.5, label="Actual Combined Update $v_t$")
    ax2.plot(2, 1, 'ks', markersize=9)
    ax2.text(2.05, 1.05, "Look-Ahead Point\n$\\tilde{\\theta}_t = \\theta_t - \\gamma v_{t-1}$", fontsize=10, fontweight="bold", color="navy")
    ax2.plot(0, 0, 'ko', markersize=9)
    ax2.text(-0.1, -0.15, "Current $\\theta_t$", fontsize=11, fontweight="bold")
    ax2.set_xlim(-0.5, 3.2)
    ax2.set_ylim(-0.4, 1.8)
    ax2.set_xlabel("Parameter Space $\\theta_1$", fontsize=11, fontweight="bold")
    ax2.set_ylabel("Parameter Space $\\theta_2$", fontsize=11, fontweight="bold")
    ax2.legend(frameon=True, fontsize=10, loc="upper left", framealpha=0.9, edgecolor="gray")
    ax2.grid(True, linestyle=":", alpha=0.5)

    # 4. Adam Optimizer: Adaptive Moment Trajectory
    ax3 = axes[1, 1]
    ax3.set_title("4. Adam (Adaptive Moments)\n(Coordinate-Wise Rescaling via $\\sqrt{r_t}$)", fontsize=13, fontweight="bold")
    ax3.contour(X, Y, Z, levels=np.logspace(-1, 2.5, 12), cmap="Blues_r", alpha=0.7)
    x_curr, y_curr = -3.5, 1.6
    m_x, m_y = 0.0, 0.0
    v_x, v_y = 0.0, 0.0
    beta1, beta2 = 0.9, 0.999
    alpha_adam = 0.25
    eps = 1e-8
    path_x_a, path_y_a = [x_curr], [y_curr]
    for t in range(1, 17):
        gx = x_curr
        gy = 20.0 * y_curr
        m_x = beta1 * m_x + (1 - beta1) * gx
        m_y = beta1 * m_y + (1 - beta1) * gy
        v_x = beta2 * v_x + (1 - beta2) * (gx**2)
        v_y = beta2 * v_y + (1 - beta2) * (gy**2)
        m_x_hat = m_x / (1 - beta1**t)
        m_y_hat = m_y / (1 - beta1**t)
        v_x_hat = v_x / (1 - beta2**t)
        v_y_hat = v_y / (1 - beta2**t)
        x_curr -= alpha_adam * m_x_hat / (np.sqrt(v_x_hat) + eps)
        y_curr -= alpha_adam * m_y_hat / (np.sqrt(v_y_hat) + eps)
        path_x_a.append(x_curr)
        path_y_a.append(y_curr)
    ax3.plot(path_x_a, path_y_a, 'm-^', lw=2.2, markersize=5, label="Adam Trajectory")
    ax3.plot(0, 0, 'g*', markersize=14, label="Optimum (0, 0)")
    ax3.set_xlabel("$w_1$", fontsize=11, fontweight="bold")
    ax3.set_ylabel("$w_2$", fontsize=11, fontweight="bold")
    ax3.legend(frameon=True, fontsize=10, loc="lower right", framealpha=0.9, edgecolor="gray")
    ax3.grid(True, linestyle=":", alpha=0.5)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig04_optimization_and_momentum.png"), dpi=180, facecolor="white")
    plt.close()

# =========================================================================
# Figure 5: Regularization Geometry: L1 vs L2 Unit Balls & Sparsity
# =========================================================================
def fig05_regularization_l1_vs_l2():
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))

    # Shared Loss Contours (Elliptical Unconstrained Minimum at (1.8, 1.6))
    w1 = np.linspace(-2.2, 2.8, 200)
    w2 = np.linspace(-2.2, 2.8, 200)
    W1, W2 = np.meshgrid(w1, w2)
    L_unconstrained = 1.5 * (W1 - 1.8)**2 + 0.8 * (W2 - 1.6)**2

    # 1. L1 Regularization (Diamond Ball -> Sharp Axis Intersect)
    ax0 = axes[0]
    ax0.set_title("1. $L_1$ Lasso Regularization\n(Diamond Contour $\\to$ Sparse $w_2=0$)", fontsize=13, fontweight="bold", pad=10)
    ax0.contour(W1, W2, L_unconstrained, levels=[0.2, 0.8, 1.8, 3.2, 5.0, 7.5], cmap="Blues_r", alpha=0.6)
    # Draw L1 diamond: |w1| + |w2| <= 1.2
    c_l1 = 1.2
    poly_l1 = plt.Polygon([[c_l1, 0], [0, c_l1], [-c_l1, 0], [0, -c_l1]], facecolor="#ffdddd", edgecolor="crimson", lw=2.5, alpha=0.5, label=r"$L_1$ Ball $\|w\|_1 \leq C$")
    ax0.add_patch(poly_l1)
    ax0.plot(c_l1, 0, 'ro', markersize=12, label="Sparse Optimum $(C, 0)$")
    ax0.plot(1.8, 1.6, 'k*', markersize=14, label="Unconstrained $\\theta^*$")
    ax0.axhline(0, color="black", lw=1.2)
    ax0.axvline(0, color="black", lw=1.2)
    ax0.set_xlim(-2.0, 2.6)
    ax0.set_ylim(-2.0, 2.6)
    ax0.set_aspect("equal")
    ax0.set_xlabel("$w_1$", fontsize=12, fontweight="bold")
    ax0.set_ylabel("$w_2$", fontsize=12, fontweight="bold")
    ax0.legend(frameon=True, fontsize=10, loc="lower left", framealpha=0.9, edgecolor="gray")
    ax0.grid(True, linestyle=":", alpha=0.5)

    # 2. L2 Regularization (Circular Ball -> Smooth Uniform Shrinkage)
    ax1 = axes[1]
    ax1.set_title("2. $L_2$ Ridge Regularization / Weight Decay\n(Circular Contour $\\to$ Smooth Shrinkage)", fontsize=13, fontweight="bold", pad=10)
    ax1.contour(W1, W2, L_unconstrained, levels=[0.2, 0.8, 1.8, 3.2, 5.0, 7.5], cmap="Blues_r", alpha=0.6)
    # Draw L2 circle: w1^2 + w2^2 <= 1.1^2
    r_l2 = 1.1
    circle_l2 = plt.Circle((0, 0), r_l2, facecolor="#ddeeff", edgecolor="royalblue", lw=2.5, alpha=0.5, label=r"$L_2$ Ball $\|w\|_2 \leq C$")
    ax1.add_patch(circle_l2)
    # Tangent point around (0.85, 0.70)
    ax1.plot(0.85, 0.70, 'bo', markersize=12, label="Constrained Min ($w_1, w_2 > 0$)")
    ax1.plot(1.8, 1.6, 'k*', markersize=14, label="Unconstrained $\\theta^*$")
    ax1.axhline(0, color="black", lw=1.2)
    ax1.axvline(0, color="black", lw=1.2)
    ax1.set_xlim(-2.0, 2.6)
    ax1.set_ylim(-2.0, 2.6)
    ax1.set_aspect("equal")
    ax1.set_xlabel("$w_1$", fontsize=12, fontweight="bold")
    ax1.set_ylabel("$w_2$", fontsize=12, fontweight="bold")
    ax1.legend(frameon=True, fontsize=10, loc="lower left", framealpha=0.9, edgecolor="gray")
    ax1.grid(True, linestyle=":", alpha=0.5)

    # 3. Lp Norms Shape Progression (p = 0.5, 1, 2, infinity)
    ax2 = axes[2]
    ax2.set_title("3. Geometric $L_p$ Unit Balls\n($p \\to 0$ Pinches Axes $\\to$ Sparsity)", fontsize=13, fontweight="bold", pad=10)
    t_vals = np.linspace(-1, 1, 400)
    # p = 0.5: |x|^0.5 + |y|^0.5 = 1 -> y = (1 - |x|^0.5)^2
    y_p05_pos = (1.0 - np.sqrt(np.abs(t_vals)))**2
    ax2.plot(t_vals, y_p05_pos, 'purple', lw=2.2, label="$p=0.5$ (Non-convex)")
    ax2.plot(t_vals, -y_p05_pos, 'purple', lw=2.2)
    # p = 1: diamond
    ax2.plot([1, 0, -1, 0, 1], [0, 1, 0, -1, 0], 'r-', lw=2.5, label="$p=1.0$ (Lasso, Diamond)")
    # p = 2: circle
    theta = np.linspace(0, 2*np.pi, 200)
    ax2.plot(np.cos(theta), np.sin(theta), 'b-', lw=2.5, label="$p=2.0$ (Ridge, Sphere)")
    # p = inf: square
    ax2.plot([-1, 1, 1, -1, -1], [-1, -1, 1, 1, -1], 'k--', lw=2.2, label=r"$p=\infty$ (Box)")
    ax2.axhline(0, color="black", lw=1)
    ax2.axvline(0, color="black", lw=1)
    ax2.set_xlim(-1.5, 1.5)
    ax2.set_ylim(-1.5, 1.5)
    ax2.set_aspect("equal")
    ax2.set_xlabel("$w_1$", fontsize=12, fontweight="bold")
    ax2.set_ylabel("$w_2$", fontsize=12, fontweight="bold")
    ax2.legend(frameon=True, fontsize=9.5, loc="lower left", framealpha=0.9, edgecolor="gray")
    ax2.grid(True, linestyle=":", alpha=0.5)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig05_regularization_l1_vs_l2.png"), dpi=180, facecolor="white")
    plt.close()

# =========================================================================
# Figure 6: Dropout Architecture & Weight Symmetry Breaking
# =========================================================================
def fig06_dropout_and_symmetry():
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))

    # 1. Standard Fully Connected Layer
    ax0 = axes[0]
    ax0.set_title("1. Standard Dense Layer\n(Dense Co-Adaptation Risk)", fontsize=13, fontweight="bold", pad=10)
    y_in = [0.2, 0.4, 0.6, 0.8]
    y_out = [0.3, 0.5, 0.7]
    for yi in y_in:
        ax0.plot(0.2, yi, 'bo', markersize=12)
    for yo in y_out:
        ax0.plot(0.8, yo, 'go', markersize=14)
    for yi in y_in:
        for yo in y_out:
            ax0.plot([0.2, 0.8], [yi, yo], 'k-', alpha=0.3, lw=1.2)
    ax0.text(0.2, 0.08, "Input Layer $l$\n(All Active)", ha="center", fontsize=10.5, fontweight="bold")
    ax0.text(0.8, 0.08, "Hidden Layer $l+1$\n(All Active)", ha="center", fontsize=10.5, fontweight="bold")
    ax0.set_xlim(0.0, 1.0)
    ax0.set_ylim(0.0, 0.95)
    ax0.axis("off")

    # 2. Dropout Training Pass (Randomly Zeroed Neurons p=0.5)
    ax1 = axes[1]
    ax1.set_title("2. Dropout Training ($p=0.5$)\n(Decouples Neurons, Prevents Co-adaptation)", fontsize=13, fontweight="bold", pad=10)
    active_in = [True, False, True, True]
    active_out = [False, True, True]
    for idx, (yi, act) in enumerate(zip(y_in, active_in)):
        col = "royalblue" if act else "gray"
        ax1.plot(0.2, yi, 'o', color=col, markersize=12)
        if not act:
            ax1.plot(0.2, yi, 'rx', markersize=14, markeredgewidth=2.5)
    for idx, (yo, act) in enumerate(zip(y_out, active_out)):
        col = "forestgreen" if act else "gray"
        ax1.plot(0.8, yo, 'o', color=col, markersize=14)
        if not act:
            ax1.plot(0.8, yo, 'rx', markersize=16, markeredgewidth=2.5)
    for yi, act_i in zip(y_in, active_in):
        for yo, act_o in zip(y_out, active_out):
            if act_i and act_o:
                ax1.plot([0.2, 0.8], [yi, yo], 'b-', alpha=0.8, lw=2.0)
            else:
                ax1.plot([0.2, 0.8], [yi, yo], 'k:', alpha=0.15, lw=1.0)
    ax1.text(0.5, 0.08, "Ensemble of $2^N$ Sub-Networks\nInverted Dropout Scaling: $a / (1-p)$", ha="center",
             fontsize=10.5, fontweight="bold", color="darkred")
    ax1.set_xlim(0.0, 1.0)
    ax1.set_ylim(0.0, 0.95)
    ax1.axis("off")

    # 3. Symmetry Breaking Pathology: Constant Initial Weights
    ax2 = axes[2]
    ax2.set_title("3. Symmetry Breaking Pathology\n(Constant Initialization $W_{ij} = c$)", fontsize=13, fontweight="bold", pad=10)
    epochs = np.arange(1, 20)
    # If initialized to identical constants, both neurons evolve along identical trajectory!
    w_neuron1 = 0.5 + 0.3 * np.log(epochs)
    w_neuron2 = 0.5 + 0.3 * np.log(epochs) # exactly identical
    # Random init diverges to learn complementary features
    w_rand1 = 0.4 + 0.5 * np.log(epochs) + np.random.normal(0, 0.02, len(epochs))
    w_rand2 = -0.3 - 0.4 * np.log(epochs) + np.random.normal(0, 0.02, len(epochs))

    ax2.plot(epochs, w_neuron1, 'r-', lw=3.0, label="Neuron 1 (Constant Init)")
    ax2.plot(epochs, w_neuron2, 'r--', lw=3.0, label="Neuron 2 (Locked Symmetrically)")
    ax2.plot(epochs, w_rand1, 'g-', lw=2.2, label="Neuron 1 (Random Init $\\to$ Feature A)")
    ax2.plot(epochs, w_rand2, 'b-', lw=2.2, label="Neuron 2 (Random Init $\\to$ Feature B)")
    ax2.text(10, 0.1, "Constant weights receive\nIDENTICAL gradients $\\nabla W$\nand never diverge!",
             ha="center", fontsize=10.5, fontweight="bold", color="darkred",
             bbox=dict(boxstyle="round,pad=0.3", fc="#fff2f2", ec="red", lw=1.2))
    ax2.set_xlabel("Training Epochs", fontsize=12, fontweight="bold")
    ax2.set_ylabel("Learned Weight Value", fontsize=12, fontweight="bold")
    ax2.legend(frameon=True, fontsize=9.5, loc="upper left", framealpha=0.9, edgecolor="gray")
    ax2.grid(True, linestyle=":", alpha=0.5)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig06_dropout_and_symmetry.png"), dpi=180, facecolor="white")
    plt.close()

# =========================================================================
# Figure 7: Weight Initialization Variance Scaling (Xavier vs He/Kaiming)
# =========================================================================
def fig07_weight_initialization_variance():
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))
    L = 10
    layers = np.arange(1, L + 1)

    # 1. Activation Variance Collapse (Small Random Init: Var = 0.01)
    ax0 = axes[0]
    ax0.set_title("1. Small Random Init ($\\mathrm{Var} = 0.01$)\n(Forward Signal Vanishes to Zero)", fontsize=13, fontweight="bold", pad=10)
    var_small = (0.5) ** layers # n * Var(w) < 1
    ax0.semilogy(layers, var_small, 'r-o', lw=2.5, markersize=7, label="Activation Var $\\operatorname{Var}(a^{(l)})$")
    ax0.axhline(1.0, color="gray", ls="--", label="Target Unit Variance (1.0)")
    ax0.set_ylim(1e-4, 2.0)
    ax0.set_xlabel("Layer Depth $l$", fontsize=12, fontweight="bold")
    ax0.set_ylabel("Activation Variance", fontsize=12, fontweight="bold")
    ax0.legend(frameon=True, fontsize=10, loc="lower left", framealpha=0.9, edgecolor="gray")
    ax0.grid(True, which="both", linestyle=":", alpha=0.5)

    # 2. Activation Variance Explosion (Large Random Init: Var = 1.0)
    ax1 = axes[1]
    ax1.set_title("2. Large Random Init ($\\mathrm{Var} = 1.0$)\n(Forward Signal Explodes to Inf)", fontsize=13, fontweight="bold", pad=10)
    var_large = (1.8) ** layers # n * Var(w) > 1
    ax1.semilogy(layers, var_large, 'm-s', lw=2.5, markersize=7, label="Activation Var $\\operatorname{Var}(a^{(l)})$")
    ax1.axhline(1.0, color="gray", ls="--", label="Target Unit Variance (1.0)")
    ax1.set_ylim(0.5, 500.0)
    ax1.set_xlabel("Layer Depth $l$", fontsize=12, fontweight="bold")
    ax1.set_ylabel("Activation Variance", fontsize=12, fontweight="bold")
    ax1.legend(frameon=True, fontsize=10, loc="upper left", framealpha=0.9, edgecolor="gray")
    ax1.grid(True, which="both", linestyle=":", alpha=0.5)

    # 3. Variance Preservation: Xavier vs He/Kaiming
    ax2 = axes[2]
    ax2.set_title("3. Variance-Preserving Schemes\n(Xavier for Tanh, He for ReLU)", fontsize=13, fontweight="bold", pad=10)
    # Under He init with ReLU: Var(w) = 2/n_in -> preserves Var(a) = 1.0
    var_he = np.ones_like(layers, dtype=float) + np.random.normal(0, 0.04, len(layers))
    # Under Xavier with ReLU: misses factor of 2 -> decays by 0.5 per layer
    var_xavier_relu = (0.5) ** layers

    ax2.plot(layers, var_he, 'g-^', lw=3.0, markersize=8, label="He / Kaiming (ReLU): $\\operatorname{Var}(w) = 2/n_{\\text{in}}$")
    ax2.plot(layers, var_xavier_relu, 'b--o', lw=2.5, markersize=7, label="Xavier (on ReLU): Decays by $0.5^l$")
    ax2.axhline(1.0, color="black", ls=":", lw=1.5, label="Ideal Preservation (1.0)")
    ax2.set_ylim(0.0, 1.4)
    ax2.set_xlabel("Layer Depth $l$", fontsize=12, fontweight="bold")
    ax2.set_ylabel("Layer Output Variance", fontsize=12, fontweight="bold")
    ax2.legend(frameon=True, fontsize=10, loc="center right", framealpha=0.9, edgecolor="gray")
    ax2.grid(True, linestyle=":", alpha=0.5)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig07_weight_initialization_variance.png"), dpi=180, facecolor="white")
    plt.close()

# =========================================================================
# Figure 8: Batch Normalization Mini-Batch Standardization & Scale/Shift
# =========================================================================
def fig08_batch_normalization_pipeline():
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))

    # 1. Unnormalized Activation Distribution Across Channels
    ax0 = axes[0]
    ax0.set_title("1. Internal Covariate Shift\n(Drifting Activations Across Batches)", fontsize=13, fontweight="bold", pad=10)
    np.random.seed(12)
    b1 = np.random.normal(loc=4.5, scale=2.2, size=1000)
    b2 = np.random.normal(loc=-3.0, scale=0.8, size=1000)
    b3 = np.random.normal(loc=1.2, scale=3.5, size=1000)
    sns.kdeplot(b1, ax=ax0, color="crimson", lw=2.2, label=r"Mini-batch 1 ($\mu=4.5, \sigma=2.2$)")
    sns.kdeplot(b2, ax=ax0, color="navy", lw=2.2, label=r"Mini-batch 2 ($\mu=-3.0, \sigma=0.8$)")
    sns.kdeplot(b3, ax=ax0, color="forestgreen", lw=2.2, label=r"Mini-batch 3 ($\mu=1.2, \sigma=3.5$)")
    ax0.set_xlim(-8, 12)
    ax0.set_xlabel("Pre-Activation Value $x_i$", fontsize=12, fontweight="bold")
    ax0.set_ylabel("Probability Density", fontsize=12, fontweight="bold")
    ax0.legend(frameon=True, fontsize=9.5, loc="upper right", framealpha=0.9, edgecolor="gray")
    ax0.grid(True, linestyle=":", alpha=0.5)

    # 2. Standardized Distribution (Mean=0, Variance=1)
    ax1 = axes[1]
    ax1.set_title(r"2. Mini-Batch Standardized $\hat{x}_i$\n$\hat{x}_i = (x_i - \mu_{\mathcal{B}}) / \sqrt{\sigma_{\mathcal{B}}^2 + \epsilon}$", fontsize=13, fontweight="bold", pad=10)
    b1_norm = (b1 - np.mean(b1)) / np.std(b1)
    b2_norm = (b2 - np.mean(b2)) / np.std(b2)
    b3_norm = (b3 - np.mean(b3)) / np.std(b3)
    sns.kdeplot(b1_norm, ax=ax1, color="crimson", lw=2.2, label="Batch 1 Normalized")
    sns.kdeplot(b2_norm, ax=ax1, color="navy", lw=2.2, label="Batch 2 Normalized")
    sns.kdeplot(b3_norm, ax=ax1, color="forestgreen", lw=2.2, label="Batch 3 Normalized")
    ax1.set_xlim(-4, 4)
    ax1.set_xlabel(r"Standardized Score $\hat{x}_i$", fontsize=12, fontweight="bold")
    ax1.set_ylabel("Probability Density", fontsize=12, fontweight="bold")
    ax1.legend(frameon=True, fontsize=10, loc="upper right", framealpha=0.9, edgecolor="gray")
    ax1.grid(True, linestyle=":", alpha=0.5)

    # 3. Learnable Scale & Shift (Restoring Expressive Capacity)
    ax2 = axes[2]
    ax2.set_title(r"3. Learnable Affine Scale & Shift\n$y_i = \gamma \hat{x}_i + \beta$ (Restores Representation)", fontsize=13, fontweight="bold", pad=10)
    gamma, beta = 1.8, 0.5
    y_scaled = gamma * b1_norm + beta
    sns.kdeplot(b1_norm, ax=ax2, color="gray", ls="--", lw=2.0, label="Standardized ($\\mu=0, \\sigma=1$)")
    sns.kdeplot(y_scaled, ax=ax2, color="purple", lw=3.0, label=f"Restored: $\\gamma={gamma}, \\beta={beta}$")
    ax2.text(0, 0.35, "Allows network to undo\nnormalization if linear\nidentity is optimal!",
             ha="center", fontsize=10.5, fontweight="bold", color="purple",
             bbox=dict(boxstyle="round,pad=0.3", fc="#fdf5ff", ec="purple", lw=1.2))
    ax2.set_xlim(-4, 6)
    ax2.set_xlabel("Output Activation $y_i$", fontsize=12, fontweight="bold")
    ax2.set_ylabel("Probability Density", fontsize=12, fontweight="bold")
    ax2.legend(frameon=True, fontsize=10, loc="upper right", framealpha=0.9, edgecolor="gray")
    ax2.grid(True, linestyle=":", alpha=0.5)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig08_batch_normalization_pipeline.png"), dpi=180, facecolor="white")
    plt.close()

if __name__ == "__main__":
    print("Generating Figure 1: Early Neurons & XOR Crisis...")
    fig01_early_neurons_and_xor()
    print("Generating Figure 2: Activations & Vanishing Gradients...")
    fig02_activations_and_gradients()
    print("Generating Figure 3: Backpropagation Computational Graph...")
    fig03_backpropagation_computational_graph()
    print("Generating Figure 4: Optimization & Momentum...")
    fig04_optimization_and_momentum()
    print("Generating Figure 5: Regularization L1 vs L2...")
    fig05_regularization_l1_vs_l2()
    print("Generating Figure 6: Dropout & Symmetry Breaking...")
    fig06_dropout_and_symmetry()
    print("Generating Figure 7: Weight Initialization Variance...")
    fig07_weight_initialization_variance()
    print("Generating Figure 8: Batch Normalization Pipeline...")
    fig08_batch_normalization_pipeline()
    print(f"All 8 figures successfully generated in {OUT_DIR}!")
