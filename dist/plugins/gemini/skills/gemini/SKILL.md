---
name: gemini
description: Run the Gemini CLI headless as a second-opinion reviewer for code, architecture or plan reviews and big-context (>200k token) analysis of repositories, multi-directory projects or document sets, then verify its claims before reporting. Use when the user asks to use or run Gemini, wants a second opinion or cross-model review, or has a codebase or doc set too large for one context. Not for Gemini API or SDK integration, installing the CLI, model benchmark comparisons, Codex runs, or having Gemini implement changes.
---

# Gemini CLI review

Gemini is a second analyst, not an authority: every finding is a claim until the source confirms it.

## Defaults

- Model `gemini-3-pro-preview`; a model the user names wins. Read `references/model-selection.md` only when the user weighs speed or cost, or the CLI rejects the model.
- Headless prompt with `-p`, never a positional prompt (see Gotchas).
- `--approval-mode default`. Headless, a tool call that needs approval is denied, not prompted: Gemini can still read (`read_file`, `glob`, `grep_search` are allowed by default) but cannot write files or run shell. That is the read-only review.
- `timeout --kill-after=10s 300`: TERM at 300 s, KILL 10 s later. Use 900 for a >200k-token scope or three or more included directories. Never run unbounded.

| `--approval-mode` | Headless effect | Use |
|---|---|---|
| `default` (CLI default) | reads allowed; writes and shell denied | every review unless the user says otherwise |
| `plan` | read-only while planning, then exits into `yolo` (see Gotchas) | interactive only |
| `auto_edit` | some edits auto-approved | only when the user authorizes edits |
| `yolo` | every tool, shell included, auto-approved | only with explicit user authorization, in a throwaway clone or with `-s` sandbox |

## Workflow

1. **Scope.** Name the target paths and criteria. A plan review with no plan text or path: ask for it; do not launch.
2. **Context boundary.** Gemini's file tools see its cwd plus `--include-directories` (repeat the flag or comma-separate, 5 at most); a path named only in the prompt is unreadable. Rule: `cd` into the first target and pass every other target with `--include-directories`. Send a single file from outside (a plan, a spec) on stdin rather than widening the workspace: `-p` text is appended to stdin. Before launching, list secret-looking files in the cwd and every included directory:
   ```bash
   find <scope> -path '*/.git' -prune -o -type f \( -name '.env*' -o -name '*.pem' -o -name '*.key' -o -name 'id_rsa*' -o -name '*credentials*' -o -name '*.tfstate' \) -print
   ```
   Any hit: keep it out as the workspace gotcha says, or ask the user.
3. **Run or propose.** From a harness, run headless only. An interactive session (`-i`) is always a command for the user to run in their terminal. For a background run, record the `timeout` PID and wait on it; to stop early, `kill -TERM "$pid"`: `timeout` forwards it and sends KILL 10 s later.
   ```bash
   timeout --kill-after=10s 300 gemini -m gemini-3-pro-preview --approval-mode default -p "..." > gemini-review.log 2>&1 & pid=$!
   wait "$pid"; echo "exit $?"
   ```

   When only proposing, say the command was not run and give no findings.
4. **Check the exit.** `0` with a non-empty response is the only complete run. `124` timeout (`137` if KILL was needed), `1` API or auth error, `42` bad arguments, `53` turn limit, `FatalUntrustedWorkspaceError` untrusted folder. Anything else is incomplete: report the code and symptom, never present partial output as a review, and ask before retrying with a longer timeout, a narrower scope or a different mode.
5. **Verify, then report.** Open each cited file and line. Go/no-go per finding: **accepted** only when the source shows it; **rejected** when the source contradicts it (say why); **unverified** when the cited file is unavailable or the evidence is ambiguous. Report accepted findings, rejected and unverified claims, limits (scope, denied tools, timeout), and the exact command and model. Verifying confirms or refutes Gemini's claims only; add findings of your own only when the user asks for your review too.

## Command shapes

Headless review of two directories:

```bash
cd /work/api && timeout --kill-after=10s 300 gemini -m gemini-3-pro-preview --approval-mode default \
  --include-directories /work/web \
  -p "Review /work/api and /work/web for <criteria>. Report findings only; change nothing. For each: severity, file:line, evidence, uncertainty."
```

Plan review with the plan outside the workspace, sent on stdin:

```bash
timeout --kill-after=10s 300 gemini -m gemini-3-pro-preview --approval-mode default \
  -p "The text above is the plan. Review it against this repository for missing failure modes and scalability risks. Cite plan section and file:line." \
  < /work/plan.md
```

Interactive, for the user's terminal:

```bash
cd /srv/payments && timeout --foreground --kill-after=10s 1800 gemini -m gemini-3-pro-preview --approval-mode default \
  -i "Review /srv/payments for risky permissions. Report findings only."
```

## Gotchas

- The workspace (cwd plus included directories) limits only Gemini's file tools, not shell: once shell runs (`yolo`), Gemini can read anything the user can. Never claim the include list protects secrets. A file left out of the prompt is still readable, so to exclude one, run from a cwd that does not contain it or from an isolated copy of the target. A hard boundary with shell enabled needs `-s`/`--sandbox` confirmed to start (Docker, Podman or macOS Seatbelt) on such a cwd, or a genuinely isolated copy.

- A positional prompt (`gemini "..."`) in a TTY opens an interactive session that waits for input. Headless runs use `-p`.
- `timeout` without `--foreground` puts the CLI in a background process group, so an interactive session stops on its first terminal read and sits until killed. Interactive commands need `--foreground`.
- Headless `plan` mode auto-approves leaving the plan and then switches to `yolo` to implement it, so a "read-only" plan review can edit files and run shell. Use `default` for headless reviews.
- Denied tools fail silently: a headless `default` run that needed shell (tests, `git log`) returns a review built from file reads only. State that under limits.
- `FatalUntrustedWorkspaceError`: `--skip-trust` or `GEMINI_CLI_TRUST_WORKSPACE=true` trusts the folder for the session, which also loads its `.gemini/settings.json`, `.env` files and MCP servers. Use either only after the user confirms they trust the repository.
- Never `pkill -f gemini`: it also kills the user's own Gemini sessions. Stop only the PID you launched.
- `-y`/`--yolo` is deprecated; write `--approval-mode yolo`. Check `gemini --version` when a flag is rejected.
