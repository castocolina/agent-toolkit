---
name: agentskills-research
description: Re-fetch the pinned Agent Skills docs and skills-ref validator into skill-judge's references, report which rules changed, and bump the rubric's rubric_version and spec_sha. Use when the maintainer of this repo asks to "refresh agent skills spec", "update skill-judge from agentskills.io", re-fetch the agentskills docs, check whether the Agent Skills specification or the skills-ref validator changed since the last pin, or sync skill-judge's rubric with upstream, even if they do not name fetch-spec.sh. Works only from a checkout of this repo. Not for writing, judging, or validating a skill.
---

# Agentskills Research

Run from this repo's root. It keeps `skills/skill-judge/references/agentskills/` (verbatim, CC-BY-4.0 copies of the Agent Skills docs and the `skills-ref` validator, pinned in `SOURCE.json`) and `skills/skill-judge/references/rubric.md` in step with github.com/agentskills/agentskills.

## Workflow

1. Run `bash skills/agentskills-research/scripts/fetch-spec.sh` with no options (`-h` lists them). It prints one JSON object; the branches use `changed`, `rubric_stale` and `sha` (the pin). `fetch-spec.sh -h` documents the other fields and the overrides. If it exits 1, go to Failures.
2. If `structure_changed` is true, or `rubric-check` reports a broken source anchor, follow **When upstream structure changes** before considering the unchanged early return. Otherwise, `changed` empty AND `rubric_stale` false means report "spec unchanged at <sha>" and stop. Do not edit the rubric.
3. Otherwise pick exactly one branch, first match wins. Docs and the validator both count: a validator-only change is a rule change.
   1. `skills/skill-judge/references/rubric.md` missing: restore it with `git checkout -- skills/skill-judge/references/rubric.md` and re-run from step 1; if git has no copy, stop and report.
   2. `rubric_stale` false (so `changed` is non-empty: references repaired to the pin the rubric already matches): no rule change. Report the repair, leave the rubric alone, and record the pending commit without performing it.
   3. `rubric_stale` true (whether or not `changed` is empty): diff from the commit that introduced the rubric's old `spec_sha`, never the working-tree diff alone, which misses rule changes from earlier pins.
      ```bash
      OLD_SHA=$(sed -n 's/^spec_sha:[[:space:]]*//p' skills/skill-judge/references/rubric.md)
      BASE=$(git log --format=%H -S"$OLD_SHA" -- skills/skill-judge/references/agentskills/SOURCE.json | tail -1)
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
   - Check every `source` anchor still matches a heading in the refreshed copies (`grep -n '^#' skills/skill-judge/references/agentskills/<file>.md`; slug = lowercase, spaces to hyphens, punctuation dropped). `rubric-check` verifies each anchor against its reference file.
6. Both branches that continue (reference repair and rule update) must run `python3 scripts/build_plugins.py` (skill-judge is mirrored into `dist/`), then `python3 scripts/audit/audit.py rubric-check` and require exit 0 before committing. Commit only after both checks succeed. The answer must end by running `python3 scripts/audit/audit.py rubric-check`: report its exit code. `rubric-check` verifies both the spec pin and source anchors.

## When upstream structure changes

Run this section when `fetch-spec.sh` reports `structure_changed: true` or `rubric-check` reports a broken source anchor. Update the fetcher's source map, fixture, and tests for added or removed pages; add or delete the matching reference copy; remap every affected rubric `source`; review criteria for rules added or removed with those pages; bump `rubric_version`; and keep the judge eval `files` lists aligned with cited sources. For a new page, use its pre-downloaded `--pages-dir` raw file (the repair job has no network), prepend the standard verbatim-copy header, and add its header-inclusive SHA-256 to `SOURCE.json`. Finish with `rubric-check` and `test-fetch-spec.sh` passing.

The pin `sha` is also what `uvx --from "git+https://github.com/agentskills/agentskills@<sha>#subdirectory=skills-ref" skills-ref validate <dir>` should use.

## Failures

- Fetcher exits 1: report its stderr and stop. References are rolled back only if the failure happened during publish; a later failure (e.g. "cannot build changed list") leaves the new references in place. Check stderr and `git status -- skills/skill-judge/references/agentskills` before assuming they are unchanged.
- stderr says recovery failed: restore from the backup directory it names (copy the files back over `skills/skill-judge/references/agentskills/`). Use `git checkout -- skills/skill-judge/references/agentskills` only after `git status` shows no local reference changes you want to keep and the user confirms; it discards them. Do not touch the rubric or run `build_plugins.py` until the references match `SOURCE.json`.
- `rubric-check` fails: fix the reason it prints (usually `spec_sha` != `SOURCE.json`) and re-run until it exits 0.
- `build_plugins.py` fails: report the error and stop before committing.

## Gotchas / NEVER

- The fetcher needs bash 4+.
- `git log -S"$OLD_SHA"` also matches the commit that later removed that sha from `SOURCE.json`: the OLDEST match (`tail -1`) is BASE. Taking the newest one diffs from the wrong baseline and misses rule changes.
- A repair-only run while upstream head has moved advances the pin (any `changed` file moves `sha` to `resolved`). `rubric_stale` then becomes true and the run goes down the BASE-diff path, not the repair path.
- References must match `SOURCE.json` before `build_plugins.py`; otherwise `dist/` mirrors unpinned or hand-edited docs.
- NEVER edit the copied references by hand: the next fetch silently reverts them and reports them in `changed`.
