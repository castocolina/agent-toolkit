---
name: codex
description: "Run or resume OpenAI Codex CLI tasks with `codex exec` or `codex exec resume`, choosing permissions for read-only analysis or user-authorized workspace edits and reporting the outcome. Use when asked to invoke Codex for review, debugging, refactoring, automated edits, or continuation of an existing session. Not for installing the CLI, configuring credentials, conceptual explanations, summarizing prior output without invocation, or other vendors' CLIs."
---

# Codex CLI

## Preflight

1. Check availability and version with `codex --version`. If absent or unsupported, stop and report the exact error; do not guess flags, and give no command, not even a hypothetical "once it is installed" one.
2. When option support or resume syntax is uncertain, inspect installed `codex exec --help` and `codex exec resume --help` before constructing the command.
3. Prepare the invocation in this order:
   1. Pick the sandbox: the narrowest one that satisfies the request (see Run).
   2. Resolve model and effort (high for architecture/refactor/security, medium for features/bugs, low for formatting/docs). Omit `-m` to run the user's configured default; pass a model only when the user names one or the task needs a specific one, and read valid ids from `codex debug models` instead of writing one from memory. As one decision: use the configured default model and the effort from the mapping; ask only when the request conflicts with the configured default or names an effort the model does not support.
   3. Get authorization for gated flags. Confirm required permissions before execution (see Authorization and gotchas).
   4. Assemble the command: flags first, then `resume` if continuing a session, then the prompt as the final argument.
   5. Run it and capture stdout and stderr in separate logs (see Run).
   6. Report the model, effort, sandbox, and whether edits actually occurred.

## Run

Choose the narrowest sandbox that satisfies the request:

- Analysis/review: `--sandbox read-only`.
- Requested local edits: `--sandbox workspace-write`; when the user explicitly asks Codex to perform the edits and authorizes automatic approval review, add `--approve-for-me` (it routes approval requests through automatic review inside the workspace-write sandbox; flag listed by `codex exec --help` on codex-cli 0.162.1, checked 2026-11-13; confirm it there before use). For a command proposal or edits without that authorization, omit it and explain the approval boundary. `--full-auto` is rejected by current CLIs (`unexpected argument` on codex-cli 0.162.1); never use it.
- Network: network need is not permission for broad filesystem access. Use the narrowest supported network/workspace configuration. Reserve `--sandbox danger-full-access` for an explicitly approved task where narrower configuration cannot work: name it and ask the user before escalating to it. The narrower option is the workspace-write network setting, `-c sandbox_workspace_write.network_access=true` together with `--sandbox workspace-write`; try it before considering `danger-full-access`. Confirm the key against the config reference (it describes it as allowing outbound network access inside the workspace-write sandbox) at https://learn.chatgpt.com/docs/config-file/config-reference, checked 2026-11-08; `codex exec --help` documents `-c, --config <key=value>` and `--sandbox`.

Model and effort: `-m, --model <MODEL>` and `-c model_reasoning_effort="<level>"` (`-c, --config <key=value>`, the value parsed as TOML). Levels are `low`, `medium`, `high`, `xhigh`, and on some models `max` and `ultra`; `codex debug models` lists each model's `slug`, `default_reasoning_level` and `supported_reasoning_levels`, and `codex exec --help` lists the flags. When the CLI has no `debug models`, read https://learn.chatgpt.com/docs/models. Flags go before the prompt, which is the final positional argument. Checked 2026-11-07 against codex-cli 0.162.1 and https://learn.chatgpt.com/docs/config-file/config-reference.

Git context: inside a Git repository (check with `git -C <dir> rev-parse --is-inside-work-tree`) omit `--skip-git-repo-check`. Outside one, Codex refuses to run; include the flag only with the user's approval to run there, and pass it again on every invocation including `resume` (source: https://learn.chatgpt.com/docs/non-interactive-mode, checked 2026-11-07).

Put flags before the `resume` subcommand. Use `-C <dir>` when the requested project is not the current directory.

Capture stdout and stderr separately (for example, `>codex.stdout.log 2>codex.stderr.log`). By default, keep stderr available in a log and do not replay it to the user on success; display it only when diagnosing an error or when it contains a relevant warning. Never redirect stderr to `/dev/null` by default: it can contain the only useful failure diagnostics. If reasoning/progress noise must be hidden, filter only known progress lines while retaining warnings and all output on non-zero exit. On failure, report actual diagnostics and stop; do not silently retry.

## Resume

When the user says the latest session was in another project or directory, do not use `--last`: resume by session id (see the fallback below) and say how you confirmed the id's directory. Use `codex exec resume --last` only after confirming the most recent session belongs to the intended repository/task; `--last` can select another project's session. Resume configuration is inherited from the original run; do not add model/sandbox configuration unless explicitly requested and supported. Pass the follow-up as a single-quoted final argument; for long or untrusted text pass `-` and feed it on stdin from a prompt file (`< prompt.md`; `codex exec resume --help` documents `-` as reading the prompt from stdin, checked 2026-11-13)—never interpolate arbitrary user text into shell syntax. Example shape: `codex exec resume --last` (add `--skip-git-repo-check` before `resume` only under the Git context rule in Run).

Confirm the session belongs to the intended repository/task: `codex exec resume --help` documents `--all` as "Show all sessions (disables cwd filtering)", so without `--all` the session list is scoped to the current directory. Run from the intended repository directory, leave `--all` off, and check that the resumed session's earlier context matches the task before relying on it (checked 2026-11-08 against codex-cli 0.162.1). `codex exec resume` takes no `-s` or `-C`; run it from the intended directory and keep the original session's sandbox (checked with `codex exec resume --help`, codex-cli 0.162.1, 2026-11-13).

Complete example with a quoted prompt argument and separate logs:

```bash
codex exec resume --last "Continue the review and list only new findings." >codex.stdout.log 2>codex.stderr.log
```

To send a longer follow-up from a prompt file instead, pass `-` as the prompt (the help says `-` reads the prompt from stdin): `codex exec resume --last - < prompt.md >codex.stdout.log 2>codex.stderr.log`.

Fallback when `--last` belongs to another project: resume by id instead, since `[SESSION_ID]` accepts a session UUID or thread name (UUIDs take precedence): `codex exec resume <SESSION_ID> "Continue the review." >codex.stdout.log 2>codex.stderr.log`.

## Authorization and gotchas

- Ask before `--approve-for-me`, `danger-full-access` or (outside a Git repository) `--skip-git-repo-check` unless the user already authorized that exact scope. If denied, do not execute; offer a narrower mode.
- Never assume `--last` is safe solely because it is recent; cross-project session selection can disclose or modify the wrong workspace.
- Never interpolate task text directly into shell syntax. Use a safely quoted argument or stdin to avoid command expansion.
- `--full-auto` fails with an unexpected-argument error on codex-cli 0.162.1 (checked with `codex exec --help` 2026-11-13), so never copy it from older examples; see Run for the supported approval flag.
- Never send stderr to `/dev/null`: it carries the only failure diagnostics (see Run for separate logs).
- Preserve warnings and partial results in the report. State model/effort/sandbox and whether edits actually occurred; do not imply completion from a launched process alone.
