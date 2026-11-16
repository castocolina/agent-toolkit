# Sources: explain-pr-changes (command)

Checked 2026-11-13. Review only: no `track` call, no registry or README edit made here.

## Origin found

- Softaworks original: `softaworks/agent-toolkit:commands/explain-pr-changes.md`, added by Leonardo Flores (@leonardocouy) in commit `673fe769` (2026-01-18, "feat: add 6 agents and 4 commands from claude-plugins"; the message lists "explain-pr-changes: Explain PR changes clearly"). The message says the command came from "claude-plugins" without naming a repository. A web search on the distinctive phrases ("Code-Sage", "expert AI code reviewer and technical writer", "Holistic Analysis", the `NEEDS_REVIEW` / `APPROVED` triage) found no earlier source; the hits were unrelated "CodeSage" projects. Treat softaworks as the only provable origin.
- Upstream blob at `main` (`gh api repos/softaworks/agent-toolkit/contents/commands/explain-pr-changes.md`) is `8ef54cd2090dd5776882014059004fe9cea5636d`, the same blob as at the fork point `3027f20f` and at the recovery baseline `dbff837f` (`git rev-parse dbff837f:commands/explain-pr-changes.md`). The upstream has had one commit on this path (`673fe769`) and none since the fork, so the current file diverges only through this repository's own rewrites (diagram modes, promotion reuse, `gh --attach`, 2026-10-28 onward).
- Today the registry holds a `kind: local` row with empty source (`last_reviewed` 2026-11-04). The sibling commands viral-tweet, codex-plan and explain-changes-mental-model carry (or are proposed) a `github-path` row to the same upstream with a credit, so this command is inconsistent.
- Inside the repository: the body templates and the Mermaid, draw.io and branch-publish recipes this command used to hold inline now live in `skills/pr-diagrams/references/pr-body.md` and `skills/mermaid-diagrams/references/authoring-rules.md`; those are our own text and need no row here.

## Proposed registry rows (docs/audit/upstream-sources.json)

Replace the existing `local` row of `explain-pr-changes` with these (codex-plan, which has no `local` row, is the precedent). One origin row, then one `unversioned` row per official page used for the facts in `facts.md`:

```json
{
  "skill": "explain-pr-changes",
  "kind": "github-path",
  "source": "softaworks/agent-toolkit:commands/explain-pr-changes.md",
  "ref": "main",
  "credit": "Leonardo Flores (@leonardocouy), via softaworks/agent-toolkit",
  "artifact_kind": "command"
}
```

```json
{
  "skill": "explain-pr-changes",
  "kind": "unversioned",
  "source": "GitHub CLI manual, gh pr create (--head, --attach, partial attach failure): https://cli.github.com/manual/gh_pr_create",
  "ref": null,
  "credit": "GitHub",
  "artifact_kind": "command"
}
```

```json
{
  "skill": "explain-pr-changes",
  "kind": "unversioned",
  "source": "GitHub CLI manual, gh pr edit (--attach, --add-reviewer, --body-file): https://cli.github.com/manual/gh_pr_edit",
  "ref": null,
  "credit": "GitHub",
  "artifact_kind": "command"
}
```

```json
{
  "skill": "explain-pr-changes",
  "kind": "unversioned",
  "source": "GitHub CLI manual, gh pr list (--head, --state, --limit, JSON fields): https://cli.github.com/manual/gh_pr_list",
  "ref": null,
  "credit": "GitHub",
  "artifact_kind": "command"
}
```

```json
{
  "skill": "explain-pr-changes",
  "kind": "unversioned",
  "source": "GitHub CLI manual, gh pr view (JSON fields, --repo with an argument): https://cli.github.com/manual/gh_pr_view",
  "ref": null,
  "credit": "GitHub",
  "artifact_kind": "command"
}
```

```json
{
  "skill": "explain-pr-changes",
  "kind": "unversioned",
  "source": "GitHub CLI release v2.99.0, attach images and videos to issues and pull requests: https://github.com/cli/cli/releases/tag/v2.99.0",
  "ref": null,
  "credit": "GitHub",
  "artifact_kind": "command"
}
```

```json
{
  "skill": "explain-pr-changes",
  "kind": "unversioned",
  "source": "GitHub Docs, Creating diagrams (Mermaid in pull requests): https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams",
  "ref": null,
  "credit": "GitHub",
  "artifact_kind": "command"
}
```

```json
{
  "skill": "explain-pr-changes",
  "kind": "unversioned",
  "source": "Claude Code, Plugins reference (environment variables, where ${CLAUDE_PLUGIN_ROOT} resolves): https://code.claude.com/docs/en/plugins-reference",
  "ref": null,
  "credit": "Anthropic",
  "artifact_kind": "command"
}
```

```json
{
  "skill": "explain-pr-changes",
  "kind": "unversioned",
  "source": "Claude Code, Extend Claude with skills (command frontmatter and $ARGUMENTS): https://code.claude.com/docs/en/slash-commands",
  "ref": null,
  "credit": "Anthropic",
  "artifact_kind": "command"
}
```

```json
{
  "skill": "explain-pr-changes",
  "kind": "unversioned",
  "source": "Git release notes 2.23 (git switch) and 2.22 (git branch --show-current): https://github.com/git/git/blob/master/Documentation/RelNotes/2.23.0.adoc",
  "ref": null,
  "credit": "Git project",
  "artifact_kind": "command"
}
```

```json
{
  "skill": "explain-pr-changes",
  "kind": "unversioned",
  "source": "Git documentation, git-log (--merges): https://git-scm.com/docs/git-log",
  "ref": null,
  "credit": "Git project",
  "artifact_kind": "command"
}
```

Not proposed as rows: the user-attachments URL form (verified from the gh source, not a docs page: https://github.com/cli/cli, `internal/attachments/`), the Mermaid syntax page (https://mermaid.js.org/syntax/stateDiagram.html, only a pointer for diagram keywords; the mermaid-diagrams skill owns Mermaid sources), and the 65,536-character PR body limit (no official page found).

## Missing credit line

The root `README.md` "Command credits" paragraph (line 197) names viral-tweet, codex-plan and explain-changes-mental-model; explain-pr-changes has no credit although its text derives from the softaworks file. Append to that paragraph (nothing existing is changed):

`explain-pr-changes is adapted from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit/blob/main/commands/explain-pr-changes.md) by Leonardo Flores (@leonardocouy), via softaworks/agent-toolkit; its `gh` and `git` facts follow the GitHub CLI manual and release notes (GitHub) and the Git documentation (Git project).`

The line 5 fork notice already credits the repository as a whole; this one matches the per-command form.

## skill-updater style review (review only)

- Scope: `commands/explain-pr-changes.md`; not synced. Step 2: only a `local` row exists, so there is no `upstreams` row to read (it skips `local` rows); I read the upstream directly with `gh api` (read-only).
- Step 4 contents test: the path resolves on `main`; the upstream blob equals the baseline blob, and `commits?path=` returns only `673fe769`. Upstream change since the fork: none, so there is nothing to adopt, adapt or ignore from a diff.
- Content review against the upstream file (the baseline): the rules the current file no longer states in its own body are listed in `record.md`. Two are redistributed, not lost: the body templates (old s009, s010) to `skills/pr-diagrams/references/pr-body.md`, loaded by section 5 under both literal paths, and the diagram-type and quoting guidance (old s007) to `skills/mermaid-diagrams/references/authoring-rules.md`, loaded by 2.9. Two are dropped as generic (the Code-Sage persona, the "holistic analysis" instruction). The current file is a deliberate rewrite: stricter on base and head resolution, size bound, data-not-code handling of PR titles and bodies, and one-diagram-per-run.
- Model-validity pass: not run. The repo rails forbid judging with an LLM lane in this role, and no rule here exists to counter a stylistic model habit: the rules guard git and gh state (no push of a promotion head, one `gh pr view` per source, quoted titles), so they stay. The one candidate, "do not add conversational text inside the body", is a format rule the PR body needs; keep it.
- Adopt / adapt / ignore list for the restore brief:
  - adopt: none (upstream unchanged).
  - adapt: none required. No restore row exists for this artifact (record.md has no `restore-*` or pending rows).
  - ignore: the Code-Sage persona, the unconditional "Close $ARGUMENTS" (the current feature-path-only rule is the safer one), `origin/main` as a fixed base (the current base is resolved from the open PR or `--base`), and the in-file template (it lives in the pr-diagrams reference).
- Findings outside this artifact, for the controller (not edited here, they belong to the pr-diagrams skill): `skills/pr-diagrams/scripts/pr-diagrams.sh` line 272 prints `gh 2.<minor> has no --attach, using branch` for every gh below 2.101, but the official release notes show `--attach` shipped in v2.99.0 (see the `pointer` row in `facts.md`); and `skills/pr-diagrams/README.md` states the 2.101 floor as a user choice, which is a valid policy but not a statement about gh. If the controller wants the message accurate, reword it to "below the 2.101 floor" in the pr-diagrams batch.
- Optional, not a restore item: 2.9's "when neither exists, apply these minimums" Mermaid fallback has no diagram-type choice line (the old s007 listed flowchart, sequenceDiagram, stateDiagram-v2). It only matters when neither authoring-rules.md path exists; a one-line addition would be harmless but is not owed, because the content is reachable in the normal case.
- Next skill-updater run (plan 9's cycle) should re-read the unversioned pages; `upstreams` reports `stale: false` for `unversioned` rows by design.
