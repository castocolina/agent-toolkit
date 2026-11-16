# Gemini run troubleshooting

Read this when a Gemini run produced no output for a long time, or looks hung. The `timeout --kill-after` wrapper in `SKILL.md` already bounds every run; this file only helps describe the symptom accurately in the report. Stop only the PID you launched (never search for processes by name, never `pkill -f gemini`).

## Hung run

`$pid` is the `timeout` process recorded at launch; Gemini is its child, so inspect the child. When the shell changed since the launch (a new tool call), `$pid` is empty: read the saved PID file first with `pid=$(cat gemini.pid)` (the file `SKILL.md` step 3 writes), and stop if `kill -0 "$pid"` fails because the run already ended.

```bash
child=$(pgrep -P "$pid")
ps -o pid,etime,pcpu,stat,command -p "$child"
lsof -p "$child" 2>/dev/null | grep -c ESTABLISHED
```

An `ESTABLISHED` count of 0 with 0% CPU supports "hung". Report these symptoms with the exit code, then follow `SKILL.md` step 4: ask before retrying. To stop early: `kill -TERM "$pid"` (or `kill -TERM "$(cat gemini.pid)"` when the PID came from the file).
