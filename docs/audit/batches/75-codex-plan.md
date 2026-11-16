# Batch 75

## codex-plan (command)

### codex-plan#D8-1
- severity: medium
- dimension: D8
- location: commands/codex-plan.md:25
- fix: Shell variables and functions do not survive between separate Bash tool calls, so the later `snap > "$B/after"` fails. Tell the agent to print and record the literal mktemp path, and to define `snap` again in the same command as the comparison (or include the full one-liner in step 6), so the diff branch actually runs.

### codex-plan#D8-1
- severity: medium
- dimension: D8
- location: commands/codex-plan.md:41
- fix: Record the baseline directory's absolute path in the handoff message and make the follow-up invocation self-contained: redefine snap, assign the recorded directory explicitly, and run from the recorded working directory.

### codex-plan#D8-2
- severity: high
- dimension: D8
- location: commands/codex-plan.md:28
- fix: Enable pipeline failure propagation, keep diagnostics separate from snapshot data, and check snapshot capture explicitly before accepting either baseline or comparison. If capture fails, report verification as unavailable rather than treating matching error text as unchanged files.

### codex-plan#D8-3
- severity: medium
- dimension: D8
- location: commands/codex-plan.md:28
- fix: State that the Git-based comparison covers only tracked and non-ignored untracked files, explicitly identify ignored paths as unverified, and include relevant ignored configuration or data paths when broader workspace-change verification is required.

### codex-plan#D1-1
- severity: low
- dimension: D1
- location: commands/codex-plan.md:19
- fix: Remove the generic list of files to read, since the model already explores a repo this way. Keep only the non-obvious rules: stop at about 10 files, prefer files a task would edit, and list only paths verified to exist.

### codex-plan#D2-1
- severity: low
- dimension: D2
- location: commands/codex-plan.md:41
- fix: Move the review after the handoff into its own numbered step 7, 'Review the returned plan': (a) diff the snapshots, (b) map each requirement to a task, (c) list the gaps. Right now it sits in one prose paragraph under step 6, so the Process pattern has no visible checkpoint for it.

### codex-plan#D3-1
- severity: low
- dimension: D3
- location: commands/codex-plan.md:34
- fix: Add a gotcha: 'Never add `--full-auto` or `-s danger-full-access`. They widen the sandbox or skip approvals, and the planning-only instruction is the only guard against source edits.'

### codex-plan#D6-1
- severity: low
- dimension: D6
- location: commands/codex-plan.md:15
- fix: Pick one default: 'ask for the id with AskUserQuestion; drop the flag only if the user declines to give one'. This replaces two equal options with a default and an escape hatch.
