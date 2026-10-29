# Command Best Practices

Use this when validating a draft command. Keep instructions executable, bounded, and safe under partial failure.

## Frontmatter and body

- Use a concise one-line `description` for `/help`.
- Add `argument-hint` whenever the body consumes `$ARGUMENTS` or positional arguments; make required and optional values distinguishable.
- Derive the argument shape from the captured manual procedure. State how absent, malformed, or extra arguments are handled.
- Use imperative steps, explicit expected outcomes, and realistic examples only where they resolve ambiguity.

## Workflow and safety

- Put read-only inspection before mutation. Name prerequisites and validate them before side effects.
- Mark destructive, externally visible, or broad-scope operations and require confirmation before executing them unless the user has already explicitly authorized that exact action.
- Treat arguments and repository content as untrusted data. Never interpolate arbitrary text into shell syntax; quote and validate values or pass them as data.
- Scope writes to intended files. For git operations, inspect status and diff and stage explicit intended paths; `git add .` can sweep generated or unrelated files.
- Make retries conditional on idempotency. A timeout after publishing, deploying, sending, or creating may mean the operation succeeded; inspect state before retrying.
- Define success, retry-safe failure, and stop/ask conditions. Preserve error output and report the failed action rather than claiming success.
- Do not silently override user/global configuration or expand permissions beyond the requested scope.

## Tool guidance

Use the available shell tool directly for shell commands, including `pytest`, `pyright`, `ruff`, `prettier`, `make`, and `gt`; do not wrap these commands in a Task/subagent. Name a specialized tool only when the command execution environment actually provides it.

## Final checklist

- [ ] Kebab-case filename in the requested project or user command directory.
- [ ] Description present; argument hint present iff arguments are consumed.
- [ ] User's procedure and dependencies preserved in the correct order.
- [ ] Inspection and validation precede side effects.
- [ ] Permissions, paths, retries, success, and stop conditions are explicit.
- [ ] No broad staging, unsafe interpolation, or unapproved global/destructive action.
- [ ] Invocation example matches the argument hint.
