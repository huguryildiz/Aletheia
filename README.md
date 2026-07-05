# ALETHEIA

**Operating discipline for rigorous, reproducible computational-science research — shipped
as a portable Claude skill pack.**

Aletheia (ἀλήθεια — "disclosure, the state of not being hidden") encodes how a
results-producing research repository stays honest: where evidence lands, what gates a
"done" claim, how decisions propagate, and what a number must carry before it enters a
paper. It is **markdown-only** — discipline as instructions, not enforcement as scripts —
which makes it model- and harness-portable by construction.

The pack was **mined from one real research project** (an underwater sensor-network
optimization effort targeting a journal paper — see
[examples/uwsn-ankc.md](examples/uwsn-ankc.md)), generalized until it reads naturally in
any computational domain — molecular dynamics, climate modeling, bioinformatics, ML
training — and stress-tested against that bar. Domain content lives in exactly one file:
the example.

## Who it is for

- Researchers running computation-heavy projects (a PI + student, a small lab, a solo
  PhD) who want paper-grade reproducibility without building process from scratch.
- AI-assisted workflows: the skills are runbooks an agent follows, with bindings that
  pin them to *your* repo.

## What ships

**17 skills + 1 generator + 3 agents + 5 templates + 5 docs + 1 worked example.**

### Core skills (11) — everyday discipline

| Skill | One line |
|---|---|
| `project-layout` | one home per artifact class; bulk dirs gitignored, their records tracked |
| `layer-sync` | decisions → spec → code → notebooks stay in agreement; drift gets file:line citations |
| `decision-log` | numbered ADR-lite chain, newest on top; superseded entries never deleted |
| `build-log` | write-once phase/gate evidence entries — the paper's raw methods material |
| `phase-gate` | closure = written checklist verified against named evidence; one OPEN item = no closure |
| `correctness-gate` | critical module touched → the named gate must pass before "done" |
| `canonical-params` | protected defaults change only in a sweep or with approval + record |
| `environment-lock` | manifest + lockfile committed; engine versions and native-arch fingerprinted per run |
| `data-fingerprint` | every input hashed into the run's meta; "did the data change?" has one answer |
| `evidence-convention` | no dark runs: `results/<name>_<date>/meta.json` with pre-registered expectations |
| `research-methodology` | claims follow verification; predictions precede runs; ceremony scales with consequence |

### Extended skills (6) — reproducibility + positioning (`status: recommended`)

| Skill | One line |
|---|---|
| `reproducibility-provenance` | seeds recorded and re-derivable; every figure regenerates from one command |
| `statistical-reporting` | never report a single run; replication + intervals + visible denominators |
| `numerical-determinism` | threads/kernels pinned where claimed; hardware context recorded; reproducibility tiers named |
| `negative-results-ledger` | dead ends leave a one-line record; rigorous negatives get promoted, not buried |
| `notebook-vs-script` | one-offs → notebooks, pipelines → scripts, shared logic → the package |
| `external-positioning` | novelty bookkept, citations verified one-by-one, claims scoped to evidence |

### Generator

`skill-library-generator` — binds the pack to your repo by interview (config block in
`CLAUDE.md`) and mines your project's own failure modes into local skills. Claude is the
runtime; there is no bootstrap script.

### Agents (read-only auditors)

`session-historian` (state digest from the record) · `drift-auditor` (layer-sync audit) ·
`verifier` (adversarial refutation of load-bearing claims). They write nothing, ever.

## Quickstart

```bash
# try it for one session
claude --plugin-url https://github.com/huguryildiz/aletheia
```

Then, inside your project: *"run the skill-library-generator"* — it scans (read-only),
interviews you, and scaffolds the record surfaces after your approval. Ten-minute tour:
[docs/quickstart.md](docs/quickstart.md) · install options (plugin vs plain `.claude/`
copy): [docs/install.md](docs/install.md) · full adoption walkthrough:
[docs/adopting-in-a-new-project.md](docs/adopting-in-a-new-project.md).

## Design principles (the short form)

1. **Ground-truth only** — every runbook step was verified against a real repo; inference
   is labeled.
2. **State is derived, not stored** — no mutable status file anywhere; verdicts live in
   immutable evidence and are recomputed.
3. **No source mutation** — agents are read-only reporters; writing is a skill action the
   human sees.
4. **Markdown only** — the only non-markdown files are `plugin.json` and a JSON Schema.

Full text + the portability gate: [docs/design-principles.md](docs/design-principles.md) ·
tier semantics + work-type routing: [docs/core-vs-extended.md](docs/core-vs-extended.md).

## Repository map

```text
skills/core/…  skills/extended/…  skills/skill-library-generator/
agents/        templates/         docs/          examples/uwsn-ankc.md
.claude-plugin/plugin.json        LICENSE (MIT)
```

## License

MIT © 2026 Huseyin Ugur Yildiz
