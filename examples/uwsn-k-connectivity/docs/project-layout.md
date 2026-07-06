# Project Layout — uwsn-k-connectivity

Pruned to reality (`project-layout` template). A single-model example, not a package.

```text
uwsn-k-connectivity/
├── model.py              # constants → topology → MILP → solve → export (critical module)
├── requirements.txt      # gurobipy pin (env_manifest)
├── solutions.csv         # one illustrative optimal routing (i,j,k,l,val)
├── baseline.json         # the gated invariant: objective tau
├── README.md             # what this is + how to run/gate
├── CLAUDE.md             # Aletheia config block + operating rules
├── docs/
│   ├── decisions.md      # ADR-lite chain (authority layer)
│   ├── build_log/        # empty as of adoption
│   └── project-layout.md # this file
└── results/              # kept-run evidence going forward (gitignored except records)
```

## Invariants

1. `model.py` is the only critical module; its top-of-file constants are canonical.
2. `solutions.csv` is illustrative (non-unique optimum); `baseline.json`'s `tau` is the
   gated invariant.
3. Kept runs land in `results/<name>_<date>/` with a `meta.json`; bulk outputs gitignored.
