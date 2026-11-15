# agent-md-refactor: sources

Checked 2026-11-15. Review only: no `track` call, no registry edit, no artifact edit.

## Origin

- The skill is a copy of `skills/agent-md-refactor` from softaworks/agent-toolkit. `git diff --quiet 3027f20f dbff837f -- skills/agent-md-refactor` exits 0, so the baseline equals the fork point. `gh api repos/softaworks/agent-toolkit/commits?path=skills/agent-md-refactor` returns two commits only: `63bebde3` (Leonardo Flores, 2026-01-19, "feat: add agent-md-refactor skill") and `39ab4806` (same author, 2026-01-19, "Update README with reference to prompt idea"). Both predate the fork point (2026-03-06), so upstream has not changed the skill since the fork.
- The idea is Matt Pocock's. The README credit points at his tweet (https://x.com/mattpocockuk/status/2012906065856270504, not fetchable: HTTP 403). The prompt itself is published in his AI Hero guide "A Complete Guide to AGENTS.md" (https://www.aihero.dev/a-complete-guide-to-agents-md, front matter updatedAt 2026-01-18; the page names no author, AI Hero is Pocock's site). The five phases of the skill follow that prompt step for step: find contradictions (ask which version to keep), identify essentials (one-sentence description, package manager if not npm, non-standard build and typecheck commands, anything relevant to every task), group the rest (e.g. TypeScript conventions, testing patterns, API design, Git workflow), create the file structure (minimal root with links, a suggested docs/ folder), flag for deletion (redundant, too vague, overly obvious). Many later copies exist (davila7 claude-code-templates, skills aggregators); they are derivatives, not origins.
- Registry state: `docs/audit/upstream-sources.json` has one row for this skill: the Matt Pocock tweet (`unversioned`, credit "Matt Pocock", last_reviewed 2026-11-04). It has no softaworks origin row and no row for the AI Hero guide. Only the repo-level softaworks row (`skill: null`, `kind: repo`) exists.
- Credit state: `skills/agent-md-refactor/README.md` has the line "Based on https://x.com/mattpocockuk/status/2012906065856270504 (Matt Pocock's Prompt Idea)" (keep it unchanged) and no softaworks credit. The root `README.md` credits softaworks only in its header and lists the skill in the table with no credit.

## Missing credit line

Add to `skills/agent-md-refactor/README.md`, as a new `## Credits` section above `## License`, next to (not replacing) the existing "Based on" line, in the form the softaworks-derived skills use (for example `skills/database-schema-designer/README.md`, line 43):

```text
## Credits

Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy.
```

The AI Hero guide may be added as a link inside the existing "Based on" sentence's neighbour line (a new line below it: `Prompt text: https://www.aihero.dev/a-complete-guide-to-agents-md`); the existing line itself is not reworded.

## Proposed registry rows

The first row is the softaworks origin (precedent: the marp-slide proposal; its `credit` text "softaworks/agent-toolkit" appears verbatim in the credit line above, as `check --strict` requires). The second is the prompt's published source. The last two are the official documentation pages used in facts.md. `unversioned` rows get no staleness signal from `upstreams`; the date in facts.md is the only age marker.

```json
{"skill": "agent-md-refactor", "kind": "github-path", "source": "softaworks/agent-toolkit:skills/agent-md-refactor", "ref": "main", "credit": "softaworks/agent-toolkit"}
{"skill": "agent-md-refactor", "kind": "unversioned", "source": "Matt Pocock, A Complete Guide to AGENTS.md (the refactor prompt): https://www.aihero.dev/a-complete-guide-to-agents-md", "ref": null, "credit": "Matt Pocock"}
{"skill": "agent-md-refactor", "kind": "unversioned", "source": "Claude Code docs, How Claude remembers your project (CLAUDE.md, imports, .claude/rules, AGENTS.md): https://code.claude.com/docs/en/memory", "ref": null, "credit": "Anthropic"}
{"skill": "agent-md-refactor", "kind": "unversioned", "source": "GitHub Docs, Support for different types of custom instructions (Copilot): https://docs.github.com/en/copilot/reference/custom-instructions-support", "ref": null, "credit": "GitHub"}
```

All four pass `validate_entry` by shape (existing kebab-case skill, allowed kind, `github-path` source `owner/repo:path` with a non-empty `ref`, `unversioned` with `ref` null, non-empty source and credit).

## skill-updater style review (review only)

Read `skills/skill-updater/SKILL.md`. Step 2 applies: the credit names an upstream (softaworks) with no row, so the row is proposed above and no `track` call is made; `upstreams` was not run (the one existing row is `unversioned`, which always reports `stale: false`).

- Upstream softaworks changes since the fork: none. Adopt: none. Adapt: none. Ignore: not applicable.
- Original prompt (AI Hero) against the skill:
  - Adapt (small): the explicit "package manager, only if not npm" item of the essentials list; the current step 3 covers it only through "essential commands". One clause in step 3 is enough.
  - Ignore: "a suggested docs/ folder structure" (the current default `.claude/`, with `docs/agent-instructions/` as fallback, is deliberate); the criterion "redundant (the agent already knows this)" as a deletion licence (it contradicts the current step 6 safety rule, record row s027); the generic category menu (record row s025).
- Platform facts the skill relies on (facts.md), adapt items for the restore brief, all to go into one new `references/` file (for example `references/harness-loading.md`) with a one-line trigger at step 5, so SKILL.md stays small and every value is a pointer to the live docs page, not a pinned number:
  1. Correct the Gotcha "Claude Code does not automatically load arbitrary files under `.claude/`": the subfolder `.claude/rules/` is the exception (files without `paths:` frontmatter load at launch), so conditional topic files must not sit there unless they carry `paths:` frontmatter; a `paths:` rule is itself a native conditional-load mechanism for file-type topics (for example testing rules for `**/*.test.ts`).
  2. Add the `@path` import form and its trade-off: it expands into context with the importing file, so it organises but does not reduce context cost, unlike a read-condition link.
  3. Add the AGENTS.md rule: Claude Code reads `AGENTS.md` only when no `CLAUDE.md` or `CLAUDE.local.md` is in the working directory or above; an `@AGENTS.md` import in a `CLAUDE.md` shares one file across tools.
  4. Replace `COPILOT.md` in the description and README with `.github/copilot-instructions.md` (Copilot also reads `AGENTS.md`, `CLAUDE.md` and `GEMINI.md` on most surfaces); the replacement removes no credit line.
  5. Reconcile README with SKILL.md: README still teaches "under 50 lines", "delete liberally", "aim for 3-8 files" and a deletion-first Phase 5, all of which SKILL.md replaced on purpose (and the small-root-file eval asserts the opposite). Edit the README sentences, keep the credit and license lines, and write a record row for each removed README line (those README sections, s001-s018, are currently `present`, so record-check does not name them but the removal rule still applies).
- Model-validity pass: not run (review only, no probe lane). The skill's counter-habit rules are "do not silently pick one side of a contradiction", "do not delete project-specific safety overrides as presumed defaults" and "do not stop at a request for missing files"; they restrain eagerness, not a feature a newer model has outgrown, and the evals (`claude-md-conflicts`, `small-root-file`) cover them. No removal is proposed.

## Items for the restore brief

Restore rows from record.md: none (no `restore-*` decision). One pending row, `s025 Phase 3: Group the Rest` (`drop-pending`): Step 3 verdict DROP (see the report), so the safe default is no interim restore if the controller accepts the verdict. Adapt items: the five listed above plus the one-clause package-manager adaptation and the credit line.
