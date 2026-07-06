# ALETHEIA — Audit Remediation Design

**Date**: 2026-07-06
**Source**: `audit/aletheia_fable_audit.md` (Claude Fable 5 audit, commit `75f4bc2`)
**Scope**: full 10-item roadmap from audit §10, sequenced into three waves
**Status**: design — approved for planning

---

## 1. Context

The Fable audit judged ALETHEIA "a strong but overbuilt skill pack" whose *ideas are
credible but proof is absent*. Its five protected primitives (correctness-gate, evidence
convention + schema, decision-log, lit-anchor anti-fabrication, routing-with-escalation)
are sound; what holds the pack back is a threefold gap:

1. **No adoption or trigger-reliability evidence** — the product's actual failure mode
   (does the right skill fire at the right moment on a non-exemplar repo?) is never tested.
2. **Several claims outrun their mechanism** — "mechanical" portability gate that is a
   placeholder grep, "enforced" discipline that is prompted behavior, auditor verdicts
   typeset like tool output.
3. **The taxonomy is larger than its distinct ideas** — 18 skills carry ~10–11 disciplines,
   with real overlap.

This design turns audit §10's prioritized roadmap into an executable, sequenced plan.
It changes none of the audit's conclusions; it commits to them.

## 2. Goals / Non-goals

**Goals**
- Close all 10 roadmap items (§10), preserving every idea (per §9's "no idea lost").
- Make the pack's own founding principle — *ground-truth over assertion* — true of the
  pack's own product claims.
- Keep the markdown-only thesis intact (no shipped hooks in core).

**Non-goals**
- No new disciplines invented beyond the audit.
- No enforcement adapter repo (audit "optional long-term", explicitly out of scope here).
- No abandoning the core/extended idea set — only regrouping per §9.

## 3. Approach — launch-credibility first (audit-forced ordering)

Three waves. The ordering is not a preference; audit §10 makes item 6 (taxonomy) depend on
items 1–4 shipping first ("don't churn during launch"), and items 9 & 10 depend on 6.
Items 2 (honesty pass) and 6 (refactor) both touch `README.md`, `templates/CLAUDE.md`, and
`docs/core-vs-extended.md`, so they are serialized, not parallelized.

```
Wave 1  Launch credibility (P0 + CI)      surface frozen while marketed
Wave 2  Structural hardening (P1)          after Wave 1 ships
Wave 3  Retention & evidence (P2)          after skill set is stable
```

---

## 4. Wave 1 — Launch credibility

Parallelizable, low-risk, no structural churn. Freezes the public surface once done.

### 4.1 Honesty pass (audit §6 items 2,3,4,6,8; roadmap #2)
Pure wording. Fix the five over-claims + label authored verdict strings:
| Claim | Fix |
|---|---|
| "holds the claim until the interval is reported…" (`README.md` hero ×2) | "the discipline directs the agent to hold the claim until…" |
| "your first **enforced** discipline" (`docs/quickstart.md:4-5`) | "your first practiced discipline / your first gate" |
| "**every** runbook step was verified against a real repository" (`README.md:155-156`) | mirror `core-vs-extended.md`'s honest core-vs-extended split |
| "adapts the library to **any** research repository" (`plugin.json`, `marketplace.json`) | "to computational-research repositories" + document gate-command shape assumption |
| example gate-verdict strings (`monte-carlo-pi.md:71`, `a2g-pathloss-3gpp.md:99-100`) | in-page label: "verdict as the agent should phrase it — the artifacts, not the string, are the evidence" |

**Verify**: grep the repo for each old phrasing → zero hits; the two manifests still validate.

### 4.2 README golden path above the fold (§7; roadmap #4)
Insert the five-line golden path (install → 2-question bind → gate green before "done" →
keep a run with pre-registered expectation → phase-gate verifies checklist) above the
etymology/hero/philosophy. Link `docs/quickstart.md` from the first screen.
**Verify**: first screenful of `README.md` answers "what does this do to my Tuesday?".

### 4.3 Portability gate made real (§3 portability; roadmap #3)
Either commit `docs/portability-vocab.txt` (the domain-term denylist) and wire the grep
into CI, **or** delete the word "mechanical" from `README.md:173-174` + `CONTRIBUTING.md:12-14`.
Decision: **commit the list + CI** (keeps the strongest repeated claim true).
**Verify**: the grep runs verbatim in CI against `skills/` + `templates/` and passes.
Depends on 4.4 (CI skeleton).

### 4.4 Minimal CI (roadmap #5)
`.github/workflows/ci.yml` with single-command jobs the repo already documents but never runs:
symlink integrity, relative-link check, JSON/schema validity (3 manifests + `results-meta.schema.json`),
`claude plugin validate --strict`, and the portability grep (4.3).
**Verify**: CI green on a clean checkout; deliberately breaking a symlink turns it red.

### 4.5 Adoption transcript — the single highest-leverage artifact (§5, §8; roadmap #1)

**Subject repo**: the real UWSN k-connectivity codebase currently at `examples/Codes`
(MATLAB + Python), behind the *published* paper "Mitigating Energy Cost of Connection
Reliability in UWSNs Through Non-Uniform k-Connectivity" (IEEE doc 11143186). Published →
public exposure is fine and the example can cite the DOI (also feeds `lit-anchor`).

**Why this repo is better than a tidy Python exemplar**: it is MATLAB-first, has a
non-standard layout, and has *no single fast shell-invocable gate*. Running the generator
here stress-tests the binding's weakest assumption in public (§3 portability, §6 gap 6:
"batch-scheduled / non-`src/tests` repos don't fit `{{gate_command}}`"). One artifact closes
three audit gaps: adoption evidence + structural-portability proof + gate-command honesty.

**Pre-process — two layers (approved boundary):**
1. **Mandatory cleanup (hygiene + size + privacy), BEFORE running the generator:**
   remove `.DS_Store`, `Cagla.zip` (5 MB), the 15 MB `Results-2024-09-25` dump, heavy
   `.eps`/`.fig` output; keep source (`.m`, `.py`, `Model/`, `solutions_*.csv`) + one small
   `Results-*` sample; strip any personal data; rename `Codes/` → `uwsn-k-connectivity/`.
   Slimmed subject lands < ~1 MB.
2. **NO structural re-architecting (deliberate):** leave the MATLAB messiness, the dated
   `Results-*` folders, and mixed naming *as-is* so the generator's read-only discovery is
   genuine. The transcript states honestly what was removed for size/privacy and that the
   layout the generator saw is otherwise the real repo.

**Deliverables (committed):** the slimmed `examples/uwsn-k-connectivity/` subject; the
generator run `examples/adoption-transcript.md` (annotated, observed-vs-inferred labels
preserved); the resulting scaffold diff (generated `CLAUDE.md` + any local skills + an
example `results/<name>_<date>/meta.json` with a pre-registered expectation); a
"where `{{gate_command}}` did not fit a MATLAB batch workflow" section.
`examples/README.md` updated to list it as the third *real* worked example.
**Verify**: transcript is reproducible in spirit; scaffold's `gate_command` (or its honest
absence) is documented; no removed-for-size file is implied to still exist.

---

## 5. Wave 2 — Structural hardening (after Wave 1 ships)

### 5.1 Taxonomy simplification 18 → 13, per §9 exactly (roadmap #6)
Group by artifact governed, not tier. Recorded as decision-log entries D04+ (dogfoods the
ADR discipline on a real design decision). Re-symlink the Codex surface, bump the 3 manifests
in lockstep, collapse routing to one canonical copy.

| §9 group | Skills | Change |
|---|---|---|
| The record (3) | `decision-log`, `build-log`, `negative-results-ledger` | unchanged |
| The gates (2) | `correctness-gate`, `phase-gate` | unchanged |
| The run (3) | `evidence-convention`, **`run-provenance`** (merge `environment-lock` + `data-fingerprint` + seeds-half of `reproducibility-provenance`), `numerical-determinism` (kept separate) | merge 3→1 + keep 1 |
| The claims (3) | `statistical-reporting`, `lit-anchor` (sole citation authority), `external-positioning` (citation section deleted; figure-regeneration bar absorbed from `reproducibility-provenance`) | de-dupe |
| The workspace (2) | `project-layout` (absorbs `notebook-vs-script` as a "placement + notebook discipline" section), `layer-sync` | merge 2→1 |
| Meta (1 + demotion) | `skill-library-generator`; `research-methodology` → `docs/methodology.md` | demote to doc |

Routing table: exactly one canonical copy (`templates/CLAUDE.md`); `core-vs-extended.md`
links to it instead of mirroring; the prose copy dies with `research-methodology`'s demotion.
**Verify**: 13 skill dirs; Codex symlink surface re-checked (all 120000, none broken);
3 manifests same version; `grep -r` finds one routing table; no dangling skill references.

### 5.2 Auditor coverage footers + verifier rename (§5; roadmap #7)
- `drift-auditor`: mandatory "coverage" footer (files opened, greps run) so a ✅ verdict is
  falsifiable.
- `verifier`: rename passing verdict `CONFIRMED` → `SURVIVED REFUTATION (N angles tried)`;
  require enumerating refutation angles *not* tried.
- `session-historian`: label the age/source of the copied "Test total" line.
**Verify**: each agent's output spec now requires the coverage/angles/age field.

### 5.3 Windows / symlink caveat (§3; roadmap #8)
Document in `docs/install.md` Path B/C that a Windows checkout without developer mode /
`core.symlinks=true` yields text files, plus a copy-instead-of-symlink manual fallback.
**Verify**: install doc names the failure and the workaround.

---

## 6. Wave 3 — Retention & evidence (after skill set is stable)

### 6.1 `aletheia-doctor` re-audit mode (roadmap #9)
Generator-scope mode: check an adopted repo's bindings still resolve — `gate_command` runs,
declared paths exist, gate is green on a clean tree. Files: `skill-library-generator/SKILL.md`,
`docs/adopting-in-a-new-project.md`. Depends on 5.1 (stable skill set).
**Verify**: running it on the Wave 1 adoption scaffold reports resolve/green or names the gap.

### 6.2 Trigger-reliability corpus (§3, §8; roadmap #10)
Recorded prompt→skill-fired trials for the core skills (even ~10 each), committed as evidence
with honest methodology. Addresses the product's actual unknown (does routing fire?) and
enables tuning noisy `description` triggers. Depends on 5.1.
**Verify**: committed trials with a stated method; at least the noisy everyday-speech triggers
("that didn't work", "let's just check this number") have a measured fire/no-fire record.

---

## 7. Dependency graph

```
4.4 CI ─────► 4.3 portability gate
4.1, 4.2, 4.5 ── independent, parallel ──┐
                                         ▼
        (all Wave 1 shipped) ────► 5.1 taxonomy ────► 6.1 doctor
                                         │            └► 6.2 trigger corpus
                                   5.2, 5.3 independent
```

## 8. Risks

- **Over-cleaning the adoption subject** kills its evidentiary value → mitigated by the
  two-layer pre-process boundary (§4.5): hygiene yes, re-architecting no.
- **Taxonomy refactor churn during launch** → mitigated by sequencing 5.1 strictly after
  Wave 1 and after the honesty pass touches the shared files.
- **Counterfeit ceremony** (agent emits verdict strings without running anything) is a
  pack-wide failure the audit names but this remediation only *reduces* (labeling authored
  strings, verifier rename); it does not eliminate it. Called out, not solved, in scope.

## 9. Success criteria (whole effort)

A serious lab's three unanswered questions (§11) now have answers:
1. *One repo that isn't the exemplar running this* → the UWSN adoption transcript.
2. *Skills actually fire when they should* → the trigger-reliability corpus.
3. *No claim exceeds the mechanism* → the honesty pass + real portability gate + CI.
Plus: 13 skills (size matches idea count) and a doctor mode (self-maintenance by the pack's
own rules).
