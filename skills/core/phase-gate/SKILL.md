---
name: phase-gate
description: >-
  Use when closing a project phase or milestone gate — the user believes the phase's acceptance criteria are met and wants it closed formally, with evidence verified item by item. Runs the closure ritual in strict order and blocks on any open item. Trigger phrases: "close the phase", "close the gate", "is the phase done", "phase-gate check", "milestone closure", "can we call this phase complete".
tier: core
---

# phase-gate

Close a phase the way a reviewer would: verify the phase's *written* acceptance checklist
item by item against named evidence artifacts, then update the record everywhere it lives.
A phase closes on evidence, not on recollection — and one open item means it does not close.

## When to use

- A phase, milestone, or gate from the project plan (`{{phase_plan}}`) appears complete and
  the user wants formal closure.

## When NOT to use

- Mid-phase "is this sub-task done?" — that is an execution-turn question against the
  current TODO buffer.
- "Where are we / what's next" — dispatch the `session-historian` agent.
- Declaring partial victory — there is no partial closure (see Rules).

## The ritual (strict order — no step skipped, no step reordered)

1. **Load the contract.** Read the phase's acceptance checklist from `{{phase_plan}}` (and
   its gate registry row, if the plan keeps one). *This written checklist — never memory —
   is what gets verified.*
2. **Verify each item with evidence.** For every checklist item, name the artifact that
   proves it: fresh gate-test output, an `{{evidence_dir}}/<name>_<date>/` run directory
   with its meta file, a decision entry, an executed notebook or committed figure. An item
   without an artifact is **OPEN** — the phase does not close. Run `{{gate_command}}` fresh
   as part of this step; a red gate blocks closure regardless of checklist state.
3. **Decision sweep.** Every decision this phase owed (check the plan's decision queue, if
   any) must exist in `{{decision_log}}` with a real number — assigned at write time, never
   reserved in advance.
4. **Build-log entry.** Invoke the `build-log` skill (phase-completion bar applies). The
   entry links every evidence artifact from step 2.
5. **Layer-sync audit** scoped to the phase. Drift found → fix in a separate approved turn
   per that skill's rules, then re-run the audit before closing.
6. **Update the status surfaces.** Mark the phase ✅ on the plan's status board, and rewrite
   the TODO buffer to the *next* phase's sub-tasks — the buffer is ephemeral; completed-phase
   content is deleted, not accumulated.
7. **Regenerate derived views** (project wiki, dashboards, generated indexes), if the
   project keeps any. Derived views are never hand-edited: wrong content means a
   source-layer fix first, then regeneration.
8. **User sign-off.** Present the closure summary — checklist verdicts, evidence links,
   decision/build-log diffs — and get explicit approval **before committing**. Gate
   decisions with branches (pass/drop calls, representative-point choices) are the user's
   call, never auto-resolved.

## Output format

```
## Phase closure — <phase name> / <gate id>

| Acceptance criterion | Evidence | Status |
|---|---|---|
| ... | {{evidence_dir}}/<run>/ or build-log NN or D<n> | ✅ / ❌ OPEN |

**Gate test**: <N> tests green (summary of fresh output)
**Decisions**: D<n>, ... | **Build log**: NN_topic.md | **Layer sync**: ✅/⚠
**Verdict**: CLOSED / BLOCKED — <open items>
```

## Rules

1. **One OPEN item = no closure.** Pre-declared off-ramps written into the plan (e.g. "if
   the result window is empty, branch to X") are legitimate closures; silent scope-shrinking
   is not.
2. **Evidence means versioned evidence.** "It ran and the output looked fine" without an
   `{{evidence_dir}}` run directory is a dark run — treat the item as OPEN
   (see `evidence-convention`).
3. **Never soften a negative result to pass a gate.** An infeasibility, a null effect, or a
   hardness finding — rigorously recorded — is a *valid closure artifact*; record it
   verbatim and close on it (see `negative-results-ledger`).
4. **Commits happen after sign-off**, following the project's git workflow.
5. **Fresh runs only.** Cached test output, yesterday's logs, or "it passed last week" do
   not satisfy step 2.

## Configuration

- `{{phase_plan}}` — the plan document holding phase tables + acceptance checklists.
- `{{gate_command}}` — the named correctness gate (see `correctness-gate`).
- `{{decision_log}}`, `{{build_log_dir}}`, `{{evidence_dir}}` — the record surfaces.

## Provenance & maintenance

Generalized from the gate-closure ritual of a working computational-research repository
(checklist-with-evidence verification, decision sweep, build-log + sync audit coupling,
sign-off-before-commit); see the pack's `examples/` directory for the worked exemplar
mapping. The eight-step order and rules 1–3 are verified practice; step 7 applies only if
the project keeps derived views (labeled optional by construction).

Re-verify in your project:

- `{{gate_command}}` — must be green before any closure claim.
- `grep -n "OPEN\|⬜\|🟡" <status board>` — anything still open on the board contradicts a
  closure claim.
- `ls -t {{evidence_dir}} | head -3` — the runs cited as evidence actually exist and are
  recent.
