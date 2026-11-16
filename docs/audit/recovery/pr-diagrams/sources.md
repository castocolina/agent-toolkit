# pr-diagrams: sources, credits and skill-updater review (2026-11-15)

Mode FACTS-ONLY: only the sources, registry and facts steps were done. No registry row, README or artifact file was edited. Facts are in `facts.md`; fixes for the update brief are in `update-brief.md`; the proposed rows below are also stored as valid JSON in `proposed-rows.json` (checked with `audit.validate_entry`, 15 of 15 valid).

## Origin

- `skills/pr-diagrams` did not exist in the softaworks fork baseline (`git ls-tree -r 3027f20f -- skills/pr-diagrams` is empty). It was written in this repository (commits 56d1a416, abd88c02, 527b3ea6), so the script, tests, evals and SKILL.md are original work with no upstream.
- The only inherited content is the PR body template in `references/pr-body.md` ("Body templates": `# PR Summary: $title`, the three emoji headings, the `sequenceDiagram` example, the changeset block and the `[TRIAGE]` line). It comes from softaworks `commands/explain-pr-changes.md` (section 5, "The Output Template"), which `git -C WT show 3027f20f:commands/explain-pr-changes.md` shows with the same headings and example. The command itself is registered with credit `Leonardo Flores (@leonardocouy), via softaworks/agent-toolkit`; no web search was needed because the origin is a file in this very fork.
- `render` depends on `skills/draw-io` (`convert-drawio-to-png.sh`), which keeps its own rows and credits; pr-diagrams only calls it.
- Registry state today: `grep '"skill": "pr-diagrams"' docs/audit/upstream-sources.json` finds no row. `audit.py check --strict --skills pr-diagrams` passes (no row, so nothing to credit-check).

## Missing credit line

No file of the skill names softaworks, Leonardo Flores or the GitHub, Git, W3C or draw.io documentation it relies on. Proposed line for `skills/pr-diagrams/README.md` (the skill-level credit check searches SKILL.md, README.md and references/*.md for the exact `credit` text), to add under the Tests section:

```markdown
## Credits

The PR body templates in `references/pr-body.md` are adapted from the [`explain-pr-changes` command](https://github.com/softaworks/agent-toolkit/blob/main/commands/explain-pr-changes.md) of softaworks/agent-toolkit by Leonardo Flores (@leonardocouy), via softaworks/agent-toolkit. Its `gh` facts follow the GitHub CLI manual and the GitHub Docs (GitHub), its `git` facts follow the Git documentation (Git project), its `drawio` flags follow the draw.io CLI and the drawio-mcp skill (draw.io (JGraph)), and its PNG signature follows the PNG specification (W3C).
```

The root README credit sentence (not edited here) can reuse the same wording; the command's existing sentence already credits `explain-pr-changes`.

## Proposed registry rows (verbatim; also in proposed-rows.json)

```json
[
  {"skill": "pr-diagrams", "kind": "github-path", "source": "softaworks/agent-toolkit:commands/explain-pr-changes.md", "ref": "main", "credit": "Leonardo Flores (@leonardocouy), via softaworks/agent-toolkit"},
  {"skill": "pr-diagrams", "kind": "unversioned", "source": "GitHub CLI manual, gh pr create (--attach, --head, partial attach failure): https://cli.github.com/manual/gh_pr_create", "ref": null, "credit": "GitHub"},
  {"skill": "pr-diagrams", "kind": "unversioned", "source": "GitHub CLI manual, gh pr edit (--attach, --body-file, --add-reviewer): https://cli.github.com/manual/gh_pr_edit", "ref": null, "credit": "GitHub"},
  {"skill": "pr-diagrams", "kind": "unversioned", "source": "GitHub CLI manual, gh api (--paginate, --jq): https://cli.github.com/manual/gh_api", "ref": null, "credit": "GitHub"},
  {"skill": "pr-diagrams", "kind": "unversioned", "source": "GitHub CLI release v2.99.0, attach images and videos to issues and pull requests (first --attach release): https://github.com/cli/cli/releases/tag/v2.99.0", "ref": null, "credit": "GitHub"},
  {"skill": "pr-diagrams", "kind": "unversioned", "source": "GitHub changelog 2026-09-01, GitHub CLI media in issues, pull requests and comments (hosts, tokens, file types and size limits): https://github.blog/changelog/2026-09-01-github-cli-media-in-issues-pull-requests-and-comments/", "ref": null, "credit": "GitHub"},
  {"skill": "pr-diagrams", "kind": "unversioned", "source": "GitHub REST API, list pull requests associated with a commit: https://docs.github.com/en/rest/commits/commits#list-pull-requests-associated-with-a-commit", "ref": null, "credit": "GitHub"},
  {"skill": "pr-diagrams", "kind": "unversioned", "source": "GitHub REST API, pull request reviews (list reviews for a pull request): https://docs.github.com/en/rest/pulls/reviews", "ref": null, "credit": "GitHub"},
  {"skill": "pr-diagrams", "kind": "unversioned", "source": "GitHub REST API, review requests (get all requested reviewers for a pull request): https://docs.github.com/en/rest/pulls/review-requests", "ref": null, "credit": "GitHub"},
  {"skill": "pr-diagrams", "kind": "unversioned", "source": "GitHub REST API, rate limits (403 and 429, Retry-After): https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api", "ref": null, "credit": "GitHub"},
  {"skill": "pr-diagrams", "kind": "unversioned", "source": "GitHub Docs, Basic writing and formatting syntax (images, relative image paths, ?raw=true and private repositories): https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax", "ref": null, "credit": "GitHub"},
  {"skill": "pr-diagrams", "kind": "unversioned", "source": "GitHub Docs, Creating diagrams (Mermaid in pull requests): https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams", "ref": null, "credit": "GitHub"},
  {"skill": "pr-diagrams", "kind": "unversioned", "source": "draw.io CLI export (-x -f png -e --embed-diagram, --disable-update), drawio --help and the drawio-mcp Claude Code skill: https://github.com/jgraph/drawio-mcp/blob/main/plugins/claude-code/skills/drawio/SKILL.md", "ref": null, "credit": "draw.io (JGraph)"},
  {"skill": "pr-diagrams", "kind": "unversioned", "source": "W3C Portable Network Graphics specification, section 5.2 PNG signature: https://www.w3.org/TR/png/", "ref": null, "credit": "W3C"},
  {"skill": "pr-diagrams", "kind": "unversioned", "source": "Git documentation, git-ls-remote (--heads deprecated, --branches): https://git-scm.com/docs/git-ls-remote", "ref": null, "credit": "Git project"}
]
```

Credit strings that must appear verbatim in the skill's SKILL.md, README.md or references (`audit.py check --strict` reports `missing_credit` otherwise): `Leonardo Flores (@leonardocouy), via softaworks/agent-toolkit`, `GitHub`, `Git project`, `draw.io (JGraph)`, `W3C`. The credits line above contains all five. The 65,536-character PR body limit has no official page, so it gets no row (see facts.md); `drawio --help` and `gh ... --help` are tool output, not pages.

## Skill-updater style review (REVIEW ONLY: no `track` call, no registry edit)

Steps taken from `skills/skill-updater/SKILL.md`: step 2 (no row for the skill, a derived template with no credit line: propose the row and the credit, give no `track` call), then `audit.py upstreams` read-only.

- `audit.py upstreams` (exit 1 because other rows fail, as the skill warns) reports the existing `explain-pr-changes` row `softaworks/agent-toolkit:commands/explain-pr-changes.md` as `stale: false`, `error: null`, `source_updated 2026-01-18T22:41:59Z`. `gh api 'repos/softaworks/agent-toolkit/commits?path=commands/explain-pr-changes.md&sha=main'` lists exactly one commit (673fe769, 2026-01-18), older than the fork baseline 3027f20f (2026-03-05). Nothing changed upstream since the template was taken: no adopt, adapt or ignore decision on upstream text is pending.
- Model review (skill-updater step 7, no rule changes): the body template and the script contain no model-behavior rules, so there is nothing to retire.

Adopt, adapt or ignore list for the update brief:

| item | decision | reason |
| --- | --- | --- |
| Upstream `# PR Summary` template, headings, `[TRIAGE]` line | adapt (already adapted) | kept in `references/pr-body.md`, with the `--attach` image line added and `--attach` wording in the comments |
| Upstream persona "Code-Sage", branch creation rule, "Close $ARGUMENTS", `gh` create/update prose | ignore | belongs to the `explain-pr-changes` command, not to this skill |
| GitHub CLI release v2.99.0 as the origin of `--attach` | adopt | replaces the 2.101 claim (facts.md rows 2 and 3) |
| gh 2.103.0 body-directory resolution, gh 2.102 and 2.103.2 token changes | adapt | do not pin; add the "absolute path" advice and point to `gh pr create --help` |
| GitHub changelog 2026-09-01 limits (10 MB images, token types, hosts) | adapt | pointer in Failures to the live stderr and the changelog; no numbers written into the skill |
| git 2.46 deprecation of `ls-remote --heads` | adopt | pass full ref patterns without the flag |

## Official pages used (each is a proposed `unversioned` row above)

- https://cli.github.com/manual/gh_pr_create, https://cli.github.com/manual/gh_pr_edit, https://cli.github.com/manual/gh_api
- https://github.com/cli/cli/releases/tag/v2.99.0 (and v2.100.0, v2.101.0, v2.102.0, v2.103.0, v2.103.2 notes, read through `gh api repos/cli/cli/releases/tags/<tag>`)
- https://github.blog/changelog/2026-09-01-github-cli-media-in-issues-pull-requests-and-comments/
- https://docs.github.com/en/rest/commits/commits, https://docs.github.com/en/rest/pulls/reviews, https://docs.github.com/en/rest/pulls/review-requests, https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api
- https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax, https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams
- https://www.w3.org/TR/png/, https://git-scm.com/docs/git-ls-remote, https://github.com/git/git/blob/master/Documentation/RelNotes/2.46.0.adoc (release note, same row as git-ls-remote)
- https://docs.github.com/en/rest/pulls/pulls#create-a-pull-request was read for the 65,536 limit and states none; it is not a source for any written value, so no row.

## Not done

- No live test of the PR body limit (it needs a PR write).
- The root README credit sentence for pr-diagrams was not drafted beyond reuse of the line above (README.md is out of scope).
