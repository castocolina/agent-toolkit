# Plan 13 — Intent: the user's rulings (2026-11-06)

Two plans carry these rulings and must satisfy every one below: [plan 13, judge preservation](2026-11-06-13-judge-preservation.md) holds R3, R5 and the judge half of R4 (skill-judge checks sources on every judgment), and [plan 14, content recovery](2026-11-06-14-content-recovery.md) holds R1, R2 and the per-artifact half of R4 (each artifact's sources found and facts verified when its turn comes). Each ruling is quoted as the user wrote it (rulings given in Spanish appear in English rendering, since every artifact is written in English), followed by a plain restatement.

## R1. Every artifact, not one example

> (English rendering) "I mentioned codex as an example; it should be done with every skill, each when its turn comes."

Codex was only an example. The exercise (recover content, find sources, re-verify facts such as model IDs) applies to every skill, command and agent, each when its turn comes.

## R2. Classify each loss before acting; recovery is not automatic

> "the is not recover only because something was lose, is check if the lose content was redistributed or removed only to fit or it was real valuable for the skill/command/agent"

A removed piece is not restored just because it was removed. For each piece of lost content, establish which it is:

- **redistributed**: it moved elsewhere (another file of the artifact, or another artifact) and is still reachable;
- **removed only to fit**: it was cut to satisfy the judge or a size target, not because it was wrong or useless;
- **of real value** to that skill, command or agent (or not).

Only content of real value that was removed to fit, and is not reachable elsewhere, is restored.

## R3. skill-judge itself advises on removals and verifies them

> "also the skill judge must be advidsor about that and check the content where not removed to fit"

skill-judge must warn about this and check, on every judgment, that content was not removed only to fit.

## R4. Sources, every time

> "and every time check sources to verify what the skill say or reference"

Every review checks the sources, to verify what the artifact states and what it references (claims, facts, links, versions).

## R5. Collateral deletions

> (English rendering) "It is also common for agents asked to change one sentence to remove what they should not, or to delete the adjacent paragraph or line by mistake; that must be avoided and verified by skill-judge itself."

Agents asked to change one sentence often remove something they should not, or delete the adjacent paragraph or line by mistake. That must be prevented, and skill-judge itself must verify it.

## R6. CI rubric repairs (ruling 2026-11-06)

When the scheduled audit's research job repairs skill-judge's rubric after an Agent Skills spec change, the removal check must not flag those edits on later runs. Ruling: leave the vendored upstream mirror (`skills/skill-judge/references/agentskills/`) out of the previous-version comparison, because it is upstream text, not ours; and the apply job's fixer writes record rows for each rubric repair it applies, so every CI edit to our own text is explained.

## R7. What the removal rule protects (ruling 2026-11-06, during plan 13)

The user, in English rendering: "I have not forbidden editing fixtures. I asked for care not to remove a skill's original content (its SKILL.md, README, references/, scripts) marginally just to fit, or carelessly, losing possibly valuable content. Everything removed must be justified, and the judge must likewise rule on whether the justification is valid. [...] A modified eval or fixture is less serious than lost content." A follow-up ruling the same day: skill-judge must state its responsibilities: guard against arbitrary removal and against content added only to satisfy the evaluations; everything must make sense for the skill's purpose; editing is allowed, but not just to get past the judge; the rules of the judge and of Agent Skills must be met while keeping the skill's spirit, without careless losses from misused edit tools or unrequested rewrites that drop paragraphs or meaning.

The rule protects an artifact's own content (SKILL.md, README, `references/`, `scripts/`): nothing is removed marginally, to fit, or carelessly; every removal is justified, and the judge rules on whether the justification is valid. Editing an eval or a calibration fixture is allowed and far less serious than losing content. The same goes for coordination: an executor that skips part of a task with an excuse, or silently omits it, must be caught by the coordinator, who checks that every deviation is genuine.

## Earlier rulings this plan also carries

- Never remove attribution, credit or license lines.
- Judge each artifact by its own pinned spec; never delete an artifact for being unaudited.
- Facts that churn (model IDs, flags, prices) are checked against official documentation, not third-party summaries.
- Implementers: native sonnet subagents (Claude Code `Agent` tool, `model: sonnet`, effort medium), dispatched by the controller; Opus high or xhigh may plan and fix. `router-env/my-coding` is no longer used for implementation and never reviews or judges (ruling 2026-11-02; this supersedes plan 8 Task 3 Step 2's `pi ... my-coding` dispatch).
- Review and judging lanes: two referee lanes per round is ideal, one is enough, and a third replaces an unavailable one. Lanes are not blockers: when lanes are down, pivot or wait, never stop the plan (standing ruling, 2026-11-04/05). This overrides any earlier plan's "stop with fewer than two lanes" rule.
