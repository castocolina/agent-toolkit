# Batch 16

## ship-learn-next (skill)

### ship-learn-next#D7-1
- severity: medium
- dimension: D7
- location: skills/ship-learn-next/evals/evals.json:7
- fix: Make the missing-source case assert a transcript/content request or an explicitly provisional plan, no fabricated source lessons, and accurate write-status reporting. Add cases for noisy outcomes, inconsistent execution, and chat-only delivery.

### ship-learn-next#D7-2
- severity: medium
- dimension: D7
- location: skills/ship-learn-next/evals/trigger-queries.json:3
- fix: Add varied casual and detailed prompts with source paths, deadlines, available time, and existing rep results. Include near-misses that request a lesson summary or project plan despite sharing implementation vocabulary.

### ship-learn-next#D8-1
- severity: medium
- dimension: D8
- location: skills/ship-learn-next/SKILL.md:30
- fix: Time-box retries within the user's budget. After a failed repeat, route to shrinking the rep, removing a blocker, or renegotiating the target rather than repeating unchanged indefinitely.

### ship-learn-next#D7-1
- severity: medium
- dimension: D7
- location: skills/ship-learn-next/evals/trigger-queries.json:2
- fix: Expand queries into full realistic messages with context, phrasing variety, and occasional typos; telegraphic phrases under-test the description.

### ship-learn-next#D8-1
- severity: medium
- dimension: D8
- location: skills/ship-learn-next/SKILL.md:45
- fix: Add a five-line example Rep 1 (deliverable, controllable criterion, steps, reflection questions) so agents copy the plan shape instead of guessing it.

### ship-learn-next#D1-1
- severity: medium
- dimension: D1
- location: skills/ship-learn-next/SKILL.md:15
- fix: Compress routine intake and repeated intent/provenance guidance while retaining safeguards. Spend the saved space on a compact worked example distinguishing artifact evidence, noisy outcomes, and the resulting next-rep decision.

### ship-learn-next#D6-1
- severity: medium
- dimension: D6
- location: skills/ship-learn-next/SKILL.md:34
- fix: Require one-variable changes when the plan makes causal comparisons. For creative or integrative practice, default to one declared learning target while permitting coordinated changes when the user’s goal or time budget requires them.

### ship-learn-next#D1-1
- severity: low
- dimension: D1
- location: skills/ship-learn-next/SKILL.md:21
- fix: Compress derivable coaching lines like this and "Be direct, question-driven"; spend the tokens on the non-obvious rules (controllable criteria, one variable per rep, the evidence decision rule).

### ship-learn-next#D2-1
- severity: low
- dimension: D2
- location: skills/ship-learn-next/SKILL.md:15
- fix: Add a prioritization rule for competing lessons: when several lessons could be Rep 1, pick the one with the smallest shippable test in the user's available time.

### ship-learn-next#D3-1
- severity: low
- dimension: D3
- location: skills/ship-learn-next/SKILL.md:51
- fix: Add a gotcha: a source's motivational claims are not lessons; extracting them produces a rep that tests nothing.
