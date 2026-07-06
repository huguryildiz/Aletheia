# Adoption transcript — UWSN non-uniform k-connectivity (real model, clean subject)

Subject: [`uwsn-k-connectivity/`](uwsn-k-connectivity/) — a single-file, runnable MILP
([`model.py`](uwsn-k-connectivity/model.py)) that computes energy-minimizing non-uniform
k-connected routing for an underwater sensor network. It is a **faithful, reduced (13-node)
reimplementation** of the model behind the published paper "Mitigating Energy Cost of
Connection Reliability in UWSNs Through Non-Uniform k-Connectivity"
([IEEE doc 11143186](https://ieeexplore.ieee.org/abstract/document/11143186)). The physics
is preserved from the original 30-node MATLAB/Python code; the topology is reduced and a
fixed seed + a solution export + a fast correctness gate are added so it runs end-to-end.

Run date: 2026-07-06. This replaces an earlier adoption of the *raw, messy* 30-node repo
(kept in git history): that version had no fast gate and could not reproduce its own
committed CSVs. The subject was cleaned into one runnable model so the adoption could
demonstrate the **happy path** — a real `gate_command` that actually runs.

## 1. What the model is (faithful, reduced)

The MILP minimizes `tau`, the maximum per-node energy dissipation (THEDN), subject to:
flow conservation, node-disjoint multi-path routing, distance-tiered acoustic transmit
energy (Thorp absorption at 25 kHz), interference-aware bandwidth, and — the paper's
contribution — **non-uniform k-connectivity**: critical sources keep more node-disjoint
paths to the base station than the rest. Constants live at the top of `model.py`
(`NODE=13, SEED=6, K_HIGH=2, K_LOW=1`, plus the physical channel/traffic constants).

Two design findings, both recorded as decisions (`uwsn-k-connectivity/docs/decisions.md`):

- **Uniform k is infeasible on a small graph.** Requiring every source to hold k≥2
  node-disjoint paths needed ~16 nodes; k=3 needed more. On a long thin sparse UWSN there
  simply are not enough disjoint relays. The paper's *non-uniform* scheme (some nodes k=2,
  the rest k=1) is both its actual contribution and what makes a 13-node instance feasible.
  This scheme was present in the original code only as a commented-out block.
- **Seed 6 is the operating point.** Most seeds are infeasible at this size — a faithful
  reflection of the model's tightness, not a bug. Seed 6 is the smallest that solves.

## 2. Interview and bindings

| Key | Bound value | How |
| --- | --- | --- |
| `critical_modules` | `["model.py"]` | single file; the sole source of the result |
| `gate_command` | `python3 model.py --check` | **a real, fast (~2 s) command this time** |
| `canonical_values` | `model.py` | constants block at the top |
| `env_manifest` | `requirements.txt` | `gurobipy>=9.5,<10` (needs a Gurobi license) |
| `data_dir` | `null` | topology is generated from SEED; no external input |

## 3. The gate — and why it checks `tau`, not the CSV

`python3 model.py --check` re-solves and compares the objective `tau` against
`baseline.json` (relative tolerance 1e-6), exiting 0 (pass) or 1 (fail). It deliberately
does **not** byte-compare `solutions.csv`.

Verified live during adoption:

```
$ python3 model.py            # → solutions.csv + baseline.json, tau=49052.184769
$ python3 model.py --check    # GATE PASS (fresh process)    rc=0
$ python3 model.py --check    # GATE PASS (another process)  rc=0
# tamper baseline.json tau → GATE FAIL rc=1 ; restore → rc=0
```

**Why not the CSV**: the routing optimum is *non-unique* — many different flow assignments
achieve the same minimum `tau`, and Gurobi returns different ones across processes (even at
`Threads=1, Seed=0`, which stabilizes `tau` but not the routing). Byte-comparing
`solutions.csv` would therefore flag a solver tie-break, not a regression. The reproducible,
scientifically meaningful invariant is `tau`, so that is what the gate pins. This is the
`numerical-determinism` discipline applied honestly: gate the invariant, not the artifact.
`solutions.csv` is committed as one illustrative optimal routing (its flow values, in the
hundreds-to-1440 range, match the scale of the paper's own figure).

## 4. Scaffold produced

- **`CLAUDE.md`** — config block (§2) + operating rules, including the determinism caveat.
- **`docs/decisions.md`** — D01 (adoption) and D02 (non-uniform k + reduced topology + seed).
- **`docs/build_log/README.md`** — empty log, ready.
- **`docs/project-layout.md`** — pruned to the real single-model structure.
- **`requirements.txt`** — the environment pin (previously a gap; now bound).
- **`results/uwsn-nonuniform_2026-07-06/meta.json`** — a **genuine** run record (not
  retroactive): seed, `tau`, outputs, and an honest environment fingerprint noting the
  interpreter is x86_64 under Rosetta, **not** native arm64.

## 5. Honest notes

- **This subject is a reimplementation, not the verbatim published repo.** The original
  30-node MATLAB/Python code is in git history; it was replaced (not merely slimmed) to get
  a runnable single-file model with a real gate. Faithful to the model's physics and to the
  paper's non-uniform-k idea; not bit-identical to the paper's numbers (different size/seed).
- **The gate needs a Gurobi license**, so it is not runnable in a license-free CI; it is a
  real developer-machine gate. `python3 model.py --check` is the exact command.
- **Determinism is tiered**: `tau` reproduces across processes; the routing does not. Both
  facts are recorded rather than hidden.
