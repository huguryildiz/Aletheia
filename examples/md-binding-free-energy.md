# Worked example — molecular-dynamics binding free energy (illustrative)

> A **fictional** project, included only to show how Aletheia's domain-free skills instantiate
> in a real computational workflow. Not a real repository.

## The project in one paragraph

A computational-chemistry group computes protein–ligand binding free energies for a candidate
series by molecular-dynamics free-energy simulation on GPUs. Each ΔG is an average over
stochastic trajectories, and a single changed cutoff or force-field version silently shifts every
number — so canonical-parameter discipline and replicated statistics carry the project.

## How the skills instantiate

| Skill | In this project |
|---|---|
| `project-layout` | `src/` + `systems/` (prepared structures); gitignored `trajectories/`, `results/` with tracked READMEs; parameter files in `forcefield/` |
| `correctness-gate` | Critical modules = the force computation and the free-energy estimator. Gate = energy conservation in an NVE run + a published host–guest reference ΔG reproduced within tolerance |
| `canonical-params` | Force field, integration timestep, thermostat, nonbonded cutoff, and water model are frozen; changed only in a sweep or with approval |
| `environment-lock` | Pinned MD engine + CUDA + toolkit versions; an engine version bump is treated as a code change and recorded in meta |
| `data-fingerprint` | SHA-256 of the ligand set, starting structures, and parameter files in `meta.json` |
| `evidence-convention` | Each calculation lands in `results/<name>_<date>/` with trajectory hashes + `meta.json`; a ΔG in a scratch notebook is a dark run |
| `reproducibility-provenance` | Thermostat/barostat RNG seed logged; independent replicas share a fixed seed set; the PMF/ΔG figure regenerates from the evidence dir |
| `numerical-determinism` | GPU nondeterminism in MD is documented, not fought; ΔG reported as mean ± CI over independent replicas |
| `statistical-reporting` | Multiple independent replicas per ligand; block averaging + 95% CI; convergence diagnostics reported, never a single window |
| `negative-results-ledger` | Non-converged windows and unstable ligands are recorded, so a known-bad setup isn't silently retried |
| `external-positioning` | ΔG accuracy stated against an experimental benchmark set, with an explicit caution against overfitting the protocol to that set |

## Signature discipline here

`canonical-params`. Free energies are exquisitely sensitive to the protocol: one changed cutoff or
water model moves every ΔG by more than the effect being studied. Freezing the operating point —
and forcing any change through a sweep and a decision record — is what makes a series of numbers
comparable to each other and to experiment.
