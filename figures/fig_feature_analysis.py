"""Figure: Feature analysis mosaic (two stacked heatmaps).

Panel A: R² between input features and DAMEPLAN labels per fraction
Panel B: |Pearson r| between embedding PCs and input features

LiDAR features excluded (not used in V2).
"""
from __future__ import annotations

import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from utils_nato import (FIG_WIDTH_IN, PALETTE, ANALISE_DIR, FRACTIONS,
                         FRACTION_TITLES, save_fig, set_mpl_style)

FEATURE_NAMES_ALL = [
    "elevation", "slope", "aspect_cos", "aspect_sin", "curvature",
    "tpi", "tri", "roughness", "B02", "B03", "B04", "B08",
    "NDVI", "NDWI", "water_mask", "lidar_avail", "lidar_elev",
]
SKIP = {"lidar_avail", "lidar_elev"}
FEATURE_NAMES = [f for f in FEATURE_NAMES_ALL if f not in SKIP]
FEATURE_INDICES = [i for i, f in enumerate(FEATURE_NAMES_ALL) if f not in SKIP]

FEATURE_LABELS = [
    "Elevation", "Slope", "Aspect cos", "Aspect sin", "Curvature",
    "TPI", "TRI", "Roughness", "B02", "B03", "B04", "B08",
    "NDVI", "NDWI", "Water mask",
]

N_PCS = 10
N_SAMPLE = 500_000


def load_d11():
    path = ANALISE_DIR / "13_label_audit" / "13_label_audit_results.json"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    d11 = data["D11_correlacao"]
    matrix = np.zeros((len(FRACTIONS), len(FEATURE_NAMES)))
    for i, frac in enumerate(FRACTIONS):
        for j, fname in enumerate(FEATURE_NAMES):
            entry = d11[frac].get(fname, {})
            matrix[i, j] = entry.get("r_squared", 0.0)
    return matrix


def load_pca_corr():
    from pathlib import Path
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler
    import torch

    from src.paths import EMBEDDINGS_256

    feat_path = ANALISE_DIR / "features_full.npz"
    emb_path = EMBEDDINGS_256

    feat_data = np.load(str(feat_path))
    features = feat_data["features"]

    emb_raw = torch.load(str(emb_path), map_location="cpu", weights_only=False)
    if isinstance(emb_raw, torch.Tensor):
        emb = emb_raw.float().numpy()
    elif isinstance(emb_raw, dict):
        emb = list(emb_raw.values())[0].float().numpy()
    else:
        emb = emb_raw.float().numpy()

    rng = np.random.default_rng(42)
    N = features.shape[0]
    idx = rng.choice(N, size=min(N_SAMPLE, N), replace=False)

    feat_sample = features[idx]
    emb_sample = emb[idx]

    scaler = StandardScaler()
    emb_scaled = scaler.fit_transform(emb_sample)
    pca = PCA(n_components=N_PCS, random_state=42)
    pcs_sample = pca.fit_transform(emb_scaled)
    del emb, emb_raw, emb_scaled

    matrix = np.zeros((N_PCS, len(FEATURE_NAMES)))
    for i in range(N_PCS):
        for j, fidx in enumerate(FEATURE_INDICES):
            r = np.corrcoef(pcs_sample[:, i], feat_sample[:, fidx])[0, 1]
            matrix[i, j] = r if np.isfinite(r) else 0.0
    return matrix


def build():
    set_mpl_style()
    print("[mosaic] Loading D11 (R2 feature->label)...")
    d11 = load_d11()
    print("[mosaic] Computing PCA correlations...")
    pca_corr = load_pca_corr()

    fig, (axA, axB) = plt.subplots(
        2, 1, figsize=(FIG_WIDTH_IN * 1.45, FIG_WIDTH_IN * 1.10),
        gridspec_kw={"height_ratios": [len(FRACTIONS), N_PCS], "hspace": 0.35},
    )

    # --- Panel A: R² feature → label ---
    imA = axA.imshow(d11, aspect="auto", cmap="YlOrRd", vmin=0, vmax=0.85)
    axA.set_yticks(range(len(FRACTIONS)))
    axA.set_yticklabels([FRACTION_TITLES[f] for f in FRACTIONS], fontsize=7.5)
    axA.set_xticks(range(len(FEATURE_LABELS)))
    axA.set_xticklabels([""] * len(FEATURE_LABELS))
    axA.set_title("A)  $R^2$ between input features and DAMEPLAN labels",
                   fontsize=9.5, fontweight="bold", color=PALETTE["text"],
                   loc="left", pad=6)
    cbA = fig.colorbar(imA, ax=axA, fraction=0.025, pad=0.02, shrink=0.95)
    cbA.ax.tick_params(labelsize=6.5)
    cbA.set_label("$R^2$", fontsize=7.5)

    for i in range(d11.shape[0]):
        for j in range(d11.shape[1]):
            v = d11[i, j]
            color = "white" if v > 0.45 else "black"
            axA.text(j, i, f"{v:.2f}", ha="center", va="center",
                     fontsize=5.8, color=color)

    # --- Panel B: |r| PCs vs features ---
    abs_corr = np.abs(pca_corr)
    imB = axB.imshow(abs_corr, aspect="auto", cmap="Blues", vmin=0, vmax=0.5)
    axB.set_yticks(range(N_PCS))
    axB.set_yticklabels([f"PC{i+1}" for i in range(N_PCS)], fontsize=7.5)
    axB.set_xticks(range(len(FEATURE_LABELS)))
    axB.set_xticklabels(FEATURE_LABELS, rotation=45, ha="right", fontsize=7)
    axB.set_title("B)  |Pearson $r$| between embedding PCs and input features",
                   fontsize=9.5, fontweight="bold", color=PALETTE["text"],
                   loc="left", pad=6)
    cbB = fig.colorbar(imB, ax=axB, fraction=0.025, pad=0.02, shrink=0.95)
    cbB.ax.tick_params(labelsize=6.5)
    cbB.set_label("|Pearson $r$|", fontsize=7.5)

    for i in range(abs_corr.shape[0]):
        for j in range(abs_corr.shape[1]):
            v = abs_corr[i, j]
            color = "white" if v > 0.30 else "black"
            axB.text(j, i, f"{v:.2f}", ha="center", va="center",
                     fontsize=5.3, color=color)

    save_fig(fig, "fig_feature_analysis")


if __name__ == "__main__":
    build()
