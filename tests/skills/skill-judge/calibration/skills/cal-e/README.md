# cal-e

Calibration fixture: a well-built skill that drafts release notes from merged pull requests. It is used only to calibrate the skill judge and is not a real skill.

## What it does

- Groups merged PRs by user impact: Breaking, Added, Changed, Fixed.
- Cancels reverts, dedupes PRs merged twice and leaves out internal work.
- Reports the PRs it could not classify instead of guessing.

## Example prompts

- "Draft the release notes for the PRs merged between these two tags."
- "What shipped since the last release? Here is the PR list."

## Installation

```bash
cp -r skills/cal-e ~/.claude/skills/
```
