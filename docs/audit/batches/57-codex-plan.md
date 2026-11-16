# Batch 57

## codex-plan (command)

### codex-plan#D1-1
- severity: high
- dimension: D1
- location: commands/codex-plan.md:35
- fix: Remove the generic question banks and basic request-analysis guidance. Retain only questions driven by non-obvious Codex handoff constraints or repository-specific decisions.

### codex-plan#D5-1
- severity: high
- dimension: D5
- location: commands/codex-plan.md:149
- fix: Move the worked example and plan template into a skill bundled by the command's plugin, for example skills/codex-planning/references/plan-template.md. Add an explicit read via ${CLAUDE_PLUGIN_ROOT}/skills/codex-planning/references/plan-template.md when composing the plan prompt, and keep the command itself under 200 lines.

### codex-plan#D7-1
- severity: high
- dimension: D7
- location: commands/evals/codex-plan.json
- fix: Add commands/evals/codex-plan.json with at least three realistic scenarios: an ambiguous planning request through successful manual handoff, a prompt-file write failure, and an edge case such as an existing output file. Assert observable behavior including prompt contents, verified context paths, model and reasoning settings, no automatic Codex execution, and explicit failure or collision handling.

### codex-plan#D8-1
- severity: medium
- dimension: D8
- location: commands/codex-plan.md:13
- fix: Replace the opening's fourth item with 'Save the prompt for manual Codex execution, show the command, and wait for the user to return the plan.' State the manual-only boundary once consistently throughout the workflow.

### codex-plan#D8-2
- severity: medium
- dimension: D8
- location: commands/codex-plan.md:180
- fix: Add a Files to Read for Context section to the worked example using paths discovered during context gathering. Clearly mark illustrative paths and require their replacement with verified repository paths before saving the prompt.

### codex-plan#D8-3
- severity: medium
- dimension: D8
- location: commands/codex-plan.md:127
- fix: After writing, verify that the prompt file was saved before presenting the manual command. If writing fails, report the concrete error, provide the prompt inline or ask for a writable destination, and do not claim the handoff file is ready.

### codex-plan#D2-1
- severity: medium
- dimension: D2
- location: commands/codex-plan.md:123
- fix: Add a handoff readiness gate: distinguish confirmed requirements, blocking decisions and nonblocking assumptions; resolve blocking decisions before handoff, encode remaining assumptions explicitly, and check that the proposed tasks and acceptance criteria cover the confirmed requirements.

### codex-plan#D3-1
- severity: medium
- dimension: D3
- location: commands/codex-plan.md:316
- fix: Add concise, reasoned gotchas: --output-last-message saves Codex's final reply rather than proving codex-plan.md exists; fixed output filenames can collide with previous runs, so do not overwrite them without approval; transfer example environment keys rather than live secret values into the handoff prompt.

### codex-plan#D4-1
- severity: medium
- dimension: D4
- location: commands/codex-plan.md:2
- fix: Prepare prompt_to_codex.md for a user-run gpt-5.2-codex implementation plan with high reasoning. Use when planning a feature, API, authentication change, migration or testing strategy, including underspecified requests needing clarification. Gather repository context and provide the manual command that writes codex-plan.md. Not for implementing changes or executing Codex automatically.

### codex-plan#D6-1
- severity: medium
- dimension: D6
- location: commands/codex-plan.md:33
- fix: Ask only unanswered questions that materially affect the plan. Treat three to six questions as an optional upper range, not a minimum; when the request and repository provide sufficient information, proceed and state any bounded assumptions.
