# Batch 54

## game-changing-features (skill)

### game-changing-features#D7-1
- severity: low
- dimension: D7
- location: skills/game-changing-features/evals/evals.json:20
- fix: Make the expected output specific: name the Reach form in terms of 12,000 weekly users, S/M/L effort for a two-person team and exactly one Do Now. Add an eval where a prior session holds a recommendation the evidence now shows shipped, and assert it is marked done rather than re-pitched.

### game-changing-features#D8-1
- severity: medium
- dimension: D8
- location: skills/game-changing-features/SKILL.md:38
- fix: State whether the single-feature path still saves session-N.md and keeps the Baseline and Validation questions sections. For example: 'Still save it as the next session-N.md with Scope, Baseline, this comparison table and Validation questions.' Also state that session 1 writes 'Previous: none' on line 24.

### game-changing-features#D1-1
- severity: low
- dimension: D1
- location: skills/game-changing-features/SKILL.md:19
- fix: The model already knows this RICE-style formula. Keep only what it lacks: the lower-tier rule, the cheapest-test tie-break, the requirement for a Small Gem and the single Do Now. Cut the generic scoring explanation to one clause.

### game-changing-features#D2-1
- severity: low
- dimension: D2
- location: skills/game-changing-features/SKILL.md:19
- fix: Split Rank into numbered sub-steps (tier, order, label priority, write Reach) so the Process pattern's checkpoints stay visible. Add a checkpoint: 'exactly one Do Now and every Reach cell sourced or unknown-share' before step 5.

### game-changing-features#D3-1
- severity: medium
- dimension: D3
- location: skills/game-changing-features/SKILL.md:51
- fix: Several Gotchas are standard product-management advice the model mostly knows. Add environment-specific traps that defy assumptions, for example: flag files often differ per environment, so read the production flag state, not a staging or default config; telemetry event names change between releases, so check the tracking plan before treating a zero count as no usage.

### game-changing-features#D4-1
- severity: low
- dimension: D4
- location: skills/game-changing-features/SKILL.md:3
- fix: Use when a user wants to know what to build next or where a small team should focus. Finds and ranks high-leverage product opportunities from repository, changelog, feature-flag, feedback and usage evidence, and saves them as a strategy session file. Also use when a user asks how to fix churn, retention or stickiness, wants '10x' ideas, growth levers or small wins, or asks whether a requested feature is the right next move, even if they never say 'strategy'. Gives recommendations and assumptions to validate only. Not for implementing code, sprint plans, user stories, effort estimates, competitor or pricing research, or roadmaps with committed dates.

### game-changing-features#D6-1
- severity: medium
- dimension: D6
- location: skills/game-changing-features/SKILL.md:30
- fix: The template requires an 11-column table for every idea in what is a judgement-heavy strategy task, which pushes the agent toward filling cells over reasoning. Keep the fixed columns the evals check (Idea, Priority, Evidence, Mechanism, Reach, Effort, Assumption). Merge Risk, Adoption cost and Deciding trade-off into one 'Why this rank' note per idea.
