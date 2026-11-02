# Create custom subagents (synthetic excerpt of the new page)

## Supported frontmatter fields

Only `name` and `description` are required.

| Field | Description |
| :- | :- |
| `name` | Unique identifier, at most 256 characters, no colon |
| `description` | When Claude should delegate to this subagent |
| `tools` | Tools the subagent can use; inherits all tools if omitted |
| `model` | `sonnet`, `opus`, `haiku`, a full model ID, or `inherit` |
| `maxTurns` | Maximum number of agentic turns before the subagent stops |
| `skills` | Skills to inject into the subagent's context at startup |
| `color` | One of eight named display colors |
| `timeoutSeconds` | New: wall-clock limit in seconds; the subagent is stopped when it is exceeded |
