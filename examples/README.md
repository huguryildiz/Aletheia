# Worked examples

Aletheia's skills are **domain-free** — they name no field, no tool, no equation. Most examples
below are **fictional** — illustrations, not real repositories. One is real (see below).

The pack's Core was harvested from, and its Extended tier stress-tested against, a real
computational-research repository. That repository is **not named or reproduced here**, and no
skill or template contains a domain term — the portability gate (`grep` over `skills/` and
`templates/` for domain vocabulary must return zero) enforces this by construction.

## Real worked example

Two pages are **not** fictional. Each reproduces an actual failure mode with real numbers from a
script that was run, and shows the gate catching it — one against a published spec, one against a
mathematical constant.

| Example | Domain | Signature skill it spotlights |
|---|---|---|
| [A2G path-loss parameter mismatch (real)](a2g-pathloss-3gpp.md) | Wireless / telecom | `correctness-gate` + `canonical-params` + `lit-anchor` |
| [Monte Carlo π — lucky run, over-claimed precision (real)](monte-carlo-pi.md) | Numerical / stats | `statistical-reporting` + `reproducibility-provenance` + `correctness-gate` |

## Full (fictional) examples

| Example | Domain | Signature skill it spotlights |
|---|---|---|
| [Deep-learning training & evaluation](ml-training-pipeline.md) | CS / AI | `statistical-reporting` + `numerical-determinism` |
| [Variational quantum algorithms](quantum-vqe.md) | Quantum computing | `correctness-gate` (classical oracle) |
| [Climate ensemble calibration](climate-ensemble-calibration.md) | Earth science | `reproducibility-provenance` |
| [Molecular-dynamics binding free energy](md-binding-free-energy.md) | Computational chemistry | `canonical-params` |
| [Fusion / plasma simulation](fusion-plasma-simulation.md) | Plasma physics | `correctness-gate` + convergence |

## Portability matrix

The same bindings, one line per domain — what plays the role of each pivotal placeholder. The
five above have full pages; the rest show the pattern generalizes just as cleanly.

| Domain | Critical module (the gate guards) | Canonical params | Data fingerprinted |
|---|---|---|---|
| Deep learning | loss/metric + collator | LR schedule, batch, seed, tokenizer | train/eval shards, vocab |
| Quantum computing | Hamiltonian + estimator | shots, ansatz depth, optimizer, noise model | problem instance, noise config |
| Climate modeling | calibration objective + emulator | resolution, forcing version, spin-up | forcing datasets, obs targets |
| Molecular dynamics | forces + free-energy estimator | force field, timestep, cutoff, water model | ligand set, structures, params |
| Fusion / plasma | PDE solver kernel | grid, CFL timestep, BCs, collision model | equilibrium/geometry input |
| Materials (DFT) | SCF + energy/force kernel | functional, basis, k-point mesh, cutoff | structures, pseudopotentials |
| Astrophysics (N-body) | gravity solver + integrator | softening, timestep, opening angle | initial conditions |
| Computational fluid dynamics | flow solver | mesh, timestep, turbulence model | geometry, mesh |
| Power systems | dynamic (DAE) solver | integration step, fault-clear time | network/case data |
| Bayesian inference | likelihood + sampler kernel | chains, warmup, target accept, seed | dataset, prior config |

Every row uses the same skills; only the nouns change. That is the whole thesis.
