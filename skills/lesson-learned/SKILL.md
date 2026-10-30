---
name: lesson-learned
description: "Use when users ask what they learned, want an engineering takeaway, or reflect on recent commits, a branch diff, a specific commit, or staged/unstaged changes—even without naming Git or a principle. Ground one lesson in concrete changes and a next-time action. Not for generic engineering tutorials, ordinary bug reviews, or implementing refactors."
---

# Lesson Learned

Extract one evidence-backed engineering lesson from actual code changes. Show what the changes demonstrate, not a generic lecture.

## Prepare

Read [the diff-signal lookup](references/se-principles.md). Read [anti-patterns](references/anti-patterns.md) when 10+ files changed (check change amplification) or a changed function exceeds 50 lines (check long methods).

## Choose the evidence scope

| Request | Evidence |
|---|---|
| Feature branch (default off base branch) | Resolve base branch from repo metadata/remotes; use `<base>..HEAD` for commits absent from base and `<base>...HEAD` for diff from merge-base. Ask if base is ambiguous. |
| Last N commits | Up to N available commits and their diff; default N=5. |
| Specific commit | `git show <sha>` |
| Working changes | `git diff` and `git diff --cached` |

Two-dot log and three-dot diff can disagree after partial merges; choose deliberately and state the comparison. On base branch use the last 5 available commits. If there are no commits, analyze working/staged changes; if there is no history or diff, explain that evidence is unavailable and stop rather than forcing a lesson.

Start with the scoped log and diff. For a diff over 500 lines, inspect `git diff --stat` then representative high-signal hunks. Read changed files first. Read an unchanged caller, contract, or test only when needed to substantiate a claim, and state why you expanded scope.

## Select and verify a lesson

1. Identify candidate causal changes.
2. Rank by observable behavioral consequence and evidence strength; favor a demonstrated trade-off over a superficial principle match.
3. Choose one lesson with a defensible counterfactual: what would likely have happened without the change?
4. Verify the consequence in code/tests. A before/after improvement needs evidence from both states or a test; otherwise describe only what changed.
5. Map the signal to a named principle using the reference. If none fits, don't force a label.

Commit messages express intent, not proof: code and tests override contradictory messages. Extraction alone does not prove modularity; inspect the dependency contract. File count alone does not prove shotgun surgery; generated changes and mechanical renames produce the same signal.

## Present

```markdown
## Lesson: [Principle]

**What changed:** [Concrete files/commits and behavior, with a short code or test reference]
**Why it matters:** [Observable consequence and evidence-backed counterfactual]
**Next time:** [One actionable practice]
```

Default to one lesson. Add more only for genuinely independent concerns (at most two additional). Keep it reflective and specific; if changes are trivial or evidence is thin, say so rather than inventing insight. Avoid generic principle lists and unsupported improvement claims.

## Evidence rules

- NEVER let a commit message override contradictory code or tests; intent is not behavioral evidence.
- NEVER infer improved modularity from extraction alone; shared internals can increase coupling.
- NEVER diagnose shotgun surgery solely from file count; mechanical/generated edits are false positives.
- Don't turn reflection into a bug review or refactor proposal. State a next-time action, not an implementation plan.
