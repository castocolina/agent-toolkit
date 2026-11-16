# gemini sources

## Origin

- `skills/gemini` was added by commit 06825f04 ("feat: add 23 curated skills") from softaworks/agent-toolkit, `skills/gemini/` (identical to the baseline text at 3027f20f). No registry row exists for it today.
- Credit gap: `skills/gemini/README.md` has no origin line (the root README only says the repo is a fork of softaworks/agent-toolkit by @leonardocouy). Line to add to `skills/gemini/README.md`, matching `skills/database-schema-designer/README.md`:

  `Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy.`

## Proposed registry rows (docs/audit/upstream-sources.json)

```json
{"skill": "gemini", "kind": "github-path", "source": "softaworks/agent-toolkit:skills/gemini", "ref": "main", "credit": "softaworks"}
{"skill": "gemini", "kind": "unversioned", "source": "Gemini CLI reference: https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/cli-reference.md", "ref": null, "credit": "Google"}
{"skill": "gemini", "kind": "unversioned", "source": "Gemini CLI headless mode: https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/headless.md", "ref": null, "credit": "Google"}
{"skill": "gemini", "kind": "unversioned", "source": "Gemini CLI model selection: https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/model.md", "ref": null, "credit": "Google"}
```

## Skill-updater style review (review only, no track call)

- Upstream softaworks `skills/gemini/SKILL.md` on main still recommends `--approval-mode yolo` for background runs, gemini-3-pro-preview, `pkill -9 -f`, and CLI v0.16.0. All of it conflicts with the current reviewed text.
- ignore: upstream's yolo-for-background advice (unsafe; the current default-mode headless plan is correct), pkill by name, pinned v0.16.0, benchmark and price claims.
- adopt: none.
- adapt: none. The one thing worth carrying is the hung-process symptom list (0% CPU, no network), already rated drop-pending; restore it to references/ only if the user rejects the drop.
- Facts the restore brief must handle: add a source for the headless denial and plan-to-yolo claims (not on the pages read) and for `GEMINI_CLI_TRUST_WORKSPACE`; the installed CLI was unusable, so `--help` was not run.
