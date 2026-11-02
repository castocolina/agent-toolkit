profile_version: 4
source_digest: 564ae70c48564766185724c264b0cf06090f769e55a73ec07382034852564a62

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
- Not accepted: `name`, `paths`. Do not apply the skill `name` rules or the directory-name check. The command name is the file name.
- A missing `description` is medium, never critical: the file still loads.
- An unknown field is low: the host ignores it.

## D5 — progressive disclosure

Score whether bulky material was split out of the command file.

This repository's convention, not a spec rule. A command cannot ship its own `references/`; material moved into a skill its plugin bundles, and loaded by an explicit path only when needed, counts as split out. Score on the command file's own length:

- 200 lines or fewer: 15, unless a finding shows a concrete split need.
- Over 200 lines with bulky material split out as above: 10, with one finding naming what still belongs elsewhere.
- Over 200 lines with nothing split out: 4.

## D7 — tests and evals (15 points)

A command requires an eval file at `commands/evals/<stem>.json`. Commands have no trigger queries: do not deduct for a missing trigger file and do not deduct for a missing script test. Score D7 on this ladder only:

- 15: the eval file has at least three realistic scenarios that cover the main path, a failure path and an edge case, each with assertions that can be verified.
- 12: the main path and one failure path are covered.
- 8: the main path only.
- At most 3, with a high finding: no eval file.

Every score below 15 needs a finding that names the missing scenario kind. A scenario without verifiable assertions does not count toward a rung.

## D8 — checks that apply

Apply the rubric checks that do not need `scripts/`:

- Follow each decision branch to its outcome and cite a branch that does not resolve.
- Follow each example to its outcome.
- Look for a fallback when the main path fails, and for stated edge cases.
- A multi-step command needs a checklist or an ordered phase list.

Do not score `--help`, structured script output, or a smoke test. A missing script test is not a finding.
