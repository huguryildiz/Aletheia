---
name: project-layout
description: >-
  Use when starting a new computational-science project, restructuring an existing one, or deciding where a new module, script, notebook, dataset, or document belongs — including whether a piece of work is a notebook one-off or a reusable script, and maintaining the notebook series. Also use when reviewing whether a repository's layout still matches its documented map. Trigger phrases: "where should this file go", "set up the project structure", "scaffold the repo", "folder layout", "project organization", "does this belong in scripts or notebooks", "notebook or script", "should this be a notebook or a script", "make this rerunnable", "the notebook is stale", "promote this to a script".
tier: core
---

# project-layout

Propose and hold a canonical folder layout for a computational-science repository, and keep
a single layout document that says what every directory is *for*. The layout is a contract:
every artifact has exactly one home, bulk artifacts never enter version control, and
AI-session planning files never mix with project deliverables.

## When to use

- Scaffolding a new research repository.
- Answering "where does this go?" for any new file.
- Auditing an existing repo whose layout document has drifted from reality.

## When NOT to use

- Mid-project wholesale reorganization without an explicit decision-log entry — moving
  directories breaks links, history, and muscle memory; propose, record the decision, then move.
- Adding one module to an existing, documented layout — just follow the map; do not re-derive it.
- Deciding project *phase status* — the layout document must never carry "current phase"
  information (see Rules).

## The canonical shape

Adapt names to the project; keep the separations. The copyable version lives in the pack's
`templates/project-layout.md`.

```text
<project>/
├── README.md                 # summary, install, how to run
├── TODO.md                   # current-iteration execution buffer (ephemeral, rewritten per phase)
├── CLAUDE.md                 # operating rules + the Aletheia config block
├── <env manifest + lockfile> # pyproject.toml + lock, environment.yml, etc. (see run-provenance)
├── docs/
│   ├── README.md             # authority map: which document is current / stale / archived
│   ├── decisions.md          # ADR-lite decision chain (see decision-log)
│   ├── <spec>.md             # implementation spec — the contract code is tested against
│   ├── design/               # full technical design ("why" documents)
│   ├── roadmap/              # long-horizon plan + phase/gate registry
│   ├── build_log/            # write-once phase/gate evidence entries (see build-log)
│   └── archive/              # retired documents — moved, never deleted
├── src/<package>/            # installable package (src-layout)
│   ├── common/               # shared library — imports nothing above it
│   └── <domain subpackages>  # model / analysis / orchestration layers
├── configs/                  # declarative run configurations (reviewer can re-run from these)
├── scripts/                  # reusable CLI pipelines (run repeatedly, produce artifacts)
├── notebooks/                # numbered exploratory narratives + README manifest
├── tests/                    # unit + integration; includes the named correctness gate
├── data/                     # inputs — gitignored, README tracked (see run-provenance)
├── models/                   # trained/fitted artifacts — gitignored
└── results/                  # run evidence — gitignored, selected summaries force-added
                              # (see evidence-convention)
```

## Runbook

1. **New repo**: copy `templates/project-layout.md` into `docs/`, prune directories the
   project will not use, and create the tree. Create `data/README.md`, `results/README.md`
   stating the gitignore-plus-tracked-README policy before the first run lands.
2. **Placement question**: read the layout document, place the file, and if the answer was
   not derivable from the document, add the missing one-line intent to it in the same change.
3. **Layout audit**: diff the real tree (`find . -maxdepth 2 -type d`) against the layout
   document; report undocumented directories and documented-but-absent ones.
4. Record any structural change as a decision-log entry before moving files.

## Rules

1. **One home per artifact class.** Exploratory one-offs → `notebooks/`; reusable pipelines
   → `scripts/`; shared logic → `src/<package>/common/`; orchestration imports downward,
   never sideways or up.
2. **Import direction is bottom-up.** `common/` imports nothing from higher layers;
   orchestration layers import everything below. A violated import direction is a layout bug.
3. **Bulk directories are gitignored, their READMEs are tracked.** `data/`, `models/`,
   `results/` accumulate gigabytes; version the *policy and provenance* (READMEs, meta files,
   selected summaries via explicit force-add), not the bulk.
4. **The layout document never states current phase or status.** Status is derived from git
   history, the build log, and the roadmap's status board — a status line in a layout file is
   a drift source by construction.
5. **Session artifacts are not deliverables.** Plans, task breakdowns, and scratch specs
   generated during AI-assisted sessions live under `.claude/plans/` (or the harness
   equivalent), never in `docs/`, `scripts/`, or the repo root. `docs/` holds only artifacts
   the project's papers and reports derive from.
6. **Retired documents move to `docs/archive/`, never get deleted.** Superseded specs remain
   citable; the docs authority map (`docs/README.md`) records what is current.
7. **Every directory earns a one-line intent** in the layout document. A directory nobody can
   describe in one line is a candidate for removal.

## Placement + notebook discipline

Rule 1 states the routing (one-offs → `notebooks/`, pipelines → `scripts/`, shared logic →
the package); the discipline below is how each destination avoids its characteristic rot —
notebooks rot as un-diffable pipelines, scripts rot as unread one-offs, copy-pasted logic
rots everywhere at once.

- **The notebook is the default**; a script is *earned* by re-run demand, not granted by
  optimism. Second manual re-run of a notebook for fresh outputs is the promotion signal:
  move the logic into the package, wrap a CLI script around it, keep the notebook as the
  narrative importing the same functions, and note the promotion in the manifest.
- **Numbered series with a manifest.** `NN_kebab-topic.ipynb`, numbering append-only (reusing
  a number breaks every citation to the old one); `notebooks/README.md` states each notebook's
  role and rerun policy (live / frozen / archived).
- **Execute top-to-bottom before commit.** A committed notebook carries its outputs — run it
  in place (e.g. `jupyter nbconvert --execute --inplace`) so the repo version shows what the
  code actually produces. A stale committed notebook is a bug: re-execute it or mark it
  frozen/archived. Retired series move to `notebooks/archive/`, numbers never reused
  (historical notebooks pinned to old APIs are narrative, not drift — `layer-sync` rule 7).
- **Narrative is the point; no library logic in cells.** Prose cells state the question,
  method, and reading of each figure — a notebook that is only code should have been a script,
  and the moment a function is worth reusing it moves to the package. Scripts orchestrate
  (argument parsing + calls into `src/` + output writing); heavy logic inside a script is
  library code in hiding. Never edit defaults to probe — a probe is a notebook cell or a
  script flag (`canonical-params`).

## Configuration

Reads from the Aletheia config block in the adopter's `CLAUDE.md`:

- `{{evidence_dir}}` — the run-evidence root (default `results/`).
- `{{decision_log}}` — the decision chain file (default `docs/decisions.md`).
- `{{build_log_dir}}` — the build-log directory (default `docs/build_log/`).

## Provenance & maintenance

Generalized from the working layout of a mature computational-research repository (src-layout
package, shared-library import discipline, gitignored bulk dirs with tracked READMEs,
docs authority map, session-artifact separation); see the pack's `examples/` directory for
the worked exemplar mapping. The tree above is a *verified* pattern; directory names are
adaptable, the separations are the invariant. Inference is labeled where it occurs.

Re-verify in your project:

- `git check-ignore data results models` — confirms bulk directories are ignored (paths that
  print are ignored; adjust to your names).
- `test -f docs/README.md && test -f {{decision_log}}` — confirms the authority map and
  decision chain exist.
- `find . -maxdepth 2 -type d -not -path './.git*'` — diff this against the layout document
  for undocumented directories.
