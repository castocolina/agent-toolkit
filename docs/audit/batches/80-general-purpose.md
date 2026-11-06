# Batch 80

## general-purpose (agent)

### general-purpose#D8-1
- severity: medium
- dimension: D8
- location: agents/general-purpose.md:14
- fix: Move gate discovery ahead of the baseline. Find the gate commands (AGENTS.md, CLAUDE.md, the Makefile, else the toolchain's standard test runner) in step 2 and run them there to record pre-existing failures. Step 5 only finds the gates, so the step 2 baseline cannot be taken as written. Also say whether 'else stop and report it' stops only that requirement or the whole task.

### general-purpose#D1-1
- severity: low
- dimension: D1
- location: agents/general-purpose.md:13
- fix: Shorten step 1 to its non-obvious checkpoint (one owner per requirement, no two parallel workers share a file, each requirement has an acceptance check). Drop the general planning wording, which the model and the harness's todo and plan features already cover.

### general-purpose#D2-1
- severity: low
- dimension: D2
- location: agents/general-purpose.md:15
- fix: Add a short 'before running workers in parallel, ask:' heuristic. Parallelize only when the file sets are disjoint and each worker has its own acceptance check. Otherwise run workers one after another. This adds a thinking frame for the main serial-or-parallel choice.

### general-purpose#D3-1
- severity: low
- dimension: D3
- location: agents/general-purpose.md:29
- fix: Replace this widely known point with an environment-specific gotcha learned in practice, for example that a specialist run with isolation: worktree commits on a different branch, so its diff must be merged or cherry-picked before the gates run in your worktree.
