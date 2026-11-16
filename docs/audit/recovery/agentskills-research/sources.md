# agentskills-research sources (plan 14, batch 19, mode facts-only, checked 2026-11-15)

## Origins found

1. **Original to this repository.** `skills/agentskills-research` is not in softaworks/agent-toolkit at `3027f20f` (`git show 3027f20f --stat -- skills/agentskills-research` lists nothing). `git log` shows only local commits: `ba55859f` (2026-10-25, "ingest and track the Agent Skills spec"), `de35b734`, `18418b1d`, `c413da46` (2026-11-02, Claude Code pins). A code search for its distinctive phrases found no other source. No row of kind `github` or `github-path` for a fork origin is needed.
2. **Agent Skills specification and `skills-ref` validator** (github.com/agentskills/agentskills; docs CC-BY-4.0, code Apache-2.0). The fetcher mirrors 8 files into `skills/skill-judge/references/agentskills/`; its own `SOURCE.json` pins the commit (`69ef37e9...`). Credit already in `README.md` line 5: `[agentskills/agentskills](https://github.com/agentskills/agentskills) (CC-BY-4.0)`.
3. **Claude Code documentation** (Anthropic): `skills`, `sub-agents`, `plugins-reference` pages, hashed only. No credit naming Anthropic exists in this skill's files.
4. The registry (`docs/audit/upstream-sources.json`) has NO row with `skill: agentskills-research`.

## Proposed registry rows (the controller adds them by hand; this analyst touched no registry file)

Why four `github-path` rows instead of one on `docs`: a `docs` row went `stale: true` today from `docs/style.css` and `docs/footer.js` alone (2026-11-04, not mirrored); per-file rows follow only mirrored content. All four were run through `audit.py upstreams` from a scratch registry: `error: null`, `stale: false`, and each path passes the skill-updater contents test (`gh api` contents resolves). The credit strings were checked against the current files: `agentskills/agentskills` and `Agent Skills` appear verbatim in `README.md`; `Anthropic` does NOT (see the missing credit line below), so the three Anthropic rows trip `missing_credit` until it is added.

```json
{
  "skill": "agentskills-research",
  "kind": "github-path",
  "source": "agentskills/agentskills:docs/specification.mdx",
  "ref": "main",
  "credit": "agentskills/agentskills"
}
```

```json
{
  "skill": "agentskills-research",
  "kind": "github-path",
  "source": "agentskills/agentskills:docs/skill-creation",
  "ref": "main",
  "credit": "agentskills/agentskills"
}
```

```json
{
  "skill": "agentskills-research",
  "kind": "github-path",
  "source": "agentskills/agentskills:docs/docs.json",
  "ref": "main",
  "credit": "agentskills/agentskills"
}
```

```json
{
  "skill": "agentskills-research",
  "kind": "github-path",
  "source": "agentskills/agentskills:skills-ref/src/skills_ref/validator.py",
  "ref": "main",
  "credit": "agentskills/agentskills"
}
```

```json
{
  "skill": "agentskills-research",
  "kind": "unversioned",
  "source": "Agent Skills specification (https://agentskills.io/specification)",
  "ref": null,
  "credit": "Agent Skills"
}
```

```json
{
  "skill": "agentskills-research",
  "kind": "unversioned",
  "source": "Claude Code docs, Extend Claude with skills (https://code.claude.com/docs/en/skills)",
  "ref": null,
  "credit": "Anthropic"
}
```

```json
{
  "skill": "agentskills-research",
  "kind": "unversioned",
  "source": "Claude Code docs, Create custom subagents (https://code.claude.com/docs/en/sub-agents)",
  "ref": null,
  "credit": "Anthropic"
}
```

```json
{
  "skill": "agentskills-research",
  "kind": "unversioned",
  "source": "Claude Code docs, Plugins reference (https://code.claude.com/docs/en/plugins-reference)",
  "ref": null,
  "credit": "Anthropic"
}
```

The source strings of the Claude Code and Agent Skills rows match the wording of the existing `skill-judge` rows. `ours_updated` for this artifact reads `git log` on `skills/agentskills-research/SKILL.md` and `references/` (commits exist, 2026-11-02), so no `no local commit` error. `upstreams` never marks an `unversioned` row stale: the dated facts table and the fetchers' own hash pins are the age signal.

## Credits: README against the registry rows

- Present: `agentskills/agentskills` (README line 5), `Agent Skills` (README line 5, SKILL.md).
- Missing: `Anthropic`. Exact line to add to `skills/agentskills-research/README.md`, right after the paragraph that describes `fetch-claude-specs.sh`:

```text
The Claude Code pages (skills, sub-agents, plugins-reference) are documentation by Anthropic at code.claude.com; this repo stores only their URLs and SHA-256 hashes, never copies.
```

- No credit line is removed or shortened by any proposal here. The wording fix for the license claim (below) keeps `(CC-BY-4.0)` for the docs and adds the validator's own license.

## License wording fix (fact `corrected`, see facts.md)

Current README line 5 and SKILL.md Source 1 intro attribute both the docs and the validator to CC-BY-4.0. Upstream: docs CC-BY-4.0, `skills-ref` code Apache-2.0. Proposed replacement phrase for both files: "verbatim copies of the Agent Skills docs (CC-BY-4.0) and of the `skills-ref` validator (Apache-2.0)". The `TXT_HEADER` in `scripts/fetch-spec.sh`, the header of the mirrored `skills-ref-validator.py.txt`, and the single `license` field in `references/agentskills/SOURCE.json` carry the same imprecision; those are the vendored mirror: never hand-edit. Changing `TXT_HEADER` changes the validator copy's hash, so the next fetcher run lists it in `changed`, moves the pin to the head sha and sets `rubric_stale: true` (no rule change: `spec_sha` update only, per SKILL.md step 3.3 and step 5). That consequence needs the owner's decision.

## Skill-updater style review (review only; no `track` call)

Procedure followed: step 1 (path exists; not a synced skill), step 2 (no row, so rows proposed above; no `track` call because `track` cannot create a source row), steps 3-4 on the scratch registry, step 6 (model probe).

| upstream change (69ef37e..83021e2, `gh api compare`) | decision | reason |
| --- | --- | --- |
| `GOVERNANCE.md`, `MAINTAINERS.md` added (AAIF donation, #648) | ignore | governance files; no spec content, not mirrored |
| `docs/footer.js` added, `docs/style.css` modified | ignore | site presentation; not in the 8 mirrored paths (all 8 hashes equal at the head) |
| `docs/specification.mdx`, `docs/skill-creation/*`, `docs/docs.json`, `validator.py` | no change | newest upstream commits 2026-08-04 / 2026-04-19 / 2026-04-19 / 2025-12-18, all before the 2026-10-29 pin |

Claude Code pages (`unversioned`, read against the pin): all three hashes differ from the 2026-11-02 pin. First-pass reading against `docs/audit/artifact-specs.md` found no contradicted field row, only additions (see the rule-review hint row in facts.md). Decision: adopt (run the SKILL.md Source 2 refresh: `fetch-claude-specs.sh --keep`, read the three pages to their end, rewrite the affected rows of `artifact-specs.md`, bump `profile_version` if a rule changed, build, `rubric-check`). This is a run of the skill itself, not part of this recovery.

Model-validity pass: not applicable. The skill has no rule that exists to counter a model habit (no substitution to undo, no habit to suppress); it is a procedure over fetcher JSON. No probe run.

Stale pins, summary:

- Agent Skills mirror: pin `69ef37e` is 2 commits behind `main` (`83021e2`) but every mirrored file is byte-identical to the head; content current, nothing to refresh.
- Claude Code pins (`claude-code/SOURCE.json`, fetched 2026-11-02): skills, sub-agents and plugins-reference ALL STALE; both profiles (`command`, `agent`) report `profiles_stale`. Live hashes in facts.md.

## Adopt / adapt / ignore items for the update brief

- **adopt**: add the 8 proposed registry rows; add the Anthropic credit line to README.
- **adopt**: document the real prerequisites of `fetch-claude-specs.sh` (bash 4.4+, git 2.36+, GNU `realpath`) in README and its `-h` text.
- **adopt**: run the Source 2 refresh for the three stale Claude Code pins (separate task, with its own commit).
- **adapt**: license wording (docs CC-BY-4.0, validator Apache-2.0) in README and SKILL.md now; the fetcher header, mirror header and `SOURCE.json` license field only through a fetcher change plus fetch run, with the pin-advance consequence above and test fixtures (`tests/skills/agentskills-research`) updated together.
- **adapt**: eval fixture `evals/files/validator.diff` (invent a validator change that the pinned validator does not already contain; the constant is `MAX_SKILL_NAME_LENGTH`). Evals may be edited openly.
- **ignore**: upstream governance and site-asset changes; "hosts not pinned" scope sentence; the skill-judge README's own credit paragraph (other artifact).
