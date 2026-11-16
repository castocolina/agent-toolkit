# Sources: game-changing-features (2026-11-07)

## Origins found

1. **softaworks/agent-toolkit, skills/game-changing-features** (README.md and SKILL.md). The baseline `dbff837f` files and the fork point `3027f20f` are byte-identical to each other, and to upstream `main` today (SKILL.md blob 667daffa; the only upstream commit touching the path is 06825f04, 2026-01-18, "feat: add 23 curated skills"). Compared with `gh api` raw contents: both files identical to the baseline, so there is no upstream change to review.
2. Not an origin: `davila7/claude-code-templates` (cli-tool/components/skills/productivity/game-changing-features, commit 1c194fd2, 2026-01-25) and `aleksiuno/backlog-generator-prompt` (2026-02-23) hold the same text but are dated after softaworks and carry no credit. Many other mirrors exist (skills.sh, aiskillstore, skillshub). The author before softaworks was not found; a phrase search ("find the moves that 10x the product's value") returned only copies. No row is proposed for them.

## Registry row proposed (docs/audit/upstream-sources.json)

The artifact has no row today (grep of the registry: no match).

```json
{
  "skill": "game-changing-features",
  "kind": "github-path",
  "source": "softaworks/agent-toolkit:skills/game-changing-features",
  "ref": "main",
  "credit": "softaworks/agent-toolkit"
}
```

The `credit` text appears verbatim in the credit line below, which `missing_credit` needs.

## Missing credit line

`skills/game-changing-features/README.md` has no credit line (the baseline README had none either). Add, as the sibling softaworks skills do (database-schema-designer, naming-analyzer, meme-factory):

```
## Credits

Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy.
```

## Documentation rows

None proposed: the current files and the planned restores contain no vendor-specific facts (see facts.md), so no `unversioned` rows are needed.

## skill-updater style review (review only, no `track` call, `upstreams` not run)

- Upstream drift: none (both files identical to upstream `main`). Adopt: none. Adapt: none. Ignore: none.
- Local divergence from the baseline is deliberate and is not an upstream matter: the skill was rewritten to be evidence-grounded (baseline, scoring formula, one Do Now, hypothesis labels). Restore items for the brief are in the record (restore-references rows) and are local content, not upstream changes.
- Model-validity pass: not run. The probe lane sends a prompt to an LLM, which the analyst rails forbid; for the controller, the rules that counter a model habit are the four NEVER rules (no bare "add AI", the request does not anchor Do Now, `hypothesis:` prefix, parity is not leverage). Suggested probe prompt per rule: ask for 10x ideas for a small SaaS app with no evidence and check for bare "add AI/dashboard" ideas and unprefixed numbers.
- Items for the restore brief: one `references/` file (suggested `ideation-lenses.md`) holding the idea-category table, the per-tier discovery questions, the unstick prompts, the mindset rules (with the "Not 10% better... how did I live without this?" bar as its lead line), and, if the controller keeps them, the Frequency and Defensibility lenses; SKILL.md links it from Discover. Add the credit line above and the registry row. Add an eval scenario for the restored behavior (a session that runs the category check and names a category-sourced idea with its mechanism).

## Controller one-line rows

{"skill": "game-changing-features", "kind": "github-path", "source": "softaworks/agent-toolkit:skills/game-changing-features", "ref": "main", "credit": "softaworks/agent-toolkit"}
