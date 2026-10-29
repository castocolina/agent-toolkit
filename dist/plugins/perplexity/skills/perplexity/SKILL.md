---
name: perplexity
description: "Route external web research to Perplexity MCP: perplexity_search for current facts and links (default max_results 3, max_tokens_per_page 512), perplexity_ask for sourced synthesis. Use for general web information, recent news/comparisons/tutorials, or current-information questions. Not for library/framework docs (Context7), Graphite gt CLI help (Graphite MCP), workspace questions (Nx MCP), one supplied URL (URL Crawler), or repository-local lookup."
---

# Perplexity web research

Use based on intent, not whether the user says “search”: sourced explanations and current-information questions qualify. Do not route unrelated workspace/repository lookup here.

## Route by request

| Request | Route |
|---|---|
| Official library/framework documentation | Context7, if configured |
| Graphite `gt` CLI help | Graphite MCP, if configured |
| This workspace/project question | Nx MCP, if configured |
| Fetch one supplied URL | URL Crawler, if configured |
| Current public facts, resources, links | Perplexity Search |
| Sourced conversational explanation | Perplexity Ask |
| Multi-part investigation requiring broad source coverage | Configured `/research` agent |

Check the requested integration is actually available before calling it. If unavailable, use an available appropriate tool; otherwise report the limitation. Do not assume MCP tools, `/research`, credentials, or integrations exist.

## Search and escalation

Search defaults: `max_results: 3`, `max_tokens_per_page: 512`. Query only information safe to disclose externally: search terms leave the workspace. Ask before sending confidential identifiers, unreleased details, or private data; redact where possible.

A bounded search is sufficient for one factual question or a small number of claims with clear authoritative sources. Escalate when there are several independent subquestions, an explicit need for coverage across multiple source types, or material disagreement remains after checking primary sources. Raise Search limits modestly (up to 5 results / 1024 tokens) only when the initial result set is empty or inadequate, then use Ask or WebSearch if available. For broad investigations, use `/research <topic>` only if configured.

Do not use `mcp__perplexity__perplexity_research` in this environment: it has unbounded token spend without the citation and scope controls needed here. Search result snippets can be stale or incomplete; open and verify source pages, dates, and claim support. Attribute claims to the sources actually inspected and distinguish source statements from synthesis.

For Ask follow-ups, include the prior user/assistant turns needed for context; use a fresh messages array for an unrelated topic.
