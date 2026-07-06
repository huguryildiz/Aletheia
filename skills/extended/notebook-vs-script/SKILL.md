---
name: notebook-vs-script
description: >-
  Use when deciding where a piece of computational work belongs — an exploratory one-off versus a reusable pipeline versus library code — and when maintaining the notebook series (numbering, manifest, execute-before-commit) or promoting a notebook into a script. Trigger phrases: "notebook or script", "where does this analysis go", "let's just check this number", "make this rerunnable", "the notebook is stale", "promote this to a script".
tier: extended
status: recommended
---

# notebook-vs-script

Three destinations, one routing rule: **one-off exploration → notebook; reusable pipeline →
script; shared logic → the package.** Each destination rots in a characteristic way when it
receives the wrong work — notebooks rot as un-diffable pipelines, scripts rot as unread
one-offs, and copy-pasted logic rots everywhere at once.

## When to use

- Starting any "let's see this number / check this hypothesis / profile this" probe.
- A notebook is being re-run on demand — promotion time?
- Setting up or auditing the notebook series conventions.
- Reviewing a PR that adds analysis code somewhere questionable.

## When NOT to use

- Deciding whether a run's *outputs* need recording — `evidence-convention` (a notebook
  probe can still produce a kept result; the conventions compose).
- Library-design questions (module boundaries, APIs) — `project-layout`.

## The routing rule

| Work | Destination | Because |
|---|---|---|
| One-off probe, hypothesis check, profiling look | `notebooks/NN_kebab.ipynb` | narrative + figure + result stay in one citable file |
| Repeated runs, CLI arguments, CI/evidence artifacts | `scripts/` | reproducible entry point; notebooks make bad CLIs |
| Logic used by ≥2 callers (or any script + notebook) | `src/<package>/` | single tested copy; copy-paste is the failure mode |

Default for anything exploratory is the notebook; a script is *earned* by re-run demand,
not granted by optimism.

## Notebook discipline

1. **Numbered series with a manifest**: `NN_kebab-topic.ipynb`, numbering append-only, plus
   a `notebooks/README.md` manifest stating each notebook's role and rerun policy (live /
   frozen / archived).
2. **Execute before commit.** A committed notebook carries its outputs — run it end-to-end
   in place (e.g. `jupyter nbconvert --execute --inplace`) so the repo version shows what
   the code actually produces.
3. **Narrative is the point.** Prose cells state the question, the method, and the reading
   of each figure — a notebook that is only code should have been a script.
4. **Cite, don't duplicate.** Notebooks link the decisions and evidence dirs they rest on
   and get cited by build-log entries; they do not become the record themselves.
5. **Archive, don't delete.** A retired series moves to `notebooks/archive/`; its numbers
   are never reused. Historical notebooks pinned to old APIs are narrative, not drift
   (`layer-sync` rule 7).
6. **No library logic in cells.** The moment a function is worth reusing, it moves to the
   package and the notebook imports it.

## Script discipline

1. **CLI arguments, no hardcoded paths** — parameters and output locations are arguments
   with sane defaults, so probes go through flags, not edits (`canonical-params`).
2. **Outputs follow the evidence convention** — a script that produces kept results writes
   into `{{evidence_dir}}/<name>_<date>/` with a meta file.
3. **Scripts orchestrate; the package computes.** A script is argument parsing + calls into
   `src/` + output writing; heavy logic inside a script is library code in hiding.

## Promotion path (notebook → script)

Second manual re-run of the same notebook for fresh outputs = promotion signal. Move the
logic into the package, wrap a CLI script around it, keep the notebook as the narrative
demonstration importing the same functions — and note the promotion in the manifest.

## Rules

1. **Never edit defaults to probe** — a probe is a notebook cell or a script flag, full stop.
2. **A stale committed notebook is a bug** — either re-execute it or mark it frozen/archived
   in the manifest; silent staleness misleads readers.
3. **One question per notebook**, roughly — a notebook answering five questions is five
   notebooks or a pipeline pretending.
4. **Notebook numbering is append-only** — reusing numbers breaks every citation to the old
   one.

## Configuration

- `{{evidence_dir}}` — where script campaigns land.

## Provenance & maintenance

Generalized from a working repository's explicit routing rule (probes to a numbered,
manifest-governed notebook series; reusable pipelines to CLI scripts; shared logic to the
package) and its stated rationale — a notebook keeps narrative, figure, and result in one
citable file, while a lone script goes stale or loses its outputs. Execute-in-place before
commit is verified exemplar practice. See the pack's `examples/` directory for the worked
exemplar mapping.

Re-verify in your project:

- `ls notebooks/ | grep -E '^[0-9]{2}_'` — the series is numbered; `test -f
  notebooks/README.md` — the manifest exists.
- `git diff --stat HEAD -- notebooks/ | tail -1` — committed notebooks change with outputs
  (execute-before-commit leaves its trace).
- `grep -rn "def " scripts/*.py | wc -l` — heavy function definitions in scripts are
  promotion candidates (adapt to your stack).
