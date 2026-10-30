# Write the pull request body

Write the body of the automated skill-audit pull request as one Markdown document on stdout. You have no shell and no network access; rely only on the evidence below. Follow the section structure of `commands/explain-pr-changes.md`:

- Start with a `# PR Summary: <title>` line, using the decision's own title.
- A `## 📜 High-Level Summary` section: one concise paragraph (max 150 words).
- A `## 📊 Architectural Impact & Visualizations` section with exactly one fenced `mermaid` code block, preceded by a one-sentence explanation of what the diagram illustrates. When the diagram format below is `none`, omit this section entirely.
- A `## ⚙️ Detailed Changeset Breakdown` section grouping the diff into logical changesets: a meaningful title per changeset, the affected files, a bulleted summary, and a triage status of `NEEDS_REVIEW` or `APPROVED`.

Print the body only: no conversation, no extra fences around the document, no tool use, no file writes.

## Decision evidence

Title: {{TITLE}}
Type: {{TYPE}}; targets: {{TARGETS}}.

Rationale:

{{RATIONALE}}

## Diff stat

{{DIFF_STAT}}

## Diff (trimmed)

{{DIFF}}

## Diagram format

{{DIAGRAMS}}
