# Results — evidence convention

Kept runs land under `results/<name>_<date>/` with a `meta.json` conforming to the pack's
run-evidence schema. Gitignored except `README.md`, `meta.json`, and curated summaries.

## `uwsn-nonuniform_2026-07-06/`

The real solve done during adoption: `python3 model.py` at the canonical operating point
(seed 6, 13 nodes, non-uniform k). A genuine run (not retroactive) — its `meta.json` records
the seed, objective `tau`, and the honest environment fingerprint (x86_64 under Rosetta, not
native arm64).
