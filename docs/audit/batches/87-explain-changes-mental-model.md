# Batch 87

## explain-changes-mental-model (command)

### explain-changes-mental-model#D8-1
- severity: medium
- dimension: D8
- location: commands/explain-changes-mental-model.md:43
- fix: Add the no-commits branch that rule 1 already handles: 'with no commits yet, use the union of `git diff --cached --name-only` and `git diff --name-only` plus the untracked list'. Without it, `git diff HEAD --name-only` fails and the manifest check cannot pass.

### explain-changes-mental-model#D8-2
- severity: medium
- dimension: D8
- location: commands/explain-changes-mental-model.md:43
- fix: Mirror rule 7's merge-commit branch: 'for a merge commit, use `git diff --name-only "<arg>^1" "<arg>"`'. As written, `git show` gives a combined listing that does not match the first-parent diff used for grouping, so the check of exactly one group per file fails.

### explain-changes-mental-model#D8-3
- severity: medium
- dimension: D8
- location: commands/explain-changes-mental-model.md:30
- fix: Measure size before reading, then use a threshold that matches the truncation gotcha: 'First run `--shortstat` on the same source. If more than about 800 changed lines or 25K characters, switch to this procedure.' A 5000-line diff is well beyond the 10-30K-character truncation limit, and its size is only known after the full output has been read. Also change 'as in step 2' to 'as in section 2' to remove the ambiguous reference to sub-step 2.

### explain-changes-mental-model#D1-1
- severity: low
- dimension: D1
- location: commands/explain-changes-mental-model.md:41
- fix: Delete this generic ordering advice, which the model already applies. Keep the non-obvious rule before it: configuration and migrations go first when later behaviour needs them.

### explain-changes-mental-model#D2-1
- severity: low
- dimension: D2
- location: commands/explain-changes-mental-model.md:39
- fix: Give a concrete test for merging, for example: 'Before splitting two groups, ask: can a reviewer judge group B's hunks without reading group A's? If B only renames or forwards A's symbols, merge them.'
