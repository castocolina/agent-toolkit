# Cause Exploration

Playbooks for recurring behavior or quality problems where the user does not know the cause yet. The opener, the dispute test and the follow-up rules live in `SKILL.md`; this file covers what to do after the opener: ask about the cause, respond to what comes back, and state the bar. Never present a guessed cause as fact; each branch below starts from the answer the person gave.

## Sequence

1. **Prepare:** collect one or two dated instances (PRs, bug reports, timestamps), not every entry (R2).
2. **Deliver:** SBI opener ending in an open question: "In [PRs #X and #Y], [what happened]. I want to understand what is going on and how I can help. How did you see it?"
3. **Explore:** ask about causes with open questions (see the playbooks). Listen before responding.
4. **Respond by cause:** pick the branch the answer matches; if none matches, ask one more question.
5. **Check the power relationship first, then state the bar** (SKILL.md section 1 and gotcha on power). A manager, or anyone with authority over the work, may state an authorized mandatory bar as required, then ask what would help the person meet it. A peer, or the user giving upward feedback, has no authority to set a mandate: make a specific request for the change and ask what would help, and if the bar itself needs setting, take it to the appropriate decision-maker (the manager or team lead).
6. **Follow up** with a dated check-in and a written recap (`SKILL.md` section 6).

## Playbook: recurring lateness (standup)

**Opening** (dated instances):
> "Standup starts at 9:00. You joined at about 9:15 on Monday and Wednesday of this week. I want to understand what is happening."

**If they get defensive:**
> "I'm not trying to call you out. I want to make sure I'm not missing something. Is there a scheduling conflict or something else going on?"

**If they give a reason:**
> "Thanks for telling me. Let's find something that works: could we move the meeting, or is there another change that would help?"

Keep a personal reason (health, family) out of the recap and the notes, even if they ask for it to be written down (Confidentiality test in `SKILL.md`): record only the agreed work change ("standup moves to 9:30"). If they need a formal accommodation, send that documentation to the appropriate authorized process (HR or the manager's policy), not into an ordinary recap or note.

**If there is no clear reason** (branch on power first):

- Manager or lead who owns the standup rule:
> "I need everyone in at the start for standup to work. Can you commit to 9:00 from now on? What would help you make that happen?"

- Peer, or upward feedback to a manager (no authority to set the rule): make a specific request about the effect on your work, and take the rule itself to whoever owns it.
> "When you join at 9:15, [the effect on your own work, for example: I have to repeat my update]. Could you join by 9:00? What would help you make that happen?" If the start time itself is the issue, raise it with the team lead, who owns the rule.

**Follow-up with a dated criterion:**
> "Let's check in on [date, about two weeks out]. If you've been there at 9:00 each day, we'll consider this resolved."

## Playbook: quality issues in code

**Opening** (dated instances):
> "The most recent PR ([#]) [and the one before it ([#])] had [tests failing in CI / bugs found in QA]. I want to understand what is going on."

Use the most recent one or two PRs, not a longer list (R2 in `SKILL.md`).

**Explore** (one question at a time, open):

- "Are the requirements clear?"
- "Is the timeline realistic?"
- "Is something about our testing setup making this harder?"
- "Is other work pulling your attention?"

**If it is workload:**
> "If you're stretched this thin, let's look at your commitments and see what we can adjust."

**If it is skill:**
> "Would it help to pair with someone on the next feature, or to go through our testing practices together?"

**If it is tooling:**
> "Let's fix the setup first. What would make it easy to run the suite before opening a PR?"

**If the bar was unclear:**
> "Here is what I need going forward: PRs have tests and pass CI before review. What would help you meet that bar consistently?" (Manager or reviewer who owns the standard. A peer asks instead: "Could you run the suite before tagging me for review? What would help?" and takes a disputed standard to the team lead.)

Close with a dated check-in on the next few PRs and recognize the improvement when it shows (a recognition message is separate from this conversation, R1).
