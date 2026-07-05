# Core vs Extended — what the tiers mean

Every skill carries a `tier` in its frontmatter. The split is about *adoption pressure*,
not importance.

## Core (11) — `tier: core`

The everyday operating discipline. These were **harvested from a working research
repository** (nine directly from its practiced rules and skills, two — `environment-lock`,
`data-fingerprint` — promoted from that project's own gap audit as the highest-value
reproducibility levers). A project adopting Aletheia is expected to run all of Core from
day one; each one exists because its absence produced a real failure mode.

`project-layout` · `layer-sync` · `decision-log` · `build-log` · `phase-gate` ·
`correctness-gate` · `canonical-params` · `environment-lock` · `data-fingerprint` ·
`evidence-convention` · `research-methodology`

## Extended (6) — `tier: extended`, `status: recommended`

The reproducibility-and-positioning canon: authored against computational-science best
practice, grounded in the exemplar where it practiced them. Recommended, adopted
deliberately — a small exploratory project may defer some; a project writing a paper should
be running all six by submission time.

`reproducibility-provenance` · `statistical-reporting` · `numerical-determinism` ·
`negative-results-ledger` · `notebook-vs-script` · `external-positioning`

## Generator (1) — `tier: generator`

`skill-library-generator` — the meta-skill that binds the pack to a repo and mines
project-local skills. Run at adoption and quarterly thereafter.

## Work-type routing (mirror)

The operative copy of this table lives in the adopter's `CLAUDE.md`
([templates/CLAUDE.md](../templates/CLAUDE.md)) so it is always loaded; this is the
documentation mirror. **Default is the minimum; escalation is conditional. Never turn a
small change into bureaucracy.**

| Work type (trigger) | Default (do this) | Escalate to … when … |
|---|---|---|
| small exploration | notebook + light note (`notebook-vs-script`) | — (stays light) |
| reusable experiment / real run | script + `evidence-convention` (results dir + meta) | + `environment-lock` & `data-fingerprint` when it feeds a paper figure/claim or must be reproduced by others |
| critical logic change | `correctness-gate` (run the named gate) | + `canonical-params` when it touches protected defaults; + `decision-log` when a red gate is an *intentional* formulation change |
| stochastic run | record seeds (`reproducibility-provenance`) | + `numerical-determinism` when results must be bit-reproducible / cross-machine |
| numeric claim / result | `statistical-reporting` (replication + interval) | + `verifier` agent when the claim is load-bearing (goes in the paper); + `external-positioning` when it is a novelty claim |
| phase conclusion | `phase-gate` checklist | + `build-log` when it is a real milestone, not a trivial sub-step |
| assumption / default change | `decision-log` entry | + `layer-sync` when it touches ≥ 2 layers; + `canonical-params` when it is a canonical default |
| dead end / failed attempt | one-line `negative-results-ledger` entry | — (stays light) |

## Agents (3) — read-only auditors

`session-historian` (state digest), `drift-auditor` (layer sync), `verifier` (adversarial
claim refutation). All strictly read-only reporters: they write nothing; log/decision
writing is a *skill* action in the main session. Writer agents (runners, implementers) are
deliberately out of scope — execution automation is project-specific workflow; the generic
patterns are documented in [../examples/uwsn-ankc.md](../examples/uwsn-ankc.md).
