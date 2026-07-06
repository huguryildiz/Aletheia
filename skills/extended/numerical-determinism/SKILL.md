---
name: numerical-determinism
description: >-
  Use when the same code and same seed still produce different numbers — pinning thread counts, parallel reduction order, GPU kernels, and engine-level nondeterminism — and when a claim requires bit-reproducibility or a timing result requires hardware context. Also defines the hardware-context fields every run's meta file should record. Trigger phrases: "same seed different result", "pin the threads", "deterministic mode", "results differ across machines", "record the hardware", "timing needs the machine specs".
tier: extended
status: recommended
---

# numerical-determinism

Seeds pin the *draws*; they do not pin the *arithmetic*. Parallel reductions reorder
floating-point sums, GPU atomics race, and optimization engines take time-dependent paths —
so "same seed, different number" is expected behavior until execution is pinned too. This
skill sets the pinning knobs, defines honest reproducibility tiers, and (folded in) the
hardware-context record every run should carry.

## When to use

- A seeded computation gives different results across runs or machines.
- A claim needs bit-reproducibility (regression pins, cross-checking two implementations).
- Any timing/performance number is about to be reported.
- Setting up the meta-file fields for a new project.

## When NOT to use

- Variation you *want* — spread across seeds/realizations is the object of study
  (`statistical-reporting`); do not pin it away.
- Version-level differences (library upgrades changing algorithms) — `run-provenance`.
- Recording which seeds were drawn — `run-provenance`.

## Sources of nondeterminism (check in this order)

1. **Thread-count drift** — BLAS/OpenMP pools sized by the machine. Pin explicitly
   (e.g. `OMP_NUM_THREADS`, `MKL_NUM_THREADS`, or single-threaded mode for pinned runs).
2. **Parallel reduction order** — float addition is not associative; multi-threaded sums
   differ run to run. Pinning threads to 1, or using deterministic-reduction options where
   the library offers them, removes it.
3. **Hash/iteration order** — order-dependent iteration over hashed containers (pin the
   hash seed, e.g. `PYTHONHASHSEED`, or sort before iterating).
4. **GPU kernels** — atomics and autotuned algorithm selection; enable the framework's
   deterministic mode for pinned runs and accept the speed cost.
5. **Engine-level nondeterminism** — optimization/simulation engines with parallel search:
   the incumbent found can depend on thread scheduling and wall-clock limits. Pin the
   engine's thread count and seed parameters; prefer deterministic work-limit options over
   wall-clock limits where the engine offers them; otherwise report engine results as
   tolerance-reproducible, not bit-reproducible.

## Reproducibility tiers (state which one a claim uses)

- **Tier A — bit-reproducible**: same machine, locked environment, pinned threads/kernels.
  Required for regression pins and cross-implementation parity checks
  (`correctness-gate`).
- **Tier B — tolerance-reproducible**: same environment class, numbers agree within a
  stated tolerance. The realistic tier for parallel/GPU/engine runs; the tolerance is part
  of the claim.
- **Tier C — statistically reproducible**: distributions agree across replications
  (`statistical-reporting`). The tier most scientific claims actually need.

Chasing Tier A where Tier C suffices wastes compute; claiming Tier A while delivering
Tier B corrupts regression baselines. Name the tier.

## Hardware context (folded field-set — record into `meta.json`)

Every kept run records the machine it ran on; timing claims are meaningless without it and
numeric differences are undiagnosable without it:

```json
"hardware": {
  "cpu_model": "...", "cores_physical": 0, "ram_gb": 0,
  "gpu_model": "... or null", "gpu_driver": "... or null",
  "os": "...", "arch": "...", "threads_pinned": "OMP=1,ENGINE=1 or 'unpinned'"
}
```

(Schema: `templates/results-meta.schema.json`. Architecture-native verification is
`run-provenance`'s preflight; the field lands here.)

## Rules

1. **Pinned runs declare their pins** — thread settings and deterministic-mode flags go in
   the meta file next to the seeds; an undeclared pin is an unreproducible pin.
2. **Timing numbers always ship with hardware context and thread settings.** "2.3× faster"
   on unstated hardware is marketing, not measurement.
3. **Cross-machine comparisons compare Tier B or C**, never raw bits; put the tolerance in
   the text.
4. **Nondeterminism found ≠ nondeterminism fixed.** If a pinned run still varies, that is a
   finding to record and diagnose (`negative-results-ledger` if abandoned), not to rerun
   until it looks stable.

## Configuration

- `{{evidence_dir}}` — meta files carrying pins + hardware context.
- `{{gate_command}}` — the gate whose pins depend on Tier A holding.

## Provenance & maintenance

Authored from the numerical-computing canon (non-associative float reduction, GPU
determinism modes, engine scheduling effects), grounded in working practice: campaign
preflights that verify native architecture, meta files recording an
architecture-verified flag, and engine runs treated as tolerance-reproducible with the
tolerance pinned in a correctness gate. Hardware-context is a documented field-set here by
design — not a separate skill. See the pack's `examples/` directory for the worked exemplar
mapping.

Re-verify in your project:

- `python -c "import os; print(os.environ.get('OMP_NUM_THREADS'))"` — pins are actually set
  in the run environment (adapt variable names).
- Run a pinned computation twice and `diff` the outputs — Tier A holds where claimed.
- `grep -h "hardware\|arch" {{evidence_dir}}/*/meta.json | head -3` — runs record the
  machine.
