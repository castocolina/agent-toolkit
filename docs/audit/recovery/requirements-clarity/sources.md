# requirements-clarity: sources (batch 7, checked 2026-11-07)

## Origins found

1. softaworks/agent-toolkit, `skills/requirements-clarity` (MIT, author Leonardo Flores, @leonardocouy; added in 06825f04 and renamed in 8453994c, both 2026-01-18). `git diff --quiet 3027f20f dbff837f -- skills/requirements-clarity` exits 0, so the baseline is the upstream text unchanged; the current files are a full rewrite. The repo has no registry row for this skill and `docs/audit/upstream-sources.json` has no row with `"skill": "requirements-clarity"`.
2. Possible deeper origin, not confirmed: the 100-point clarity score with a 90 gate resembles `skills/product-requirements` in cexll/myclaude (a Product Owner persona with its own five-dimension rubric, not the same weights), and the YAGNI/KISS question pair has no earlier source I could find. Copies in davila7/claude-code-templates (2026-01-25), pedronauck/skills and others are later than the softaworks commit, so they are not origins. No row or credit proposed for myclaude: the text is not copied, only the idea is similar.
3. Official documentation used for the Step 5 facts (proposed `unversioned` rows below): Claude Code skills docs and the Claude Help Center skills article.

## Proposed registry rows (docs/audit/upstream-sources.json)

```json
{"skill": "requirements-clarity", "kind": "github-path", "source": "softaworks/agent-toolkit:skills/requirements-clarity", "ref": "main", "credit": "softaworks/agent-toolkit"}
{"skill": "requirements-clarity", "kind": "unversioned", "source": "Claude Code docs, Extend Claude with skills: https://code.claude.com/docs/en/skills", "ref": null, "credit": "Anthropic"}
{"skill": "requirements-clarity", "kind": "unversioned", "source": "Claude Help Center, Using Skills in Claude: https://support.claude.com/en/articles/12512180-using-skills-in-claude", "ref": null, "credit": "Anthropic"}
```

(The registry file is pretty-printed, one field per line, other rows use the same fields: `skill`, `kind`, `source`, `ref`, `credit`. The coordinator adds the rows; I did not touch the registry.)

## Missing credit line

`skills/requirements-clarity/README.md` has no credit line, and neither had the baseline README (the upstream original carried none). The root README only credits the fork as a whole (line 5). Add, in the style of the sibling skills `game-changing-features`, `mui` and `qa-test-planner` (a `## Credits` section before `## Installation`):

```markdown
## Credits

Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy; this version is rewritten.
```

If the documentation pages above are listed, a second sentence in the `qa-test-planner` style may follow: "Documentation owners credited (official pages listed in `docs/audit/upstream-sources.json`, checked 2026-11-07): Anthropic (skills documentation)."

## skill-updater style review (REVIEW ONLY, no `track` call, nothing edited)

- Scope: `skills/requirements-clarity/`, a skill that is neither synced nor `gepetto`/`datadog-cli`. No source row exists, so under step 2 the review proposes the row (above) and gives no `track` call.
- Upstream drift: `gh api repos/softaworks/agent-toolkit/compare/3027f20f...main` lists 0 changed files under `skills/requirements-clarity`; the path still exists on `main` (SKILL.md, README.md); the commits-by-path query shows only the two January 2026 commits we already carry. There is nothing to adopt, adapt or ignore from upstream.
- Model-validity pass: not run (no `pi` probe, rails forbid an LLM lane here). Rules that counter a model habit and deserve the controller's probe at the restore step: "never blend or compromise conflicting answers" (Conflict rule), "no metric, deadline or number the user did not supply" (Pre-save check), "never fill sections with generic phases or architecture" (Gotchas), "proposal on 'you decide' is an assumption, not a decision". Keep all four until probed.
- Adopt/adapt/ignore list for the restore brief:
  - adapt: Why? and Simpler? core questions (s010, s021): keep one low-cost "simplest version" question in the round-1 set, as a product decision with an owner, not a design suggestion; include the MVP versus later distinction.
  - adapt: worked example (s011, s012): one session, round 1 and round 2, in the current response format (per-category lines, applicable maximum, decisions with sources, carried-over questions); no question the repository can answer; generic stack; do not paste the old scores or phases.
  - ignore: Success Criteria, DO and DON'T lists, Related Skills, Tips, execution phases, PRD structure and Instructions (intended changes or drops, see record.md).
  - fact fix (not an upstream item): README claude.ai install sentence (facts.md, corrected).
  - add: README credit line above.
