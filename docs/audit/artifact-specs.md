# Artifact specs: slash commands and subagents (Claude Code)

command_digest: 564ae70c48564766185724c264b0cf06090f769e55a73ec07382034852564a62
agent_digest: f922066dae75510ff7373ba144d20d38d2fc7f63f330fadad7579cf1feebf8c9
skills: 118879 bytes, sha256 d2a5d07c0d1cef1d1edcf30f38f6b2712ff70ac050e3d50601cd3dadb42f9097
sub-agents: 116225 bytes, sha256 0fc7d550f8580d12fefae642c4c74b84889817cb3c9f41501c38093016448532
plugins-reference: 43335 bytes, sha256 a10a371d18d571e769f99720d4402f3ec13ceb668561266f57145cfa940fa4ed

Derived 2026-11-02 from the raw Markdown of three pages, each read to its last line:
`https://code.claude.com/docs/en/skills.md`, `.../sub-agents.md`, `.../plugins-reference.md`.
The pins live in `skills/skill-judge/references/claude-code/SOURCE.json`; the digests above must equal it
(`rubric-check` enforces this). The tables are our own wording, not copies of the pages. Short quotes are
collected in section 4. Anything the pages do not state is marked UNVERIFIED with a reason.
Scope: Claude Code plugins only (commands and agents ship through `.claude-plugin/marketplace.json`).

## 1. Commands

A command is a flat Markdown file. The pages treat commands as merged into skills (quote Q1): a command file and a
skill of the same name both create `/name`, and when both exist the skill wins.

### Location and name
- Project `.claude/commands/<name>.md`; a subfolder becomes a `:` separator (`frontend/component.md` is `/frontend:component`).
- Plugin: `commands/` at the plugin root, namespaced as `/plugin-name:command` (a manifest object-map key `about` in plugin `deploy-tools` runs as `/deploy-tools:about`). The plugins page steers new work to `skills/` (Q2).
- A manifest `commands` key replaces the default `commands/` scan; list `./commands/` explicitly to keep it.
- The command name is the file name without extension; there is no `name` field.
- Personal `~/.claude/commands/`: UNVERIFIED. The pages name only the project path and added directories.
- Command-name format (kebab-case, length): UNVERIFIED. No rule is stated for command files.

### Frontmatter
All fields are optional; `description` is recommended (without it the first non-empty body line is used).
Same fields as a skill except `name` and `paths`.

| Field | Our reading |
| :- | :- |
| `description` | what and when; `description` + `when_to_use` is cut at 1,536 chars in the listing; `<` `>` display escaped |
| `when_to_use` | extra trigger text, counts toward the same cap |
| `argument-hint` | autocomplete hint such as `[issue-number]` |
| `arguments` | named positions for `$name`; space string or YAML list |
| `disable-model-invocation` | `true`: only the user runs it; also blocks preloading into subagents; default false |
| `user-invocable` | `false` hides it from the `/` menu; default true |
| `allowed-tools` | tools pre-approved for the invoking turn only; space/comma string or list; does not restrict the pool |
| `disallowed-tools` | tools removed from the pool for the turn |
| `model` | model for the rest of the turn, or `inherit`; with `context: fork` it sets the subagent's model |
| `effort` | `low`, `medium`, `high`, `xhigh`, `max` |
| `context` | `fork` runs the body as the task of a new subagent |
| `agent` | subagent type for `context: fork`; default `general-purpose` |
| `background` | only with `context: fork`; `false` waits for the result; default true |
| `hooks` | hooks registered while the command is active |
| `shell` | `bash` (default) or `powershell` for inline `!` commands |
| `metadata` | free-form map, not acted on |
| `license`, `compatibility` | Agent Skills spec fields, accepted and not acted on; `compatibility` is a string up to 500 chars |

Plugin manifest object-map commands use their own camelCase keys: `source` xor `content` (setting both or neither fails
validation), `description`, `argumentHint`, `model`, `allowedTools`.

### Body features
`$ARGUMENTS` (all as typed; appended as `ARGUMENTS: <value>` when no placeholder consumes it), `$ARGUMENTS[N]` and `$N`
(0-based, so `$0` is the first), `$name`, `${CLAUDE_SESSION_ID}`, `${CLAUDE_EFFORT}`, `${CLAUDE_SKILL_DIR}`,
`${CLAUDE_PROJECT_DIR}`, and in plugins `${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}`. A missing indexed placeholder stays
literal, a missing named one becomes empty, `\$` escapes. Inline `` !`cmd` `` runs before the model sees the body; a failing
command aborts the whole invocation. Body size: the pages state 500 lines for `SKILL.md`, nothing for commands; the 200-line
limit used by the profiles is a repository convention.

### Validation rules
- Name refused (file does not load): zero-width or control character, private-use or unassigned character, direction-changing character, any blank other than one plain space between words, `<` or `>`.
- Reserved: `anthropic-skills` and names starting `anthropic-skills:` do not load outside a plugin.
- Frontmatter is read only when the opening `---` is line 1. Unparseable YAML: the body still loads with no fields. Unknown fields are ignored without an error. Booleans accept true/false/yes/no/on/off/1/0 in any case.
- No minimum or maximum description length is stated beyond the 1,536 listing cap.

## 2. Agents (subagents)

The Markdown body is the whole system prompt; the agent gets only that plus environment details, not the Claude Code prompt.

### Location, priority, identity
| Priority | Location |
| :- | :- |
| 1 | managed settings `.claude/agents/` |
| 2 | `--agents` CLI JSON (session only) |
| 3 | project `.claude/agents/` (walked up to the repo root; closest wins) |
| 4 | user `~/.claude/agents/` |
| 5 | plugin `agents/` (lowest) |

- A higher location wins when names clash. `.claude/agents/` and `~/.claude/agents/` are scanned recursively and identity comes only from `name`, never the path.
- Plugin agents are also scanned recursively, but a subfolder becomes part of the scoped identifier: `agents/review/security.md` in plugin `my-plugin` is `my-plugin:review:security`. Every plugin agent is addressable as `plugin:agent`; `--agent security-reviewer` also works when no other plugin has that name.
- The manifest `agents` key takes `.md` file paths only (never directories) and replaces the default `agents/` scan.
- Built-ins: `Explore`, `Plan`, `general-purpose`, plus `claude`, `statusline-setup`, `claude-code-guide`. The page states that a user or project agent named `Explore` overrides the built-in (Q7). Same override for `general-purpose`: UNVERIFIED, the page states it only for `Explore` and its priority table does not list built-ins.
- Same name twice in one directory tree: one loads, chosen by file system order, not a documented rule.

### Frontmatter
Required: `name`, `description`. Field names are camelCase and must match exactly; an unrecognised field is ignored silently (Q3).

| Field | Our reading |
| :- | :- |
| `name` | unique id, at most 256 chars, no `:` (reserved for plugin scope), must not start with `-`; the file name need not match (Q4) |
| `description` | when to delegate; all agent descriptions together over 15,000 tokens give a startup warning (agents still load) |
| `tools` | allowlist, comma string or list; all tools if omitted; `Agent(a, b)` limits spawnable types only for a `--agent` main thread |
| `disallowedTools` | denylist applied before `tools`; a specifier like `Bash(git push *)` still removes the whole tool |
| `model` | `sonnet`, `opus`, `haiku`, `fable`, a full model ID, or `inherit`; omitted means the model order below |
| `permissionMode` | `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan`, `manual` (alias of default); ignored for plugin agents |
| `maxTurns` | turn cap; output is then marked partial and can be resumed |
| `autoCompactWindow` | integer 100000-1000000 (write `200000`, not `200k`); needs v2.1.296 |
| `skills` | skills whose full content is injected at startup, first 32 distinct names |
| `mcpServers` | server names or inline definitions; ignored for plugin agents |
| `hooks` | agent-scoped hooks; ignored for plugin agents |
| `memory` | `user`, `project` or `local`; adds a memory directory and Read/Write/Edit |
| `background` | `true` keeps it in the background |
| `omitClaudeMd` | `true` skips user, project and local CLAUDE.md; needs v2.1.271 |
| `effort` | `low`, `medium`, `high`, `xhigh`, `max` |
| `isolation` | `worktree` |
| `color` | `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink`, `cyan` (not accepted in `--agents` JSON) |
| `initialPrompt` | first user turn when the agent runs as the main session agent; ignored for plugin agents |
| `experimental` | map; only `cacheTtl` (`5m` or `1h`) is read |

Model order: per-call parameter, then the agent's `model` (`inherit` selects the main model), then `CLAUDE_CODE_SUBAGENT_MODEL`,
then the main conversation's model.

### Plugin agents
- `hooks`, `mcpServers`, `permissionMode` are ignored (Q5), and the field table adds `initialPrompt`. Plugin authors ship hooks in `hooks/hooks.json` and MCP servers in `.mcp.json` instead.
- A plugin agent with no `name`, or one whose YAML does not parse, still loads under its file name (Q6). Whether a plugin agent without `description` loads: UNVERIFIED, the skip list covers project, user, managed and `--add-dir` directories only.
- `skills:` value format for an agent that preloads a skill of its own plugin: UNVERIFIED. The sub-agents page shows only plain names (`api-conventions`) and says plugin skills stay reachable through the Skill tool (Q8); the skills page names plugin skills `/plugin-name:skill` for invocation and says a name already carrying the plugin prefix is not prefixed twice (a `name` rule, not a `skills:` rule). No page says whether `skills:` takes the plain name or the namespaced one for plugin skills. A wrong value is silent: a listed skill that is missing is skipped with a debug-log warning only (Q9). Verify at run time with `claude --debug` before relying on either form.
- A skill with `disable-model-invocation: true` cannot be preloaded. Preloading is the inverse of `context: fork` in a skill.

### Files Claude Code skips (project, user, managed, `--add-dir`; silent)
No `name` (treated as documentation); opening `---` not on line 1; `name` starting with `-`, containing `:` or over 256 chars;
`name` without `description`; YAML that does not parse. `claude plugin validate <dir>` finds unparseable frontmatter but not a
missing `name`.

### Repository convention, not a spec rule
`audit.py check --kind agent` requires `name` to equal the file stem because verdicts are keyed by the file stem. The pages
say the file name does not have to match (Q4), so a mismatch breaks this repository's tooling, not Claude Code.

## 3. In this repository (observed 2026-10-31, not re-counted)


Commands (7 files in `commands/*.md`; `commands/evals/` is not a command):
- `description`: 6 of 7; `argument-hint`: 5 of 7; `allowed-tools`: 2 of 7 (`Read, AskUserQuestion`; `Read, Write, Bash, AskUser`, comma lists, `AskUser` looks like a short name, UNVERIFIED as a valid tool).
- No frontmatter at all: 1 (`explain-pr-changes.md`, starts with `# PR workflow`). `model`: 0. Other fields: 0.
- `argument-hint` values are free text: `[target]`, `<tweet idea or topic>`, `"<what you want to plan>"`; the docs say `<`/`>` are for `argument-hint`, not `description`.

Agents (6 files in `agents/*.md`):
- `name` and `description`: 6 of 6 (in `mermaid-diagram-specialist.md` `description` is a folded multi-line scalar).
- `model`: 5 of 6 (`opus` 2, `sonnet` 2, `default` 1; `default` is NOT in the documented value list above). `color`: 4 of 6 (green 2, blue 1, purple 1); `tools`: 2 of 6 (`Grep, Glob, Read, LS`; `Read, Glob, Grep`).
- Non-documented fields (ignored by Claude Code per the page): `mermaid-diagram-specialist.md` carries `category`, `usage`, `input`, `output`. Documented but unused here: `permissionMode`, `skills`, `maxTurns`, `disallowedTools`, `memory`, `isolation`, `effort`.

## 4. Quotes (each at most 25 words)

- Q1 (skills.md): "Custom commands have been merged into skills."
- Q2 (plugins-reference.md): "Prefer `skills/` for new plugins"
- Q3 (sub-agents.md): "Claude Code ignores a field it doesn't recognize without reporting an error."
- Q4 (sub-agents.md): "The filename doesn't have to match."
- Q5 (sub-agents.md): "These fields are ignored when loading agents from a plugin."
- Q6 (sub-agents.md): "whose frontmatter has no `name` or doesn't parse still loads, under its filename."
- Q7 (sub-agents.md): "named `Explore` overrides the built-in"
- Q8 (sub-agents.md): "Subagents can still invoke unlisted project, user, and plugin skills through the Skill tool"
- Q9 (sub-agents.md): "Claude Code skips it and logs a warning to the debug log."
