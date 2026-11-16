# Batch 76

## sync-branch (command)

### sync-branch#D8-1
- severity: medium
- dimension: D8
- location: commands/sync-branch.md:19
- fix: Finish the lease-rejected branch: 'Report that the local branch is already rebased and was not pushed. Give the pre-rebase tip `$orig` and the recovery command `git reset --hard $orig`. Then list the new remote commits with `git fetch origin && git log --oneline "$branch..origin/$branch"`.' The agent should not leave the user with no next step.

### sync-branch#D8-1
- severity: high
- dimension: D8
- location: commands/sync-branch.md:17
- fix: Compute the reflog fork point even when `old_base` is set, before selecting normal rebase. When it is non-empty and differs from the ordinary merge base, use `git rebase --onto "origin/$target" "$fork" "$branch"`. Retain the pre-fetch-base fallback for rewrites detected during this fetch; stop for clarification if a known rewrite has no trustworthy cutoff.

### sync-branch#D1-1
- severity: low
- dimension: D1
- location: commands/sync-branch.md:25
- fix: Cut this to one clause or delete it. The model already knows how shell quoting works, and step 5 already quotes "$branch".

### sync-branch#D2-1
- severity: medium
- dimension: D2
- location: commands/sync-branch.md:16
- fix: Add one decision check before any mutation: 'Before rebasing, ask whether anyone else pushes to this branch. If `git log --format=%ae "origin/$target..$remote"` shows authors other than the user, stop.' The description excludes shared branches, but the body never tells the agent how to spot one. Right now it only notices a shared branch when the remote has diverged.

### sync-branch#D3-1
- severity: low
- dimension: D3
- location: commands/sync-branch.md:21
- fix: Replace the quoting item with a gotcha from real use, for example: 'Stacked branches: rebasing a branch that other local branches build on leaves them on the old SHAs. Pass `--update-refs` (git 2.38+) or tell the user which dependent branches need rebasing.'
