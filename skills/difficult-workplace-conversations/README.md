# Difficult Workplace Conversations

A skill for Claude Code that prepares, rehearses, and follows up on high-stakes workplace conversations: negotiations, bad news, conflicts with disputed facts, mediating disputes between others, sensitive concerns, and moments where emotions may derail the talk.

## What It Does

- Classifies the request (role and power, desired outcome, stakes, formal process) and routes it, sending routine behavior feedback, recognition, and scope or deadline resets to `feedback-mastery`.
- Runs a negotiation procedure that classifies each objection (evidence, budget, process, authority) and closes on a decision owner, criteria, and a date.
- Gates any joint meeting between other people on authority, consent, and suitability, and plans the facilitated session when the gate passes.
- Puts safety, harassment, and retaliation concerns on a formal channel instead of informal coaching.
- Ends with a factual written summary that keeps disputed points marked as disputed.

`SKILL.md` holds the workflow, gotchas, and the gated reference list. The references hold worked material:

| Reference | Content |
| --- | --- |
| `references/preparation-template.md` | Full written worksheet with negotiation, bad-news, and conflict add-ons |
| `references/delivery-scripts.md` | Lines for denial, deflection, attack, shutdown, distress, reactions to a decision, sensitive disclosures, escalation |
| `references/emotional-regulation.md` | Regulation worksheet, trigger inventory, day-of preparation, one-technique picker |
| `references/facilitation.md` | Facilitated session plan: confidentiality limits, facts table, ground rules, turns, stop conditions, agreements |

## When to Use

- "Prepare me to ask my manager for a raise; she already said budget is tight."
- "I have to tell someone tomorrow that their role is being eliminated."
- "My coworker tore apart my design in front of the director. I'm furious."
- "Two of my reports remember the handoff differently. Should I get them in a room?"
- "A senior coworker keeps threatening me. What do I do?"

Not for feedback on a specific behavior, recognition, replies to vague criticism, scope or deadline pushback, or feedback recaps (see `feedback-mastery`), nor for legal advice, formal complaint drafting, PIPs, ratings, policy, or company-wide announcements.

## Installation

```bash
cp -r skills/difficult-workplace-conversations ~/.claude/skills/
```

On claude.ai, add the skill to project knowledge or paste `SKILL.md` into the conversation.

## Directory Structure

```
difficult-workplace-conversations/
  SKILL.md        # Routing, procedures, gotchas, gated reference list
  references/     # Worksheet, rehearsal scripts, composure, facilitation plan
  evals/          # Output evals, trigger queries, fixtures
```

## Related Skills

- **feedback-mastery**: feedback delivery with SBI, recognition, receiving criticism, and expectation resets
- **professional-communication**: general workplace emails, messages, and updates
