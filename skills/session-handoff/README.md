# Session Handoff Skill

Creates, validates and resumes handoff documents in a project's `.claude/handoffs/`, so a fresh agent session can continue work without rediscovering context. [SKILL.md](SKILL.md) is the single source for the workflow, verdicts and gotchas; this file covers installation and layout only.

## Installation

**Claude Code:**

```bash
cp -r skills/session-handoff ~/.claude/skills/
```

**claude.ai:** add the skill to project knowledge, or paste the contents of `SKILL.md` into the conversation. The scripts need Python 3.10+ and, for git metadata and staleness, `git` on `PATH`. No network access is required.

## Contents

| Path | What it is |
|------|------------|
| `SKILL.md` | Mode selection, CREATE and RESUME workflows, verdict tables, gotchas |
| `scripts/create_handoff.py` | Writes a scaffold with git metadata and the baseline commit; never overwrites |
| `scripts/validate_handoff.py` | Checks placeholders, required sections, secrets and file references; READY/NEEDS_WORK/BLOCKED |
| `scripts/list_handoffs.py` | Lists handoffs newest first |
| `scripts/check_staleness.py` | Compares a handoff's baseline with the current git state |
| `references/handoff-template.md` | What each handoff section should hold |
| `references/resume-checklist.md` | Environment checks and stop signals for a stale resume |
| `evals/` | Output evals, trigger queries and their input files |

Each script documents its arguments and exit codes under `--help` and supports `--json`.

## Tests

Script tests live in [tests/skills/session-handoff](https://github.com/castocolina/agent-toolkit/tree/main/tests/skills/session-handoff):

```bash
python3 -m unittest discover -s tests/skills/session-handoff -p 'test_*.py'
```
