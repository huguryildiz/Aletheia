---
name: statistical-reporting
description: Use when a numeric result is about to be reported, compared, or put in a paper — enforcing replication counts, uncertainty intervals, paired comparisons on matched instances, and visible denominators. Also use when designing how many runs a claim needs. Trigger phrases: "is this difference real", "how many replications", "report with confidence intervals", "single run result", "compare method A vs B", "is N=3 enough".
tier: extended
status: recommended
---

# statistical-reporting

**Never report a single run as a result.** A number from one draw of a stochastic system is
an anecdote; a claim is a distribution summarized honestly: center, spread, replication
count, and — for comparisons — a paired design with the pairing stated. This skill governs
how numbers become claims.

## When to use

- A numeric result is entering a build-log entry, a decision's evidence, or a paper draft.
- Designing a campaign: choosing the replication unit and count before launch.
- Comparing methods, configurations, or arms.
- Reviewing a draft for naked point estimates.

## When NOT to use

- Deterministic quantities (an exact count, a closed-form value, a proven bound) — report
  the value; intervals around determinism are theater.
- Exploratory probes not yet feeding a claim — but promote them through this skill before
  they do.
- Choosing seeds/realization mechanics — `reproducibility-provenance`.

## Runbook

1. **Declare the replication unit before running** — what varies across replications
   (random instances, seeds, data splits, noise draws) and what stays fixed. The unit
   defines what population the claim generalizes to.
2. **Set N in the run contract**, not after seeing results. Working default: ~10
   realizations per cell for expensive computations, more when cheap; the honest minimum is
   whatever supports the interval you intend to report.
3. **Run paired where comparing.** All arms see the *same* realization list (same instances,
   same seeds); report per-realization differences, not differences of aggregates.
4. **Summarize with center + spread + N**: median (or mean) with an interquartile band /
   bootstrap CI / standard error — and N visible in every table and caption. For small N or
   unknown distributions prefer rank-based tests (e.g. paired signed-rank) over normality
   assumptions.
5. **Keep denominators visible.** Failed, infeasible, and timed-out cells are part of the
   result: "median over the 6/10 realizations that solved; 4 infeasible (recorded)" — never
   silently condition on success (`evidence-convention` rule 5).
6. **Report direction, magnitude, and uncertainty** — not a bare p-value. A significant
   difference of negligible size and a non-significant trend are both reportable truths;
   say which you have.

## Rules

1. **One run, no claim.** A single-realization number may appear only as a labeled
   illustration ("representative realization"), never as the result.
2. **The comparison set is declared in advance** (the run contract / `expectation` field —
   see `research-methodology`). Comparisons invented after seeing the numbers are labeled
   post-hoc and carry no confirmatory weight.
3. **No selective replication.** Adding realizations until the test passes, or dropping
   "unlucky" seeds, is p-hacking with extra steps; N is fixed by the contract, deviations
   are recorded.
4. **Match before you compare.** Arms differing in more than the treatment (different
   instances, different budgets) produce differences with no interpretation; matching is a
   design property, not a statistical patch.
5. **Uncertainty from the right variance.** Spread across realizations ≠ spread within one
   realization's iterates; state which is shown.
6. **Small-N humility.** With N ≤ 5, report the raw per-realization table alongside any
   summary — readers can then judge for themselves.

## Configuration

- `{{evidence_dir}}` — campaign outputs and per-realization tables.

## Provenance & maintenance

Authored from the statistical-reporting canon for computational experiments (replication,
pairing, visible denominators, rank-based small-N tests), grounded in working practice: a
campaign design of ~10 realizations per cell with paired rank-based comparison across arms
on identical realization lists, infeasible cells recorded verbatim as findings, and
per-realization difference tables computed post-hoc from the evidence CSVs. See the pack's
`examples/` directory for the worked exemplar mapping.

Re-verify in your project:

- `grep -h "seeds\|realizations" {{evidence_dir}}/*/meta.json | head -3` — N is declared in
  the contract, not improvised.
- Spot-check a recent table/caption for center + spread + N all present.
- `grep -rn "INFEASIBLE\|TIMEOUT\|failed" {{evidence_dir}}/*/README.md | head` — denominators
  are recorded, not conditioned away (adapt status names).
