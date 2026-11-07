# Gemini run troubleshooting

Read this when a Gemini run produced no output for a long time, looks hung, or ran out of memory. The `timeout --kill-after` wrapper in `SKILL.md` already bounds every run; this file only helps describe the symptom accurately in the report. Stop only the PID you launched (never search for processes by name, never `pkill -f gemini`).

## Hung run

Likely hung when, well past the expected duration (20+ minutes is the old rule of thumb, far beyond the 300 or 900 s bound):

- CPU stays at 0%.
- The process is sleeping (state `S`).
- It holds no established network connections.

`$pid` is the `timeout` process recorded at launch; Gemini is its child, so inspect the child:

```bash
child=$(pgrep -P "$pid")
ps -o pid,etime,pcpu,stat,command -p "$child"
lsof -p "$child" 2>/dev/null | grep -c ESTABLISHED
```

An `ESTABLISHED` count of 0 with 0% CPU supports "hung". Report these symptoms with the exit code, then follow `SKILL.md` step 4: ask before retrying. To stop early: `kill -TERM "$pid"`.

## Out of memory or too much context

For a very large codebase:

- Narrow the scope with `--include-directories` and review one area per run.
- Break the analysis into smaller chunks and combine the verified findings yourself.
- Offer a faster model (see `references/model-selection.md`); do not switch without the user's say.

State the narrower scope under limits in the report.
