# skill-updater

Check whether a skill, command or agent in this repo is still current against its upstream sources and against the models it targets. It records the result in `docs/audit/upstream-sources.json` through `audit.py track`. It does not create skills, and it refuses the synced skills `gepetto` and `datadog-cli`.

## Install

**Claude Code:**

```bash
cp -r skills/skill-updater ~/.claude/skills/
```

**claude.ai:** add the skill to project knowledge, or paste `SKILL.md` into the conversation.

## What it decides

| observation | recorded status |
|-------------|-----------------|
| source unchanged, or an `unversioned` source after reading it | `current` |
| source changed | `stale`, plus an `adopt`, `adapt` or `ignore` note |
| path missing, and exactly one new path confirmed | `path-moved` |
| path missing, several candidate paths | nothing; the candidates are listed and the user picks |
| auth, rate-limit or network error, or no candidate path | `unreachable` |
| a command or agent (no source rows), after the model probe | `current` on its `local` row |

A rule written to counter a model behavior is checked with a probe before anyone proposes removing it. Nothing is edited unless you ask for the update itself.

## Layout

- `SKILL.md`: the eight-step review with its checkpoints (error branch, contents test, tree search, model probe), the adopt/adapt/ignore decision and the gotchas.
- `evals/`: output evals, trigger queries and the registry fixtures they use.

## Related skills

- `agentskills-research`: refreshes the Agent Skills spec pin. This skill does not.
- `skill-judge`: scores a skill after its content changed. This skill records review state; it does not grade.
