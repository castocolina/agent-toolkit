# codex-plan (command): sources

## Origin found

- The command is `softaworks/agent-toolkit:commands/codex-plan.md`, written by Leonardo Flores (@leonardocouy): commits `69ed8873` (2026-01-19) and `8bbb1fb8` (2026-01-22). `git rev-parse 3027f20f:commands/codex-plan.md` and `dbff837f:commands/codex-plan.md` are the same blob (`2760514f`), so the recovery baseline is the upstream file byte for byte, and everything the baseline holds is upstream text.
- The upstream file is unchanged since: `gh api repos/softaworks/agent-toolkit/commits?path=commands/codex-plan.md` lists `8bbb1fb8` as the newest commit, and the contents API blob sha is `2760514f...`. softaworks/agent-toolkit is MIT licensed (checked with `gh api repos/softaworks/agent-toolkit/license`, 2026-11-07). Its main head is `3027f20f3181` (2026-03-05).
- No further origin: web searches on the plan template headings ("Test-First Approach", "Estimated Complexity", "Dependency Graph", "Potential Risks", "Rollback Plan") and on the `codex exec --full-auto --skip-git-repo-check -c model_reasoning_effort=high --output-last-message` recipe found no earlier source of this text, only generic test-plan guides and cheat sheets. Nothing else is credited.
- Today the registry holds only `{"skill": "codex-plan", "kind": "local", ..., "artifact_kind": "command"}` (no upstream), and the root README has no credit line for codex-plan (only viral-tweet has one under "Command credits"). Both are wrong: the command has an upstream.

## Proposed registry rows (docs/audit/upstream-sources.json)

Replace the existing `kind: local` row of codex-plan with the first row below (a `local` row means "no upstream"); add the five docs rows. One JSON object per line:

```json
{"skill": "codex-plan", "kind": "github-path", "source": "softaworks/agent-toolkit:commands/codex-plan.md", "ref": "main", "credit": "Leonardo Flores (@leonardocouy), via softaworks/agent-toolkit", "artifact_kind": "command"}
{"skill": "codex-plan", "kind": "unversioned", "source": "OpenAI Codex, Non-interactive mode: https://learn.chatgpt.com/docs/non-interactive-mode", "ref": null, "credit": "OpenAI", "artifact_kind": "command"}
{"skill": "codex-plan", "kind": "unversioned", "source": "OpenAI Codex, Configuration Reference: https://learn.chatgpt.com/docs/config-file/config-reference", "ref": null, "credit": "OpenAI", "artifact_kind": "command"}
{"skill": "codex-plan", "kind": "unversioned", "source": "OpenAI Codex, Agent approvals & security: https://learn.chatgpt.com/docs/agent-approvals-security", "ref": null, "credit": "OpenAI", "artifact_kind": "command"}
{"skill": "codex-plan", "kind": "unversioned", "source": "Claude Code, Tools reference: https://code.claude.com/docs/en/tools-reference", "ref": null, "credit": "Anthropic", "artifact_kind": "command"}
{"skill": "codex-plan", "kind": "unversioned", "source": "Claude Code, Extend Claude with skills (command frontmatter and $ARGUMENTS): https://code.claude.com/docs/en/slash-commands", "ref": null, "credit": "Anthropic", "artifact_kind": "command"}
```

Notes: `validate_entry` accepts no `credit` on `local` rows, so the `local` row is replaced, not kept beside the new ones. The old developers.openai.com/codex/* addresses answer with 308 redirects to learn.chatgpt.com (checked 2026-11-07), so the registry uses the final addresses. If the controller prefers to keep the `local` row until `skill-updater` runs, the first row can be added with `track` afterwards; this analyst made no `track` call.

## Missing credit line (root README.md; the controller applies it)

Under "Command credits" (README.md line 197), append to that paragraph, keeping the viral-tweet sentence unchanged:

`codex-plan is adapted from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit/blob/main/commands/codex-plan.md) by Leonardo Flores (@leonardocouy), via softaworks/agent-toolkit.`

Also in README.md line 189 the table row says "Create implementation plans using Codex 5.2" (stale model name, see facts.md); proposed text: `Prepare a prompt so you can run Codex yourself and get an implementation plan`. The command file itself has no credit line (commands carry none; the root README is the place).

## Skill-updater style review (review only; no `track` call, no edit)

- Rows: only a `local` row today, so `upstreams` would skip it. The upstream was compared by hand: blob `2760514f` upstream main equals the baseline and the fork point, newest path commit `8bbb1fb8` is inside the baseline. No upstream change to adopt, adapt or ignore. Status once the row is added: `current`, `--sha 8bbb1fb8a898d8c7b11431b46f84b4dc3aa7789a` is the newest commit touching the path.
- Adopt / adapt / ignore for the restore brief (the "upstream" here is the baseline text itself):
  - **adapt** s011 plan template, task guidelines and bad/good decomposition: restore into `commands/codex-plan.md` (own file; the command is about 69 lines, so it stays well under 200) as a compact skeleton under the Prompt contents heading, and keep the current rules: sections that do not apply are dropped (Rollback), every task carries the fields the current list names, verified paths only. Write the decomposition example without a package name (see facts.md), and keep "Follow test-driven development: specify what tests to write BEFORE implementation" as the existing Test-First field. Add an eval scenario that checks the prompt carries the dependency graph (parallel start tasks, critical path), the task guidelines and the testing-strategy levels.
  - **adapt (optional, small)** s008: add "existing tests (to show the testing pattern) and type definitions" to the step 1 list of files to read; the current list names manifest, schema, entry points, middleware and `.env.example`, and a plan for "add testing" needs the existing tests. This is not a record row (the section is `not-lost`), so it is the controller's call.
  - **ignore** s009/s014 recipe (`--full-auto`, `-c model=gpt-5.2-codex`, Portuguese comments, /tmp output file): unsupported flag, stale pin, and the current command is safer.
  - **ignore** s002 "Execute Codex" and s013 "Always ask clarifying questions first": contradict the current manual-run and readiness-gate design.
  - **ignore** s004, s005, s010 question topics and banks (dropped, generic).
- Model-validity pass: rules that counter a model habit are "Never add `--full-auto` or `-s danger-full-access`" (models trained on older docs recommend `--full-auto`; codex-cli 0.162.1 now rejects it, so the rule is kept and its evidence is the CLI output, not a probe), "ask only blocking questions" (counters over-asking) and "do not run `codex` yourself". No LLM probe was run (this analyst may not dispatch or judge with an LLM lane); keep all three; propose no removal.
