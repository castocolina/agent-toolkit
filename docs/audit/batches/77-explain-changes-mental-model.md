# Batch 77

## explain-changes-mental-model (command)

### explain-changes-mental-model#D8-1
- severity: medium
- dimension: D8
- location: commands/explain-changes-mental-model.md:29
- fix: Handle the branch that resolves to the base and the remote branch. If <arg> is itself the chosen base (for example `/explain-changes-mental-model main`), `main...main` is empty and the command wrongly reports 'No changes found'. In that case explain the tip commit as in step 7, or ask for a base. For a `refs/remotes/<arg>` branch, prefer the matching remote base (`origin/main`), because local `main` may be stale.

### explain-changes-mental-model#D8-1
- severity: medium
- dimension: D8
- location: commands/explain-changes-mental-model.md:32
- fix: For non-merge commits and tags, obtain patch-only output with `git show --format= --no-color "<arg>^{commit}"`, fetching metadata separately if needed. Preserve the first-parent diff for merges, and apply the no-changes stopping condition to patch content rather than metadata-bearing stdout.

### explain-changes-mental-model#D1-1
- severity: low
- dimension: D1
- location: commands/explain-changes-mental-model.md:8
- fix: Delete the invocation sentence. The harness already handles slash-command discovery and naming, and the model never needs this to do the task. Keep the usage block only if it shows how arguments are classified.

### explain-changes-mental-model#D1-2
- severity: low
- dimension: D1
- location: commands/explain-changes-mental-model.md:10
- fix: Trim the usage block to the cases section 1 does not already make clear (`HEAD~3` as one commit, `#123`). Every other example repeats a numbered rule in section 1.

### explain-changes-mental-model#D2-1
- severity: medium
- dimension: D2
- location: commands/explain-changes-mental-model.md:36
- fix: Add a self-check before the output step: 'Before writing the report, compare the groups against `git diff --stat` (or the patch's file list). Every changed file appears in exactly one group, and every Depends on names a group that comes earlier in the review order. Fix the grouping and check again until both hold.' This turns the Process pattern into a checkpointed workflow.

### explain-changes-mental-model#D3-1
- severity: medium
- dimension: D3
- location: commands/explain-changes-mental-model.md:26
- fix: Add a gotcha: '`git diff A..B` is the same as `git diff A B`, not log-range semantics. It includes changes made on A since the branches split, and those appear as reversed hunks. If the user means the changes on the branch only, use `A...B` and say which form you used.' Models routinely assume `..` in diff means what it means in `git log`.

### explain-changes-mental-model#D4-1
- severity: low
- dimension: D4
- location: commands/explain-changes-mental-model.md:3
- fix: argument-hint: [commit|branch|range|#PR|custom] (the hint is shown at invocation; without it users cannot see that the command supports the PR path in step 4)

### explain-changes-mental-model#D1-1
- severity: medium
- dimension: D1
- location: commands/explain-changes-mental-model.md:45
- fix: Condense the generic summary, concepts and explanatory fields into a short output instruction. Retain the distinctive requirements: dependency-ordered groups, file references, concrete dependency evidence, enables relationships, review sequence and the single-group exception.
