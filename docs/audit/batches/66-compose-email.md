# Batch 66

## compose-email (command)

### compose-email#D8-1
- severity: medium
- dimension: D8
- location: commands/compose-email.md:17
- fix: Say what to ask in the nothing-known branch: 'If nothing at all is known, ask in one question for the topic or facts, the recipient and the desired outcome, then stop.' The eval empty-request-asks-for-facts expects all three, but 'ask only for blocking gaps' points to asking for the topic alone.

### compose-email#D8-1
- severity: medium
- dimension: D8
- location: commands/compose-email.md:32
- fix: Add a disclosure fallback before drafting: when permission or recipient access is unknown, omit internal links and sensitive details, use a safe summary or an explicit placeholder, and identify anything withheld. Treat disclosure confirmation as a blocking question when a safe draft is impossible, and exempt deliberate redactions from the every-source-fact validation rule.

### compose-email#D1-1
- severity: medium
- dimension: D1
- location: commands/compose-email.md:23
- fix: Shorten this audience bullet to the one rule the model misses without help (leadership: decision in the first sentence, at most 5 sentences). Cut the peer and manager clauses, because they are standard business-writing advice the model already follows.

### compose-email#D2-1
- severity: low
- dimension: D2
- location: commands/compose-email.md:24
- fix: Keep the step but replace the generic framework name with the domain ordering it stands for (ask or impact first, then reason, then next action and owner). That way the step adds a sequence and does not only restate a well-known framework.

### compose-email#D3-1
- severity: low
- dimension: D3
- location: commands/compose-email.md:33
- fix: Delete this gotcha: steps 1 and 4 already state it and the model knows it. Replace it with a hard-won one, for example: NEVER put the ask only in the subject line, because many clients truncate subjects on mobile and the reader misses it.

### compose-email#D1-1
- severity: medium
- dimension: D1
- location: commands/compose-email.md:19
- fix: Condense the routine request/status guidance into one rule: "Lead with the decision or recipient impact; include the context needed to act, and do not invent an ask for an FYI." Retain the more distinctive scope trade-offs, missing-thread fallback, uncertainty preservation and proposed-deadline safeguards.
