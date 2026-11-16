# command-creator: sources (checked 2026-11-07)

## Origins found

1. **softaworks/agent-toolkit, `skills/command-creator`.** The baseline (`dbff837f`) files `SKILL.md`, `README.md` and `references/{patterns,examples,best-practices}.md` are byte-identical to the fork point `3027f20f` (`git diff --stat 3027f20f dbff837f` is empty for all five), and the upstream `main` copy of `SKILL.md`, `README.md` and `best-practices.md` is still byte-identical to the baseline (compared through `gh api`). Upstream's last commit on the path is `2423b4f0` (2026-01-19, "replace invalid agent references"); nothing changed upstream since the fork. No registry row exists for it yet (`rg command-creator docs/audit/upstream-sources.json` finds none).
2. **The erk project (dagster-io/erk).** The skill text and its four examples (`submit-stack`, `ensure-ci`, `create-implementation-plan`, `codex-review`) come from erk: erk file paths, the erk-specific `dot-agent` PR names, `make all-ci`, `.PLAN.md`, and the upstream commit message above ("devrun agent" was erk's own agent). The current README already credits the examples to erk. vibeindex lists a `command-creator` skill under dagster-io/erk ("ERK skill that helps create new slash commands ...", https://www.vibeindex.ai/skills/dagster-io/erk/command-creator, third-party listing). `gh api repos/dagster-io/erk` returns 404 from this machine and the github.com tree URL returned 404, so the repository could not be read directly (private, renamed or moved); the registry row is therefore `unversioned`, not `github`, and the license could not be checked.
3. **Official Claude Code and vendor docs** used to verify facts (see facts.md). Each page is an `unversioned` row.

## Proposed registry rows (docs/audit/upstream-sources.json, one JSON object per line)

```json
{"skill": "command-creator", "kind": "github-path", "source": "softaworks/agent-toolkit:skills/command-creator", "ref": "main", "credit": "softaworks/agent-toolkit"}
{"skill": "command-creator", "kind": "unversioned", "source": "dagster-io/erk, command-creator skill and the example commands in references/examples.md: https://github.com/dagster-io/erk", "ref": null, "credit": "Dagster Labs (dagster-io/erk)"}
{"skill": "command-creator", "kind": "unversioned", "source": "Claude Code docs, Skills (custom commands merged into skills, frontmatter, substitutions): https://code.claude.com/docs/en/skills", "ref": null, "credit": "Anthropic"}
{"skill": "command-creator", "kind": "unversioned", "source": "Claude Code docs, Explore the .claude directory (commands/*.md scope and fields): https://code.claude.com/docs/en/claude-directory", "ref": null, "credit": "Anthropic"}
{"skill": "command-creator", "kind": "unversioned", "source": "Claude Code docs, Subagents (built-in types, Task renamed Agent): https://code.claude.com/docs/en/sub-agents", "ref": null, "credit": "Anthropic"}
{"skill": "command-creator", "kind": "unversioned", "source": "Claude Code docs, Tools reference (TodoWrite and Task tools): https://code.claude.com/docs/en/tools-reference", "ref": null, "credit": "Anthropic"}
{"skill": "command-creator", "kind": "unversioned", "source": "Claude Code docs, Commands (the / menu): https://code.claude.com/docs/en/commands", "ref": null, "credit": "Anthropic"}
{"skill": "command-creator", "kind": "unversioned", "source": "Graphite docs, CLI command reference (gt submit, restack, log): https://graphite.com/docs/command-reference", "ref": null, "credit": "Graphite"}
{"skill": "command-creator", "kind": "unversioned", "source": "Ruff docs, Linter (fixes and unsafe fixes): https://docs.astral.sh/ruff/linter/", "ref": null, "credit": "Astral"}
{"skill": "command-creator", "kind": "unversioned", "source": "Ruff docs, Formatter (format --check): https://docs.astral.sh/ruff/formatter/", "ref": null, "credit": "Astral"}
```

The `github-path` row can be tracked (upstream exists and is unchanged). The erk row cannot be checked by `upstreams` (no `github` kind possible while the repository is unreachable); re-read the repository with `gh` when it is reachable and then replace the row with a `github-path` one. The npm docs page returned empty content, so no npm row is proposed (the `npm view` fact is a pointer).

## Credit line

The existing README credit is kept as is: "The worked examples in `references/examples.md` are real commands from the erk project, adapted here." It does not name the softaworks origin of the skill itself, so a credit line is missing. Exact line to add after it in `skills/command-creator/README.md` (the controller or restore dispatch adds it; the existing line is not edited):

> This skill is adapted from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit/tree/main/skills/command-creator), whose command-creator skill and examples come from the erk project (dagster-io/erk).

The root README already carries the general line "Fork of softaworks/agent-toolkit by @leonardocouy", so no root change is needed.

## skill-updater style review (review only; no `track` call, no edit)

Method: read `skills/skill-updater/SKILL.md`; applied steps 2 to 5 by hand with `gh api` read-only calls (no `upstreams` or `track` run, since no row exists yet).

- **Upstream softaworks path:** reachable, `error: null` equivalent, content equal to our baseline; no upstream change to classify. Adopt: none. Adapt: none. Ignore: nothing pending.
- **Official docs diff against the current artifact** (adopt or adapt items for the restore brief, all small and all on the current files, none restoring old text):
  1. **adapt** (fact-update): SKILL.md Location note says the pinned docs "document the project path only". The `.claude` directory reference now lists `commands/*.md` for project and global scope. Replace the sentence with a pointer to that page; keep the advice to tell the user to check that `/<name>` appears.
  2. **adopt**: add one Gotchas line: `<` and `>` inside `description` display as `&lt;` and `&gt;`; use square brackets there (an `argument-hint` is not affected).
  3. **adopt**: add to the broken-frontmatter Gotcha how to find it: `claude --debug` shows the parse error and `claude plugin validate <dir>` lists files whose frontmatter does not parse (page says v2.1.233 or later; read `claude plugin validate --help` for the live flag).
  4. **adapt**: the Frontmatter table lists nine fields; add a pointer to the live frontmatter reference (https://code.claude.com/docs/en/skills#frontmatter-reference) for the rest (`when_to_use`, `user-invocable`, `disallowed-tools`, `background`, `hooks`, `shell`), instead of copying them.
  5. **ignore**: bang-line exit-code nuance (exit 1 from some search commands is injected); the current `|| true` advice is safe as written.
  6. **ignore**: `${CLAUDE_SKILL_DIR}`, `${CLAUDE_PLUGIN_ROOT}` and plugin-scoped commands; the skill writes plain project and personal commands.
- **Model-validity pass:** not run. The brief forbids judging with an LLM lane (rail 4) and the skill's rules counter no single model habit that a one-shot probe could test (they are platform behaviors: placeholder substitution, bang-line timing, shadowing). Recorded as skipped.
- **Dropped baseline rows that cite stale vendor facts** (`Task tool`, `subagent_type=subagent`, TodoWrite, `gt` as git-town) are recorded in record.md and facts.md; none of them is restored.
