---
name: codex
description: "Run or resume OpenAI Codex CLI tasks with `codex exec` or `codex exec resume`, choosing permissions for read-only analysis or user-authorized workspace edits and reporting the outcome. Use when asked to invoke Codex for review, debugging, refactoring, automated edits, or continuation of an existing session. Not for installing the CLI, configuring credentials, conceptual explanations, summarizing prior output without invocation, or other vendors' CLIs."
---

# Codex CLI

## Preflight

1. Check availability and version with `codex --version`. If absent or unsupported, stop and report; do not guess flags.
2. When option support or resume syntax is uncertain, inspect installed `codex exec --help` and `codex exec resume --help` before constructing the command.
3. Resolve task intent, model (default `gpt-5.2`), and effort (high for architecture/refactor/security, medium for features/bugs, low for formatting/docs). Ask only when an unresolved choice affects the result. Confirm required permissions before execution.

## Run

Choose the narrowest sandbox that satisfies the request:

- Analysis/review: `--sandbox read-only`.
- Requested local edits: `--sandbox workspace-write`; when the user explicitly asks Codex to perform the edits and authorizes autonomous execution, include `--full-auto`. For a command proposal or edits without that authorization, omit it and explain the approval boundary.
- Network: network need is not permission for broad filesystem access. Use the narrowest supported network/workspace configuration. Reserve `--sandbox danger-full-access` for an explicitly approved task where narrower configuration cannot work.

Use `--skip-git-repo-check` when needed for this harness. Put flags before the `resume` subcommand. Use `-C <dir>` when the requested project is not the current directory.

Capture stdout and stderr separately (for example, `>codex.stdout.log 2>codex.stderr.log`). By default, keep stderr available in a log and do not replay it to the user on success; display it only when diagnosing an error or when it contains a relevant warning. Never redirect stderr to `/dev/null` by default: it can contain the only useful failure diagnostics. If reasoning/progress noise must be hidden, filter only known progress lines while retaining warnings and all output on non-zero exit. On failure, report actual diagnostics and stop; do not silently retry.

## Resume

Use `codex exec resume --last` only after confirming the most recent session belongs to the intended repository/task; `--last` can select another project's session. Resume configuration is inherited from the original run; do not add model/sandbox configuration unless explicitly requested and supported. Pipe the follow-up prompt as stdin, with shell-safe quoting or a heredoc—never interpolate arbitrary user text into shell syntax. Example shape: `codex exec --skip-git-repo-check resume --last`.

## Authorization and gotchas

- Ask before `--full-auto` or `danger-full-access` unless the user already authorized that exact scope. If denied, do not execute; offer a narrower mode.
- Never assume `--last` is safe solely because it is recent; cross-project session selection can disclose or modify the wrong workspace.
- Never interpolate task text directly into shell syntax. Use a safely quoted argument or stdin to avoid command expansion.
- Preserve warnings and partial results in the report. State model/effort/sandbox and whether edits actually occurred; do not imply completion from a launched process alone.
