# CLAUDE.md — {{PROJECT_NAME}}

<!-- Aletheia template: copy to your project root and fill every {{...}}.
     The Aletheia skills read the config block below; the routing table tells the
     agent which discipline applies to which kind of work. Keep both. -->

## One line

{{ONE_LINE: what this project computes/optimizes/models, for which output — e.g. "X pipeline
targeting one journal paper + one dataset release".}}

Current phase status is NOT kept in this file (it drifts) — derive it from `git log`, the
latest `{{build_log_dir}}` entry, and `TODO.md`.

## Quick start

```bash
{{INSTALL_COMMAND}}        # e.g. "uv sync" / "conda env create -f environment.yml"
{{TEST_COMMAND}}           # full test suite
{{gate_command}}           # the correctness gate (Rule 1 below)
```

## Aletheia config block

Machine-readable bindings; every Aletheia skill resolves its `{{placeholder}}` references
here. Filled by the `skill-library-generator` interview, or by hand.

```yaml
aletheia:
  critical_modules: ["src/{{pkg}}/core/**", "src/{{pkg}}/model/**"]  # correctness-gate scope
  gate_command:     "{{e.g. pytest tests/test_correctness.py}}"      # the named gate
  canonical_values: "src/{{pkg}}/config/constants.py"                # protected defaults (canonical-params)
  evidence_dir:     "results/"                                       # evidence-convention root
  doc_layers:       [decisions, spec, code, notebooks]               # layer-sync order (authority first)
  decision_log:     "docs/decisions.md"                              # decision-log file
  build_log_dir:    "docs/build_log/"                                # build-log entries
  phase_plan:       "docs/roadmap/plan.md"                           # phase tables + acceptance checklists (phase-gate)
  env_manifest:     "pyproject.toml"                                 # + lockfile alongside (environment-lock)
  data_dir:         "data/"                                          # input data root (data-fingerprint)
```

## Work-type routing (default + escalation — NOT mandatory-every-time)

Which discipline applies to which kind of work. **Default is the minimum; escalation is
conditional. Never turn a small change into bureaucracy.**

| Work type (trigger) | Default (do this) | Escalate to … when … |
|---|---|---|
| small exploration | notebook + light note (`notebook-vs-script`) | — (stays light) |
| reusable experiment / real run | script + `evidence-convention` (results dir + meta) | + `environment-lock` & `data-fingerprint` when it feeds a paper figure/claim or must be reproduced by others |
| critical logic change | `correctness-gate` (run the named gate) | + `canonical-params` when it touches protected defaults; + `decision-log` when a red gate is an *intentional* formulation change |
| stochastic run | record seeds (`reproducibility-provenance`) | + `numerical-determinism` when results must be bit-reproducible / cross-machine |
| numeric claim / result | `statistical-reporting` (replication + interval) | + `verifier` agent when the claim is load-bearing (goes in the paper); + `external-positioning` when it is a novelty claim |
| phase conclusion | `phase-gate` checklist | + `build-log` when it is a real milestone, not a trivial sub-step |
| assumption / default change | `decision-log` entry | + `layer-sync` when it touches ≥ 2 layers; + `canonical-params` when it is a canonical default |
| dead end / failed attempt | one-line `negative-results-ledger` entry | — (stays light) |

## Operating rules (project-pinned summaries; the skills carry the detail)

1. **Correctness gate** — any change under `critical_modules` → `gate_command` must pass
   before "done". Red = bug OR intentional change (then: approval + pin update + decision
   entry). Never pass silently.
2. **Canonical operating point** — values in `canonical_values` change only inside a sweep
   or with explicit approval; probes are script-level arguments.
3. **Session artifacts** — AI-generated plans/scratch specs live under `.claude/plans/`,
   never in `docs/` or the repo root.
4. **Rhythm** — execution turns work from `TODO.md`; phase ends close via `phase-gate`;
   sessions after a gap open with the `session-historian` agent, not from memory.
5. {{PROJECT_SPECIFIC_RULES: language conventions, math-notation rules, review cadence — add
   your own numbered rules here.}}

## Pointers

- Decisions: `{{decision_log}}` (authority layer — newest on top).
- Spec: {{SPEC_DOC_PATH: the implementation contract the gate tests against}}.
- Plan/status: `{{phase_plan}}` (+ status board).
- Evidence: `{{evidence_dir}}<name>_<date>/` — no dark runs.
