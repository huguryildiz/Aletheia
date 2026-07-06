---
name: run-provenance
description: >-
  Use when a kept run must be attributable to exactly what produced it — the environment it ran under (interpreter, locked packages, domain engines, system layer, native architecture), the input bytes it consumed (datasets, external files, config/constants), and the random draws it made (seeds recorded and re-derivable). Everything `results/<name>_<date>/meta.json` must record about a run, and how to make each field true. Also use before any campaign whose results will be kept, when two machines disagree on a result, and when asking "did the data change between these two runs". Trigger phrases: "pin the environment", "lockfile", "which versions produced this", "works on my machine", "environment drift", "hash the inputs", "did the data change", "which dataset version", "fingerprint the config", "data provenance", "record the seeds", "which seed produced this", "unseeded randomness", "make this run reproducible", "what produced this number".
tier: core
---

# run-provenance

"What produced this number?" must have one answer, computed and recorded, not remembered.
Every kept run carries a meta file — `{{evidence_dir}}/<name>_<date>/meta.json` — and that
file must pin three provenance chains, each of which dies silently if not captured at run
time: the **environment** it ran under, the **inputs** it consumed, and the **seeds** it
drew from. "It worked last month" is not provenance — it is a memory.

## When to use

- Before any campaign that lands in `{{evidence_dir}}` (preflight) — the meta file needs all
  three chains.
- Creating or onboarding a project without a lockfile; adding a dependency or upgrading an
  interpreter/domain engine.
- Launching any run that consumes input data, or registering a new external dataset.
- Any stochastic computation whose output will be kept.
- Debugging cross-machine or cross-month differences: same code, different number.

## When NOT to use

- Choosing *values* of run parameters — that is `canonical-params` (protected defaults).
- Chasing bit-level nondeterminism *within* one pinned environment (threads, BLAS, GPU
  kernels) — that is `numerical-determinism`; seeds and locks cannot fix what scheduling
  scrambles.
- Deciding *how many* seeds/replications a claim needs — that is `statistical-reporting`.
- The schema the meta file is written into and which runs are "kept" — that is
  `evidence-convention` (the hub this writes into).
- Verifying a computation's correctness — provenance proves *which inputs/env/draws*, not
  *right answer*.

## Environment — declare → lock → commit → fingerprint

1. **Declare**: dependencies live in a manifest — `{{env_manifest}}` (e.g. `pyproject.toml`,
   `environment.yml`). Direct dependencies only; no pip-install-by-hand history.
2. **Resolve and commit the lock**: a lockfile pinning the full transitive set (`uv.lock`,
   `poetry.lock`, `conda-lock.yml`) is committed next to the manifest, plus the interpreter
   pin (e.g. `.python-version`). Group heavyweight/phase-specific stacks (dev tooling, GPU
   frameworks) in optional dependency groups so the base install stays resolvable.
3. **Record the system layer**: domain engines and system libraries the lockfile cannot see
   (commercial engine builds, CUDA/driver versions, compiler toolchains, BLAS
   implementation) are recorded in the README or environment doc, and their versions land in
   each run's meta file.
4. **Run native, not emulated.** On mixed-architecture machines, verify the interpreter
   matches the hardware — an emulated interpreter (e.g. x86-64 under translation on ARM) runs
   native extensions silently and sometimes drastically slower, and can change numerical
   library code paths. Preflight: `python -c "import platform; print(platform.machine())"`
   must print the machine's native architecture.
5. **Fingerprint into evidence**: each run's meta file records interpreter version,
   architecture (+ native-arch verified flag), lockfile hash, and domain-engine versions.

## Inputs — hash every byte the run reads

1. **Hash inputs at read time**: `shasum -a 256 <file>` (or the in-code equivalent) for every
   dataset file the run reads, recorded as
   `{"<logical name>_sha256": "<hash>", "<logical name>_path": "<path>"}` pairs in the meta
   file. **Hash what was read, not what should have been read** — compute from the actual path
   the code opened; a hash of the "official" copy proves nothing about the run.
2. **Hash the defaults too.** The config/constants file defining the canonical operating point
   (`{{canonical_values}}`) is an input; record its hash (e.g. `config_sha256`) so every
   result is pinned to the exact defaults it assumed (see `canonical-params`).
3. **Pin the code identity.** Record the git commit and whether the tree was clean at launch;
   for scripts that ran from a dirty tree, record per-file git blob hashes
   (`git hash-object <script>`) so the exact executed version is recoverable.
4. **Register external data on arrival**: in `{{data_dir}}/<dataset>/README.md` record the
   source (URL/DOI), retrieval date, version/identifier, license note, and the archive hash.
   Bulk data is gitignored; its README and hashes are tracked (see `project-layout`). External
   data is immutable after registration — a corrected upstream file is a *new* version with a
   new hash, never an overwrite in place.
5. **Content-address derived caches.** Expensive derived artifacts get cache keys built from
   the inputs that determine them (`<source id>_<config id>_<param signature>`), so a stale
   cache is structurally impossible rather than procedurally avoided.
6. **Answer "did it change?" by diffing hashes**, never by mtime, file size, or memory.

## Seeds — recorded and re-derivable

1. **No unseeded global randomness in kept runs.** Every stochastic entry point takes an
   explicit seed (or RNG object) as a parameter; library calls draw from passed-in
   generators, not module-level global state.
2. **Derive, don't invent.** A campaign uses a base seed plus a documented derivation
   (e.g. `seed_i = base + i` or a seed-sequence spawn per realization), so "realization 7"
   means the same draws everywhere, forever.
3. **Record the seed list in the meta file** — the actual list or (base, rule, count), plus
   the RNG library and algorithm when the library offers several.
4. **Re-derivation check**: re-running one realization from its recorded seed must reproduce
   its draws bit-for-bit within the same locked environment. If it does not, find out why
   before trusting any aggregate.
5. **Same seed across arms when comparing.** Paired comparisons run both arms on the same
   realizations (same seeds), so differences come from the treatment, not the draw (see
   `statistical-reporting`).

## Rules

1. **No kept run without all three chains.** A meta file with parameters but no environment
   fingerprint, no input hashes, or no seed list answers "what did we ask?" but not "under
   what, about what, and from which draws?".
2. **Manifest + lockfile are both committed.** A manifest without a lock resolves differently
   next year; a lock without a manifest cannot be evolved. One environment manager per
   project; environment changes are visible changes (lockfile diffs go through review).
3. **Engine versions are result-relevant.** Optimizers, simulators, and training frameworks
   change numerical behavior between versions; treat an engine upgrade like a code change to a
   critical module — run `{{gate_command}}` after it.
4. **Derived data traces to (input hash, code identity).** If either is missing, the artifact
   is decorative, and regenerating it is the only honest option.
5. **Seeds are data**: they belong in `meta.json`, not in code defaults or shell history. A
   kept stochastic result without a recorded seed list is unreproducible by definition — treat
   it like a dark run (`evidence-convention`). Changing the seed-derivation rule invalidates
   cross-campaign realization identity — record it as a decision (`decision-log`).
6. **Changed hash + unchanged conclusion still needs a sentence.** When inputs legitimately
   change (new data release), the first run after the change states what moved and why the
   comparison remains valid.

## Configuration

- `{{env_manifest}}` — manifest path(s), e.g. `pyproject.toml` (+ lockfile alongside).
- `{{data_dir}}` — input-data root (default `data/`), gitignored with tracked READMEs.
- `{{evidence_dir}}` — where meta files carrying all three chains live.
- `{{canonical_values}}` — the defaults file(s) whose hash every run records.
- `{{gate_command}}` — the correctness gate re-run after an environment/engine change.

## Provenance & maintenance

Consolidated from the computational-science reproducibility canon (declare → lock → commit →
fingerprint; hash inputs and pin code identity; explicit generators with derived seeds),
grounded in a working repository's practice: a locked package manager with committed lockfile
and interpreter pin, a native-architecture preflight enforced before campaigns, run meta files
carrying a config-file SHA-256 plus per-script git blob hashes alongside the git commit and a
tree-clean flag, and campaign meta files recording explicit realization lists with paired arms
run on identical seeds. See the pack's `examples/` directory for the worked exemplar mapping;
`templates/results-meta.schema.json` gives the portable meta schema. `numerical-determinism`
(making runs pinnable) and `canonical-params` (protected defaults) are separate skills;
`evidence-convention` is the hub this writes into.

Re-verify in your project:

- `test -f {{env_manifest}} && ls *lock* 2>/dev/null` — manifest and lockfile exist and are
  tracked; `python -c "import platform; print(platform.machine(), platform.python_version())"`
  — native architecture and pinned interpreter.
- `grep -l "sha256" {{evidence_dir}}/*/meta.json | head -3` — recent runs carry input hashes;
  `shasum -a 256 <a registered dataset file>` — recompute and diff against the recorded value.
- `grep -h "seed\|realization" {{evidence_dir}}/*/meta.json | head -5` — kept runs record
  their draws; re-run one realization from its recorded seed and diff the output.
