# Artifact specs: slash commands and subagents (Claude Code)

command_digest: 564ae70c48564766185724c264b0cf06090f769e55a73ec07382034852564a62
agent_digest: f922066dae75510ff7373ba144d20d38d2fc7f63f330fadad7579cf1feebf8c9
skills: 118879 bytes, sha256 d2a5d07c0d1cef1d1edcf30f38f6b2712ff70ac050e3d50601cd3dadb42f9097
sub-agents: 116225 bytes, sha256 0fc7d550f8580d12fefae642c4c74b84889817cb3c9f41501c38093016448532
plugins-reference: 43335 bytes, sha256 a10a371d18d571e769f99720d4402f3ec13ceb668561266f57145cfa940fa4ed

(excerpt of section 2, Agents, frontmatter table; agent profile is at profile_version: 3)

| Field | Our reading |
| :- | :- |
| `name` | unique id, at most 256 chars, no `:` |
| `description` | when to delegate |
| `tools` | allowlist; all tools if omitted |
| `model` | `sonnet`, `opus`, `haiku`, a full model ID, or `inherit` |
| `maxTurns` | turn cap |
| `skills` | skills injected at startup |
| `color` | one of eight named colors |
