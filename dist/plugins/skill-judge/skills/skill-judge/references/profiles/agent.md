profile_version: 4
source_digest: f922066dae75510ff7373ba144d20d38d2fc7f63f330fadad7579cf1feebf8c9

# Agent profile

Load this only when the prompt judges an agent. Do not load it for a skill or a command.

The verdict JSON still names the artifact in `skill`. Set `skill` to the file stem (the file name without `.md`). `judge`, `rubric_version`, `spec_sha`, `scores`, `max`, `total`, `max_total`, `percent`, `grade` and `findings` stay as the schema defines them.

An agent has no `scripts/` directory and no script test. Do not read `tests/skills/<name>/` and do not deduct for a missing script test.

Score D1-D8 from `references/rubric.md`. A section below replaces only the skill-only part of that dimension. The body after the closing `---` is the system prompt.

## D1, D2, D3, D6

Unchanged. Judge the agent body. Do not look for a `SKILL.md` layout or a skill directory.

## D4 — frontmatter

Validity uses the agent fields recorded in `docs/audit/artifact-specs.md`. Every agent in this repository ships in a Claude Code plugin, so judge it as a plugin agent.

- Required by the spec: `name` and `description`. A missing `description` is high: the agent cannot be routed to. A missing `name` is low: a plugin agent still loads under its file name.
- `name` is at most 256 characters, must not contain `:` and must not start with `-`.
- A filename that differs from `name` is not a finding. Do not apply the skill `name` rules. (This repository's own tooling wants name equal to file stem; `audit.py check` reports that, not the judge.)
- Optional: `tools`, `disallowedTools`, `model`, `permissionMode`, `maxTurns`, `autoCompactWindow`, `skills`, `mcpServers`, `hooks`, `memory`, `background`, `omitClaudeMd`, `effort`, `isolation`, `color`, `initialPrompt`, `experimental`.
- `permissionMode`, `hooks`, `mcpServers` or `initialPrompt` in a plugin agent is low: the host ignores it. Ship hooks and MCP servers at plugin level instead.
- A `model` that is not `sonnet`, `opus`, `haiku`, `fable`, `inherit` or a full model ID is low. A `color` outside the eight documented names is low.
- An unknown field is low: the host ignores it.
- `skills:` takes a list of skill names. The spec does not say whether a skill of the agent's own plugin is written plain or plugin-namespaced: do not deduct for either form.

## D5 — progressive disclosure

Score whether bulky material was split out of the agent file. Preloading a skill through `skills:` counts as splitting bulky rules out of the body.

This repository's convention, not a spec rule. Score on the agent file's own length:

- 200 lines or fewer: 15, unless a finding shows a concrete split need.
- Over 200 lines with bulky rules moved into a preloaded skill: 10, with one finding naming what still belongs in the skill.
- Over 200 lines with nothing split out and no `skills:` preload: 4.

## D7 — tests and evals (15 points)

An agent has no eval location and no trigger queries. A missing eval file is never a finding by itself, and a missing script test is never a finding. Score D7 on this ladder only:

- 15, with no D7 finding: the body has a sentence that states when the task is done and it states the output format.
- At most 8, with one medium finding that names what is missing (the done-sentence, the output format, or both): otherwise.

## D8 — checks that apply

Apply the rubric checks that do not need `scripts/`:

- Follow each decision branch to its outcome and cite a branch that does not resolve.
- Follow each example to its outcome.
- Look for a fallback when the main path fails, and for stated edge cases.
- A multi-step agent needs a checklist or an ordered action list.

Do not score `--help`, structured script output, or a smoke test. A missing script test is not a finding.
