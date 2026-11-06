# Batch 56

## sync-branch (command)

### sync-branch#D1-1
- severity: high
- dimension: D1
- location: commands/sync-branch.md:6
- fix: Condense the familiar Git mechanics into a compact execution sequence and spend the remaining instructions on repository-specific remote conventions, branch ownership and history-rewrite edge cases.

### sync-branch#D2-1
- severity: high
- dimension: D2
- location: commands/sync-branch.md:8
- fix: Before rebasing, inspect `git log --left-right --cherry-pick --oneline origin/<target>...HEAD`, identify the feature-only patches and state the behavior that must survive. If the base was rewritten or feature patches already landed, identify the correct replay range before proceeding.

### sync-branch#D3-1
- severity: high
- dimension: D3
- location: commands/sync-branch.md:8
- fix: Add a Gotchas section explaining that rebase conflict sides are counterintuitive: ours is the onto history and theirs is the replayed feature commit. Never select --ours or --theirs solely by the label; inspect the patch intent to avoid discarding feature work.

### sync-branch#D6-1
- severity: high
- dimension: D6
- location: commands/sync-branch.md:13
- fix: Before any mutation, capture the current branch and HEAD; stop for detached HEAD, protected/base branches, dirty or unmerged worktrees, or an existing Git operation. Verify the intended PR head remote/ref and establish authorization before rewriting a shared branch. Push the saved branch explicitly rather than rediscovering it after the rebase.

### sync-branch#D7-1
- severity: high
- dimension: D7
- location: commands/evals/sync-branch.json
- fix: Add commands/evals/sync-branch.json with at least three realistic scenarios and verifiable assertions: successful synchronization, a conflict or rejected-push failure, and an edge case such as a non-main target or detached HEAD. Assert the resulting branch state, preservation of feature work and whether a push occurred.

### sync-branch#D8-1
- severity: medium
- dimension: D8
- location: commands/sync-branch.md:12
- fix: Make the conflict branch explicit: inspect and resolve each conflict, stage only resolved paths, run `git rebase --continue`, and repeat until the rebase completes. If resolution requires an uncertain semantic choice, ask the user or run `git rebase --abort` and report the blocker. Do not enter the push step while the rebase is incomplete or has failed.

### sync-branch#D4-1
- severity: medium
- dimension: D4
- location: commands/sync-branch.md:2
- fix: Rebase the current feature branch onto the latest origin/main or a supplied target, then update its PR branch with --force-with-lease. Use when a feature branch or PR is behind its base and needs updating; not for merge-based synchronization or updating local main.

## explain-changes-mental-model (command)

### explain-changes-mental-model#D1-1
- severity: high
- dimension: D1
- location: commands/explain-changes-mental-model.md:65
- fix: Collapse standard Git extraction instructions to the unique large-diff fallback and remove generic explanatory advice. Retain the report contract and source-selection semantics; add non-obvious dependency and review pitfalls grounded in real changesets instead of reteaching native diffing.

### explain-changes-mental-model#D5-1
- severity: high
- dimension: D5
- location: commands/explain-changes-mental-model.md:178
- fix: Move the worked example into a skill bundled with this command's plugin, for example skills/change-mental-model/references/examples.md, and add an explicit conditional read when a worked example is needed. Keep the command itself at 200 lines or fewer.

### explain-changes-mental-model#D7-1
- severity: high
- dimension: D7
- location: commands/evals/explain-changes-mental-model.json
- fix: Add at least three realistic scenarios with verifiable assertions: a commit or range producing correct file groups and dependency order; an invalid reference or empty diff producing a clear diagnostic without invented changes; and an edge case such as HEAD~3 resolving to a single-commit patch or custom mode waiting for pasted input.

### explain-changes-mental-model#D8-1
- severity: high
- dimension: D8
- location: commands/explain-changes-mental-model.md:21
- fix: Replace every /mental-model example with /explain-changes-mental-model for project installation, and document /command-explain-changes-mental-model:explain-changes-mental-model for this repository's plugin installation.

### explain-changes-mental-model#D8-2
- severity: high
- dimension: D8
- location: commands/explain-changes-mental-model.md:54
- fix: Make dispatch mutually exclusive: handle exact custom first, then explicit ranges, then verified branch refs, then other verified commit-ish expressions using git show. Recognize HEAD~3 and tags as commit-ish values, validate and quote arguments, and ask for a comparison base when neither main nor master exists.

### explain-changes-mental-model#D2-1
- severity: medium
- dimension: D2
- location: commands/explain-changes-mental-model.md:100
- fix: Derive review prerequisites from changed callers, data flow, schema contracts, feature flags, and test fixtures. Require a concrete reason for each dependency, merge inseparable groups, and place configuration or migrations first when they enable later behavior rather than ordering them last by category.

### explain-changes-mental-model#D3-1
- severity: medium
- dimension: D3
- location: commands/explain-changes-mental-model.md:151
- fix: Add actual gotchas with reasons: inspect historical source at the analyzed revision rather than the current working tree, which may contain later changes; distinguish patch-proven behavior from inferred author intent; and verify generated-file or formatting churn before treating it as semantically irrelevant.

### explain-changes-mental-model#D4-1
- severity: medium
- dimension: D4
- location: commands/explain-changes-mental-model.md:2
- fix: Explain Git diffs, commits, branch comparisons, revision ranges, or pasted changes as dependency-ordered logical groups with file references and a review sequence. Use when the user wants to understand a changeset, asks what to read first, or needs a conceptual walkthrough. Not for editing code or conducting a defect-focused code review.
