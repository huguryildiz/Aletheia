---
name: external-positioning
description: >-
  Use when a claim is about to face the outside world — classifying what is novel versus known, verifying every citation actually exists and says what it is cited for, scoping claims to what the evidence supports, and holding the reproducibility bar before anything enters a draft. Trigger phrases: "is this novel", "position against the literature", "check the citations", "are we over-claiming", "ready for submission", "what's our contribution".
tier: extended
status: recommended
---

# external-positioning

The project's claims will be read by skeptical strangers. This skill keeps the external
story honest before it ships: novelty is bookkept rather than felt, citations are verified
rather than pattern-matched, claim strength is scoped to evidence strength, and nothing
enters a draft that a reviewer could not reproduce from the record.

## When to use

- Writing or reviewing contribution statements, abstracts, related-work sections.
- Adding any citation to the project record.
- A claim is about to travel — paper draft, talk, README, funding text.
- Pre-submission: the full positioning + citation + reproducibility sweep.

## When NOT to use

- Internal decisions and their rationale — `decision-log`.
- The statistical form of a result — `statistical-reporting`.
- Whether the figures regenerate — `reproducibility-provenance` (this skill *checks* that
  bar was met; it does not implement it).

## Novelty bookkeeping

Keep a claims ledger (a section in the paper-planning doc or a standalone file): each
paper-bound claim classified and anchored —

- **novel** — no prior work found doing this; the search that failed to find it is recorded
  (venues/queries/date), because "we found nothing" is an auditable statement;
- **known, applied** — exists elsewhere, new in this setting; cite the origin;
- **confirmation / negative** — replicates or refutes something; cite what it tests.

A novelty claim without a recorded search is a feeling with formatting. Re-run the search
near submission — the literature moved while you worked.

## Citation integrity

1. **Verify every citation individually**: the work exists, the identifier (DOI/archive ID)
   resolves, the bibliographic fields match, and the work actually supports the sentence
   citing it.
2. **Distrust bulk-generated bibliographies.** Machine-assembled reference lists fabricate
   plausible entries; the verified protocol is one-at-a-time lookup against the source of
   record, never a batch of citations accepted on pattern.
3. **Abstract-only reading cannot carry a load-bearing claim.** A source skimmed at
   abstract level may be cited for existence ("prior work considers X"), never for a
   specific result or number until the relevant full text is read; track the read-status
   and clear the debt before submission.
4. **Citation debt is tracked, not remembered** — unresolved/abstract-only entries carry an
   explicit marker in the draft so they cannot silently survive to camera-ready.

## Claim scoping (honesty labels)

Scope every claim to its evidence tier, in the text itself:

- calibrated measurement → claim the number;
- physics/theory-grounded model without calibration → claim *shape and ranking*, label the
  absolute values "to be calibrated";
- design operating point → say so ("chosen design point", not "optimal");
- single-setting evidence → claim the setting, not the universe ("in our configuration").

Over-claiming is the cheapest thing a reviewer can catch and the most expensive to walk
back; the label costs one clause.

## The reproducibility bar (before any claim travels)

A claim may enter a draft only when its chain is complete: evidence directory with meta
(`evidence-convention`), environment + data fingerprints (`environment-lock`,
`data-fingerprint`), seeds (`reproducibility-provenance`), statistical treatment
(`statistical-reporting`), and regenerable figures. The pre-submission sweep re-checks the
chain end-to-end for every headline claim.

## Rules

1. **The contribution list is written against the ledger**, not from memory — every "we are
   the first to X" traces to a recorded search.
2. **Negative and boundary results go in the story** — a mapped dead end or a binding
   constraint (`negative-results-ledger`) positioned honestly reads as rigor, not weakness.
3. **Every number in the abstract exists in a table** with N and uncertainty behind it.
4. **Fix the source, then the story.** When positioning review finds an unsupported claim,
   the evidence gets strengthened or the claim gets weakened — the wording never bridges
   the gap alone.

## Configuration

- `{{evidence_dir}}`, `{{decision_log}}` — where claim chains and their decisions live.

## Provenance & maintenance

Authored from the scholarly-integrity canon (novelty auditing, citation verification,
calibrated claim language), grounded in working practice: a one-at-a-time identifier
verification protocol adopted after machine-generated references were caught fabricating
entries; an explicit full-text-before-submission obligation for abstract-only sources; and
shipped claims scoped as physics-grounded shape/ranking with absolute calibration labeled
future work. See the pack's `examples/` directory for the worked exemplar mapping.

Re-verify in your project:

- Pick two random bibliography entries; resolve their identifiers and check they support
  their citing sentences.
- `grep -rn "TODO.*cite\|abstract-only\|UNVERIFIED" docs/ | head` — citation debt is marked,
  and shrinking.
- For one headline claim, walk the chain: draft sentence → table → evidence dir → meta →
  seeds. Any missing link fails the bar.
