# excalidraw: sources

Checked 2026-11-13. Nothing under skills/ was edited and no `track` call was made.

## Origins found

1. **softaworks/agent-toolkit, `skills/excalidraw`** (MIT, per the repository's license metadata). The baseline `dbff837f` copy of SKILL.md and README.md is byte-identical to the upstream copy at `3027f20f` (`git diff dbff837f 3027f20f -- skills/excalidraw` is empty), so the whole baseline text is upstream's. Upstream's `skills/excalidraw` still has the single commit `06825f04` (2026-01-18, "feat: add 23 curated skills with comprehensive documentation"), and its current SKILL.md and README.md equal the `3027f20f` files, so there is no upstream change to adopt. The softaworks text itself carries one author trace: the BAD/GOOD example names a private path `.ryanquinn3/ticketing/detailed-architecture.excalidraw.json`, which suggests the pattern came from a repository of Ryan Quinn. No credit or license line in the upstream files names him, and a web search for the distinctive phrase ("Main agents NEVER read Excalidraw files") returned only softaworks and forks of it (tessl, skills.cat, playbooks, davila7/claude-code-templates, cachemoney/agent-toolkit), none with an earlier origin. So no registry row or credit line is proposed for him.
2. **The current design is original to this repository**: `scripts/scene.py`, its tests, the worker contract, the route table and the gotchas have no upstream.
3. **Official Excalidraw documentation and source** used to verify the facts in `facts.md`, and the Obsidian plugin source and Anthropic's models overview.

## Credit line

Present: `skills/excalidraw/README.md` ends with "Part of the Softaworks Agent Skills collection." (a line kept from the baseline). No credit line is missing, and nothing is added or reworded. The registry has no excalidraw row today (only the repo-level `softaworks/agent-toolkit` row), so the origin is not tracked.

## Proposed registry rows (for docs/audit/upstream-sources.json, added by the controller)

Rows 1-5 are needed (the origin and every documentation page used). Rows 6-7 are optional `github-path` rows that make `upstreams` notice a change in the two source files the facts rest on; the controller may skip them.

```json
{
  "skill": "excalidraw",
  "kind": "github-path",
  "source": "softaworks/agent-toolkit:skills/excalidraw",
  "ref": "main",
  "credit": "softaworks/agent-toolkit"
}
```

```json
{
  "skill": "excalidraw",
  "kind": "unversioned",
  "source": "Excalidraw JSON Schema: https://plus.excalidraw.com/docs/sdk/codebase/json-schema",
  "ref": null,
  "credit": "Excalidraw"
}
```

```json
{
  "skill": "excalidraw",
  "kind": "unversioned",
  "source": "Excalidraw utils API, export (exportEmbedScene): https://plus.excalidraw.com/docs/sdk/excalidraw/api/utils/export",
  "ref": null,
  "credit": "Excalidraw"
}
```

```json
{
  "skill": "excalidraw",
  "kind": "unversioned",
  "source": "Obsidian Excalidraw plugin default settings (compress, useExcalidrawExtension): https://github.com/zsviczian/obsidian-excalidraw-plugin/blob/master/src/core/settingsDefaults.ts",
  "ref": null,
  "credit": "Zsolt Viczian"
}
```

```json
{
  "skill": "excalidraw",
  "kind": "unversioned",
  "source": "Claude models overview (context window): https://platform.claude.com/docs/en/about-claude/models/overview",
  "ref": null,
  "credit": "Anthropic"
}
```

```json
{
  "skill": "excalidraw",
  "kind": "github-path",
  "source": "excalidraw/excalidraw:packages/common/src/constants.ts",
  "ref": "master",
  "credit": "Excalidraw"
}
```

```json
{
  "skill": "excalidraw",
  "kind": "github-path",
  "source": "excalidraw/excalidraw:packages/excalidraw/scene/export.ts",
  "ref": "master",
  "credit": "Excalidraw"
}
```

Notes: `validate_entry` accepts these shapes (kebab-case skill that exists, `ref` non-empty for `github-path`, `null` for `unversioned`, non-empty credit). The softaworks row copies the credit format of the other softaworks `github-path` rows. Excalidraw's default branch is `master`, not `main`. The upstream `docs.excalidraw.com` URLs answer 308 to `plus.excalidraw.com/docs/sdk/...`, so the rows use the redirect targets.

## skill-updater style review (review only)

- Rows: none for `excalidraw` today, so the procedure's step 2 case "no row": record would be a source-less call, but the origin above is a real upstream, so the controller adds row 1 first and then runs `track` on it later (not done here).
- Upstream change (step 4): none. The upstream path exists on `main`, its history is the one commit `06825f04` of 2026-01-18, and the files equal the baseline. Decision: nothing to adopt, adapt or ignore. Status for `track` when the row exists: `current`.
- Model-validity pass (step 6): the only rule that counters a model habit is the NEVER-read rule ("whatever the size", the tiny-file clause). It is already exercised by eval `small-file-exception`. The probe lane was not run here (implementers do not run LLM lanes); keep the rule.
- Adopt, adapt and ignore items for the restore brief (all from this review, none from upstream):
  - adapt: README Why sentence "a third of a 200k context" to state that the window size varies by model; replace the token figures for the two example diagrams by line and byte counts, per `facts.md`.
  - adapt (optional): scene.py `new_id` must never return an id starting with `-` (see the defect note in `facts.md`); this is a code change outside the record, for the fixer to take or leave.
  - adapt (optional, small): `new` writes `fontFamily: 1` (Virgil); the editor default is Excalifont (5). Valid as is; change only if a consistent look with newly drawn editor text matters.
  - ignore: restoring any removed section. The Step 3 verdicts in the report show every pending row is DROP.
  - gap noted, not a restore item: Obsidian drawings saved with the plugin's `.md` extension option (frontmatter `excalidraw-plugin: parsed`) are not matched by the `.excalidraw.md` rule; the fixer may add the frontmatter as a second signal in the route table row.
