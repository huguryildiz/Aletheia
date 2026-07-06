#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Draw LoS probability vs distance for the correct UMa-AV model and the buggy UMi-AV mix,
from the same 3GPP TR 36.777 formulas model.py uses. Reproduces this example's figure:
the correct curve stays in line of sight; the wrong one quietly collapses (~10 dB at 1 km).

Run:  python3 plot.py     ->  writes los-probability.svg / .png
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import model as M

GOOD, BAD = "#16a34a", "#dc2626"


def curve(scenario):
    p1, d1 = M.LOS_COEFFS[scenario](M.H)
    xs = list(range(1, 4001, 10))
    return xs, [M.p_los(d, p1, d1) for d in xs]


def main():
    fig, ax = plt.subplots(figsize=(8, 5))
    xs_ok, ys_ok = curve("UMa-AV")
    xs_bad, ys_bad = curve("UMi-AV")
    ax.plot(xs_ok, ys_ok, color=GOOD, lw=2.2, label="UMa-AV — correct (stays in line of sight)")
    ax.plot(xs_bad, ys_bad, color=BAD, lw=2.2, ls="--", label="UMi-AV — the AI's mix (collapses)")

    # highlight the 1 km divergence: 0.85 vs 0.25
    p1o, d1o = M.LOS_COEFFS["UMa-AV"](M.H); p1b, d1b = M.LOS_COEFFS["UMi-AV"](M.H)
    yo, yb = M.p_los(1000, p1o, d1o), M.p_los(1000, p1b, d1b)
    ax.scatter([1000, 1000], [yo, yb], color=[GOOD, BAD], zorder=5, s=45)
    ax.annotate(f"at 1 km: {yo:.2f} → {yb:.2f}\n≈ 10 dB error · backwards",
                xy=(1000, (yo + yb) / 2), xytext=(1450, 0.62),
                fontsize=9, color=BAD,
                arrowprops=dict(arrowstyle="->", color="#888"))

    ax.set_xlabel("2D distance from base station (m)")
    ax.set_ylabel("LoS probability")
    ax.set_title("A2G LoS probability — mixing 3GPP scenarios (TR 36.777, UAV @ 100 m)",
                 fontsize=11)
    ax.set_ylim(0, 1.02); ax.grid(alpha=0.15); ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    fig.savefig("los-probability.svg"); fig.savefig("los-probability.png", dpi=150)
    print("wrote los-probability.svg and los-probability.png")


if __name__ == "__main__":
    main()
