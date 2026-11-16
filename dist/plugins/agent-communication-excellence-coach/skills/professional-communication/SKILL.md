---
name: professional-communication
description: "Draft and improve software-team emails, Slack/Teams messages, stakeholder status updates, escalations, review or help requests, meeting agendas (standup, sprint planning, retrospective, 1:1, design or code review), meeting summaries and team communication norms. Use when translating technical work for non-technical audiences without inventing metrics, making an async request actionable, choosing a channel across time zones, or structuring a project update, even if the user only says 'make this clearer' or 'tell the execs'. Not for performance-review coaching or difficult feedback (feedback-mastery), sales copy, legal documents, sentence-level style edits (writing-clearly-and-concisely), or actually scheduling meetings."
allowed-tools: Read Glob Grep
---

# Professional Communication

## Procedure

1. List the facts supplied and the unknowns (see Audience and accuracy checks).
2. Pick the route by goal (see Route by goal).
3. Pick the channel (see Channel).
4. Load the matching reference (see Load by deliverable).
5. Draft with What-Why-How, or the escalation order for an escalation (see Frame: What-Why-How).
6. Run the Final check (see Frame: What-Why-How).

## Frame: What-Why-How

Organize any message as **What** (the topic, request, or decision), **Why** (the reasoning or evidence), and **How** (next steps, owner, deadline). Example with facts the request supplied: What: "We need to delay the release by one week"; Why: "A critical bug was found in payment processing"; How: "QA retests Thursday; I update stakeholders Friday." Three golden rules: a clear subject or purpose, scannable formatting (bullets, headlines), and the key message first.

Precedence: What-Why-How is the default order. For an escalation, lead with impact (Why), then the decision needed (What), then mitigation and owner (How), matching the Escalation route below.

Final check: before returning a draft, check every date, number, owner and promise against the facts supplied, and mark anything else `Proposed:` or unknown (decision rule: Audience and accuracy checks).

## Route by goal

- **Request:** state the decision/action needed, accountable recipient, deadline with timezone, and consequence of delay. If no deadline was supplied, ask or leave it unspecified; do not invent urgency.
- **Escalation:** lead with user/business impact, current mitigation, decision/authority needed, and the time it is needed. Route urgent incidents through the team's monitored incident channel, not an assumed-to-be-monitored chat.
- **FYI:** name affected audience, what changed, effective time, and whether any action is required.
- **Meeting:** schedule only when a decision or interaction cannot be resolved asynchronously. Include decision owner, pre-read, options, and desired outcome.
- **Status update:** separate verified progress, risks/blockers, decisions needed, and next owner/date. Preserve uncertainty; do not turn an implementation detail into an unsupported metric or business claim.

## Channel

Pick the channel in this order: incident (the monitored incident path), then formal or external (email), then a document (durable record), then chat. Default to the lightest channel the recipient reads daily; use email for external or formal records. Use the monitored incident path only for actual operational incidents or cases meeting the team's documented incident criteria. For urgent non-incident decisions, use the recipient's agreed acknowledgement/escalation channel and put supporting detail in a durable record. A Slack thread may not notify the full channel; summarize decisions and actions back to the channel when channel-wide awareness matters. For a request that is also an escalation, lead with impact and end with the single decision needed.

## Audience and accuracy checks

Before drafting, identify recipient, desired outcome, sensitivity, and facts supplied. Translate jargon only as far as the audience needs, preserving technical meaning and uncertainty. Keep unknown dates, measurements, ownership, and commitments marked as unknown or ask a targeted question. Do not invent performance improvements, causal claims, or approval.

Decision rule for unknown facts: ask a targeted question when the missing fact blocks the message (the recipient, the ask itself). Otherwise draft with the fact marked unknown, or as `Proposed:` when you suggest a value. Do not claim an activity, a fix in progress or an investigation, and do not promise an update, date or named person, unless the request supplied it (an update promise is allowed only when marked `Proposed:`). Strike sentences that are promises in disguise ("we will share it once confirmed", "we won't give a date until we can stand behind it"), severity words the request did not use ("critical"), impact lines it did not supply ("no action needed", "everything keeps working"), and any deadline you made up: leave a placeholder such as `[date, time, time zone]` and ask for the value.

## Gotchas

- “EOD” is ambiguous across time zones; use an explicit date, time, and zone or ask which zone applies.
- Never send incident urgency through an unmonitored channel; identify the team's actual on-call/escalation path. A post in a general channel at night can sit unread while the on-call pager stays silent.
- Do not paste credentials, customer data, or sensitive logs into broad channels. Redact and link to access-controlled evidence. A broad channel decides who can read and retain the content, and you cannot recall it.
- Do not forward an internal thread to an external stakeholder as is: the earlier internal discussion sits below the new message and is exposed. Write a fresh message with the relevant facts instead.
- **Evidence trap:** a status number without its source and time window can be repeated upstream as a business metric; cite provenance or omit it.

When a fact is unknown (cause, date, owner), say it is unknown and do not promise a future update, date, or named person that the request did not supply; label any proposed next step or owner “Proposed:”. For a meeting objective, name the decision and its owner by the role the request gives (for example the product and engineering leads), marked proposed if no person is named. The decision rule for unknown facts is in Audience and accuracy checks.

## Load by deliverable

- Before sending email, or when asked for a review request, meeting request, new-team introduction, request for help, or retrospective summary email: `references/email-templates.md` (verify subject, owner, ask, evidence, and unknowns).
- Before a meeting, or when asked for a standup, retrospective (phases, Start/Stop/Continue, 4Ls, Mad/Sad/Glad), 1:1, code review walkthrough, or meeting summary: `references/meeting-structures.md` (verify decision need, capacity, owner, and follow-through); use the reference's five phase names and its "typical, adapt" minutes framing verbatim (Derby and Larsen, Agile Retrospectives), including Close the Retrospective, never shortened to Close.
- Before translating technical work, or when asked for the plain-language version of a common technical phrase: `references/jargon-simplification.md` (separate observed results from intended benefits).
- Before choosing a channel, coordinating across time zones, deciding whether a meeting is needed (write first, collect async feedback, then decide), or drafting team communication norms: `references/remote-async-communication.md` (verify monitoring, consent, and escalation route).

For difficult feedback, use `feedback-mastery` rather than treating it as ordinary status communication.
