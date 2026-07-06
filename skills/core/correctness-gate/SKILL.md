---
name: correctness-gate
description: >-
  Use when a change touches any critical module — the modules whose silent breakage would corrupt the project's results — before claiming the change is done, ready, or working. Also use when the named gate test goes red and the bug-or-intentional-change call must be made. Trigger phrases: "run the gate", "is the correctness gate green", "I changed the core model", "the gate is red", "can I say this is done", "update the gate tolerance".
tier: core
---

# correctness-gate

The project names a set of critical modules (`{{critical_modules}}`) and one gate command
(`{{gate_command}}`). The contract: **if any critical module changed, "done" may not be said
until the gate passes.** Silent breakage in these modules does not crash — it quietly
changes numbers, and wrong numbers end up in the paper. The gate is the tripwire.

## When to use

- Any edit lands inside `{{critical_modules}}` — run the gate before reporting completion.
- The gate is red and you must decide: bug, or intentional formulation change?
- A new module is becoming result-critical and should enter the gate's scope.

## When NOT to use

- Changes outside `{{critical_modules}}` (orchestration, plotting, docs) — the general test
  suite and review suffice; do not inflate the gate's scope with noise.
- As a substitute for the full test suite — the gate is a fast, named correctness contract,
  not total coverage.
- Verifying a scientific claim — that is the `verifier` agent (the gate checks the machinery,
  not the conclusion).

## Runbook

1. **Detect scope contact**: `git diff --name-only HEAD` filtered against
   `{{critical_modules}}`. No contact → done, no gate needed.
2. **Run the gate fresh**: `{{gate_command}}`. Never reuse a previous run's output.
3. **Green** → state the result with numbers ("gate: N tests passed") and proceed.
4. **Red** → stop all completion claims and branch:
   - **Bug** — the change broke pinned behavior. Fix until green, then step 2 again.
   - **Intentional formulation change** — the pinned expectations themselves must move.
     Get explicit user approval, update the gate's tolerances/pins *in the same change*,
     record the decision (`decision-log`), and only then report green. **Passing silently by
     loosening a tolerance without approval is the one unforgivable move.**

## What a good gate looks like

Verified patterns from working practice (adapt, don't copy blindly):

- **Analytic pins**: small scenarios with hand-derivable expected values, asserted within a
  stated tolerance (e.g. ±2%).
- **Cross-form parity**: when two independent implementations of the same computation exist
  (a production form and a reference form), the gate asserts they agree on shared scenarios —
  the strongest silent-breakage detector available.
- **Oracle checks**: an independent, simpler computation (closed-form case, brute-force
  small instance) that the main machinery must reproduce.
- **Divergence assertions**: where two quantities *should* differ by design, assert that they
  do — agreement would mean a collapsed distinction.

A gate of a few dozen focused tests that runs in minutes beats a thousand-test suite nobody
runs before claiming "done".

## Enforcement (documented, not shipped)

This pack ships no executable hooks. If your harness supports lifecycle hooks, the exemplar
pattern is a *stop hook*: on turn end, diff the working tree against `{{critical_modules}}`;
on contact, run `{{gate_command}}`; on failure, block the completion claim and feed the last
~25 lines of test output back with the bug-or-intentional question. Implement it in your
project if you want mechanical enforcement; this skill is the discipline either way.

## Rules

1. **The gate list is closed and named.** `{{critical_modules}}` is declared in the config
   block, not inferred per-turn; changing the list is a decision-log entry.
2. **Red gate = no "done", no "ready", no "works".** Not in commit messages, not in chat,
   not in the build log.
3. **Tolerance/pin updates require approval and a decision entry.** The gate's expectations
   are part of the project's scientific record.
4. **A red gate blocks phase closure** (`phase-gate` step 2) regardless of checklist state.
5. **Keep the gate fast.** A slow gate gets skipped; move slow scenarios to the nightly/full
   suite and keep the gate under a few minutes.

## Configuration

- `{{critical_modules}}` — glob list of result-critical paths.
- `{{gate_command}}` — the single command that runs the gate (e.g.
  `pytest tests/test_correctness.py`).

## Provenance & maintenance

Generalized from a named correctness-gate rule and its stop-hook enforcement in a working
computational-research repository (scope-diff → gate-run → red-means-bug-or-intentional
protocol, cross-form parity testing, tolerance-update-with-approval); see the pack's
`examples/` directory for the worked exemplar mapping. The gate patterns listed are verified
practice; the hook sketch is a description of working code, shipped here as documentation
only.

Re-verify in your project:

- `{{gate_command}}` — runs and is green on a clean tree (a red gate on main is an
  emergency, not a baseline).
- `git diff --name-only HEAD | grep -E '<critical pattern>'` — the scope filter actually
  matches your critical paths.
- `time {{gate_command}}` — still fast enough to run on every touch.
