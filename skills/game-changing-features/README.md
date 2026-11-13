# Game-Changing Features

A product strategy skill that finds and ranks high-leverage opportunities ("what would make this 10x more valuable?") from your repository, feedback and usage data, and saves each analysis as a session file.

## When to Use

- "What should we build next?"
- "What would make this product 10x better?"
- "Is this feature request the right next move?"
- Looking for growth levers or small wins with outsized impact

Not for writing code, sprint plans, user stories, effort estimates, competitor or pricing research, or roadmaps with committed dates.

## What You Get

A short ranked set of opportunities, each with its evidence or hypothesis label, value mechanism, reach, adoption cost, effort, risk and the assumption to validate, grouped as Massive, Medium and Small Gems and prioritized as Do Now, Do Next, Explore or Backlog. The workflow and its rules live in [SKILL.md](SKILL.md).

## Example

```
User: What should we build next for our habit tracker? The repo is checked out.

The skill reads the changelog, feature flags, feedback and metrics first, so it
does not pitch a feature that already ships or sits behind a flag, sizes reach
on active users rather than signups, and saves the result as
.claude/docs/ai/habit-tracker/10x/session-2.md next to the earlier session.
```

## Output Location

```
.claude/docs/ai/<product-or-area>/10x/session-N.md
```

Each run writes the next unused session number; earlier sessions are never overwritten. Without file access, the full report comes back in the reply with its intended path.

## Credits

Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy.

## Installation

**Claude Code:**

```bash
cp -r skills/game-changing-features ~/.claude/skills/
```

**claude.ai:** add the skill to project knowledge or paste the SKILL.md contents into the conversation.
