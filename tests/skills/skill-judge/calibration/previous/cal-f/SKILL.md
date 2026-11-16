---
name: cal-f
description: Turn raw incident material (a chat export, an alert timeline, a deploy log, a pasted pager thread) into a blameless incident summary with a verified timeline, impact figures and follow-up owners. Use when asked to "write up the incident", "summarize the outage", "draft the postmortem", or to reconcile conflicting timestamps from several sources, even when the user only pastes a chat log and asks what happened. Returns the summary text and a list of unverified claims; it does not page anyone or edit tickets. Not for live incident response, root-cause analysis of code, or status-page announcements.
---

# Incident Summary

A reader who was not there needs a timeline they can trust, so every line carries its source and its clock. This skill writes text only: it never pages anyone and never edits a ticket.

## Workflow

1. **Collect the sources and note each one's clock.** Chat tools show the viewer's local zone, alert tools usually use UTC, and deploy logs often use the runner's zone. Convert everything to UTC before ordering events, and never merge two sources before their zones are stated.
2. **Find the three anchor times.** Start of impact is the earliest customer-visible failure in the metrics, which usually comes before any alert. Detection is the first alert that fired, not the first human message. Resolution is when the metric recovered, not when someone said it was fixed.
3. **Mark each claim** "confirmed" (two independent sources, or a log line) or "reported" (one person's recollection). Keep the reported claims for the final list.
4. Build the timeline rows with the template in the section below.
5. **Write impact** as counts and durations taken from metrics the user supplied. With no metrics, write "impact not measured"; never estimate.
6. **List follow-ups** with an owner and a date, or the word "unassigned". Never invent an owner.

## Timeline template

Fill in this template, one row per timeline event, copying the Status column from step 3:

```text
| Time (UTC) | Source | Event | Status |
|---|---|---|---|
| 14:02 | alert tool | Error-rate alert fired for checkout | confirmed |
| 14:09 | chat export | On-call acknowledged the page and opened a bridge | reported |
```

## NEVER

- Never name a person as the cause: write the action and the condition that made it reasonable, because blame stops people from reporting what they saw.
- Never write "human error" as a root cause: it ends the analysis where it should start.
- Never drop a conflicting timestamp: show both and say which you trusted and why.

## Gotchas

- A daylight-saving change inside the incident window shifts local-zone logs by an hour; check the date before converting.
- A chat export timestamp is the time the message was sent for the exporter, not for the author, so exports from two people can disagree by minutes.

## Output

The summary, then the timeline, the unverified claims and the follow-ups, in that order.
