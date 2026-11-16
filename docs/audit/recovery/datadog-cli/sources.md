# Sources: datadog-cli (skill, synced, report-only)

Checked 2026-11-16. Analyst review only: no `track` call, no skill-updater run, no edit of the skill, the registry or README.md. Nothing under `skills/datadog-cli` was touched.

## Origins found

1. **Sync source: leonardocouy/cc-datadog** (MIT, default branch `main`, last push 2025-12-23, not archived). `.github/workflows/sync-datadog-cli.yaml` (present in this repo, daily cron) clones it, replaces `skills/datadog-cli/` with `cc-datadog/skills/datadog-cli/` and copies the repo-root `README.md` into the skill directory. The synced files are byte-identical to the current upstream: `SKILL.md`, the five `references/*.md` and `README.md` all matched `gh api contents/...` output (checked 2026-11-16). The last sync commit touching the skill here is `812fc051` (2026-01-19); the upstream last push (2025-12-23) is older, so the copy is current.
2. **Tool the skill drives: leonardocouy/datadog-cli** (npm `@leoflores/datadog-cli`, MIT, last push 2025-12-22, latest published version 1.1.0 on 2025-12-22, bin `datadog`, `engines: bun >=1.0.0`, `#!/usr/bin/env bun` shebang). Its `cli.ts` help text and `src/*.ts` were read as the tool's own output (the CLI itself was not executed: `datadog-ci`, `pup` and `datadog-cli` are not installed here and npm is banned; `npx` here is aliased to `pnpm dlx`, so nothing was run).
3. **Origin of the softaworks copy (baseline): softaworks/agent-toolkit at `3027f20f`.** `git diff --stat 3027f20f -- skills/datadog-cli skills/gepetto` is empty, so the softaworks original and the current files are identical; `git show 3027f20f:skills/datadog-cli/SKILL.md` equals the current SKILL.md. The skill entered this repo in `26cbbe5e` ("feat: add datadog-cli skill with automated sync", Leonardo Flores, 2026-01-19).
4. **Vendor documentation the skill's facts rest on:** Datadog docs (sites, API and application keys, log search syntax, metrics and trace metrics, dashboards and dashboard lists APIs) and the Datadog API client OpenAPI spec. They are listed in facts.md and proposed below as `unversioned` rows.

## Credit line

Present and untouched. `skills/datadog-cli/README.md` credits the tool through links only: line 7 `[datadog](https://github.com/leonardocouy/datadog-cli) CLI`, line 18 `leonardocouy/datadog-cli`, line 31 `leonardocouy/cc-datadog`, and line 72 `MIT`. The root `README.md` lines 3 and 5 credit @leonardocouy and softaworks/agent-toolkit for the repository; the root README has no per-skill credit paragraph for skills (only for agents and commands), and none was asked for. No credit line was edited or proposed for removal.

## Registry state (docs/audit/upstream-sources.json)

- `rg -i "datadog|leoflores|leonardocouy"` over the file finds no row for `datadog-cli`; `python3 audit.py --root WT upstreams --registry ...` output (read-only, run 2026-11-16) has no `datadog-cli` row either. The only row that covers the skill indirectly is the repo row `{skill: null, kind: repo, source: softaworks/agent-toolkit, ref: main}` (merge_base `3027f20f`, stale false).
- The `upstreams` exit code was 1 on 2026-11-16, caused by rows of other artifacts only: `crafting-effective-readmes` / `webern/cargo-readme` (`gh: Not Found (HTTP 404)`) and a stale `humanizer` Wikipedia row. Neither belongs to this skill; both are for the controller.
- Stale sources of this skill: none. Synced files equal upstream (checked 2026-11-16). The upstream tool's own latest version (1.1.0) is not pinned anywhere in the skill, so there is nothing to go stale there.

## Proposed registry rows (the controller applies them; I did not edit docs/audit/upstream-sources.json)

Required by the brief: `unversioned` rows for the vendor docs pages used (`upstreams` reports `stale: false` for them, so the date in facts.md is the age marker).

```json
{"skill": "datadog-cli", "kind": "unversioned", "source": "Datadog docs, Getting started with Datadog sites: https://docs.datadoghq.com/getting_started/site/", "ref": null, "credit": "Datadog"}
{"skill": "datadog-cli", "kind": "unversioned", "source": "Datadog docs, API and application keys: https://docs.datadoghq.com/account_management/api-app-keys/", "ref": null, "credit": "Datadog"}
{"skill": "datadog-cli", "kind": "unversioned", "source": "Datadog docs, Log search syntax: https://docs.datadoghq.com/logs/explorer/search_syntax/", "ref": null, "credit": "Datadog"}
{"skill": "datadog-cli", "kind": "unversioned", "source": "Datadog docs, Logs API (Search logs): https://docs.datadoghq.com/api/latest/logs/search-logs-post.md", "ref": null, "credit": "Datadog"}
{"skill": "datadog-cli", "kind": "unversioned", "source": "Datadog docs, Metric distributions: https://docs.datadoghq.com/metrics/distributions/", "ref": null, "credit": "Datadog"}
{"skill": "datadog-cli", "kind": "unversioned", "source": "Datadog docs, Advanced filtering (metric query grammar): https://docs.datadoghq.com/metrics/advanced-filtering/", "ref": null, "credit": "Datadog"}
{"skill": "datadog-cli", "kind": "unversioned", "source": "Datadog docs, APM trace metrics namespace: https://docs.datadoghq.com/tracing/metrics/metrics_namespace/", "ref": null, "credit": "Datadog"}
{"skill": "datadog-cli", "kind": "unversioned", "source": "Datadog docs, Dashboard Lists API (Add items to a dashboard list): https://docs.datadoghq.com/api/latest/dashboard-lists/add-items-to-a-dashboard-list.md", "ref": null, "credit": "Datadog"}
{"skill": "datadog-cli", "kind": "unversioned", "source": "Datadog API client OpenAPI spec, v1 (DashboardLayoutType, DashboardTemplateVariable, LogsListRequest): https://github.com/DataDog/datadog-api-client-python/blob/master/.generator/schemas/v1/openapi.yaml", "ref": null, "credit": "Datadog"}
{"skill": "datadog-cli", "kind": "unversioned", "source": "datadog-cli source and help text (cli.ts, src/logs.ts, src/dashboards.ts, src/metrics.ts): https://github.com/leonardocouy/datadog-cli", "ref": null, "credit": "Leonardo Flores (@leonardocouy)"}
{"skill": "datadog-cli", "kind": "unversioned", "source": "npm registry, @leoflores/datadog-cli (version 1.1.0, engines bun >=1.0.0): https://www.npmjs.com/package/@leoflores/datadog-cli", "ref": null, "credit": "Leonardo Flores (@leonardocouy)"}
```

Optional, not required by the brief (the controller decides; `track` refuses synced skills, so these would only feed `upstreams`): rows for the two sync sources, in the `github` shape the registry already uses.

```json
{"skill": "datadog-cli", "kind": "github", "source": "leonardocouy/cc-datadog", "ref": "main", "credit": "Leonardo Flores (@leonardocouy)"}
{"skill": "datadog-cli", "kind": "github", "source": "leonardocouy/datadog-cli", "ref": "main", "credit": "Leonardo Flores (@leonardocouy)"}
```

Note: the `github` rows need `last_reviewed`/`status` fields written by `track` in other rows; `validate_entry` was not run on these proposals (I did not touch the registry), so check them before applying.

## Stale source dates

| source | state | date checked |
|---|---|---|
| leonardocouy/cc-datadog (sync source) | not stale: all 7 synced files byte-identical to `main` | 2026-11-16 |
| leonardocouy/datadog-cli (tool) | not stale for the skill; skill text has drifts from the tool, listed in facts.md | 2026-11-16 |
| softaworks original at `3027f20f` | identical to current files | 2026-11-16 |
