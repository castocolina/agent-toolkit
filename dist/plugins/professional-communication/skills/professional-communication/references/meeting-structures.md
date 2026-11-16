# Meeting agendas and follow-through

Use a meeting only when a decision or interaction needs live exchange. Before scheduling, name the decision, owner, participants, pre-read, and outcome; otherwise use an async document.

Minute counts below are typical values: adapt them to the team, the sprint length, and the time actually available.

## Daily standup

The Scrum Guide sets the Daily Scrum as a 15-minute event; run it daily and keep to that time box. A common format (the Scrum Guide does not prescribe the questions) has each person answer three questions in about one to two minutes:

1. **Yesterday:** what did I complete?
2. **Today:** what am I working on?
3. **Blockers:** what is in my way?

Failure modes to avoid:

- Turning it into a status report to a manager: it is a team sync.
- Problem-solving during the standup: note the blocker and take it offline.
- Technical detail: save it for pairing or a follow-up.
- Skipping the standup because there is "nothing to report": a brief update still keeps the team aligned.

## Sprint planning

Check actual capacity before selecting scope: PTO/absences, support load, standing commitments, and dependencies. Then order and select refined backlog items against that capacity; commitment is the result, not a phase before the check.

```markdown
1. Goal and decision owner
2. Capacity: availability, support, and dependencies
3. Prioritized, ready work and acceptance criteria
4. Select scope that fits capacity; surface risks
5. Record commitments, owners, and unresolved questions
```

## Design review

```markdown
1. Problem and constraints
2. Proposed design and data/control flow
3. Alternatives, trade-offs, failure modes
4. Decision (owner, outcome, rationale)
5. Actions (owner, due date) and unresolved items
```

## Retro / incident review

Separate observed timeline from interpretation. For incidents, assess impact and contributing system conditions without assigning blame. End with one to three prevention/detection/response actions, each with an owner and follow-up date.

## Sprint retrospective

Five phases (names from Derby and Larsen, *Agile Retrospectives*), with typical minutes for a 65-minute session, to be scaled to the time available. The Scrum Guide caps the Retrospective at three hours for a one-month Sprint and less for shorter Sprints.

| Phase | Minutes (typical, adapt) | Activity |
| --- | --- | --- |
| Set the Stage | 5 | Check in, set the tone |
| Gather Data | 20 | Collect what happened and how the team felt |
| Generate Insights | 20 | Discuss patterns and causes |
| Decide What to Do | 15 | Choose one to three improvements, each with an owner |
| Close the Retrospective | 5 | Appreciate, wrap up, decide how actions are tracked |

Common formats for the Gather Data phase (prompts paraphrased):

- **Start / Stop / Continue:** what should we start doing, stop doing, and keep doing because it works?
- **4Ls:** Atlassian's version is **Loved** (what went well), **Loathed** (what made things worse), **Longed for** (what we wished we had), **Learned** (what we discovered). An older variant reads **Liked / Learned / Lacked / Longed for**. Print the Atlassian version unless the team already uses the older wording, and say which one the agenda prints.
- **Mad / Sad / Glad:** what frustrated you, what disappointed you, what made you glad.

Send the outcome with the retrospective summary in `email-templates.md`.

## One-on-one (1:1)

Typically 30-60 minutes, weekly or bi-weekly, for support, feedback, and career growth. This is the agenda only; for difficult feedback use `feedback-mastery`.

```markdown
1. Their topics first (15-20 min): what is on their mind; blockers, concerns, wins
2. Feedback exchange (10-15 min): recognition for recent work; growth areas or coaching
3. Career and growth (10-15 min): progress on development goals; upcoming opportunities
4. Admin and updates (5 min): organization updates; schedule impacts
```

## Code review walkthrough

Typically 30-45 minutes, as needed for complex or significant changes; for deep review, not routine pull requests.

```markdown
1. Context (5 min): what problem this solves; why this approach was chosen
2. High-level walkthrough (10 min): architecture or structure; key files and their purposes
3. Detailed review (20 min): critical paths; non-obvious decisions; questions answered live
4. Wrap-up (5 min): remaining concerns; the approval path
```

## Before / during / after

- **Before:** distribute the decision question and relevant evidence; invite only decision-makers and contributors.
- **During:** keep discussion on the stated decision, capture dissent and unknowns, and defer unrelated problem-solving.
- **After:** send the decision, rationale, owners, due dates, and open questions. Do not record a meeting by default; follow consent and organizational policy.

During the meeting:

- [ ] Start on time
- [ ] State the objective at the opening
- [ ] Time-box each discussion
- [ ] Capture action items live
- [ ] Leave about 5 minutes for wrap-up
- [ ] End on time, or early

After the meeting:

- [ ] Send the summary promptly (within 24 hours is typical; adapt to urgency)
- [ ] Every action item has an owner and a due date
- [ ] Follow up on commitments
- [ ] Cancel recurring meetings that no longer add value

## Meeting summary

```markdown
**Meeting: [topic] - [date]**

**Attendees:** [names]

**Decisions:**
- [decision, with owner]

**Action items:**
- [ ] [person]: [task], due [date and time zone, if agreed]

**Open questions:**
- [question and who will answer it, if known]

**Next steps:**
- [follow-up meeting if needed; documents to share]
```

Record only what was said in the meeting; mark dates or owners that were not agreed as "Proposed:".

Sources (checked 2026-11-07): [The Scrum Guide](https://scrumguides.org/scrum-guide.html) for the 15-minute Daily Scrum and the Retrospective time box; [Derby and Larsen, Agile Retrospectives (2nd ed.), O'Reilly listing](https://www.oreilly.com/library/view/agile-retrospectives-2nd/9798888650868/f_0010.xhtml) for the phase names; Atlassian Team Playbook for the [4Ls](https://www.atlassian.com/team-playbook/plays/4-ls-retrospective-technique) and [Mad/Sad/Glad](https://www.atlassian.com/team-playbook/plays/retrospective) formats, and [Start/Stop/Continue](https://www.atlassian.com/software/confluence/templates/start-stop-continue).
