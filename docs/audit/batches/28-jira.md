# Batch 28

## jira (skill)

### jira#D8-1
- severity: high
- dimension: D8
- location: skills/jira/references/commands.md:231
- fix: Use the backend's actual epic-association or parent-field operation, checking the installed CLI interface and project metadata. Reserve issue-link commands for discovered configured link types and distinguish links from hierarchy.

### jira#D8-2
- severity: medium
- dimension: D8
- location: skills/jira/SKILL.md:36
- fix: Document supported non-interactive commands or authorized REST requests for transition and create-field discovery. If the selected CLI cannot provide that information, explicitly route to an authorized MCP/REST backend or report the blocker instead of guessing or opening a prompt.

### jira#D7-1
- severity: medium
- dimension: D7
- location: skills/jira/evals/evals.json:7
- fix: Add an approved follow-up case with backend response fixtures and assertions for required-field discovery, the exact approved mutation, and read-back verification. Include a batch partial-failure case asserting that subsequent mutations stop.

### jira#D8-1
- severity: low
- dimension: D8
- location: skills/jira/SKILL.md:14
- fix: Add a tie-break rule for when both backends exist and a capability-based choice (e.g., issue linking needs MCP/REST since the CLI table omits it), so backend selection is deterministic

### jira#D1-1
- severity: medium
- dimension: D1
- location: skills/jira/references/mcp.md:154
- fix: Trim elementary JQL explanations and duplicate setup guidance. Keep backend-specific schemas, extension limitations, required-field discovery, account-ID handling, and transition/link pitfalls.

### jira#D1-1
- severity: medium
- dimension: D1
- location: skills/jira/references/mcp.md:149
- fix: Cut the standard JQL syntax tables (operators, functions, relative dates) the model already knows; keep only the non-obvious parts (ScriptRunner limits, 'Epic Link' quoting, link-creation gap)

### jira#D2-1
- severity: low
- dimension: D2
- location: skills/jira/SKILL.md:34
- fix: Merge the checklist into the operation paths as one ordered procedure and say why each gate exists (one-way transitions, opaque --no-input failures) instead of repeating fetch-approve-apply

### jira#D3-1
- severity: low
- dimension: D3
- location: skills/jira/SKILL.md:34
- fix: Extract a Gotchas list naming each trap and its consequence (no general undo, display names not valid assignee IDs, transition IDs differ per project) in one place

### jira#D6-1
- severity: low
- dimension: D6
- location: skills/jira/SKILL.md:32
- fix: Give the rationale for the batch cap (reviewability of the change list, blast radius on partial failure) or make it a default the user can raise
