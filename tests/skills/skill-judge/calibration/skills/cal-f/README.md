# cal-f

Calibration fixture: a small skill that turns raw incident material into a blameless incident summary. It is used only to calibrate the skill judge and is not a real skill.

## What it does

- Converts every source to UTC before ordering events.
- Marks each claim confirmed or reported.
- Lists follow-ups with an owner or the word unassigned.

## Example prompts

- "Write up the incident from this chat export."
- "Reconcile the timestamps from the alert log and the deploy log."

## Installation

```bash
cp -r skills/cal-f ~/.claude/skills/
```
