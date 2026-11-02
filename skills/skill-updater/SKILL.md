---
name: skill-updater
description: "Use when checking whether a skill, command or agent in this repo is still current, has drifted or is out of date against its upstream sources in the docs/audit/upstream-sources.json registry and against the models it targets: stale content, a source that moved or was renamed, an unreachable source, or a rule that may no longer match model behavior. Records the result with audit.py track. Not for creating a skill, not for judging or grading one (skill-judge), not for refreshing the Agent Skills spec pin (agentskills-research), not for only running audit.py upstreams, not for fixing audit.py itself, and not for editing the synced skills gepetto and datadog-cli."
---

# Skill updater

Review one artifact against `docs/audit/upstream-sources.json` and the model it targets. Record each source row with `audit.py track` and the reasoning in `docs/audit/<date>/updates.md`. Edit the artifact only when the invoker asked for the update itself.

Every `track` call below passes `--registry docs/audit/upstream-sources.json`: without it `track` writes the registry under the checkout that holds `audit.py`, not the one you stand in. Flags: `python3 scripts/audit/audit.py track --help`.

## Procedure

1. **Resolve scope.** `skills/<n>/`, `commands/<n>.md` or `agents/<n>.md`; the path must exist. `gepetto` and `datadog-cli` are synced: refuse, give no `track` command, stop.
2. **Find the rows** whose `skill` is the name. Only a skill can have source rows; commands and agents have none, so go to step 6 and record in step 7. Otherwise run `python3 scripts/audit/audit.py upstreams --registry docs/audit/upstream-sources.json` and take this artifact's rows. It exits 1 when any row of any artifact fails, so read the rows, not the exit code.
3. **Checkpoint: branch on `error`.** A non-empty `error` is never "no change".

   | `error` | cause | action |
   |---------|-------|--------|
   | null | success | step 4 |
   | `list index out of range` on a `github-path` row | the commits query for the path returned `[]` | step 5 |
   | starts with `invalid entry:` | the row is malformed | propose the corrected row in `updates.md`; record nothing for it |
   | `no local commit for source material` | no commit touches `skills/<n>/SKILL.md` or `skills/<n>/references/` | stop and report that the local side is empty (`git log` covers only those two paths, so a README, eval or script commit does not count); do not edit or commit the artifact to make the row pass; never relocate |
   | anything else (`HTTP 401`, `HTTP 403`, `API rate limit exceeded`, a repo-level `Not Found (HTTP 404)`, a timeout) | auth, rate limit, network, repo gone | run `gh auth status`, retry once; still failing: `unreachable`, never relocate |

4. **Checkpoint: contents test, then classify.** On a `github-path` row with `stale: true`, test the row's `new_path` when set, otherwise the path after the colon in `source`: `gh api --silent 'repos/<o>/<r>/contents/<path>?ref=<ref>'`. A `Not Found (HTTP 404)` means moved: step 5. A 404 on the stored `source` path while `new_path` resolves is not a move. Then classify: `stale: false` is `current`. `stale: true`: read both versions, decide `adopt`, `adapt` or `ignore` per upstream change, write each with a one-line reason to `updates.md`, and record `stale` whatever the decision.
5. **Checkpoint: tree search** (path gone only).
   - List the tree at the row's `ref`: `gh api 'repos/<o>/<r>/git/trees/<ref>?recursive=1' --jq '.tree[] | .path'`.
   - A candidate is a directory or file whose last segment, with any `.md` dropped, equals the old path's last segment (`.md` dropped) or the artifact name. A `SKILL.md` names its directory, not itself.
   - Zero candidates: `unreachable`; say in `updates.md` that the old path is gone and nothing matched.
   - One candidate: confirm it with `gh api 'repos/<o>/<r>/commits?path=<candidate>&sha=<ref>&per_page=1' --jq '.[0].sha'`, then record `path-moved --new-path <candidate> --sha <sha>`.
   - Several: list them in `updates.md`, record no `path-moved`, ask the user which one.
   - Rewriting `source` is a user decision: propose it in `updates.md`. A recorded `new_path` makes `upstreams` query the new path while `source` stays.
6. **Checkpoint: model probe**, for every artifact, rows or not. See Model-validity pass.
7. **Record.** One call per source row, `--source` copied exactly from the row: `python3 scripts/audit/audit.py track --registry docs/audit/upstream-sources.json --artifact NAME --source SOURCE --status STATUS [--sha SHA] [--model MODEL] [--new-path PATH]`. A command or agent gets one source-less call, which writes its `local` row: `track --registry docs/audit/upstream-sources.json --artifact NAME --artifact-kind command|agent --status current --model MODEL`.
8. **Judge** the artifact with `skill-judge` when its content changed. A skill's commit must touch `SKILL.md` or `references/` for `upstreams` to see it: `ours_updated` reads `git log` on those two paths only and ignores `README.md`, `evals/` and `scripts/`.

## Adopt, adapt or ignore

- **adopt**: the upstream rule still applies to this artifact unchanged. Port it as written.
- **adapt**: it applies, but the local artifact diverges on purpose (a repo convention or ruling). Port the intent, keep the difference, name it.
- **ignore**: the change targets something this artifact does not do, or contradicts a repo ruling. Name which.

Example: upstream `writing` adds a ban on hedging words, moves its banned-word list into a separate `words.txt`, and adds a plugin-marketplace install section. The hedging ban applies as is: adopt. The new words apply, but our skill keeps its list inline on purpose: adapt, port the words into the inline list. The marketplace section is distribution this skill does not do: ignore. The row is recorded `stale` in all three cases.

## Model-validity pass

For each rule that exists to counter a model behavior (a substitution to undo, a habit to suppress):

1. Write one short prompt that should elicit the behavior: the task the rule guards, without the skill loaded.
2. Run it once through the repo's tool-less probe lane, on the model the invoker names, else `router-env/my-referee-two`: `printf '%s\n' "$PROMPT" | $(python3 scripts/audit/audit.py pi-cmd runner --model router-env/my-referee-two)`. It reads the prompt on stdin, runs with no tools, and mutates nothing.
3. Behavior present: keep the rule. Behavior absent: propose removal. One run is weak evidence, so never edit or delete the rule yourself. No prompt can elicit it: keep the rule and say so.
4. Write per rule to `updates.md`: the rule, the prompt, what the output showed, keep or propose removal. Pass `--model <id>` to `track`; it writes `reviewed_for_model` on every row of the artifact.

## Gotchas

- **A moved path can look fine.** The commits-by-path query on a deleted path returns the commit that deleted it, so a moved `github-path` source prints `error: null`, `stale: true`. That is why step 4 runs the contents test before any adopt/adapt/ignore.
- **`kind: unversioned`** sources (a post, a talk) have no commit: `upstreams` prints `stale: false` without comparing. Read the source, then record `current` with no `--sha`.
- **The `kind: repo` row** (`skill` null) is the fork origin for the CI drift check. `track` cannot address it; never track it.
- **`status`** is the comparison state only. `adopt`, `adapt` and `ignore` live in `updates.md`, never in the registry.
