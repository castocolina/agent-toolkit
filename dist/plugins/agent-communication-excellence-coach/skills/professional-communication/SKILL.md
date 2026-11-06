---
name: professional-communication
description: Draft and improve software-team emails, Slack/Teams messages, stakeholder updates, meeting agendas, and decision/action summaries. Use when translating technical work for non-technical audiences, making an async request actionable, or structuring a project update. Not for performance-review coaching, sales copy, legal documents, or scheduling meetings.
allowed-tools: Read Glob Grep
---

# Professional Communication

## Route by goal

- **Request:** state the decision/action needed, accountable recipient, deadline with timezone, and consequence of delay. If no deadline was supplied, ask or leave it unspecified; do not invent urgency.
- **Escalation:** lead with user/business impact, current mitigation, decision/authority needed, and the time it is needed. Route urgent incidents through the team's monitored incident channel, not an assumed-to-be-monitored chat.
- **FYI:** name affected audience, what changed, effective time, and whether any action is required.
- **Meeting:** schedule only when a decision or interaction cannot be resolved asynchronously. Include decision owner, pre-read, options, and desired outcome.
- **Status update:** separate verified progress, risks/blockers, decisions needed, and next owner/date. Preserve uncertainty; do not turn an implementation detail into an unsupported metric or business claim.

Default to the lightest channel the recipient reads daily; use email for external or formal records. Use the monitored incident path only for actual operational incidents or cases meeting the team's documented incident criteria. For urgent non-incident decisions, use the recipient's agreed acknowledgement/escalation channel and put supporting detail in a durable record. A Slack thread may not notify the full channel; summarize decisions and actions back to the channel when channel-wide awareness matters. For a request that is also an escalation, lead with impact and end with the single decision needed.

## Audience and accuracy checks

Before drafting, identify recipient, desired outcome, sensitivity, and facts supplied. Translate jargon only as far as the audience needs, preserving technical meaning and uncertainty. Keep unknown dates, measurements, ownership, and commitments marked as unknown or ask a targeted question. Do not invent performance improvements, causal claims, or approval.

## Gotchas

- “EOD” is ambiguous across time zones; use an explicit date, time, and zone or ask which zone applies.
- Never send incident urgency through an unmonitored channel; identify the team's actual on-call/escalation path.
- Do not paste credentials, customer data, or sensitive logs into broad channels. Redact and link to access-controlled evidence.
- **Evidence trap:** a status number without its source and time window can be repeated upstream as a business metric; cite provenance or omit it.

When a fact is unknown (cause, date, owner), say it is unknown and do not promise a future update, date, or named person that the request did not supply; label any proposed next step or owner “Proposed:”. For a meeting objective, name the decision and its owner by the role the request gives (for example the product and engineering leads), marked proposed if no person is named.

## Load by deliverable

- Before sending email: `references/email-templates.md` (verify subject, owner, ask, evidence, and unknowns).
- Before a meeting: `references/meeting-structures.md` (verify decision need, capacity, owner, and follow-through).
- Before translating technical work: `references/jargon-simplification.md` (separate observed results from intended benefits).
- Before choosing a channel or coordinating across time zones: `references/remote-async-communication.md` (verify monitoring, consent, and escalation route).

For difficult feedback, use `feedback-mastery` rather than treating it as ordinary status communication.
