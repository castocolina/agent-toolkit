---
name: game-changing-features
description: "Find and prioritize product opportunities and high-impact features. Use when users ask what to build next, seek product strategy, or want a product to be substantially more valuable, including ‘10x’ ideas, feature opportunities, growth levers, or small wins. Give evidence-based recommendations and validation priorities only; not for implementing code, sprint planning, or committed-date roadmaps."
---

# 10x Product Strategy

Produce evidence-grounded strategy recommendations and assumptions to validate—not code, sprint plans, or committed-date roadmaps. Save each analysis to `.claude/docs/ai/<product-or-area>/10x/session-N.md` by default; never overwrite an existing session.

## Establish evidence before ideas

If no filesystem or evidence source is available to you, do not stop at asking for access or inputs. State a bounded assumption from the prompt, produce concrete hypotheses with impact/feasibility reasoning and priorities, and identify what to validate; do not claim the assumptions are observed facts.

1. Infer product area from the repository if the user does not name one; state the inference. If no repository/context exists, request the minimum product, user, and current-value context or label assumptions explicitly.
2. Inspect available product evidence before brainstorming: existing features and unreleased work, issues/support feedback, user research, telemetry/drop-off, and relevant data/assets. Cite exact evidence locations. If a source is unavailable, treat the relevant claim as unknown rather than inventing user behavior.
3. Mine complaints and friction first, then generate a small ranked set of concrete opportunities. When evidence and user context are sufficient, include a tiered set labeled **Massive Gems**, **Medium Gems**, and **Small Gems** (at least one low-effort small gem). For each candidate, state the user problem and a plausible value mechanism; do not wait for perfect telemetry when useful hypotheses can be labeled with confidence and validation needs.
4. For each candidate, record: user/value mechanism, evidence and confidence, reach (actual affected users, not total registrations), adoption constraint, effort, and risk. Explain which trade-off determines its rank. A strategic bet may outrank an easier idea only with an explicit reason and validation plan.

## Prioritization tests

- Characterize low-cost, limited-scope requests such as CSV export as small/incremental unless evidence supports a larger opportunity. Compare them with at least one broader opportunity using impact and feasibility when the user asks whether a specific request is transformative.
- Request frequency is not willingness to pay or proof of severity; distinguish repeated vocal requests from observed behavior and impact.
- Adoption friction can erase theoretical value: identify setup, workflow-switching, permissions, and trust costs.
- Call something a network effect only when another participant increases value for existing users; “collaboration” alone is not a mechanism.
- Search the repository and roadmap for existing or unreleased versions before proposing a feature as novel.
- Separate facts, inference, and hypotheses. Turn low-confidence, high-consequence assumptions into validation questions rather than polished claims.

## Session file handling

Choose a concise product slug. Find the next unused `session-N.md` in the target folder (create directories as needed); preserve all prior reports. If file writing is unavailable, state the intended path and provide the complete strategy artifact in the response so the user still receives the deliverable. If current-state evidence is missing, explicitly list blockers/assumptions in the saved artifact when possible.

Use a short ranked set by default, grouped into **Massive Gems**, **Medium Gems**, and **Small Gems** when the available context supports concrete hypotheses; mark assumptions and confidence rather than withholding all ideas for missing evidence. For each recommendation include its evidence or explicit hypothesis, value mechanism, adoption constraint, estimated impact and feasibility/effort, rank rationale, and assumption to validate. Assign a practical priority such as **Do Now**, **Do Next**, **Explore**, or **Backlog**, with a reason; these are recommendations, not implementation or committed dates. Expand to a full opportunity sweep only when product scope and evidence support it.
