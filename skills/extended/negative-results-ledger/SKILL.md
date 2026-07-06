---
name: negative-results-ledger
description: >-
  Use when an idea, approach, or experiment fails, dead-ends, or gets abandoned — recording it in one line so it is never re-attempted from scratch and never silently buried. Also use when a negative or infeasibility result might itself be a finding, and when auditing a project for unrecorded dead ends. Trigger phrases: "that didn't work", "abandon this approach", "record the dead end", "why didn't we try X" , "we tried that before", "the result was negative".
tier: extended
status: recommended
---

# negative-results-ledger

Dead ends are expensive knowledge — burying them buys the same failure twice. The contract:
**every abandoned approach leaves at least one line** — what was tried, why it died, where
the evidence is — in a place the next person (or the same person, six months later) will
actually search. And a *rigorous* negative result is promoted, not just logged: infeasibility
with evidence can be a primary finding.

## When to use

- An approach is being abandoned — algorithmic idea, modeling variant, tooling attempt,
  data source that didn't pan out.
- A run produced a negative/null/infeasible outcome and someone is tempted to "just not
  mention it".
- Before starting something that feels familiar: check the ledger first.
- Pre-paper sweep: which dead ends belong in the text (limitations, "we also tried")?

## When NOT to use

- Bugs — a broken implementation is fixed or filed, not memorialized as a negative result.
  Only record it here if the *approach itself* was abandoned because of what the bug
  revealed.
- Deferred-not-dead ideas — those are `decision-log` entries with status `deferred`.
- Every failed exploratory cell in a notebook — the ledger records abandoned *directions*,
  not every red cell on the way.

## The ledger

A single tracked file (recommended: `docs/negative_results.md`), newest first, one line per
entry — with a link when evidence exists:

```markdown
- YYYY-MM-DD — **<what was tried>**: <why it died — one clause>. Evidence: <link or "none, reasoning only">. See D<NN> if a decision was involved.
```

The bar for an entry is deliberately low (one line, ≤30 seconds); the bar for *skipping* one
is high — "too minor to record" is how the same dead end gets re-explored quarterly.

## Escalation ladder (one line is the floor, not the ceiling)

1. **One-liner** (default) — the ledger line above.
2. **Rejected decision** — the dead end settled a real design question → `decision-log`
   entry with status `rejected`; the ledger line points to it.
3. **Build-log entry** — the failure came from a real campaign with numbers → the evidence
   and its interpretation get a `build-log` entry (write-once, citable), and the ledger line
   points to it.
4. **Primary finding** — the negative result *answers the research question* (an
   infeasibility that proves a constraint is binding, a null that kills a hypothesized
   effect). Treat it as a first-class result: full evidence chain, statistical treatment,
   pre-registered branch honored (`research-methodology`), and a place in the paper.

## Rules

1. **Never soften, never bury.** Recording a negative result verbatim is a norm the
   `phase-gate` enforces (a rigorous negative is a valid closure artifact); deleting a
   failed branch without a ledger line is the violation.
2. **"Didn't work" needs one clause of *why*.** "Too slow at realistic sizes", "assumption
   X false in our data", "upstream data unusable" — the why is what prevents the re-attempt,
   and it distinguishes *abandoned* from *abandoned prematurely*.
3. **Date everything.** A dead end from an old code era may deserve a revisit; the date is
   what makes that judgment possible.
4. **Check before you start.** The ledger is read at idea-triage time
   (`research-methodology` idea lifecycle) — a hit does not forbid retrying, it demands
   engaging with why it died last time.
5. **Negative results are publishable material.** The limitations section, the "approaches
   we ruled out" paragraph, and sometimes the headline finding come straight from this
   ledger — keep entries paper-quality honest.

## Configuration

- `{{decision_log}}`, `{{build_log_dir}}`, `{{evidence_dir}}` — escalation targets.

## Provenance & maintenance

Authored from the research-hygiene canon (file-drawer effect countermeasures, tried-and-
failed registries), grounded in working practice: a decision log with an explicit `rejected`
status kept in place rather than deleted, infeasible cells recorded verbatim as data, and a
pre-registered infeasibility branch that fired and was promoted to the project's primary
finding rather than smoothed away. See the pack's `examples/` directory for the worked
exemplar mapping.

Re-verify in your project:

- `test -f docs/negative_results.md && head -5 docs/negative_results.md` — the ledger
  exists and is current (adapt the path).
- `grep -c "rejected" {{decision_log}}` — rejected decisions are recorded, not deleted.
- Ask "what did we abandon this quarter?" — if the answer is from memory rather than the
  ledger, the discipline has lapsed.
