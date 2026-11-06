---
description: Explain a git diff, commit, branch, range, PR or pasted patch as dependency-ordered logical groups with file references and a review sequence. Use when the user wants to understand, onboard onto or walk through a changeset, asks what changed or what to read first, even without saying 'mental model'. Not for editing code, a defect-focused code review, or the PR-workflow command explain-pr-changes.
argument-hint: [commit|branch|range|#PR|custom]
---

# Mental Model Builder

Present changes as a mental model: logical groups ordered by dependency so they can be understood incrementally.

```bash
/explain-changes-mental-model                 # uncommitted changes
/explain-changes-mental-model HEAD~3          # one commit, not the last three
/explain-changes-mental-model feature/x       # branch vs main
/explain-changes-mental-model #123            # PR number or URL
/explain-changes-mental-model custom          # user pastes the diff next
```

## 1. Pick the source

Check in this order; the first match wins. Quote the argument in every command.

1. No argument: `git diff HEAD --no-color`, plus each untracked file from `git ls-files -z --others --exclude-standard` via `git diff --no-index --no-color -- /dev/null "<file>"` (exit 1 there means "differs", not failure). With no commits yet (`git rev-parse --verify --quiet HEAD` fails) there is no `HEAD` diff: collect both `git diff --cached --no-color` and `git diff --no-color`, then explain the final worktree state (a staged file edited afterwards appears in both). Run the untracked-file step in this case too. All sources empty: report "No uncommitted changes to analyze" and stop.
2. Exactly `custom`: run no git command; reply "Please paste or describe the changes you want me to analyze in your next message." and wait. If the user describes changes instead of pasting a patch, say the report rests on the description, skip the size and manifest checks, and mark every group unverified.
3. Contains `..` (covers `...`): `git diff "<arg>" --no-color`. `A..B` here equals `git diff A B`, not `git log` semantics: it also shows changes made on `A` since the split, as reversed hunks. If the user means only the branch's changes, use `A...B`; say which form you used. On a non-zero exit (for example `fatal: ambiguous argument` for `main..typo`) report stderr, suggest `git branch -a`, and stop.
4. A PR number (`#123`) or PR URL: `gh pr diff "<pr>" --color=never`, without the `#`. If `gh` is missing, unauthenticated or fails, ask the user to paste the patch and continue as `custom`.
5. Otherwise verify first: `git rev-parse --verify "<arg>^{commit}"`. On failure report its stderr, suggest `git branch -a`, and stop. Never invent changes.
6. Verified and it is a branch (`git show-ref --verify --quiet "refs/heads/<arg>"` or `refs/remotes/<arg>`): base is the first that exists of `main`, `master`, `origin/main`, `origin/master` (for a `refs/remotes` argument try the `origin/` ones first, since local `main` may be stale), else ask the user for a base; then `git diff "<base>...<arg>" --no-color`. If `<arg>` is the base itself or its remote twin (`main`, `origin/main`), that diff is empty: explain the tip commit as in rule 7 instead.
7. Verified, not a branch (hash, `HEAD~3`, tag): `git show --format= --no-color "<arg>^{commit}"`, a patch-only single-commit diff (the `^{commit}` also peels tags). If `git rev-list --parents -n1 "<arg>"` lists more than one parent (a merge commit), `git show` prints an empty combined diff: use `git diff "<arg>^1" "<arg>" --no-color` instead.

Check each command's exit status first (stop on failure with its stderr, e.g. a branch with no merge base); only a successful empty output is an empty diff: report "No changes found for the specified source" and stop. Measure size before reading: run `--shortstat` on the same source (no argument: add the untracked files' lines, `git ls-files -o --exclude-standard -z | xargs -0 -r wc -l`, since `--shortstat` omits them; for a PR, `gh pr diff "<pr>" --color=never | wc -l`; for `custom`, judge the pasted patch). Above roughly 800 changed lines or 30 files, which is where the truncation gotcha below starts to bite, switch to this procedure:

1. Run `--stat` on the same source as above and cluster the paths into candidate groups. No `--stat` for the source (a PR, a pasted `custom` patch): use `gh pr diff "<pr>" --name-only` or the patch's `diff --git` headers, and read one file's hunks at a time.
2. Read the contract and schema files' diffs first (types, schemas, migrations, public APIs) to fix the dependency order.
3. Per group, read the per-file diffs, then build the groups as in section 2. Git sources: same command plus `-- <path>`. PR (`gh pr diff` takes no pathspec): save the full output once, `gh pr diff "<pr>" --color=never > "$(mktemp)"`, and read it in sections by file; `custom`: split the pasted text at `diff --git` headers. No complete patch obtainable: ask the user for it, or use step 4.
4. If the diff is still too large to read, output the group list with file counts, mark it provisional, and offer a deep-dive per group.

## 2. Build the groups

Group files by purpose (not by directory), one group per reviewable idea. Put mechanical-only files (renames, moves, signature-only call-site updates) in their own group so the reviewer can skim them; a file mixing mechanical and behavioural hunks goes once into its behavioural group, with the mechanical hunks noted there; mark groups with no import, caller or contract link as independent rather than inventing an order. For each group note what it depends on and what depends on it, from real evidence in the patch: imports, callers, schema or type contracts, feature flags, test fixtures. Require a concrete reason for every dependency; merge groups that cannot be understood apart. When the direction is unclear, ask: if a refactor and a feature change the same call site, which does a reviewer need first to understand the other; which group's tests fail if the other group is reverted?

Configuration or migrations go first when later behavior needs them, not last by category.

Before writing the report, compare the groups with the selected patch's file list (the manifest, built from the same source: no argument, `git diff HEAD --name-only` plus the untracked list from step 1 (`--stat` omits untracked files), or with no commits yet the union of `git diff --cached --name-only`, `git diff --name-only` and the untracked list; commit, `git show --name-only --format= "<arg>^{commit}"` (merge commit: `git diff --name-only "<arg>^1" "<arg>"`); range or branch, `git diff --name-only` with the same range or `<base>...<arg>`; PR, `gh pr diff "<pr>" --name-only`; `custom`, the `diff --git` headers of the pasted patch): every changed file is in exactly one group and every Depends on names an earlier group. Fix the grouping and recheck until both hold.

## 3. Output

```markdown
## Mental Model: [what these changes accomplish]

### Summary
[2-3 sentences: goal and approach; add key concepts only if a group needs them]

### Change Groups (in review order)
#### 1. [Group] - [Purpose]
**Files:** `a.ts`, `b.ts`
**Key changes:** [what and why]
**Depends on:** [group and concrete reason, or Nothing]
**Enables:** [groups]

### Review Sequence
1. **[Group]** - start here because [reason]

### Gotchas and Non-Obvious Details
- [tricky parts, implicit assumptions, things that look wrong but are intentional]
```

A single-group change keeps only the summary, the one group and its gotchas.

## Gotchas

- Tool output is truncated beyond roughly 10-30K characters without warning. Never group from a diff you did not see in full: page with `--stat` on the same source as step 1 (for example `git diff --stat "<base>...<arg>"` or `git show --stat --format= "<arg>^{commit}"`), then read per-file diffs from that source (Git: `-- <path>`; PR or `custom`: sections of the saved patch, see section 1).
- NEVER run `git checkout`, `git switch`, `gh pr checkout`, `git stash` or `git fetch` to inspect a source: they change the user's working state and can hide the uncommitted changes this command explains by default. Use `git show <rev>:<path>` and `gh pr diff`.
- Read historical source with `git show <rev>:<path>`, not the working tree: it may contain later changes that the analyzed revision lacks.
- Hunk headers `@@ -a,b +c,d @@`: cite new code by the `+c` post-image lines, not working-tree lines. Binary files, submodule bumps and mode-only changes show little diff text but can be the real change; give them their own group.
- State only what the patch proves. Mark author intent that you infer as inferred; the diff does not show why.
- Check generated files and formatting churn (lockfiles, snapshots, reformatting) before dismissing them as irrelevant: they can hide a real change. Skip an import reorder only after checking it keeps side-effect and initialization order; explain one that changes it.
