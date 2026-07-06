---
name: decision-log
description: >-
  Use when a project decision is made or changed — a modeling assumption, a default value, a method choice, a scope cut, a rejected alternative — and it must be recorded as a numbered ADR-lite entry, or when an existing decision is superseded, or when the user asks "why did we choose X" / "is there a decision for this". Trigger phrases: "record this decision", "write an ADR", "add a D-number", "supersede D12", "why is this the default", "log the rationale".
tier: core
---

# decision-log

Keep one append-mostly file — `{{decision_log}}` — holding the project's numbered decisions
with status and rationale. It is the project's authority layer: when code, docs, and
notebooks disagree, the decision log arbitrates (see `layer-sync`). Entries are conclusions,
not discussions; superseded entries stay in place with a changed status so the derivation
chain of the eventual paper stays traceable.

## When to use

- An assumption, default, threshold, data source, or method is chosen — especially anything
  another layer (spec, code, notebook, paper) will depend on.
- A previously accepted decision is replaced, relaxed, or reversed.
- An alternative was seriously evaluated and **rejected** — negative decisions are entries
  too; they stop the team from re-litigating.
- A decision is consciously **deferred** past the current publication target.

## When NOT to use

- Implementation details fully visible in the code and its tests — the diff is the record.
- Transient exploration ("let's see this number") — that is a notebook note
  (`notebook-vs-script`), promoted to a decision only if it changes a default.
- Run evidence and numbers — those live in the build log and `{{evidence_dir}}`; the
  decision entry *links* to them.
- Rewriting history — never edit an old entry's substance; supersede it.

## Entry format

Newest entry at the top, directly under the conventions header. Undated founding
conventions live at the bottom.

```markdown
## D<NN> — <one-line imperative title>

**Status**: accepted | superseded (→ D<MM>) | rejected | deferred
**Date**: YYYY-MM-DD

**Context**: why the question arose — 2–5 sentences, with links to the triggering
artifact (roadmap item, audit finding, notebook, failing gate).

**Decision**: the resolution, as numbered items when it has parts. State values
explicitly ("threshold = 0.85"), name the alternative that lost and in one line why.

**Impact**: which layers must change (spec §, module, notebook, status board), whether any
protected default changed (see canonical-params), and what evidence backs the choice
(link to {{evidence_dir}} run dirs or build-log entries).
```

## Runbook

1. **Find the next free number**: `grep -oE '^## D[0-9]+' {{decision_log}} | sort -V | tail -1`
   and increment. Never reserve numbers in advance; the number is assigned at write time.
2. **Check for a predecessor.** If this decision changes an existing one, write the new
   entry, then edit only the old entry's `Status:` line to `superseded (→ D<new>)`.
3. **Write the entry at the top** in the format above. Conclusion language, not deliberation
   transcripts; link the background instead of pasting it.
4. **Propagate or schedule.** Either update the dependent layers in the same change, or state
   in Impact what remains — the next `layer-sync` audit will hold you to it.

## Rules

1. **One decision per entry.** Two questions resolved together are two entries that
   cross-reference each other.
2. **Statuses are exactly**: `accepted`, `superseded`, `rejected`, `deferred`. A superseded
   entry keeps its body verbatim; only the status line changes.
3. **Every numeric default cites a justification** — a measurement, a reference, or an
   explicit "design operating point, to be calibrated" honesty label. Unjustified constants
   are how silent errors enter papers.
4. **The Impact section is a propagation contract.** Layers it names are what `layer-sync`
   audits; omitting a layer there does not exempt it, it just makes the drift harder to find.
5. **Cite decisions by number everywhere else** (docs, notebooks, commit messages) — "per
   D14" — and gloss the meaning on first use in any document ("the count-matching decision
   (D14)"), so readers never need a lookup table.
6. **Findings can be decisions.** A negative or infeasibility result that fixes the
   project's direction deserves an entry with the evidence linked — do not soften it.

## Configuration

- `{{decision_log}}` — the file (default `docs/decisions.md`).
- `{{evidence_dir}}` — where linked run evidence lives.

## Provenance & maintenance

Generalized from a 50+-entry ADR-lite chain in a working computational-research repository
(newest-on-top ordering, four-status lifecycle, supersede-don't-edit, Impact-as-propagation-
contract); see the pack's `examples/` directory for the worked exemplar mapping. The format
block is the exemplar's structure with domain content removed; the four status values and
the next-free-number rule are verified practice.

Re-verify in your project:

- `grep -oE '^## D[0-9]+' {{decision_log}} | sort -V | tail -1` — highest number = next − 1;
  duplicates mean a numbering collision to fix.
- `grep -cE '\*\*Status\*\*: (accepted|superseded|rejected|deferred)' {{decision_log}}` —
  should equal the entry count.
- `head -20 {{decision_log}}` — the newest entry must be at the top.
