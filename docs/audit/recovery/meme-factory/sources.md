# Sources: meme-factory

Reviewed 2026-11-07 (analyst, plan 14 batch 4). No registry row exists for meme-factory today (`grep -i meme docs/audit/upstream-sources.json` is empty). No `track` call was made.

## Origins found

1. **softaworks/agent-toolkit, skills/meme-factory** (fork origin). The baseline `dbff837f` files are byte-identical to the fork point `3027f20f` (same blob ids for SKILL.md, README.md, references/examples.md, references/markdown-memes-guide.md and scripts/meme_generator.py) and to upstream `main` today (upstream file blob ids read with `gh api repos/softaworks/agent-toolkit/contents/skills/meme-factory`; the path was last touched 2026-01-18 by the commit that added 23 skills, and upstream main head is 3027f20f, 2026-03-05). Upstream has not changed since the fork, so nothing is staleness-flagged.
2. **jacebrowning/memegen** (the service and its README). The current README already credits it ("by Jace Browning (MIT)"). Every escape rule, query parameter and URL shape in SKILL.md comes from its README and live behavior.
3. **Authorship of the guide.** A web search for the guide title and the distinctive "Department of Vibes" notice found no third-party origin; an agent-skills index (agentskillsfinder.com) lists meme-factory by softaworks. The guide is therefore softaworks text. Two samples are public internet memes with no single author: the "Navy Seals" copypasta in old s088 (known meme text, profane, not restored) and the greentext/Wojak formats. No credit is owed for them.
4. **Vendor docs used for the restore sections** (not content origins): Meta (Open Graph image size, already stated in SKILL.md), Material for MkDocs (admonitions, content tabs), Docusaurus (admonitions, tabs), MDN (details).

## Missing credit line

The skill README has no softaworks credit although sibling skills from the same fork carry one. Add to `skills/meme-factory/README.md` (below Resources), copied from the siblings (database-schema-designer, gemini, naming-analyzer):

`Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy.`

The memegen credit line stays as is.

## Proposed registry rows (one JSON object per line)

```json
{"skill": "meme-factory", "kind": "github-path", "source": "softaworks/agent-toolkit:skills/meme-factory", "ref": "main", "credit": "softaworks/agent-toolkit"}
{"skill": "meme-factory", "kind": "github-path", "source": "jacebrowning/memegen:README.md", "ref": "main", "credit": "Jace Browning"}
{"skill": "meme-factory", "kind": "unversioned", "source": "memegen.link OpenAPI (version 11.2): https://api.memegen.link/docs/openapi.json", "ref": null, "credit": "Jace Browning"}
{"skill": "meme-factory", "kind": "unversioned", "source": "Meta for Developers, Sharing image requirements: https://developers.facebook.com/docs/sharing/webmasters/images", "ref": null, "credit": "Meta"}
{"skill": "meme-factory", "kind": "unversioned", "source": "Material for MkDocs, Admonitions: https://squidfunk.github.io/mkdocs-material/reference/admonitions/", "ref": null, "credit": "Material for MkDocs"}
{"skill": "meme-factory", "kind": "unversioned", "source": "Material for MkDocs, Content tabs: https://squidfunk.github.io/mkdocs-material/reference/content-tabs/", "ref": null, "credit": "Material for MkDocs"}
{"skill": "meme-factory", "kind": "unversioned", "source": "Docusaurus, Admonitions: https://docusaurus.io/docs/markdown-features/admonitions", "ref": null, "credit": "Docusaurus"}
{"skill": "meme-factory", "kind": "unversioned", "source": "Docusaurus, Tabs: https://docusaurus.io/docs/markdown-features/tabs", "ref": null, "credit": "Docusaurus"}
{"skill": "meme-factory", "kind": "unversioned", "source": "MDN Web Docs, The Details disclosure element: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/details", "ref": null, "credit": "MDN Web Docs"}
```

Credit note for the restore: `check --strict` fails with `missing_credit` when a row's `credit` text is not found verbatim in SKILL.md, README.md or references/*.md. Each credit string above (softaworks/agent-toolkit, Jace Browning, Meta, Material for MkDocs, Docusaurus, MDN Web Docs) must therefore appear in the artifact's text: the README credit line covers the first two; the restored reference must name the other four where it cites them (the Meta line is already satisfiable by adding "Meta" to the Open Graph note). If the controller prefers fewer rows, the three vendor rows for MkDocs/Docusaurus/MDN can be dropped together with the platform-trick restore, but the Meta row backs a fact already in SKILL.md.

## skill-updater style review (review only)

Upstream change since the last review: none (blob ids identical, see Origin 1), so every upstream item is **ignore**. Review of the artifact against the memegen README and live service:

| item | decision | why |
| --- | --- | --- |
| `color=<name or hex>[,<name or hex>]` query parameter | adapt | documented in the memegen README Custom Colors, live 200; add one bullet to SKILL.md Query parameters (or the restored query reference) |
| overlay parameters `center` and `scale` for `style=<image URL>` | adapt | README Image Overlays; one line next to the `style` bullet |
| 415 on an unreachable or non-image `background` or `style` URL | adopt | probed live; step 6 lists 404 and 422 only |
| bare `-` and `_` both mean space | ignore | SKILL already tells readers to double literal ones; the helper escapes for them |
| emoji aliases such as `:thumbsup:` | ignore | the helper percent-encodes real emoji, which the service accepts |
| POST /images returns canonical URLs | ignore | not needed for URL building |
| /templates/{id} detail endpoint (lines, styles) | adopt | verified 200; belongs with the restored endpoints table (s045) |
| animated gif and webp rules | adopt | README Available Formats; restored under s038 |
| watermark removal parameter | ignore | does not exist on the public API (302 strips it) |

Model-validity pass: the rules that counter a model habit all still hold and stay: "never guess an ID from the meme's name" (the model's remembered long IDs such as two-buttons, surprised-pikachu, gru-plan all return 404 today), redact captions first, never say a deploy succeeded unconfirmed, fence greentext, and "never feed escaped text to the helper". None is stale.

Controller addition (batch 4 restore cited one more vendor page):

{"skill": "meme-factory", "kind": "unversioned", "source": "Python-Markdown, Markdown in HTML extension: https://python-markdown.github.io/extensions/md_in_html/", "ref": null, "credit": "Python-Markdown"}
