# Plugin Structure Reference

Source: https://code.claude.com/docs/en/plugins/manifest-reference and https://code.claude.com/docs/en/plugins/components (checked 2026-11-04).

## Default layout

Every path is relative to the plugin root. Add only the directories you use.

```
plugin-name/
├── .claude-plugin/plugin.json   # manifest; optional, but create_plugin.py writes one
├── skills/<skill>/SKILL.md      # preferred for new instructions
├── commands/<file>.md           # legacy flat command files
├── agents/<agent>.md
├── hooks/hooks.json
├── .mcp.json
├── .lsp.json
├── output-styles/
├── bin/                         # on the Bash tool's PATH while enabled; claude.ai and Cowork refuse plugins that have it
└── settings.json                # only `agent` and `subagentStatusLine` take effect
```

A `CLAUDE.md` at the plugin root is not loaded as context (`claude plugin validate` warns); put instructions in a skill.

## Component names

Every component is namespaced under the `plugin.json` `name`:

- `skills/deploy/SKILL.md` -> `/plugin-name:deploy`
- `commands/status.md` -> `/plugin-name:status`
- `commands/db/migrate.md` -> `/plugin-name:db:migrate` (each subdirectory adds a segment)
- agent `reviewer` -> `plugin-name:reviewer`

Confirm the names after install by typing `/plugin-name:` in a session. `claude plugin details <plugin-name>` lists skills and flat commands but omits commands in subdirectories (checked on Claude Code 2.1.318).

## plugin.json

`name` is the only required key: kebab-case, no spaces, `@`, `:` or path separators. Names starting with `claude-`, `anthropic-` or `cc-plugin-` fail validation as impersonating Anthropic.

Common optional keys: `version` (any string, not checked against semver; pins users until changed), `description`, `author` (`name` required, `email` and `url` optional), `homepage` (must parse as a URL or the plugin fails to load), `repository`, `license` (SPDX id), `keywords`, `displayName`, `dependencies`, `userConfig`.

Unknown top-level keys are stripped with a validate warning; an unknown key inside `userConfig`, `channels`, `lspServers` or `monitors` stops the plugin from loading.

## Component path rules

Needed only when components live outside the default layout:

- Paths start with `./` (`commands/foo.md` fails validation), stay inside the plugin root (no `..`), and must exist.
- `commands`, `agents` and `outputStyles` replace their default scan. To keep `commands/` and add more, list both: `"commands": ["./commands/", "./extras/"]`.
- `skills` adds to the default `skills/` scan.
- `hooks`, `mcpServers` and `lspServers` merge with `hooks/hooks.json`, `.mcp.json` and `.lsp.json`.
- `agents` takes `.md` files, not directories.
- In hook commands and MCP configs, reference bundled files as `${CLAUDE_PLUGIN_ROOT}/...`. An installed hosted plugin runs from a per-version cache directory, so that path changes on every version; keep durable files in `${CLAUDE_PLUGIN_DATA}`.
