---
name: evidence-convention
description: >-
  Use when launching any computational campaign whose results will be kept, cited, or decided upon — sweeps, batch runs, Monte Carlo draws, precomputes — and when auditing for "dark runs" (results that exist only in caches, scratch dirs, or chat logs). Defines where evidence lands and what a run must record. Trigger phrases: "where do the results go", "record this run", "write the meta file", "dark run", "promote these results", "run report".
tier: core
---

# evidence-convention

**No dark runs.** A result that exists only in a gitignored cache, a scratch directory, a
terminal scrollback, or a chat transcript is not evidence — it is a rumor with numbers. The
contract: **every kept campaign lands in `{{evidence_dir}}/<name>_<YYYY-MM-DD>/` with a
`meta.json`, and what the repo tracks is the record (meta + curated summaries), not the
bulk.**

## When to use

- Launching a sweep, batch run, sampling campaign, or precompute whose output will be kept.
- A decision, build-log entry, or paper claim is about to cite a run — does the run have an
  evidence directory?
- Auditing the project for dark runs.
- Writing the run report after a campaign finishes.

## When NOT to use

- Small exploratory probes — those are notebook work (`notebook-vs-script`); the convention
  starts when a result will outlive the session.
- Pure cache regeneration with no new claim attached (caches are inputs, not evidence — but
  see `data-fingerprint` for their keys).

## The convention

1. **One directory per campaign**: `{{evidence_dir}}/<name>_<YYYY-MM-DD>/`.
2. **`meta.json` is mandatory.** Minimum fields (schema: `templates/results-meta.schema.json`):
   - `task` — what this campaign is, with a pointer to the plan item or contract it executes;
   - `git_commit` + `git_tree_clean_at_launch` — code identity;
   - config hash + input-data hashes (see `data-fingerprint`);
   - environment fingerprint (see `environment-lock`);
   - parameters/grid actually run, seeds/realization list;
   - `expectation` — what was predicted **before** running (see `research-methodology`);
   - `status` and pointers to output files.
   If the script does not write `meta.json` itself, the runner writes it by hand — absence
   of tooling is not absence of obligation.
3. **Bulk outputs may be gitignored; the record is tracked.** Track `meta.json`, a README
   with the key numbers, and curated summary files (explicit force-add per the project's
   gitignore policy). If output logs stay ignored, embed the load-bearing numbers in the
   tracked README — a claim must not depend on an untracked file.
4. **Preflight before long campaigns**: `{{gate_command}}` green; tree clean (or the dirty
   state explicitly waived and blob-hashed); environment native-arch verified. A red gate
   aborts the launch.
5. **Failed and degenerate cells are data.** Infeasible points, timeouts, divergences, and
   empty windows are recorded verbatim with their counts — never re-run with a nudged grid
   to make them disappear, and never dropped silently. A truncated or skipped portion gets
   an explicit "not done / dropped" note in the run report.
6. **Run report** at completion: command, wall time, output directory, status distribution
   table (per-cell outcomes and counts), anomalies, and the not-done list.

## The runner role (documented pattern)

Working practice separates **deciding** from **running**: campaigns are executed by a runner
(a person, a subagent, or a script harness) under a written task contract — entry point,
grid/axes, seeds, time limits, output directory, definition of done. The runner runs and
records; it never reformulates the model, never edits source or protected defaults, never
alters the grid beyond the contract, and stops to report anomalies instead of "fixing" them.
This pack ships no writer agents — the pattern is documented here and in the pack's
`examples/` directory; implement the role with whatever executes runs in your project.

## Rules

1. **A claim without an evidence directory is treated as unverified** — by `phase-gate`
   (item stays OPEN), by `decision-log` (Impact cannot cite it), and by reviewers.
2. **Caches are not records.** Scratch/cache dirs hold reproducible intermediates; evidence
   dirs hold what claims rest on. Promoting from cache to evidence is a deliberate act that
   produces a meta file.
3. **Name by content and date**, `<name>_<YYYY-MM-DD>/` — discoverable by `ls`, sortable by
   time, no "final_v2_really".
4. **The expectation field is written before launch.** Post-hoc "expected" values are
   predictions in name only.
5. **Anomaly patterns are flags to report, not noise to smooth** — a status-rate split
   across seed batches, cells far above the median cell time, cache misses forcing recomputes.

## Configuration

- `{{evidence_dir}}` — evidence root (default `results/`).
- `{{gate_command}}` — preflight gate.

## Provenance & maintenance

Generalized from a working repository's runner discipline and audit history — the convention
exists because an audit found kept results living only in gitignored caches ("dark runs"),
and the fix (evidence dirs + mandatory meta + tracked key numbers) is enforced there as an
acceptance criterion. The meta-field minimum mirrors a real campaign meta file; the
run-report shape mirrors the exemplar runner's report format. See the pack's `examples/`
directory for the worked exemplar mapping.

Re-verify in your project:

- `ls {{evidence_dir}} | grep -E '_[0-9]{4}-[0-9]{2}-[0-9]{2}$'` — campaigns follow the
  naming convention.
- `find {{evidence_dir}} -maxdepth 2 -name meta.json | wc -l` — evidence dirs carry meta
  files (compare with the dir count).
- `git ls-files {{evidence_dir}} | head` — the record layer (meta/READMEs/summaries) is
  actually tracked, not just present on disk.
