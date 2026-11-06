# Batch 51

## daily-meeting-update (skill)

### daily-meeting-update#D7-1
- severity: medium
- dimension: D7
- location: skills/daily-meeting-update/evals/evals.json
- fix: Add an eval in which the user says "no blockers" and "finished X" while gh-prs.json shows X's PR still open. Assert that the reply names both conflicts and asks about them instead of drafting silently. Add a Monday prompt that asserts the agent asks which day counts as yesterday before it queries.

### daily-meeting-update#D7-2
- severity: low
- dimension: D7
- location: skills/daily-meeting-update/evals/trigger-queries.json:2
- fix: Rewrite about half the queries with real context and casual wording, for example "standup in 10 min, did PAY-231 yday and reviewed dana's PR in acme/payments, help". Also replace weak negatives such as the career one-on-one with near-misses such as "turn my last 5 standup notes into a weekly summary for my manager".

### daily-meeting-update#D8-1
- severity: low
- dimension: D8
- location: skills/daily-meeting-update/SKILL.md:51
- fix: Say which date goes in the header, for example "`YYYY-MM-DD` = the meeting date (today), not `DATE`". That stops the agent from writing the activity date taken from the Step 2 queries.

### daily-meeting-update#D8-1
- severity: high
- dimension: D8
- location: skills/daily-meeting-update/SKILL.md:44
- fix: Require a project-specific successful resolution or user confirmation before treating a closed ticket as completed work. Preserve cancelled or duplicate tickets as triage outcomes, and ask when the status or resolution does not establish delivery.

### daily-meeting-update#D8-2
- severity: medium
- dimension: D8
- location: skills/daily-meeting-update/SKILL.md:23
- fix: Define the reporting interval and timezone before classifying activity. Treat updated-time searches as discovery only; verify completion and review events against that interval using mergedAt, review timestamps, or Jira transition/resolution timestamps. Ask when event timing is unavailable, and keep today's events out of Yesterday.

### daily-meeting-update#D8-3
- severity: medium
- dimension: D8
- location: skills/daily-meeting-update/scripts/claude_digest.py:187
- fix: Discover log directories belonging to the approved project subtree, including sessions launched from descendant directories, while retaining per-message cwd filtering and avoiding unrelated projects. Add a regression where the only session is stored under an encoded child-directory path and --project names its parent.

### daily-meeting-update#D7-1
- severity: low
- dimension: D7
- location: skills/daily-meeting-update/evals/trigger-queries.json:2
- fix: Give this positive query explicit daily-sync or yesterday/today context, and add an otherwise similar weekly-meeting or agenda request labelled false so the pair tests the intended routing boundary.

### daily-meeting-update#D1-1
- severity: low
- dimension: D1
- location: skills/daily-meeting-update/SKILL.md:42
- fix: Cut this generic interview advice down to the part the model would miss: "Ask for topics even when tools found plenty: no tool can detect them." Keep the gates that follow it.

### daily-meeting-update#D2-1
- severity: low
- dimension: D2
- location: skills/daily-meeting-update/SKILL.md:51
- fix: Replace the prose layout with a short inline Markdown template: the H1 header, then the ## Yesterday, ## Today, ## Blockers, optional ## PRs & Reviews / ## Jira, and ## Topics for Discussion sections, each with an example bullet. Agents match a concrete template more reliably than a description of one.
