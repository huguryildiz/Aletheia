# Installing Aletheia

Three supported paths: as a **Claude Code plugin** (recommended for Claude Code — skills
stay updatable and namespaced), as a **plain template** copied into your project's
`.claude/` directory, or through **Codex's native plugin marketplace flow**
(harness-portable — the pack is markdown-only by design).

## Path A — Claude Code plugin

Try it for one session, no installation:

```bash
claude --plugin-dir /path/to/aletheia        # local clone
# or
claude --plugin-url https://github.com/huguryildiz/Aletheia
```

Install persistently: register this repository as a plugin marketplace, then install from it
(the marketplace name and the plugin name are both `aletheia`, per
[`.claude-plugin/marketplace.json`](../.claude-plugin/marketplace.json), so the install target
is `aletheia@aletheia`):

```bash
claude plugin marketplace add huguryildiz/Aletheia
claude plugin install aletheia@aletheia
```

Or, inside an interactive session, the `/plugin` slash-command equivalents:

```text
/plugin marketplace add huguryildiz/Aletheia
/plugin install aletheia@aletheia
```

Everything loads namespaced: `aletheia:correctness-gate`, `aletheia:phase-gate`,
`aletheia:skill-library-generator`, and the three agents (`aletheia:session-historian`,
`aletheia:drift-auditor`, `aletheia:verifier`).

**How discovery works** (verified against the plugins reference, 2026-07-06):

- The `skills` field in `.claude-plugin/plugin.json` declares the nested category
  directories (`./skills/core`, `./skills/extended`). This field **adds to** the default
  one-level `skills/` scan — which is what catches `skills/skill-library-generator/`.
- The `agents/` directory at the plugin root is auto-discovered; the manifest deliberately
  does **not** declare an `agents` field, because declaring one *replaces* the default
  scan instead of extending it.

Sanity check after changes to the manifest: `claude plugin validate ./aletheia --strict`.

## Path B — manual copy into `.claude/`

Plain `.claude/skills/` discovery is **one level deep**, so copy the **leaf skill folders**,
flattening the core/extended grouping (that grouping is repo-side human organization; the
plugin manifest is what bridges it):

```bash
# from the aletheia checkout, inside your project:
cp -R aletheia/skills/core/*      .claude/skills/
cp -R aletheia/skills/extended/*  .claude/skills/
cp -R aletheia/skills/skill-library-generator .claude/skills/
cp    aletheia/agents/*.md        .claude/agents/
```

Result: `.claude/skills/correctness-gate/SKILL.md` etc. — each leaf directly under
`skills/`. Skill names do not change (they come from frontmatter); only the namespace
prefix is absent compared to the plugin path.

## Path C — Codex CLI plugin

Codex's plugin format needs its own plugin root — a repository root cannot double as both
the Claude Code plugin root (`skills/core/`, `skills/extended/`, two levels deep) and a
Codex plugin root, because Codex's default `<plugin-root>/skills/*/SKILL.md` scan is
additive to (not replaced by) anything declared in `plugin.json`, and it would find
`skills/core` and `skills/extended` and fail validation since neither holds a `SKILL.md`
directly. So Aletheia gives Codex a separate plugin root:

- `plugins/aletheia/.codex-plugin/plugin.json` — plugin manifest, rooted at
  `plugins/aletheia/` instead of the repository root.
- `plugins/aletheia/skills/<name>/SKILL.md` — flattened Agent Skills surface (14 skills +
  1 generator + 3 former agents = 18 symlinks), implemented as symlinks to the canonical
  markdown sources under `skills/` and `agents/` — single source, no generated copies.
- `.agents/plugins/marketplace.json` — repo marketplace catalog; its plugin entry points
  at `./plugins/aletheia`.

Verified against OpenAI's own `plugin-creator` skill and its `validate_plugin.py`:
`python3 <path-to>/plugin-creator/scripts/validate_plugin.py plugins/aletheia` passes.

Add the marketplace from GitHub:

```bash
codex plugin marketplace add huguryildiz/Aletheia
codex plugin add aletheia@aletheia
```

Or test a local checkout:

```bash
codex plugin marketplace add ./aletheia
codex plugin add aletheia@aletheia
```

Bundled skills load namespaced by the plugin (`aletheia:correctness-gate`,
`aletheia:verifier`, etc.). There is no zero-install path for Codex the way Claude Code's
`--plugin-url` gives a single-session try: a live check with `codex debug prompt-input`
found no repo-scoped `.agents/skills` auto-discovery in this Codex CLI build, so the
marketplace-and-install flow above is the only verified route.

### Windows / symlink note (Paths B & C)

The Codex surface under `plugins/aletheia/skills/` is **relative symlinks**. A Windows
checkout made *without* developer mode or `git config core.symlinks true` does not
materialize them as links — each `SKILL.md` lands as a small text file whose contents are a
path string (e.g. `../../../../skills/core/correctness-gate/SKILL.md`), not the skill body,
and the agent runtime reads that literal path text instead of the discipline.

Fallback — **copy the sources, not the symlink surface**: use Path B's `cp -R` flatten,
which copies the real `skills/…/SKILL.md` bodies into `.claude/skills/` and never touches
the symlink layer. Equivalently, resolve links on copy (`cp -RL` / `git config --global
core.symlinks true` before cloning). Verify a copied skill is real content, not a one-line
path, before relying on it:

```bash
head -1 .claude/skills/correctness-gate/SKILL.md   # expect "---" (frontmatter), not a "../.." path
```

## After any path

1. Open your project in the target agent runtime and invoke the
   **`skill-library-generator`** skill — it interviews you, fills the config block in your
   `CLAUDE.md`, and scaffolds the record surfaces. (Or hand-fill from
   `templates/CLAUDE.md`.)
2. The skills resolve their `{{placeholder}}` references from that config block; without
   it they will ask rather than guess.

See [quickstart.md](quickstart.md) for the ten-minute version and
[adopting-in-a-new-project.md](adopting-in-a-new-project.md) for the full walkthrough.
