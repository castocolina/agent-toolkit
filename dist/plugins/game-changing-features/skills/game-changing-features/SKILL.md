---
name: game-changing-features
description: "Find and rank high-leverage product opportunities from repository, feedback and usage evidence, saved as a session file. Use when users ask what to build next, where a small team should focus, how to fix retention or churn, for '10x' ideas, growth levers or small wins, or whether a requested feature is the right next move, even without the word 'strategy'. Recommendations and assumptions to validate only; not for implementing code, sprint plans, user stories, effort estimates, competitor or pricing research, or committed-date roadmaps."
---

# 10x Product Strategy

Output: ranked, evidence-grounded opportunities and the assumptions to validate, never code. Default path: `.claude/docs/ai/<product-slug>/10x/session-N.md`.

## Workflow

1. **No evidence source?** Do not stop to ask for access: state a bounded assumption drawn from the prompt, proceed, and label every claim a hypothesis.
2. **Baseline.** List the folders under `.claude/docs/ai/` and reuse the one whose prior session names the same product, even when its slug differs from the repo name; only when none matches, kebab-case the product name. If that folder has sessions, read the latest first and mark each earlier recommendation and open question as done, still open or dropped against the current evidence; carry the open ones forward. Then read shipped features, unreleased or flagged work, issues and support feedback, research and telemetry, applying the Gotchas below. A source you cannot see makes its claims unknown, not invented.
   **Checkpoint:** fill the template's Baseline table before Discover. A built-but-unreleased or flagged row is never pitched as a new build; its release or rollout step can be a candidate, with its own reach and evidence.
3. **Discover.** Draw candidates from three sources: friction points in the evidence, user groups who cannot use the product today (platform, permissions, language, price, skill), and what users do right before and right after using it (absorbing one of those steps is a Massive Gem candidate). For each, check once:
   1. Does the idea remove the binding step or unlock the group, or only relieve the symptom?
   2. Its value mechanism: a network effect only when another participant raises value for existing users; "collaboration" alone is not one.
   3. The segment, the metric it should move, and the cheapest test.
4. **Rank.**
   1. Tier by test, taking the lower tier when two fit: **Massive Gems** remove a whole step of the user's job or unlock a new user group; **Medium Gems** remove friction inside a step that stays; **Small Gems** are polish on one known pain. Five to ten ideas by default, with at least one Small Gem when the evidence supports one (otherwise say none qualified).
   2. Score and order within each tier: reach share (percentage points, 0-100) × evidence (1 hypothesis, 2 one source, 3 two agreeing sources) / (effort S=1, M=2, L=3 + adoption cost low=1, medium=2, high=3); ties go to the cheapest test. When reach is unknown, score a bounded hypothesis share marked `hypothesis:`; when none is defensible, leave the idea unscored (lowest in its tier) and make a reach-measurement test its validation question. A strategic bet outranks a higher score only with an explicit reason and validation plan.
   3. Prioritize: exactly one idea in the session is **Do Now**, the highest-scoring idea across all tiers whose cheapest test fits the team's stated capacity (ties go to the higher tier); when capacity is unstated or no test fits, write "No Do Now yet", name the missing capacity constraint and the cheapest question or test that resolves it; every other is **Do Next**, **Explore** or **Backlog**, each with its reason. These are recommendations, not commitments or dates.
   4. Reach: every cell names the user-base number from the request or evidence, in the template's form; when neither gives one, write "unknown share of the active base; measure <metric>" and ask for the number in the validation questions.
5. **Check, then save.** Before writing, confirm every citation resolves: the file and line exist, the issue number exists, the metric or query name is real. Drop or relabel as hypothesis any that do not. Write the next unused `session-N.md` in the product folder; never overwrite an earlier session, it is the decision record the next session builds on. When file writing is unavailable, state the intended path and give the full artifact in the reply.

```markdown
# <Product> 10x session N (<date>)
Previous: session-<N-1>.md or none, items carried forward or closed
## Scope and assumptions
## Baseline
| Capability or fact | Live / built-but-unreleased / planned / unknown | Citation |
## Opportunities
### Massive Gems
| Idea (in rank order) | Priority | Evidence or hypothesis | Mechanism | Reach ("hypothesis: ~20% of 12,000 weekly" or "unknown share of 12,000 weekly; measure X") | Effort (S under 1 week, M 1-6 weeks, L more than 6 weeks, for the team given) | Deciding trade-off (two factors: "high reach vs 3-week effort", never a bare label) | Assumption to validate |
Under each table, one line: the main risk and adoption cost (low, medium or high: setup, switch, permissions, trust) behind the order.
(Repeat the table and line under `### Medium Gems` and `### Small Gems`.)
## Validation questions (each with its cheapest test)
```

For one requested feature (such as "add CSV export"), check the Baseline first: if it is built-but-unreleased or flagged, say so and apply the checkpoint rule. Otherwise classify its scale from the evidence, usually Small or incremental, and write a short comparison instead of the full session tables: the requested feature plus two to four broader alternatives in one table (Idea, Priority, Mechanism and impact, Reach, Effort, Next test), exactly one Do Now. Still save it as the next `session-N.md` with Scope, Baseline, this table and Validation questions; the tier tables and five to ten ideas stay the default for every other session.

## NEVER

- NEVER pitch "add AI", "add social" or "add a dashboard" without naming the step it removes or the group it unlocks: trend features sound big and rank high with no mechanism behind them.
- NEVER make the requested feature Do Now just because the user asked for it: the request anchors the ranking, so it must win the comparison with at least one broader opportunity on impact and feasibility.
- NEVER state a number or causal claim that is not verbatim in a cited source without the prefix `hypothesis:`: an inference written plainly reads as measured fact.
- NEVER treat matching a competitor as evidence of leverage: tier a parity feature by the same step-removal and group-unlock tests, and call it Massive only when cited evidence shows it unlocks an excluded group or removes a step; otherwise it is Small or Medium.

## Gotchas

- Code is not availability. Feature flags, plan entitlements, partial rollouts and merged-but-unreleased work mean a capability in the repository may reach no customer. Count it in the current baseline only with release or exposure evidence (changelog entry, flag state, rollout percentage).
- Roadmaps go stale: they keep shipped or abandoned items listed as planned. Check the changelog or git history before citing one as future work.
- Registered accounts overstate reach; size an opportunity by active users of the affected flow.
- A checked-in flag file is often only the default or one environment's state, and production may override it remotely: say which environment it shows before calling a feature live.
- Telemetry event names change between releases, so a zero count can mean a renamed event; check the tracking plan or changelog before reading zero as no usage.
- When two sources disagree (tickets ask for X, telemetry shows X is ignored), report both and make the conflict a validation question; silently picking one hides the real unknown.
