# Real worked example — a lucky run and an over-claimed precision, caught at the gate

> Like [the A2G one](a2g-pathloss-3gpp.md), this example is **real, not fictional** — every
> number below comes from a script that was actually run. It is deliberately tiny (a Monte
> Carlo estimate of π) so the disciplines, not the domain, are what you read. Its power is that
> π has a **known ground truth** (`math.pi`), so the correctness-gate rules against a real
> answer, not an assertion — the pack's whole thesis in one page.

## The claim

*"Monte Carlo estimate of π ≈ 3.1424, accurate to 1e-4 — done."*

One run, a nice-looking number, ready to report.

## The rot (each item is genuinely present here)

| Hidden | Why it is real in *this* problem | Discipline |
|---|---|---|
| seed unlogged | the estimate genuinely changes with the seed | `run-provenance` |
| one run reported | the estimate has real variance → needs replication + an interval | `statistical-reporting` |
| precision over-claimed | "1e-4" was asserted; the run's actual error is **8.4e-4** | `correctness-gate` |
| figure can't regenerate | the convergence plot must rebuild from the recorded seeds | `external-positioning` |

## What it actually does — real run

```python
import math, statistics as st, numpy as np
def est(seed, n):                     # π by random darts in the unit square
    rng = np.random.default_rng(seed); x = rng.random(n); y = rng.random(n)
    return 4.0 * np.count_nonzero(x*x + y*y <= 1.0) / n

N = 1_000_000
e1 = est(42, N)                                        # the single "done" run
ests = [est(s, N) for s in range(20)]                  # 20 replications, seeds recorded
m  = st.mean(ests); sd = st.stdev(ests)
hw = 2.093 * sd / len(ests)**0.5                        # 95% CI half-width (t, 19 df)
print(f"single (seed 42):  pi_hat={e1:.6f}  |err|={abs(e1-math.pi):.2e}")
print(f"20 reps:  mean={m:.6f}  95% CI ±{hw:.2e}  |mean-pi|={abs(m-math.pi):.2e}")
```

```text
single (seed 42):  pi_hat=3.142436  |err|=8.43e-04
20 reps:  mean=3.141469  95% CI ±8.89e-04  |mean-pi|=1.24e-04
```

The single run's error is **8.4e-4** — the "accurate to 1e-4" claim was never met. And the 95%
confidence interval over 20 runs is **±8.9e-4**: the honest precision at N = 10⁶ is about 10⁻³,
not 10⁻⁴. You cannot assert 1e-4 from this data.

## How Aletheia holds it at the gate

- **[`run-provenance`](../skills/core/run-provenance/SKILL.md)** — no
  seed, no result. Seeds `42` and `0..19` are recorded so every number above is re-derivable, and
  the convergence figure regenerates from them with one command (the figure-regeneration bar
  itself is held by `external-positioning`).
- **[`statistical-reporting`](../skills/extended/statistical-reporting/SKILL.md)** — never a single
  run. The claim must carry a replication count, a mean, an interval, and a visible denominator
  (20 runs × 10⁶ draws), not one lucky point.
- **[`correctness-gate`](../skills/core/correctness-gate/SKILL.md)** — the estimate is checked
  against the **named ground truth** `math.pi`. `|mean − π| = 1.2e-4` is consistent with the
  ±8.9e-4 interval, but the *claimed* precision (1e-4) exceeds the *achieved* precision (~10⁻³).

**Gate verdict:** `⛔ CLOSURE BLOCKED — 1 OPEN item: claimed 1e-4 precision is not supported (95% CI is ±8.9e-4; single-run error 8.4e-4; seed unlogged; n=1).`

## Closing the gate

Two honest ways to close it, both recorded:

- **Scope the claim to the evidence:** report `π ≈ 3.1415 ± 0.0009 (95% CI, 20×10⁶ draws, seeds 0–19)` — true at the precision actually achieved.
- **Earn the precision:** to legitimately claim 1e-4, raise N. Monte Carlo error falls as ≈1.64/√N, so a 1e-4 standard error needs **~2.7×10⁸ draws per run** — a change of scale that must be logged, not a tolerance quietly loosened.

**Gate verdict:** `✔ CLOSURE VERIFIED — seeds recorded, replication + 95% CI reported, precision scoped to what was measured against math.pi.`

> *Verdict as the agent should phrase it — the artifacts (recorded seeds, the CI table, the
> interval), not the string, are the evidence. The string alone proves nothing.*

## Provenance

- **Ground truth:** `math.pi` (the mathematical constant) — the estimate is checked against it directly.
- **Numbers:** produced by the script above, executed as shown; the output block is verbatim (NumPy 2.0, `default_rng`).
- **Honesty note:** this example ships as markdown; the script was run in a scratch directory and only its verified output is quoted here — the pack itself stays code-free.
