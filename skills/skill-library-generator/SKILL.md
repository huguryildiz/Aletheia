---
name: skill-library-generator
description: >-
  Use when adopting the Aletheia discipline in a new or existing research repository — discovering the project's actual conventions, interviewing the maintainer to fill the config bindings, extracting the project's own recurring failure modes into project-local skills, and scaffolding the record surfaces (decision log, build log, evidence dirs) after approval. Trigger phrases: "adopt aletheia here", "set up the research discipline", "generate skills for this repo", "bind the pack to this project", "run the adoption interview".
tier: generator
---

# skill-library-generator

The meta-skill that adapts the pack to a concrete repository. Two jobs: **bind** the
portable skills to this project (fill the config block by interview, grounded in what the
repo actually contains), and **mine** the project's own recurring failure modes into
project-local skills the pack does not ship. The invoking agent is the runtime: everything
below is done with file tools at invocation time — there is no bootstrap script.

## When to use

- First-time adoption in a new or existing research repo.
- Re-binding after a restructure (paths in the config block went stale).
- Periodic harvest: "what keeps going wrong here that deserves a skill?"

## When NOT to use

- The repo is already bound and the bindings are current — invoke the individual skills
  directly.
- Mid-incident debugging — adopt discipline calmly, not during a fire.
- A repo you have no mandate to restructure — discovery and interview are fine, but the
  scaffold step needs an owner's approval by design.

## Phase 0 — Discovery (read-only)

Scan before asking. Establish, from the repo itself:

- layout: package dirs, tests, docs, notebooks, scripts, data/results dirs (`find . -maxdepth 2 -type d`);
- environment: manifest + lockfile present? which manager? (`ls pyproject.toml uv.lock poetry.lock environment.yml 2>/dev/null`);
- tests: runner, existing correctness-critical tests (`ls tests/`);
- record surfaces: decision log? build log? existing conventions in README/CLAUDE.md;
- history: `git log --oneline -30` — what does work here actually look like? repeated
  fix-the-fix commits, "oops" reverts, and stale-doc commits are failure-mode evidence.

Label every conclusion **observed** (with the path/command) or **inferred** (with the
reasoning). Never present an inference as an observation.

## Phase 1 — Interview (bindings)

Fill the config block from `templates/CLAUDE.md`, one proposal at a time: for each key,
propose the value discovery suggests, and confirm or correct with the maintainer.

| Key | Interview question (propose first, then ask) |
|---|---|
| `critical_modules` | "Which modules, if silently wrong, corrupt your results?" |
| `gate_command` | "Which single test command must pass before 'done' on those modules?" |
| `canonical_values` | "Where do the protected default parameters live?" |
| `evidence_dir` | "Where should kept run evidence land?" |
| `doc_layers` | "What are your knowledge layers, authority first?" |
| `decision_log` / `build_log_dir` / `phase_plan` | "Where do decisions / phase evidence / the plan live (or should)?" |
| `env_manifest` / `data_dir` | "Which manifest pins your environment? Where does input data live?" |

A key with no honest answer is a **gap**, not a blank to invent — record it as a
recommendation (e.g. "no gate exists yet; candidate: pin these three computations").

## Phase 2 — Failure-mode extraction

From discovery + interview, list the project's recurring failure modes ("results only in
scratch dirs", "figures nobody can regenerate", "defaults edited during probes"). Sort each
into:

- **covered by the pack** → the binding from Phase 1 activates it; note which skill;
- **project-specific** → a candidate *local* skill (e.g. a domain instrument-calibration
  checklist, a lab-specific data-ingest runbook).

## Phase 3 — Draft local skills

For each approved project-specific candidate, draft a project-local `SKILL.md` in the
active harness's skill directory (`.claude/skills/<name>/SKILL.md` for Claude Code; for
Codex CLI, see this pack's `docs/install.md` Path C for the current verified plugin-root
layout) in the pack's house format: frontmatter
(`name`, trigger-rich `description`), imperative runbook, a "when NOT to use" note, and a
"Provenance & maintenance" section whose re-verification commands were **actually run in
this repo during discovery**. Ground-truth-only: a runbook step you could not verify here
does not ship; label anything inferred.

## Phase 4 — Audit before scaffold

Self-review the drafts: every path exists (`test -f` / `test -d`), every command ran, no
invented conventions, no duplication of a pack skill under a new name. Present the full
plan — bindings, gaps, local skill drafts, files to be created — and **stop for approval**.

## Phase 5 — Scaffold (post-approval only)

Only after explicit approval, and never overwriting an existing file without showing it
first:

1. Write the filled config block + routing table into the project's `CLAUDE.md`
   (from `templates/CLAUDE.md`).
2. Create missing record surfaces: `{{decision_log}}` (from `templates/decisions.md`,
   founding entry D01 = the adoption itself), `{{build_log_dir}}/`, the negative-results
   ledger, `{{evidence_dir}}` with its README + gitignore policy, and
   `templates/results-meta.schema.json` copied to the project's docs.
3. Install the layout document (`templates/project-layout.md` → `docs/`, pruned to reality).
4. For manual installs, copy the pack's leaf skill folders into the active harness's skill
   directory — `.claude/skills/` for Claude Code, flattened; for Codex CLI, follow the
   plugin-root layout in `docs/install.md` Path C.
5. Commit only if the maintainer asks; report exactly what was created either way.

## Re-audit mode — `aletheia-doctor`

Trigger: "run aletheia-doctor", "re-audit the bindings", "are the Aletheia
bindings still valid?" — used weeks after adoption, when binding rot is the risk
(paths renamed, gate command changed, critical modules moved). This is the
read-only counterpart to first-time generation: same config block, opposite
direction — it *checks* what generation *wrote*.

Read-only. Writes nothing; reports. Steps:

1. **Read the config block** in the repo's `CLAUDE.md`. If absent → report
   NOT ADOPTED and stop (suggest the generator, not the doctor).
2. **Resolve each binding** and mark it:
   - `{{critical_modules}}` — each path exists? → RESOLVES / MISSING (name it).
   - `{{doc_layers}}` — each declared doc/layer path exists? → RESOLVES / MISSING.
   - `results/` convention — directory present; most recent `meta.json` parses? → RESOLVES / STALE / MISSING.
3. **Re-run the gate on a clean tree.** Confirm the working tree is clean
   (uncommitted changes make the result unattributable — report DIRTY and stop).
   Run `{{gate_command}}`. Report the honest outcome:
   - GREEN / RED — the gate ran to a verdict.
   - UNRUNNABLE — the command, interpreter, or a required dependency/license is
     absent in this environment, so no GREEN/RED verdict is possible here. Treat
     as MANUAL: the gate is real but must be VERIFY BY HAND on a machine that can
     run it (e.g. the UWSN gate `python3 model.py --check` needs a Gurobi license
     — see the adoption transcript). Never fabricate GREEN for a gate you could
     not actually run.
   - MANUAL — VERIFY BY HAND — the binding is a documented by-hand check rather
     than a shell command at all. Name it.
4. **Report**, one line per binding + a coverage footer (what was read, what was
   run). Never "fix" — a MISSING/RED finding is handed to the human.

## Rules

1. **Ground-truth-only.** Every command, path, and claim in anything you generate is
   verified against this repository during this invocation; inference is labeled. Wrong
   runbooks are worse than none.
2. **Nothing is written before Phase 5**, and Phase 5 requires explicit approval of the
   Phase 4 plan.
3. **State is derived, not stored** — do not create a status/state file for the adoption;
   the scaffold's own artifacts (D01 entry, config block) are the record.
4. **Bind before inventing.** A failure mode the pack already covers gets a binding, not a
   new near-duplicate skill.
5. **Small is honest.** A project that needs five bindings and one local skill should get
   exactly that — adoption size is set by the repo's needs, not the pack's inventory.

## Provenance & maintenance

The generator's phase structure (discover → interview → extract → draft → audit → scaffold)
generalizes how this pack itself was produced: portable skills were harvested from one
working repository's conventions and re-bound through a config block; see the pack's
`examples/` directory for that worked mapping. The interview table mirrors
`templates/CLAUDE.md` — keep the two in lockstep when either changes.

Re-verify (pack maintainer):

- `grep -o '{{[a-z_]*}}' templates/CLAUDE.md | sort -u` — the interview table covers every
  placeholder key.
- `ls skills/core skills/extended` — the "covered by the pack" sort in Phase 2 reflects the
  real inventory.
