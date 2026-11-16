# Sources: perplexity

Checked 2026-11-15. Review only: no `track` call, no registry edit, no artifact edit. `upstreams` was not run: the registry has no row for this skill (`rg perplexity docs/audit/upstream-sources.json` finds nothing), so there is nothing for it to read; the upstream comparison below was done with `gh api` and `git`.

## Origins found

1. **softaworks/agent-toolkit, `skills/perplexity`** (origin of the whole skill). At the fork point `3027f20f` the skill's two files (`SKILL.md`, `README.md`) are byte-identical to the baseline `dbff837f` (`git diff --stat 3027f20f dbff837f -- skills/perplexity` is empty), and upstream `main` still lists the same blob SHAs (`README.md` `fad1bc24...`, `SKILL.md` `dbf0d69f...`, equal to `git rev-parse 3027f20f:skills/perplexity/...`). The upstream path's last commit is `c0556074` (2026-01-18, "feat: add plugin-forge skill and fix perplexity frontmatter"), the commit already in our history, so upstream has not changed since. The upstream author is Leonardo Flores (@leonardocouy), per the fork notice in the root `README.md` line 5. No registry row names this skill, and no credit line exists in any of its files.
2. No second origin. A web search on the distinctive phrases ("Default is 10 - too many", `max_tokens_per_page: 512`, "Tool Selection Chain") found only the vendor's own MCP schema pages and unrelated third-party servers; nothing credits a source for the routing chain. The routing rules are repo-local policy, not copied vendor text.

## Missing credit line

Add to `skills/perplexity/README.md` as a new final section (never reword it later; the line is the one used by `naming-analyzer` and `mui`):

```text
## Credits

Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy.
```

The `credit` field of the origin row below (`softaworks/agent-toolkit`) then appears verbatim in README.md, so `audit.py check --strict` raises no `missing_credit`. Each unversioned row's `credit` below is also a word already present in SKILL.md or README.md (`Perplexity AI`, `Graphite`, `Nx`, `Context7`), so those rows need no further credit text.

## Proposed registry rows (docs/audit/upstream-sources.json)

Origin row (`credit` follows the `naming-analyzer` precedent):

```json
{"skill": "perplexity", "kind": "github-path", "source": "softaworks/agent-toolkit:skills/perplexity", "ref": "main", "credit": "softaworks/agent-toolkit"}
```

Docs pages used for facts.md (each `unversioned`, as plan 14 Step 5 says; `upstreams` never reports these stale, so only a `skill-updater` run re-reads them):

```json
{"skill": "perplexity", "kind": "unversioned", "source": "Perplexity API Platform MCP Server (tool list, schemas and presets in README and src/server.ts): https://github.com/perplexityai/modelcontextprotocol", "ref": null, "credit": "Perplexity AI"}
{"skill": "perplexity", "kind": "unversioned", "source": "Perplexity docs, MCP Server integration: https://docs.perplexity.ai/docs/getting-started/integrations/mcp-server", "ref": null, "credit": "Perplexity AI"}
{"skill": "perplexity", "kind": "unversioned", "source": "Perplexity docs, Search quickstart (max_results default and range): https://docs.perplexity.ai/docs/search/quickstart", "ref": null, "credit": "Perplexity AI"}
{"skill": "perplexity", "kind": "unversioned", "source": "Perplexity docs, Agent API presets (fast, high step budgets, output-token budget): https://docs.perplexity.ai/docs/agent-api/presets", "ref": null, "credit": "Perplexity AI"}
{"skill": "perplexity", "kind": "unversioned", "source": "Graphite docs, gt mcp: https://graphite.com/docs/gt-mcp", "ref": null, "credit": "Graphite"}
{"skill": "perplexity", "kind": "unversioned", "source": "Nx docs, Nx MCP server reference: https://nx.dev/docs/reference/nx-mcp", "ref": null, "credit": "Nx"}
{"skill": "perplexity", "kind": "unversioned", "source": "Context7 (Upstash), README: https://github.com/upstash/context7", "ref": null, "credit": "Context7"}
```

`https://docs.perplexity.ai/api-reference/search-post` and `https://nx.dev/docs/getting-started/ai-setup` were also read; they add no fact the rows above do not cover, so no row is proposed for them.

## skill-updater style review (review only)

- **Step 2/3/4 (rows, error, contents test):** no registry row exists, so per the skill a credit-less origin is proposed as a row (above) and no `track` call is given. The upstream path resolves (`gh api repos/softaworks/agent-toolkit/contents/skills/perplexity` lists both files) and has no commit after the one in our history: nothing to adopt, adapt or ignore from upstream.
- **Model-validity pass:** no rule exists to counter a model habit. The `perplexity_research` prohibition is a cost-and-scope policy, the routing table is a tool-boundary rule, and the limits are a budget policy; none suppresses a model behavior, so no probe lane was run and no `--model` is recorded.
- **Vendor drift worth the restore brief** (tool changes since the artifact was written; adopt, adapt or ignore):
  1. **adapt** README.md reconciliation with SKILL.md (README is unchanged since the baseline and contradicts it): (a) "Use Perplexity tools ONLY when users explicitly request" and the keyword list in `When to Use This Skill` against SKILL.md's intent-based opener; (b) the "30-50k tokens" figure in `3. Perplexity Research (PROHIBITED)` and `Prohibited Tool` (facts.md row 10); (c) the numbered `Tool Selection Chain` and the "WebSearch last resort" lines against the SKILL.md route table. Each removed or reworded README line needs a `para:` row (record-check will name them).
  2. **adapt** one clause in SKILL.md facts: say the 3 and 512 limits apply to `perplexity_search` and that the tool's own defaults are 10 results and 1024 tokens per page (so 1024 is the default, not an increase; the schema maximum is 2048). Pointer wording preferred over pinning the numbers.
  3. **adapt (optional)** SKILL.md `perplexity_research` wording: replace "without the citation and scope controls needed here" with "no budget, recency or domain parameters (the tool takes only messages)" (facts.md row 9). The prohibition itself stays.
  4. **ignore** vendor additions the tool schema already carries to the model: `search_recency_filter`, `search_domain_filter`, `search_type: "fast"` on `perplexity_search`, and the `max_tokens` budgets of `perplexity_ask`.
  5. **ignore (user decision)** `perplexity_reason` (Agent API `medium` preset) is a fourth tool the skill never mentions; the route table sends reasoning questions nowhere. Adding a row is a scope change, so it is listed for the controller rather than proposed as a fix.
- **Out-of-scope finding (not an artifact file):** `.claude-plugin/marketplace.json` line 48 still carries the old keyword-only description ("Use when user says 'search', 'find', 'look up', 'ask', 'research', or 'what's the latest' for generic queries"), which contradicts SKILL.md's intent-based description. It is not on the plan 14 scope-check allowlist; report it to the user.
