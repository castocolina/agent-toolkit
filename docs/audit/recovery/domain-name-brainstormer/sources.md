# Sources: domain-name-brainstormer

Reviewed 2026-11-07, base 972b61fb, baseline dbff837f, upstream fork point 3027f20f.

## Origins found

1. **Lenny's Newsletter, "Everyone should be using Claude Code more" (Lenny Rachitsky, dated Oct 14, 2025 on the page)**. Item 1, "Brainstorming domain names", credits Ben Aiad: "Just describe your project, and it'll suggest creative options across multiple TLDs". This is the inspiration the SKILL.md and README credit lines name. URL: https://www.lennysnewsletter.com/p/everyone-should-be-using-claude-code (fetched 2026-11-07). Existing registry row has the title but no URL.
2. **softaworks/agent-toolkit, `skills/domain-name-brainstormer`** (the fork origin; the root README line 5 credits the repo as a whole). The baseline `SKILL.md` and `README.md` are byte-identical to the upstream files at `3027f20f` (diff empty); upstream's newest commit on the path is `06825f04` (2026-01-18, before the fork point) and the path still holds only `README.md` and `SKILL.md`. The current skill is a full rewrite, so no upstream text is carried over except the Ben Aiad credit. The skill has no per-skill credit for softaworks.
3. No other uncredited distinctive content: the baseline text is generic naming advice and prompts; a web search for the "Domain Name Brainstormer" skill finds the same softaworks text re-listed on many mirrors (claudemarketplaces.com, skills.sh, awesome-skills lists), all downstream of softaworks. The Procedure, labels and Gotchas are our own.

## Credit lines

- Present and verbatim: SKILL.md `**Inspired by:** Ben Aiad's use case from Lenny's Newsletter`; README `Inspired by Ben Aiad's use case from Lenny's Newsletter.` Nothing to restore. The registry row's `credit` ("Ben Aiad") appears in both.
- Missing (proposal, the controller decides): a softaworks origin line in `skills/domain-name-brainstormer/README.md` under Credits. Exact line to add after the existing one:
  `Based on the original skill in [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit/tree/main/skills/domain-name-brainstormer); this version is rewritten.`
  If the row below is added with `credit` = `softaworks/agent-toolkit`, that string must also appear verbatim in the README or SKILL.md (`check --strict` `missing_credit`); the line above contains it.

## Proposed registry rows (docs/audit/upstream-sources.json)

Replace the existing row's `source` only if the controller wants the URL in it (the `track --source` value must then be copied exactly). Proposed replacement:

```json
{"skill": "domain-name-brainstormer", "kind": "unversioned", "source": "Lenny's Newsletter, Everyone should be using Claude Code more (Ben Aiad's domain-name use case, item 1): https://www.lennysnewsletter.com/p/everyone-should-be-using-claude-code", "ref": null, "last_reviewed": "2026-11-07", "status": "current", "credit": "Ben Aiad"}
```

New origin row (softaworks):

```json
{"skill": "domain-name-brainstormer", "kind": "github-path", "source": "softaworks/agent-toolkit:skills/domain-name-brainstormer", "ref": "main", "last_reviewed": "2026-11-07", "status": "current", "credit": "softaworks/agent-toolkit"}
```

Official docs used for facts (one `unversioned` row each, `ref` null, `credit` = the vendor, `last_reviewed` 2026-11-07, `status` current):

```json
{"skill": "domain-name-brainstormer", "kind": "unversioned", "source": "RDAP.org about page: https://about.rdap.org/", "ref": null, "credit": "RDAP.org"}
{"skill": "domain-name-brainstormer", "kind": "unversioned", "source": "IANA RDAP bootstrap for DNS (dns.json): https://data.iana.org/rdap/dns.json", "ref": null, "credit": "IANA"}
{"skill": "domain-name-brainstormer", "kind": "unversioned", "source": "ICANN UDRP policy: https://www.icann.org/resources/pages/policy-2012-02-25-en", "ref": null, "credit": "ICANN"}
{"skill": "domain-name-brainstormer", "kind": "unversioned", "source": "ICANN EPP status codes: https://www.icann.org/resources/pages/epp-status-codes-2014-06-16-en", "ref": null, "credit": "ICANN"}
{"skill": "domain-name-brainstormer", "kind": "unversioned", "source": "Google Registry .dev, .app, .page pages (HSTS preload): https://www.registry.google/domains/dev/", "ref": null, "credit": "Google Registry"}
{"skill": "domain-name-brainstormer", "kind": "unversioned", "source": "HSTS Preload List Submission: https://hstspreload.org/", "ref": null, "credit": "Google Chrome team"}
{"skill": "domain-name-brainstormer", "kind": "unversioned", "source": "Chromium IDN display policy: https://chromium.googlesource.com/chromium/src/+/main/docs/idn.md", "ref": null, "credit": "Chromium"}
{"skill": "domain-name-brainstormer", "kind": "unversioned", "source": "Unicode UTS #39 Security Mechanisms: https://www.unicode.org/reports/tr39/", "ref": null, "credit": "Unicode Consortium"}
{"skill": "domain-name-brainstormer", "kind": "unversioned", "source": "Dynadot Help, registry premium domains: https://www.dynadot.com/help/question/what-are-registry-premium-domains", "ref": null, "credit": "Dynadot"}
{"skill": "domain-name-brainstormer", "kind": "unversioned", "source": "Claude Help Center, Create and edit files with Claude: https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude", "ref": null, "credit": "Anthropic"}
```

Credit-verbatim caution: `check --strict` fails `missing_credit` when a row's `credit` text is not in SKILL.md, README.md or references/*.md. Of the docs rows, none of the credits above appear in the skill today. The existing house pattern for `unversioned` fact rows should be followed (does the `credit` field have to appear? yes if present). Either add a short "Sources" line to the README naming those vendors, or omit `credit` on the docs rows (it is optional per `validate_entry`). Recommended: omit `credit` on the docs rows, keep it on the two origin rows.

## skill-updater review (REVIEW ONLY, no `track` call)

- Scope resolved: `skills/domain-name-brainstormer/`, not synced.
- Rows today: one `unversioned` row. `upstreams` read-only: `error: null`, `stale: false`, `ours_updated` 2026-11-06 (unversioned rows are never compared; per the skill's Gotchas the source was read instead). The Lenny article was read and contains the Ben Aiad credit: status `current`.
- Proposed `github-path` row (softaworks): read upstream at `main`. The path exists (`README.md`, `SKILL.md`), its last commit is `06825f04`, 2026-01-18, which is older than the fork point and identical to the baseline text. No upstream change since the fork: nothing to adopt or adapt.
  - ignore: upstream's availability claims, price table and emoji example; they contradict the current Gotchas (never write "available", never quote a price) and the records show the removal is an intended safety change.
  - ignore: upstream "Register immediately", social-handle and logo next steps; outside the current description.
- Model-validity pass (rules that counter a model habit): the skill's rules (never say "available", never quote prices, label status, UDRP framing) counter a strong, well-known model habit (a model asked "is X.com available?" without tools reliably guesses). Not run: the brief makes the review read-only and the tool-less probe lane is a separate LLM call; the rules concern fabricated claims a model does make, so keep all of them. Record as not probed this session.
- Adopt / adapt / ignore list for the restore brief: adopt none; adapt none required. Optional (the controller decides, not a restore): add one worked example in the current honest format (grouped by naming direction, status labels, rdap.org URLs, no "available" word) to `references/` or to README, because the Output section describes the table in prose only and the baseline's example was the part users could copy.
- gepetto and datadog-cli untouched.
