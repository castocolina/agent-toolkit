# Batch 30

## commit-work (skill)

### commit-work#D7-1
- severity: medium
- dimension: D7
- location: skills/commit-work/evals/evals.json:6
- fix: Add disposable-repository or explicit state fixtures with pre-existing unrelated staged content, mixed intended and unrelated hunks, and a hook that changes the index. Assert that unrelated state is preserved and that retries require a fresh index review.

### commit-work#D8-1
- severity: high
- dimension: D8
- location: skills/commit-work/SKILL.md:14
- fix: Route by requested intent before the workflow: message-only returns a proposed message without mutation; review-only reports findings without mutation; staging-only stops after index review; only an authorized commit request proceeds to git commit.

### commit-work#D7-1
- severity: low
- dimension: D7
- location: skills/commit-work/evals/evals.json
- fix: Add evals/files fixtures (a status/diff snapshot with mixed staged and unstaged content) so selective-staging assertions grade real command sequences.

### commit-work#D8-1
- severity: medium
- dimension: D8
- location: skills/commit-work/references/commit-message-template.md:3
- fix: SKILL.md step 6 never states the shape; add the minimal template there (type(scope)!: subject, blank line, body, footer) or move the shape into this reference so the cross-reference resolves.

### commit-work#D1-1
- severity: medium
- dimension: D1
- location: skills/commit-work/SKILL.md:17
- fix: Compress standard Git and Conventional Commit instructions. Prioritize the non-obvious constraints: user-owned index content, non-interactive mixed-hunk staging, index-versus-worktree verification, hook mutations, and stopping at the approved change set.

### commit-work#D6-1
- severity: medium
- dimension: D6
- location: skills/commit-work/SKILL.md:25
- fix: Specify a safe verification branch when index and working tree differ: export the index tree to a disposable directory, run applicable checks there without changing the user's index or worktree, or stop and explicitly report that the staged version could not be verified. Do not silently stash or reset user changes.

### commit-work#D1-1
- severity: low
- dimension: D1
- location: skills/commit-work/SKILL.md:15
- fix: Ground the generic parts: check staged paths against .gitignore and the build outputs the CI config produces; keep lockfile-churn and scope-accuracy, the checks the model actually skips.

### commit-work#D2-1
- severity: low
- dimension: D2
- location: skills/commit-work/SKILL.md:12
- fix: Split into 1a inspect, 1b ownership rule, 1c stop rule; one 60-word step hides the stop condition an agent must not miss.

### commit-work#D3-1
- severity: low
- dimension: D3
- location: skills/commit-work/SKILL.md:24
- fix: Extend to the rebase case: during a rebase git status shows 'rebasing' and a commit silently continues it; check status in step 1, not just for conflict markers.

### commit-work#D6-1
- severity: medium
- dimension: D6
- location: skills/commit-work/SKILL.md:12
- fix: Name the default tactic after authorization (e.g., stash unrelated staged content with git stash push --keep-index, or build the commit from a temporary index); 'an index-isolation strategy' leaves the fragile step to invention.
