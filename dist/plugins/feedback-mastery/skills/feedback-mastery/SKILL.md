---
name: feedback-mastery
description: "Prepare, deliver, receive and follow up on specific workplace feedback using Situation-Behavior-Impact (SBI), and reset stakeholder expectations with explicit scope/date trade-offs. Use when thanking or recognizing a teammate for specific work, raising an observable behavior (broken builds, missed commitments, interrupting), answering vague criticism such as \"you're unreliable\" even if the user never says feedback, prepping a 1:1 or upward feedback, giving feedback to two people in a conflict you lead, writing the follow-up recap, or pushing back on a deadline or scope creep. Not for ceremonial congratulations (work anniversaries, birthdays, farewells), legal or HR determinations, PIPs, ratings, policy drafting, or layoffs and salary talks (use difficult-workplace-conversations)."
allowed-tools: Read Glob Grep
---

# Feedback Conversations

## 1. Classify before drafting

Settle purpose, power (report, peer, manager, stakeholder: it decides who may set the expectation), and evidence: what the user can point to (PR, ticket, chat log, calendar) versus what they heard or infer.

Test: if the user can name any dated event, the evidence is thin, not missing; if they can name none, it is an impression.

Default when purpose and power are clear but evidence is thin: draft one opener with bracketed placeholders and ask for the one missing fact. Never interrogate the user with a list of questions first. Example: "In [which standup], you [what was said or done]. [What it delayed or blocked]. How did you see it?" plus "Which standup was it, and what did it hold up?"

If the user has only an impression ("seems checked out") or hearsay, ask for one concrete instance first; SBI built on an impression is still an accusation. If they still cannot name one, do not draft feedback: suggest they watch for the next instance and raise it then, or open with a question ("How do you feel the last sprint went?") that makes no claim.

## 2. Pick the path

| Situation | Do | Load |
| --- | --- | --- |
| Recognition and corrective feedback in one request | R1 | nothing |
| One incident, or recognition | SBI opener plus one open question | [feedback-sbi-model.md](references/feedback-sbi-model.md) only if evidence is disputed or there is a power gap |
| Someone else reported the behavior to the user | Use only an instance the user observed themselves; never name the reporter | [feedback-sbi-model.md](references/feedback-sbi-model.md) for the third-party example |
| Recurring behavior | R2 | [difficult-conversation-scripts.md](references/difficult-conversation-scripts.md) only to rehearse reactions |
| Same issue across several people or a team | R3 | nothing |
| Feedback to the user's manager | R4 | [feedback-sbi-model.md](references/feedback-sbi-model.md) for the upward example |
| User is receiving feedback | Section 4 | nothing |
| Scope, date, ownership, or success criteria disputed | Section 5 | [expectation-alignment.md](references/expectation-alignment.md) for sample dialogue, the scope-change template, or an ownership reset |
| Conflict between two other people | R5 | [difficult-conversation-scripts.md](references/difficult-conversation-scripts.md) only once R5's conditions hold |
| Formal performance process, misconduct, harassment, discrimination, safety | R6 | nothing |

### Rules R1-R6

- **R1 Mixed request:** deliver recognition and corrective feedback separately, never in the same conversation or message. The praise reads as a setup and the correction erases it.
- **R2 Recurring:** pick one or two instances, the most recent and clearest; never list every entry. A dated list turns the talk into litigating each item. Say what was raised before and what is new.
- **R3 Several people:** give it to each person individually, on their own instance. A group announcement aimed at a few lands on everyone and changes nothing for the few. A team-wide norm ("CI green before review") may be restated to the group as a norm, with no names or examples.
- **R4 Upward:** one instance and its effect on the user's work, then a request for a specific change. No verdict on the manager, no demand; private, in a 1:1.
- **R5 Conflict between others:** help the user give each person their own SBI feedback first. Facilitate jointly only if all hold: the user has a role over the shared work (lead, manager, agreed facilitator) and no stake in which side wins; both people agreed to meet; the issue is work behavior. Otherwise suggest a neutral facilitator both accept.
- **R6 Formal matters:** do not substitute coaching for the required process. Help the user list factual questions and name the HR or policy channel.

## 3. Deliver

Dispute test, for each factual assertion in the opener: could the other person dispute it by pointing to a record? If not, it is an inference; cut it or turn it into a question.

- **Situation, Behavior, Impact, open question**: "In Tuesday's review [situation], you interrupted Maya twice before she finished [behavior]. We missed her deployment concern until Thursday [impact]. How did you see that discussion?"
- **Impact** is an effect on the work (blocked merge, missed concern, slipped release) or the user's own reaction stated as theirs. Never the other person's feelings or motives.
- **Recognition** names the behavior and its effect, then stops: no "but next time", no improvement point, no recap or check-in.

Pre-send gate, on the final text of every draft: every factual assertion passes the dispute test (open questions, requests, commitments and the user's own labeled reactions are allowed; check future options against the stated estimates, assumptions and costs, not a record); no inferred motive or feeling; written for private delivery; passes the [Confidentiality test](#confidentiality-test). Revise until all four pass.

## 4. Receive

Before drafting a reply, ask of each statement the user received: is it about an instance (a date, an artifact, an effect) or about them (a label)? Reply to instances; turn labels into a request for an instance.

- Do not argue the label; ask for one recent example and what it affected.
- For each disputed claim, name what would settle it (ticket history, a timeline, the reviewer) instead of rebutting it in the meeting.
- If no example comes, agree to revisit when there is one and ask how the next instance should be flagged.

Sample reply to "You're unreliable":

> "I want to fix this, so I need to know what you're seeing. Which project or date do you have in mind, and what was the effect?"
> If no example: "Then can we come back to it when one comes up? Flag the next one to me the day it happens, and I'll act on it."

## 5. Expectation reset

Before you reset expectations, ask: what does the date exist for? Name that goal first ("the launch matters for the board demo"), then the constraint, and keep only options that still serve the goal.

- Offer at least two options, each with its cost. If only one is feasible, say so and name what refusing it costs.
- Do not answer "can't you just work faster?" with a softer estimate; that accepts the date with hidden risk. Restate the options.
- If every option is rejected (full scope and the original date both demanded), restate the cost of the refused option once, record the decision and the accepted risk in writing, and escalate to whoever owns both priorities.
- "Add people" has a ramp-up cost: on a short timeline it often moves the date later. Name it whenever you offer it.
- With no stated preference, recommend the reduced-scope option on the original date (it ships value and keeps the commitment); fall back to moving the date when the cut would remove what the date exists for.
- Record the choice and the accepted risk in writing.

Contrast. Weak: "Two weeks is really tight; we'll try our best." That accepts the date and hides the risk. Strong: "Six weeks of work won't fit in two. In two weeks we can ship checkout without saved cards; full scope lands in six. Which do you want? I'll write up the choice."

## 6. Follow up

For corrective feedback and expectation resets, send a written recap within one working day:

```text
Recap of [date]: [situation and behavior discussed]
Agreed: [action] / [owner] / [date]
Agreed: [action] / [owner] / [date]
Open: [disputed or unresolved item]
Check-in: [date]
```

Default check-in: two weeks for a behavior change, or the next occurrence of the recurring event (next sprint planning, next release); for an expectation reset, the agreed decision date. The recipient of feedback can send the same recap; it fixes vague commitments in writing.

Private details and speculation in the user's notes (health, family, guesses about motive) are dropped silently: never named, not even in a note about what was left out. If you mention the omission, say only "left out personal details and guesses about motive".

## Gotchas

- **Never state inferred motive, intent, or another person's feelings as observed fact** ("you didn't care", "made Alex frustrated"). The conversation becomes a dispute about mind-reading instead of the behavior.
- **Never pad an opener with "I feel like you..." or "I think you..."** It is the same inference with a hedge, and it is the first thing a drafting model reaches for to sound soft.
- **Never surprise someone with an accumulated, undocumented pattern.** It invites "this is the first I've heard of it", which is true. Raise timely examples and own any earlier silence.
- **Even when the user asks for a channel post, draft for private delivery.** A draft written for a public channel gets pasted there; the audience turns a behavior conversation into a status threat and exposes private information.
- **Written channels lose tone and are retained** (chat and email can be exported in HR investigations or legal discovery). Default to a private live conversation for the first delivery of corrective feedback. A short, factual private written opener is acceptable when accessibility, agreed preferences or asynchronous work call for it and policy permits; apply the same confidentiality checks and offer a live follow-up. Write every recap so the user can send it as-is: facts and agreements only, no speculation about health, personal life, or motive.
- **Never deliver corrective feedback right before the person presents, demos, or goes on call.** They can neither absorb it nor act on it in time, and the event goes worse; deliver after, within days.
- **Formal processes (PIPs, discipline, investigations) usually require dated, contemporaneous records in the HR system.** Private notes reconstructed later may not count, and an informal side deal can contradict the process. If one is underway or likely, have the user check the policy before the conversation.
- **When power is unequal, state a required change as required.** "Could you maybe try..." from a manager makes a non-optional expectation sound optional.
- **Never have the user promise confidentiality that policy may override** (safety, harassment, legal reporting duties); a broken promise costs more trust than an honest "I may have to report this".

## Confidentiality test

Include or record a detail only if all three hold: the person receiving it needs it to act; workplace policy allows sharing it; it concerns work behavior, not health, family, or protected characteristics. If any is unclear, leave it out and ask the user.
