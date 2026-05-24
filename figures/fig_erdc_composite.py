"""Composite figure: ERDC TIN-CCM results (Rehrer et al. 2022).

Combines original Figures 7 and 9 from ERDC/GRL TR-22-5 into a single
stacked composite for the Defence Technology article.

Panel A: TIN CCM overlays for four terrain archetypes (top)
Panel B: TIN vs SAGE raster comparison -- Mostly Flat AOI detail (bottom)
"""
from __future__ import annotations

from pathlib import Path
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

from utils_nato import FIG_WIDTH_IN, PALETTE, save_fig, set_mpl_style

HERE = Path(__file__).resolve().parent
IMG_FIG7 = HERE / "fig_erdc_fig7_tin_ccm.png"
IMG_FIG9 = HERE / "fig_erdc_fig9_comparison.png"


def _crop(img_path, top=0.0, bottom=1.0, left=0.0, right=1.0):
    img = Image.open(img_path)
    w, h = img.size
    return np.array(img.crop((int(w*left), int(h*top),
                               int(w*right), int(h*bottom))))


def build():
    set_mpl_style()

    img7 = _crop(IMG_FIG7, top=0.12)
    img9 = _crop(IMG_FIG9, top=0.17)

    h7, w7 = img7.shape[:2]
    h9, w9 = img9.shape[:2]

    fig_w = FIG_WIDTH_IN * 1.35
    aspect7 = h7 / w7
    aspect9 = h9 / w9

    panel_a_h = fig_w * aspect7
    panel_b_h = fig_w * aspect9 * 0.55

    total_h = panel_a_h + panel_b_h + 1.0

    fig = plt.figure(figsize=(fig_w, total_h))

    gs = fig.add_gridspec(2, 1,
                          height_ratios=[panel_a_h, panel_b_h],
                          hspace=0.12,
                          left=0.02, right=0.98,
                          top=1 - 0.35/total_h,
                          bottom=0.02)

    axA = fig.add_subplot(gs[0])
    axA.imshow(img7, interpolation="lanczos")
    axA.axis("off")
    axA.set_title("A)  TIN CCM overlays for four terrain archetypes",
                   fontsize=9, fontweight="bold", color=PALETTE["text"],
                   loc="left", pad=6)

    axB = fig.add_subplot(gs[1])
    axB.imshow(img9, interpolation="lanczos")
    axB.axis("off")
    axB.set_title("B)  TIN (left) vs SAGE raster (right) -- "
                   "Mostly Flat AOI detail (0.25 km x 0.25 km)",
                   fontsize=9, fontweight="bold", color=PALETTE["text"],
                   loc="left", pad=6)

    fig.suptitle("Cross-Country Mobility via Triangulated Irregular "
                 "Networks (Rehrer et al., 2022)",
                 fontsize=10, fontweight="bold", color=PALETTE["text"],
                 y=1 - 0.08/total_h)

    save_fig(fig, "fig_erdc_composite")


if __name__ == "__main__":
    build()
