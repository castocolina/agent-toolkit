# qa-test-planner: sources (plan 14, batch 3)

Checked 2026-11-07.

## Origin

- The skill is the softaworks/agent-toolkit skill `skills/qa-test-planner`. The fork point `3027f20f` and the baseline `dbff837f` hold identical skill files (`git diff 3027f20f dbff837f -- skills/qa-test-planner` is empty), so every baseline section is upstream text.
- Upstream history for the path (`gh api repos/softaworks/agent-toolkit/commits?path=skills/qa-test-planner&sha=main`): one commit, `06825f04` by Leonardo Flores (@leonardocouy), 2026-01-18, "feat: add 23 curated skills with comprehensive documentation". The path still exists on `main` (contents API exit 0). No per-skill author is named upstream; the original README carries no credit line, only two decorative quotes.
- The current SKILL.md, references and scripts are a heavy local rewrite (SKILL.md 757 lines at baseline, 147 now). Origin is still softaworks.
- No registry row exists for `qa-test-planner`, and the skill README has no credit line. `docs/audit/upstream-sources.json` has only the repo-level row `softaworks/agent-toolkit` (`kind: repo`).
- Searching a distinctive phrase on the web was not needed: the origin is fully explained by the fork-point tree and the upstream commit above.

## Proposed registry rows (not applied)

Origin row, same shape and credit wording as the `database-schema-designer` row:

```json
{"skill": "qa-test-planner", "kind": "github-path", "source": "softaworks/agent-toolkit:skills/qa-test-planner", "ref": "main", "credit": "softaworks/agent-toolkit"}
```

One `unversioned` row per official docs page used for the facts (see facts.md); `ref` is null, `credit` is the vendor:

```json
{"skill": "qa-test-planner", "kind": "unversioned", "source": "Figma Help, Manage color profiles: https://help.figma.com/hc/en-us/articles/360039825114-Manage-color-profiles", "ref": null, "credit": "Figma"}
{"skill": "qa-test-planner", "kind": "unversioned", "source": "Figma Help, Explore text properties: https://help.figma.com/hc/en-us/articles/360039956634-Explore-text-properties", "ref": null, "credit": "Figma"}
{"skill": "qa-test-planner", "kind": "unversioned", "source": "Figma Plugin API, LetterSpacing: https://developers.figma.com/docs/plugins/api/LetterSpacing/", "ref": null, "credit": "Figma"}
{"skill": "qa-test-planner", "kind": "unversioned", "source": "Figma Help, Share a link to a specific layer or frame: https://help.figma.com/hc/en-us/articles/360040531773-Share-a-link-to-a-specific-layer-or-frame", "ref": null, "credit": "Figma"}
{"skill": "qa-test-planner", "kind": "unversioned", "source": "Figma MCP server, Tools and prompts: https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/", "ref": null, "credit": "Figma"}
{"skill": "qa-test-planner", "kind": "unversioned", "source": "OWASP Top 10:2025: https://top10.owasp.org/2025", "ref": null, "credit": "OWASP Foundation"}
{"skill": "qa-test-planner", "kind": "unversioned", "source": "Stripe docs, Supported currencies (zero-decimal currencies): https://docs.stripe.com/currencies", "ref": null, "credit": "Stripe"}
```

Each row needs `last_reviewed` 2026-11-07 and `status: current` when added through `track`/the controller, as other unversioned rows have.

## Missing credit line

The skill README has no credit. Add this section to `skills/qa-test-planner/README.md` (same wording as `skills/database-schema-designer/README.md` and `skills/gemini/README.md`), before any License section:

```markdown
## Credits

Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy.
```

The root README table row for qa-test-planner (line 147) has no credit either; the fork credit on README line 5 names softaworks. Nothing to change there unless the controller wants a per-skill line.

The baseline README quotes ("Testing shows the presence, not the absence of bugs." - Edsger Dijkstra; "Quality is not an act, it is a habit." - Aristotle) were removed. They carry attribution lines; row s034 is `drop-pending`, so the user decides. If the user rejects the drop, restore both lines verbatim.

## skill-updater style review (review only, no `track` call)

Run on 2026-11-07 without any `track` call, following `skills/skill-updater/SKILL.md`:

- Step 2: no registry row for the artifact other than none at all. A credit line naming an upstream does not exist either, so the registry row above is proposed and no `track` call is given (`track` cannot create a source row).
- Step 4 contents test: `gh api repos/softaworks/agent-toolkit/contents/skills/qa-test-planner?ref=main` exits 0. Upstream has a single commit (2026-01-18) that predates the fork point (2026-03-06), so there is no upstream change to adopt, adapt or ignore. Upstream changes: none.
- Local divergence (for the restore brief): the whole rewrite is deliberate (explicit trigger, `Unknown` instead of guesses, release gate instead of pass rate, severity by cost). Nothing in the upstream text should be adopted over it.
- Model-validity pass: not run. It needs an LLM probe lane and the rails forbid dispatching or judging with an LLM lane in this task. Candidate rules for the controller to probe if wanted: never fill a gap with a plausible value (section 2), never write Always for an intermittent bug (3b), never take a sandbox result as production proof (section 6), never write a bare pass rate as an exit gate (section 6). Each counters a plain model habit, so the expected outcome is keep.

### Adopt, adapt, ignore items for the restore brief

- adopt: none (upstream is unchanged since the baseline and the baseline text is what the restore rows rewrite).
- adapt (restore rows rewritten in the current style, into `references/`): the s051 plan sections without the 90 percent exit line; the s058/s107-s110/s131 suite tiers and critical path questions; the s061/s118 run report template with per-case evidence and no pass rate as gate; the s072-s074, s077, s082 bug template blocks; the s122, s126, s128, s129, s070, s071 case templates and examples with seeded data and placeholder credentials; the s091/s093/s095/s104/s125 Figma checklist.
- ignore: s054, s056, s060, s079, s105, s115 pass-rate, color-picker, response-time and severity-equals-priority wording (deliberate corrections); s101 and s117 automation tooling (out of scope); s032 time-saved table (unsourced marketing).
