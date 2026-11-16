# Batch 62

## communication-excellence-coach (agent)

### communication-excellence-coach#D1-1
- severity: high
- dimension: D1
- location: agents/communication-excellence-coach.md:189
- fix: Delete the generic email checklist and repeated capability descriptions; replace framework primers with concise, non-obvious coaching decisions grounded in actual failure cases. Preserve the agent-specific constraints and output requirements.

### communication-excellence-coach#D3-1
- severity: high
- dimension: D3
- location: agents/communication-excellence-coach.md:197
- fix: Add specific coaching prohibitions with explanations: never remove hedging that communicates genuine uncertainty merely to sound confident; never turn inferred motives into SBI Behavior, because that converts observable feedback into an accusation; never polish away an explicit safety or escalation concern for the sake of friendliness.

### communication-excellence-coach#D5-1
- severity: high
- dimension: D5
- location: agents/communication-excellence-coach.md:100
- fix: Move the long output templates into a communication-coaching skill and preload it through skills:. Keep routing, constraints, concise output requirements, and the core coaching workflow in an agent file of 200 lines or fewer.

### communication-excellence-coach#D7-1
- severity: medium
- dimension: D7
- location: agents/communication-excellence-coach.md:78
- fix: Add: 'A review is done after the applicable Markdown template contains the requested analysis and actionable suggestions; a roleplay is done after the agreed number of exchanges (default three), or when the user asks to stop, followed by the Coach Feedback template.'

### communication-excellence-coach#D8-1
- severity: medium
- dimension: D8
- location: agents/communication-excellence-coach.md:82
- fix: Add an intake branch: require the actual draft or outline for specific review, and the counterpart plus conversation goal for roleplay. If a required input is missing, ask a targeted clarification instead of inventing it; if the user cannot share source text, offer a clearly labeled generic checklist. State assumptions and proceed only when optional context is missing.

### communication-excellence-coach#D2-1
- severity: medium
- dimension: D2
- location: agents/communication-excellence-coach.md:77
- fix: Define a rehearsal procedure: identify a recipient concern tied to the user's goal, introduce it through an in-character objection, assess whether the reply resolves that concern without abandoning the intended request, and use the diagnosis to select the next practice scenario.

### communication-excellence-coach#D4-1
- severity: low
- dimension: D4
- location: agents/communication-excellence-coach.md:3
- fix: Review existing professional or technical communication drafts for clarity, tone, audience fit, and risk; provide suggested edits, presentation feedback, and difficult-conversation roleplay. Use before sending an email or Slack message, presenting an architecture review, or delivering feedback, including requests such as 'does this sound too harsh?' Suggestions and practice only; not for writing from scratch, sending messages, code review, or legal/compliance review.

## viral-tweet (command)

### viral-tweet#D1-1
- severity: high
- dimension: D1
- location: commands/viral-tweet.md:43
- fix: Condense the familiar engagement-signal definitions, hook tactics and sentence-style advice into brief activation cues. Retain substantive space for verified X-specific trade-offs, concrete failure cases and corrective choices that general copywriting knowledge would not supply.

### viral-tweet#D7-1
- severity: high
- dimension: D7
- location: commands/evals/viral-tweet.json
- fix: Add commands/evals/viral-tweet.json with at least three realistic scenarios and verifiable assertions: a supplied launch idea yielding three distinct rewrites and a recommendation; empty arguments yielding a clarification request without invented drafts; and a long or emotionally sensitive draft yielding appropriately bounded, voice-preserving posts.

### viral-tweet#D8-1
- severity: high
- dimension: D8
- location: commands/viral-tweet.md:131
- fix: Replace the example with a rewrite using only the supplied launch and six-month development facts. Add a factual-grounding check before recommending a version: preserve supplied facts and ask for confirmation of proposed numbers, actions or dramatic events instead of inventing them.

### viral-tweet#D8-2
- severity: medium
- dimension: D8
- location: commands/viral-tweet.md:98
- fix: Add an ordered validation phase: draft, check each version against X's standard 280-weighted-character limit unless the user specifies an extended-post allowance, shorten, and recheck. If essential content cannot fit, ask whether to use a thread rather than silently returning an over-limit standalone tweet.

### viral-tweet#D2-1
- severity: medium
- dimension: D2
- location: commands/viral-tweet.md:40
- fix: Add a diagnostic procedure: identify the intended reader and their payoff, choose one primary engagement objective, identify the strongest supported angle, and apply only tactics that reinforce that objective. Explain when a substantive discussion prompt should take precedence over a self-contained, repostable statement, and vice versa.

### viral-tweet#D3-1
- severity: medium
- dimension: D3
- location: commands/viral-tweet.md:81
- fix: Replace subjective labels with observable failure signatures and reasons. Show the difference between a substantive discussion question and reply bait, explain why an unanswered curiosity hook disappoints readers, and distinguish irrelevant promotional links or mentions from links needed to substantiate the post.

### viral-tweet#D4-1
- severity: low
- dimension: D4
- location: commands/viral-tweet.md:2
- fix: Rewrite tweet ideas and drafts into three X/Twitter post variants, explain their engagement trade-offs, and recommend one. Use when asked to sharpen a hook, improve reply or repost potential, or turn a launch idea into a tweet. Drafting and strategy only; not for publishing posts or managing an X account.

### viral-tweet#D6-1
- severity: medium
- dimension: D6
- location: commands/viral-tweet.md:56
- fix: Treat high-arousal framing as a default, not a requirement. Preserve the author's emotional intent; for grief, calm reflection or factual updates, prioritize relevance and clarity rather than forcing anger, FOMO or surprise.
