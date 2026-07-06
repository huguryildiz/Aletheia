---
name: data-fingerprint
description: >-
  Use when a run consumes input data — datasets, external downloads, caches, config/constants files — and the run's evidence must record exactly which bytes went in; and when asking "did the data change between these two runs". Also use when registering a new external dataset (source, version, access date) or setting up content-addressed caching. Trigger phrases: "hash the inputs", "did the data change", "which dataset version", "fingerprint the config", "content-addressed cache", "data provenance".
tier: core
---

# data-fingerprint

"Did the data change?" must have one answer, computed, not remembered. The contract: **every
input a kept run consumes — datasets, external files, and the config/constants files that
define defaults — is hashed, and the hashes land in the run's meta file.** Two runs whose
input hashes match consumed the same bytes; two that differ are not comparable until the
difference is explained.

## When to use

- Launching any run that lands in `{{evidence_dir}}` (the meta file needs the hashes).
- Registering a new external dataset in `{{data_dir}}`.
- Investigating a result change: same code, same environment, different number.
- Designing a cache for expensive derived artifacts.

## When NOT to use

- Version-controlled small text inputs — git already fingerprints them; record the commit
  hash instead of duplicating it.
- Pinning package versions — that is `environment-lock`.
- Verifying a computation's correctness — hashing proves *which inputs*, not *right answer*.

## Runbook

1. **Hash inputs at read time**: `shasum -a 256 <file>` (or the in-code equivalent) for every
   dataset file the run reads, recorded as `{"<logical name>_sha256": "<hash>", "<logical name>_path": "<path>"}`
   pairs in the run's meta file.
2. **Hash the defaults too.** The config/constants file defining the canonical operating
   point (`{{canonical_values}}`) is an input; record its hash (e.g. `config_sha256`) so
   every result is pinned to the exact defaults it assumed (see `canonical-params`).
3. **Pin the code identity.** Record the git commit and whether the tree was clean at
   launch; for scripts that ran from a dirty tree, record per-file git blob hashes
   (`git hash-object <script>`) so the exact executed version is recoverable.
4. **Register external data on arrival**: in `{{data_dir}}/<dataset>/README.md` record the
   source (URL/DOI), retrieval date, version/identifier, license note, and the archive
   hash. Bulk data is gitignored; its README and hashes are tracked (see `project-layout`).
5. **Content-address derived caches.** Expensive derived artifacts (preprocessed matrices,
   simulation lookups) get cache keys built from the inputs that determine them
   (`<source id>_<config id>_<param signature>`), so a stale cache is structurally
   impossible rather than procedurally avoided.
6. **Answer "did it change?" by diffing hashes**, never by mtime, file size, or memory.

## Rules

1. **No kept run without input hashes.** A meta file with parameters but no data
   fingerprints answers "what did we ask?" but not "what did we ask it about?".
2. **Hash what was read, not what should have been read.** Compute from the actual path the
   code opened; a hash of the "official" copy proves nothing about the run.
3. **Derived data traces to (input hash, code identity).** If either is missing, the
   artifact is decorative, and regenerating it is the only honest option.
4. **External data is immutable after registration.** A corrected upstream file is a *new*
   version with a new hash and a README note — never overwrite in place.
5. **Changed hash + unchanged conclusion still needs a sentence.** When inputs legitimately
   change (new data release), the first run after the change states what moved and why the
   comparison remains valid.

## Configuration

- `{{data_dir}}` — input-data root (default `data/`), gitignored with tracked READMEs.
- `{{evidence_dir}}` — where meta files carrying the hashes live.
- `{{canonical_values}}` — the defaults file(s) whose hash every run records.

## Provenance & maintenance

Authored from the computational-science reproducibility canon (hash inputs, pin code
identity, content-address caches), grounded in a working repository's practice: run meta
files carrying a config-file SHA-256 plus per-script git blob hashes alongside the git
commit and a tree-clean flag, gitignored bulk data with tracked provenance READMEs, and
content-addressed caching of expensive derived artifacts. See the pack's `examples/`
directory for the worked exemplar mapping. Field names shown are the exemplar's convention;
the pack's `templates/results-meta.schema.json` gives the portable schema.

Re-verify in your project:

- `grep -l "sha256" {{evidence_dir}}/*/meta.json | head -3` — recent runs actually carry
  hashes.
- `shasum -a 256 <a registered dataset file>` — recompute and diff against the recorded
  value.
- `git hash-object <script>` — blob-hash machinery works and matches a recorded value.
