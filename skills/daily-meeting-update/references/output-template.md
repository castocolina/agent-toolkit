# Output template

Read this when writing the update (SKILL.md step 4). It fixes the layout of the PRs & Reviews section and the Links footer, and gives a fill-in template and one filled example. The step 3 gates still decide what goes where.

## Where each PR goes

| What the evidence shows | Where it goes |
|---|---|
| Merged PR, `mergedAt` inside the window | Yesterday (`merged PR #N - title`) and `**Merged:**` |
| PR still open or draft, whatever the session or the user says | never Yesterday; `**Opened:**` (with its state) only under the window rule in the next row; Today when the user continues it |
| PR you opened inside the window (`createdAt` in [`START`, `END`)) | `**Opened:**`, when `createdAt` from `gh pr view` falls in the window or the user says so; ask only when neither is known |
| Your review with `submittedAt` inside the window | `**Reviews:**` with its outcome |
| Review submitted at or after `END` | left out, like any later event |
| Closed PR, not merged | say it was closed unmerged; never as delivered |

An open PR is activity, not an outcome, so it never appears under Yesterday. When the user says the work is finished while its PR is still open, that is the step 3 contradiction: name it and ask.

## Review outcomes

Write the outcome from the review's `state`: `APPROVED` as approved, `CHANGES_REQUESTED` as changes requested, `COMMENTED` as commented. Several reviews of one PR in the window: the latest one.

## Fill-in template

Drop every line and section that has no approved data behind it; `## Blockers` and `## Topics for Discussion` always stay.

```markdown
# Daily Update - YYYY-MM-DD

## Yesterday
- <work item> (merged PR #N - <title>)

## Today
- <plan> (PR #N - <title>, open)

## Blockers
- No blockers

## PRs & Reviews
- **Opened:** PR #N - <title> (open or draft)
- **Merged:** PR #N - <title>
- **Reviews:** PR #N - <title> (approved, changes requested or commented)

## Jira
- KEY-N - <title> (<status>)

## Topics for Discussion
- None

---
*Links:*
- <URL of every PR or ticket named above, only when known>
```

Several PRs on one line are separated by `;`, each keeping its title. The date is the meeting date, today, not the window.

## Filled example

User answers: finished the login timeout fix, researched payment providers, continues the OAuth work today, no blockers, wants to discuss the payments module. Approved data: PR #120 merged in the window, PR #125 opened in the window and still open, a review of PR #123 approved and one of PR #456 with changes requested, both inside the window.

```markdown
# Daily Update - 2026-01-22

## Yesterday
- Fixed login timeout (merged PR #120 - fix: login timeout)
- Researched payment providers

## Today
- Continue OAuth flow (PR #125 - feat: add OAuth flow, open)

## Blockers
- No blockers

## PRs & Reviews
- **Opened:** PR #125 - feat: add OAuth flow (open)
- **Merged:** PR #120 - fix: login timeout
- **Reviews:** PR #123 - fix: cache invalidation (approved); PR #456 - feat: export CSV (changes requested)

## Topics for Discussion
- Architecture of the new payments module

---
*Links:*
- https://github.com/org/repo/pull/125
- https://github.com/org/repo/pull/120
- https://github.com/org/repo/pull/123
- https://github.com/org/repo/pull/456
```

PR #125 appears under Today and Opened, not under Yesterday, because it is open.
