# Content recovery report (plan 14)

Built from recorded data on 2026-11-16: phrase fate from `docs/audit/recovery/<name>/sections.json` (before) and `recovery inventory --fate-only` against dbff837f (after); decisions from `record.md`; registry rows added since `139d50f9^`; facts outcomes from `facts.md`; final grade from the last `merged.json` that holds the artifact.

Columns: phrase fate is kept/moved/gone in percent of the baseline's phrases; decisions are the restored/dropped/intended-change rows of `record.md` for sections and files, and `para rows` counts its paragraph-level rows (small rewrites and drops) apart; facts are verified/corrected/pointer (report-only adds reported).

| artifact | kind | mode | batches | fate before | fate after | restored/dropped/intended (sections and files) | para rows | sources added | facts | final grade |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| agent-md-refactor | skill | full | 15 | 51/9/39 | 39/7/54 | 0/2/10 | 27 | 4 | 3/4/6 | 92.4 |
| agentskills-research | skill | facts-only | 19 | n/a | n/a | 0/0/0 | 7 | 8 | 7/4/5 | 94.0 |
| ascii-ui-mockup-generator | agent | full | 18 | 1/1/98 | 1/1/98 | 0/0/0 | 1 | 6 | 6/1/2 | 92.8 |
| backend-to-frontend-handoff-docs | skill | full | 15 | 62/2/37 | 55/2/44 | 2/1/13 | 16 | 5 | 8/4/1 | 90.4 |
| c4-architecture | skill | full | 11 | 5/2/93 | 7/3/90 | 12/17/6 | 17 | 6 | 30/3/3 | 93.6 |
| codebase-pattern-finder | agent | full | 13 | 2/0/98 | 1/0/99 | 0/1/3 | 7 | 4 | 6/1/1 | 94.4 |
| codex | skill | full | 8 | 30/0/69 | 17/0/82 | 2/1/8 | 6 | 7 | 19/9/3 | 84.8 (accepted by the user) |
| codex-plan | command | full | 7 | 1/0/99 | 4/0/96 | 1/3/5 | 0 | 6 | 9/2/4 | 94.4 |
| command-creator | skill | full | 8 | 4/0/96 | 4/0/96 | 0/54/15 | 6 | 10 | 31/3/6 | 92.8 |
| commit-work | skill | full | 4 | 0/1/99 | 0/3/97 | 4/4/3 | 6 | 8 | 34/0/1 | 92.4 |
| communication-excellence-coach | agent | full | 13 | 1/0/99 | 1/0/99 | 0/7/0 | 4 | 5 | 8/0/1 | 94.8 |
| compose-email | command | full | 11 | 2/1/97 | 3/1/97 | 0/2/1 | 2 | 4 | 6/1/1 | 86.8 (accepted by the user) |
| crafting-effective-readmes | skill | full | 17 | 75/2/24 | 82/2/16 | 10/10/4 | 44 | 31 | 29/2/2 | 92.4 |
| daily-meeting-update | skill | full | 5 | 1/1/98 | 1/3/96 | 6/9/5 | 2 | 14 | 14/3/5 | 98.4 |
| database-schema-designer | skill | full | 1 | 0/0/99 | 0/1/99 | 5/47/1 | 76 | 21 | 24/0/13 | 94.4 |
| datadog-cli | skill | report-only | 21 | n/a | n/a | 0/0/0 | 0 | 11 | 25/0/4/6 | not judged (report-only) |
| dependency-updater | skill | full | 14,23 | 47/9/44 | 36/6/58 | 5/5/51 | 58 | 30 | 39/10/4 | 95.6 |
| design-system-starter | skill | full | 2 | 1/0/99 | 1/1/97 | 32/37/18 | 29 | 9 | 17/6/5 | 93.6 |
| difficult-workplace-conversations | skill | full | 3 | 0/0/99 | 2/10/88 | 39/34/9 | 9 | 3 | 1/3/4 | 90.8 |
| domain-name-brainstormer | skill | full | 5 | 1/2/97 | 1/2/96 | 0/8/12 | 0 | 12 | 16/0/3 | 96.0 |
| draw-io | skill | full | 16 | 45/1/53 | 39/2/59 | 2/10/27 | 106 | 12 | 20/6/6 | 93.2 |
| excalidraw | skill | full | 9 | 1/0/99 | 0/0/99 | 0/15/11 | 4 | 5 | 11/1/1 | 92.8 |
| explain-changes-mental-model | command | full | 9 | 3/0/97 | 3/0/97 | 0/4/0 | 3 | 4 | 10/0/3 | 95.2 |
| explain-pr-changes | command | full | 11 | 2/17/81 | 2/17/81 | 0/2/0 | 0 | 11 | 17/0/5 | 92.0 |
| feedback-mastery | skill | full | 9 | 2/1/97 | 3/3/95 | 11/29/5 | 9 | 2 | 4/4/0 | 95.6 |
| frontend-to-backend-requirements | skill | full | 15 | 48/19/34 | 47/20/33 | 3/1/2 | 3 | 2 | 3/0/0 | 90.0 |
| game-changing-features | skill | full | 5 | 1/1/99 | 1/8/92 | 11/15/0 | 1 | 1 | 5/0/0 | 94.4 |
| gemini | skill | full | 2 | 1/1/98 | 1/1/98 | 2/8/26 | 10 | 4 | 8/2/5 | 94.8 |
| general-purpose | agent | full | 14 | 0/0/100 | 0/0/100 | 1/0/1 | 2 | 2 | 9/1/2 | 97.2 |
| gepetto | skill | report-only | 21 | n/a | n/a | 0/0/0 | 0 | 12 | 17/0/0/15 | not judged (report-only) |
| humanizer | skill | full | 10 | 6/12/81 | 5/12/83 | 0/0/16 | 2 | 4 | 16/6/2 | 98.4 |
| jira | skill | full | 6 | 1/0/99 | 1/0/99 | 4/29/3 | 9 | 10 | 40/6/10 | 93.6 |
| lesson-learned | skill | full | 6 | 5/0/94 | 5/0/94 | 0/9/11 | 0 | 7 | 13/0/0 | 96.0 |
| marp-slide | skill | full | 12 | 24/2/74 | 24/2/73 | 18/30/27 | 67 | 13 | 35/6/7 | 94.8 |
| meme-factory | skill | full | 4 | 0/1/99 | 0/17/83 | 37/35/7 | 23 | 10 | 29/13/3 | 90.0 |
| mermaid-diagram-specialist | agent | full | 1 | 0/1/99 | 0/1/99 | 0/1/0 | 0 | 5 | 5/0/2 | 96.0 |
| mermaid-diagrams | skill | full | 12 | 13/3/84 | 18/4/78 | 17/61/8 | 41 | 21 | 47/10/7 | 90.8 |
| mui | skill | full | 4 | 15/4/81 | 15/9/76 | 12/50/10 | 37 | 14 | 15/1/5 | 93.6 |
| naming-analyzer | skill | full | 3 | 0/0/99 | 0/3/97 | 7/10/4 | 4 | 36 | 27/2/2 | 96.0 |
| openapi-to-typescript | skill | full | 7 | 1/1/98 | 1/1/98 | 0/8/12 | 0 | 13 | 22/2/0 | 96.8 |
| perplexity | skill | full | 17 | 64/12/24 | 50/8/42 | 0/0/7 | 28 | 8 | 10/2/2 | 89.2 (accepted by the user) |
| plugin-forge | skill | full | 10 | 1/1/98 | 1/1/98 | 0/16/21 | 6 | 12 | 43/10/4 | 91.2 |
| pr-diagrams | skill | facts-only | 19 | n/a | n/a | 0/0/0 | 11 | 15 | 17/6/9 | 94.0 |
| professional-communication | skill | full | 8 | 14/3/83 | 17/3/80 | 21/48/7 | 6 | 8 | 5/3/2 | 84.8 (accepted by the user) |
| qa-test-planner | skill | full | 3 | 0/0/99 | 2/1/97 | 31/35/11 | 14 | 8 | 8/0/8 | 95.6 |
| react-dev | skill | full | 6 | 1/1/98 | 1/1/98 | 4/82/19 | 3 | 31 | 43/0/4 | 96.0 |
| react-useeffect | skill | full | 17 | 2/1/97 | 2/1/97 | 3/1/0 | 7 | 13 | 19/0/1 | 90.0 |
| reducing-entropy | skill | full | 10 | 13/4/82 | 15/6/79 | 10/11/4 | 0 | 7 | 18/2/1 | 91.2 |
| requirements-clarity | skill | full | 7 | 0/0/100 | 0/0/99 | 4/8/8 | 1 | 3 | 2/1/2 | 96.0 |
| session-handoff | skill | full | 16 | 15/2/83 | 15/2/83 | 0/4/4 | 9 | 7 | 9/3/1 | 94.8 |
| ship-learn-next | skill | full | 12 | 39/4/57 | 36/6/58 | 2/8/6 | 6 | 4 | 5/0/2 | 95.2 |
| skill-judge | skill | full | 14 | 1/3/96 | 2/5/93 | 17/3/10 | 7 | 9 | 17/2/8 | 99.2 |
| skill-updater | skill | facts-only | 19 | n/a | n/a | 0/0/0 | 6 | 4 | 22/0/1 | 94.0 |
| sync-branch | command | full | 18 | 2/0/98 | 2/0/98 | 0/0/0 | 1 | 9 | 21/1/0 | 95.6 |
| sync-skills-readme | command | full | 13 | 10/1/89 | 10/1/89 | 0/0/1 | 1 | 4 | 7/1/1 | 96.0 |
| ui-ux-designer | agent | full | 1,22 | 3/0/96 | 4/0/95 | 8/4/8 | 1 | 10 | 6/4/5 | 95.6 |
| ui-ux-principles | skill | facts-only | 20 | n/a | n/a | 0/0/0 | 27 | 44 | 49/11/6 | 92.4 |
| viral-tweet | command | full | 2 | 1/0/99 | 2/0/98 | 5/1/4 | 2 | 4 | 4/2/4 | 92.0 |
| web-to-markdown | skill | full | 16 | 66/2/32 | 58/2/40 | 1/0/6 | 18 | 6 | 16/2/3 | 88.8 (accepted by the user) |
| writing-clearly-and-concisely | skill | full | 18 | 96/0/4 | 96/0/4 | 0/8/6 | 2 | 4 | 14/1/3 | 94.4 |

Totals: 60 artifacts, 349 restored, 788 dropped, 456 intended-change section and file decisions, 794 paragraph-level rows, 602 registry rows added, facts 1020 verified, 167 corrected, 201 pointer, 21 reported.

Notes: ui-ux-designer is in batches 1 and 22 (batch 22 applied the accepted purpose change); dependency-updater in batches 14 and 23 (batch 23 restored auto-apply). datadog-cli and gepetto are synced from upstream and report-only: nothing was edited, their stale facts are in `docs/audit/upstream-findings.md`. web-to-markdown (88.8), perplexity (89.2) and compose-email (86.8) hold grades under 90 that the user accepted in the PR forms; professional-communication and codex were accepted at 84.8 in the PR 2 form.
