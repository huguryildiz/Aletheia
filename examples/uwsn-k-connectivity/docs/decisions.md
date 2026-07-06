<!-- markdownlint-disable MD024 -->
# Decision Log

Significant decisions + rationale. Authority layer: when code and docs disagree, this
arbitrates. New decision at the top; numbers assigned at write time.

---

## D02 — Non-uniform k assignment and reduced topology

**Status**: accepted
**Date**: 2026-07-06

**Context**: The clean reimplementation had to (a) demonstrate the paper's actual
contribution — *non-uniform* k-connectivity — and (b) solve fast enough to serve as a
correctness gate. A uniform k across all sources was found infeasible on small topologies
(k=2 needed ~16 nodes, k=3 more), because node-disjoint multi-path routing on a long thin
sparse network runs out of disjoint relays. The original `Model/VariableK_MR.py` (now in git
history only) carried the intended non-uniform scheme as a *commented-out* block
(`if k < NodeRate: k1 else: k2`).

**Decision**: Implement non-uniform k per that commented block: sources with index below
`NODE*RATE` require `K_HIGH=2` node-disjoint paths, the rest `K_LOW=1`. Use `NODE=13` (the
paper's own illustrative figure uses ~13 nodes) and fixed `SEED=6` (the smallest-index seed
for which the non-uniform instance is feasible; most seeds are infeasible, which faithfully
reflects the model's tightness). Losing alternative: uniform k — rejected because it needs a
large network to be feasible and does not show the paper's non-uniform idea.

**Impact**: `model.py` constants `NODE=13, SEED=6, K_HIGH=2, K_LOW=1`. Operating-point
values are canonical (`canonical-params`). The chosen instance solves in ~2 s with
`tau=49052.184769`, recorded in `baseline.json` and gated by `python3 model.py --check`.

---

## D01 — Adopt the Aletheia operating discipline

**Status**: accepted
**Date**: 2026-07-06

**Context**: This repo is Aletheia's clean end-to-end adoption example — a runnable subject
with a real, fast correctness gate (contrast the earlier adoption of the messy 30-node
MATLAB repo, which had no fast gate; that version is in git history and
`../adoption-transcript.md`).

**Decision**: Adopt the pack. Bindings in `CLAUDE.md`: `critical_modules=[model.py]`,
`gate_command="python3 model.py --check"` (a real command this time), `canonical_values=model.py`,
`env_manifest=requirements.txt`. `data_dir` bound to `null` (topology generated from SEED,
no external input).

**Impact**: `CLAUDE.md`, `docs/`, and `results/` created; the gate is runnable from the
committed code alone (`pip install -r requirements.txt` + a Gurobi license).
