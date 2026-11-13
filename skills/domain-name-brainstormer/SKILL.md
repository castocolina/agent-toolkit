---
name: domain-name-brainstormer
description: Brainstorm, screen and rank brandable domain names (.com, .io, .app, .dev and other TLDs) for apps, products, companies and personal brands, and report registration status honestly via RDAP/WHOIS lookups. Use when naming a project, launching or rebranding, asking "is this domain available", or replacing a taken first choice, even if the user only describes the business. Not for DNS, email, hosting or transfers on a domain already owned, naming without domains, social handles, or legal trademark clearance.
---

# Domain Name Brainstormer

A shortlist is worth only as much as its status claims. Ideation is cheap; the skill's value is screening names hard and never presenting a guess as a lookup.

## Defaults

When the user does not say otherwise, assume: English-speaking audience, 10 candidates, short (about 12 characters or fewer before the TLD), no hyphens or digits, `.com` first plus two TLDs that fit the product. State these assumptions in one line and proceed. A number, length, character rule or TLD the user states replaces the default it touches; only the unstated defaults apply. Ask first only when the answer would change the shortlist: a non-English target language, a hard budget, or a word that must appear or must not.

## Procedure

1. **Apply hard constraints first.** Target languages, forbidden meanings, required TLDs and a budget cap (checked in step 6) are filters, not ranking weights. A name that fails one is cut, however good it sounds. A budget cap cuts a name only when the user supplied a registrar checkout quote; otherwise step 6's `unverified` budget-fit label is the only outcome.
2. **Generate and screen in one pass.** Spread candidates across distinct naming directions (compound, affix, evocative real word, coined blend); spelling variants of one idea count as one candidate. Cut any candidate that has more than one plausible spelling when heard (two equally likely spellings and no tie-breaker; keep a name whose intended spelling is the common one and record the rival spelling in the spelling-or-confusion-risk column, as `references/example.md` does), an unwanted meaning or sound in any target language, or an established same-category brand nearby. Read the joined form for unintended word splits too: `therapistfinder` reads "the rapist finder".
3. **Rank the survivors** by the user's stated priorities; default order is spelling reliability, then memorability, then descriptiveness, then TLD fit. When the top pick wins one axis and loses another (for example memorable but needs a premium `.com`), say the trade-off in one line.
4. **When the first choice is taken**, keep the name on another TLD only if people will find it through search or links, can remember the full address, and the `.com` holder is unrelated; say that some traffic and email typed to `.com` will reach the holder. Pick a new name if users habitually type `.com`, or the `.com` holder is a competitor or would confuse people.
5. **Report status from a lookup or not at all.** Use exactly these labels:
   - `unverified`: no lookup ran, or it failed or was inconclusive. This is the default.
   - `registered`: the registry's RDAP server returned 200 or WHOIS returned a record with a creation date, whatever its status (`pending delete` and `redemption period` are still registered).
   - `not found in registry`: the registry's own RDAP server returned 404, or its WHOIS gave an explicit no-record reply (`.de` says `Status: free`, others `No match`, `NOT FOUND` or `Domain not found.`). This is still not "available": see Gotchas.

   With a shell, run `curl -sS -L --connect-timeout 5 --max-time 20 -o rdap.json -w '%{http_code} %{url_effective}' https://rdap.org/domain/<name>` and classify by the printed status and final host. Classify even when curl exits non-zero: Verisign closes the connection on a 404 and curl prints error 56 after `404 https://rdap.verisign.com/...` (observed against rdap.verisign.com, checked 2026-11-07). Whatever curl's exit code, the printed `%{http_code} %{url_effective}` decides.

   | Printed result | Label |
   |---|---|
   | `200` on a registry host (for example `rdap.verisign.com`, `pubapi.registry.google`) | `registered` |
   | `404` on a registry host | `not found in registry` |
   | `404` still on `rdap.org` ("No RDAP service is available for this resource") | no RDAP for this TLD; use WHOIS |
   | `429`, `5xx`, `000` (no connection) or a timeout | `unverified`; stop querying, no retry |

   WHOIS fallback for a TLD without RDAP (`.io`, `.co`, `.de`, `.es`, `.mx` had none in IANA's bootstrap file `https://data.iana.org/rdap/dns.json` in October 2026): `timeout 20 whois -h whois.iana.org <tld>` names the registry server in its `whois:` line, then `timeout 20 whois -h <server> <name>`. When the IANA reply has no `whois:` line (it may give only a `remarks:` registration URL; every TLD tried on 2026-11-07, including `.io`, had a `whois:` line, so the case is rare), label the name `unverified`, quote the remark or URL it gave, and point the user at a registrar search; never guess a WHOIS host. Any other WHOIS reply, including restricted-access or rate-limit text, is `unverified`. If `whois` is not installed, the fetch tool hides redirects or the status code, or a server throttles you, label the name `unverified` and point to a registrar search; never retry in a loop. For each checked name record the source (final URL or WHOIS server), the UTC check time and the raw result. Without network tools, say no lookup was done, label every candidate `unverified`.
6. **Check the budget only against confirmed terms.** When the user has a budget cap and a registrar checkout or quote they supply gives first-year and renewal prices, cut candidates over the cap. Otherwise mark each candidate's budget fit `unverified` and ask for the registrar checkout price, first year and renewal, before calling it within budget.
7. **Keep legal risk separate.** Recommend trademark screening in the relevant jurisdictions and product classes before money is spent on the name. Registering a domain grants no trademark right. Under ICANN's UDRP, the holder of a mark can have a domain cancelled or transferred if it is confusingly similar to the mark, the registrant has no legitimate interest in it, and it was registered and is used in bad faith. Never call a near-match to another company's mark safe.

## Gotchas

- NEVER write "available" for a domain. A registry "not found" is not a purchase offer: reserved, blocked and premium names can return it too, and only a registrar's checkout confirms that a name can be bought and at what price.
- NEVER quote a price or estimate a taken domain's value. Premium pricing is set per name by the registry, can apply to every renewal and not just the first year, and appears only at the registrar's checkout.
- Reject confusable characters outright: IDN homographs (Cyrillic `U+0430` drawn like Latin `a`) and look-alike swaps (`0`/`O`, `1`/`l`, `rn`/`m`). They make the name easy to impersonate, and browsers may show a mixed-script IDN as punycode (`xn--...`). If the user explicitly wants an IDN, check it against the Unicode confusables data (UTS #39) before shortlisting.
- `.app`, `.dev` and `.page` are HSTS-preloaded TLD-wide in Chrome's list, which Firefox, Safari and Edge build on: no page on them loads over plain HTTP. Say so when suggesting them, because the site needs a TLS certificate before launch.

## Output

Group candidates by naming direction, then give a ranked table: candidate, intended pronunciation, rationale, spelling or confusion risk, TLD fit, status label, and the full `https://rdap.org/domain/<name>` URL in every row whether or not it was checked. Add source and UTC time for every checked name, and a budget-fit column when the user gave a cap. End by noting that price and renewal terms must be confirmed at a registrar. Read `references/example.md` for a filled-in shortlist (illustrative statuses, not live lookups) when the user asks for a sample or you are unsure of the layout.

## Credits

**Inspired by:** Ben Aiad's use case from Lenny's Newsletter
