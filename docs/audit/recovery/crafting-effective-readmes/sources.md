# crafting-effective-readmes: sources (checked 2026-11-15)

## Origins found

1. **Original skill: joshuadavidthomas/agent-skills, `crafting-effective-readmes/` (MIT).** Credited in `skills/crafting-effective-readmes/README.md` ("Original skill by @joshuadavidthomas ... (MIT)"). The baseline `dbff837f:skills/crafting-effective-readmes/` is byte-identical to the softaworks import at `3027f20f` (`git diff --stat 3027f20f dbff837f -- skills/crafting-effective-readmes` is empty) and to upstream today apart from one line: upstream still has `SKILL.md` (Overview, Process Steps 1-3, Project Types table, References), `section-checklist.md`, `style-guide.md`, `using-references.md`, `templates/{oss,personal,internal,xdg-config}.md` and `references/` (the path resolves: `gh api repos/joshuadavidthomas/agent-skills/git/trees/main?recursive=1` lists all of them). Upstream history for the path: `dd2ead06` (2026-02-18, move to repo root) and `516dee7a` (2026-07-20, "consolidate writing skills": only `style-guide.md`, the pointer now reads "Orwell's and Strunk's rules ... use the `writing` skill"). Registry row exists (`github-path`, `main`) and `upstreams` reports `error: null`, `stale: false`, `source_updated` 2026-07-20; `stale: false` is a timestamp signal only, so the review below read the content.
2. **Intermediary: softaworks/agent-toolkit, `skills/crafting-effective-readmes`.** Same files as the baseline; its commit `efbd228d` (2026-01-26, "Add attribution for @joshuadavidthomas skills") is where the credit line comes from. No registry row and no credit line for the intermediary on this skill (the root README credits the fork at repo level).
3. **`references/art-of-readme.md`: hackergrrl/art-of-readme (Creative Commons Attribution License 2.0).** Registry row `github`, `hackergrrl/art-of-readme`, `master`, status `unreachable`. See the stale-row finding below.
4. **`references/standard-readme-spec.md` and the two example files: RichardLitt/standard-readme (MIT).** Registry row `github`, `main` exists. The vendored examples are byte-identical to upstream `example-readmes/`; the vendored spec lacks one upstream line (facts.md, "Standard Readme spec text is current").
5. **`references/make-a-readme.md`: Danny Guo, makeareadme.com.** Registry row `unversioned` exists; the live page still contains the text (facts.md).
6. **Our own rewrites:** `de35b734` (2026-10-29, moved the checklist, style guide and using-references into `references/`, shrank SKILL.md) and `46b06765` (2026-11-06, judged fixes: new SKILL.md, deleted `templates/`, `style-guide.md` and `using-references.md`, no record row). The record rows s007, s024 and the template rows explain the template deletion.

Credit status: every origin that is in the artifact has a credit line in `skills/crafting-effective-readmes/README.md` (Attribution) and a registry row. Only the softaworks intermediary is uncredited on the skill.

### Credit line to add (optional, softaworks intermediary; never reword the existing four lines, add this as a fifth bullet under Attribution)

```text
- Imported through [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) (`skills/crafting-effective-readmes`)
```

## Stale registry row: hackergrrl/art-of-readme

`gh api repos/hackergrrl/art-of-readme` answers `Not Found (HTTP 404)` (checked 2026-11-15; `audit.py upstreams` reports the same error). Findings:

- Not moved or renamed. `https://github.com/hackergrrl`, `https://raw.githubusercontent.com/hackergrrl/art-of-readme/master/README.md` and `https://api.github.com/repos/hackergrrl/art-of-readme` all answer 404. The Wayback Machine holds the repository page (snapshot 2026-06-15) and the owner's profile (snapshot 2026-09-05, "hackergrrl (Kira)", GitHub user id 489362), so the account existed in September 2026. `gh api user/489362` now answers 404: the account id itself is gone (deleted or removed), so there is no new owner name for GitHub to redirect to. A rename would have kept the id.
- `noffle/art-of-readme` was tried as a possible new home (the project is widely associated with the handle `noffle`; that link is from memory, not verified): it is 404, and the `noffle` account exists but `gh api users/noffle/repos` lists no repository. GitHub repository search and web search find only unrelated copies: `bradparks/art-of-readme` (a one-file README.md copy from 2016, no license metadata), `cochimu/art-of-readme`, `Stella418/art-of-readme-` and `crazyorr/art-of-readme` (404). None is the author's project, so none is a credible replacement source; a search-result snippet claiming the repository was archived by its owner in August 2022 is unverified.
- The text in `references/art-of-readme.md` is licensed CC BY 2.0 (confirmed in the archived copy), so keeping it is allowed; the credit line in README.md stays exactly as it is.
- Only the archived copy remains as a verifiable origin. Proposed corrected row (replaces the `github` row; a `github` row can never resolve again and keeps `upstreams` failing):

```json
{"skill": "crafting-effective-readmes", "kind": "unversioned", "source": "hackergrrl (Kira), The Art of README, repository removed from GitHub in 2026, last archived copy 2026-06-15: https://web.archive.org/web/20260615180708/https://github.com/hackergrrl/art-of-readme", "ref": null, "credit": "hackergrrl/art-of-readme"}
```

Proposed line for `docs/audit/upstream-findings.md` (not edited by this analyst):

```text
- `crafting-effective-readmes`: registry row `hackergrrl/art-of-readme` (kind `github`, ref `master`) answers `gh: Not Found (HTTP 404)` since 2026-11-06 and is not a rename: the owner account (user id 489362, "hackergrrl (Kira)") is gone (`gh api user/489362` 404; no `noffle/art-of-readme`), the last archived copy is the Wayback snapshot 2026-06-15; the vendored `references/art-of-readme.md` (CC BY 2.0, credit kept) has no live source to compare against; propose replacing the row with an `unversioned` row pointing at the snapshot (checked 2026-11-15).
```

## Proposed registry rows (docs/audit/upstream-sources.json, by hand; `validate_entry` rules checked: kebab-case skill, `github-path` source `owner/repo:path`, non-empty credit, `unversioned` has `ref` null and a non-empty title and URL)

New origin row (softaworks intermediary):

```json
{"skill": "crafting-effective-readmes", "kind": "github-path", "source": "softaworks/agent-toolkit:skills/crafting-effective-readmes", "ref": "main", "credit": "softaworks"}
```

Replacement row for hackergrrl: see above. One `unversioned` row per official page used in facts.md (credit = the vendor; `known limit`: `upstreams` never reports an `unversioned` row stale, so a changed page is noticed only when `skill-updater` runs on the artifact):

```json
{"skill": "crafting-effective-readmes", "kind": "unversioned", "source": "GitHub Docs, Basic writing and formatting syntax: https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax", "ref": null, "credit": "GitHub"}
{"skill": "crafting-effective-readmes", "kind": "unversioned", "source": "GitHub Docs, Adding a workflow status badge: https://docs.github.com/en/actions/how-tos/monitor-workflows/add-a-status-badge", "ref": null, "credit": "GitHub"}
{"skill": "crafting-effective-readmes", "kind": "unversioned", "source": "GitLab Docs, GitLab Flavored Markdown (heading anchors): https://docs.gitlab.com/user/markdown/#heading-anchors", "ref": null, "credit": "GitLab"}
{"skill": "crafting-effective-readmes", "kind": "unversioned", "source": "npm Docs, package.json: https://docs.npmjs.com/cli/v11/configuring-npm/package-json", "ref": null, "credit": "npm"}
{"skill": "crafting-effective-readmes", "kind": "unversioned", "source": "npm Docs, config: https://docs.npmjs.com/cli/v11/using-npm/config", "ref": null, "credit": "npm"}
{"skill": "crafting-effective-readmes", "kind": "unversioned", "source": "npm Docs, npm view: https://docs.npmjs.com/cli/v11/commands/npm-view", "ref": null, "credit": "npm"}
{"skill": "crafting-effective-readmes", "kind": "unversioned", "source": "pnpm Docs, pnpm-workspace.yaml: https://pnpm.io/pnpm-workspace_yaml", "ref": null, "credit": "pnpm"}
{"skill": "crafting-effective-readmes", "kind": "unversioned", "source": "Python Packaging User Guide, pyproject.toml specification: https://packaging.python.org/en/latest/specifications/pyproject-toml/", "ref": null, "credit": "Python Packaging Authority"}
{"skill": "crafting-effective-readmes", "kind": "unversioned", "source": "Python Packaging User Guide, Core metadata specifications: https://packaging.python.org/en/latest/specifications/core-metadata/", "ref": null, "credit": "Python Packaging Authority"}
{"skill": "crafting-effective-readmes", "kind": "unversioned", "source": "PyPI, Classifiers: https://pypi.org/classifiers/", "ref": null, "credit": "Python Software Foundation"}
{"skill": "crafting-effective-readmes", "kind": "unversioned", "source": "PyPI Docs, Project descriptions: https://docs.pypi.org/project-management/project-descriptions/", "ref": null, "credit": "Python Software Foundation"}
{"skill": "crafting-effective-readmes", "kind": "unversioned", "source": "pip documentation, pip index: https://pip.pypa.io/en/stable/cli/pip_index/", "ref": null, "credit": "Python Packaging Authority"}
{"skill": "crafting-effective-readmes", "kind": "unversioned", "source": "setuptools documentation, Keywords: https://setuptools.pypa.io/en/latest/references/keywords.html", "ref": null, "credit": "Python Packaging Authority"}
{"skill": "crafting-effective-readmes", "kind": "unversioned", "source": "The Cargo Book, The Manifest Format: https://doc.rust-lang.org/cargo/reference/manifest.html", "ref": null, "credit": "The Rust Project"}
{"skill": "crafting-effective-readmes", "kind": "unversioned", "source": "The Cargo Book, Configuration: https://doc.rust-lang.org/cargo/reference/config.html", "ref": null, "credit": "The Rust Project"}
{"skill": "crafting-effective-readmes", "kind": "unversioned", "source": "The Cargo Book, cargo search: https://doc.rust-lang.org/cargo/commands/cargo-search.html", "ref": null, "credit": "The Rust Project"}
{"skill": "crafting-effective-readmes", "kind": "unversioned", "source": "Go Modules Reference: https://go.dev/ref/mod", "ref": null, "credit": "The Go Authors"}
{"skill": "crafting-effective-readmes", "kind": "unversioned", "source": "SPDX License List: https://spdx.org/licenses/", "ref": null, "credit": "SPDX"}
{"skill": "crafting-effective-readmes", "kind": "unversioned", "source": "Node.js, Previous releases: https://nodejs.org/en/about/previous-releases", "ref": null, "credit": "OpenJS Foundation"}
{"skill": "crafting-effective-readmes", "kind": "unversioned", "source": "Shields.io, GitHub Actions Workflow Status: https://shields.io/badges/git-hub-actions-workflow-status", "ref": null, "credit": "Shields.io"}
{"skill": "crafting-effective-readmes", "kind": "unversioned", "source": "Shields.io, npm Version: https://shields.io/badges/npm-version", "ref": null, "credit": "Shields.io"}
{"skill": "crafting-effective-readmes", "kind": "unversioned", "source": "Shields.io, Static Badge: https://shields.io/badges/static-badge", "ref": null, "credit": "Shields.io"}
{"skill": "crafting-effective-readmes", "kind": "unversioned", "source": "All Contributors, Bot installation: https://allcontributors.org/docs/en/bot/installation", "ref": null, "credit": "All Contributors"}
{"skill": "crafting-effective-readmes", "kind": "unversioned", "source": "usethis, use_readme_rmd(): https://usethis.r-lib.org/reference/use_readme_rmd.html", "ref": null, "credit": "Posit"}
{"skill": "crafting-effective-readmes", "kind": "github", "source": "thlorenz/doctoc", "ref": "master", "credit": "Thorsten Lorenz"}
{"skill": "crafting-effective-readmes", "kind": "github", "source": "terraform-docs/terraform-docs", "ref": "master", "credit": "terraform-docs"}
{"skill": "crafting-effective-readmes", "kind": "github", "source": "jonschlinkert/markdown-toc", "ref": "master", "credit": "Jon Schlinkert"}
{"skill": "crafting-effective-readmes", "kind": "github", "source": "orium/cargo-rdme", "ref": "main", "credit": "Diogo Sousa"}
{"skill": "crafting-effective-readmes", "kind": "github", "source": "webern/cargo-readme", "ref": "master", "credit": "cargo-readme contributors"}
```

Notes on the last five (tool repositories read only for one marker each): they are cheap `github` rows only if the coordinator wants drift tracking on the markers; if not, drop them and keep the marker facts as `pointer` rows (the markers are the tools' own documented output, so a repository README is the tool's output source). Branch names were not verified with `gh api` beyond the raw README fetch that succeeded on that branch; verify before adding. The two Standard Readme and Make a README rows already exist.

## skill-updater style review (REVIEW ONLY; no `track` call, no edit)

Method: `audit.py upstreams --registry docs/audit/upstream-sources.json` read-only (this artifact's rows: joshuadavidthomas `stale: false`, `error: null`; hackergrrl `error: Not Found (HTTP 404)`; RichardLitt `stale: false`; Danny Guo unversioned), then step 4 (contents test passes for the joshuadavidthomas path, content read against the artifact) and step 5 (hackergrrl is a repo-level 404, so no tree search applies; the account is gone, see above). Step 6, the model-validity probe, was not run (rail 4 bars an LLM lane for this analyst and no `pi` runner was started; the coordinator may run it). Rules that counter a model habit: "Missing facts become visible placeholders (`<install command: not found in repo>`), never plausible inventions", "Run the documented first-use path verbatim in a clean environment" and "Report each claim as `executed`, `static`, or `unverified`"; keep all three, no removal is proposed. No `track` call is proposed for the hackergrrl row (it cannot resolve); record the row change by hand first.

Adopt / adapt / ignore for the restore brief:

| source change | decision | reason |
| --- | --- | --- |
| upstream `templates/{oss,personal,internal,xdg-config}.md` (unchanged since the baseline) as the source of the template restore (record rows s007, s024, s107, s110, s113, s114, s126, s127, s130, para:dbd0d31e, para:2384846c, para:95864c62, para:be2294d5, s002) | adapt | restore into `references/templates/` (or one `references/templates.md`) in the current style: visible placeholders, load trigger in SKILL.md References at "creating or restructuring a README" (the checklist stays the router). Differences to keep, named: no unconditional "Contributions are welcome!" (conditional on repository evidence, SKILL.md Workflow 2); badge lines use the checked routes in facts.md and carry a note that each badge needs its workflow file or published package (Gotchas: badges are claims); no badge lines in the Internal template (Gotchas: external badges break for that audience); the runtime-requirement example must not pin a Node version (facts.md pointer); the license line takes the SPDX id from LICENSE, not a hard-coded `MIT`. Only fragments the record marks restore come back: leave out the sections the record marks not-lost or drop (documentation placeholder s116). |
| upstream Process Steps 1-3 (interview, "Always Ask") | ignore | superseded by the evidence-first workflow (record rows s006, s021, s022, s023); an unconditional question blocks unattended runs. |
| upstream "Update 'Last reviewed' date if present" (Step 2, Reviewing) | adapt (A1) | one line in `references/section-checklist.md` Config note: when reviewing a README that has `> Last reviewed:`, update the date after the check; model omits it unprompted. It is the one residual item of record row s022. |
| upstream `516dee7a`: style-guide pointer now names a `writing` skill with Orwell's rules | ignore | this repo's skill is `writing-clearly-and-concisely`, already pointed to by SKILL.md; no style-guide file exists. |
| upstream `dd2ead06`: skills moved to repo root | ignore | path move only; the registry path already follows it. |
| RichardLitt/standard-readme `c57b4b29` (2026-06-17): Badges line "For static badges, consider using a locally hosted image to avoid external requests, which can result in tracking, and to avoid unnecessary resource usage." | adopt | add the line to `references/standard-readme-spec.md` at the same place (Badges, after the shields/badge guidance), as upstream wrote it; the vendored file otherwise matches. After the edit, record `track` for the standard-readme row with `--sha 5d18ad4d` (newest commit read). |
| RichardLitt/standard-readme `5d18ad4d` / `fd4528da` (2026-09-29): npm funding field replaces postinstall | ignore | package metadata of the upstream repo, not part of the spec text. |
| `hackergrrl/art-of-readme` | ignore (no change readable) | repository gone; keep the vendored file and the credit line; the row is changed by hand as proposed above. |
| makeareadme.com | ignore | live page unchanged from the vendored text (facts.md). |

## Other findings for the restore dispatch (outside the record rows)

- `SKILL.md` Gotchas, anchor slugs: correct the GitLab sentence (facts.md, first corrected row). Suggested wording: "GitHub and GitLab 17.0 and later lowercase, drop punctuation except `-` and `_`, keep repeated hyphens, and suffix duplicate headings `-1`, `-2`; a link to `## A & B` is `#a--b` on both; older self-managed GitLab collapses repeated hyphens, so check the host's version." The trailing "so check links for the host the README is read on" stays.
- `README.md`: the Directory Structure block must list the restored template file(s) and the What It Does list advertises the templates again (record rows s002, s007, s016).
- Evals (may be edited openly): add one scenario for an Internal README (asserts Team and On-call header, Symptom/Cause/Fix, environments table, no external badges) and one for a Config README with the restored Why This Setup and Dependencies sections (the current `internal-config-readme` eval asserts only what's here, how to extend and gotchas), and one for the corrected GitLab anchor fact (a scenario that would have failed on the stale "collapses repeated hyphens" text: a TOC link for `## A & B` on GitLab 17 is `#a--b`).
- `.claude-plugin/marketplace.json` description for the plugin and `dist/plugins/crafting-effective-readmes/` need no change from these findings; run `python3 scripts/build_plugins.py` after the restore so `dist/` matches.
- Root `README.md` row for the skill ("Write effective README files") is unchanged by these findings.
