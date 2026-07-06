# Worked example — deep-learning training & evaluation (illustrative)

> A **fictional** project, included only to show how Aletheia's domain-free skills instantiate
> in a real computational workflow. Not a real repository.

## The project in one paragraph

A team trains and evaluates transformer models on a text-classification benchmark, comparing a
new architecture against published baselines. The headline claim is a benchmark score, so the
stakes are exactly the ones this pack defends: a single lucky seed, an unpinned tokenizer, or
GPU nondeterminism can turn noise into a "result" that never reproduces.

## How the skills instantiate

| Skill | In this project |
|---|---|
| `project-layout` | `src/` package; gitignored `checkpoints/`, `datasets/`, `runs/` with tracked READMEs; run configs in `configs/`; session plans out of `docs/` |
| `correctness-gate` | Critical modules = the loss and metric functions and the data collator. Gate = unit tests asserting metrics against hand-computed values + a tiny-overfit test (the model must memorize 10 examples to ~0 loss) |
| `canonical-params` | The frozen recipe (learning-rate schedule, batch size, base seed, tokenizer version) changes only inside a sweep or with approval; ad-hoc probes stay script-level |
| `run-provenance` | Pinned CUDA + framework + tokenizer versions in a lockfile with GPU driver and arch recorded per run; SHA-256 of the train/eval shards and the tokenizer vocab ("did the data change?" is answered from the hash, not from memory); the base seed logged with deterministic dataloader ordering — all in each run's `meta.json` |
| `evidence-convention` | Every run lands in `runs/<name>_<date>/` with `meta.json` (config hash, git commit, metrics); a metric printed only to a scratch log is a dark run |
| `numerical-determinism` | cuDNN determinism flags set where feasible; residual GPU-atomic / mixed-precision nondeterminism documented, not hidden; architecture recorded |
| `statistical-reporting` | Each configuration run over N seeds; report **mean ± 95% CI**, never a single run; paired comparison against the baseline on the same seed set |
| `external-positioning` | Benchmark claims stated against the published SOTA number with a train/test contamination check done *before* claiming; ablations separate the architecture's effect from the recipe's; the results figure regenerates by one command from the logged metrics |

## Signature discipline here

`statistical-reporting` + `numerical-determinism`. In deep learning the temptation to report the
best-of-many-seeds run is enormous and the variance is real — so a bare single-seed score is not
a result. The evidence bar is a seed distribution with a confidence interval, and any claimed
gain must survive a paired comparison on a shared seed set.
