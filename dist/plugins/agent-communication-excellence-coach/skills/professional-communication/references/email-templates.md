# Email patterns

Adapt these patterns to the facts provided. Preserve unknowns explicitly; do not invent metrics, deadlines, causes, commitments, or urgency.

## Status

```text
Subject: [Project]: [period] update

Status: [verified state]
Completed: [facts and evidence/source]
Next: [owner and date, if known]
Risk/blocker: [impact, mitigation, decision needed]
Unknowns: [what is not yet known]
```

## Escalation

```text
Subject: Decision needed: [impact]

Impact: [verified user/business effect]
Current mitigation: [what is being done]
Unknowns: [cause/extent not yet confirmed]
Decision needed: [one decision and owner] by [explicit time/time zone if supplied]
Evidence: [access-controlled source]
```

## Decision request

```text
Subject: Decision needed: [choice]

Context and constraints: [facts]
Options: [material trade-offs]
Recommendation: [if supported, with rationale]
Decision owner: [name/role]
Needed by: [date/time/time zone, or mark unspecified]
```

## Review or feedback request

```text
Subject: Review request: [document/PR/design name]

Hi [name],

I would appreciate your feedback on [document/PR/design].

What it is: [one-line description]
Link: [URL]
Feedback wanted: [specific areas, for example correctness of the migration plan]
Timeline: [date/time/time zone if supplied; otherwise "no deadline set" or ask]
Optional: [offer to walk through it together]

[Name]
```

State "no rush" only when the sender said so; otherwise leave the timeline unspecified rather than inventing a deadline.

## Meeting request

```text
Subject: Meeting request: [topic] ([proposed time range, if any])

Hi [name],

I would like to meet to discuss [topic].

Purpose and decision: [what the meeting must settle, and who decides]
Duration: [proposed length]
Proposed times: [options with time zone, or "share your availability"]
Preparation: [none, or the pre-read]
Optional: [offer to take a slot from my calendar]

[Name]
```

Offer a meeting only when the decision or interaction cannot be settled asynchronously (see `remote-async-communication.md`, Meeting decision rule). Mark proposed times and length "Proposed:" until the recipient confirms.

## Introducing yourself to a new team

```text
Subject: Introduction: [your name], [your role]

Hi team,

I am [name], joining as [role] starting [date, if known].

Background: [relevant experience; what you will work on first, if known]
Looking forward to: [something specific about the team or project]
How to reach me: [chat handle; preferred channel]

[Optional: offer a short intro chat]

[Name]
```

## Asking for help

```text
Subject: Question: [specific topic]

Hi [name],

I am working on [task/feature] and need your expertise on [specific area].

What I am trying to do: [goal]
What I have tried: [approach and result, for each]
Where I am stuck: [the specific question or blocker]
Context: [link to code or doc; error message, with secrets redacted]
Timeline: [when you need an answer, if known]

[Name]
```

In chat, send the same fields as one self-contained message: the error, what was already checked, and one direct question. Name the person who can help; do not invent urgency.

## Retrospective summary

```text
Subject: [Team/sprint] retrospective summary

Hi team,

Thanks for joining the retrospective. Summary:

Went well: [items from the session]
Could improve: [items from the session]
Actions: [owner]: [action], due [date] (Proposed: until the owner confirms)
Follow-up: [Proposed: revisit these at the next retrospective on [date], if one is scheduled]

[Name]
```

Use only what was said in the session; do not add items, owners, or dates the notes do not contain.

Use an informative subject that names the project and requested action/decision. For formal or external records, use email; otherwise choose the lightest channel the recipient checks daily. When a request is also an escalation, lead with impact and end with the single decision needed.
