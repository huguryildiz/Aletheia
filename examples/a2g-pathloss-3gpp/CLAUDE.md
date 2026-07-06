# CLAUDE.md — a2g-pathloss-3gpp

## One line

Single-file 3GPP TR 36.777 A2G propagation model (UMa-AV) with a correctness gate that checks
every coefficient against the published tables. See [`README.md`](README.md).

## Quick start

```bash
python3 model.py                 # solve → solutions.csv (stdlib only)
python3 model.py --check         # the correctness gate (Rule 1)
pip install -r requirements.txt  # only for plot.py
```

## Aletheia config block

Filled by the `skill-library-generator` interview on 2026-07-06 (see `docs/decisions.md` D01).

```yaml
aletheia:
  critical_modules: ["model.py"]
  gate_command:     "python3 model.py --check"   # correctness vs 3GPP ground truth
  canonical_values: "model.py"                   # PL_SCENARIO / LOS_SCENARIO + coefficients
  ground_truth:     "expected.json"              # 3GPP TR 36.777 verified values
  evidence_dir:     "results/"
  decision_log:     "docs/decisions.md"
  env_manifest:     "requirements.txt"
  data_dir:         null
```

## Operating rules

1. **Correctness gate** — any change to `model.py` → `python3 model.py --check` must pass
   before "done". Unlike a reproducibility gate (which only checks the answer did not *change*),
   this checks the answer is *right*: it compares the computed LoS probability and total loss to
   `expected.json`, whose values are anchored to 3GPP TR 36.777, and asserts every coefficient
   names one scenario. If a change *intentionally* alters the result (e.g. a new scenario or
   frequency), that is a formulation change → update `expected.json` **with the new spec-anchored
   values** and add a `decision-log` entry; never edit the ground truth to make a red gate green.
2. **Canonical operating point** — the scenario bindings and coefficients in `model.py`, and the
   ground truth in `expected.json`, are protected (`canonical-params`); each coefficient traces
   to a named 3GPP table (`lit-anchor`).
3. **Kept runs** — evidence lands in `results/<name>_<date>/meta.json` (`evidence-convention`).

## Pointers

- Decisions: `docs/decisions.md` · Layout: `docs/project-layout.md`
- Worked example (narrative): [`../a2g-pathloss-3gpp.md`](../a2g-pathloss-3gpp.md)
