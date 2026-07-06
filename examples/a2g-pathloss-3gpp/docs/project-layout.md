# Project Layout — a2g-pathloss-3gpp

Pruned to reality (`project-layout` template). A single-model example.

```text
a2g-pathloss-3gpp/
├── model.py          # 3GPP TR 36.777 A2G model + correctness gate (critical module; stdlib only)
├── plot.py           # LoS-probability figure from the same formulas
├── expected.json     # 3GPP-verified ground truth — the gate's authority
├── requirements.txt  # matplotlib (plot.py only)
├── solutions.csv     # computed P_LOS / total loss vs distance
├── los-probability.svg / .png   # rendered figure (regenerable via plot.py)
├── README.md · CLAUDE.md
└── docs/
    ├── decisions.md
    └── project-layout.md   # this file
```

## Invariants

1. `model.py` is the only critical module; the gate checks it against `expected.json`.
2. `expected.json` is ground truth anchored to 3GPP TR 36.777 — changed only with a
   `decision-log` entry and new spec-anchored values, never to make a red gate green.
3. Kept runs land in `results/<name>_<date>/meta.json`.
