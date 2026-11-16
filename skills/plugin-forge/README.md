# CC Plugin Forge

A skill for building and maintaining Claude Code marketplace plugins: it scaffolds a plugin into an existing marketplace, bumps the plugin version where Claude Code reads it, and walks through validation, a local install test, and publishing. `SKILL.md` holds the script contract, the workflow and the gotchas; nothing here repeats them.

## When it triggers

Requests to create a Claude Code plugin, add skills, commands, agents, hooks or MCP servers to one, edit `plugin.json` or `marketplace.json`, bump a plugin version, or test and publish a plugin marketplace. It is not for VS Code, JetBrains or browser extensions, npm package releases, or a standalone skill or command that is not packaged as a plugin.

## Installation

**Claude Code:**

```bash
cp -r skills/plugin-forge ~/.claude/skills/
```

**claude.ai:** add the skill to project knowledge or paste `SKILL.md` into the conversation.

The scripts need Python 3.10+. Validation and install testing need the `claude` CLI.

## File structure

```
plugin-forge/
├── SKILL.md                          # Script contract, workflow, gotchas
├── README.md                         # This file
├── scripts/
│   ├── create_plugin.py              # Scaffold a plugin and register its marketplace entry (--dry-run to preview)
│   └── bump_version.py               # Bump the winning version (plugin.json, else the marketplace entry)
├── references/
│   ├── plugin-structure.md           # Layout, component names, plugin.json fields, path rules
│   ├── marketplace-schema.md         # marketplace.json fields, source types, pluginRoot, team distribution
│   └── workflows.md                  # Local install test, publish, user update flow
└── evals/                            # Output evals, fixtures in evals/files/, trigger queries
```

Script tests live in `tests/skills/plugin-forge/` at the repository root.

## Resources

- [Create a plugin](https://code.claude.com/docs/en/plugins/create)
- [Plugin manifest reference](https://code.claude.com/docs/en/plugins/manifest-reference)
- [Marketplace reference](https://code.claude.com/docs/en/plugins/marketplace-reference)
- [Plugin commands reference](https://code.claude.com/docs/en/plugins/cli-reference)
