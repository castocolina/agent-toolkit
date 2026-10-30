# Gemini CLI models

Default to `gemini-3-pro-preview` unless the user specifies another model or a material latency/cost constraint changes the choice. Confirm availability with `gemini --help`/CLI errors rather than relying on stale claims.

| Model | Choose when |
|---|---|
| `gemini-3-pro-preview` | Complex review and broad reasoning; default |
| `gemini-3-flash` | Latency matters more than depth |
| `gemini-2.5-pro` | Compatibility requires the prior generation |
| `gemini-2.5-flash` / `gemini-2.5-flash-lite` | Cost/throughput dominates and the CLI account exposes them |
