# Batch 64

## explain-pr-changes (command)

### explain-pr-changes#D8-1
- severity: medium
- dimension: D8
- location: commands/explain-pr-changes.md:227
- fix: Make the filter track Markdown fences: accept up to three leading spaces and opening runs of at least three backticks or tildes, recognize the mermaid info string, and require a closing fence of the same character with sufficient length. Preserve surrounding prose and retain the explicit error for an unclosed Mermaid fence.

### explain-pr-changes#D4-1
- severity: medium
- dimension: D4
- location: commands/explain-pr-changes.md:1
- fix: Generate or update a GitHub pull request from the current branch's committed diff, with changeset triage and optional Mermaid or draw.io diagrams. Use when asked to explain PR changes, refresh a PR summary, promote a release branch, or reuse merged PR bodies and reviewers. Pushes feature branches and writes PRs; not for a read-only explanation of a diff.

### explain-pr-changes#D1-1
- severity: medium
- dimension: D1
- location: commands/explain-pr-changes.md:5
- fix: Remove the self-descriptive persona and compress the standard diff-analysis and summary-writing advice into the actual output constraints: a 150-word overview, diagram eligibility, public-contract notes, and conservative changeset triage. Preserve the non-obvious promotion, reuse, quoting, and failure-handling rules.

### explain-pr-changes#D5-1
- severity: medium
- dimension: D5
- location: commands/explain-pr-changes.md:106
- fix: Move the detailed mode-specific assembly, attachment, and reviewer procedures into skills/pr-diagrams/references/pr-workflow.md and the report template into skills/pr-diagrams/assets/pr-summary.md. Keep the command at 200 lines or fewer with its arguments, safety gates, ordered phases, and explicit conditional reads for the relevant modes.
