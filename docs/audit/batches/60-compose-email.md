# Batch 60

## compose-email (command)

### compose-email#D1-1
- severity: high
- dimension: D1
- location: commands/compose-email.md:65
- fix: Condense standard subject-line, paragraph, and formatting advice into a short activation checklist. Replace the repetition with developer-specific communication decisions, such as separating committed dates from proposed dates and presenting scope-versus-deadline trade-offs in extension requests.

### compose-email#D7-1
- severity: high
- dimension: D7
- location: commands/compose-email.md
- fix: Add commands/evals/compose-email.json with at least three realistic scenarios and verifiable assertions: a fully specified approval request, an empty or substantively insufficient request that must elicit missing facts, and a minimal existing-draft rewrite that preserves facts and requested brevity.

### compose-email#D8-1
- severity: medium
- dimension: D8
- location: commands/compose-email.md:19
- fix: Ask for the message's topic, known facts or source draft, and desired outcome before drafting. Reuse information already supplied, ask only blocking follow-up questions, and use explicit placeholders for nonblocking unknowns rather than inventing facts. If AskUserQuestion is unavailable, ask the same questions in plain text.

### compose-email#D8-2
- severity: medium
- dimension: D8
- location: commands/compose-email.md:120
- fix: Replace all three example invocations with /command-compose-email:compose-email for the packaged plugin, or /compose-email when explicitly demonstrating project-local installation.

### compose-email#D2-1
- severity: medium
- dimension: D2
- location: commands/compose-email.md:44
- fix: Add a compact purpose-to-strategy checkpoint: requests identify the smallest decision, decision owner, and needed-by time; escalations distinguish observed impact, uncertainty, and mitigation; FYIs identify what changes for the recipient and whether a response is needed.

### compose-email#D3-1
- severity: medium
- dimension: D3
- location: commands/compose-email.md:137
- fix: Add specific prohibitions with reasons: never present a proposed delivery date as a commitment without confirmation, because recipients may treat it as an agreed deadline; never copy internal logs or incident links into external messages without checking disclosure and accessibility, because they can expose sensitive details or leave recipients unable to act.

### compose-email#D4-1
- severity: medium
- dimension: D4
- location: commands/compose-email.md:2
- fix: Draft or refine professional emails to technical peers, stakeholders, managers, and leadership using What-Why-How. Use for status updates, approval requests, escalations, follow-ups, or rewriting an existing draft for clearer tone and structure, even when the user only asks to make a message shorter or less defensive. Produce a subject and email body; do not send messages.

### compose-email#D6-1
- severity: medium
- dimension: D6
- location: commands/compose-email.md:134
- fix: Make What-Why-How an internal organizing default rather than mandatory visible labels. Default to a ready-to-paste email that preserves supplied voice, length, and formatting constraints; show framework labels or a subject rationale only when requested or useful for coaching.
