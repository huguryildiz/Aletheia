# Aletheia Wave 1 — Launch Credibility Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the P0 "credibility" bundle from the audit — make no product claim exceed its mechanism, put the payoff above the fold, make the portability gate real and CI-checked, and commit one real adoption transcript — so a serious lab takes the pack seriously.

**Architecture:** Documentation / repository remediation, not application code. "Tests" are verification commands (grep returning zero hits, CI jobs green, JSON validating, manifests unchanged in version). Each task ends with a verifiable check and a commit. No skill bodies change in Wave 1 (the taxonomy refactor is Wave 2) — the public surface is frozen after this wave while it is marketed.

**Tech Stack:** Markdown, JSON manifests, GitHub Actions (bash), `python3` (arm64) for JSON/schema validation, the Aletheia `skill-library-generator` skill itself (for Task 5).

## Global Constraints

- **Markdown-only thesis holds** — no shipped hooks/scripts in `skills/`; the only new executable is CI (`.github/workflows/`) and one throwaway preprocess step.
- **Single source of truth** — never edit a symlinked copy under `plugins/aletheia/skills/`; edit sources under `skills/…` and `agents/…`.
- **Do not bump `version: 0.1.0`** in any of the three manifests during Wave 1 — no skill set changes here.
- **No domain terms in `skills/` or `templates/`** — Task 2 makes this checkable; do not introduce any while editing.
- **Commit message co-author trailer** (per repo convention): `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`
- **Push target:** direct to `main`, no PR.
- **Spec:** `docs/superpowers/specs/2026-07-06-aletheia-audit-remediation-design.md` (Wave 1 = §4).

---

## File Structure

| File | Responsibility | Task |
|---|---|---|
| `.github/workflows/ci.yml` | Symlink integrity, relative-link check, JSON/schema validity, plugin-validate, portability grep | 1, 2 |
| `docs/portability-vocab.txt` | Newline-delimited denylist of domain terms forbidden in `skills/`+`templates/` | 2 |
| `docs/design-principles.md` | Replace placeholder grep with the real one pointing at the vocab file | 2 |
| `CONTRIBUTING.md` | Reword "mechanical gate" claim to match the shipped mechanism | 2 |
| `README.md` | Honesty pass (hero captions, design-principle 1, provenance para) + golden path above the fold | 3, 4 |
| `docs/quickstart.md` | "enforced" → "practiced" | 3 |
| `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` | "any research repository" → "computational-research repositories" | 3 |
| `examples/monte-carlo-pi.md`, `examples/a2g-pathloss-3gpp.md` | Label authored gate-verdict strings as agent phrasing, not tool output | 3 |
| `examples/uwsn-k-connectivity/**` | Slimmed real subject repo (from `examples/Codes`) | 5 |
| `examples/adoption-transcript.md` | Annotated generator run + scaffold diff + gate-command-fit section | 5 |
| `examples/README.md` | List the adoption transcript as the third *real* worked example | 5 |

---

## Task 1: Minimal CI skeleton

**Files:**
- Create: `.github/workflows/ci.yml`

**Interfaces:**
- Produces: a `checks` job other tasks extend (Task 2 adds the portability step).

- [ ] **Step 1: Write the CI workflow (verification job first)**

Create `.github/workflows/ci.yml`:

```yaml
name: ci
on:
  push: { branches: [main] }
  pull_request:
jobs:
  checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Codex symlink surface is intact (all present, none broken)
        run: |
          set -euo pipefail
          # every entry under plugins/aletheia/skills must be a symlink that resolves
          broken=$(find -L plugins/aletheia/skills -type l -print)
          if [ -n "$broken" ]; then echo "BROKEN SYMLINKS:"; echo "$broken"; exit 1; fi
          n=$(find plugins/aletheia/skills -type l | wc -l | tr -d ' ')
          echo "symlinks resolving: $n"
          test "$n" -ge 20 || { echo "expected >=20 symlinks, got $n"; exit 1; }

      - name: Relative markdown links resolve
        run: |
          set -euo pipefail
          fail=0
          while IFS= read -r md; do
            # extract ](target) links that are not http/mailto/anchor-only
            grep -oE '\]\(([^)]+)\)' "$md" | sed -E 's/^\]\(//; s/\)$//' | while IFS= read -r link; do
              case "$link" in
                http*|mailto:*|\#*) continue ;;
              esac
              target="${link%%#*}"                       # strip #anchor
              [ -z "$target" ] && continue
              dir=$(dirname "$md")
              if [ ! -e "$dir/$target" ] && [ ! -e "$target" ]; then
                echo "DEAD LINK in $md -> $link"; exit 3
              fi
            done || fail=1
          done < <(git ls-files '*.md')
          test "$fail" -eq 0

      - name: Manifests and schema are valid JSON
        run: |
          set -euo pipefail
          for f in .claude-plugin/plugin.json .claude-plugin/marketplace.json \
                   plugins/aletheia/.codex-plugin/plugin.json \
                   templates/results-meta.schema.json; do
            python3 -c "import json,sys; json.load(open('$f')); print('ok', '$f')"
          done

      - name: results-meta schema is a valid JSON Schema
        run: |
          set -euo pipefail
          python3 -m pip install --quiet jsonschema
          python3 -c "import json,jsonschema; jsonschema.Draft202012Validator.check_schema(json.load(open('templates/results-meta.schema.json'))); print('schema ok')"

      - name: Plugin validate (best-effort; runs only if the CLI is present)
        run: |
          if command -v claude >/dev/null 2>&1; then
            claude plugin validate --strict || exit 1
          else
            echo "claude CLI not present in CI runner — skipping (run locally before release)"
          fi
```

- [ ] **Step 2: Run the checks locally to verify they pass on current tree**

Run each block's logic locally (bash):
```bash
cd /Users/huguryildiz/Documents/GitHub/aletheia
find -L plugins/aletheia/skills -type l -print            # expect: no output
find plugins/aletheia/skills -type l | wc -l              # expect: >= 20 (audit says 22)
for f in .claude-plugin/plugin.json .claude-plugin/marketplace.json plugins/aletheia/.codex-plugin/plugin.json templates/results-meta.schema.json; do python3 -c "import json; json.load(open('$f')); print('ok','$f')"; done
```
Expected: no broken symlinks, `>=20` count, four `ok` lines.

- [ ] **Step 3: Deliberately break a symlink to prove the check fails, then restore**

```bash
mv plugins/aletheia/skills/decision-log /tmp/_dl_test 2>/dev/null || true
find -L plugins/aletheia/skills -type l -print            # expect: prints the now-broken link (non-empty)
mv /tmp/_dl_test plugins/aletheia/skills/decision-log 2>/dev/null || true
find -L plugins/aletheia/skills -type l -print            # expect: empty again
```
Expected: the middle command prints a broken link; the last prints nothing. (If the symlink target name differs, adjust — the point is to observe a red→green transition.)

- [ ] **Step 4: Commit**

```bash
git add .github/workflows/ci.yml
git commit -m "ci: add minimal integrity checks (symlinks, links, JSON, schema, plugin-validate)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
git push origin main
```

- [ ] **Step 5: Confirm CI is green on GitHub**

Run: `gh run list --workflow=ci.yml --limit 1`
Expected: latest run `completed  success`. If red, read `gh run view --log-failed` and fix before continuing.

---

## Task 2: Make the portability gate real

**Files:**
- Create: `docs/portability-vocab.txt`
- Modify: `.github/workflows/ci.yml` (add portability step)
- Modify: `docs/design-principles.md:65-69` (real grep)
- Modify: `CONTRIBUTING.md:13-14` (reword claim)

**Interfaces:**
- Consumes: the `checks` job from Task 1.
- Produces: `docs/portability-vocab.txt` — one forbidden domain term per line, `#` comments allowed.

- [ ] **Step 1: Create the denylist**

Create `docs/portability-vocab.txt` (domain proper nouns that must never appear in the generic layer; example-domain terms are fine in `examples/` which is NOT scanned):

```text
# Domain-vocabulary denylist for the portability gate.
# The gate greps skills/ and templates/ for these (case-insensitive, word-boundary)
# and must return ZERO matches. Add a term when a domain noun risks leaking into
# the generic layer. Do NOT add generic infrastructure words (CUDA, solver, seed).
# --- source project (UWSN k-connectivity) ---
UWSN
underwater
k-connectivity
sonobuoy
acoustic modem
# --- example domains (legit only inside examples/) ---
3GPP
UMa-AV
UMi-AV
path loss
tokamak
plasma
VQE
ansatz
climate ensemble
molecular dynamics
binding free energy
```

- [ ] **Step 2: Run the gate against the current tree — observe it passes**

```bash
cd /Users/huguryildiz/Documents/GitHub/aletheia
grep -riwEf <(grep -vE '^\s*#|^\s*$' docs/portability-vocab.txt) skills templates && echo "LEAK FOUND (fix)" || echo "clean (zero matches)"
```
Expected: `clean (zero matches)`. If a term leaks, that is a real finding — remove the domain term from the offending `skills/`/`templates/` file (not from the denylist) and note it in the commit.

- [ ] **Step 3: Wire the gate into CI**

In `.github/workflows/ci.yml`, add this step to the `checks` job (after the schema step):

```yaml
      - name: Portability gate — no domain terms in skills/ or templates/
        run: |
          set -euo pipefail
          terms=$(grep -vE '^\s*#|^\s*$' docs/portability-vocab.txt)
          if grep -riwE "$(echo "$terms" | paste -sd'|' -)" skills templates; then
            echo "Domain vocabulary leaked into skills/ or templates/"; exit 1
          fi
          echo "portability gate: clean"
```

- [ ] **Step 4: Replace the placeholder grep in the docs**

In `docs/design-principles.md`, replace the placeholder code block (currently):
```bash
grep -riE "<your project's domain vocabulary — solver names, model terms, place names>" skills templates
```
with:
```bash
# denylist lives in docs/portability-vocab.txt; CI runs this on every push
grep -riwE "$(grep -vE '^\s*#|^\s*$' docs/portability-vocab.txt | paste -sd'|' -)" skills templates
```

- [ ] **Step 5: Reword the CONTRIBUTING claim to match the mechanism**

In `CONTRIBUTING.md` item 2, change:
> a **mechanical gate requires zero domain vocabulary there**.

to:
> a **CI portability gate** (denylist in `docs/portability-vocab.txt`) **requires zero domain vocabulary there**.

- [ ] **Step 6: Commit and confirm CI green**

```bash
git add docs/portability-vocab.txt .github/workflows/ci.yml docs/design-principles.md CONTRIBUTING.md
git commit -m "ci: make the portability gate real (committed denylist + CI grep)

Backs the repo's most-repeated 'mechanical gate' claim with a runnable check.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
git push origin main
gh run list --workflow=ci.yml --limit 1   # expect: completed success
```

---

## Task 3: Honesty pass — no claim exceeds its mechanism

**Files:**
- Modify: `README.md` (lines 42, 46, 156, 174)
- Modify: `docs/quickstart.md:5`
- Modify: `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`
- Modify: `examples/monte-carlo-pi.md:71`, `examples/a2g-pathloss-3gpp.md:99-100`

**Interfaces:** none (pure wording).

- [ ] **Step 1: README hero captions — Aletheia "holds" → the discipline "directs"**

In `README.md` line 42 (alt text) change `Aletheia holds the claim until the interval is reported and the seed logged.` → `The discipline directs the agent to hold the claim until the interval is reported and the seed logged.`

In `README.md` line 46 (caption) change `the gate holds the claim until the interval is reported and the seed logged.` → `the discipline directs the agent to hold the claim until the interval is reported and the seed logged.`

- [ ] **Step 2: README design-principle 1 — scope the "every runbook step" claim**

In `README.md` lines 156-157, replace:
```
1. **Ground-truth only** — every runbook step was verified against a real repository; inference
   is labeled as inference, and a wrong runbook is worse than none.
```
with:
```
1. **Ground-truth only** — core runbook steps were harvested from a working repository;
   extended steps were authored from canon and grounded where that repository practiced them
   (see [core-vs-extended.md](docs/core-vs-extended.md)). Inference is labeled as inference,
   and a wrong runbook is worse than none.
```

- [ ] **Step 3: README provenance paragraph — "mechanical gate" → the real mechanism**

In `README.md` line 174, change `a\nmechanical gate requires that skills/ and templates/ contain **zero domain terms**.` to reference the CI gate:
> That source project's identity and vocabulary are deliberately excluded from the shipped pack: a **CI portability gate** (denylist in [`docs/portability-vocab.txt`](docs/portability-vocab.txt)) requires that `skills/` and `templates/` contain **zero domain terms**.

- [ ] **Step 4: quickstart — "enforced" → "practiced"**

In `docs/quickstart.md` line 5, change `This page gets you from install to your first\nenforced discipline.` → `This page gets you from install to your first practiced discipline — your first gate.`

- [ ] **Step 5: manifests — "any research repository" → "computational-research repositories"**

In BOTH `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`, change every `adapts the library to any research repository` → `adapts the library to computational-research repositories (git repo, one shell-invocable gate command)`. (There are 2 occurrences in `marketplace.json` — the top `description` and the nested `plugins[0].description`; 1 in `plugin.json`.)

- [ ] **Step 6: examples — label authored verdict strings**

In `examples/monte-carlo-pi.md`, immediately after the line 71 `**Gate verdict:** ...` block, add:
```
> *Verdict as the agent should phrase it — the artifacts (recorded seeds, the CI table, the
> interval), not the string, are the evidence. The string alone proves nothing.*
```
In `examples/a2g-pathloss-3gpp.md`, add the same italic note immediately after its `**Gate verdict:** ...` block (the `✔ CLOSURE VERIFIED` line ~99-100).

- [ ] **Step 7: Verify no over-claim phrasings remain**

```bash
cd /Users/huguryildiz/Documents/GitHub/aletheia
grep -rn "Aletheia holds the claim\|first enforced discipline\|every runbook step was verified\|any research repository\|mechanical gate" README.md docs/quickstart.md .claude-plugin/*.json
```
Expected: **no matches** (all reworded). If any line prints, it was missed — fix it.

- [ ] **Step 8: Confirm manifests still valid JSON**

```bash
for f in .claude-plugin/plugin.json .claude-plugin/marketplace.json; do python3 -c "import json; json.load(open('$f')); print('ok','$f')"; done
```
Expected: two `ok` lines.

- [ ] **Step 9: Commit and push**

```bash
git add README.md docs/quickstart.md .claude-plugin/plugin.json .claude-plugin/marketplace.json examples/monte-carlo-pi.md examples/a2g-pathloss-3gpp.md
git commit -m "docs: honesty pass — no claim outruns its mechanism (audit §6)

Reword 'holds the claim', 'enforced', 'every runbook step', 'any research
repository', 'mechanical gate'; label authored gate-verdict strings as agent
phrasing rather than tool output.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
git push origin main
```

---

## Task 4: README golden path above the fold

**Files:**
- Modify: `README.md` (insert new section between the Overview/hero block and `## Motivation`)

**Interfaces:** none.

- [ ] **Step 1: Insert the five-line golden path**

In `README.md`, immediately BEFORE `## Motivation` (line 49), insert:

```markdown
## What you actually do (five steps)

1. **Install** — `claude plugin install aletheia@aletheia` (or trial one session with `--plugin-url`).
2. **Bind** — "run the skill-library-generator", answer two questions: which modules corrupt
   your results if silently wrong (`critical_modules`), and the one command that must pass
   before "done" (`gate_command`).
3. **Gate** — touch critical code → that command must be green before you call it done.
4. **Keep a run** — `results/<name>_<date>/meta.json`, with the expected outcome written
   *before* you launch.
5. **Close a milestone** — `phase-gate` verifies your written checklist against named artifacts.

Ten-minute tour: [`docs/quickstart.md`](docs/quickstart.md).

```

- [ ] **Step 2: Verify placement and links**

```bash
cd /Users/huguryildiz/Documents/GitHub/aletheia
grep -n "What you actually do" README.md            # expect: a line number ABOVE the "## Motivation" line
grep -n "## Motivation" README.md
```
Expected: "What you actually do" line number < "## Motivation" line number. Confirm the CI relative-link check still passes (the `docs/quickstart.md` link resolves).

- [ ] **Step 3: Commit and push**

```bash
git add README.md
git commit -m "docs: put the five-step golden path above the fold (audit §7)

Answers 'what does this do to my Tuesday?' before etymology/philosophy.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
git push origin main
gh run list --workflow=ci.yml --limit 1   # expect: completed success (link check green)
```

---

## Task 5: Real adoption transcript on the UWSN repo

**Files:**
- Rename/slim: `examples/Codes/` → `examples/uwsn-k-connectivity/` (commit slimmed subject)
- Create: `examples/adoption-transcript.md`
- Modify: `examples/README.md`

**Interfaces:**
- Consumes: the Aletheia `skill-library-generator` skill (run it live against the subject).
- Produces: committed subject repo + transcript + generated scaffold under `examples/uwsn-k-connectivity/`.

**Boundary (from spec §4.5 — approved):** pre-process is *hygiene + size + privacy only*. Do NOT re-architect the layout — the generator must see the real (messy) MATLAB structure so its read-only discovery is genuine.

- [ ] **Step 1: Slim the subject (mandatory cleanup) — remove size/privacy, keep source**

```bash
cd /Users/huguryildiz/Documents/GitHub/aletheia/examples/Codes
# size: drop the 15 MB results dump, the 5 MB zip, top-level binary output
rm -rf "Results-2024-09-25"
rm -f Cagla.zip fig_network_model.eps
# hygiene: strip macOS cruft recursively
find . -name .DS_Store -delete
# keep: *.m, *.py, Model/, solutions_*.csv, one small results sample (Results-2025-05-01,
#       Results-2024-09-15), the .xlsx (16 KB). Verify what remains is small:
du -sh .
```
Expected: remaining size well under ~1 MB. (If `Model/` or a kept `Results-*` still holds heavy binaries, trim those files too — keep representative source/output only.)

- [ ] **Step 2: Privacy scan, then rename the folder**

```bash
cd /Users/huguryildiz/Documents/GitHub/aletheia/examples
# quick scan for anything personal to strip (emails, absolute home paths)
grep -rniE "@(gmail|hotmail|outlook)|/Users/[a-z]+/|[A-Za-z]+\\\\Users\\\\" Codes || echo "no obvious PII"
git mv Codes uwsn-k-connectivity 2>/dev/null || mv Codes uwsn-k-connectivity
```
Expected: no PII (or it is removed); folder renamed. (`git mv` fails silently for untracked files — the `mv` fallback handles that; the rename is then staged as an add.)

- [ ] **Step 3: Commit the slimmed subject BEFORE running the generator**

Committing first gives the transcript a clean "before" baseline and a diff to show.
```bash
cd /Users/huguryildiz/Documents/GitHub/aletheia
git add examples/uwsn-k-connectivity
git commit -m "examples: add slimmed UWSN k-connectivity subject repo for adoption transcript

Real MATLAB/Python repo behind IEEE doc 11143186 (published). Slimmed for
size/privacy only (dropped 15 MB results dump, 5 MB zip, .DS_Store); layout
left as-is so the generator's discovery is genuine.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

- [ ] **Step 4: Run the generator live against the subject; capture the transcript**

Invoke the Aletheia `skill-library-generator` skill with `examples/uwsn-k-connectivity/` as the target repository. As it runs, record verbatim:
- the read-only discovery output, **preserving its observed-vs-inferred labels**;
- the two-question interview and the answers given (critical modules; the gate command — here the honest answer is that the "gate" is a MATLAB figure-regeneration/consistency check, *not* a fast single shell command);
- the proposed scaffold, and your approval;
- the scaffolded files (`CLAUDE.md` config block, `docs/decisions.md` D01, `results/` convention).

Let the generator write its scaffold *into* `examples/uwsn-k-connectivity/` so the committed example shows real output.

- [ ] **Step 5: Write `examples/adoption-transcript.md`**

Structure (fill with the ACTUAL run content — no invented steps):
```markdown
# Adoption transcript — UWSN k-connectivity (real repo)

Subject: examples/uwsn-k-connectivity/ — MATLAB/Python code behind
"Mitigating Energy Cost of Connection Reliability in UWSNs Through Non-Uniform
k-Connectivity" (IEEE doc 11143186, published). Slimmed for size/privacy;
layout unchanged.

## 1. What the generator discovered (read-only)
<paste discovery, observed vs inferred labels intact>

## 2. Interview and bindings
<the two questions + answers; critical_modules; gate_command>

## 3. Where the gate-command binding did NOT fit
This repo has no fast single shell-invocable gate. Its "gate" is a
figure-regeneration + scenario-consistency check over MATLAB scripts. Records
honestly how {{gate_command}} was bound (or left as a documented manual check),
and what that means for the binding's single-fast-command assumption.

## 4. Scaffold produced (diff)
<the CLAUDE.md config block, D01, results/ convention that were written>

## 5. Honest notes
- Files removed before the run (size/privacy) and why.
- What the generator inferred vs. observed, and any binding left as a recommendation.
```

- [ ] **Step 6: List it as the third REAL example**

In `examples/README.md`, add `uwsn-k-connectivity` / `adoption-transcript.md` to the *real* worked examples (alongside `a2g-pathloss-3gpp.md` and `monte-carlo-pi.md`), and note it is the first end-to-end generator adoption on a public repo.

- [ ] **Step 7: Verify links and JSON of any scaffolded meta**

```bash
cd /Users/huguryildiz/Documents/GitHub/aletheia
# any meta.json the generator wrote must be valid JSON
find examples/uwsn-k-connectivity -name meta.json -exec python3 -c "import json,sys; json.load(open(sys.argv[1])); print('ok',sys.argv[1])" {} \;
# transcript's relative links resolve (CI will also enforce)
grep -oE '\]\(([^)]+)\)' examples/adoption-transcript.md
```
Expected: any `meta.json` prints `ok`; links point to existing paths.

- [ ] **Step 8: Commit the transcript + scaffold + README update**

```bash
git add examples/adoption-transcript.md examples/README.md examples/uwsn-k-connectivity
git commit -m "examples: real adoption transcript — generator run on the UWSN repo (audit §5,§8)

First end-to-end generator adoption on a public repo; documents where the
{{gate_command}} single-fast-command assumption did not fit a MATLAB workflow.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
git push origin main
gh run list --workflow=ci.yml --limit 1   # expect: completed success
```

---

## Wave 1 exit check (run before declaring the wave done)

- [ ] CI is green on `main` (`gh run list --workflow=ci.yml --limit 1` → success).
- [ ] `grep -rn "Aletheia holds the claim\|first enforced discipline\|every runbook step was verified\|any research repository\|mechanical gate" README.md docs/quickstart.md .claude-plugin/*.json` → no matches.
- [ ] Portability gate returns zero matches (Task 2 Step 2 command).
- [ ] README first screenful contains the five-step golden path.
- [ ] `examples/adoption-transcript.md` exists, references a committed slimmed subject, and has the gate-command-fit section.
- [ ] No manifest `version` changed from `0.1.0`.

## Self-review notes (spec coverage)

Spec §4.1→Task 3 · §4.2→Task 4 · §4.3→Task 2 · §4.4→Task 1 · §4.5→Task 5. All five Wave 1 items covered. Waves 2 (§5) and 3 (§6) are deliberately deferred to their own plans, written after this wave ships (spec §3 sequencing).
