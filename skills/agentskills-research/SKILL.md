---
name: agentskills-research
description: Refresh the specs that skill-judge scores against. Re-fetches the pinned Agent Skills docs and skills-ref validator from agentskills.io, and the Claude Code skills, sub-agents and plugins-reference pages from code.claude.com. Reports which rules changed and updates the judge rubric or the command/agent profiles to match. Use when the maintainer of this repo asks to "refresh agent skills spec", "update skill-judge from agentskills.io", "update the subagent spec the judge uses", "update the Claude Code docs we vendor", or whether upstream skill-format rules changed since the last pin, even without naming the fetch scripts. Works only from a checkout of this repo. Not for writing, judging, or validating a skill.
---

# Agentskills Research

Two sources, two fetchers; run each from this repo's root. A request that names only one source runs only its fetcher (the Agent Skills spec: `fetch-spec.sh` alone; the Claude Code pages: `fetch-claude-specs.sh` alone); with no source named, run both: finish each source's edits, run `build_plugins.py` and `rubric-check` once at the end, and make one commit; if one fetcher exits 1, still run the other and report both results.

## Source 1: Agent Skills (agentskills.io)

Run from this repo's root. It keeps `skills/skill-judge/references/agentskills/` (verbatim, CC-BY-4.0 copies of the Agent Skills docs and the `skills-ref` validator, pinned in `SOURCE.json`) and `skills/skill-judge/references/rubric.md` in step with github.com/agentskills/agentskills.

### Workflow

1. Run `bash skills/agentskills-research/scripts/fetch-spec.sh` with no options (`-h` lists them). It prints one JSON object; the branches use `changed`, `removed` (references pruned), `rubric_stale` and `sha` (the pin). `fetch-spec.sh -h` documents the other fields and the overrides. If it exits 1, go to Failures.
2. If `structure_changed` is true, or `rubric-check` reports a broken source anchor, read `references/structure-change.md` and follow it, then resume at step 3 with the latest fetcher JSON; never take the unchanged early return first. Otherwise, `changed` empty AND `removed` empty AND `rubric_stale` false means report "spec unchanged at <sha>" and stop. Do not edit the rubric.
3. Otherwise pick exactly one branch, first match wins. Docs and the validator both count: a validator-only change never takes the unchanged early return; changed validation behavior is a rule change, comment-only or format-only is editorial (update `spec_sha` only).
   1. `skills/skill-judge/references/rubric.md` missing: restore it with `git checkout -- skills/skill-judge/references/rubric.md` and re-run from step 1; if git has no copy, stop and report.
   2. `rubric_stale` false (so `changed` or `removed` is non-empty: references repaired or pruned to the pin the rubric already matches): no rule change. Report the repair, leave the rubric alone, and run step 6's checks and report the pending commit without committing.
   3. `rubric_stale` true (whether or not `changed` is empty): diff from the commit that introduced the rubric's old `spec_sha`, never the working-tree diff alone, which misses rule changes from earlier pins.
      ```bash
      OLD_SHA=$(sed -n 's/^spec_sha:[[:space:]]*//p' skills/skill-judge/references/rubric.md)
      BASE=$(git log --format=%H -S"$OLD_SHA" -- skills/skill-judge/references/rubric.md | tail -1)
      git diff "$BASE" -- skills/skill-judge/references/agentskills
      ```
      If `BASE` is empty (commit not found), compare every rubric `source` section against the current references and list the differences instead.
   State in the answer which diff the rule changes came from and its `BASE` commit (or that the `source` sections were compared).
4. List the rule changes for the user. A rule change is a new, removed or changed MUST/SHOULD/NEVER statement, a numeric limit, a frontmatter field or constraint, or a validator check. Editorial is rewording, typos or example-only edits. When unsure, treat it as a rule change. Example: "description max 1024 -> 512 chars" is a rule change; "Keep SKILL.md short" reworded to "Keep SKILL.md concise" is editorial.
5. Update `skills/skill-judge/references/rubric.md`:
   - For each rule in step 4, find the dimension whose `source` column cites the changed section (`grep -n '<file>.md#' skills/skill-judge/references/rubric.md`). Edit that dimension's criteria and bands, and its `source` anchor if a heading moved or was renamed.
   - A validator check has no `source` anchor, so the grep finds nothing. Map it to D4 if it checks frontmatter, `name` or `description`, else to D5 (body, file layout). If no existing criterion fits, add one to that dimension's criteria paragraph and bottom band, citing `references/agentskills/skills-ref-validator.py.txt`.
   - Turning a rule into rubric text: a new hard limit goes in the dimension's criteria paragraph and caps its bottom band; a new SHOULD goes in the middle-band criteria; a removed rule means deleting its criterion.
   - THEN, if any rule changed (also when `changed` is empty): `rubric_version` +1, and the `# Skill Judge Rubric vN` title to match.
   - `spec_sha` = the `sha` in the fetcher output (equal to `SOURCE.json`). No rule changed: update `spec_sha` only.
   - Check every `source` anchor still matches a heading in the refreshed copies (`grep -n '^#' skills/skill-judge/references/agentskills/<file>.md`). rubric-check verifies each anchor against its reference file.
6. Both branches that continue (reference repair and rule update) must run `python3 scripts/build_plugins.py` (skill-judge is mirrored into `dist/`), then `python3 scripts/audit/audit.py rubric-check` and require exit 0. Only the rule-update branch then commits; the repair branch reports the pending commit instead. The answer must end by running `python3 scripts/audit/audit.py rubric-check`: report its exit code. `rubric-check` verifies both the spec pin and source anchors.

## Source 2: Claude Code command and agent pages

Pins `skills`, `sub-agents` and `plugins-reference` from code.claude.com in `skills/skill-judge/references/claude-code/SOURCE.json`. The raw pages carry no license grant and are never committed: the fetcher keeps them only in a temp directory outside every checkout, and `docs/audit/artifact-specs.md` holds our own field tables. Run `bash skills/agentskills-research/scripts/fetch-claude-specs.sh --keep` (`-h` lists options). Output fields: `changed` and `unchanged` (page names), `digests` (`command`, `agent`), `profiles_stale` (kinds whose profile `source_digest` differs from `digests`), `kept` (the temp directory). Exit 1: report stderr and stop; the old `SOURCE.json` survives.

1. `changed` empty AND `profiles_stale` empty: delete the `kept` directory, report "Claude Code specs unchanged", edit nothing, stop.
2. `changed` empty, `profiles_stale` non-empty: an interrupted earlier refresh may have skipped the rule review, so do not just copy digests. Go to step 3. If the comparison finds no rule change, only set `source_digest` and the `command_digest` / `agent_digest` line to `digests[kind]`; otherwise apply step 4. `source_digest` must stay on line 2 of the profile (`source_digest: <digest>`, right after `profile_version`) or `profiles_stale` never clears.
3. In `kept`, read to its end the union of the `changed` pages and the pages of every `profiles_stale` kind (command = `skills` + `plugins-reference`; agent = `sub-agents` + `plugins-reference`), deduplicated, and compare it with the field tables and rules in `docs/audit/artifact-specs.md`. That file is the only record: no old page is kept.
4. Judge each change as in Source 1 step 4.
   - Rule change (a new, removed or changed field, allowed value, limit, validation rule or plugin restriction): rewrite the affected rows and sections of `artifact-specs.md` in our own words (quotes at most 25 words, with the URL); update D4, D5 and D7 of the affected profile(s) (`command.md`, `agent.md`) to match; bump `profile_version` by 1; set `source_digest`; update the provenance header (digest lines and the `<page>: <bytes> bytes, sha256 <hash>` lines).
   - Editorial (rewording, same fields and values): update only `source_digest` and the provenance header. No rule row edit, no `profile_version` bump. When unsure, treat as a rule change.
5. Delete the `kept` directory. Run `python3 scripts/build_plugins.py`, then `python3 scripts/audit/audit.py rubric-check` and require exit 0 before committing; the answer ends with that exit code (expect 0; if you cannot run it, say so and name the command).

Other hosts (opencode, Codex, Cursor) are not pinned.

## Attribution survives every refresh

Never remove or shorten a credit, upstream link or license line. The agentskills docs are CC-BY-4.0: keep their attribution headers and the `license` in `references/agentskills/SOURCE.json`. Keep rule 5 of `skills/skill-judge/references/judge-prompt.md`, which forbids findings that remove attribution. A refresh that drops either is wrong; restore it before committing.

The pin `sha` is also what `uvx --from "git+https://github.com/agentskills/agentskills@<sha>#subdirectory=skills-ref" skills-ref validate <dir>` should use.

## Failures

- Fetcher exits 1: report its stderr and stop. References are rolled back only if the failure happened during publish; a later failure (e.g. "cannot build changed list") leaves the new references in place. Check stderr and `git status -- skills/skill-judge/references/agentskills` before assuming they are unchanged.
- stderr says recovery failed: restore from the backup directory it names (copy the files back over `skills/skill-judge/references/agentskills/`). Use `git checkout -- skills/skill-judge/references/agentskills` only after `git status` shows no local reference changes you want to keep and the user confirms; it discards them. Do not touch the rubric or run `build_plugins.py` until the references match `SOURCE.json`.
- `rubric-check` fails: fix the reason it prints (usually `spec_sha` != `SOURCE.json`) and re-run until it exits 0.
- `build_plugins.py` fails: report the error and stop before committing.

## Gotchas / NEVER

- The fetcher needs bash 4+ (`declare -A`). macOS `/bin/bash` 3.2 fails with `declare: -A: invalid option`; run it with a Homebrew bash.
- `git log -S"$OLD_SHA"` also matches any later commit that removed that sha from `rubric.md`: the OLDEST match (`tail -1`) is BASE. Taking the newest one diffs from the wrong baseline and misses rule changes.
- A repair-only run while upstream head has moved advances the pin (any `changed` file moves `sha` to `resolved`). `rubric_stale` then becomes true and the run goes down the BASE-diff path, not the repair path.
- References must match `SOURCE.json` before `build_plugins.py`; otherwise `dist/` mirrors unpinned or hand-edited docs.
- NEVER edit the copied references by hand: the next fetch silently reverts them and reports them in `changed`.
