# Quickstart — first gate in an afternoon

Aletheia in one sentence: **a set of runbooks that make a computational-research repo
produce evidence instead of anecdotes.** This page gets you from install to your first
enforced discipline.

## 1. Install (2 min)

Plugin or manual copy — see [install.md](install.md). Fastest trial:

```bash
claude --plugin-url https://github.com/huguryildiz/aletheia
```

## 2. Bind it to your repo (10 min, interactive)

In your project, ask Claude to run the **`skill-library-generator`** skill. It will:

- scan the repo (read-only) and propose bindings;
- interview you for the config block — the two questions that matter most:
  - *"Which modules, if silently wrong, corrupt your results?"* → `critical_modules`
  - *"Which single test command must pass before 'done' on those?"* → `gate_command`
- scaffold, **after your approval**: the config block in `CLAUDE.md`, `docs/decisions.md`
  (founding entry D01), `docs/build_log/`, and the `results/` evidence convention.

No generator run? Hand-fill `templates/CLAUDE.md` and copy `templates/decisions.md` — the
skills only need the config block to exist.

## 3. Use three disciplines this week

- **Touch a critical module** → the `correctness-gate` skill: gate must be green before
  "done"; red means bug or intentional change, never silence.
- **Run something you'll keep** → the `evidence-convention` skill:
  `results/<name>_<date>/meta.json`, with the *expected* outcome written **before** the run.
- **Make a real decision** → the `decision-log` skill: one numbered entry, newest on top.

Everything else escalates conditionally — the routing table in your `CLAUDE.md` (and
[core-vs-extended.md](core-vs-extended.md)) says when. Default is the minimum; never turn a
small change into bureaucracy.

## 4. Close your first phase

When a milestone feels done, ask for the **`phase-gate`** skill: it verifies the written
acceptance checklist item by item against named evidence, and blocks on anything OPEN.
The first closure is the moment the discipline pays for itself.

## Where to go next

- Full adoption walkthrough: [adopting-in-a-new-project.md](adopting-in-a-new-project.md)
- What ships and why: [core-vs-extended.md](core-vs-extended.md),
  [design-principles.md](design-principles.md)
- The worked exemplar the pack was mined from: [../examples/uwsn-ankc.md](../examples/uwsn-ankc.md)
