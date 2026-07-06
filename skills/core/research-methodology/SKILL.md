---
name: research-methodology
description: >-
  Use when shaping how research work is conducted and claimed — setting the evidence bar for "done", pre-registering expected numbers before a run, deciding whether an idea becomes an experiment or gets retired, choosing test density for new code, or calibrating how much process a change deserves. Also use at session start after a gap. Trigger phrases: "what should we expect before running", "is this claim backed", "adopt or retire this idea", "how much testing does this need", "pre-register the hypothesis", "process for this change".
tier: core
---

# research-methodology

The connective discipline over all other skills: what counts as evidence, when a hypothesis
must commit to numbers, how ideas enter and leave the project, and how much process a given
change deserves. The stance: **claims follow verification, predictions precede runs, negative
results are findings, and ceremony scales with consequence — never with enthusiasm.**

## When to use

- Before a run: forcing the "what do we expect?" question into writing.
- Before a claim: checking the evidence bar is met.
- Triaging an idea: probe it, adopt it, or retire it?
- Writing new code: deciding test density.
- Session start after a gap: rehydrating state from the record.

## When NOT to use

- Executing the specific rituals this skill routes to — closure (`phase-gate`), run
  recording (`evidence-convention`), decision capture (`decision-log`) have their own skills.
- Statistical mechanics of reporting (replications, intervals) — `statistical-reporting`.

## The evidence bar

1. **Never claim "done / works / ready" without fresh verification output** — a test count,
   a gate result, a measured number, an artifact link. If verification wasn't run this turn,
   the claim is a forecast; label it as one.
2. **Report outcomes faithfully.** Tests red → say so with the output. Step skipped → say
   so. A softened failure costs more than a failure.
3. **A rigorous negative result is a finding.** Infeasibility, a null effect, a dead end —
   recorded verbatim with evidence — is a legitimate deliverable and a valid gate artifact
   (see `negative-results-ledger`); softening it to pass a gate is falsification-lite.

## Predictions precede runs

Before any kept campaign, write the expectation into the run's meta file (the `expectation`
field, see `evidence-convention`): the predicted direction, rough magnitude, and — when the
design anticipates branches — the pre-registered branch ("if the window is empty, that
confirms X; the comparison arm then runs at relaxed points"). Hypotheses that predict
numbers before running are falsifiable; hypotheses fitted to output afterward are captions.

## Idea lifecycle

- **Probe** — a one-off question runs as a notebook or script-level flag
  (`notebook-vs-script`), never by editing defaults (`canonical-params`). Cheap, disposable,
  logged lightly.
- **Adopt** — the probe changed a default, a method, or the plan → `decision-log` entry with
  evidence linked; propagation owed to the other layers (`layer-sync`).
- **Retire** — the idea failed or lost → one-line `negative-results-ledger` entry (why it
  died, pointer to evidence). Retired ideas stay findable so they are not re-attempted from
  scratch.

An idea that is neither adopted nor retired after its probe is an open loop — close it.

## Test density (where tests are owed)

One question decides: **"can this code fail silently and corrupt a result?"**

- **Yes — result-critical code** (core computations, data transforms feeding claims):
  high density, analytic pins, cross-checks; lives inside `{{critical_modules}}` under the
  `correctness-gate`.
- **Sometimes — shared utilities**: a handful of sanity tests at the boundaries.
- **No — orchestration, plotting, one-offs**: skip; their failures are loud or their outputs
  are inspected visually.

Do not write defensive-raise tests, trivial shape/type tests, or subsets of existing tests —
test count is not the metric; silent-failure coverage is.

## Ceremony scales with consequence

Default is the minimum; escalation is conditional (the full work-type routing table ships in
the pack's `templates/CLAUDE.md`):

- small exploration → notebook + light note — nothing more;
- kept campaign → `evidence-convention` (+ env/data fingerprints when it feeds a claim);
- critical-logic change → `correctness-gate` (+ `decision-log` if pins move intentionally);
- numeric claim → `statistical-reporting` (+ adversarial `verifier` when load-bearing);
- phase end → `phase-gate` (+ `build-log` for real milestones);
- dead end → one ledger line.

Never turn a small change into bureaucracy; never let a paper-bound claim skip the ritual.

## Session hygiene

After a gap, rehydrate from the record — the build log's latest entries, recent git history,
the current TODO buffer — not from memory (dispatch the `session-historian` agent where
available). Memory of a project is a cache with no invalidation; the record is the source.

## Configuration

- `{{critical_modules}}`, `{{gate_command}}` — the test-density high tier.
- `{{decision_log}}`, `{{build_log_dir}}`, `{{evidence_dir}}` — the record surfaces.

## Provenance & maintenance

Generalized from the working principles of a mature computational-research repository:
the silent-failure test-density rule and its module table, the evidence bar and
faithful-reporting norms, pre-registered expectations in campaign meta files (including a
pre-registered branch that fired and became a primary finding), the
probe-vs-default-edit separation, and record-first session starts. See the pack's
`examples/` directory for the worked exemplar mapping. The routing summary mirrors the
pack's config-block table (single source: `templates/CLAUDE.md`).

Re-verify in your project:

- `grep -h "expectation" {{evidence_dir}}/*/meta.json | head -3` — campaigns carry
  pre-registered expectations.
- `{{gate_command}}` — the high-density tier is green.
- `ls {{build_log_dir}} | tail -1 && git log --oneline -5` — the rehydration record exists
  and is current.
