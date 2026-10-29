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
