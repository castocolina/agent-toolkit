# Batch 84

## viral-tweet (command)

### viral-tweet#D8-1
- severity: medium
- dimension: D8
- location: commands/viral-tweet.md:17
- fix: Resolve what happens when the user asks for replies or reposts on a sensitive post. Step 3 forbids any question or call to action there. Add: 'For sensitive posts, clarity overrides a stated objective; say so in ANALYSIS and offer a question only if the user confirms.'

### viral-tweet#D8-2
- severity: medium
- dimension: D8
- location: commands/viral-tweet.md:48
- fix: Step 4 can return three alternative threads, one per VERSION, but the Output template has no place for them. Add: 'When step 4 returns three threads, each VERSION block holds its thread as numbered posts with per-post weighted counts, and the THREAD section is omitted.'

### viral-tweet#D1-1
- severity: low
- dimension: D1
- location: commands/viral-tweet.md:36
- fix: Cut the generic social-media hygiene the model already follows. Keep only the non-obvious part: keep a link only when it backs up the claim, and count it as 23.

### viral-tweet#D2-1
- severity: medium
- dimension: D2
- location: commands/viral-tweet.md:17
- fix: Move the objective check from step 2, which runs before any variant exists, into step 5 ('Recommend one'). Step 2 then only picks the objective, and step 5 checks the candidate, revises it and recommends.

### viral-tweet#D3-1
- severity: low
- dimension: D3
- location: commands/viral-tweet.md:29
- fix: Add platform-specific gotchas taken from observed failures. For example, a link in a standalone post turns into a card that pushes the text down. Another: a thread's first post must stand alone, because readers often see only that post.

### viral-tweet#D6-1
- severity: low
- dimension: D6
- location: commands/viral-tweet.md:20
- fix: Give one default with an escape hatch: 'trim to at least 15 under the limit; only if trimming would drop a supplied fact or qualifier, keep it and tell the user to confirm the count in X's composer.'
