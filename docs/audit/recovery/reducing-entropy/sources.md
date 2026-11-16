# reducing-entropy sources (checked 2026-11-13)

## Origins found

1. **joshuadavidthomas/agent-skills, `reducing-entropy`** (MIT, license read through `gh api repos/joshuadavidthomas/agent-skills/license`). Already in the registry (`github-path`, ref `main`, credit `@joshuadavidthomas`) and already credited in `skills/reducing-entropy/README.md` (Attribution line, unchanged since 3027f20f). The upstream path has one commit, dd2ead06 (2026-02-18, "Move skills to repo root"), which predates the softaworks fork (2026-03-06) and the registry's `last_reviewed` (2026-11-04). The softaworks copy at 3027f20f (identical to our baseline dbff837f for every skill file) differs from upstream `main` in one line only: the frontmatter description (upstream "Use when evaluating designs, reviewing code, or refactoring ...", softaworks "Manual-only skill ... Only activate when explicitly requested by user ...").
2. **Simon Willison, "PAGNIs: Probably Are Gonna Need Its" (2021-07-01)**: origin of the PAGNI concept and of the items CI and automated deploys, API pagination, detailed API logs, mobile app kill switch, and of the override-YAGNI sentence. Cited in references/expensive-to-add-later.md External References; no registry row yet.
3. **Luke Plant, "YAGNI exceptions" (2021-06-29)**: origin of timestamps, logging, versioning, zero-one-many (the many-to-many item). Cited; no registry row.
4. **Jacob Kaplan-Moss, "Application Security PAGNIs" (2021-07-08)**: origin of the vulnerability disclosure policy and security@ address, audit trails, session or password invalidation, redacted data out of production. Cited; no registry row.
5. **Rich Hickey, "Simple Made Easy" and "The Value of Values"**: the simple-versus-easy and data-over-objects lenses paraphrase these talks. Cited in README and references; no registry row.
6. **Alan J. Perlis, "Epigrams in Programming" (ACM SIGPLAN, September 1982), epigram 9**: the "100 functions on one data structure" line in the old data-over-abstractions.md, given there with no attribution. No credit line and no row today.
7. Git project documentation: the step-2 counter relies on `git ls-files` flags and pathspec magic; no registry row today.

Other External References (Out of the Tar Pit, No Silver Bullet, Grug Brained Developer, Worse Is Better, Philosophy of Software Design, Zen of Python, Data-Oriented Design book, Mike Acton talk) are reading lists, not sources of stated content; no rows proposed.

Web search for uncredited distinctive phrases: only the Perlis line needed it (found, epigram 9). The old text's "Design is about taking things apart" is Hickey's phrase and is credited through the Simple Made Easy link.

## Proposed registry rows (docs/audit/upstream-sources.json)

The existing `github-path` row stays as it is. New rows (`last_reviewed` and `status` follow the neighboring `unversioned` rows):

```json
{"skill": "reducing-entropy", "kind": "unversioned", "source": "Simon Willison, PAGNIs: Probably Are Gonna Need Its: https://simonwillison.net/2021/Jul/1/pagnis/", "ref": null, "credit": "Simon Willison", "last_reviewed": "2026-11-13", "status": "current"}
{"skill": "reducing-entropy", "kind": "unversioned", "source": "Luke Plant, YAGNI exceptions: https://lukeplant.me.uk/blog/posts/yagni-exceptions/", "ref": null, "credit": "Luke Plant", "last_reviewed": "2026-11-13", "status": "current"}
{"skill": "reducing-entropy", "kind": "unversioned", "source": "Jacob Kaplan-Moss, Application Security PAGNIs: https://jacobian.org/2021/jul/8/appsec-pagnis/", "ref": null, "credit": "Jacob Kaplan-Moss", "last_reviewed": "2026-11-13", "status": "current"}
{"skill": "reducing-entropy", "kind": "unversioned", "source": "Alan J. Perlis, Epigrams in Programming (ACM SIGPLAN, September 1982): https://cs.yale.edu/homes/perlis-alan/quotes.html", "ref": null, "credit": "Alan Perlis", "last_reviewed": "2026-11-13", "status": "current"}
{"skill": "reducing-entropy", "kind": "unversioned", "source": "Rich Hickey, Simple Made Easy: https://www.infoq.com/presentations/Simple-Made-Easy/", "ref": null, "credit": "Rich Hickey", "last_reviewed": "2026-11-13", "status": "current"}
{"skill": "reducing-entropy", "kind": "unversioned", "source": "git-ls-files documentation: https://git-scm.com/docs/git-ls-files", "ref": null, "credit": "Git project", "last_reviewed": "2026-11-13", "status": "current"}
{"skill": "reducing-entropy", "kind": "unversioned", "source": "Git documentation, gitglossary (pathspec magic exclude and glob): https://git-scm.com/docs/gitglossary", "ref": null, "credit": "Git project", "last_reviewed": "2026-11-13", "status": "current"}
```

`audit.py check --strict` fails with `missing_credit` when a row's `credit` text is absent from SKILL.md, README.md or references/*.md. Today `Simon Willison`, `Luke Plant`, `Jacob Kaplan-Moss` and `Rich Hickey` are present; `Alan Perlis` and `Git project` are not, so the credit lines below must land in the same change as the rows.

## Missing credit lines (exact text to add)

- references/data-over-abstractions.md, External References (and beside the restored lead quote): `- [Epigrams in Programming, no. 9](https://cs.yale.edu/homes/perlis-alan/quotes.html) - Alan Perlis (ACM SIGPLAN, September 1982), source of the "100 functions on one data structure" line`
- skills/reducing-entropy/README.md, after the primary-sources list (same pattern as skills/lesson-learned/README.md line 50): `The git commands in the step-2 counter of SKILL.md follow the documentation of the Git project ([git-ls-files](https://git-scm.com/docs/git-ls-files), [gitglossary](https://git-scm.com/docs/gitglossary)), checked 2026-11-13.`
- references/expensive-to-add-later.md, on the override-YAGNI quote: attribute it to Simon Willison (his own sentence, not a quote from Luke Plant). Do not reword the existing External References credits.
- No change to the existing Attribution line (joshuadavidthomas, MIT). The softaworks hop is not credited per skill in the README or registry for this skill; the root README names the fork origin. Optional, not required: `via softaworks/agent-toolkit` in the registry credit would be a reword of an existing credit field and is not proposed.

## skill-updater style review (review only; no `track` call, `upstreams` not run for the whole registry)

Step 1: scope is skills/reducing-entropy, not synced. Step 2: one `github-path` row. Step 3: the equivalent read-only checks succeeded (commits and contents of `reducing-entropy` at `main` answered 200, no error). Step 4: path exists; upstream's only change since fork is older than `last_reviewed` (no `stale`). Compared every upstream file with the baseline.

| item | decision | reason |
| --- | --- | --- |
| Upstream description "Use when evaluating designs, reviewing code, or refactoring" | ignore | Contradicts the repo's manual-only rule; the current description is a deliberate, richer rewrite with explicit triggers and exclusions. |
| Upstream `adding-reference-mindsets.md` (still present upstream) | adapt | Restore its template (s026) and exclusion list (s029) in references/adding-reference-mindsets.md in the current decision-lens shape; skip the candidate table (s028, out of scope). |
| Upstream four references | adapt | Keep the current guarded versions; restore only the lead principle and questions of data-over-abstractions (s033, s036) and the missing PAGNI bullets (s048). |
| Upstream SKILL.md red flags and when-this-doesn't-apply | adapt | Restore in a new references file with the type-safety row rewritten so it cannot override the step-1 contract rule (s008, s009, s019, s021, s022). |
| Fact fix: Out of the Tar Pit URL (typo `MosesleyMarks06a`) in README.md and references/design-is-taking-apart.md; Mike Acton talk title in references/data-over-abstractions.md | adopt (fix) | Verified 2026-11-13 in facts.md; also present upstream, so the upstream copy has the same defect (could be reported upstream, not required). |
| Credit lines and registry rows above | adopt | Provenance for restored and existing content. |

Model-validity pass (step 6): not run. It needs the `pi-cmd` probe lane and the rails forbid dispatching an LLM lane from an analyst. Rules that counter a model habit and would be probed: the NEVER rules in Gotchas (empty caller search is not proof of dead code; no rename of names held by stored data) and the red flags restored under s008. The controller can run one probe per rule with `--model MODEL`.

## Official or primary pages used (each a proposed `unversioned` row above)

- https://git-scm.com/docs/gitglossary and https://git-scm.com/docs/git-ls-files (Git project): pathspec magic and ls-files flags.
- https://simonwillison.net/2021/Jul/1/pagnis/, https://lukeplant.me.uk/blog/posts/yagni-exceptions/, https://jacobian.org/2021/jul/8/appsec-pagnis/, https://cs.yale.edu/homes/perlis-alan/quotes.html: primary sources of the PAGNI items and the Perlis epigram.
