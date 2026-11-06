# Batch 74

## viral-tweet (command)

### viral-tweet#D8-1
- severity: medium
- dimension: D8
- location: commands/viral-tweet.md:19
- fix: State that the one-liner only replaces scheme-prefixed URLs. A bare domain such as example.com/launch is also auto-linked by X and counts as 23. Tell the agent to add https:// to every link before counting, or extend the regex to catch bare domains, so drafts with short bare links are not undercounted.

### viral-tweet#D8-1
- severity: high
- dimension: D8
- location: commands/viral-tweet.md:19
- fix: Replace the regex and ordinal-sum counter with a twitter-text-compatible validator that handles URL boundaries, normalization and emoji sequences, such as twitter-text's parseTweet(text).weightedLength. Recount after each revision against the applicable ceiling; retain a conservative margin and label counts approximate when an accurate validator is unavailable.

### viral-tweet#D1-1
- severity: low
- dimension: D1
- location: commands/viral-tweet.md:36
- fix: Shorten the generic social-media hygiene items (hashtag stacks, ragebait) to one line each or merge them. Current models already avoid these. Keep the space for the non-obvious items such as the weighted counting, compression falsifying claims and fancy-text cost.

### viral-tweet#D2-1
- severity: medium
- dimension: D2
- location: commands/viral-tweet.md:18
- fix: Give lever (b) the same concrete technique that (a) and (c) have. For example: end with one specific question the author genuinely wants answered, tied to the supplied facts, never a generic 'thoughts?'. Then the agent can tell a reply-led draft apart from the engagement bait banned in NEVER.

### viral-tweet#D3-1
- severity: low
- dimension: D3
- location: commands/viral-tweet.md:52
- fix: Add a Gotcha that the '1/n ' prefix and any thread emoji count toward each post's 280-character weighted limit. Tell the agent to count the post with the prefix included, so a thread post that fits without the prefix does not end up over the limit.

### viral-tweet#D1-1
- severity: medium
- dimension: D1
- location: commands/viral-tweet.md:35
- fix: Condense familiar tone, engagement-bait and curiosity-gap reminders into a brief activation checklist while retaining their reasons. Replace repetition with a compact worked transformation demonstrating how to change a hook without losing scope, baseline or causal meaning.

### viral-tweet#D2-1
- severity: medium
- dimension: D2
- location: commands/viral-tweet.md:17
- fix: Add an objective-based comparison before recommending: for dwell, require a concrete observation and a complete lesson or story payoff without withholding information; for clarity, prefer the quiet variant with the least ambiguity or emotional spin. Use these checks to select or revise a candidate rather than relying on its hook/reply/repost label.
