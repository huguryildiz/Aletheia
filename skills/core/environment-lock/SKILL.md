---
name: environment-lock
description: Use when setting up or auditing a project's computational environment — pinning the interpreter, package versions, domain engines (solvers, simulators, training frameworks), and system libraries so a run is attributable to one resolvable environment. Also use before any campaign whose results will be kept, and when two machines disagree on a result. Trigger phrases: "pin the environment", "lockfile", "which versions produced this", "works on my machine", "set up reproducible deps", "environment drift".
tier: core
---

# environment-lock

Every kept result must be attributable to one resolvable environment: interpreter version,
locked package set, domain-engine versions, and the system layer under them. "It worked
last month" with no lockfile is not an environment — it is a memory. The contract: **the
environment is declared in a manifest, resolved into a lockfile, both are committed, and
every evidence run records the environment fingerprint it ran under.**

## When to use

- Creating a new project or onboarding to one without a lockfile.
- Before any campaign that lands in `{{evidence_dir}}` (preflight).
- Debugging cross-machine or cross-month result differences.
- Adding a dependency, upgrading the interpreter, or changing a domain-engine version.

## When NOT to use

- Choosing *values* of run parameters — that is `canonical-params`.
- Chasing bit-level nondeterminism within one pinned environment — that is
  `numerical-determinism` (threads, BLAS, GPU kernels).
- Hashing input *data* — that is `data-fingerprint`.

## Runbook

1. **Declare**: dependencies live in a manifest — `{{env_manifest}}` (e.g. `pyproject.toml`,
   `environment.yml`). Direct dependencies only; no pip-install-by-hand history.
2. **Resolve and commit the lock**: a lockfile pinning the full transitive set (`uv.lock`,
   `poetry.lock`, `conda-lock.yml`) is committed next to the manifest, plus the interpreter
   pin (e.g. `.python-version`).
3. **Group the optional extras**: heavyweight or phase-specific stacks (dev tooling, GPU
   frameworks) go in optional dependency groups so the base install stays resolvable.
4. **Record the system layer**: domain engines and system libraries that the lockfile cannot
   see (commercial engine builds, CUDA/driver versions, compiler toolchains, BLAS
   implementation) are recorded in the project README or environment doc, and their versions
   land in each run's meta file.
5. **Run native, not emulated.** On mixed-architecture machines, verify the interpreter
   matches the hardware — an emulated interpreter (e.g. x86-64 under translation on ARM)
   runs native extensions silently and sometimes drastically slower, and can change
   numerical library code paths. Preflight: `python -c "import platform; print(platform.machine())"`
   must print the machine's native architecture.
6. **Fingerprint into evidence**: each `{{evidence_dir}}` run's meta file records —
   interpreter version, architecture (+ native-arch verified flag), lockfile hash, and
   domain-engine versions. "Which environment produced this number?" must have one answer.

## Rules

1. **Manifest + lockfile are both committed.** A manifest without a lock resolves
   differently next year; a lock without a manifest cannot be evolved.
2. **One environment manager per project.** Mixing managers (conda + pip + system packages)
   creates unresolvable states; pick one and route everything through it.
3. **Engine versions are result-relevant.** Optimizers, simulators, and training frameworks
   change numerical behavior between versions; treat an engine upgrade like a code change to
   a critical module — run `{{gate_command}}` after it.
4. **Environment changes are visible changes.** Lockfile diffs go through review like code;
   a drive-by `pip install` that never reaches the manifest is drift.
5. **CI (if any) installs from the lockfile**, never from loose requirements — otherwise CI
   green means nothing about the locked environment.

## Configuration

- `{{env_manifest}}` — manifest path(s), e.g. `pyproject.toml` (+ lockfile alongside).
- `{{evidence_dir}}`, `{{gate_command}}` — for fingerprinting and post-upgrade gating.

## Provenance & maintenance

Authored from the computational-science reproducibility canon (declare → lock → commit →
fingerprint), grounded in a working repository's practice: a locked package manager with
committed lockfile and interpreter pin, optional dependency groups for phase-specific
stacks, a native-architecture preflight enforced before campaigns, and an
architecture-verified flag recorded in run meta files. See the pack's `examples/` directory
for the worked exemplar mapping. The emulation-slowdown warning is verified exemplar
experience; the specific manager named in your project is yours to choose.

Re-verify in your project:

- `test -f {{env_manifest}} && ls *lock* 2>/dev/null` — manifest and lockfile exist and are
  tracked.
- `python -c "import platform; print(platform.machine(), platform.python_version())"` —
  native architecture and pinned interpreter version.
- `git log --oneline -3 -- <lockfile>` — lock changes are deliberate commits, not
  untracked drift.
