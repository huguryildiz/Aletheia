---
name: canonical-params
description: >-
  Use when a change would touch the project's canonical operating point — the protected default parameter values that all results are reported against — or when a "let's just try X" probe risks editing a default instead of passing a script-level argument. Trigger phrases: "change the default", "try a different value", "tweak the operating point", "why is this parameter frozen", "can I edit the constants".
tier: core
---

# canonical-params

A results-producing project has a *canonical operating point*: the named set of default
parameter values (`{{canonical_values}}`) that every reported result implicitly assumes.
Changing one of them outside a declared sweep silently forks the project's evidence base —
yesterday's figures and today's no longer describe the same system. The contract: **protected
defaults change only inside a sweep or with explicit user approval, and every approved change
leaves a record.**

## When to use

- Any edit that touches a file or value listed in `{{canonical_values}}`.
- A "let's quickly try X" impulse during exploration.
- Reviewing a diff that changes a constants/preset/config-default file.
- Deciding whether a new parameter should join the protected set.

## When NOT to use

- Sweep code that *parameterizes over* a value without changing its default — that is the
  intended mechanism, not a violation.
- Free parameters explicitly documented as unpinned (still record them per run in the meta
  file — see `evidence-convention`).
- One-off script arguments (`--threshold 0.9`) — encouraged; that is exactly where probes
  belong.

## Runbook

1. **Identify contact.** Does the edit touch `{{canonical_values}}` (the file, or a frozen
   token inside it)? No → proceed normally.
2. **Classify the intent:**
   - **Temporary probe** → do not edit the default. Revert, and pass the value as a
     script/CLI/notebook argument instead. Defaults are not a scratchpad.
   - **Intentional permanent change** → stop and get explicit user approval *before* the
     edit.
3. **On approval:** make the edit, write a `decision-log` entry (old value → new value, why,
   what evidence motivated it), and update the document that fixes the operating point
   (typically a build-log entry recording how the point was chosen).
4. **Check the blast radius.** A changed canonical value can invalidate cached artifacts,
   stored baselines, and every figure produced at the old point — state in the decision's
   Impact section what must be re-run, and let `layer-sync` hold you to it.

## Enforcement (documented, not shipped)

The exemplar pattern is a *pre-edit hook*: intercept file edits; if the target path is in
the protected set AND the edited text matches a frozen-token pattern (specific parameter
names, preset identifiers), block the edit and print the probe-vs-permanent instructions
from the runbook. Mechanical enforcement catches the honest mistake; this skill is the
discipline either way. This pack ships documentation only, no executable hooks.

## Rules

1. **The protected set is named, small, and closed.** List the files (and ideally the exact
   tokens) in the config block. A protected set nobody can enumerate protects nothing.
2. **Probes never edit defaults.** Script-level parameters exist precisely so exploration
   does not touch the canon.
3. **Every approved change = decision entry + operating-point document update.** The
   canonical point is part of the scientific record; an undocumented change is drift with a
   timestamp.
4. **Results cite their operating point.** Run meta files record the canonical-values hash
   (see `data-fingerprint`), so "which defaults produced this number?" always has one answer.
5. **Fixed-by-finding beats fixed-by-fiat.** When a canonical value is chosen from a
   measured sweep, link the sweep evidence; when it is a design guess, label it honestly as
   "to be calibrated".

## Configuration

- `{{canonical_values}}` — path(s) holding protected defaults, plus optional frozen-token
  list (e.g. `src/config/canonical.py`).
- `{{decision_log}}`, `{{evidence_dir}}` — where changes and their motivating evidence land.

## Provenance & maintenance

Generalized from an operating-point protection rule and its pre-edit guard hook in a working
computational-research repository (probe-vs-permanent branching, script-level
parameterization for probes, approval-plus-record on permanent change); see the pack's
`examples/` directory for the worked exemplar mapping. The runbook and rules are verified
practice; the hook sketch documents working code without shipping it.

Re-verify in your project:

- `git log --oneline -5 -- {{canonical_values}}` — every commit touching the canon should
  pair with a decision entry; spot-check the latest.
- `grep -n "<frozen token>" {{canonical_values}}` — the protected tokens still live where
  the config block says they do.
- `grep -rn "expectation\|canonical" {{evidence_dir}}/*/meta.json | head -5` — runs record
  the operating point they assumed (adjust field names to your meta schema).
