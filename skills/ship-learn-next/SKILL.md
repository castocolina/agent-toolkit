---
name: ship-learn-next
description: "Turn articles, tutorials, YouTube transcripts, talks or course notes into a Ship-Learn-Next plan: a first rep the user can ship within their time budget, with controllable completion criteria, reflection questions and provisional next reps; also reviews a reported rep's results to choose the next rep. Use when the user says \"make this actionable\", \"I watched/read X, now what?\", \"help me actually implement this advice\", \"turn my notes into something I can ship\", or reports how a rep went and asks what to do next. Not for summaries or key takeaways, reading lists, curricula, exam-study schedules, or project and sprint plans that do not start from learning content."
allowed-tools: Read Write
---

# Ship-Learn-Next

A loop: ship a small deliverable, read the evidence, choose the next rep. The plan keeps Rep 1 fully actionable and later reps provisional.

## Workflow

1. **Route the request.**
   - Content supplied (pasted text or a file): read it, go to step 2.
   - Only a URL, a title or the user's memory of the content: ask for the transcript or text. If the user wants a plan now, give one headed `Provisional: not derived from the source`, with its lessons listed as assumptions drawn from the stated goal.
   - The user reports how a rep went: go to step 4.
   - The user wants a summary, reading list or study schedule: answer that; do not force a rep.
2. **Extract and pick.** For each lesson ask: what would the user do differently tomorrow, and what single artifact proves it? No answer means drop the lesson. When several compete for Rep 1, pick the one with the smallest shippable test inside the user's available time. Reuse the stated deadline and time budget; ask only for a missing constraint that changes Rep 1, otherwise state the assumption ("assuming 3 hours this week") and continue.
3. **Design Rep 1** in the shape below.
   - Done-when criteria are actions the user controls: publish, send, build, demo. Replies, revenue, conversion and adoption are learning metrics.
   - When outcomes are noisy (small samples, slow feedback, a market), add a process measure the user can observe during the rep.
   - Causal comparison (A/B test, before/after a metric): change exactly one variable. Creative or integrative practice (a first song, a portfolio site): declare one learning target; coordinated changes are fine when the goal or time budget needs them, but say the result will not isolate a cause.
   - Steps fit the stated time budget; list only the resources this rep needs.
   - Later reps are one-line outlines, each naming the one thing it changes from the rep before. Expand Rep 2 only after Rep 1 evidence.
4. **Review evidence and choose next.** Separate artifact and process evidence (what shipped, which steps happened) from outcome metrics and anecdote, then take the first matching row:

   | Evidence | Next rep |
   |---|---|
   | Not shipped (no artifact produced) | Shrink the rep or remove the named blocker |
   | Shipped, execution inconsistent (skipped steps or days, or a partial run with some artifacts, such as 4 of 10 posts) | Repeat the same rep once, with the observed blocker removed and the process measure as the target |
   | Shipped consistently, outcome noisy or ambiguous | Draw no conclusion from the outcome; keep the same single variable and extend the sample or time |
   | Shipped consistently, usable evidence | Raise difficulty or test the next lesson |

   Time-box: every repeat must fit the remaining budget and deadline. If a repeat fails too, never offer the same rep a third time: shrink it, remove the blocker, or renegotiate the target or deadline with the user.

   Then go to step 5 with a `Rep N review` section (evidence read, row taken) and the next rep expanded in the shape below.
5. **Save and present.** Default path `Ship-Learn-Next Plan - <brief title>.md` unless the user names one. Contents: source (or the provisional heading), extracted lessons, Rep 1 in the shape below, provisional later reps. After a review, append the `Rep N review` section and the expanded next rep to the existing plan file; with no plan file, put them in the reply. On a chat-only request or without write access, put the complete plan, or the section to append marked with the target plan path, in the reply and say it was not saved. End by asking for a ship date or naming the next concrete commitment.

## Rep 1 shape

```markdown
## Rep 1: Send 10 cold emails with the one-ask template (lesson 2)
- Done when: 10 emails sent by Friday, each with one ask and one recipient-specific reason
- Learning metric: replies within 7 days (not a gate; 10 sends is noise)
- Process measure: template followed (yes/no per email), minutes per email
- Steps: list 10 prospects (30 min); draft from the template (60 min); send and log (15 min)
- Reflect: Which step took longest? Which emails broke the template, and why? What changes first?
```

## Worked review

"Sent all 10, one reply, only 6 followed the template": process evidence (6 of 10) outranks the outcome, so the reply count is not read at all; the inconsistent-execution row applies.

## Gotchas

- A source's motivational claims ("consistency beats talent") are not lessons: a rep built on one has no testable action, so it tests nothing.
- Never gate completion on a market response: the user can do all the work and still be told they did not ship.
- An experiment is complete even when its hypothesis is disproved; folding the learning metric into done-when hides that result.
- Never cite a section or timestamp the content does not show: false provenance makes a generic plan look source-derived.
- Never leave setup (accounts, tools, research) out of the Rep 1 step estimates: users budget only the shipping steps, so the rep overruns and lands in the Not shipped row.
- Never report a plan file as saved before the write succeeded; a tool-less or chat-only run must say the plan was not saved.
