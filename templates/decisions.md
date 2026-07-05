<!-- markdownlint-disable MD024 -->
# Decision Log

The project's significant decisions + their rationale. This file is a **summary** (ADR-lite);
each entry links to detailed background instead of containing it. It is the project's
authority layer: when code, docs, and notebooks disagree, this file arbitrates
(see the `layer-sync` skill).

## Conventions

- **Status**: `accepted` (in force) / `superseded` (obsolete — link the successor) /
  `rejected` (tried, abandoned) / `deferred` (postponed past the current target)
- New decision → added at the top; a superseded entry stays in place, only its status changes
- Conclusions, not discussion; follow the links for detail
- Numbers are assigned at write time (next free number), never reserved in advance

Ordering: date (new → old). Undated decisions (in force since project founding) at the bottom.

---

## D02 — {{One-line imperative title}}

**Status**: accepted
**Date**: {{YYYY-MM-DD}}

**Context**: {{Why the question arose — 2–5 sentences, linking the triggering artifact
(plan item, audit finding, notebook, failing gate).}}

**Decision**: {{The resolution, as numbered items when it has parts. State values
explicitly; name the losing alternative and, in one line, why it lost.}}

**Impact**: {{Which layers must change (spec section, module, notebook, status board);
whether any protected default changed; what evidence backs the choice (link run dirs or
build-log entries).}}

---

## D01 — Adopt the Aletheia operating discipline

**Status**: accepted
**Date**: {{YYYY-MM-DD}}

**Context**: The project needs a written operating discipline before results accumulate:
where evidence lands, what gates a "done" claim, how decisions propagate.

**Decision**: Adopt the Aletheia skill pack. Bindings live in the config block in
`CLAUDE.md` (critical modules, gate command, canonical values, evidence dir, layers).

**Impact**: `CLAUDE.md` config block filled; `docs/build_log/`, `results/` conventions
active from the first run. This entry is the log's founding record — replace or follow it
with real decisions.
