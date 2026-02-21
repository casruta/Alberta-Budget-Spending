"""
Generate a publication-quality infographic of Alberta's fiscal performance (2000-01 to 2024-25).
Dark theme consistent with the sibling project's visual language.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import numpy as np

# ── Paths ────────────────────────────────────────────────────────────────────
PROJECT = Path(r"C:\Users\Casper Ruta\Desktop\Kacper Ruta 2026\Alberta Budget Analysis")
PLOTS = PROJECT / "plots"
PLOTS.mkdir(exist_ok=True)

# ── Colour palette ───────────────────────────────────────────────────────────
BG         = "#0D1117"
CARD_BG    = "#161B22"
GRID       = "#21262D"
TEXT       = "#C9D1D9"
MUTED      = "#8B949E"
SURPLUS_C  = "#56D364"   # green
DEFICIT_C  = "#F85149"   # red
REVENUE_C  = "#58A6FF"   # blue
EXPENSE_C  = "#FFB703"   # amber
RESOURCE_C = "#BD93F9"   # purple

# Party colours (background shading)
PC_C  = "#1B4F8A"   # Progressive Conservative – blue
NDP_C = "#D4610A"   # NDP – orange
UCP_C = "#1A6B3C"   # UCP – green

# ── Data ─────────────────────────────────────────────────────────────────────
labels = [
    "00-01","01-02","02-03","03-04","04-05","05-06","06-07","07-08",
    "08-09","09-10","10-11","11-12","12-13","13-14","14-15",
    "15-16","16-17","17-18","18-19","19-20","20-21",
    "21-22","22-23","23-24","24-25",
]

revenue = np.array([
    25527,21926,22662,25887,29328,35542,38017,38169,
    39325,39512,38976,43395,42544,49434,49481,
    42619,42293,47295,49572,46224,43137,
    68322,75982,74738,82469,
], dtype=float)

expense = np.array([
    18956,20845,20529,21751,24153,26991,29507,33588,
    40256,39988,41238,43509,45643,49736,48366,
    49061,53077,55318,56283,58376,60099,
    64407,64498,70453,74149,
], dtype=float)

surplus = np.array([
    6571,1081,2133,4136,5175,8551,8510,4581,
    -931,-476,-2262,-114,-3099,-302,1115,
    -6442,-10784,-8023,-6711,-12152,-16962,
    3915,11484,4285,8320,
], dtype=float)

resource_rev = np.array([
    10586,6227,7130,7676,9744,14347,12260,11024,
    11915,6768,8428,11636,7779,9578,8948,
    2789,3097,4980,5429,5937,3091,
    16170,25242,19287,21986,
], dtype=float)

# Party spans (index ranges, inclusive)
party_spans = [
    (0, 14, "PC",  PC_C),    # 2000-01 to 2014-15
    (15, 18, "NDP", NDP_C),  # 2015-16 to 2018-19
    (19, 24, "UCP", UCP_C),  # 2019-20 to 2024-25
]

n = len(labels)
x = np.arange(n)


def billions(val, _):
    """Format tick as $XXB."""
    return f"${val / 1000:.0f}B"


def add_party_shading(ax, alpha=0.08):
    """Add subtle background shading by governing party."""
    for start, end, _, colour in party_spans:
        ax.axvspan(start - 0.5, end + 0.5, color=colour, alpha=alpha, zorder=0)


# ═══════════════════════════════════════════════════════════════════════════════
#  FIGURE: 3-panel stacked infographic
# ═══════════════════════════════════════════════════════════════════════════════
fig, (ax1, ax2, ax3) = plt.subplots(
    3, 1, figsize=(22, 20),
    gridspec_kw={"height_ratios": [3, 3, 2], "hspace": 0.28},
)
fig.patch.set_facecolor(BG)

# ── PANEL 1: Revenue vs Expense ──────────────────────────────────────────────
ax1.set_facecolor(CARD_BG)
add_party_shading(ax1, alpha=0.10)

bar_w = 0.35
bars_rev = ax1.bar(x - bar_w / 2, revenue, bar_w, color=REVENUE_C, alpha=0.85,
                   label="Total Revenue", zorder=3, edgecolor="none")
bars_exp = ax1.bar(x + bar_w / 2, expense, bar_w, color=EXPENSE_C, alpha=0.85,
                   label="Total Expense", zorder=3, edgecolor="none")

ax1.set_ylabel("$ Millions", color=TEXT, fontsize=13, fontweight="bold")
ax1.set_title("Alberta Government Revenue vs. Expense",
              color=TEXT, fontsize=18, fontweight="bold", pad=16, loc="left")
ax1.set_xticks(x)
ax1.set_xticklabels(labels, rotation=45, ha="right", fontsize=9, color=MUTED)
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(billions))
ax1.tick_params(colors=MUTED, labelsize=10)
ax1.set_xlim(-0.7, n - 0.3)
ax1.grid(axis="y", color=GRID, linewidth=0.5, zorder=0)
ax1.spines[:].set_visible(False)

# Add key value labels on tallest bars
peak_rev_idx = np.argmax(revenue)
peak_exp_idx = np.argmax(expense)
ax1.annotate(f"${revenue[peak_rev_idx]/1000:.1f}B",
             xy=(peak_rev_idx - bar_w/2, revenue[peak_rev_idx]),
             ha="center", va="bottom", color=REVENUE_C, fontsize=9, fontweight="bold")
ax1.annotate(f"${expense[peak_exp_idx]/1000:.1f}B",
             xy=(peak_exp_idx + bar_w/2, expense[peak_exp_idx]),
             ha="center", va="bottom", color=EXPENSE_C, fontsize=9, fontweight="bold")

leg1 = ax1.legend(loc="upper left", fontsize=11, framealpha=0.3,
                  facecolor=CARD_BG, edgecolor=GRID, labelcolor=TEXT)

# ── PANEL 2: Surplus / Deficit ───────────────────────────────────────────────
ax2.set_facecolor(CARD_BG)
add_party_shading(ax2, alpha=0.10)

colours = [SURPLUS_C if v >= 0 else DEFICIT_C for v in surplus]
bars_sd = ax2.bar(x, surplus, 0.7, color=colours, alpha=0.9, zorder=3, edgecolor="none")

ax2.axhline(0, color=MUTED, linewidth=1, zorder=2)
ax2.set_ylabel("$ Millions", color=TEXT, fontsize=13, fontweight="bold")
ax2.set_title("Surplus / (Deficit)",
              color=TEXT, fontsize=18, fontweight="bold", pad=16, loc="left")
ax2.set_xticks(x)
ax2.set_xticklabels(labels, rotation=45, ha="right", fontsize=9, color=MUTED)
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(billions))
ax2.tick_params(colors=MUTED, labelsize=10)
ax2.set_xlim(-0.7, n - 0.3)
ax2.grid(axis="y", color=GRID, linewidth=0.5, zorder=0)
ax2.spines[:].set_visible(False)

# Annotate extremes
worst_idx = np.argmin(surplus)
best_idx = np.argmax(surplus)
ax2.annotate(f"$(  {abs(surplus[worst_idx])/1000:.1f}B)",
             xy=(worst_idx, surplus[worst_idx]),
             xytext=(worst_idx, surplus[worst_idx] - 2500),
             ha="center", va="top", color=DEFICIT_C, fontsize=10, fontweight="bold",
             arrowprops=dict(arrowstyle="-", color=DEFICIT_C, lw=0.8))
ax2.annotate(f"$+{surplus[best_idx]/1000:.1f}B",
             xy=(best_idx, surplus[best_idx]),
             xytext=(best_idx, surplus[best_idx] + 2000),
             ha="center", va="bottom", color=SURPLUS_C, fontsize=10, fontweight="bold",
             arrowprops=dict(arrowstyle="-", color=SURPLUS_C, lw=0.8))

# Legend for surplus/deficit
s_patch = mpatches.Patch(color=SURPLUS_C, alpha=0.9, label="Surplus")
d_patch = mpatches.Patch(color=DEFICIT_C, alpha=0.9, label="Deficit")
ax2.legend(handles=[s_patch, d_patch], loc="lower left", fontsize=11,
           framealpha=0.3, facecolor=CARD_BG, edgecolor=GRID, labelcolor=TEXT)

# ── PANEL 3: Resource Revenue + Party Timeline ──────────────────────────────
ax3.set_facecolor(CARD_BG)
add_party_shading(ax3, alpha=0.10)

ax3.fill_between(x, resource_rev, color=RESOURCE_C, alpha=0.25, zorder=2)
ax3.plot(x, resource_rev, color=RESOURCE_C, linewidth=2.5, zorder=3,
         marker="o", markersize=5, markerfacecolor=RESOURCE_C, markeredgecolor=BG)

ax3.set_ylabel("$ Millions", color=TEXT, fontsize=13, fontweight="bold")
ax3.set_title("Non-Renewable Resource Revenue",
              color=TEXT, fontsize=18, fontweight="bold", pad=16, loc="left")
ax3.set_xticks(x)
ax3.set_xticklabels(labels, rotation=45, ha="right", fontsize=9, color=MUTED)
ax3.yaxis.set_major_formatter(mticker.FuncFormatter(billions))
ax3.tick_params(colors=MUTED, labelsize=10)
ax3.set_xlim(-0.7, n - 0.3)
ax3.grid(axis="y", color=GRID, linewidth=0.5, zorder=0)
ax3.spines[:].set_visible(False)

# Annotate peak
peak_r = np.argmax(resource_rev)
ax3.annotate(f"${resource_rev[peak_r]/1000:.1f}B\n({labels[peak_r]})",
             xy=(peak_r, resource_rev[peak_r]),
             xytext=(peak_r - 2, resource_rev[peak_r] + 3000),
             ha="center", va="bottom", color=RESOURCE_C, fontsize=10, fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=RESOURCE_C, lw=1.2))

# Annotate trough
trough_r = 15  # 2015-16
ax3.annotate(f"${resource_rev[trough_r]/1000:.1f}B\n({labels[trough_r]})",
             xy=(trough_r, resource_rev[trough_r]),
             xytext=(trough_r + 2, resource_rev[trough_r] + 5000),
             ha="center", va="bottom", color=DEFICIT_C, fontsize=10, fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=DEFICIT_C, lw=1.2))

# Party legend at bottom
pc_patch  = mpatches.Patch(color=PC_C,  alpha=0.35, label="Progressive Conservative")
ndp_patch = mpatches.Patch(color=NDP_C, alpha=0.35, label="NDP")
ucp_patch = mpatches.Patch(color=UCP_C, alpha=0.35, label="UCP")
ax3.legend(handles=[pc_patch, ndp_patch, ucp_patch], loc="upper left",
           fontsize=11, framealpha=0.3, facecolor=CARD_BG, edgecolor=GRID,
           labelcolor=TEXT, title="Governing Party", title_fontsize=11)
ax3.legend_.get_title().set_color(TEXT)

# ── Suptitle + footer ────────────────────────────────────────────────────────
fig.suptitle("Alberta Fiscal Performance  |  2000-01 to 2024-25",
             color=TEXT, fontsize=24, fontweight="bold", y=0.98)

fig.text(0.5, 0.008,
         "Source: Government of Alberta Budget & Annual Report PDFs  |  "
         "FY 2000-08: Fiscal Plan basis  |  FY 2008-25: Consolidated Financial Statements basis  |  "
         "All figures in millions CAD",
         ha="center", va="bottom", fontsize=9, color=MUTED, style="italic")

# ── Save ─────────────────────────────────────────────────────────────────────
out = PLOTS / "alberta_fiscal_summary_infographic.png"
fig.savefig(out, dpi=200, bbox_inches="tight", facecolor=BG, edgecolor="none")
plt.close(fig)
print(f"Saved: {out}")
