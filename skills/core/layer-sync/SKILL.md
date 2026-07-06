---
name: layer-sync
description: >-
  Use when checking whether the project's knowledge layers agree — the decision log, the spec/docs, the code, and the notebooks/reports — after a decision lands, after a refactor, before a phase closes, or when the user asks "is there drift", "did that decision propagate", "are docs and code in sync". Also use to register an explicit doc-to-source anchor link for point-precise checking. Trigger phrases: "sync check", "drift audit", "is the spec up to date with the code", "did D-numbers propagate", "link this doc to this source file".
tier: core
---

# layer-sync

A research project's knowledge lives in ordered layers — typically
`{{doc_layers}}` = decision log → spec/docs → code → notebooks/reports. Any change that
lands in one layer and not the others is *drift*, and drift silently corrupts the paper the
project is building toward. This skill audits a scoped slice of the layers, reports drift
with file:line evidence, and proposes exactly one next action. It never fixes anything in
the same turn.

## When to use

- After a decision-log entry lands (did it reach spec, code, notebooks?).
- After a commit range that touched a documented behavior.
- As a phase-gate step (the `phase-gate` skill calls this before closing).
- When any two layers are suspected to disagree.

## When NOT to use

- "Where are we / what's next" — that is a status question for the `session-historian` agent.
- Verifying a single computed result — that is the `verifier` agent's job.
- General code review, style review, or test-coverage review.
- Fixing the drift — fixes happen in a separate, user-approved turn.

## Scoping the audit

Parse the user's scope; default to `recent`.

| Scope | Meaning |
|---|---|
| `recent` (default) | last ~7 days of commits + last 2 decision-log entries |
| decision scope (e.g. `D15`) | that decision checked across all layers |
| module scope (e.g. `channel`) | one subpackage + the docs/notebooks that reference it |
| commit scope (e.g. `HEAD~3..HEAD`) | what that range changed and where else it must land |
| `links` / `links <id>` | check registered doc↔source anchor pairs only (see below) |

## Runbook

1. Read the layers **in authority order**: `{{decision_log}}` (newest entries first), then
   `git log --oneline -20` (+ `--name-only` for the scope window), then the spec docs and
   `{{build_log_dir}}` (last ~3 entries), then the implementation, then notebooks/reports.
   Read only what the scope needs — for notebooks prefer targeted greps over full parses.
2. For each in-scope decision or change, build a layer-by-layer row: reflected / missing /
   contradicting, with a `file:line` citation for every non-✅ cell.
3. Emit the report:

   ```
   ## Drift audit — <date>
   **Scope**: <…>   **Layers**: <{{doc_layers}}>
   **Verdict**: ✅ in sync | ⚠ drift detected | ❌ contradictions

   | Decision / change | <layer 1> | <layer 2> | <layer 3> | <layer 4> | Status |
   | ... | ✅ | ✅ | ⚠ old term at src/x.py:42 | ✅ | ⚠ |

   ### Drift details (⚠/❌ only)
   - What the authority layer says (cite), what the drifted layer says (cite),
     one concrete suggested fix.
   ```

4. Append **exactly one** next action:
   - ✅ → "no drift — proceed with <next planned item>".
   - ⚠ → the single highest-value fix, phrased as a proposal awaiting approval.
   - ❌ → stop; ask the user which layer is canonical before proposing anything.

## Anchor links (point-precise mode)

For pairs that must never drift (a doc section describing a specific function, a constant
table mirroring a config file), register an explicit link in a small manifest,
`docs/drift_links.yml`:

```yaml
links:
  - id: 1
    doc: docs/<doc>.md        # optionally with a doc_anchor section
    src: src/<file>           # optionally with a #symbol
    note: "what this pair pins"
    created: YYYY-MM-DD
```

Adding a link: verify the doc path exists, the source path exists, and the symbol (if given)
is actually declared in the source (grep for its definition; no match → refuse, show the
grep). Reject duplicates of the same (doc, src, symbol) triple. Removing: by id. The
manifest is the only file this mode ever writes. Audits with scope `links` compare each
pair's *content substance* directly — the manifest says where to look, never what is correct.

## Rules

1. **The decision log is the source of truth.** If code and the decision log disagree, the
   code is the drift — unless the entry is itself marked superseded.
2. **Cite file:line for every drift claim.** "The notebook still has the old form" is not a
   finding; the cell/line reference is.
3. **Read-only audit.** No test runs, no builds, no notebook execution, no edits.
4. **Skip layers that are out of scope for a given decision.** A code-only decision with no
   notebook impact must not be flagged for "missing notebook reference".
5. **Group related drifts** into one row with the missing piece — not N rows for N sub-edits.
6. **Recency bias.** Decisions older than ~30 days (or several numbers back) are assumed
   propagated unless the caller explicitly widens the scope.
7. **Historical narrative is not drift.** A prose cell explaining the *old* form next to code
   using the new form is documentation; flag only executable code that uses a retired form.
8. **Beware short-token renames.** Grep with word boundaries (`\bold_name\b`) — short
   identifiers collide.
9. **One action, not a menu.** Three drifts found → propose the first fix; the rest surface
   on the next audit.
10. **Never soften the verdict letter.** ⚠ and ❌ are load-bearing for the next-action
    branching; do not downgrade them to "minor inconsistency" prose.

## Dispatching to the auditor agent

The pack ships a read-only `drift-auditor` agent implementing exactly this protocol. When
subagents are available, this skill is a thin coordinator: parse the scope, dispatch the
agent, present its report verbatim (do not re-summarize its table), append the single action
line. Do not pre-read layer files before dispatching — that duplicates the agent's work. Do
not run the audit inside another agent; it is a top-level, user-facing flow.

## Configuration

- `{{doc_layers}}` — ordered layer list (default: decisions, spec, code, notebooks).
- `{{decision_log}}` — the authority layer file.
- `{{build_log_dir}}` — build-log directory (part of the docs layer).

## Provenance & maintenance

Generalized from a working four-layer sync discipline (coordinator skill + read-only audit
agent + anchor-link manifest) in a mature computational-research repository; see the pack's
`examples/` directory for the worked exemplar mapping. The scope table, verdict semantics,
and rules 1–10 are verified practice; the YAML manifest schema is copied verbatim from the
exemplar (field names are the convention, not a requirement).

Re-verify in your project:

- `test -f {{decision_log}} && head -40 {{decision_log}}` — the authority layer exists and
  is newest-first.
- `git log --oneline -10 -- <spec doc>` — the spec layer actually changes over time (a
  never-touched spec is itself a drift signal).
- `test -f docs/drift_links.yml && cat docs/drift_links.yml` — anchor manifest present (only
  if you use the links mode).
