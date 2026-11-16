---
description: Use when adding a new decision lens to the reducing-entropy references; it gives the file template and the kinds of content a lens must not hold.
---

# Adding a reference mindset

Add a reference only for a distinct decision lens that changes a real delete or consolidate judgment (README, "Adding a reference mindset"). Name the file by the concept, then link it from the step-3b lens list in `SKILL.md` with its trigger.

## File template

```markdown
---
description: Use when <the delete or consolidate decision this lens changes>.
---

# Concept name

<One or two sentences: the central idea, credited to its source when it is a quote.>

- <A question to ask of a candidate, with the answer that favors deletion.>
- <A second question, or a check to apply to the proposed change.>
- <The counter-case: when the lens stops applying and the code stays.>

## External References

- [Title](url) - author and what it explains
```

Keep it to a few lines. List only primary sources (talks, papers, books that originated or best explain the idea) and verify each link before adding it.

## What not to add

- **Technology-specific advice**: it belongs in project docs or in a skill for that technology. Examples to refuse: "React components should...", "In Rust, prefer...".
- **Process or workflow rules**: they belong in skills, not lenses. Examples: "Always run tests before...", "Use TDD when...".
- **Vague platitudes**: with no actionable insight, skip it. Examples: "Write clean code", "Think before you code".
- **Anything that needs context to hold**: a lens must apply to any codebase. Examples: "In microservices architectures...", "When working with legacy code...".
