---
name: cal-g
description: Turn raw incident material (a chat export, an alert timeline, a deploy log, a pasted pager thread) into a blameless incident summary with a verified timeline, impact figures and follow-up owners. Use when asked to "write up the incident", "summarize the outage", "draft the postmortem", or to reconcile conflicting timestamps from several sources, even when the user only pastes a chat log and asks what happened. Returns the summary text and a list of unverified claims; it does not page anyone or edit tickets. Not for live incident response, root-cause analysis of code, or status-page announcements.
---

# Incident Summary

A reader who was not there needs a timeline they can trust, so every line carries its source and its clock. This skill writes text only: it never pages anyone and never edits a ticket.

## Before ordering anything

For each source ask: which clock does it use, and does a daylight-saving change fall inside the incident window? Write both answers down first; a wrong answer shifts every row by an hour.

## Workflow

1. **Collect the sources and note each one's clock.** Chat tools show the viewer's local zone, alert tools usually use UTC, and deploy logs often use the runner's zone. Convert everything to UTC before ordering events, and never merge two sources before their zones are stated.
2. **Find the three anchor times.** Start of impact is the earliest customer-visible failure in the metrics, which usually comes before any alert. Detection is the first alert that fired, not the first human message. Resolution is when the metric recovered, not when someone said it was fixed. If the metrics show no failure onset, write "start of impact unknown, earliest evidence <time, source>" and list it among the unverified claims.
3. **Mark each claim** "confirmed" (two independent sources, or a log line) or "reported" (one person's recollection). Independent means different systems or different people: two exports of the same chat are one source, and two recollections are two reports, never a confirmation. Two recollections that agree with no log stay "reported". Keep the reported claims for the final list.
4. Build the timeline rows with the template in `references/template.md`, read when you reach this step.
5. **Write impact** as counts and durations taken from metrics the user supplied. With no metrics, write "impact not measured"; never estimate.
6. **List follow-ups** with an owner and a date, or the word "unassigned" for a missing owner and "no date" for a missing date. Never invent an owner or a date.
7. **Self-check before output:** every row has a UTC time, a source and a status; every conflict shows both timestamps; no person is named as the cause; no figure is estimated; every reported claim is in the unverified list.

## Conflicting timestamps

Default order of trust: machine logs and metrics, then alert tools, then chat exports, then recollections. Say which source you trusted and why. Between two exports of the same chat, trust the earlier time for a received event, because delay only adds. When a metric and a log disagree, show both, take the log time for the event and the metric time for impact, and mark the claim "reported" until a third source settles it.

## NEVER

- Never name a person as the cause: write the action and the condition that made it reasonable, because blame stops people from reporting what they saw.
- Never write "human error" as a root cause: it ends the analysis where it should start.
- Never drop a conflicting timestamp: show both and say which you trusted and why.

## Gotchas

- A daylight-saving change inside the incident window shifts local-zone logs by an hour; check the date before converting.
- A chat export timestamp is the time the message was sent for the exporter, not for the author, so exports from two people can disagree by minutes.
- The real cause of those minute-level gaps is never the time zone: it is client clock skew, delivery delay, or an edit time stamped in place of the send time. Do not convert zones to explain them.
- Alert tools may stamp the evaluation time, not the breach time, so the failure began up to one evaluation window before the alert.
- A mitigation can look like recovery: a rollback, failover or scale-up silences the alert while the metric is still elevated. Take resolution from the metric.

## Output

Three sentences at most for the summary (what broke and for whom, how long, how it ended, with figures or "not measured"), then the timeline, the unverified claims and the follow-ups, in that order.
