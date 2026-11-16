# Channel and async decisions

Default to the lightest channel the recipient checks daily. Use email for external or formal records; use a durable document for complex decisions or evidence; use chat for short coordination. If an urgent alert needs detail, alert through the team's actual monitored paging/on-call path and put the context in a durable record.

| Situation | Channel | Required detail |
|---|---|---|
| Short coordination | Team chat | Ask, owner, explicit response expectation |
| Decision with options/evidence | Document or tracked issue | Decision owner, options, trade-offs, source links, due time if known |
| External/formal record | Email | Clear subject, decision/action, verified facts |
| Incident urgency | Documented paging/on-call mechanism | Impact, mitigation, exact acknowledgement request |
| Sensitive feedback/conflict | Private conversation or appropriate HR/manager path | Consent, confidentiality, follow-up summary |

## Traps

- A status number without its source and time window can be repeated as a business metric. Cite provenance or omit it.
- “EOD” is ambiguous across time zones. State date, time, and zone only when known; otherwise ask or mark unspecified.
- A Slack thread may not notify everyone. When channel-wide awareness matters, post a concise decision/action summary in the channel.
- Record calls only when participants consent, policy permits it, access is restricted appropriately, and the subject is suitable. If any condition is unknown or sensitivity makes recording inappropriate, use a written decision/action summary instead.
- Do not assume `@here`, a call, or a particular channel is monitored. Verify the team's documented escalation chain and confirm acknowledgement; follow its fallback if no acknowledgement arrives.

## Meeting decision rule

Before scheduling a meeting:

1. **Write first:** draft the problem, context, and options in a document.
2. **Collect async feedback:** give reviewers a window, typically 24-48 hours; adapt it to time zones and the decision's deadline.
3. **Then decide:** if the question is still unresolved, schedule the meeting and send the document as the pre-read.

Many meetings are avoided when the organizer documents well enough that no discussion is needed. If the decision is urgent, use the documented escalation path instead of waiting out the window.

## Team norms template

Use when a team asks for written communication norms. The response times and hours below are example values, not standards: replace them with the team's agreed norms and do not present them as a vendor or industry rule.

```markdown
## Our communication norms

### Response times (example values; replace with the team's agreement)
- Chat direct message: within [4 working hours]
- Chat channel: within [24 hours]
- Email: within [48 hours]
- Document comments: before the stated deadline

### Urgent vs non-urgent
- Urgent operational issues: use the team's documented paging or escalation path, [link or name]
- Everything else: assume async

### Deep work protection
- No expectation of a reply during focus time (blocked on the calendar)
- "Do Not Disturb" is respected

### Time zones
- Core overlap hours: [HH:MM-HH:MM] [zone name, UTC offset]
- Meetings are scheduled inside the overlap hours
- Async is preferred outside the overlap
```

Write each zone as a name plus a UTC offset, or leave the placeholder, and never use "EOD" without a zone.
