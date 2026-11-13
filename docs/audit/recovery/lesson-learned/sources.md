# lesson-learned sources

Checked 2026-11-07.

## Origin

- The skill came from softaworks/agent-toolkit, added by PR #11 "feat: add lesson-learned skill" (GitHub login `mattwhite8`, commit author Matt White, 0c042f22, merged 2026-02-08). Our fork point `3027f20f` and the baseline `dbff837f` hold the same files; `git diff 3027f20f dbff837f -- skills/lesson-learned` is empty.
- Upstream is unchanged since: `gh api 'repos/softaworks/agent-toolkit/commits?path=skills/lesson-learned'` returns that one commit, and upstream `SKILL.md` has blob SHA `e358582cc398ba0c02b9a2cc2ae13b29d3e6ba59`, identical to `dbff837f:skills/lesson-learned/SKILL.md`.
- The baseline and the current files carry no credit line. Everything the October rewrite added (evidence-first workflow, git gotchas, the diff-signal lookup, evals) is our own work; the old catalogs (SOLID, DRY, KISS and the rest, Fowler refactoring names) are general engineering knowledge with no distinctive phrase to search, so no web search found a further origin.
- The registry (`docs/audit/upstream-sources.json`) has no row for lesson-learned.

## Proposed registry rows

```json
{"skill": "lesson-learned", "kind": "github-path", "source": "softaworks/agent-toolkit:skills/lesson-learned", "ref": "main", "credit": "Matt White, via softaworks/agent-toolkit"}
{"skill": "lesson-learned", "kind": "unversioned", "source": "git-log documentation: https://git-scm.com/docs/git-log", "ref": null, "credit": "Git project"}
{"skill": "lesson-learned", "kind": "unversioned", "source": "git-diff documentation: https://git-scm.com/docs/git-diff", "ref": null, "credit": "Git project"}
{"skill": "lesson-learned", "kind": "unversioned", "source": "git-show documentation: https://git-scm.com/docs/git-show", "ref": null, "credit": "Git project"}
{"skill": "lesson-learned", "kind": "unversioned", "source": "git-status documentation: https://git-scm.com/docs/git-status", "ref": null, "credit": "Git project"}
{"skill": "lesson-learned", "kind": "unversioned", "source": "git-symbolic-ref documentation: https://git-scm.com/docs/git-symbolic-ref", "ref": null, "credit": "Git project"}
{"skill": "lesson-learned", "kind": "unversioned", "source": "git-rev-parse documentation: https://git-scm.com/docs/git-rev-parse", "ref": null, "credit": "Git project"}
```

The six `unversioned` rows are the pages the facts table cites. I read their text through the installed git 2.56.0 man pages (the same text the site publishes) and a probe repo, not through the web pages, so the URLs are pointers. Existing precedent for credit wording: `viral-tweet` and `ui-ux-designer` use "<name>, via softaworks/agent-toolkit".

## Missing credit line

`skills/lesson-learned/README.md` has none. Proposed last line, after "Related Files" (precedent: `skills/domain-name-brainstormer/README.md` line 43):

```text
Based on the original skill in [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit/tree/main/skills/lesson-learned) by Matt White (PR #11); this version is rewritten.
```

## skill-updater style review (review only, no `track` call)

- Step 1: `skills/lesson-learned/` exists and is not synced.
- Step 2: no row exists, so the proposed `github-path` row is added first; `track` cannot create a source row, so none was called.
- Steps 3-4 (done by hand, same result): the upstream path resolves, there is a single upstream commit on the path (0c042f22, 2026-02-08), and the upstream blob equals the baseline blob. There is no upstream change after the fork point, so the adopt, adapt and ignore lists are empty. Once the row exists, a `track --status current` with `--sha 0c042f22` is the right record for the controller.
- Step 6 (model-validity pass) not run: it dispatches a probe through an LLM lane, and the analyst rails forbid LLM lanes for an analyst. The rules that counter a model habit are the NEVER rules (a commit message does not override the code, no shotgun-surgery label from file counts, never cite an unread file, no refactor plan). Each has an eval scenario that fails when the habit shows (`extraction-adds-coupling`, `mechanical-rename`, `precise-range`, `untracked-only`), so the controller should keep all four.
- Adopt, adapt or ignore items for the restore brief: none. No section of this artifact is marked for restore, so the only edit the brief needs is the credit line above plus the registry rows.
