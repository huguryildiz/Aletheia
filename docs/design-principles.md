# Design principles

Four principles govern everything in this pack. They are constraints, not aspirations —
each one has a "what it forbids" clause, and pull requests are reviewed against them.

## 1. Ground-truth only

Every command, path, format, and claim in a skill was verified against a real repository —
either the exemplar it was harvested from or (for canon-authored skills) working practice —
and **inference is labeled as inference**. Each skill's "Provenance & maintenance" section
states what was verified and gives one-line re-verification commands.

*Forbids*: plausible-but-unverified runbook steps; documenting a flag nobody ran; provenance
sections that cite nothing. A wrong runbook is worse than no runbook — it spends the
reader's trust exactly when they followed it.

## 2. State is derived, not stored

There is no mutable central status file — no `.aletheia-state.json`, no "current phase"
field anywhere. Status drifts the moment it is hand-maintained. Gate verdicts live in
immutable evidence (`results/<name>_<date>/meta.json`, write-once build-log closures, git
history) and are **re-derived on demand** — that is exactly what the `session-historian`
agent does at session start.

*Forbids*: adding a state file to the pack or to an adopter scaffold; a layout document
that says "we are in phase 3"; skills that cache verdicts instead of recomputing them.

## 3. No source mutation

Agents never write. The three shipped agents are strictly read-only reporters — auditing,
digesting, refuting — and log/decision writing is a *skill* action performed in the main
session where the human can see it. The generator writes only in its post-approval scaffold
phase, and never overwrites without showing the file first. And the exemplar repository the
pack was mined from was never modified by this project.

*Forbids*: writer agents in the pack (runners/implementers are documented patterns, not
shipped components); an agent that "helpfully" fixes the drift it found; scaffolding
before approval.

## 4. Markdown only

The pack ships **discipline as instructions, not enforcement as scripts**. No Python, no
shell, no executable hooks — the only non-markdown files are declarative data:
`.claude-plugin/plugin.json` (manifest) and `templates/results-meta.schema.json` (a JSON
Schema). Where mechanical enforcement is worth having (stop hooks for the correctness gate,
pre-edit guards for canonical params), the skill *documents the pattern* and the adopter
implements it in their own harness.

*Why*: instructions are model- and harness-portable, auditable at a glance, and cannot
acquire dependencies, platforms, or CVEs. Claude is the runtime — adoption is done by
*invoking* the `skill-library-generator` skill, which scaffolds via file tools at
invocation time.

*Forbids*: `bootstrap.sh`, `generator.py`, shipped hook scripts, vendored binaries.

## The portability bar

Domain content lives in **exactly one file**: [../examples/uwsn-ankc.md](../examples/uwsn-ankc.md).
Skills and templates must read naturally in a domain that has no solver at all — the pack is
stress-tested against foreign domains (e.g. molecular dynamics, climate modeling,
bioinformatics, ML training), and any skill that only makes sense next to an optimization
model gets demoted to the examples file.

Mechanical gate, run before every release (must return zero matches):

```bash
grep -ri "bellhop\|milp\|kappa\|acoustic\|uwsn\|gurobi\|cp-sat" skills templates
```

Consequence: skills and templates refer to the exemplar namelessly ("see the pack's
`examples/` directory") — only the README and `docs/` may link it by name.
