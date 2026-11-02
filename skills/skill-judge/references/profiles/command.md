# Command profile

Load this only when the prompt judges a command. Do not load it for a skill or an agent.

The verdict JSON still names the artifact in `skill`. Set `skill` to the file stem (the file name without `.md`). `judge`, `rubric_version`, `spec_sha`, `scores`, `max`, `total`, `max_total`, `percent`, `grade` and `findings` stay as the schema defines them.

A command has no `scripts/` directory and no script test. Do not read `tests/skills/<name>/` and do not deduct for a missing script test.

Score D1-D8 from `references/rubric.md`. A section below replaces only the skill-only part of that dimension.

## D1, D2, D3, D6

Unchanged. Judge the command body. Do not look for a `SKILL.md` layout, a `name` field, or a skill directory.

## D4 — frontmatter

Validity uses the command fields recorded in `docs/audit/artifact-specs.md`.

- No field is required. `description` is recommended. If it is omitted, the host uses the first non-empty body line.
- Accepted: `description`, `when_to_use`, `argument-hint`, `arguments`, `disable-model-invocation`, `user-invocable`, `allowed-tools`, `disallowed-tools`, `model`, `effort`, `context`, `agent`, `background`, `hooks`, `shell`, `metadata`, `license`, `compatibility`.
- Not accepted: `name`, `paths`. Do not apply the skill `name` rules or the directory-name check.
- A missing `description` is medium, never critical: the file still loads.
- An unknown field is low: the host ignores it.

## D5 — progressive disclosure

Score whether bulky material was split out of the command file.

This repository's convention, not a spec rule: an artifact with no references scores full marks when it is under 200 lines. Over 200 lines with nothing split out scores at most 10.

## D7 — tests and evals

A command requires an eval file at `commands/evals/<stem>.json`.

- Missing that file is a high finding and puts D7 in the bottom band.
- Commands have no trigger queries. Do not deduct for a missing trigger file.
- Do not deduct for a missing script test.

## D8 — checks that apply

Apply the rubric checks that do not need `scripts/`:

- Follow each decision branch to its outcome and cite a branch that does not resolve.
- Follow each example to its outcome.
- Look for a fallback when the main path fails, and for stated edge cases.
- A multi-step command needs a checklist or an ordered phase list.

Do not score `--help`, structured script output, or a smoke test. A missing script test is not a finding.
