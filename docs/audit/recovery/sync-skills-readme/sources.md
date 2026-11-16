# Sources: sync-skills-readme (command)

Checked 2026-11-15. Review only: no `track` call was made and no registry or README edit.

## Origin

- The command comes from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit), file `commands/sync-skills-readme.md`, by Leonardo Flores (@leonardocouy). Its history there is `a6ca35c1` (add project commands) and `570f26c7` (Meta category, 2026-01-19, the last commit on that path).
- The file at the baseline `dbff837f` is byte-identical to the upstream file at `3027f20f` (`git diff 3027f20f dbff837f` is empty) and to the upstream `main` file today (git blob `232e86af` on both sides). So the baseline text is the upstream original and every difference in the current file is a local rewrite ("adapted from").
- The current registry row is `kind: local` (reviewed 2026-11-04), which is wrong: the command has an upstream. The current command file and root `README.md` carry no credit line for it (the "Command credits" paragraph names five other commands).
- The repo also holds `.claude/commands/sync-skills-readme.md`, the project-local copy of the same upstream command. It is outside the artifact and is reported only (it still names GPT-5.2; see `docs/audit/upstream-findings.md` line 9).

## Proposed registry rows (docs/audit/upstream-sources.json)

Replace the `local` row of `sync-skills-readme` with these four rows (same fields as the `viral-tweet` and `codex-plan` rows):

```json
{
  "skill": "sync-skills-readme",
  "kind": "github-path",
  "source": "softaworks/agent-toolkit:commands/sync-skills-readme.md",
  "ref": "main",
  "credit": "Leonardo Flores (@leonardocouy), via softaworks/agent-toolkit",
  "artifact_kind": "command"
}
```

```json
{
  "skill": "sync-skills-readme",
  "kind": "unversioned",
  "source": "Agent Skills specification (SKILL.md frontmatter fields): https://agentskills.io/specification",
  "ref": null,
  "credit": "Agent Skills",
  "artifact_kind": "command"
}
```

```json
{
  "skill": "sync-skills-readme",
  "kind": "unversioned",
  "source": "Claude Code, Extend Claude with skills (command frontmatter and $ARGUMENTS): https://code.claude.com/docs/en/slash-commands",
  "ref": null,
  "credit": "Anthropic",
  "artifact_kind": "command"
}
```

```json
{
  "skill": "sync-skills-readme",
  "kind": "unversioned",
  "source": "Claude Code, Tools reference (Bash and Grep tool behavior): https://code.claude.com/docs/en/tools-reference",
  "ref": null,
  "credit": "Anthropic",
  "artifact_kind": "command"
}
```

The last two `source` strings reuse the titles of the existing `codex-plan` and `compose-email` rows (the first matches them exactly, the second adds a parenthetical). If the controller prefers an identical title, copy the `codex-plan` one: `Claude Code, Tools reference: https://code.claude.com/docs/en/tools-reference`.

The `credit` of the first row appears verbatim in the root README "Command credits" paragraph once the line below is added, which `check --strict` (`missing_credit`) needs.

## Missing credit line

A command has no README, so the credit goes in the root `README.md`, appended to the "Command credits:" paragraph (line 197), in the style of its neighbours:

`sync-skills-readme is adapted from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit/blob/main/commands/sync-skills-readme.md) by Leonardo Flores (@leonardocouy), via softaworks/agent-toolkit; its frontmatter and tool facts follow the Agent Skills specification and Anthropic's documentation (Anthropic).`

(README.md is not edited by this analysis; the controller adds the line.)

## skill-updater style review (review only)

- Rows: only `kind: local`, so `upstreams` skips the artifact; steps 3 to 5 do not apply until the row above exists.
- Upstream change since the baseline: none. `main` has the same blob as the baseline and a single commit on the path (`570f26c7`, 2026-01-19), which is already in our history. Decision: ignore (nothing to adopt or adapt). Record `current` with `--sha 570f26c70aa682e6706c39a07b50e6ee357012d3` when the row exists (`track` is the controller's call).
- Model-validity pass: two rules counter a model habit, "never add model versions, context sizes or other details the description does not state" (summary inflation, which produced the stale GPT-5.2 row) and "do not use Grep to parse frontmatter" (reading one line of a folded description). Both stay; no probe was run (no probe lane was used in this analysis) and nothing is proposed for removal.
- Adopt / adapt / ignore items for the restore brief:
  - adopt: none.
  - adapt: none. Nothing is restored (every section is `not-lost` or an `intended-change`).
  - ignore: the baseline's "Advanced code analysis with GPT-5.2" and "Large-scale review (200k+ context)" examples (stale, contradict the current rule); the dropped second shortening example "API handoff docs for frontend" (low value, same pattern as the kept example).
  - source fixes: replace the `local` row, add the credit line, add the three `unversioned` rows (listed above).
- Not done: `track`, `updates.md` entry (the controller records it if wanted).
