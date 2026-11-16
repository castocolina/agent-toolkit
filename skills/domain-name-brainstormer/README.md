# Domain Name Brainstormer

Brainstorms, screens and ranks brandable domain names for apps, products, companies and personal brands. Each candidate carries a registration-status label that comes from an RDAP or WHOIS lookup, or reads `unverified` when no lookup ran. The skill never calls a name available or quotes a price; a registrar's checkout confirms both.

## When to use

- Naming a new project, product or company
- Launching or rebranding
- Replacing a first-choice domain that is taken
- Reading RDAP or WHOIS results you already ran

It is not for DNS, email, hosting or transfers on a domain you already own, for product names without domains, for social handles, or for trademark clearance.

## Example requests

```
I'm building a project management tool for remote teams. Suggest domain names.
Brainstorm 12 short names for a Spanish-English tutoring app, .com and .app.
My bakery's first-choice domain is taken; suggest alternatives.
Here are my RDAP results; which names are registered?
```

Mention the target languages, a budget cap and any word that must or must not appear. Without them the skill assumes an English-speaking audience, 10 short candidates and `.com` first.

## What is in the skill

| File | Purpose |
|------|---------|
| `SKILL.md` | Defaults, the generate-screen-rank procedure, status labels, lookup fallbacks and gotchas |
| `references/example.md` | A filled-in shortlist in the output format, with illustrative statuses |
| `evals/` | Output evals, trigger queries and a pasted-RDAP fixture |

## Install

Claude Code: `cp -r skills/domain-name-brainstormer ~/.claude/skills/`

claude.ai: add `SKILL.md` to project knowledge or paste it into the conversation. Live lookups need network access to `rdap.org` and the registry RDAP servers; add them in your capabilities settings (`claude.ai/settings/capabilities`; Team and Enterprise owners manage allowed domains in organization settings, and labels change between plans and releases, see [Anthropic's Help Center](https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude), checked 2026-11-07).

## Credits

Inspired by Ben Aiad's use case from Lenny's Newsletter.

Based on the original skill in [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit/tree/main/skills/domain-name-brainstormer); this version is rewritten.

Documentation owners credited (official pages listed in `docs/audit/upstream-sources.json`, checked 2026-11-07): RDAP.org, IANA, ICANN, Google Registry, Google Chrome team, Chromium, Unicode Consortium, Dynadot, Anthropic.
