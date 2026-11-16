# Sources: explain-changes-mental-model (command)

Checked 2026-11-13. Review only: no `track` call, no registry or README edit made here.

## Origin found

- Softaworks original: `softaworks/agent-toolkit:commands/explain-changes-mental-model.md`, added by Leonardo Flores (@leonardocouy) in commit `673fe769` (2026-01-18, "add 6 agents and 4 commands from claude-plugins"). The commit message says the command came from "claude-plugins" without naming a repository; no earlier origin is named in the file and two web searches on its distinctive phrases ("Highlight the aha moments", "Foundation changes", "Key Concepts to Understand") found none. Treat softaworks as the only provable origin.
- Upstream blob at `main` (`2f28d4dd54ca8bc0d7bfe5a91db884c47c925ae4`, via `gh api repos/softaworks/agent-toolkit/contents/commands/explain-changes-mental-model.md`) is identical to the blob at the fork point `3027f20f` and at the recovery baseline `dbff837f`. The upstream has not changed since the fork, so the current file diverges from upstream only through this repo's own rewrites.
- Today the registry holds a `kind: local` row with empty source (`last_reviewed` 2026-11-04). The sibling commands viral-tweet and codex-plan carry a `github-path` row to the same upstream with a credit, so this command is inconsistent.

## Proposed registry rows (docs/audit/upstream-sources.json)

Replace the existing `local` row of `explain-changes-mental-model` with these four (codex-plan, which has no `local` row, is the precedent):

```json
{
  "skill": "explain-changes-mental-model",
  "kind": "github-path",
  "source": "softaworks/agent-toolkit:commands/explain-changes-mental-model.md",
  "ref": "main",
  "credit": "Leonardo Flores (@leonardocouy), via softaworks/agent-toolkit",
  "artifact_kind": "command"
}
```

```json
{
  "skill": "explain-changes-mental-model",
  "kind": "unversioned",
  "source": "GitHub CLI manual, gh pr diff: https://cli.github.com/manual/gh_pr_diff",
  "ref": null,
  "credit": "GitHub",
  "artifact_kind": "command"
}
```

```json
{
  "skill": "explain-changes-mental-model",
  "kind": "unversioned",
  "source": "Git documentation, git-diff (A..B versus A...B, --no-index, --cached): https://git-scm.com/docs/git-diff",
  "ref": null,
  "credit": "Git project",
  "artifact_kind": "command"
}
```

```json
{
  "skill": "explain-changes-mental-model",
  "kind": "unversioned",
  "source": "Git documentation, git-show (merge commits show a combined diff): https://git-scm.com/docs/git-show",
  "ref": null,
  "credit": "Git project",
  "artifact_kind": "command"
}
```

## Missing credit line

The root `README.md` "Command credits" paragraph (line 197) names viral-tweet and codex-plan only; explain-changes-mental-model has no credit although its text is derived from the softaworks file. Append to that paragraph (nothing existing is changed):

`explain-changes-mental-model is adapted from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit/blob/main/commands/explain-changes-mental-model.md) by Leonardo Flores (@leonardocouy), via softaworks/agent-toolkit.`

The line 5 fork notice already credits the repository as a whole; this one matches the per-command form.

## skill-updater style review (review only)

- Scope: `commands/explain-changes-mental-model.md`; not synced. Step 2: only a `local` row exists, so there is no `upstreams` row to read yet (it skips `local` rows). I read the upstream directly with `gh api` instead (read-only).
- Step 4 contents test: the path resolves on `main`; the blob equals the baseline. Upstream change since the fork: none, so there is nothing to adopt, adapt or ignore from a diff.
- Content review against the upstream file (the baseline): the upstream rules the current file no longer has are the ones in `record.md` (s007, s008, s010 drops, the s012 example). The current file is a deliberate rewrite that is stricter on source detection, size handling, grouping evidence and "state only what the patch proves".
- Model-validity pass: not run. No rule in the current file exists to counter a stylistic model habit (its rules guard git state: no checkout, stash or fetch; verify refs before use; do not invent changes), and the repo rails forbid judging with an LLM lane here. The one candidate, "mark author intent that you infer as inferred", is a truthfulness rule; keep it.
- Adopt / adapt / ignore list for the restore brief:
  - adopt: none (upstream unchanged).
  - adapt: none required. Optional, only if the restore round touches section 1: the old command name `/mental-model` appeared in the baseline usage block; the current block already uses the real name.
  - ignore: the old "Test/config changes depend on everything else" ordering and "Skip trivial changes" (contradicted by the current config-first and churn-check rules, both safety improvements).
- Optional improvement, not a restore item: `gh pr diff --exclude <glob>` (verified in `gh pr diff --help`, gh 2.101.0) can strip lockfiles and generated files before reading a large PR; the current text says a PR has "no pathspec", which stays true, since `--exclude` only filters out. Mention only if the controller wants to extend section 1; it is not required.
- Next skill-updater run (plan 9's cycle) should re-read the three docs pages; `upstreams` reports `stale: false` for `unversioned` rows by design.
