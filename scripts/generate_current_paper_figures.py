"""Regenerate the current paper Figures 2--4 as vector PDFs.

These figures use the checkpoint-specific values currently reported in the
paper. Figure 3 will be regenerated again after the queued beam-200/Top-200
dense-depth evaluation completes.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Figures"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "axes.labelcolor": "black",
        "axes.edgecolor": "black",
        "xtick.color": "black",
        "ytick.color": "black",
        "text.color": "black",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
)


def save(fig, name):
    fig.savefig(OUT / name, bbox_inches="tight", format="pdf")
    plt.close(fig)


def figure2():
    labels = ["Q1 (rare)\n$n$=192", "Q2\n$n$=582", "Q3\n$n$=1,321", "Q4 (popular)\n$n$=3,945"]
    values = [24.0, 47.1, 56.1, 70.8]
    x = np.arange(len(values))
    fig, ax = plt.subplots(figsize=(7.2, 5.4))
    bars = ax.bar(x, values, width=0.48, color="#E69F00")
    ax.text(
        0.985,
        0.96,
        "TIGER-style SID (beam width 100)",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=15,
        fontweight="bold",
        color="black",
    )
    ax.set_ylabel("Beam Search Reachability (%)", fontsize=16, color="black")
    ax.set_xticks(x, labels, fontsize=13, color="black")
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.tick_params(axis="y", labelsize=13, colors="black")
    ax.set_ylim(0, 100)
    ax.grid(axis="y", alpha=0.15)
    ax.set_axisbelow(True)
    ax.legend([bars], ["TIGER"], loc="upper left", frameon=False, fontsize=14)
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 2.2,
            f"{value:.1f}%",
            ha="center",
            va="bottom",
            fontsize=14,
            fontweight="bold",
            color="black",
        )
    ax.spines[["top", "right"]].set_visible(False)
    save(fig, "fig3_reachability.pdf")


def figure3():
    ks = np.array([10, 50, 90])
    panels = [
        ("Q1 (rare, 192 users)", [0.0521, 0.1615, 0.2396], [0.0677, 0.1875, 0.2396], 0.240),
        ("Q2 (582 users)", [0.1615, 0.4107, 0.5017], [0.1753, 0.3900, 0.4691], 0.471),
        ("Q3 (1,321 users)", [0.2506, 0.5026, 0.5927], [0.2438, 0.4807, 0.5579], 0.561),
        ("Q4 (popular, 3,945 users)", [0.3546, 0.6347, 0.7234], [0.3473, 0.6269, 0.7049], 0.708),
    ]
    fig, axes = plt.subplots(2, 2, figsize=(11.5, 4.7), sharex=False)
    blue, gold = "#0072B2", "#E69F00"
    for idx, (ax, (title, cqg, tiger, ceiling)) in enumerate(zip(axes.flat, panels)):
        ax.plot(ks, cqg, "-o", color=blue, lw=2.3, ms=6, label="CQG-Single")
        ax.plot(ks, tiger, "-s", color=gold, lw=2.3, ms=6, label="TIGER")
        ax.axhline(ceiling, color="#E67E22", lw=1.2, ls=(0, (5, 4)), alpha=0.9)
        ax.text(
            11,
            ceiling + 0.012,
            f"Target support ({ceiling * 100:.1f}%)",
            color="#D95F02",
            fontsize=8,
            fontstyle="italic",
        )
        ax.set_title(title, fontsize=11)
        ax.set_xticks(ks, [f"R@{k}" for k in ks])
        ax.grid(axis="y", alpha=0.13)
        ax.spines[["top", "right"]].set_visible(False)
        if idx in (0, 2):
            ax.set_ylabel("Recall")

    tie_ax = axes[0, 0]
    tie_x, tie_y = 90, 0.2396
    tie_ax.scatter(
        [tie_x],
        [tie_y],
        s=180,
        facecolors="none",
        edgecolors="black",
        linewidths=2.8,
        zorder=8,
    )
    tie_ax.annotate(
        "TIE: R@90 = 0.2396",
        xy=(tie_x, tie_y),
        xytext=(48, 0.108),
        arrowprops=dict(arrowstyle="->", color="black", lw=1.8),
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=1.8),
        fontsize=9,
        fontweight="bold",
        color="black",
        zorder=9,
    )
    axes[0, 0].text(24, 0.09, "TIGER +30%", color=gold, fontsize=9, fontweight="bold")
    axes[0, 1].text(24, 0.205, "TIGER +9%", color=gold, fontsize=9, fontweight="bold")
    axes[0, 1].text(80, 0.525, "CQG +7%", color=blue, fontsize=9, fontweight="bold")
    axes[1, 0].text(80, 0.62, "CQG +6%", color=blue, fontsize=9, fontweight="bold")
    axes[1, 1].text(80, 0.76, "CQG +3%", color=blue, fontsize=9, fontweight="bold")
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=2, frameon=False, bbox_to_anchor=(0.5, -0.02))
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    save(fig, "fig2_crossover.pdf")


def figure4():
    labels = [
        "v3\nDual",
        "v4\nDual",
        "v5h\nMSE-warm",
        "v6\nQuery-only",
        "v7\nText-aware",
        "Scratch\nCQG-Rec",
    ]
    values = [0.003, 0.0, 0.0, 0.044, 0.212, 0.242]
    colors = ["#D95F02", "#8C8C8C", "#8C8C8C", "#984807", "#984807", "#E69F00"]
    x = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(7.0, 4.6))
    bars = ax.bar(x, values, width=0.64, color=colors, edgecolor="#3B3B3B", linewidth=1.2)
    ax.axhline(0.242, color="#3B94C5", lw=2, ls="--")
    ax.text(4.15, 0.253, "Scratch baseline", color="#0072B2", ha="center", fontsize=12)
    for index in (3, 4, 5):
        ax.text(x[index], values[index] + 0.006, f"{values[index]:.3f}", ha="center", fontsize=11)
    for index, text in enumerate(["I-I=0.93", "I-I=0.93", "I-I=0.994"]):
        ax.text(
            x[index],
            0.119,
            text,
            ha="center",
            va="center",
            color="white",
            fontweight="bold",
            fontsize=8.5,
            bbox=dict(boxstyle="round,pad=0.18", fc="#E67E22", ec="#333333", lw=1.3),
        )
    ax.text(1.0, 0.018, "Item embedding\ncollapse", color="#D95F02", ha="center", fontstyle="italic")
    ax.text(3.25, 0.072, "Loss-metric\ndecoupling", color="#8C3F0A", ha="center", fontstyle="italic")
    ax.set_ylabel("Test R@10", fontsize=13)
    ax.set_xticks(x, labels)
    for index, label in enumerate(ax.get_xticklabels()):
        label.set_rotation(28)
        label.set_ha("right")
        label.set_rotation_mode("anchor")
        label.set_y(-0.015 if index % 2 == 0 else -0.045)
    ax.tick_params(axis="x", labelsize=10, pad=5)
    ax.tick_params(axis="y", labelsize=10)
    ax.set_ylim(0, 0.28)
    ax.spines[["top", "right"]].set_visible(False)
    fig.subplots_adjust(bottom=0.31, left=0.12, right=0.98, top=0.96)
    save(fig, "fig4_llm_diagnostic.pdf")


if __name__ == "__main__":
    figure2()
    figure3()
    figure4()
