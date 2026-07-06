# CLAUDE.md — uwsn-k-connectivity

## One line

Single-file MILP computing energy-minimizing non-uniform k-connected routing for an
underwater sensor network — faithful reduced (13-node) reimplementation of the model behind
IEEE doc 11143186. See [`README.md`](README.md).

Current phase status is NOT kept in this file — derive it from `git log` and the latest
`docs/build_log/` entry.

## Quick start

```bash
pip install -r requirements.txt   # gurobipy (needs a Gurobi license; free for academics)
python3 model.py                  # solve → solutions.csv + baseline.json
python3 model.py --check          # the correctness gate (Rule 1)
```

## Aletheia config block

Filled by the `skill-library-generator` interview on 2026-07-06 (see `docs/decisions.md`
D01 and [`../adoption-transcript.md`](../adoption-transcript.md)).

```yaml
aletheia:
  critical_modules: ["model.py"]
  gate_command:     "python3 model.py --check"   # re-solves, compares tau to baseline.json
  canonical_values: "model.py"                   # constants block at the top of the file
  evidence_dir:     "results/"
  decision_log:     "docs/decisions.md"
  build_log_dir:    "docs/build_log/"
  env_manifest:     "requirements.txt"
  data_dir:         null   # no external input data; topology is generated from SEED
```

## Operating rules (project-pinned summaries)

1. **Correctness gate** — any change to `model.py` → `python3 model.py --check` must pass
   (exit 0) before "done". The gate re-solves and compares the objective `tau` to
   `baseline.json` within relative tolerance 1e-6. It deliberately does **not** compare
   `solutions.csv` byte-for-byte: the routing optimum is non-unique (many flows hit the same
   `tau`), so byte-comparison would flag a solver tie-break, not a regression (see
   `numerical-determinism`). If a change *intentionally* moves `tau`, that is a formulation
   change → update `baseline.json` and add a `decision-log` entry (never edit the baseline
   silently).
2. **Canonical operating point** — the constants at the top of `model.py` (`NODE`, `SEED`,
   `RATE`, `K_HIGH`, `K_LOW`, and the physical channel/traffic constants) change only inside
   a sweep or with an explicit `decision-log` entry (`canonical-params`).
3. **Determinism caveat** — `tau` is reproducible across processes; the exact `solutions.csv`
   routing is not (Gurobi returns different equally-optimal routings). `model.py` pins
   `Threads=1` + `Seed=0`, which stabilizes `tau` but not the routing (`numerical-determinism`).
4. **Kept runs** — a run worth keeping lands in `results/<name>_<date>/` with a `meta.json`
   (`evidence-convention`); record the environment, since the tested interpreter here is
   x86_64 under Rosetta, not native arm64 (`run-provenance`).

## Pointers

- Decisions: `docs/decisions.md` (authority layer — newest on top).
- Evidence: `results/<name>_<date>/meta.json`.
- Layout: `docs/project-layout.md`.
