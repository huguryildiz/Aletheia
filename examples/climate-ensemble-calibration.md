# Worked example — climate ensemble calibration (illustrative)

> A **fictional** project, included only to show how Aletheia's domain-free skills instantiate
> in a real computational workflow. Not a real repository.

## The project in one paragraph

A group calibrates an intermediate-complexity climate model against observational targets and
produces a perturbed-parameter ensemble of projections on an HPC cluster. The headline is an
ensemble spread, not a single trajectory, and the runs are large and expensive — so provenance,
conservation checks, and honest uncertainty are the whole game.

## How the skills instantiate

| Skill | In this project |
|---|---|
| `project-layout` | `src/` + `configs/` (forcing scenarios, resolutions); gitignored bulk `output/` with tracked READMEs; HPC job scripts in `jobs/` |
| `correctness-gate` | Critical modules = the calibration objective and the emulator. Gate = energy/mass-conservation checks + a known radiative-equilibrium analytic case within tolerance |
| `canonical-params` | The control configuration (resolution, forcing-dataset version, spin-up length) is frozen; changed only in a sweep |
| `run-provenance` | Pinned compiler + MPI + numerical-library stack with HPC module versions recorded per run; SHA-256 of forcing datasets and observational targets (content-addressed, so "which forcing produced this?" is answerable); an explicit realization/seed list with perturbed-parameter members sharing a fixed seed set — all in `meta.json` |
| `evidence-convention` | Each ensemble lands in `results/<name>_<date>/` with the realization list + `meta.json`; results left only in scratch are dark runs |
| `numerical-determinism` | Bitwise-reproducibility caveats across MPI decomposition and compiler are documented; architecture recorded so cross-machine diffs are explicable |
| `statistical-reporting` | Ensemble spread reported as confidence intervals; skill scores carry uncertainty; a single member is never reported as "the" projection |
| `external-positioning` | Projections framed against prior assessment ranges; the reproducibility bar is met before any headline number leaves the group; every figure regenerates from the evidence dir |

## Signature discipline here

`run-provenance`. In ensemble science the ensemble *is* the result: a lone member is
a sample, not a finding. Recording the exact realization list — and reusing the same seed set for
paired perturbations — is what lets a spread be compared, reproduced, and defended.
