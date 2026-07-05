# Adopting Aletheia in a new project

The full walkthrough: what the generator does, what it asks, what it creates, and what your
first weeks look like. (Ten-minute version: [quickstart.md](quickstart.md).)

## Before you start

- A git repository (existing code is fine; greenfield is fine).
- Twenty minutes of the maintainer's attention for the interview — the bindings encode
  *your* judgment about what is critical; they cannot be guessed well.
- Nothing else. No scripts run; Claude scaffolds via its file tools at invocation.

## Step 1 — run the generator

Invoke **`skill-library-generator`**. Its phases, and what you'll see:

1. **Discovery (read-only).** It scans layout, environment manifests, tests, docs, and
   recent git history. Every conclusion is labeled *observed* (with the path) or
   *inferred* (with the reasoning). Nothing is written.
2. **Interview.** For each config key it proposes a discovered value and asks you to
   confirm or correct: critical modules, gate command, canonical values, evidence dir,
   layers, record-surface paths, environment manifest, data dir. An honest "we don't have
   that yet" becomes a recorded gap with a recommendation — not an invented path.
3. **Failure-mode extraction.** From discovery + interview it lists your recurring failure
   modes and sorts them: covered-by-the-pack (a binding activates an existing skill) vs
   project-specific (a candidate local skill unique to your lab/domain).
4. **Drafts + audit.** Project-specific skills are drafted in the pack's house format,
   with re-verification commands that were actually run in your repo. Then it presents the
   complete plan and **stops**.
5. **Scaffold (only after your approval).** Config block + routing table into `CLAUDE.md`;
   `docs/decisions.md` with founding entry D01; `docs/build_log/`; the negative-results
   ledger; the evidence directory with its README and gitignore policy; the layout document.

## Step 2 — first working session

- Open with the **`session-historian`** agent (there is little history yet — that's fine;
  the habit is the point).
- Do one real piece of work and let the routing table in `CLAUDE.md` pick the discipline:
  exploration → notebook; kept run → evidence convention; decision → decision log.
- Before your first "it's done" on critical code, run the gate. If no gate exists yet, the
  generator flagged it — building a first gate (a handful of pinned scenarios with a stated
  tolerance) is the highest-value early investment in the whole pack.

## Step 3 — first phase closure

Define a small first phase with 3–5 written acceptance criteria
(`templates/phase-close-checklist.md`). When it feels done, invoke **`phase-gate`** and let
it verify each criterion against a named artifact. Expect one item to be OPEN — closing
that loop honestly, or taking a pre-declared off-ramp, is the discipline working, not
failing.

## Steadying rhythm (weeks 2+)

- **Execution turns**: work items from `TODO.md`; the buffer is rewritten per phase.
- **Gate turns**: phase ends via `phase-gate` → build-log entry → layer-sync audit →
  status board.
- **Maintenance turns**: `drift-auditor` on `recent` scope; stale docs are fixed at the
  source layer.
- Load-bearing claims meet the **`verifier`** agent before they travel
  (`external-positioning` for anything novelty-shaped).

## Growing your local library

Re-run the generator quarterly (or after any painful incident) in harvest mode: "what kept
going wrong that deserves a skill?" The pack's own history is the precedent — it was mined
from the accumulated working conventions of one real research repository; see
[../examples/uwsn-ankc.md](../examples/uwsn-ankc.md) for that mapping, including how each
shipped skill traces to a concrete practice.
