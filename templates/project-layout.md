# Project Layout — {{PROJECT_NAME}}

<!-- Aletheia template: copy into docs/ and prune to what your project uses.
     Companion to the project-layout skill. Every directory gets a one-line intent;
     a directory nobody can describe in one line is a removal candidate. -->

This document defines the folder/package organization and each module's responsibility.
**Phase status is never kept here** (it drifts) — derive it from `git log`, the latest
build-log entry, and `TODO.md`.

## Canonical tree

```text
{{project}}/
├── README.md                 # summary, install, how to run
├── TODO.md                   # current-iteration execution buffer (rewritten per phase)
├── CLAUDE.md                 # operating rules + Aletheia config block
├── {{env manifest}}          # pyproject.toml / environment.yml — lockfile committed alongside
├── .gitignore                # data/**, models/**, results/** (READMEs re-included)
│
├── docs/
│   ├── README.md             # authority map: which document is current / stale / archived
│   ├── project-layout.md     # this file
│   ├── decisions.md          # ADR-lite decision chain (authority layer)
│   ├── {{spec}}.md           # implementation spec — the contract the gate tests against
│   ├── design/               # full technical design ("why" documents)
│   ├── roadmap/              # phase plan + gate registry + status board
│   ├── build_log/            # write-once phase/gate evidence entries (NN_topic.md)
│   ├── negative_results.md   # one-line dead-end ledger
│   └── archive/              # retired documents — moved here, never deleted
│
├── src/{{package}}/          # installable package (src-layout)
│   ├── common/               # shared library — imports nothing above it
│   ├── {{model}}/            # core computation (typically inside critical_modules)
│   └── experiments/          # orchestration — imports everything below it
│
├── configs/                  # declarative run configs (a reviewer can re-run from these)
├── scripts/                  # reusable CLI pipelines → write into results/
├── notebooks/                # numbered exploration series + README manifest
│   └── archive/              # retired series (numbers never reused)
├── tests/                    # unit + integration; includes the named correctness gate
│
├── data/                     # inputs — gitignored; README + provenance/hashes tracked
├── models/                   # fitted/trained artifacts — gitignored
└── results/                  # evidence — gitignored; meta.json + curated summaries force-added
```

## Module responsibilities

| Directory | Responsibility | Notes |
|---|---|---|
| `src/{{package}}/common/` | shared constants, IO, domain primitives | everything imports from here; it imports nothing above |
| `src/{{package}}/{{model}}/` | the result-producing computation | high test density; in `critical_modules` |
| `src/{{package}}/experiments/` | orchestration of sweeps/campaigns | called by `scripts/`; low test density |
| `scripts/` | reusable CLI entry points | args + defaults; no library logic |
| `notebooks/` | exploratory narratives | numbered, manifest-governed, executed before commit |

## Invariants (from the project-layout skill)

1. Import direction is bottom-up; `common/` never imports upward.
2. Bulk dirs (`data/`, `models/`, `results/`) are gitignored; their READMEs, meta files,
   and curated summaries are tracked.
3. Session/planning artifacts live under `.claude/plans/`, never in `docs/`.
4. Retired documents move to `docs/archive/` — never deleted.
5. Structural changes get a decision-log entry before files move.
