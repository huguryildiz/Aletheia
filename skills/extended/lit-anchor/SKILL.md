---
name: lit-anchor
description: >-
  Use when assembling or adding to a bibliography, citing prior work, or making a novelty or absence claim — especially with AI assistance, which fabricates plausible-but-fake DOIs, titles, and authors. Governs DOI-verified, small-step literature anchoring so no unverified citation enters the record. Trigger phrases: "add a citation", "find references for", "cite prior work", "is this novel", "no one has done", "the literature says", "build the bibliography", "related work".
tier: extended
---

# lit-anchor

Every citation is a claim that a specific work exists and says a specific thing. AI assistants
produce **plausible-but-fabricated** references — real-looking DOIs that resolve to nothing, or to
a different paper; correct-sounding titles with invented authors or years. A bulk "give me twenty
references" response is a **draft to verify, never a result**. This skill is the discipline that
keeps a fabricated citation out of your paper.

## When to use

- Assembling or extending a bibliography / related-work section.
- Adding a single citation to support a claim.
- Making a **novelty or absence claim** ("no prior work does X", "we are the first to…").
- Any moment an AI hands you a formatted, confident-looking citation.

## When NOT to use

- Summarizing or reasoning about a paper you already hold — that is reading, not sourcing.
- Internal cross-references to your own artifacts (use `layer-sync` / `decision-log`).

## Runbook

1. **Treat every AI-produced identifier as a hypothesis.** A DOI, title, author list, year, or
   venue emitted by a model is unverified until resolved against an authoritative source.
2. **Verify one citation at a time.** Resolve each DOI/URL against a real source (the DOI
   resolver, the publisher page, an indexed search) and confirm **title + authors + year + venue**
   all match. Do not batch — batching is where fabrications hide.
3. **Main agent synthesizes; sub-agents fetch small pieces.** Never delegate "produce the
   verified bibliography" to a sub-agent that returns a finished, verified-looking table — that is
   exactly the pattern that launders fabrications. Sub-agents retrieve single documents; the main
   agent assembles and vouches.
4. **Mark unverified and abstract-only sources explicitly.** An abstract-only source carries a
   documented "full text before submission" debt; an unresolved citation is flagged, never
   silently included.
5. **Back absence claims with a documented search.** "No prior work does X" requires the actual
   queries run and their date recorded — not a model's confidence.

## Rules

1. **No fabricated identifiers.** Every DOI/URL in the record resolves to the exact claimed work.
2. **Bulk AI citation output is a draft.** It enters the record only after per-item verification.
3. **Every citation carries provenance:** where it was verified and the as-of date; trained
   knowledge about a paper is a hypothesis about the present, not an observation.
4. **Absence/novelty claims are search-backed**, with the search recorded.
5. **A citation that will not resolve after a documented search is dropped or flagged** — never
   quietly kept because it "looks right".

## Configuration

- `{{bibliography}}` — where verified citations live (e.g. `docs/references.bib`, a notes file).
- `{{claim_log}}` — optional: where novelty/absence claims and their backing searches are recorded.

## Provenance & maintenance

Generalized from a working computational-research repository's DOI-verification protocol, adopted
after a bulk literature-review sub-agent was caught emitting fabricated references: the fix was
small-step manual retrieval with one-by-one resolution and main-agent synthesis, plus an
explicit abstract-only debt on sources not yet read in full. See the pack's `examples/` directory
for the worked exemplar mapping.

Re-verify in your project:

- Resolve every identifier in `{{bibliography}}` and confirm the resolved metadata matches the
  entry (a stale or redirected DOI is a silent corruption).
- Confirm each novelty/absence claim in `{{claim_log}}` still has its backing search recorded.
