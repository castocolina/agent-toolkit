# Batch 53

## game-changing-features (skill)

### game-changing-features#D7-1
- severity: low
- dimension: D7
- location: skills/game-changing-features/evals/evals.json
- fix: Add an eval where the prior session sits under a slug that differs from the repo name, and assert that the skill reuses that folder and writes the next session-N.md. Add a second eval that runs without write access, and assert that the reply gives the intended path and the full artifact.

### game-changing-features#D8-1
- severity: medium
- dimension: D8
- location: skills/game-changing-features/SKILL.md:35
- fix: Cover the case where the Baseline shows the requested feature already exists, either built but unreleased or live behind a flag. Right now line 14 forbids pitching it and line 35 says to evaluate it as a new idea. Add: 'If the requested feature appears in the Baseline as built-but-unreleased or live, say so, and recommend a rollout or exposure decision instead of building it; then compare that decision with one broader opportunity.'

### game-changing-features#D1-1
- severity: low
- dimension: D1
- location: skills/game-changing-features/SKILL.md:15
- fix: Shorten this jobs-to-be-done framing, which the model already knows, to the parts that are specific to this skill: the network-effect test and the requirement for a segment-and-metric hypothesis with its cheapest test.

### game-changing-features#D2-1
- severity: low
- dimension: D2
- location: skills/game-changing-features/SKILL.md:15
- fix: Add one prompt that produces Massive Gems, for example: 'before ranking, ask what the user does right before and right after using the product; a candidate that absorbs either step is a Massive Gem candidate.' Without it the step only finds friction and tends to yield Medium and Small ideas.

### game-changing-features#D3-1
- severity: medium
- dimension: D3
- location: skills/game-changing-features/SKILL.md:37
- fix: Add: 'NEVER make the user's requested feature Do Now just because they asked for it. A request anchors the ranking, so it has to win the comparison with at least one broader opportunity on impact and feasibility.' Also add: 'NEVER put a number in the Reach column that no source gives you, because a made-up percentage reads as measured.'

### game-changing-features#D4-1
- severity: low
- dimension: D4
- location: skills/game-changing-features/SKILL.md:3
- fix: Find and rank high-leverage product opportunities from repository, feedback, changelog, feature-flag and usage evidence, and save them as a strategy session file. Use when the user asks what to build next, where to focus a small team, how to cut churn or improve retention, what would make the product 10x more valuable, for growth levers or small wins, or whether a requested feature is the right next move, even if they never say 'strategy' or '10x'. Gives recommendations and assumptions to validate only. Not for implementing code, sprint plans, user stories, effort estimates, competitor or pricing research, or roadmaps with committed dates.

### game-changing-features#D6-1
- severity: low
- dimension: D6
- location: skills/game-changing-features/SKILL.md:27
- fix: Set a default scale and keep it consistent across sessions: 'Effort: S (under a week), M (weeks), L (a quarter or more) for the team size given; Risk: low, medium or high, plus the main failure mode.'
