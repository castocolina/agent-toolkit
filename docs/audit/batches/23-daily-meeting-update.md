# Batch 23

## daily-meeting-update (skill)

### daily-meeting-update#D7-1
- severity: low
- dimension: D7
- location: skills/daily-meeting-update/evals/evals.json:1
- fix: Add an approved-integration case with scoped activity fixtures. Assert from the tool trace that authentication/history access occurs only after approval, only approved scope or sessions are used, duplicate work is merged, and raw session text is not exposed.

### daily-meeting-update#D8-1
- severity: medium
- dimension: D8
- location: skills/daily-meeting-update/scripts/claude_digest.py:257
- fix: Preserve cwd and branch on individual messages, filter by the requested day first, and derive metadata from those filtered messages. Split or explicitly represent sessions that change project or branch.

### daily-meeting-update#D8-2
- severity: medium
- dimension: D8
- location: skills/daily-meeting-update/scripts/claude_digest.py:220
- fix: Convert each timestamp with the system's date-aware local conversion, such as timestamp.astimezone() without the captured fixed-offset argument, or use an explicit ZoneInfo timezone. Add deterministic tests on both sides of a DST transition.

### daily-meeting-update#D8-1
- severity: medium
- dimension: D8
- location: skills/daily-meeting-update/SKILL.md:22
- fix: Add: if the digest reports zero sessions, say so once and continue with the interview

### daily-meeting-update#D1-1
- severity: medium
- dimension: D1
- location: skills/daily-meeting-update/SKILL.md:33
- fix: Compress the standard questions and output headings into a compact contract. Retain the higher-value consent ordering, day filtering, unresolved-path handling, privacy safeguards, and cross-source deduplication.

### daily-meeting-update#D2-1
- severity: medium
- dimension: D2
- location: skills/daily-meeting-update/SKILL.md:38
- fix: Add a provenance gate before drafting: require user confirmation or explicit completion evidence for outcome claims; treat read/edit/command counts as activity only, and ask for confirmation before promoting them to completed work.

### daily-meeting-update#D1-1
- severity: low
- dimension: D1
- location: skills/daily-meeting-update/SKILL.md:29
- fix: Compress the four interview questions into a single line and keep only the expert rules (grouping, outcome-vs-investigation distinction)

### daily-meeting-update#D2-1
- severity: low
- dimension: D2
- location: skills/daily-meeting-update/SKILL.md:38
- fix: Add: if approved activity contradicts an answer (e.g. user says no blockers but commits suggest stalled work), surface the discrepancy and ask before including it

### daily-meeting-update#D3-1
- severity: low
- dimension: D3
- location: skills/daily-meeting-update/SKILL.md:73
- fix: Append a one-clause reason to each item (e.g. investigations reported as done inflate status and mislead sprint tracking)

### daily-meeting-update#D6-1
- severity: low
- dimension: D6
- location: skills/daily-meeting-update/SKILL.md:22
- fix: State: always run claude_digest.py with --format json and render the summary yourself
