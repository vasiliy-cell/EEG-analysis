"""
Compare alpha-band power (8-13 Hz) between runs R01 and R02.

Nothing is recomputed here: analysis.py is imported as-is and every value
plotted below (spectra, band mask, alpha powers) is read straight out of it.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch

import analysis

# ---------------------------------------------------------------- palette
SURFACE = "#fcfcfb"
INK     = "#0b0b0b"
INK_2   = "#52514e"
MUTED   = "#898781"
GRID    = "#e1e0d9"
AXIS    = "#c3c2b7"
S1      = "#2a78d6"   # R01
S2      = "#eb6834"   # R02

V2_TO_UV2 = 1e12      # V^2 -> uV^2, otherwise the labels read 1.6e-10

plt.rcParams.update({
    "font.family": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 10,
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "text.color": INK,
    "axes.labelcolor": INK_2,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
})

# ------------------------------------------------- values from analysis.py
f01, P01 = analysis.f_R01, analysis.Pxx_R01 * V2_TO_UV2
f02, P02 = analysis.f_R02, analysis.Pxx_R02 * V2_TO_UV2
alpha = analysis.mask

a01, a02 = analysis.alpha_power_R01, analysis.alpha_power_R02
a01_uv, a02_uv = a01 * V2_TO_UV2, a02 * V2_TO_UV2
ratio = a02_uv / a01_uv

# ---------------------------------------------------------------- figure
fig = plt.figure(figsize=(12, 5.2))
gs = fig.add_gridspec(1, 2, width_ratios=[2.3, 1], wspace=0.26,
                      left=0.06, right=0.97, top=0.78, bottom=0.13)
ax1, ax2 = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])

fig.text(0.06, 0.93, "Alpha rhythm (8–13 Hz): R01 vs R02",
         fontsize=16, fontweight="bold", color=INK)
fig.text(0.06, 0.875,
         f"Subject S001 · channel {analysis.raw_R01.ch_names[0].strip('.')} · "
         f"Welch PSD, Hann window of 320 samples, 50 % overlap · fs = 160 Hz",
         fontsize=10, color=INK_2)


def style(ax):
    ax.set_axisbelow(True)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(AXIS)
        ax.spines[side].set_linewidth(1)


# --- panel A: power spectral density ------------------------------------
style(ax1)
# Below 1 Hz there is drift/DC an order of magnitude above everything else:
# it has nothing to do with alpha and would flatten the whole scale if shown.
band = (f01 >= 1) & (f01 <= 30)
inner = (f01 >= 3) & (f01 <= 30)
ymax = max(P01[inner].max(), P02[inner].max())

ax1.axvspan(8, 13, color=MUTED, alpha=0.10, lw=0, zorder=0)
ax1.fill_between(f01[alpha], 0, P01[alpha], color=S1, alpha=0.16, lw=0)
ax1.fill_between(f02[alpha], 0, P02[alpha], color=S2, alpha=0.16, lw=0)

ax1.plot(f01[band], P01[band], color=S1, lw=2,
         solid_capstyle="round", label="R01", zorder=3)
ax1.plot(f02[band], P02[band], color=S2, lw=2,
         solid_capstyle="round", label="R02", zorder=3)

# in-band peaks — coloured marker plus a label in a text token
for f_, P, color, name, off, ha in ((f02, P02, S2, "R02", (-12, 8), "right"),
                                    (f01, P01, S1, "R01", (12, 6), "left")):
    i = np.argmax(np.where(alpha, P, -np.inf))
    ax1.plot(f_[i], P[i], "o", ms=8, color=color, mec=SURFACE, mew=2, zorder=4)
    ax1.annotate(f"{name}: peak {f_[i]:.1f} Hz", (f_[i], P[i]),
                 textcoords="offset points", xytext=off, ha=ha,
                 fontsize=9, color=INK_2, zorder=5)

ax1.set_xlim(1, 30)
ax1.set_ylim(0, ymax * 1.28)
ax1.set_xlabel("Frequency, Hz")
ax1.set_ylabel("Power spectral density, µV²/Hz")
ax1.set_title("Spectrum: the shaded area is what integrates into alpha power",
              fontsize=11, color=INK_2, loc="left", pad=10)
ax1.text(10.5, ymax * 1.24, "8–13 Hz", ha="center", va="top",
         fontsize=9, color=MUTED)
ax1.legend(frameon=False, loc="upper right", fontsize=10,
           handlelength=1.6, labelcolor=INK).set_zorder(5)

# --- panel B: the scalars themselves ------------------------------------
style(ax2)


def rounded_bar(ax, x, height, width, color, r_frac=0.035):
    """Bar with rounded top corners, anchored flat to the baseline."""
    r = min(width * 0.18, height * r_frac)
    l, rt = x - width / 2, x + width / 2
    verts = [(l, 0), (l, height - r), (l, height), (l + r, height),
             (rt - r, height), (rt, height), (rt, height - r), (rt, 0), (l, 0)]
    codes = [Path.MOVETO, Path.LINETO, Path.CURVE3, Path.CURVE3,
             Path.LINETO, Path.CURVE3, Path.CURVE3, Path.LINETO, Path.CLOSEPOLY]
    ax.add_patch(PathPatch(Path(verts, codes), fc=color, ec="none", zorder=3))


xs, vals = [0, 1], [a01_uv, a02_uv]
top = max(vals)

for x, v, c in zip(xs, vals, (S1, S2)):
    rounded_bar(ax2, x, v, 0.52, c)
    ax2.text(x, v + top * 0.035, f"{v:.1f}", ha="center", va="bottom",
             fontsize=15, fontweight="bold", color=INK)

y = top * 1.14
ax2.annotate("", xy=(1, y), xytext=(0, y),
             arrowprops=dict(arrowstyle="<->", color=MUTED, lw=1.2,
                             shrinkA=0, shrinkB=0))
ax2.text(0.5, y + top * 0.025, f"×{ratio:.2f}", ha="center", va="bottom",
         fontsize=11, fontweight="bold", color=INK)

ax2.set_xticks(xs)
ax2.set_xticklabels(["R01\neyes open", "R02\neyes closed"],
                    fontsize=10, color=INK_2)
ax2.tick_params(axis="x", length=0, pad=8)
ax2.set_xlim(-0.62, 1.62)
ax2.set_ylim(0, top * 1.32)
ax2.set_ylabel("Alpha power (8–13 Hz), µV²")
ax2.set_title("Integral of the spectrum over the alpha band",
              fontsize=11, color=INK_2, loc="left", pad=10)

fig.text(0.06, 0.035,
         f"R02 / R01 = {ratio:.2f}  ·  raw values in V²: "
         f"R01 = {a01:.3e}, R02 = {a02:.3e}  (plotted as µV², × 1e12)  ·  "
         f"x-axis clipped at 1 Hz: below it sits drift, outside the alpha band",
         fontsize=9, color=MUTED)

plt.show()
