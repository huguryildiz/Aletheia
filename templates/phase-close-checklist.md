# Phase Closure Checklist — {{PHASE_NAME}} / {{GATE_ID}}

<!-- Aletheia template: instantiate one per phase in your plan document (or copy at closure
     time). Companion to the phase-gate skill — the ritual verifies THIS written checklist,
     never memory. One OPEN item = no closure. -->

**Phase**: {{name + one-line scope}}
**Gate**: {{gate id / plan row link}}
**Closure attempt date**: {{YYYY-MM-DD}}

## Acceptance criteria (fill at phase START, verify at closure)

| # | Acceptance criterion | Evidence artifact (named at closure) | Status |
|---|---|---|---|
| 1 | {{criterion — testable, with a number where possible}} | {{evidence_dir}}/<run>/ or build-log NN or D-number | ⬜ / ✅ / ❌ OPEN |
| 2 | {{…}} | | ⬜ |
| 3 | Correctness gate green (fresh run) | paste summary line of `{{gate_command}}` output | ⬜ |

Pre-declared off-ramps (legitimate alternative closures, written BEFORE execution):

- {{e.g. "if the feasible window is empty → record as finding, branch to relaxed arm"}}

## Closure ritual (strict order — see the phase-gate skill)

- [ ] 1. Contract loaded from `{{phase_plan}}` (this checklist, not memory)
- [ ] 2. Every criterion verified with a named artifact; `{{gate_command}}` run fresh
- [ ] 3. Decision sweep: owed entries exist in `{{decision_log}}` with real numbers
- [ ] 4. Build-log entry written (links every evidence artifact)
- [ ] 5. Layer-sync audit scoped to this phase — drift fixed (approved) + re-audited
- [ ] 6. Status board updated; `TODO.md` rewritten to the next phase
- [ ] 7. Derived views regenerated (if the project keeps any)
- [ ] 8. User sign-off obtained → then commit

## Verdict

**CLOSED / BLOCKED** — {{open items, or the off-ramp taken}}

| Record | Value |
|---|---|
| Gate test | {{N passed, fresh output summary}} |
| Decisions | D{{n}}, … |
| Build log | {{NN_topic.md}} |
| Layer sync | ✅ / ⚠ (+ fix commit) |
