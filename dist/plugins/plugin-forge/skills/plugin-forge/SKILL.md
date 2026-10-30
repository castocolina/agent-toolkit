---
name: plugin-forge
description: "Create and manage Claude Code marketplace plugins: scaffold plugin directories, edit plugin.json and marketplace.json, add commands, skills, agents, hooks, and MCP components, bump versions, and test or publish packages. Use when packaging Claude Code capabilities or repairing marketplace registration/manifests. Not for other IDE extensions, npm releases, or authoring standalone skills/commands without plugin packaging."
---

# Claude Code Plugin Forge

Use `scripts/create_plugin.py` by default; manually scaffold only when the marketplace layout is non-standard. If `.claude-plugin/marketplace.json` is missing, initialize it with marketplace name, owner, and `plugins` per `references/marketplace-schema.md` first.

## Core workflow

If repository files or script execution are unavailable, state that limitation and still answer with the concrete scaffold behavior: `create_plugin.py` updates an existing marketplace manifest and generates the plugin `.claude-plugin/plugin.json` and `README.md`; it does not create a missing marketplace manifest.

1. Confirm marketplace root and valid kebab-case plugin name.
2. Run `python3 scripts/create_plugin.py ...`; the script requires an existing marketplace manifest.
3. Run `python3 scripts/create_plugin.py <name> --marketplace-root <root> --author-name <name> --author-email <email> --description <text> --keywords <comma,separated,keywords>`. The script updates an existing marketplace manifest and generates the plugin's `.claude-plugin/plugin.json` plus `README.md`. It requires the marketplace manifest to exist; if missing, initialize it manually first as described in `references/marketplace-schema.md`. Add components at plugin root: `commands/`, `skills/`, `agents/`, `hooks/`, `.mcp.json`. For questions about schemas or paths, load `references/plugin-structure.md`.
4. Register paths and metadata in marketplace manifest. Load `references/marketplace-schema.md` for initialization or distribution.
5. Before publication validate both manifests, every referenced component path, and invoke each new command/skill/agent. Exercise hook/MCP behavior when present. Install/reinstall locally and verify the installed version after Claude Code reload. Load `references/workflows.md` for detailed testing/publishing steps.
6. Bump with `python3 scripts/bump_version.py <name> major|minor|patch`; both the `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` manifest versions must match.

Pattern choice: skills plus references → Framework; commands only → Utility; curated domain knowledge → Domain.

## Gotchas

- `plugin.json` belongs under `.claude-plugin/`, but component paths resolve from plugin root; placing components inside `.claude-plugin/` breaks discovery.
- Never update only `plugin.json`: marketplace version drift can make installs skip the intended release.
- Reinstalling may leave cached plugin files active; restart Claude Code and verify the loaded version before trusting tests.

## References and tools

- `references/plugin-structure.md`: component layout, manifests, and path/schema questions.
- `references/marketplace-schema.md`: marketplace initialization, catalog, or distribution.
- `references/workflows.md`: end-to-end local testing and publishing.
- `scripts/create_plugin.py`: scaffold; emits a JSON result on stdout, diagnostics on stderr.
- `scripts/bump_version.py`: synchronized version update; emits JSON result on stdout.
