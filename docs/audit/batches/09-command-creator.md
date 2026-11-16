# Batch 09

## command-creator (skill)

### command-creator#D7-1
- severity: medium
- dimension: D7
- location: skills/command-creator/evals/evals.json:1
- fix: Add assertions for maximum attempts and stuck detection, plus edge cases covering shell-special characters in arguments and a timed-out publication that may already have succeeded. Verify validation, state inspection before retry, and explicit authorization boundaries.

### command-creator#D8-1
- severity: high
- dimension: D8
- location: skills/command-creator/references/patterns.md:202
- fix: Apply the registered-agent check to every delegation example. Select an actually available suitable agent, and otherwise continue directly while preserving the planning and approval boundary; remove unconditional references to the custom subagent type.

### command-creator#D7-1
- severity: low
- dimension: D7
- location: skills/command-creator/evals/evals.json
- fix: Add a fixture transcript of a user's manual release procedure so the underspecified-workflow eval can grade requirement extraction against real input.

### command-creator#D8-1
- severity: medium
- dimension: D8
- location: skills/command-creator/SKILL.md:16
- fix: Add an adaptation caveat when examples load: their tools (Graphite gt, make all-ci, .PLAN.md, TodoWrite) are project-specific; map them to the user's toolchain before reusing the skeleton.

### command-creator#D1-1
- severity: medium
- dimension: D1
- location: skills/command-creator/references/patterns.md:9
- fix: Collapse generic workflow tutorials and native planning, todo, and delegation explanations. Keep command-specific field semantics, argument boundaries, environment constraints, and concrete failure-recovery decisions.

### command-creator#D2-1
- severity: medium
- dimension: D2
- location: skills/command-creator/SKILL.md:14
- fix: Treat plan–approval–execution as an approval-gated workflow independent of delegation. Choose delegation only when specialization, isolation, or parallel work provides a concrete benefit.

### command-creator#D3-1
- severity: medium
- dimension: D3
- location: skills/command-creator/SKILL.md:33
- fix: Add concise Gotchas explaining that argument-hint is display metadata rather than validation and that pre-run ! shell blocks execute during prompt expansion, before written workflow inspection or approval steps. Prohibit state-changing pre-run blocks and require explicit body-level argument validation.

### command-creator#D6-1
- severity: medium
- dimension: D6
- location: skills/command-creator/references/examples.md:113
- fix: Replace the blanket prohibition with bounded inspection criteria: permit checks necessary to establish prerequisites, intended changes, authorization, and verification, while requiring approval before unrelated or open-ended exploration.

### command-creator#D1-1
- severity: low
- dimension: D1
- location: skills/command-creator/SKILL.md:14
- fix: Keep these four expert patterns in references/patterns.md; drop the generic Advanced Patterns section (context-file priority, conditional tool selection, progressive disclosure, makefile wrapper) that the model derives on its own.

### command-creator#D2-1
- severity: low
- dimension: D2
- location: skills/command-creator/SKILL.md:16
- fix: State the validation loop explicitly: draft, check against the best-practices checklist, fix, re-check until it passes; step 5 names validation without the loop.

### command-creator#D3-1
- severity: low
- dimension: D3
- location: skills/command-creator/SKILL.md:33
- fix: Add the why: a global override silently changes behavior for every future invocation in every project, not just this command run.

### command-creator#D6-1
- severity: low
- dimension: D6
- location: skills/command-creator/SKILL.md:15
- fix: Define the one ambiguous case concretely (a repo exists but the user says 'for all my projects'); 'meaningful ambiguity' otherwise leaves a default-vs-ask boundary to judgment.
