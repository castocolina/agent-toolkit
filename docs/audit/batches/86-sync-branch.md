# Batch 86

## sync-branch (command)

### sync-branch#D7-1
- severity: low
- dimension: D7
- location: commands/evals/sync-branch.json
- fix: Allow `"$branch"`, the form the command itself prescribes in step 5, in this assertion. Also add scenarios for a rejected lease (no --force retry, report $orig) and for a remote that is ahead (stop and list the commits).

### sync-branch#D8-1
- severity: medium
- dimension: D8
- location: commands/sync-branch.md:19
- fix: State the question and what each answer does. For example, ask "fork-point would drop N commits; use the plain merge-base rebase instead, or stop?" On use, run `git rebase "origin/$target"`. On anything else, stop and change nothing.

### sync-branch#D8-2
- severity: medium
- dimension: D8
- location: commands/sync-branch.md:6
- fix: Add an edge case for fork-based PRs. If an `upstream` remote exists and the PR base lives there, fetch and rebase onto `upstream/$target` instead of `origin/$target`, or stop and ask. As written, a stale fork main is used without any warning. Also reject an argument that already starts with `origin/`.

### sync-branch#D1-1
- severity: low
- dimension: D1
- location: commands/sync-branch.md:27
- fix: Delete this gotcha. The model already knows how shell quoting works, and the steps already quote "$branch" everywhere.

### sync-branch#D2-1
- severity: medium
- dimension: D2
- location: commands/sync-branch.md:19
- fix: Split step 3 into ordered sub-steps: (a) compute fork and the plain merge-base; (b) compare the commit counts of the two ranges and stop if the fork-point range is shorter; (c) only then choose one of the three rebase forms from a short decision list. The safety check currently comes after the instruction it guards.

### sync-branch#D3-1
- severity: low
- dimension: D3
- location: commands/sync-branch.md:19
- fix: Give the reason for each NEVER: local main is often stale, so the rebase goes onto an old base. `git pull` merges or rebases the wrong upstream (the feature branch's own remote). `git merge` adds a merge commit that the PR's linear history rejects.
