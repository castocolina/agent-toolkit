# Agent profile

Load this only when the prompt judges an agent. Do not load it for a skill or a command.

The verdict JSON still names the artifact in `skill`. Set `skill` to the file stem (the file name without `.md`). `judge`, `rubric_version`, `spec_sha`, `scores`, `max`, `total`, `max_total`, `percent`, `grade` and `findings` stay as the schema defines them.

An agent has no `scripts/` directory and no script test. Do not read `tests/skills/<name>/` and do not deduct for a missing script test.

Score D1-D8 from `references/rubric.md`. A section below replaces only the skill-only part of that dimension. The body after the closing `---` is the system prompt.

## D1, D2, D3, D6

Unchanged. Judge the agent body. Do not look for a `SKILL.md` layout or a skill directory.

## D4 — frontmatter

Validity uses the agent fields recorded in `docs/audit/artifact-specs.md`.

- Required: `name` and `description`. Missing either is critical: the host skips the file.
- `name` is at most 256 characters, must not contain `:`, and must not start with `-`.
- A filename that differs from `name` is not a finding. Do not apply the skill `name` rules.
- Optional: `tools`, `disallowedTools`, `model`, `permissionMode`, `maxTurns`, `autoCompactWindow`, `skills`, `mcpServers`, `hooks`, `memory`, `background`, `omitClaudeMd`, `effort`, `isolation`, `color`, `initialPrompt`, `experimental`.
- An unknown field is low: the host ignores it.

## D5 — progressive disclosure

Score whether bulky material was split out of the agent file.

This repository's convention, not a spec rule: an artifact with no references scores full marks when it is under 200 lines. Over 200 lines with nothing split out scores at most 10.

## D7 — tests and evals

An agent has no required eval file.

- A missing eval file is a medium finding, never high.
- That finding does not by itself put D7 in the bottom band.
- Agents have no trigger queries. Do not deduct for a missing trigger file.
- Do not deduct for a missing script test.

## D8 — checks that apply

Apply the rubric checks that do not need `scripts/`:

- Follow each decision branch to its outcome and cite a branch that does not resolve.
- Follow each example to its outcome.
- Look for a fallback when the main path fails, and for stated edge cases.
- A multi-step agent needs a checklist or an ordered action list.

Do not score `--help`, structured script output, or a smoke test. A missing script test is not a finding.
