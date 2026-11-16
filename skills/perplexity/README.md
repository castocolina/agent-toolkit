# Perplexity Skill

A comprehensive guide for using Perplexity AI tools effectively within Claude Code. This skill helps you choose the right search and research tool for your needs while avoiding context bloat and unnecessary API calls.

## Purpose

This skill provides clear guidelines for when and how to use Perplexity's search and conversational AI capabilities, ensuring you select the most appropriate tool for each task while respecting token budgets and avoiding overlaps with other specialized tools.

## When to Use This Skill

Use Perplexity tools based on intent, not only on keywords: sourced explanations and current-information questions qualify. Typical requests:
- **Search queries**: "search", "find", "look up", "research"
- **Current information**: "what's the latest", "recent trends"
- **Generic questions**: Broad topics not covered by specialized tools

## When NOT to Use This Skill

Do NOT use Perplexity for:
- **Library/framework documentation** → Use Context7 MCP instead
- **Graphite `gt` CLI commands** → Use Graphite MCP instead
- **Workspace-specific questions** → Use Nx MCP instead
- **Specific URLs** → Use URL Crawler instead
- **Deep research** → Use Researcher agent (`/research`) instead

## Available Tools

### 1. Perplexity Search

**Best for**: Finding resources, URLs, and current best practices

**When to use**:
- Discovering tutorials, blog posts, or articles
- Finding recent information about technologies
- User says "search for...", "find...", "look up..."

**Default usage** (always start with these limits):
```typescript
mcp__perplexity__perplexity_search({
  query: "your search query",
  max_results: 3,           // Default is 10 - too many!
  max_tokens_per_page: 512  // Reduce per-result content
})
```

**When to increase limits**:
Only increase limits if the initial search found nothing useful (an empty or inadequate first result set). This is the only trigger, as in SKILL.md "Search and escalation". These needs do not raise limits:
- Comprehensive coverage across sources, or a multi-source report: use `/research <topic>` when configured; otherwise split into separate bounded searches and say `/research` is not configured
- A complex topic with several independent questions: split it into separate bounded searches

```typescript
// Increased limits (use sparingly, only after an empty or inadequate first result set)
mcp__perplexity__perplexity_search({
  query: "complex topic",
  max_results: 5,
  max_tokens_per_page: 1024
})
```

### 2. Perplexity Ask

**Best for**: Getting conversational explanations synthesized from web sources

**When to use**:
- Need explanation, not just search results
- Synthesize information from multiple web sources
- Explain concepts with current context

**Usage**:
```typescript
mcp__perplexity__perplexity_ask({
  messages: [
    {
      role: "user",
      content: "Explain how postgres advisory locks work"
    }
  ]
})
```

**NOT for**:
- Library documentation (use Context7)
- Deep multi-source research (use researcher agent)

### 3. Perplexity Research (PROHIBITED)

**NEVER use**: `mcp__perplexity__perplexity_research`

**Why**: No fixed token budget; runs take minutes (checked 2026-11-15, https://docs.perplexity.ai/docs/agent-api/presets)

**Use instead**: Researcher agent (`/research <topic>`)
- Provides multi-source synthesis with citations
- Use sparingly for complex questions only

## Tool Selection Chain

Route by request, as in the SKILL.md route table: pick the row that matches the request, not a fixed sequence. Check that the integration is configured before calling it.

- **Context7 MCP** - Library/framework documentation
- **Graphite MCP** - Any `gt` CLI mention
- **Nx MCP** - Questions about THIS workspace
- **Perplexity Search** - Generic searches
- **Perplexity Ask** - Conversational answers
- **Researcher agent** - Deep multi-source research (only if configured)
- **WebSearch** - Fallback when Perplexity results stay empty or inadequate

## Usage Examples

### Correct Usage

**Use Perplexity Search:**
```
User: "Find postgres migration best practices"
User: "Search for React testing tutorials"
User: "Look up latest trends in microservices"
```

**Use Perplexity Ask:**
```
User: "Explain how postgres advisory locks work"
User: "What are the trade-offs of microservices?"
```

### Incorrect Usage (Use Other Tools)

**Use Context7 instead:**
```
❌ "Search for React hooks documentation"
❌ "Find Next.js routing docs"
❌ "Look up Temporal workflow API"
```

**Use Graphite MCP instead:**
```
❌ "Search for gt stack commands"
❌ "Find gt branch workflow"
```

**Use Nx MCP instead:**
```
❌ "Search for build config" (in THIS workspace)
❌ "Find project dependencies" (in THIS workspace)
```

## Key Features

- **Token budget awareness**: Default to limited results to avoid context bloat
- **Clear tool boundaries**: Know when to use Perplexity vs. specialized tools
- **Fallback order**: Search → Ask or WebSearch when results stay inadequate
- **Research delegation**: Use researcher agent for deep dives, not raw Perplexity API

## Best Practices

1. **Start conservative**: Always use `max_results: 3` and `max_tokens_per_page: 512`
2. **Check alternatives first**: Check an alternative only when the request matches its route row (library docs, gt CLI, this workspace, one URL); do not call Context7, Graphite or Nx before a general web query.
3. **Route by intent**: "search", "find", "look up", "research", "latest" are common signals, but sourced explanations and current-information questions qualify too
4. **Avoid research tool**: Never use `perplexity_research` - use researcher agent instead
5. **Respect the routes**: Follow the tool selection routes (SKILL.md route table)

## Common Pitfalls

- Using Perplexity for library docs (use Context7)
- Using high limits by default (causes context bloat)
- Using `perplexity_research` directly (use researcher agent)
- Skipping the tool selection routes
- Calling Context7, Graphite or Nx before a general web query, or skipping them when the request matches their route row (library docs, gt CLI, this workspace, one URL)

## Integration with Other Skills

- **Context7**: For library/framework documentation
- **Graphite MCP**: For `gt` CLI operations
- **Nx MCP**: For workspace-specific queries
- **Researcher agent**: For deep research tasks
- **WebSearch**: Fallback when Perplexity results stay empty or inadequate

## Quick Decision Matrix

| User Request | Tool to Use |
|--------------|-------------|
| React hooks docs | Context7 MCP |
| gt stack command | Graphite MCP |
| Build config here | Nx MCP |
| Find migration guide | Perplexity Search |
| Explain advisory locks | Perplexity Ask |
| Deep research report | Researcher agent |
| Generic web search | Perplexity Search (WebSearch if results stay inadequate) |

## Summary

The Perplexity skill ensures you use Perplexity AI tools effectively and appropriately:
- Choose the right tool (Search vs. Ask)
- Respect token budgets with conservative limits
- Defer to specialized tools when appropriate
- Avoid the expensive research tool
- Follow the tool selection routes

By following these guidelines, you'll provide better, faster, and more cost-effective responses to users.

## Credits

Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy.

Tool facts checked against the documentation of Perplexity AI (MCP server and Agent API presets), Graphite (`gt mcp`), Nx (Nx MCP server) and Context7 (Upstash).
