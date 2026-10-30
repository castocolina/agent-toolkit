---
name: ship-learn-next
description: "Turn supplied articles, tutorials, YouTube transcripts, or course notes into a Ship-Learn-Next implementation quest with a shippable first rep, measurable completion criteria, reflection, and evidence-driven next iterations. Use when the user wants to implement advice or practice lessons. Not for summaries, reading lists, curricula, or exam-study schedules."
allowed-tools: Read Write
---

# Ship-Learn-Next

Use when the user wants to act on learning content, not merely understand or summarize it. Build a short loop: ship a controllable deliverable, inspect evidence, then choose the next rep. Be direct, question-driven, and end with a concrete commitment.

## Source and extraction

When the eval or runtime cannot write files, state that assumption and provide the complete Markdown plan in the response rather than stopping at a request for inputs. If inputs are absent, give a clearly labeled provisional plan based only on the stated goal and identify missing source lessons as assumptions; do not claim it is source-derived. Name the intended saved Markdown plan path.

- Read the content the user provides, whether pasted text or a file. If they provide only a YouTube URL and no accessible transcript, ask them to paste/upload the transcript; do not invent source lessons or timestamps.
- Extract only practice-worthy claims and techniques. Link each to the source section or timestamp only when actually available. If content is missing, ask for it instead of presenting a generic plan as source-derived.
- Identify what outcome the user wants. Reuse their deadline and available time; ask only for missing constraints that change the first rep.

## Design the first rep

Choose the smallest real deliverable that tests one lesson and can be completed with the user's available time. Make its completion criteria controllable (publish, send, build, demonstrate); keep external response, revenue, or adoption as a learning metric, not a shipment gate. Include only resources needed for this rep.

A rep must be small enough that its outcome is interpretable. Change one experimental variable at a time; otherwise a result cannot show which change mattered. Where outcomes are noisy, define an observable process measure alongside the external result.

## Review evidence and choose next

After the user reports a rep, distinguish shipped artifact/process evidence from outcome metrics and anecdote. Apply this rule:

- Deliverable not shipped: shrink or remove the blocker before repeating.
- Execution inconsistent: repeat the same rep until execution is reliable.
- Evidence ambiguous: isolate one variable and run a cleaner rep.
- Reliable completion with usable evidence: increase difficulty or test the next lesson.

Keep Rep 1 fully actionable. Later reps are provisional outlines only; each proposed later rep should add or change exactly one element relative to the prior rep, and state that single change. Expand Rep 2 after reviewing Rep 1 evidence, and never pretend future learning is known.

## Save and present

Save as `Ship-Learn-Next Plan - <brief title>.md` unless the user names a path. File saving is the default, not a requirement: honor chat-only requests and state if writing is unavailable. Save source, extracted lessons, Rep 1 deliverable/criteria/steps/reflection, and provisional future direction. Report the path only if the file was actually written. End by asking for a ship date or naming the next concrete commitment.

## Gotchas

- Never make completion depend on an uncontrollable market response; otherwise the user can do the work and still be told they did not ship.
- Keep completion criteria separate from learning metrics; an experiment can be completed even when its hypothesis is disproved.
- Never fabricate source references or timestamps. False provenance makes the plan look grounded when it is not.
- Never vary several elements in one rep: confounded results cannot guide the next decision.
