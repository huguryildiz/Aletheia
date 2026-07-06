<!-- markdownlint-disable MD024 -->
# Decision Log

The Aletheia repository's significant decisions + their rationale. This file is a
summary (ADR-lite); detailed behavior remains in the relevant docs and skill files.

## Conventions

- **Status**: `accepted` / `superseded` / `rejected` / `deferred`
- New decision -> added at the top; superseded entries stay in place
- Conclusions, not discussion; follow links for detail
- Numbers are assigned at write time, never reserved in advance

Ordering: date (new -> old).

---

## D03 — Give the Codex plugin its own root folder, separate from the repo root

**Status**: accepted
**Date**: 2026-07-06

**Context**: D02 put `.codex-plugin/plugin.json` at the repository root and pointed its
`skills` field at `.agents/skills/`. Verified against OpenAI's own bundled
`plugin-creator` skill and its `validate_plugin.py`, this fails validation: a
manifest's `skills` field is *additive* to the default `<plugin-root>/skills/*/SKILL.md`
scan, not a replacement for it. Because the repo root's own `skills/` directory is two
levels deep (`skills/core/<name>`, `skills/extended/<name>`, for the Claude Code plugin),
Codex's default scan finds `skills/core` and `skills/extended` as if they were skill
folders and fails because neither contains a `SKILL.md` directly. The repo root cannot
double as both plugins' root without this collision.

**Decision**:

1. Move the Codex plugin manifest to `plugins/aletheia/.codex-plugin/plugin.json` — a
   plugin root separate from the repository root, so its default `skills/` scan never
   sees the Claude-oriented `skills/core|extended` layout.
2. Populate `plugins/aletheia/skills/<name>/SKILL.md` (flattened, 19 skills + 3 former
   agents) as relative symlinks to the canonical sources under `skills/` and `agents/`;
   no generated copies, no `skills` field in `plugin.json` (default discovery already
   matches this shape).
3. Point `.agents/plugins/marketplace.json`'s plugin entry at
   `"path": "./plugins/aletheia"` (relative to the repo root, per the marketplace path
   convention), not `"./"`.
4. Drop the plain `.agents/skills/` tree: a live check with `codex debug prompt-input`
   run from the repository root did not list a repo-scoped `.agents/skills` root at all
   in this Codex CLI build, so that path bought no real auto-discovery — only the
   marketplace/plugin path is verified to work (`validate_plugin.py` passes on
   `plugins/aletheia`).

**Impact**: `codex plugin marketplace add huguryildiz/Aletheia` then
`codex plugin add aletheia@aletheia` installs a manifest that actually validates.
D02's repo-root manifest and its `.agents/skills` claim are superseded; D01's
single-source-via-symlink principle is preserved, just rooted at
`plugins/aletheia/skills/` instead.

---

## D02 — Add a separate native Codex plugin surface

**Status**: superseded (-> D03)
**Date**: 2026-07-06

**Context**: Codex can install Aletheia through the legacy-compatible `.claude-plugin/`
layout, but that makes the Codex distribution depend on a Claude-named metadata folder.
Codex's native plugin shape has a `.codex-plugin/plugin.json` manifest and a repo
marketplace catalog at `.agents/plugins/marketplace.json`. Aletheia should expose that
native surface while keeping skill bodies single-source.

**Decision**:

1. Keep `.claude-plugin/marketplace.json` and `.claude-plugin/plugin.json` for Claude Code.
2. Add `.codex-plugin/plugin.json` for Codex's native plugin manifest.
3. Add `.agents/plugins/marketplace.json` for Codex's repo marketplace catalog.
4. Populate `.agents/skills/<name>/SKILL.md` as relative symlinks to the canonical
   markdown sources under `skills/` and `agents/`; no generated copies.

**Impact**: Claude Code and Codex now have separate native metadata folders, but the
operating discipline remains single-source: edits land in `skills/` or `agents/`, and
Codex sees those files through symlinks. Codex users can add the repository as a
marketplace source and install `aletheia@aletheia`.

---

## D01 — Use symlinked Codex Agent Skills as the native distribution

**Status**: superseded (-> D02)
**Date**: 2026-07-06

**Context**: Aletheia already ships as a Claude Code plugin and as plain markdown skill
folders, but Codex CLI now discovers repo-scoped Agent Skills from `.agents/skills`.
Duplicating every `SKILL.md` into that path would create a second source of truth that can
drift from the Claude plugin surface. The pack's own design principles favor markdown-only
portability and layer-sync discipline over generated copies or bootstrap scripts.

**Decision**:

1. Add `.agents/skills/<name>/SKILL.md` entries as relative symlinks to the canonical
   markdown sources under `skills/core/`, `skills/extended/`, `skills/skill-library-generator/`,
   and `agents/`.
2. Carry the three read-only auditor procedures (`session-historian`, `drift-auditor`,
   `verifier`) as Codex-invoked skills rather than adding `.codex/agents/*.toml`.
3. Do not add an `agents/openai.yaml`, repo-wide Codex manifest, bootstrap script, or
   generated-copy step.

**Impact**: A Codex session opened inside an Aletheia clone sees the native skill surface
without installation. Claude Code continues to read the canonical plugin skill and agent
files. Manual adoption into another repository is a snapshot copy, like the existing
Claude `.claude/skills/` path; the Aletheia source repository remains single-source.
