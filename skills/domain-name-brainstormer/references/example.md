# Worked example: a filled-in shortlist

Read this when the user asks for a sample, or when you are unsure how the grouped table, status labels and lookup details fit together. The names, statuses and times below are illustrative: no lookup produced them, so never copy a label, source or time into a real answer. In a real answer every label comes from a lookup you ran, or reads `unverified`.

**User**: "I'm building a tool for developers to share code snippets. Suggest creative domain names."

**Response** (shortened to six candidates; the default is 10):

Assumptions: English-speaking audience, short names (about 12 characters or fewer), no hyphens or digits, `.com` first plus `.dev` and `.app`. Say if any of that is wrong.

Cut during screening: `codeshare` (an established same-category brand sits nearby) and `sharecode` (heard aloud it can be spelled `sharecode` or `sharekode`, with no tie-breaker).

**Compound**

| Rank | Candidate | Pronunciation | Rationale | Spelling or confusion risk | TLD fit | Status | RDAP URL | Source and UTC time |
|---|---|---|---|---|---|---|---|---|
| 1 | snippetbox.com | SNIP-it-box | Says what the product does; easy to recall | Low; "snippit" is a plausible misspelling | `.com` is the default for a broad audience | `registered` | https://rdap.org/domain/snippetbox.com | `200` from rdap.verisign.com, 2026-11-07T10:02:11Z |
| 2 | devpaste.com | DEV-payst | Familiar from the pastebin habit; names the audience | Medium; "paste" and "past" sound alike | `.com` | `not found in registry` | https://rdap.org/domain/devpaste.com | `404` from rdap.verisign.com, 2026-11-07T10:02:14Z |

**Affix**

| Rank | Candidate | Pronunciation | Rationale | Spelling or confusion risk | TLD fit | Status | RDAP URL | Source and UTC time |
|---|---|---|---|---|---|---|---|---|
| 3 | clipwise.dev | KLIP-wize | Short, friendly, suggests clipping code and doing it well | Low | `.dev` signals a developer tool; HSTS-preloaded, so the site needs a TLS certificate before launch | `not found in registry` | https://rdap.org/domain/clipwise.dev | `404` from pubapi.registry.google, 2026-11-07T10:02:17Z |

**Coined blend**

| Rank | Candidate | Pronunciation | Rationale | Spelling or confusion risk | TLD fit | Status | RDAP URL | Source and UTC time |
|---|---|---|---|---|---|---|---|---|
| 4 | snipfold.app | SNIP-fold | Snip plus fold: a snippet kept folded away; distinctive | Low; both halves are common words with one obvious spelling | `.app` is HSTS-preloaded, so HTTPS only | `unverified` | https://rdap.org/domain/snipfold.app | not queried in this sample; run the RDAP check before offering it |
| 5 | snipfold.io | SNIP-fold | Same name on a second TLD | Low, as above | `.io` is common for developer tools | `unverified` | https://rdap.org/domain/snipfold.io | not queried in this sample; `.io` has no RDAP service on rdap.org (seen for another `.io` name, 2026-11-07), so use the WHOIS fallback |

**Evocative real word**

| Rank | Candidate | Pronunciation | Rationale | Spelling or confusion risk | TLD fit | Status | RDAP URL | Source and UTC time |
|---|---|---|---|---|---|---|---|---|
| 6 | quillbin.com | KWIL-bin | A quill and a bin: writing, then storing; memorable | Medium; "quill" is spelled unusually | `.com` | `unverified` | https://rdap.org/domain/quillbin.com | not checked |

Trade-off: `snippetbox.com` is the clearest name but is `registered`, so it is only a candidate if its holder is unrelated and willing to sell, which the skill cannot establish. `clipwise.dev` is the strongest name with no registry record found.

Next steps: no name above is confirmed as buyable. A registrar's checkout is the only place that confirms a name can be bought, at what first-year and renewal price, so check the top picks there; premium names can show a record-free result here and still carry a high price. Screen the finalists for trademarks in the relevant jurisdictions and product classes before spending money on the name.
