# sync-branch sources

## Origin found

- Baseline `dbff837f` and the first import (`673fe769`, "feat: add 6 agents and 4 commands from claude-plugins") hold a 16-line command whose text is byte-identical to `softaworks/agent-toolkit:commands/sync-branch.md` (read through `gh api repos/softaworks/agent-toolkit/contents/commands/sync-branch.md`). The upstream file has exactly one commit, `673fe76917d9fcf73ef059a40c6e543f95bfad98` (2026-01-18); this checkout's import commit has the same hash, so the artifact is a fork-inherited copy and upstream has not changed since.
- The softaworks path carries no credit line of its own; the command file has none either. Credit follows the other softaworks commands in this repo: "Leonardo Flores (@leonardocouy), via softaworks/agent-toolkit" (the same author line the registry uses for compose-email, explain-pr-changes and sync-skills-readme).
- Today the registry holds only a `local` row (`source: ""`) for sync-branch, which is wrong: the baseline is a softaworks file, and the current text is a heavy rewrite of it (a derivative).

## Proposed registry rows

Replace the existing `local` row of sync-branch with these (verbatim JSON):

```json
{
  "skill": "sync-branch",
  "kind": "github-path",
  "source": "softaworks/agent-toolkit:commands/sync-branch.md",
  "ref": "main",
  "credit": "Leonardo Flores (@leonardocouy), via softaworks/agent-toolkit",
  "artifact_kind": "command"
}
```

```json
{
  "skill": "sync-branch",
  "kind": "unversioned",
  "source": "Git documentation, git-rebase (--onto, --rebase-merges, --continue, --abort, ours and theirs during a rebase): https://git-scm.com/docs/git-rebase",
  "ref": null,
  "credit": "Git project",
  "artifact_kind": "command"
}
```

```json
{
  "skill": "sync-branch",
  "kind": "unversioned",
  "source": "Git documentation, git-push (--force-with-lease=<refname>:<expect>, -u): https://git-scm.com/docs/git-push",
  "ref": null,
  "credit": "Git project",
  "artifact_kind": "command"
}
```

```json
{
  "skill": "sync-branch",
  "kind": "unversioned",
  "source": "Git documentation, git-merge-base (--is-ancestor, --fork-point): https://git-scm.com/docs/git-merge-base",
  "ref": null,
  "credit": "Git project",
  "artifact_kind": "command"
}
```

```json
{
  "skill": "sync-branch",
  "kind": "unversioned",
  "source": "Git documentation, git-cherry (patch-equivalence output): https://git-scm.com/docs/git-cherry",
  "ref": null,
  "credit": "Git project",
  "artifact_kind": "command"
}
```

```json
{
  "skill": "sync-branch",
  "kind": "unversioned",
  "source": "Git documentation, git-status, git-rev-parse (--git-path), git-fetch (--prune, FETCH_HEAD), git-branch (--show-current), git-diff (--diff-filter), git-rev-list (--merges), git-log: https://git-scm.com/docs",
  "ref": null,
  "credit": "Git project",
  "artifact_kind": "command"
}
```

```json
{
  "skill": "sync-branch",
  "kind": "unversioned",
  "source": "GitHub CLI manual, gh pr view (JSON fields; no baseRepository field): https://cli.github.com/manual/gh_pr_view",
  "ref": null,
  "credit": "GitHub",
  "artifact_kind": "command"
}
```

```json
{
  "skill": "sync-branch",
  "kind": "unversioned",
  "source": "Claude Code, Tools reference (AskUserQuestion): https://code.claude.com/docs/en/tools-reference",
  "ref": null,
  "credit": "Anthropic",
  "artifact_kind": "command"
}
```

```json
{
  "skill": "sync-branch",
  "kind": "unversioned",
  "source": "Claude Code, Extend Claude with skills (command frontmatter): https://code.claude.com/docs/en/slash-commands",
  "ref": null,
  "credit": "Anthropic",
  "artifact_kind": "command"
}
```

(Registry rows for Git documentation pages already exist for other artifacts in the same wording style, for example git-status, git-rev-parse and git-log; the rows above are per artifact, so the `skill` field differs.)

## Credit line

- Missing in the root README command-credits paragraph (the only place credits live for commands; sync-branch is not named there). Line to add, in the existing style:

  `sync-branch is adapted from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit/blob/main/commands/sync-branch.md) by Leonardo Flores (@leonardocouy), via softaworks/agent-toolkit; its `git` and `gh` facts follow the Git documentation (Git project), the GitHub CLI manual (GitHub) and Anthropic's documentation (Anthropic).`

- The command file itself has no credit line and the baseline had none to preserve; the coordinator decides whether to add one there (the README row is the repo's convention for commands).
- README line 193 also lists the command as "Sync feature branch with main" (not edited by me).

## Skill-updater style review (review only, no `track` call)

- Upstream: one commit in the path history (`673fe769`, 2026-01-18) equals the baseline text; the file at `main` is still the same 16 lines (read). Nothing new upstream: no adopt/adapt candidates from upstream.
- Local divergence from upstream, all adapt/intended: steps 1-5 kept in order (fetch, target, rebase, conflicts, force-with-lease push); the conflict step changed from "resolve any conflicts" to "stop, name files, no push" (safety), `origin/${target:-main}` became an explicit ref with fork-point handling, and the push gained an explicit lease and recovery text.
- The artifact has a `local` registry row only, so `upstreams` would skip it; recommend the github-path row above (the registry change is for the coordinator, not edited here). With that row, `ours_updated` reads `git log` on `commands/sync-branch.md`, which has commits, so `track` would work.
- Model-validity pass: not run (no `track` call is made and the rules are git-safety rules, not model-habit counters); nothing to propose for removal.
- Factual defect to fix in the restore brief: `gh pr view --json baseRepository` is not a valid field (see facts.md). Suggested replacement for the preamble sentence: use `gh pr view --json url,isCrossRepository` and take owner/repo from the PR `url` as the base repository, else ask once.
- Evals (`commands/evals/sync-branch.json`, 7 evals, 3 or 2 assertions each): every assertion matches the current command (default target main, `origin/develop`, fetch before rebase, explicit lease on the saved remote tip, quoted branch, detached HEAD and on-target refusals, dirty-tree stop, conflict message). Coverage gaps worth an eval, none contradicting the command: fork PR with an `upstream` remote (would have caught the `baseRepository` fault), remote-only commits (`git cherry` with `+` lines), fork-point differing from the plain merge base, merge commits and `--rebase-merges`, rebase stopping without conflicts, lease rejection (no `--force` retry), argument starting with `origin/`. The dirty-tree eval's scenario prints `git status --porcelain` while the command uses `--untracked-files=no`; the assertion says "or equivalent", so it holds.
