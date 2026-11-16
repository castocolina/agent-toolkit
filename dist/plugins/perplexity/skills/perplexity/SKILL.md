---
name: perplexity
description: "Route external web research to Perplexity MCP: perplexity_search for current facts and links (default max_results 3, max_tokens_per_page 512), perplexity_ask for sourced synthesis. Use for general web information, recent news/comparisons/tutorials, or current-information questions. Not for library/framework docs (Context7), Graphite gt CLI help (Graphite MCP), workspace questions (Nx MCP), one supplied URL (URL Crawler), or repository-local lookup."
---

# Perplexity web research

Use based on intent, not whether the user says “search”: sourced explanations and current-information questions qualify. Do not route unrelated workspace/repository lookup here.

## Route by request

First ask: is this a current public fact or a sourced explanation, or is it a library doc, a `gt` command, a question about this workspace, or one supplied URL? Only the first reaches Perplexity.

| Request | Route |
|---|---|
| Official library/framework documentation | Context7, if configured |
| Graphite `gt` CLI help | Graphite MCP, if configured |
| This workspace/project question | Nx MCP, if configured |
| Fetch one supplied URL | URL Crawler, if configured |
| Current public facts, resources, links | Perplexity Search |
| Sourced conversational explanation | Perplexity Ask |
| Multi-part investigation requiring broad source coverage | Configured `/research` agent |

Check the requested integration is actually available before calling it. If it is unavailable, use an available appropriate tool, say which substitution was made, and report the limitation if no suitable tool exists. Do not assume MCP tools, `/research`, credentials, or integrations exist.

If only the selected Perplexity tool is unavailable, use the other appropriate Perplexity tool or WebSearch, say which substitution was made, and report the limitation if no suitable tool exists. If `perplexity_search` and `perplexity_ask` are both absent, use WebSearch when it is available and say that Perplexity was not configured. If WebSearch is also absent, check for another available appropriate web or browsing tool and use it, saying which substitution was made; report that no web tool is available, and invent nothing, only when none exists.

Read README.md only when you need the call-shape examples; do not load it for a single routing decision.

## Search and escalation

Search defaults: `max_results: 3`, `max_tokens_per_page: 512`. These are this skill's own limits for `perplexity_search`; the tool's defaults are 10 results and 1024 tokens per page (read the live schema; checked 2026-11-15, https://github.com/perplexityai/modelcontextprotocol), so escalating from this skill's 3 results and 512 tokens to 5 and 1024 raises both values; the ceiling stays below the tool default for results (10) and equals it for tokens per page (1024). Query only information safe to disclose externally: search terms leave the workspace. Ask before sending confidential identifiers, unreleased details, or private data; redact where possible.

A bounded search is sufficient for one factual question or a small number of claims with clear authoritative sources. Before escalating, ask one question: is the gap one missing fact (raise Search limits), several independent questions (split into separate bounded searches), or a sourced explanation (use Ask)?

- The only trigger for raising Search limits to 5 results / 1024 tokens is an empty or inadequate first result set. Raise them modestly, then use Ask or WebSearch if available.
- Material disagreement between sources is not a reason to raise limits: open the cited pages and, if it is still unresolved, use Ask.
- A need for coverage across source types, or a requested multi-source report, uses `/research <topic>` only if configured; otherwise split into separate bounded searches and say `/research` is not configured.
- Several independent subquestions are split into separate bounded searches instead of escalating.

Do not use `mcp__perplexity__perplexity_research` in this environment: it takes only `messages` (no budget, recency or domain parameters), so its token spend is unbounded; it returns numbered citations, but a run can use up to 40 tool calls and takes minutes (checked 2026-11-15, https://docs.perplexity.ai/docs/agent-api/presets). Search result snippets can be stale or incomplete; open and verify source pages, dates, and claim support. Attribute claims to the sources actually inspected and distinguish source statements from synthesis.

For Ask follow-ups, include the prior user/assistant turns needed for context; use a fresh messages array for an unrelated topic.

## Gotchas

- Snippets can be stale: open the cited page before attributing a claim to it.
- Never present an unverified citation as support: inspect an available primary source, or qualify the claim and report the limit.
- Search terms leave the workspace: ask before sending confidential or unreleased identifiers.
