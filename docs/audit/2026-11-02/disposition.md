# Disposition of commands, agents and the two new skills (plan 7 Task 3)

Scores are the two-lane merge in `merged.json` (lanes `my-referee-one` and `my-referee-three`; `my-referee-two` returned 503 on 2026-11-02). Commands and agents were judged with the plan 6 profiles, which were never calibrated: their scores are an **uncalibrated baseline**. Plan 12 pins the command and agent specs, calibrates both profiles and judges these 13 again; plan 8 fixes them from that calibrated file, not from this one.

User ruling (2026-11-02): skills, commands and agents are distinct capabilities, and none is deleted, merged or converted for never having been audited or for a low uncalibrated score. Every command and agent is kept and refined. Duplicated rules move into the matching skill, and the agent preloads that skill with `skills:` and stays an agent.

Findings columns: critical / high / medium / low.

| artifact | kind | score | findings | decision | reason | plan 8 tasks |
|---|---|---|---|---|---|---|
| codex-plan | command | 42.0 F | 0/3/14/1 | fix | real entry point; pins `gpt-5.2-codex` in the body and has no eval file | Task 5 Step 1 (eval file first), Task 3 batch |
| compose-email | command | 50.0 F | 0/4/9/2 | fix | user-triggered drafting flow; no eval file | Task 5 Step 1, Task 3 batch |
| explain-changes-mental-model | command | 48.4 F | 0/5/9/3 | fix | no eval file | Task 5 Step 1, Task 3 batch |
| explain-pr-changes | command | 76.0 C | 0/3/5/4 | fix | has a full eval suite (not rerun here, Review Focus 4); no frontmatter `description` | Task 4 (diagram rules), Task 3 batch |
| sync-branch | command | 38.8 F | 0/10/5/0 | fix | side effects (rebase, force-with-lease push); `$target` is never bound to the argument; no eval file | Task 5 Step 1 (eval file before any edit), Task 3 batch |
| sync-skills-readme | command | 60.0 D | 0/4/9/4 | fix | side effects (rewrites README.md); no eval file | Task 5 Step 1 (eval file before any edit), Task 3 batch |
| viral-tweet | command | 51.6 F | 0/4/8/2 | fix | no eval file | Task 5 Step 1, Task 3 batch |
| ascii-ui-mockup-generator | agent | 46.0 F | 1/4/9/1 | fix | real delegate worth its own context (mockups before implementation) | Task 5 Step 3 batch |
| codebase-pattern-finder | agent | 50.4 F | 0/3/14/2 | fix | real delegate: read-only search in a separate context | Task 5 Step 3 batch |
| communication-excellence-coach | agent | 46.8 F | 0/4/11/2 | fix | real delegate (review and roleplay in its own context); lanes disagree, see below | Task 5 Step 3 batch |
| general-purpose | agent | 41.2 F | 0/5/11/0 | fix | a preset agent with house rules is worth having; whether an installed agent of this name replaces Claude Code's built-in `general-purpose` is UNVERIFIED (the sub-agents page states the override only for `Explore`); today it only restates generic traits | Task 5 Step 3 batch |
| mermaid-diagram-specialist | agent | 38.8 F | 0/7/12/4 | fix | overlaps `mermaid-diagrams`: unique rules move into the skill, the agent preloads it with `skills:` and keeps the delegate role; lanes disagree, see below | Task 4 Step 5, Task 5 Step 3 batch |
| ui-ux-designer | agent | 51.6 F | 0/5/12/2 | fix | overlaps `ui-ux-principles`: the agent preloads the skill and keeps only its critique role, never a second copy of the rules | Task 5 Step 2, Task 5 Step 3 batch |
| ui-ux-principles | skill | 86.8 B | 0/0/7/4 | fix | under 90 | Task 2 queue |
| skill-updater | skill | 93.2 A | 0/1/7/3 | fix | 90 or more but holds a high finding (queue predicate) | Task 2 queue |

## Agents: load on demand or own context? (Review Focus 2)

All six are real delegates: each runs a task that benefits from its own context window, tool list or model, and none is a long reference that would be better loaded on demand. Where an agent carries reference material that duplicates a skill (`mermaid-diagram-specialist`, `ui-ux-designer`), the material moves to the skill and the agent preloads it; the agent stays.

## Commands: eval files

Only `explain-pr-changes` has `commands/evals/<name>.json`. The side-effecting `sync-branch` and `sync-skills-readme` get one before plan 8 edits them; every other command gets one in its first fix dispatch (plan 8 Task 5 Step 1).

## Lane disagreements (gap above 10 points)

Both artifacts already have a lane-three verdict, so per Task 2 Step 6 they are listed here instead of being judged a third time:

- `communication-excellence-coach`: one 52.8, three 40.8.
- `mermaid-diagram-specialist`: one 44.8, three 32.8.

Both are F on either lane, so the gap does not change the decision. Plan 12's calibrated re-judge supersedes both.

## Decisions that need the user

None open. The user answered on 2026-11-02: keep and refine all 13 commands and agents (no `delete`, `convert-to-skill` or `merge-into`).
