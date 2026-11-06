---
name: skill-updater
description: "Use when checking whether a skill, command or agent in this repo is still current, has drifted or is out of date against its upstream sources in the docs/audit/upstream-sources.json registry and against the models it targets: stale content, a source that moved or was renamed, an unreachable source, or a rule that may no longer match model behavior. Records the result with audit.py track. Not for creating a skill, not for judging or grading one (skill-judge), not for refreshing the Agent Skills spec pin (agentskills-research), not for only running audit.py upstreams, not for fixing audit.py itself, and not for editing the synced skills gepetto and datadog-cli."
---

# Skill updater

Review one artifact against `docs/audit/upstream-sources.json` and the model it targets. Record each source row with `audit.py track` and the reasoning in `docs/audit/<date>/updates.md`. Edit the artifact only when the invoker asked for the update itself.

Every `track` call below passes `--registry docs/audit/upstream-sources.json`: without it `track` writes the registry under the checkout that holds `audit.py`, not the one you stand in. Flags: `python3 scripts/audit/audit.py track --help`.

## Procedure

1. **Resolve scope.** `skills/<n>/`, `commands/<n>.md` or `agents/<n>.md`; the path must exist. `gepetto` and `datadog-cli` are synced: refuse, give no `track` command, stop.
2. **Find the rows** whose `skill` is the name. No row other than `kind: local` (every command and agent, and a skill with no upstream): go to step 6, then record the source-less call in step 7. A credit line naming an upstream with no row: propose the row in `updates.md` with `credit` copied verbatim, still run step 6, and give no `track` call at all (no source row, no source-less `local` row); `track` cannot create a source row. Otherwise run `python3 scripts/audit/audit.py upstreams --registry docs/audit/upstream-sources.json` and take this artifact's rows (it skips `local` rows). It exits 1 when any row of any artifact fails, so read the rows, not the exit code.
3. **Checkpoint: branch on `error`.** A non-empty `error` is never "no change".

   | `error` | cause | action |
   |---------|-------|--------|
   | null | success | step 4 |
   | `list index out of range` on a `github-path` row | the commits query for the path returned `[]` | step 5 |
   | starts with `invalid entry:` | the row is malformed | propose the corrected row in `updates.md`; give no `track` command for any row of this artifact (a call rewrites every sibling row and fails on a malformed one): re-run the review once the registry is corrected |
   | `no local commit for source material` | `ours_updated` reads `git log` on `skills/<n>/SKILL.md` and `skills/<n>/references/` only, so a README, eval or script commit does not count | stop and report that the local side is empty; record nothing; do not edit or commit the artifact to make the row pass |
   | anything else (`HTTP 401`, `HTTP 403`, `API rate limit exceeded`, a repo-level `Not Found (HTTP 404)`, a timeout) | auth, rate limit, network, repo gone | run `gh auth status`, retry once; still failing: `unreachable`, no tree search |

4. **Checkpoint: contents test, then classify.** On every `github-path` row with `error: null`, whatever `stale` says, test the row's `new_path` when set, otherwise the path after the colon in `source`: `gh api --silent 'repos/<o>/<r>/contents/<path>?ref=<ref>'`. Exit 0: classify. `Not Found (HTTP 404)`: moved, step 5 even when `stale: false` (a 404 on the stored `source` path while `new_path` resolves is not a move). Any other error: the last row of the step-3 table; never classify a change you have not seen.
   - `stale: false` is a timestamp signal only (an unrelated newer local commit also yields it). With `last_upstream_sha`, run the compare below against the current `<ref>` and inspect any patch as for `stale: true`; with none, read the current upstream against the artifact. Only then record `current`. An `unversioned` row: see Gotchas.
   - `stale: true`: get the upstream change. With `last_upstream_sha` on the row: `gh api 'repos/<o>/<r>/compare/<last_upstream_sha>...<ref>' --jq '.files[] | select(.filename | startswith("<path>")) | .patch'` (drop the `select` on a `github` row). Without it: `gh api --paginate 'repos/<o>/<r>/commits?path=<path>&sha=<ref>&since=<last_reviewed>T00:00:00Z&per_page=100' --jq '.[].sha'` (drop `path=<path>&` on a `github` row), then each commit's patch from `repos/<o>/<r>/commits/<sha>` (`.files[].patch`). Page or patch retrieval that fails or is cut short: the review is unresolved. Make no `track` call for this artifact, on any row: every call stamps `last_reviewed` on all its sibling rows, which can be the fallback base. Log it in `updates.md` and retry later. No `last_reviewed` either, or a `wikipedia` row: read the current upstream against the artifact.
   - Decide `adopt`, `adapt` or `ignore` per change, write each with a one-line reason to `updates.md`, and record `stale` whatever the decision, with `--sha` set to the newest commit you read so the next review has a diff base.
5. **Checkpoint: tree search** (path gone only).
   - List the tree at the row's `ref`: `gh api 'repos/<o>/<r>/git/trees/<ref>?recursive=1' --jq '.tree[] | .path'`.
   - A candidate is a directory or file whose last segment, with any `.md` dropped, equals the old path's last segment (`.md` dropped) or the artifact name. A `SKILL.md` names its directory, not itself.
   - Zero candidates: `unreachable`; say in `updates.md` that the old path is gone and nothing matched.
   - One candidate: confirm it with `gh api 'repos/<o>/<r>/commits?path=<candidate>&sha=<ref>&per_page=1' --jq '.[0].sha'`, then read the candidate's current content against the artifact and decide adopt/adapt/ignore as in step 4 before recording `path-moved --new-path <candidate> --sha <sha>`. Content review not completed: make no `track` call, and mark the relocation and the review unresolved in `updates.md`.
   - Several: list them in `updates.md`, record no `path-moved`, ask the user which one.
   - Rewriting `source` is a user decision: propose it in `updates.md`. A recorded `new_path` makes `upstreams` query the new path while `source` stays.
6. **Checkpoint: model probe**, for every artifact, rows or not. See Model-validity pass.
7. **Record.** One call per source row, `--source` copied exactly from the row: `python3 scripts/audit/audit.py track --registry docs/audit/upstream-sources.json --artifact NAME --source SOURCE --status STATUS [--sha SHA] [--model MODEL] [--new-path PATH]`. A row that already has `new_path` gets `--new-path <that value>` on every call, unless the user corrected the source or step 5 confirmed a replacement candidate (then pass the new candidate; `source` stays pending the user's decision). An artifact with no source row gets one source-less call, which writes its `local` row: `track --registry docs/audit/upstream-sources.json --artifact NAME --artifact-kind skill|command|agent --status current --model MODEL`.
8. **Judge** the artifact with `skill-judge` when its content changed: `commands/<n>.md` or `agents/<n>.md` itself, or for a skill `SKILL.md` or `references/` (the only files `ours_updated` reads, step 3).

## Adopt, adapt or ignore

- **adopt**: the upstream rule still applies to this artifact unchanged. Port it as written.
- **adapt**: it applies, but the local artifact diverges on purpose (a repo convention or ruling). Port the intent, keep the difference, name it.
- **ignore**: the change targets something this artifact does not do, or contradicts a repo ruling. Name which.

Example: upstream `writing` adds a ban on hedging words, moves its banned-word list into a separate `words.txt`, and adds a plugin-marketplace install section. The hedging ban applies as is: adopt. The new words apply, but our skill keeps its list inline on purpose: adapt, port the words into the inline list. The marketplace section is distribution this skill does not do: ignore. The row is recorded `stale` in all three cases.

## Model-validity pass

For each rule that exists to counter a model behavior (a substitution to undo, a habit to suppress):

1. Write one prompt that should elicit the behavior: the rule's trigger task as a user would ask it, without the skill loaded, long enough for the habit to show (about 150 words of prose for an em dash rule). The behavior is present if it appears once.
2. Run it once through the repo's tool-less probe lane. `MODEL` is the model the invoker names, else `router-env/my-referee-two`: `printf '%s\n' "$PROMPT" | $(python3 scripts/audit/audit.py pi-cmd runner --model MODEL)`. It reads the prompt on stdin, runs with no tools, and mutates nothing.
3. Behavior present: keep the rule. Behavior absent: propose removal. One run is weak evidence, so never edit or delete the rule yourself. No prompt can elicit it: keep the rule and say so.
4. Write per rule to `updates.md`: the rule, the prompt, what the output showed, keep or propose removal. Pass the same `--model MODEL` to `track`; it writes `reviewed_for_model` on every row of the artifact.

## Gotchas

- **A moved path can look fine.** The commits-by-path query on a deleted path returns the commit that deleted it, so a moved `github-path` source prints `error: null`, `stale: true`. That is why step 4 runs the contents test before any adopt/adapt/ignore.
- **`kind: unversioned`** sources (a post, a talk) have no commit: `upstreams` prints `stale: false` without comparing. Read the source, then record `current` with no `--sha`.
- **The `kind: repo` row** (`skill` null) is the fork origin for the CI drift check. `track` cannot address it; never track it.
- **`track` drops `new_path`** on any status but `path-moved` unless `--new-path` is passed again. `upstreams` then queries the deleted path, which returns the deleting commit and reads as a fresh `stale`.
- **Never search the tree or record `path-moved` on an auth, rate-limit or repo-level error.** The tree query fails the same way, and a wrong `new_path` silently redirects every later `upstreams` run.
- **Always pass `--model MODEL` to both `pi-cmd runner` and `track`.** `pi-cmd` without `--model` defaults to `router-env/my-referee-one`, not the probe default, so `reviewed_for_model` would name a model the probe never ran on.
- **`status`** is the comparison state only. `adopt`, `adapt` and `ignore` live in `updates.md`, never in the registry.
- **Never remove, shorten or reword a credit**, including when you adopt or adapt upstream text. Credit lines and the row's `credit` field are provenance: they say where to fetch the upstream from. `audit.py check --strict` fails with `missing_credit` when a row's `credit` text no longer appears verbatim in `SKILL.md`, `README.md` or `references/*.md`; restore the credit, never delete the row.
