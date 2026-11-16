# Batch 21

## lesson-learned (skill)

### lesson-learned#D7-1
- severity: medium
- dimension: D7
- location: skills/lesson-learned/evals/evals.json:9
- fix: Add before/after code or diff fixtures and assert a concrete behavioral consequence with citations. Include an extraction that increases coupling, a mechanical multi-file rename, and partial-merge comparison evidence; allow the correct result to reject an improvement claim or decline a principle label.

### lesson-learned#D8-1
- severity: medium
- dimension: D8
- location: skills/lesson-learned/SKILL.md:21
- fix: Inspect git status before declaring evidence absent. Include relevant untracked files as new-file additions, respecting ignore rules and scope, or explicitly ask whether they should be included.

### lesson-learned#D7-1
- severity: medium
- dimension: D7
- location: skills/lesson-learned/evals/evals.json:5
- fix: Add fixture diffs or a small fixture repo under evals/files/ so assertions about file citations, counterfactuals and no-fabrication can be graded against real output instead of hypothetical descriptions

### lesson-learned#D8-1
- severity: low
- dimension: D8
- location: skills/lesson-learned/SKILL.md:17
- fix: Add the fallback branch: with no remotes, compare against main/master if it exists, otherwise fall back to the last 5 commits, stating the choice instead of only asking

### lesson-learned#D1-1
- severity: medium
- dimension: D1
- location: skills/lesson-learned/SKILL.md:51
- fix: Keep each evidence rule once, at the decision where it matters. Replace generic anti-pattern definitions and refactoring prescriptions with concise diff-specific evidence requirements and counterexamples not already covered by se-principles.md.

### lesson-learned#D1-1
- severity: medium
- dimension: D1
- location: skills/lesson-learned/references/anti-patterns.md:5
- fix: Cut the textbook definitions (God Object, Feature Envy, Magic Numbers, Long Method) the model already knows; keep only each pattern's diff-signal and false-positive mapping, which is the part the model lacks

### lesson-learned#D2-1
- severity: low
- dimension: D2
- location: skills/lesson-learned/SKILL.md:35
- fix: Keep this rule in one place: cite se-principles.md's change-amplification row from the body instead of restating it, freeing body lines for scoping judgment the reference lacks

### lesson-learned#D3-1
- severity: low
- dimension: D3
- location: skills/lesson-learned/SKILL.md:22
- fix: Extend the evidence-scope gotchas with the other non-obvious git traps: shallow clones have no merge-base for three-dot diffs, and `git show` on a merge commit shows only the squashed conflict resolution

### lesson-learned#D6-1
- severity: low
- dimension: D6
- location: skills/lesson-learned/SKILL.md:39
- fix: Allow a one-paragraph conversational answer when the user asks a quick reflective question, reserving the four-field template for requested artifacts or written reports
