# skill-updater: sources (batch 19, BASE d7a61091, checked 2026-11-15)

## Origin

- skill-updater is original to this repository. It was added by commit 9a4ba26c ("feat(skills): add ui-ux-principles and skill-updater"), and `git -C WT ls-tree -r 3027f20f skills/skill-updater` is empty, so it is not in the softaworks original.
- Neither SKILL.md nor README.md carries a credit line; the registry has exactly one row for it, `kind: local`, which takes no `credit`. No credit is missing and no web search for distinctive phrases was needed (the text is procedural and specific to this repo's `audit.py`).
- Its upstream review (skill-updater run on itself, REVIEW ONLY, no `track` call, no `upstreams` run needed because the only row is `local` and `upstreams` skips `local` rows): no source row, so step 6 (model probe) applies and nothing else. No adopt/adapt/ignore items exist for a restore brief.
- Model probe (step 6) was not run: the rules in SKILL.md are procedural, none exists to counter a model habit (no banned-word or substitution rule), so per the skill's own text "No prompt can elicit it: keep the rule". `reviewed_for_model` stays `null`. Recording is the coordinator's call.

## Facts the skill depends on that have a vendor page

The skill's `gh api` calls rely on four documented endpoints and one CLI command. No row covers them today. Proposed `unversioned` rows (these are reference pages with no commit to track; `credit` must appear verbatim in SKILL.md, README.md or `references/*.md`, so the credit line below must be added together with the rows):

```json
{
  "skill": "skill-updater",
  "kind": "unversioned",
  "source": "GitHub REST API, Commits (list commits, compare two commits, get a commit): https://docs.github.com/en/rest/commits/commits",
  "ref": null,
  "credit": "GitHub"
},
{
  "skill": "skill-updater",
  "kind": "unversioned",
  "source": "GitHub REST API, Git trees (get a tree, recursive limit and truncated flag): https://docs.github.com/en/rest/git/trees",
  "ref": null,
  "credit": "GitHub"
},
{
  "skill": "skill-updater",
  "kind": "unversioned",
  "source": "GitHub REST API, Repository contents (get repository content, ref parameter): https://docs.github.com/en/rest/repos/contents",
  "ref": null,
  "credit": "GitHub"
},
{
  "skill": "skill-updater",
  "kind": "unversioned",
  "source": "GitHub CLI manual, gh api (--silent, --jq, --paginate, --slurp): https://cli.github.com/manual/gh_api",
  "ref": null,
  "credit": "GitHub"
}
```

Validity check against `validate_entry`: all four have a kebab-case existing skill, `kind` unversioned, non-empty `source`, `ref` null, a non-empty `credit`, and no `artifact_kind` (skill is the default). The existing `local` row stays; `track` addresses a `local` row with a source-less call and `--source` with an exact source string for the rows above. Adding them changes nothing in `upstreams` (unversioned rows are never compared) but a later `track` call stamps their `last_reviewed`, which is intended.

Tools with no vendor URL (own `--help` is the source, pointer only, no row): `audit.py` (repo script), `pi` (`pi --help`, `pi --list-models`), `gh auth status`.

## Missing credit line

None is required today (no upstream). If the four rows above are added, `check --strict` will report `missing_credit` for "GitHub" until a line containing that exact text is added to README.md or SKILL.md (a `references/` file also counts). Suggested line for the README (do not shorten or reword once added):

```
## Sources

Endpoint behavior (commits, compare, git trees, repository contents) and `gh api` flags are read from the GitHub REST API documentation and the GitHub CLI manual (GitHub): https://docs.github.com/en/rest and https://cli.github.com/manual/gh_api.
```

## Proposed corrections for the restore brief (not applied: the artifact is not edited in this mode)

1. SKILL.md line 10: say `track` writes under `--root` when given, else under the checkout that holds `audit.py`. Source: `audit.py` `default_root()` and the `--root` option.
2. README.md line 24: replace "(every command and agent)" with nothing, or "(a command or agent with no upstream)"; many commands and agents have source rows.
3. SKILL.md step 4: after "Page or patch retrieval that fails or is cut short", add that the compare response lists at most 300 files for the whole comparison, caps at 250 commits without `page`/`per_page`, and has no `patch` for binary files, so a `null` patch or a 300-file list counts as cut short. Source: GitHub REST Commits docs.
4. SKILL.md step 5: add that when the tree response has `truncated: true` (cap 100,000 entries or 7 MB with `recursive`), "zero candidates" is not proof of a missing path; mark the review unresolved. Source: GitHub REST Git trees docs.
