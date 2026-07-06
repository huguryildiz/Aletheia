#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Draw the network topology and the routing solution from solutions.csv.

Echoes the paper's own network figure (IEEE doc 11143186): base station (star),
sensor nodes, and the data-flow edges of the k-connected routing, coloured by path
index l. Regenerates the exact instance model.py solved (same SEED).

Run:  python3 plot.py            ->  writes network.svg (and network.png)
"""

import csv
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import model as M

PATH_COLORS = {1: "#2563eb", 2: "#dc2626", 3: "#16a34a"}   # l = 1 / 2 / 3


def load_flows(path="solutions.csv"):
    """Aggregate solutions.csv into per-(i,j,l) total flow (summed over sources k)."""
    agg = defaultdict(float)
    with open(path) as fh:
        for row in csv.DictReader(fh):
            i, j, l = int(row["i"]), int(row["j"]), int(row["l"])
            agg[(i, j, l)] += float(row["val"])
    return agg


def main():
    xs, ys, _ = M.node_positions(M.SEED)
    flows = load_flows()
    k_req = M.k_requirement()

    fig, ax = plt.subplots(figsize=(7.5, 6))

    # flow edges, coloured by path, width ~ log(flow)
    for (i, j, l), val in flows.items():
        if val < 1.0:
            continue
        ax.annotate("", xy=(xs[j], ys[j]), xytext=(xs[i], ys[i]),
                    arrowprops=dict(arrowstyle="-|>", color=PATH_COLORS.get(l, "#888"),
                                    lw=0.6 + 0.5 * (val ** 0.5) / 6, alpha=0.75,
                                    shrinkA=9, shrinkB=9))

    # nodes: BS as a star, k=2 sources filled, k=1 sources lighter
    ax.scatter(xs[0], ys[0], marker="*", s=420, color="#111", zorder=5, label="base station")
    for k in M.W:
        crit = k_req[k] == M.K_HIGH
        ax.scatter(xs[k], ys[k], s=130, zorder=5,
                   color="#b91c1c" if crit else "#f59e0b",
                   edgecolors="#333", linewidths=0.6)
        ax.annotate(str(k), (xs[k], ys[k]), ha="center", va="center",
                    fontsize=8, color="white", zorder=6, fontweight="bold")

    # legend
    handles = [
        plt.Line2D([], [], marker="*", color="w", markerfacecolor="#111",
                   markersize=16, label="base station (0)"),
        plt.Line2D([], [], marker="o", color="w", markerfacecolor="#b91c1c",
                   markersize=10, label=f"critical source (k={M.K_HIGH})"),
        plt.Line2D([], [], marker="o", color="w", markerfacecolor="#f59e0b",
                   markersize=10, label=f"ordinary source (k={M.K_LOW})"),
        plt.Line2D([], [], color=PATH_COLORS[1], lw=2, label="path l=1"),
        plt.Line2D([], [], color=PATH_COLORS[2], lw=2, label="path l=2"),
    ]
    ax.legend(handles=handles, loc="center left", bbox_to_anchor=(1.02, 0.5),
              fontsize=8, framealpha=0.95)

    # annotate the base station so it is not mistaken for a node
    ax.annotate("BS (0)", (xs[0], ys[0]), textcoords="offset points", xytext=(8, 8),
                fontsize=9, fontweight="bold")

    ax.set_xlabel("x (km)"); ax.set_ylabel("y (km)")
    ax.set_title(f"UWSN non-uniform k-connectivity — routing solution "
                 f"(seed {M.SEED}, τ={49052.18:.0f})", fontsize=10)
    ax.set_aspect("equal", "box"); ax.grid(alpha=0.15)
    fig.tight_layout()
    fig.savefig("network.svg")
    fig.savefig("network.png", dpi=150)
    print("wrote network.svg and network.png")


if __name__ == "__main__":
    main()
