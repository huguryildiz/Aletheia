# Contributing to Aletheia

Aletheia is **markdown only** — the discipline ships as runbooks an agent or a person
follows, not as code to install. Contributions keep that property.

## Ground rules

1. **Single source.** Every skill body lives once, under `skills/core/`, `skills/extended/`,
   or `skills/skill-library-generator/`; auditor procedures live under `agents/`. The Codex
   surface at `plugins/aletheia/skills/` is **relative symlinks** to those sources — never
   edit a copy, never add a generated one.
2. **No domain terms in `skills/` or `templates/`.** The pack is portable by construction; a
   mechanical gate requires zero domain vocabulary there. Concrete instantiation belongs in
   [`examples/`](examples/) only.
3. **Ground-truth only.** A runbook step must be verified against a real repository. Label
   inference as inference. A wrong runbook is worse than none.
4. **Record decisions.** A significant change adds an entry at the top of
   [`docs/decisions.md`](docs/decisions.md) (ADR-lite; superseded entries stay in place).

## Workflow

- Open an issue describing the discipline gap before a large change.
- Keep edits surgical: touch only what the change requires.
- Non-markdown shipped files are limited to declarative manifests, marketplace metadata,
  schema files, and presentation assets — no executable code.

## License

By contributing you agree that your contributions are licensed under the
[MIT License](LICENSE).
