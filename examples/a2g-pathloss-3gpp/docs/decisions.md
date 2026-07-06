<!-- markdownlint-disable MD024 -->
# Decision Log

Significant decisions + rationale. Authority layer. Newest on top.

---

## D01 — Adopt the Aletheia operating discipline

**Status**: accepted
**Date**: 2026-07-06

**Context**: Runnable companion to the `a2g-pathloss-3gpp.md` worked example. Chosen as the
flagship of the three real examples because 3GPP TR 36.777 provides an external, published
ground truth — so the gate can check **correctness**, not merely reproducibility (contrast the
UWSN example, whose gate can only pin a self-consistent objective).

**Decision**: Adopt the pack. Bindings in `CLAUDE.md`: `critical_modules=[model.py]`,
`gate_command="python3 model.py --check"`. The gate does two things: (1) asserts scenario
consistency (`PL_SCENARIO == LOS_SCENARIO`); (2) compares computed LoS probability and total
loss to `expected.json`, whose values are anchored to TR 36.777 Tables B-1/B-2. Ground truth is
sourced from the worked example's verified values (`lit-anchor`); it was **not** independently
re-read from the standard during this adoption — the chain is stated honestly in
`expected.json._source`.

**Impact**: `model.py` matches the 3GPP-verified values exactly (P_LOS=0.8533 at 1 km); the gate
passes, and reproducing the real bug (`LOS_SCENARIO="UMi-AV"`) fails it on both counts. The gate
is pure-stdlib and license-free, so it can also run in CI.
