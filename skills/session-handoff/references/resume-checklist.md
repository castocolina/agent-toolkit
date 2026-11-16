# Resume Checklist

Extra verification for a handoff whose staleness level is not FRESH, or that cites a missing file. SKILL.md owns the resume steps (list, staleness, load, verify branch, working tree and assumptions, begin); this file adds the environment checks and the stop signals.

## Environment

```bash
# Commits since the handoff's baseline (use the full SHA from "Baseline commit:")
git log --oneline '<baseline>'..HEAD

# A process the handoff says was running (dev server, watcher)
pgrep -af '<process-name>'

# Whether named variables are set, without printing their values
python3 -c 'import os, sys; [print(n, "set" if n in os.environ else "unset") for n in sys.argv[1:]]' STAGING_API_TOKEN DB_POOL_SIZE
```

- Compare the handoff's Files Modified table with `git status`: a listed file that is now clean was committed or reverted; find out which before relying on it.
- Services and environments the handoff names (staging, a local database, a queue) are not checked by any script; confirm each one the first next step depends on.

## Stop and ask the user

| Signal | Likely cause | Do |
|--------|--------------|----|
| Files the handoff cites do not exist | Moved, renamed or reverted | `git log --oneline --follow -- '<path>'`, then re-locate before editing |
| An assumption is now false | Requirements or code changed | Re-plan the next steps with the user |
| A blocker marked unresolved blocks you | Still unresolved | Escalate; do not work around it silently |
| Next steps are vague ("continue the refactor") | Weak handoff | Re-explore the code before implementing |
