# Feedback Mastery

A skill for Claude Code that prepares, delivers, receives, and follows up on specific workplace feedback with the Situation-Behavior-Impact (SBI) model, and resets stakeholder expectations with explicit scope and date trade-offs.

## What It Does

- Classifies the request first (purpose, power relationship, evidence quality, wanted outcome) and asks for a concrete instance when the user only has an impression.
- Routes to the right path: single incident or recognition, recurring behavior, receiving feedback, expectation reset, conflict between two other people, or a formal HR matter that needs its proper channel.
- Drafts SBI openers that keep observed behavior apart from inferred motives and feelings.
- Gives a recipient workflow for vague criticism: acknowledge, ask for an example, reflect back, separate disputed claims, then agree.
- Ends with a written recap and a default check-in.

`SKILL.md` holds the workflow, gotchas, and the gated reference list. The references hold worked material:

| Reference | Content |
| --- | --- |
| `references/feedback-sbi-model.md` | Calibrated SBI examples: observation versus interpretation, recognition, disputed evidence, power gaps, third-party reports, recurring patterns |
| `references/difficult-conversation-scripts.md` | Responses to common reactions, substitutions that prevent non-obvious failures, the separate-then-joint conflict sequence |
| `references/expectation-alignment.md` | Deadline pushback dialogue, scope-change template, ownership reset |

## When to Use

- "How do I give feedback about a colleague interrupting in standup?"
- "My manager called me unreliable with no examples. How do I respond?"
- "Help me recognize a teammate for catching a bug in review."
- "Leadership wants this in half the time. Help me push back."
- "What should the follow-up email say after we agreed on changes?"

Not for legal or HR determinations, performance improvement plans, ratings, policy drafting, or difficult conversations without a feedback or expectation goal (see `difficult-workplace-conversations`).

## Installation

```bash
cp -r skills/feedback-mastery ~/.claude/skills/
```

On claude.ai, add the skill to project knowledge or paste `SKILL.md` into the conversation.

## Directory Structure

```
feedback-mastery/
  SKILL.md        # Workflow, gotchas, confidentiality test, gated reference list
  references/     # Worked examples, reaction scripts, expectation alignment
  evals/          # Output evals, trigger queries, fixtures
```

## Recommended Reading

For deeper exploration of these concepts:

- *Crucial Conversations* by Kerry Patterson and Joseph Grenny
- *Difficult Conversations* by Stone, Patton, and Heen
- *Radical Candor* by Kim Scott
- Amy Edmondson's research on psychological safety

The SBI model was developed by the Center for Creative Leadership.
