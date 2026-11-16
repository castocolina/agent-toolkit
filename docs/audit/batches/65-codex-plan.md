# Batch 65

## codex-plan (command)

### codex-plan#D8-1
- severity: low
- dimension: D8
- location: commands/codex-plan.md:15
- fix: Resolve the malformed branch: if `--model` has no id after it, or the next token looks like part of the topic, ask for the model id with AskUserQuestion (or drop the flag and use the default). Never pass `-m` with an empty or guessed value.

### codex-plan#D8-1
- severity: medium
- dimension: D8
- location: commands/codex-plan.md:19
- fix: Scope the restriction explicitly: "In Files to Read for Context, list only paths verified with ls/Read. Output filenames and proposed new implementation paths may be named, but label them as planned/new rather than existing context files."

### codex-plan#D1-1
- severity: low
- dimension: D1
- location: commands/codex-plan.md:39
- fix: Keep the required section and per-task field list. Cut the general advice about small tasks, which the model already follows. The coverage check is already in the post-plan review on line 33, so drop it here.

### codex-plan#D2-1
- severity: medium
- dimension: D2
- location: commands/codex-plan.md:19
- fix: Add a short selection rule for step 1, for example: start with the manifest (package.json, pyproject.toml), the schema or models, the entry points and middleware the topic touches, and .env.example. Stop after about 10 files. Prefer files a task would edit over files that only document.

### codex-plan#D3-1
- severity: medium
- dimension: D3
- location: commands/codex-plan.md:28
- fix: Add a gotcha: `-s workspace-write` gives Codex write access to the whole workspace, so the planning-only instruction is the only guard against source edits. When the plan arrives, ask the user for `git status --short` (or check it yourself) and flag any changed file other than the chosen plan file before reviewing the plan.

### codex-plan#D4-1
- severity: low
- dimension: D4
- location: commands/codex-plan.md:2
- fix: Prepare prompt_to_codex.md so the user can run the Codex CLI themselves and get an implementation plan in codex-plan.md. Use when planning a feature, API, auth change, migration, refactor or test strategy, or when the user wants a plan handed off to Codex or another agent, even without the word "Codex", including underspecified requests. Gathers repo context, asks only blocking questions, shows the manual `codex exec` command. Not for implementing changes; never runs Codex.

### codex-plan#D3-1
- severity: medium
- dimension: D3
- location: commands/codex-plan.md:57
- fix: Replace this gotcha with: "A planning run reads context and writes only the plan; do not install packages, call external services or run tests. Network access depends on Codex configuration, so do not rely on the sandbox to block execution."

### codex-plan#D1-1
- severity: low
- dimension: D1
- location: commands/codex-plan.md:55
- fix: Remove this repeated warning while retaining step 3's explicit overwrite confirmation and paired numeric-suffix selection.
