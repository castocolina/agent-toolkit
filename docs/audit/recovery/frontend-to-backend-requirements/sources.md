# Sources: frontend-to-backend-requirements

## Origin found

- The skill is a fork of softaworks/agent-toolkit by Leonardo Flores (@leonardocouy), `skills/frontend-to-backend-requirements`. Evidence: the file exists at the fork base `3027f20f` (which is also upstream `main` today, sha `3027f20f3181758385a1bb8c022d4041dfb4de84`), and `git diff 3027f20f dbff837f` shows no change to its SKILL.md or README.md, so the baseline text is the upstream text. The upstream path holds only README.md and SKILL.md, and its one commit (06825f04, 2026-01-18, "feat: add 23 curated skills") is the fork base: upstream has not changed since.
- Upstream license: MIT (GitHub license API, `softaworks/agent-toolkit`).
- No other origin found for the distinctive text (the "Describe, don't prescribe" rules, the Frontend Owns / Backend Owns table, the contracts and provider examples). The current rewrite (de35b734) adds uncertainty classification, freshness and authorization rules and the template; no source is credited for them and none was found in a search of the repo.
- Registry status today: no row in `docs/audit/upstream-sources.json` for `frontend-to-backend-requirements` (grep finds none). The README.md of the skill has no credit line, so `audit.py check --strict` would report `missing_credit` the moment the row below is added unless the line is added first.

## Proposed registry rows (docs/audit/upstream-sources.json)

Origin row (credit text `softaworks/agent-toolkit` must appear verbatim in the skill's README.md, SKILL.md or references/; the credit line below carries it):

```json
{
  "skill": "frontend-to-backend-requirements",
  "kind": "github-path",
  "source": "softaworks/agent-toolkit:skills/frontend-to-backend-requirements",
  "ref": "main",
  "credit": "softaworks/agent-toolkit"
}
```

Official documentation row (the Agent Skills specification, used for the frontmatter rows in facts.md):

```json
{
  "skill": "frontend-to-backend-requirements",
  "kind": "unversioned",
  "source": "Agent Skills specification (https://agentskills.io/specification)",
  "ref": null,
  "credit": "Agent Skills"
}
```

Check before adding the second row: other skills may already carry an identical Agent Skills row; copy the exact `source` and `credit` strings used there so the registry stays uniform (the strings above follow the pattern in the README credits "Agent Skills specification (Agent Skills)").

## Missing credit line

Add to `skills/frontend-to-backend-requirements/README.md` (end of file), the same wording as the sibling forks (naming-analyzer, mui, commit-work, qa-test-planner):

```markdown
Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy.
```

The root README.md already says "Fork of softaworks/agent-toolkit by @leonardocouy"; no root change is needed for a skill.

Because `credit_issues` in `scripts/audit/audit.py` requires every row's `credit` text (including `unversioned` rows) to appear verbatim in SKILL.md, README.md or references/*.md, the Agent Skills row also needs its credit text in the README. Add a second line there (the registry row's `credit` is `Agent Skills`):

```markdown
Frontmatter limits (name, description) follow the [Agent Skills specification](https://agentskills.io/specification) (Agent Skills).
```

## skill-updater style review (review only; no `track` call, no registry write)

Rows: none exist yet, so step 2 of skill-updater applies: a credit-less upstream with no row gets a proposed row (above), no `track` call. Read-only checks done:

- `gh api repos/softaworks/agent-toolkit/contents/skills/frontend-to-backend-requirements` lists README.md and SKILL.md (path exists, no move). Upstream SKILL.md blob sha `09352d3b900ef551bce8c4a5df80eb9b386091c6`; the path has one commit, the fork base. Suggested `--sha` for the later `track` call (the controller decides): `3027f20f3181758385a1bb8c022d4041dfb4de84` (newest upstream commit read).
- Upstream change since fork: none. Adopt: none. Adapt: none. Ignore: none (nothing to classify).
- Model-validity pass NOT run: it needs the tool-less pi probe lane, and the rails forbid an LLM lane for analysts. Candidate rules and prompts for the controller: the only rule that counters a model habit is "NEVER name endpoint paths or field names" (models prescribe `GET /api/...` and JSON shapes by habit). Prompt: "I am building a contracts list screen in React with status filtering. Write what I should send to the backend team." Behavior present if the output names a route, HTTP method or field name even once; keep the rule then.

## Items for the restore brief (from this analysis)

Restore (rows s029 and s030 of record.md), one change into `templates/backend-requirements.md` (loaded at the write step) or a short block in SKILL.md; rewrite, do not paste:
1. A closing "Collaboration" instruction: write the document as a request, not a demand; say why each need exists (context); and include one or two pushback invitations such as "Let me know if this doesn't make sense for how the data is structured", "Open to suggestions on a better approach", "Push back if this complicates things unnecessarily"; end with open questions in the Questions for backend section. The frontend describes the problem, the backend proposes the solution.
2. The NEVER rule in SKILL.md should say "endpoint paths, HTTP methods or field names" (the evals' assertions already name HTTP methods).
3. Eval: the three existing evals assert no endpoint, HTTP method or field names and include backend questions; add an assertion to one eval (for example `precise-inbox`) that the document invites backend pushback or alternatives. Do not add other evals.

Other observations (not row-backed, not for edit by this analysis):
- README.md contradicts SKILL.md: it says "All output goes to `.claude/docs/ai/<feature-name>/backend-requirements.md` - no chat output", while SKILL.md now honors an inline preview and allows brief chat confirmations (record row s017). The fixer should align that README line (a wording change only; keep the credit and every other line).
- s025 to s027 (the Bad (Dictating Implementation) / Good (Describing Needs) / Good (Describing Relationship) pairs) exist only in the README now; the presence tooling counts them present because README.md is part of the artifact. They are model-known contrasts and no row was needed, but a coordinator who wants the contrasts visible to the model can fold one short pair into the template.
