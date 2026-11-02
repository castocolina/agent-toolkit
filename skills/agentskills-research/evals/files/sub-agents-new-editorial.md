# Create custom subagents (synthetic excerpt of the new page)

## Supported frontmatter fields

Just `name` and `description` are needed; every other field is optional.

| Field | Description |
| :- | :- |
| `name` | A unique identifier of up to 256 characters; a colon is not allowed |
| `description` | Tells Claude when to hand work to this subagent |
| `tools` | The tools this subagent may use; all tools are available if omitted |
| `model` | `sonnet`, `opus`, `haiku`, a full model ID, or `inherit` |
| `maxTurns` | The most agentic turns the subagent may take before it stops |
| `skills` | Skills whose content is injected into the subagent at startup |
| `color` | One of eight named display colors |
