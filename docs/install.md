# Installing Aletheia

Two supported paths: as a **Claude Code plugin** (recommended — skills stay updatable and
namespaced) or as a **plain template** copied into your project's `.claude/` directory
(harness-portable — the pack is markdown-only by design).

## Path A — Claude Code plugin

Try it for one session, no installation:

```bash
claude --plugin-dir /path/to/aletheia        # local clone
# or
claude --plugin-url https://github.com/huguryildiz/aletheia
```

Install persistently: add this repository as a plugin marketplace (see the official Claude
Code *plugin marketplaces* documentation), then:

```bash
claude plugin install aletheia@<your-marketplace-name>
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

## After either path

1. Open your project in Claude and invoke the **`skill-library-generator`** skill — it
   interviews you, fills the config block in your `CLAUDE.md`, and scaffolds the record
   surfaces. (Or hand-fill from `templates/CLAUDE.md`.)
2. The skills resolve their `{{placeholder}}` references from that config block; without
   it they will ask rather than guess.

See [quickstart.md](quickstart.md) for the ten-minute version and
[adopting-in-a-new-project.md](adopting-in-a-new-project.md) for the full walkthrough.
