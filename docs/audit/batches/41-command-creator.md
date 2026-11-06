# Batch 41

## command-creator (skill)

### command-creator#D7-1
- severity: low
- dimension: D7
- location: skills/command-creator/evals/evals.json:7
- fix: Replace the vague either-or with one observable outcome: "Writes `.claude/commands/fix-ci.md` with a description, no argument-hint, a baseline check, a max of 5 attempts, a stuck rule and SUCCESS/STUCK reports." Also add a should-trigger query that hides the domain, for example a buried multi-step chain.

### command-creator#D8-1
- severity: medium
- dimension: D8
- location: skills/command-creator/SKILL.md:108
- fix: Make the example pass its own checklist, or narrow the checklist item to: "...after `--` or `--end-of-options` unless a strict pattern such as `^[0-9]+\.[0-9]+\.[0-9]+$` was already validated, which rules out a leading `-`". Then an agent walking step 6 does not reject the canonical example.

### command-creator#D8-1
- severity: high
- dimension: D8
- location: skills/command-creator/SKILL.md:63
- fix: Escape the literal dollar signs used to document placeholders in this skill's SKILL.md, using the backslash escaping described on line 67. Preserve unescaped placeholders in the generated command files. Verify that activating command-creator with a sentinel argument leaves its instructional placeholder names intact.

### command-creator#D8-2
- severity: high
- dimension: D8
- location: skills/command-creator/SKILL.md:104
- fix: Require a successful fetch of origin's main branch, then compare HEAD directly with the fetched commit. For example, run `git fetch origin refs/heads/main`, stop on failure, and require `git rev-parse HEAD` to equal `git rev-parse --verify FETCH_HEAD` before creating the tag. Do not infer synchronization from the absence of ahead/behind text.

### command-creator#D8-3
- severity: medium
- dimension: D8
- location: skills/command-creator/SKILL.md:110
- fix: After a successful query, select the peeled value when present and otherwise the direct tag-ref value. Compare that value with TARGET to distinguish an already-landed release from a conflict. Treat successful empty output as absence and retain the existing stop rule for query failures.

### command-creator#D1-1
- severity: low
- dimension: D1
- location: skills/command-creator/SKILL.md:15
- fix: Cut the stem-equals-name and kebab-case parts, which the model already knows. Keep only the namespace rule (a subfolder gives `/group:name`), which it does not.

### command-creator#D2-1
- severity: medium
- dimension: D2
- location: skills/command-creator/SKILL.md:119
- fix: Add a rule to Workflow step 1: when the user's manual order puts a side effect before a read-only check (for example publishing before running tests), point out the reordering, propose the safe order and ask before changing it. Do not silently keep or silently change the user's order.

### command-creator#D5-1
- severity: low
- dimension: D5
- location: skills/command-creator/SKILL.md:21
- fix: Make the second condition concrete, for example: "or when the command maps several failing checks to fixes, or needs fixed SUCCESS and STUCK report formats". Add: "Do NOT load it when the skeleton in patterns.md already covers the body."

### command-creator#D1-1
- severity: low
- dimension: D1
- location: skills/command-creator/SKILL.md:15
- fix: Condense the basic file-stem and menu-discovery explanations. Retain the non-obvious command frontmatter constraints, shadowing checks, scope-conflict routing, and requirement to report the resulting path and invocation.
