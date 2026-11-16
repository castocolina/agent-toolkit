# cal-g

Calibration fixture: a well-built skill that turns raw incident material into a blameless incident summary. It is used only to calibrate the skill judge and is not a real skill.

## What it does

- Asks which clock each source uses and whether a daylight-saving change falls in the window, then converts every source to UTC before ordering events.
- Marks each claim confirmed (independent sources or a log line) or reported, and falls back to "start of impact unknown" when metrics show no onset.
- Orders conflicting timestamps by a default trust order and always shows both.
- Lists follow-ups with an owner or "unassigned" and a date or "no date".
- Loads the timeline template from `references/template.md` at the step that builds the timeline.

## Example prompts

- "Write up the incident from this chat export."
- "Reconcile the timestamps from the alert log and the deploy log."

Eval inputs live in `evals/files/`.

## Installation

```bash
cp -r skills/cal-g ~/.claude/skills/
```
