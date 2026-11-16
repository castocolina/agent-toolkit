# codex: sources (checked 2026-11-07)

## Origins found

1. Original author: skills-directory/skill-codex (MIT, "Copyright (c) 2026 skills-directory"). Evidence: `skills/codex/README.md` (unchanged since the softaworks import `3027f20f`) tells the reader to `git clone git@github.com:skills-directory/skill-codex.git`; its opening line ("Leave a star") and the "Thinking Tokens" section are that repo's README. The baseline `dbff837f:skills/codex/SKILL.md` equals upstream's SKILL.md at commit `d53a022b8d` (2025-12-23) except for the softaworks edits: the description sentence "Uses GPT-5.2 by default...", the rewritten step 1 ("Default to gpt-5.2"), `xhigh` dropped from the `--config` line, and the added Model Options and CLI Version sections (checked with a diff). Upstream today keeps the skill at `plugins/skill-codex/skills/codex/SKILL.md` (last change `f81c9b44f3`, 2026-10-21).
2. Intermediary: softaworks/agent-toolkit, `skills/codex` (identical to the baseline at `3027f20f`; last commit there `06825f0466`, 2026-01-18). Added the Model Options and CLI Version text, which this artifact has since dropped on merit (record rows s012, s015).
3. Our own rewrite: `de35b734` (judge-driven audit fixes), the source of the current SKILL.md.

Credit status: no credit line exists for skills-directory/skill-codex (the only trace is the install URL). Softaworks is credited at repo level in the root README ("Fork of softaworks/agent-toolkit") but not on this skill. No registry row exists for `codex` (the existing `codex-plan` row is `local`).

### Credit line to add (skills/codex/README.md, end of file under a "Credits" heading, wording as in `skills/design-system-starter/README.md`)

```text
Adapted from [skills-directory/skill-codex](https://github.com/skills-directory/skill-codex) (MIT) through [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit).
```

Keep the existing `git clone ... skills-directory/skill-codex` line's mention of the origin when the install command is corrected (facts.md, row "install command in README"); the credit above makes the provenance explicit either way.

## Proposed registry rows (docs/audit/upstream-sources.json, added by hand; `validate_entry` rules checked: kebab-case skill, `github-path` source `owner/repo:path`, non-empty ref, non-empty credit, `unversioned` has `ref` null)

```json
{"skill": "codex", "kind": "github-path", "source": "skills-directory/skill-codex:plugins/skill-codex/skills/codex", "ref": "main", "credit": "skills-directory/skill-codex (MIT), via softaworks/agent-toolkit"}
{"skill": "codex", "kind": "github-path", "source": "softaworks/agent-toolkit:skills/codex", "ref": "main", "credit": "softaworks"}
{"skill": "codex", "kind": "unversioned", "source": "Codex non-interactive mode: https://learn.chatgpt.com/docs/non-interactive-mode", "ref": null, "credit": "OpenAI"}
{"skill": "codex", "kind": "unversioned", "source": "Codex CLI command-line options: https://learn.chatgpt.com/docs/cli/reference", "ref": null, "credit": "OpenAI"}
{"skill": "codex", "kind": "unversioned", "source": "Codex models: https://learn.chatgpt.com/docs/models", "ref": null, "credit": "OpenAI"}
{"skill": "codex", "kind": "unversioned", "source": "Codex configuration reference: https://learn.chatgpt.com/docs/config-file/config-reference", "ref": null, "credit": "OpenAI"}
{"skill": "codex", "kind": "unversioned", "source": "Codex CLI: https://learn.chatgpt.com/docs/cli", "ref": null, "credit": "OpenAI"}
```

Each `github-path` source resolves today (`gh api repos/<o>/<r>/contents/<path>?ref=main` lists `SKILL.md`). The docs moved: `developers.openai.com/codex/...` answers `308` to `learn.chatgpt.com/docs/...`; the last two rows use the learn.chatgpt.com URL that was actually read. Known limit (plan 14 Step 5): `upstreams` never reports an `unversioned` row stale.

## skill-updater style review (REVIEW ONLY; no `track` call, no edit)

Method: skill-updater steps 2, 4 and 6 read by hand. There are no `codex` rows yet, so `upstreams` has nothing to report for this artifact and was not run; the upstream change was read directly: the current upstream SKILL.md against ours, and the upstream commit list since the baseline's origin point (`d53a022b8d`, 2025-12-23). Step 6, the model-validity probe, was not run: the brief's rail 4 bars LLM lanes for implementers and no `pi` runner was started; the coordinator may run it. Rules of the current SKILL.md that counter a model habit: "never redirect stderr to /dev/null by default" (models add `2>/dev/null`) and "do not silently retry". Both should stay (one probe cannot show the habit absent).

Adopt / adapt / ignore for the restore brief:

| upstream change (skills-directory/skill-codex) | decision | reason |
| --- | --- | --- |
| `4d4cb3aadf` remove `--full-auto` (codex 0.161 rejects it on `exec`), `f81c9b44f3` | adopt | tool output and the docs agree (facts.md); the current SKILL.md and the eval still name the flag. Say `--sandbox workspace-write` is enough, and name `--approve-for-me` as the way to ask for automatic approval review when the user authorizes it. |
| `97a6da6fca` consent gate for `--skip-git-repo-check` (inside Git omit it; outside, only with approval; resume does not inherit approval) | adapt | matches the lost baseline guard (record row s014); keep our shorter wording and our ask-less rule: ask only when it blocks the run. |
| stdin note (`codex exec` appends piped stdin to a prompt argument, so a harness with an open stdin hangs; redirect `</dev/null` or pass the prompt on stdin) | adapt | the help text confirms the append behavior (`<stdin>` block); the hang symptom is upstream's observation, not verified here, so word it as a harness caution. |
| `849b4d947c` prompt as the final positional argument | adopt | one clause in the command assembly line (s009 restore). |
| model lists (`gpt-5.3-codex`, `gpt-5.6-*`, `gpt-6-*`, `gpt-6.1-sol`), default `gpt-6-astra` at `high`, per-model effort ceilings, legacy-model rejection note | adapt | keep the idea that the model and effort are chosen from what the CLI offers, but as a pointer to `codex debug models` and the models page; never pin an id (rail 3, plan 14 Global Constraints). |
| execution-timeouts table (150s to 1800s per effort; "no intermediate output; output file silently empty if killed") | adapt | keep the principle (run synchronously; if backgrounded, give a long timeout and treat an empty output file as a killed run) without the unverified numbers. |
| `9598bf1456`, `71343e4e54`, `e5f6944d7f` "Critical Evaluation of Codex Output" (peer, not authority; check disagreements; identify yourself as Claude when resuming) | adapt, optional | new relative to the baseline, so it is an addition, not a recovery; a capable model tends to relay tool output without checking it, which makes the rule plausible. Coordinator decides; if adopted, keep it to a few lines and keep stderr preserved in the resume example. |
| step 1 asks model AND effort in one AskUserQuestion prompt | ignore | conflicts with the current ask-less rule (record row s013); the choice is resolved from the request or the configured default. |
| `2>/dev/null` everywhere (README, resume example) | ignore | contradicts the deliberate stderr safety-fix; the README still carries it and needs the correction listed in facts.md. |
| plugin-marketplace conversion, MIT file, `openpackage.yml` | ignore | distribution of the upstream repo; this repo ships its own plugin. |

## Other findings for the restore dispatch (outside the record rows)

- `skills/codex/README.md` still describes the pre-fix behavior (stderr hidden with `2>/dev/null`, `--full-auto`, models `gpt-5` / `gpt-5-codex`, effort `low|medium|high`, install by cloning upstream). Its sections are `present` by the presence check because the file never changed, so no record row names them; they now contradict the current SKILL.md. Fix them as facts.md says; keep the "Leave a star" line and add the credit line above.
- `.claude-plugin/marketplace.json` (plugin `codex`, `description`) and the generated `dist/plugins/codex/skills/codex/SKILL.md` still carry the baseline description with "Uses GPT-5.2 by default...". `python3 scripts/build_plugins.py` regenerates `dist/`; the marketplace description needs the current frontmatter text (outside `skills/codex/`, so the scope allowlist must permit it).
- Root `README.md` skills table row for `codex` says "Advanced code analysis with GPT-5.2".
- `skills/codex/evals/evals.json` eval `requested-edit` asserts `--full-auto`; edit it as facts.md says (evals may be edited openly). Add a scenario for a fresh invocation with a named model/effort (it would have failed before the s009 restore) and for `--skip-git-repo-check` outside a Git repo (s014).
- `.claude/commands/sync-skills-readme.md` also names GPT-5.2; it is not an artifact of this batch and is only reported.
