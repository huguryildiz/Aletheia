---
name: build-log
description: >-
  Use when a phase completes or a sanity-gate result is being fixed as permanent evidence — writing a new numbered entry under the build-log directory. The bar is high; single-module additions and small changes do not get entries. Trigger phrases: "phase N is done, log it", "the gate passed, record it", "write a build log entry", "completion note", "fix this result as evidence".
tier: core
---

# build-log

Maintain `{{build_log_dir}}` as a write-once series of numbered entries
(`NN_kebab_topic.md`) recording phase completions and gate results *with their numerical
evidence*. The build log is the raw "methods" material for the eventual paper and the
project's replay memory after long gaps — every entry must be worth citing in one of those
two roles.

## When to use

The threshold is deliberately high. Open an entry only for:

- **Phase completion** — all of a phase's modules and tests green, gate passed.
- **Fixing a gate result** — a correctness-gate tolerance update, a first successful
  end-to-end run of new machinery, a first result curve.
- **Documenting a decision's implementation** — the decision itself goes in
  `{{decision_log}}`; the build-log entry carries its *execution and numerical proof*
  (comparison tables, figures, before/after numbers).

**The practical test**: would the paper's methods section, or a future you reconstructing
the project, cite this entry? If no — do not open one.

## When NOT to use

- A single module was added → `git log` + the module's docstring suffice.
- A decision was just written → wait; open the entry when its first implementation +
  evidence exist.
- Transient exploratory probe → notebook (`notebook-vs-script`).
- Refactor / cleanup / docstring pass → the commit message is the record.
- Anything git already records well (commit messages, PR descriptions).

## Numbering and filename

Find the last number: `ls {{build_log_dir}} | grep -E '^[0-9]{2}_' | sort | tail -1`.
New entry = next number, `NN_kebab_topic.md`, topic short: module or main deliverable
(e.g. `09_baseline_comparison.md`).

## Required structure (in order)

```markdown
# <Module or milestone title>

**Date**: YYYY-MM-DD
**Phase**: <N> (short scope)
**Status**: ✅ / 🟡 + one-sentence summary
**Test total**: N passed, M skipped   (from real test-runner output, if applicable)

## Related artifacts

- [path](relative/path) — one-sentence description (evidence dirs, notebooks, decision entries)

## Why this exists            <!-- or: Final configuration / Decision rationale -->

Why it was built or measured, which alternative lost, which reference it rests on.

## What was implemented

| File | Public API | Responsibility |
| --- | --- | --- |
| [`path`](relative/path) | `fn(args) -> ret` | one sentence |

## Tests / evidence

- `tests/test_x.py` — N tests, what they pin down.
- Numerical results as tables (sweep tables, before/after), not prose.

## References

- Spec section, predecessor entry, decision numbers, external sources actually used.
```

## Rules

1. **Write-once.** Entries are immutable evidence; corrections and follow-ups are a new
   entry that references the old one. The single allowed retro-edit: marking the previous
   entry's "next step" pointer as done.
2. **Numbers, not adjectives.** Never "works" / "ready" — write the test count, the gate
   output, the measured value. A claim without a number or an artifact link is filler.
3. **Tables over paragraphs** — mandatory for implemented-module inventories and numerical
   results.
4. **Relative, clickable links** to every artifact named — paths a reader can follow from
   the file's location.
5. **The why-section carries the rationale** — not "added X" but "X solved <problem> because
   <reason>, over <alternative>".
6. **Status markers**: ✅ completed, 🟡 in progress, ⬜ not started (optionally ⚠ at-risk,
   ❌ blocked). Do not invent alternatives.
7. Entries link their evidence in `{{evidence_dir}}` — an entry claiming a run that has no
   evidence directory is treating "it ran fine" as evidence, which the evidence-convention
   skill forbids.

## Configuration

- `{{build_log_dir}}` — the entry directory (default `docs/build_log/`).
- `{{decision_log}}`, `{{evidence_dir}}` — for cross-links.

## Provenance & maintenance

Generalized from a 20+-entry build log in a working computational-research repository
(high-bar entry criteria, header block, artifact list, why-section, implementation table,
write-once discipline); see the pack's `examples/` directory for the worked exemplar
mapping. The structure block mirrors the exemplar's entry template with domain content
removed; the "would the paper cite it" test is verbatim exemplar practice.

Re-verify in your project:

- `ls {{build_log_dir}} | grep -E '^[0-9]{2}_' | sort | tail -3` — numbering is contiguous
  and kebab-cased.
- `grep -L '## References' {{build_log_dir}}/*.md` — entries missing a references section
  (should print nothing).
- `git log --follow --oneline -- {{build_log_dir}}/<oldest entry>` — old entries should show
  no post-creation substantive edits (write-once check).
