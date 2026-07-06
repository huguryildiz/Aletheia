# Worked example — fusion / plasma simulation (illustrative)

> A **fictional** project, included only to show how Aletheia's domain-free skills instantiate
> in a real computational workflow. Not a real repository.

## The project in one paragraph

A group runs gyrokinetic turbulence simulations to predict heat transport in a tokamak, on a
large HPC allocation. Predictions are time-averaged fluxes from a chaotic system, and the PDE
solver is the load-bearing machinery — so a solver bug, an unconverged grid, or a single-snapshot
"result" would quietly corrupt the physics.

## How the skills instantiate

| Skill | In this project |
|---|---|
| `project-layout` | `src/` solver + `cases/` (equilibria, geometries); gitignored bulk `output/` field data with tracked READMEs; HPC job scripts in `jobs/` |
| `correctness-gate` | Critical module = the PDE solver kernel. Gate = an analytic linear-growth-rate benchmark + a published verification case reproduced within tolerance |
| `canonical-params` | Grid resolution, timestep (CFL limit), boundary conditions, and collision model are frozen; changed only inside a convergence study or sweep |
| `environment-lock` | Pinned compiler + MPI + GPU stack and numerical libraries; cluster module versions recorded per run |
| `data-fingerprint` | SHA-256 of the equilibrium/geometry input and the run config in `meta.json` |
| `evidence-convention` | Each run lands in `results/<name>_<date>/` with diagnostics + `meta.json`; large fields are hashed and registered, never left as dark output |
| `reproducibility-provenance` | Seed logged for any Monte-Carlo collision component; every flux figure regenerates by one command from the diagnostics |
| `numerical-determinism` | MPI reduction-order and GPU-atomic nondeterminism documented; a convergence-under-refinement study accompanies every production claim |
| `statistical-reporting` | Time-averaged fluxes reported with error bars from block averaging over the saturated turbulent state; never a single snapshot |
| `negative-results-ledger` | Numerically unstable parameter regimes are recorded so they aren't rediscovered the hard way |
| `external-positioning` | Transport predictions framed against experimental discharges and code-comparison projects before any headline claim |

## Signature discipline here

`correctness-gate` plus convergence-under-refinement. Chaotic PDE output always *looks*
plausible, so plausibility proves nothing. The physics oracle is a linear benchmark the solver
must reproduce exactly, backed by the rule that no flux is a result until it is stable under grid
and timestep refinement.
