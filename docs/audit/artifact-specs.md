# Artifact specs: slash commands and subagents

Fetched 2026-10-31 with WebFetch. Statements not read from a fetched page are marked UNVERIFIED.
The WebFetch tool summarises pages with a small model, so field tables are second-hand renderings of the pages (not raw HTML); re-fetch before relying on a detail. Each page was longer than the first 100000 characters; the first 100000 were read for both.

## 1. Slash commands

- Source URL: https://code.claude.com/docs/en/slash-commands (content returned is the page "Extend Claude with skills", i.e. https://code.claude.com/docs/en/skills; no explicit redirect shown). Fetched 2026-10-31.
- Plugin layout source: https://code.claude.com/docs/en/plugins-reference ("Standard layout"), fetched 2026-10-31.
- Merge note (read): "Custom commands have been merged into skills. A file at `.claude/commands/deploy.md` and a skill at `.claude/skills/deploy/SKILL.md` both create `/deploy` and work the same way." Command files keep working; docs say prefer a skill for new work. If a skill and a command share a name, the skill runs.

### Location
- Project: `.claude/commands/<name>.md` (read). Subdirectory `frontend/component.md` becomes `/frontend:component` (read).
- Plugin: `commands/` at plugin root, "Flat Markdown command files. Prefer `skills/` for new plugins" (read, plugins-reference). A plugin manifest `commands` key replaces the default scan (read).
- Personal `~/.claude/commands/`: UNVERIFIED (page mentioned a personal location but not the exact path).

### Frontmatter
Command files accept the same fields as skills EXCEPT `name` and `paths`. The command name is the filename without extension. No field is strictly required; `description` is recommended (if omitted, the first non-empty line of the body is used).

| Field | Meaning |
| :- | :- |
| `description` | what it does and when to use it (recommended) |
| `when_to_use` | extra trigger context; counts toward the description cap |
| `argument-hint` | autocomplete hint, e.g. `[issue-number]` |
| `arguments` | named positional args for `$name` substitution (string or YAML list) |
| `disable-model-invocation` | `true` stops Claude loading it automatically (default false) |
| `user-invocable` | `false` hides it from the `/` menu (default true) |
| `allowed-tools` | tools usable without asking during the turn (space/comma list or YAML list) |
| `disallowed-tools` | tools removed from the pool while active |
| `model` | model override for the rest of the turn |
| `effort` | `low`, `medium`, `high`, `xhigh`, `max` |
| `context` | `fork` runs it in a forked subagent |
| `agent` | subagent type when `context: fork` |
| `background` | with `context: fork`, `false` waits for the result (default true) |
| `hooks` | hooks registered while invoked |
| `shell` | `bash` (default) or `powershell` for inline shell blocks |
| `metadata` | free-form map for own tooling |
| `license`, `compatibility` | Agent Skills spec fields, accepted but not acted on; `compatibility` up to 500 chars |

Not accepted in command files: `name`, `paths`. Plugin manifest object-map commands use camelCase `argumentHint`, `allowedTools`, `model`, `description` (read, plugins-reference).

### Arguments
`$ARGUMENTS` (all as typed; if no placeholder is used, `ARGUMENTS: <value>` is appended), `$ARGUMENTS[N]` and `$N` (0-based, shell-style quoting), `$name` (from `arguments`), `${CLAUDE_SESSION_ID}`, `${CLAUDE_EFFORT}`, `${CLAUDE_SKILL_DIR}`, `${CLAUDE_PROJECT_DIR}`. A missing indexed placeholder stays literal; a missing named one expands to empty; `\$` escapes a dollar sign.
Note: `$1` is the SECOND argument (0-based), so `$0` is the first.

### Validation rules (read)
- Name refused (file does not load) if it contains a zero-width space, control, private-use/unassigned or direction-changing character, a blank other than one plain space between words, or `<` / `>`.
- Reserved: `anthropic-skills` and `anthropic-skills:*`.
- Description: no min/max stated; `description` + `when_to_use` truncated at 1,536 chars in the listing. `<`/`>` display as `&lt;`/`&gt;`.
- Frontmatter is read only if the opening `---` is the first line. Unparseable YAML: file loads with no fields set. Unknown field names are ignored without error. Booleans accept true/false/yes/no/on/off/1/0.
- Command-name format (kebab-case, length): UNVERIFIED (none stated on the page).

## 2. Subagents

- Source URL: https://code.claude.com/docs/en/sub-agents, fetched 2026-10-31. Plugin layout: https://code.claude.com/docs/en/plugins-reference.

### Location (read)
Priority high to low: managed settings; `--agents` CLI flag; `.claude/agents/` (project); `~/.claude/agents/` (user); plugin `agents/` directory. Higher priority wins on a name clash. `.claude/agents/` and `~/.claude/agents/` are scanned recursively; identity comes only from `name`, not the path. Plugin `agents` manifest key takes `.md` files only, not directories, and replaces the default `agents/` scan (read, plugins-reference).

### Body
The Markdown after the closing `---` is the system prompt. The subagent gets only this prompt plus basic environment details, not the Claude Code system prompt.

### Frontmatter (required: `name`, `description` only)
| Field | Meaning |
| :- | :- |
| `name` | unique id, max 256 chars, no `:`, may not start with `-`; filename need not match |
| `description` | when Claude should delegate to it |
| `tools` | allowed tools, comma string or YAML list; inherits all if omitted |
| `disallowedTools` | tools to deny |
| `model` | `sonnet`, `opus`, `haiku`, `fable`, full model ID, or `inherit`; default per subagent model order |
| `permissionMode` | `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan`, `manual`; ignored for plugin agents |
| `maxTurns` | turn cap before partial stop |
| `autoCompactWindow` | auto-compact token count, 100000-1000000 (v2.1.296+) |
| `skills` | skills preloaded at start (first 32 names) |
| `mcpServers` | MCP servers (name or inline); ignored for plugin agents |
| `hooks` | subagent-scoped hooks; ignored for plugin agents |
| `memory` | `user`, `project` or `local` |
| `background` | `true` keeps it in the background |
| `omitClaudeMd` | `true` skips CLAUDE.md files (v2.1.271+) |
| `effort` | `low`, `medium`, `high`, `xhigh`, `max` |
| `isolation` | `worktree` |
| `color` | `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink`, `cyan` |
| `initialPrompt` | first user turn when run as main-session agent; ignored for plugin agents |
| `experimental` | map; `cacheTtl` is `5m` or `1h` (v2.1.248+) |

### Validation rules (read)
- Skipped silently: no `name`; opening `---` not first line; `name` starts with `-`, contains `:` or exceeds 256 chars; `name` present but `description` missing; YAML does not parse.
- `name` must be unique within a directory tree (duplicates: one loads, by filesystem order). Combined descriptions over 15,000 tokens trigger a startup warning. `tools` entries that resolve to nothing can fail the launch. Unrecognised fields are ignored.
- Description min/max length: none stated. Name case/kebab format: UNVERIFIED.

## 3. In this repository (observed)

Commands (7 files in `commands/*.md`; `commands/evals/` is not a command):
- `description`: 6 of 7; `argument-hint`: 5 of 7; `allowed-tools`: 2 of 7 (`Read, AskUserQuestion`; `Read, Write, Bash, AskUser`, comma lists, `AskUser` looks like a short name, UNVERIFIED as a valid tool).
- No frontmatter at all: 1 (`explain-pr-changes.md`, starts with `# PR workflow`). `model`: 0. Other fields: 0.
- `argument-hint` values are free text: `[target]`, `<tweet idea or topic>`, `"<what you want to plan>"`; the docs say `<`/`>` are for `argument-hint`, not `description`.

Agents (6 files in `agents/*.md`):
- `name` and `description`: 6 of 6 (in `mermaid-diagram-specialist.md` `description` is a folded multi-line scalar).
- `model`: 5 of 6 (`opus` 2, `sonnet` 2, `default` 1; `default` is NOT in the documented value list above). `color`: 4 of 6 (green 2, blue 1, purple 1); `tools`: 2 of 6 (`Grep, Glob, Read, LS`; `Read, Glob, Grep`).
- Non-documented fields (ignored by Claude Code per the page): `mermaid-diagram-specialist.md` carries `category`, `usage`, `input`, `output`. Documented but unused here: `permissionMode`, `skills`, `maxTurns`, `disallowedTools`, `memory`, `isolation`, `effort`.
