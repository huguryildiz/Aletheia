#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Air-to-ground (A2G) propagation model for a cellular-connected UAV, per 3GPP TR 36.777
("Study on Enhanced LTE Support for Aerial Vehicles", Release 15, V15.0.0):
    Table B-2 — path loss ;  Table B-1 — line-of-sight (LoS) probability.

The real failure this example is about: an AI-generated model computed PATH LOSS with the
UMa-AV formula but pulled the LoS-PROBABILITY coefficients from the UMi-AV row — both are
valid 3GPP values in adjacent rows, so nothing looks wrong on inspection, yet at 1 km it
flips LoS probability 0.85 → 0.25 (a ~10 dB total-loss error, physically backwards).

The gate here checks CORRECTNESS against a named authority (the 3GPP tables), not just
reproducibility: `python3 model.py --check` re-computes and compares to expected.json, whose
values were verified against TR 36.777 (see examples/a2g-pathloss-3gpp.md, Provenance), and
asserts every propagation coefficient names ONE scenario.

Run:  python3 model.py            -> writes solutions.csv (distance, P_LOS, Ptot_dB)
      python3 model.py --check     -> the gate: values match ground truth + scenario is consistent
"""

import csv
import json
import math
import sys

log10 = math.log10

# ============================ CONSTANTS ============================
FC = 2.0          # carrier frequency (GHz)
H_BS = 25.0       # base-station height (m)
H = 100.0         # UAV (aerial UE) height (m)
TEST_DISTANCES = [200, 500, 1000, 2000, 4000]   # 2D distance from base station (m)
GT_RTOL = 1e-3    # gate tolerance vs the 3GPP-verified ground truth

# Which 3GPP scenario each coefficient block comes from. Path loss is UMa-AV (as in the
# paper's bug, PL was kept correct); LoS probability MUST name the same scenario. Setting
# LOS_SCENARIO = "UMi-AV" reproduces the real AI bug — the gate then fails on both counts.
PL_SCENARIO = "UMa-AV"
LOS_SCENARIO = "UMa-AV"

# LoS-probability coefficients (TR 36.777 Table B-1), keyed by scenario. p1, d1 depend on H.
LOS_COEFFS = {
    "UMa-AV": lambda h: (4300 * log10(h) - 3800, max(460 * log10(h) - 700, 18)),
    "UMi-AV": lambda h: (233.98 * log10(h) - 0.95, max(294.05 * log10(h) - 432.94, 18)),
}


# ============================ MODEL (TR 36.777) ============================
def pl_los(d3d):        # Table B-2, UMa-AV LoS path loss (dB)
    return 28.0 + 22 * log10(d3d) + 20 * log10(FC)


def pl_nlos(d3d):       # Table B-2, UMa-AV NLoS path loss (dB)
    return -17.5 + (46 - 7 * log10(H)) * log10(d3d) + 20 * log10(40 * math.pi * FC / 3)


def p_los(d2d, p1, d1):     # Table B-1, LoS probability
    if d2d <= d1:
        return 1.0
    return d1 / d2d + math.exp(-d2d / p1) * (1 - d1 / d2d)


def evaluate():
    """Return per-distance (d2D, P_LOS, Ptot_dB) at the current scenario bindings."""
    p1, d1 = LOS_COEFFS[LOS_SCENARIO](H)
    rows = []
    for d2d in TEST_DISTANCES:
        d3d = math.sqrt(d2d ** 2 + (H_BS - H) ** 2)
        plos = p_los(d2d, p1, d1)
        ptot = pl_los(d3d) * plos + pl_nlos(d3d) * (1 - plos)   # TR 36.777 eq (15)
        rows.append((d2d, plos, ptot))
    return rows


# ============================ GATE ============================
EXPECTED_FILE = "expected.json"
CSV_FILE = "solutions.csv"


def check():
    """Correctness gate: (1) every coefficient names one scenario; (2) computed values
    match the 3GPP-verified ground truth in expected.json. Returns (ok, messages)."""
    msgs = []
    ok = True

    if PL_SCENARIO != LOS_SCENARIO:
        ok = False
        msgs.append(f"SCENARIO MISMATCH: path loss = {PL_SCENARIO}, "
                    f"LoS probability = {LOS_SCENARIO} (both must name one scenario)")

    with open(EXPECTED_FILE) as fh:
        gt = json.load(fh)
    exp = {int(d): v for d, v in gt["by_distance"].items()}
    for d2d, plos, ptot in evaluate():
        e = exp[d2d]
        if abs(plos - e["P_LOS"]) > GT_RTOL * max(1.0, abs(e["P_LOS"])):
            ok = False
            msgs.append(f"P_LOS({d2d}) = {plos:.4f} != ground truth {e['P_LOS']:.4f}")
        if abs(ptot - e["Ptot_dB"]) > GT_RTOL * max(1.0, abs(e["Ptot_dB"])):
            ok = False
            msgs.append(f"Ptot({d2d}) = {ptot:.2f} != ground truth {e['Ptot_dB']:.2f} dB")
    return ok, msgs


def write_csv():
    with open(CSV_FILE, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["d2D_m", "P_LOS", "Ptot_dB"])
        for d2d, plos, ptot in evaluate():
            w.writerow([d2d, f"{plos:.4f}", f"{ptot:.2f}"])


def main(argv):
    print(f"scenario: path loss = {PL_SCENARIO}, LoS probability = {LOS_SCENARIO}  "
          f"(fc={FC} GHz, h={H} m)")
    if "--check" in argv:
        ok, msgs = check()
        if ok:
            print("GATE PASS: values match 3GPP TR 36.777 ground truth; scenario consistent")
            return 0
        print("GATE FAIL:", file=sys.stderr)
        for m in msgs:
            print("  -", m, file=sys.stderr)
        return 1
    write_csv()
    print(f"wrote {CSV_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
