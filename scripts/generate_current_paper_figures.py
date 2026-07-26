"""Regenerate the current paper Figures 2--4 as vector PDFs.

These figures use protocol-matched, checkpoint-specific values reported in the
paper. The crossover curves use the saved seed-42 CQG-Single Top-200 output and
TIGER beam-200 output; every plotted depth is measured rather than interpolated.
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
    ks = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 150])
    panels = [
        ("Q1 (rare, 193 users)",
         [0.062176, 0.119171, 0.145078, 0.165803, 0.186528, 0.191710, 0.212435, 0.243523, 0.284974, 0.295337, 0.316062, 0.357513],
         [0.067358, 0.103627, 0.134715, 0.165803, 0.191710, 0.202073, 0.222798, 0.259067, 0.264249, 0.279793, 0.305699, 0.316062]),
        ("Q2 (581 users)",
         [0.177281, 0.271945, 0.323580, 0.361446, 0.395869, 0.432014, 0.450947, 0.480207, 0.492255, 0.511188, 0.550775, 0.583477],
         [0.175559, 0.254733, 0.313253, 0.352840, 0.387263, 0.423408, 0.442341, 0.464716, 0.485370, 0.497418, 0.521515, 0.547332]),
        ("Q3 (1,322 users)",
         [0.251891, 0.344932, 0.420575, 0.467474, 0.503026, 0.531014, 0.562784, 0.584720, 0.600605, 0.618759, 0.642965, 0.673979],
         [0.243570, 0.341150, 0.407716, 0.450832, 0.481089, 0.509077, 0.536309, 0.558245, 0.580182, 0.597579, 0.625567, 0.642965]),
        ("Q4 (popular, 3,944 users)",
         [0.355477, 0.475406, 0.547921, 0.597363, 0.633114, 0.662018, 0.686359, 0.703854, 0.718560, 0.733519, 0.757099, 0.784229],
         [0.347363, 0.461207, 0.530680, 0.583418, 0.627028, 0.650862, 0.679513, 0.702079, 0.720335, 0.732759, 0.760396, 0.786004]),
    ]
    fig, axes = plt.subplots(2, 2, figsize=(11.5, 4.7), sharex=False)
    blue, gold = "#0072B2", "#E69F00"
    for idx, (ax, (title, cqg, tiger)) in enumerate(zip(axes.flat, panels)):
        ax.plot(ks, cqg, "-o", color=blue, lw=2.0, ms=3.8, label="CQG-Single")
        ax.plot(ks, tiger, "-s", color=gold, lw=2.0, ms=3.8, label="TIGER")
        ax.set_title(title, fontsize=11)
        ax.set_xticks([10, 50, 100, 150])
        ax.set_xlabel("Cutoff $K$")
        ax.grid(axis="y", alpha=0.13)
        ax.spines[["top", "right"]].set_visible(False)
        if idx in (0, 2):
            ax.set_ylabel("Recall")

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
