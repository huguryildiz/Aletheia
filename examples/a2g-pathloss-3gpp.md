# Real worked example — a subtle AI parameter-mismatch, caught at the gate

> Unlike the other pages in this folder, **this example is real, not fictional.** It reproduces
> an actual failure mode reported by a researcher: an AI-generated air-to-ground (A2G) path-loss
> model that mixed 3GPP scenario parameters. Every number below is either quoted from the
> primary standard or produced by a script that was actually run — see *Provenance*.

## The scenario

A model for a cellular-connected UAV (aerial UE) link is built from **3GPP TR 36.777**
("Study on Enhanced LTE Support for Aerial Vehicles", Release 15, V15.0.0). The spec gives
**separate tables per deployment scenario** — Urban Macro (UMa-AV), Urban Micro (UMi-AV),
Rural Macro (RMa-AV) — for two things:

- **Path loss** — Table B-2
- **LoS probability** — Table B-1

The claim to be admitted: *"A2G path-loss model for a UMa UAV link at h = 100 m — done."*

## The rot (surface-correct, hard to catch)

The generated model computed **path loss with the UMa-AV formula** but pulled the
**LoS-probability parameters from the UMi-AV row**. Both are real 3GPP values; both live in
adjacent rows of the same table — so nothing looks wrong on inspection. Verified against the
primary source:

| Quantity | Correct (UMa-AV) | Wrongly used (UMi-AV) | Source |
|---|---|---|---|
| Path loss (LoS) | `28.0 + 22·log₁₀(d₃D) + 20·log₁₀(f_c)` | *(kept correct)* | TR 36.777 Table B-2 |
| LoS prob. `p₁` | `4300·log₁₀(h) − 3800` | `233.98·log₁₀(h) − 0.95` | TR 36.777 Table B-1 |
| LoS prob. `d₁` | `max(460·log₁₀(h) − 700, 18)` | `max(294.05·log₁₀(h) − 432.94, 18)` | TR 36.777 Table B-1 |

At h = 100 m that is `p₁, d₁ = 4800, 220` (UMa) versus `467, 155` (UMi) — a real, silent
divergence.

## What it actually does to the result

The script below (UMa-AV, `f_c = 2 GHz`, `h_BS = 25 m`, `h = 100 m`) was run; its output is
pasted verbatim underneath.

```python
import math
fc, hBS, h = 2.0, 25.0, 100.0
log10 = math.log10

def uma_pl_los(d3D):   return 28.0 + 22*log10(d3D) + 20*log10(fc)            # Table B-2
def uma_pl_nlos(d3D):  return -17.5 + (46 - 7*log10(h))*log10(d3D) + 20*log10(40*math.pi*fc/3)
def plos(d2D, p1, d1):                                                       # Table B-1
    return 1.0 if d2D <= d1 else d1/d2D + math.exp(-d2D/p1)*(1 - d1/d2D)

p1_uma, d1_uma = 4300*log10(h) - 3800, max(460*log10(h) - 700, 18)          # correct
p1_umi, d1_umi = 233.98*log10(h) - 0.95, max(294.05*log10(h) - 432.94, 18)  # bug

for d2D in (200, 500, 1000, 2000, 4000):
    d3D = math.sqrt(d2D**2 + (hBS-h)**2)
    Pl, Pn = uma_pl_los(d3D), uma_pl_nlos(d3D)
    ok  = plos(d2D, p1_uma, d1_uma); bug = plos(d2D, p1_umi, d1_umi)
    tot_ok  = Pl*ok  + Pn*(1-ok)                                            # eq (15)
    tot_bug = Pl*bug + Pn*(1-bug)
    print(f"{d2D:>5} | P_LOS ok={ok:.4f} bug={bug:.4f} | Ptot ok={tot_ok:.2f} bug={tot_bug:.2f} dB  Δ={tot_bug-tot_ok:+.2f}")
```

```text
  200 | P_LOS ok=1.0000 bug=0.9219 | Ptot ok=85.27  bug=86.07  dB  Δ=+0.80
  500 | P_LOS ok=0.9446 bug=0.5467 | Ptot ok=94.28  bug=99.84  dB  Δ=+5.56
 1000 | P_LOS ok=0.8533 bug=0.2544 | Ptot ok=102.53 bug=112.69 dB  Δ=+10.15
 2000 | P_LOS ok=0.6967 bug=0.0903 | Ptot ok=112.70 bug=124.80 dB  Δ=+12.10
 4000 | P_LOS ok=0.4657 bug=0.0390 | Ptot ok=125.54 bug=135.34 dB  Δ=+9.80
```

The mismatch is **not** cosmetic: at 1 km it flips LoS probability from 0.85 to 0.25 and shifts
total propagation loss by **10 dB** (a 10× power error), and it is physically backwards — a
high-altitude UAV should have *higher* LoS probability, not lower.

## How Aletheia holds it at the gate

The claim hits the [`correctness-gate`](../skills/core/correctness-gate/SKILL.md): a critical
module (the propagation model) was touched, so it must be verified against a **named ground
truth** — here, the 3GPP tables. Three disciplines converge:

- **`correctness-gate`** — "verify against the named authority." The gate asks: *which table did
  each coefficient come from?* Answering it forces the mismatch into the open.
- **[`canonical-params`](../skills/core/canonical-params/SKILL.md)** — a scenario (UMa vs UMi) is
  a protected choice. Silently drawing path loss from one scenario and LoS probability from
  another is a canonical-parameter violation, not a free implementation detail.
- **[`lit-anchor`](../skills/extended/lit-anchor/SKILL.md)** — every constant is resolved to its
  exact source, one by one. `4300·log₁₀(h) − 3800` traces to Table B-1 *UMa-AV*;
  `233.98·log₁₀(h) − 0.95` traces to Table B-1 *UMi-AV*. Two scenarios in one model → **OPEN**.

**Gate verdict:** `⛔ CLOSURE BLOCKED — 1 OPEN item: scenario-consistency (path loss = UMa-AV,
LoS probability = UMi-AV; both must name the same scenario).`

## Closing the gate

Fix: pull LoS probability from the **UMa-AV** row (`p₁ = 4300·log₁₀(h) − 3800`,
`d₁ = max(460·log₁₀(h) − 700, 18)`), add a consistency check asserting all propagation
parameters name one scenario, and record the spec table for each in the run's evidence.

**Gate verdict:** `✔ CLOSURE VERIFIED — path loss and LoS probability both UMa-AV (TR 36.777
Tables B-2 / B-1), scenario-consistency test passing, each coefficient spec-anchored.`

> *Verdict as the agent should phrase it — the artifacts (recorded seeds, the CI table, the
> interval), not the string, are the evidence. The string alone proves nothing.*

The claim now follows verification, not the other way around.

## Provenance

- **Primary source:** 3GPP TR 36.777 V15.0.0 (2017-12), *Study on Enhanced LTE Support for
  Aerial Vehicles*, Annex B — Table B-1 (LoS probability) and Table B-2 (pathloss models).
  Every coefficient in the tables above was read directly from that document.
- **Numbers:** produced by the script above, executed as shown; the output block is verbatim.
- **Honesty note:** the UMi-AV coefficients were first encountered as an AI-synthesized answer
  and were **not** trusted until confirmed against the primary source — the same discipline this
  example is about.
