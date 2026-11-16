# Expectation Alignment

Sample dialogue, the scope-change template, and the ownership reset. The reset rules and their traps live in `SKILL.md`.

## Deadline pushback: sample conversation

> **Stakeholder:** "We need the new dashboard by end of month."
>
> **You:** "I understand the date matters for the board demo. The full dashboard (charts, filters, export) took six to eight weeks the last two times we built something like it. We have four."
>
> **Stakeholder:** "We really need it by end of month."
>
> **You:** "Then here are two ways: ship the core charts by end of month and add filters and export two weeks later, or ship everything mid-next-month. Which matters more, the date or the full set?"
>
> **Stakeholder:** "Can't the team just work faster?"
>
> **You:** "Rushing moves the cost into bugs we'd fix after launch, during the demo window. The scope-first option gets you something solid to show. Can I write up the choice so we're aligned?"

## Scope-change template

Send this when a request lands mid-flight, before agreeing to it:

```markdown
**Change request:** [what is being asked]

**Impact:**
- Timeline: [current date] -> [new date]
- People: [any change]
- Risk: [new risk introduced]

**Options:**
1. Add it and move the date to [date]
2. Add it and drop [other item]
3. Defer it to the next phase

**Recommendation:** [your suggestion and why]

**Decision needed by:** [date]
```

The "decision needed by" line matters: without it, the request is often treated as accepted by default while it waits.

## Ownership reset (unclear role boundaries)

Signs: tasks dropped because each side thought the other had them, duplicated work, "I thought you were handling that".

1. **Name the gap on one instance:** "The staging deploy last week sat for two days because neither of us thought we owned it."
2. **Propose explicit owners:** "My understanding is that [A] owns [X] and [B] owns [Y]. Does that match yours?"
3. **Define the handoff condition:** "B takes over once [specific condition, e.g. the PR is merged]."
4. **Record it where the work lives** (ticket, team doc), not only in a DM, so the next person on the team can find it.

Get the ownership decision from whoever has authority over both people's work; two peers agreeing between themselves does not bind their managers.
