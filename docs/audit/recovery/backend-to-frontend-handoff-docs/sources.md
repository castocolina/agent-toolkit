# Sources: backend-to-frontend-handoff-docs (skill)

Checked 2026-11-15. Review only: no `track` call, no registry edit, no artifact edit.

## Origins found

1. **softaworks/agent-toolkit, `skills/backend-to-frontend-handoff-docs`** (author of the repository: Leonardo Flores, @leonardocouy).
   - Our `dbff837f` SKILL.md is byte-identical in its first commit to the fork point `3027f20f` (`git show 3027f20f:skills/backend-to-frontend-handoff-docs/SKILL.md`), so the skill is a fork copy that was rewritten after the baseline (de35b734, 2026-10-29).
   - Upstream `main` holds the same two files (README.md, SKILL.md); its only commit for the path is `06825f04` (2026-01-18, "feat: add 23 curated skills with comprehensive documentation"). The upstream SKILL.md is byte-identical to the fork-point copy (`cmp`, checked with `gh api`). No upstream change since the fork point.
   - No registry row exists for the skill and README.md carries no credit line (the file has no "Credits" section), so `audit.py check --strict` cannot test a credit and `upstreams` never reviews the source.
2. **No other origin found.** The wire-contract tracing procedure and "Contract decisions that are easy to miss" are our own rewrite (not in the fork copy); they rest on HTTP semantics (RFC 9110, RFC 9111, RFC 6585, RFC 3339), listed below as `unversioned` rows because Step 5 verified the status codes, idempotency and caching statements against them. The distinctive upstream phrases ("copy-paste-ready", "No Chat Output", "Simple API shortcut") appear only in the softaworks files and in forks of them, so a web search adds no other origin.

## Proposed registry rows (verbatim JSON, `docs/audit/upstream-sources.json`)

```json
{
  "skill": "backend-to-frontend-handoff-docs",
  "kind": "github-path",
  "source": "softaworks/agent-toolkit:skills/backend-to-frontend-handoff-docs",
  "ref": "main",
  "credit": "softaworks/agent-toolkit"
},
{
  "skill": "backend-to-frontend-handoff-docs",
  "kind": "unversioned",
  "source": "RFC 9110, HTTP Semantics: https://www.rfc-editor.org/rfc/rfc9110",
  "ref": null,
  "credit": "IETF"
},
{
  "skill": "backend-to-frontend-handoff-docs",
  "kind": "unversioned",
  "source": "RFC 9111, HTTP Caching: https://www.rfc-editor.org/rfc/rfc9111",
  "ref": null,
  "credit": "IETF"
},
{
  "skill": "backend-to-frontend-handoff-docs",
  "kind": "unversioned",
  "source": "RFC 6585, Additional HTTP Status Codes: https://www.rfc-editor.org/rfc/rfc6585",
  "ref": null,
  "credit": "IETF"
},
{
  "skill": "backend-to-frontend-handoff-docs",
  "kind": "unversioned",
  "source": "RFC 3339, Date and Time on the Internet: Timestamps: https://www.rfc-editor.org/rfc/rfc3339",
  "ref": null,
  "credit": "IETF"
}
```

Checks against `validate_entry`: `skill` is kebab-case and the directory exists; `github-path` source is `owner/repo:path` with a non-empty `ref`; `unversioned` rows have a non-empty source and `ref: null`; every row has a non-empty `credit`. The existing registry uses the same row shape for qa-test-planner (`credit: softaworks/agent-toolkit`) and for `IETF` (RFC 6901 row). The `credit` text must appear verbatim in SKILL.md, README.md or `references/*.md` (`missing_credit` check), which the credit line below satisfies for `softaworks/agent-toolkit` and `IETF`.

## Missing credit line

README.md has none. Add this section at the end of `skills/backend-to-frontend-handoff-docs/README.md`, in the style of qa-test-planner and naming-analyzer:

```text
## Credits

Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy.

Documentation owners credited (official pages listed in `docs/audit/upstream-sources.json`, checked 2026-11-15): IETF (RFC 9110, RFC 9111, RFC 6585, RFC 3339).
```

The root README.md needs nothing for a skill (its table row already links the skill README).

## skill-updater style review (REVIEW ONLY)

Procedure followed from `skills/skill-updater/SKILL.md`:

- Step 1: scope `skills/backend-to-frontend-handoff-docs/` exists; not a synced skill.
- Step 2: no row for this artifact and no credit line naming an upstream. Outcome: propose the rows above; give no `track` call (a `track` call cannot create a source row). Upstream comparison done by hand with `gh api` instead of `upstreams` (which would not list this artifact).
- Steps 3-4: path resolves (contents test OK); upstream unchanged since the fork point, nothing to classify. adopt: none. adapt: none. ignore: none (no upstream change exists).
- Step 6, model-validity pass: not run. It needs a model probe lane, and the analyst rails forbid running an LLM lane here; the rules that counter a model habit ("NEVER infer retry safety for mutations", "NEVER equate omitted and null", "Never infer authentication requirements ... from endpoint names") should be probed by the controller when the registry rows are tracked.

Adopt/adapt/ignore items for the restore brief (from this artifact's own gaps, not from upstream):

- adapt (README): replace the stale no-chat statement (README "How It Works" last paragraph) with SKILL.md's "brief path confirmation, answer questions normally"; align Version Management / Output Location / Example 3 with the SKILL.md rule (record row s026); remove or reword Tips 5 ("generate handoff BEFORE implementation"), which contradicts "Not for designing unimplemented APIs"; fix Related Skills (`code-reviewer` and `dev-spec` do not exist anywhere in this repo or in upstream).
- adopt (references/api-handoff-template.md, record rows s028 and s029): the restore items listed in the report: example payload slot, validation rules to mirror, call order, rate limits, display labels only when the backend defines them, assumptions and trade-offs.
- ignore: the baseline TypeScript sample interface as a fixed format (the description covers web or mobile clients; a language-neutral typed model sketch is enough), "Keep it scannable" and the persona line (generic model knowledge).
