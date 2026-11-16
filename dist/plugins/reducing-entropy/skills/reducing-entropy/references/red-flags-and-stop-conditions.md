---
description: Use when the step-6 re-measure shows a candidate's after count is not lower than its before count, when an argument for keeping code is offered, or when nothing seems worth deleting; it holds the less-total-code rule, replies to five common arguments and the conditions that end the pass.
---

# Less total code: the rule, the arguments, the stop conditions

## The rule

Count lines before and after for each candidate (the step-2 counter, rerun at the step-6 re-measure). If the after count is higher, reject the candidate unless a step-1 need (a contract, security or compliance requirement) requires the extra code; then say which one.

- "Better organized" with more code is more entropy.
- "More flexible" with more code is more entropy.
- "Cleaner separation" with more code is more entropy.

## Arguments to answer, not accept

Reply with the measured count, not with a preference. None of these overrides the step-1 boundary: a behavior, public contract or data-retention obligation that must survive stays, whatever the argument.

- **"Keep what exists."** Status quo bias: the question is total code at the end, not churn.
- **"This adds flexibility."** Flexibility for what? Without a named, current need, YAGNI applies; PAGNI ([expensive-to-add-later](expensive-to-add-later.md)) lists the few exceptions.
- **"Better separation of concerns."** More files and functions are more code, and separation is not free. Keep it only when parts change for independent reasons ([design-is-taking-apart](design-is-taking-apart.md)).
- **"Type safety."** Keep every type, annotation or validator that guards a public contract, a stored schema or a behavior from step 1, and any check a test or caller depends on: those outrank line count. Question only the ones that guard nothing of that kind: compare their lines with the failures they prevent, and replace them only with a check that protects the same contract in less code.
- **"Easier to understand."** Fourteen things are not easier to understand than two; compare the counts.

## Stop conditions

End the pass instead of forcing deletions when:

- The code is already minimal for what it does: report no candidates rather than inventing deletions.
- The framework has strong conventions: do not fight it; delete only what the convention does not require.
- A regulatory or compliance requirement mandates the structure (step 1).
- The user wants new functionality and accepts the code cost (the manual-only boundary in SKILL.md).
