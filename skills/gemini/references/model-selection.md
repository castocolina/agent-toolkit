# Gemini CLI models

`gemini-3-pro-preview` is the default. Preview models need preview features enabled for the account; when the CLI rejects one, report the error and offer `gemini-2.5-pro` instead of guessing another name. `-m` sets the main model only; subagents such as `codebase_investigator` keep their own, so usage reports can show other models.

| Model | Choose when |
|---|---|
| `gemini-3-pro-preview` | Default: deep review, broad reasoning |
| `gemini-3.1-pro-preview` | The account has it (rolling out; `/model` > Manual lists it) and the user wants the newest Pro |
| `gemini-3-flash-preview` | Latency matters more than depth |
| `gemini-2.5-pro` | No preview access; `auto` and `pro` resolve to it then |
| `gemini-2.5-flash`, `gemini-2.5-flash-lite` | Cost or throughput dominates (aliases `flash`, `flash-lite`) |

Sources: https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/model.md and https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/cli-reference.md, checked 2026-11-07. Model names change often: `/model` in the CLI lists what the account can use, and it wins over this table.
