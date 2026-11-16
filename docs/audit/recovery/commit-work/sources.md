# commit-work: sources (analysis 2026-11-07)

## Origins found

1. The baseline SKILL.md, README.md and `references/commit-message-template.md` at `dbff837f` are byte-identical to the softaworks original at `3027f20f` (`git diff --stat 3027f20f dbff837f -- skills/commit-work` is empty). The README was written by softaworks (it was added in softaworks commit `06825f04`, 2026-01-18, "Create README.md for each skill"). The reference file came in softaworks commit `e5c69afe` (2026-01-25, "add missing reference"). Source: [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) (MIT), by Leonardo Flores (@leonardocouy). The repository-level fork line (root README.md line 5) names softaworks, but `skills/commit-work/README.md` has no credit line and the registry has no `commit-work` row.
2. The SKILL.md workflow text (frontmatter description, Goal, Inputs, the 8-step checklist, Deliverable) is the same text as the first version of `commit-work/SKILL.md` in [jMerta/codex-skills](https://github.com/jMerta/codex-skills) (MIT, Jakub Merta), committed `d71cf947` on 2025-12-14, about five weeks before softaworks added it. That repository has no README or credit for that file. The origin may be earlier still: a web search found the same text on several mirrors (davila7/claude-code-templates, copied on 2026-01-25 after softaworks), none older than jMerta's. An earlier origin was not found and is not claimed.
3. Conventional Commits 1.0.0 and `@commitlint/config-conventional` are the normative sources of the message rules in the reference file and README Resources (links already present in README; no registry rows yet).

## Proposed registry rows (one JSON object per line, each passes `validate_entry`)

```json
{"skill": "commit-work", "kind": "github-path", "source": "softaworks/agent-toolkit:skills/commit-work", "ref": "main", "credit": "softaworks/agent-toolkit"}
{"skill": "commit-work", "kind": "github-path", "source": "jMerta/codex-skills:commit-work", "ref": "main", "credit": "jMerta/codex-skills"}
{"skill": "commit-work", "kind": "unversioned", "source": "Conventional Commits 1.0.0 specification: https://www.conventionalcommits.org/en/v1.0.0/", "ref": null, "credit": "Conventional Commits"}
{"skill": "commit-work", "kind": "unversioned", "source": "commitlint, Rules reference: https://commitlint.js.org/reference/rules.html", "ref": null, "credit": "commitlint"}
{"skill": "commit-work", "kind": "unversioned", "source": "commitlint, config-conventional preset source: https://github.com/conventional-changelog/commitlint/blob/master/%40commitlint/config-conventional/src/index.ts", "ref": null, "credit": "commitlint"}
{"skill": "commit-work", "kind": "unversioned", "source": "commitlint, Configuration reference: https://github.com/conventional-changelog/commitlint/blob/master/docs/reference/configuration.md", "ref": null, "credit": "commitlint"}
{"skill": "commit-work", "kind": "unversioned", "source": "GitHub Docs, Creating a pull request template for your repository: https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository", "ref": null, "credit": "GitHub"}
{"skill": "commit-work", "kind": "unversioned", "source": "Git documentation, command reference: https://git-scm.com/docs", "ref": null, "credit": "Git"}
```

Notes on the rows:

- `check --strict` fails `missing_credit` unless each row's `credit` text appears verbatim in SKILL.md, README.md or `references/*.md`. Today `softaworks/agent-toolkit` and `jMerta/codex-skills` do not appear, and `GitHub` does not either (README has no capital-G "GitHub"). `Conventional Commits`, `commitlint` and `Git` already appear. So the credit lines below, and one new Resources item, must land in the same commit as the rows.
- The Git row's primary source this session was the installed `git --help <cmd>` (git 2.56.0); `https://git-scm.com/docs` is the matching public documentation.
- The two `github-path` rows are the only ones `upstreams` can compare. softaworks has had no change to `skills/commit-work` since `e5c69afe` (2026-01-25, before the fork point), so that row reads current. jMerta's directory changed in `d853cb9e` (2026-08-17); see the review below.
- `upstreams` was not run: the registry has no `commit-work` row to read. `track` was not called.

## Missing credit lines (exact text to add to `skills/commit-work/README.md`)

Add under the existing last section (or a new `## Credits` section; the same line pattern is in `skills/gemini/README.md` and `skills/naming-analyzer/README.md`):

```text
Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy.
The same workflow text is in [jMerta/codex-skills](https://github.com/jMerta/codex-skills) by Jakub Merta (MIT), committed there on 2025-12-14, before softaworks added it on 2026-01-18.
```

Add to the README `## Resources` list (so the `GitHub` credit resolves):

```text
- [GitHub Docs, creating a pull request template](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository)
```

No credit line already in a file is touched by these additions.

## skill-updater style review (review only; no `track`, no model probe)

Scope: `skills/commit-work/`. Rows: none exist yet. The upstream diff was read by hand: the softaworks directory is unchanged since the fork; jMerta's `commit-work` was rewritten in `d853cb9e` (2026-08-17, "refresh published skills catalog"): a 10-step workflow, a Safety section, a message template with three examples, and a new `references/conventional-commit-types.md`. The local skill is already far past the original on safety (temporary index, staged-version verification, hook-tree check), so most of the upstream rewrite is ignore.

| upstream change | decision | reason |
| --- | --- | --- |
| Keep an implementation and its focused tests in one commit (step 3) | ignore | already the local rule in SKILL.md line 8, tested by eval `split-mixed-work` |
| Infer the convention from repository instructions and recent commits; Conventional Commits only when required or asked (step 4) | ignore, flag | this skill's purpose is Conventional Commits (description, step 6), and the reference already says to apply the repository's commitlint, template and `git log` vocabulary. One tension remains for the controller to note, not fix: step 6 says "Write the message in Conventional Commits 1.0.0" unconditionally while the reference says to copy the repository's vocabulary when no rules exist |
| Avoid `git commit -am` along with `git add .` and `git add -A` (step 5) | adapt | step 3 names only `git add -A` and `git add .`; `git commit -a` stages every modified tracked file (`git --help commit`: "Automatically stage files that have been modified and deleted") and sweeps in the user's unapproved edits. Add `git commit -a` / `-am` to the step 3 never-list in the local wording |
| Review `git diff --cached --check` (step 6) | adapt | `--check` warns about conflict markers and whitespace errors (`git --help diff`); add it to step 4's checks. `--stat` is not needed (the skill already names `git show --stat` and the review of the exact index) |
| A commit request does not authorize pushing (Safety) | adapt | not stated locally; the description excludes force-pushing history, but nothing says a plain commit request stops before `git push`. One sentence in the Route table or step 8 |
| Never `--no-verify` just to pass; do not claim a check passed without output (Safety) | ignore | local step 5 and step 7 are stricter ("staged version not verified"; never propose `--no-verify`) |
| Trailers only when true and repository-appropriate (step 8) | ignore | local step 6: no trailers unless the user or the repository requires them |
| `git show --stat --oneline --decorate HEAD` after the commit (step 9) and `git status -sb` at the end (step 10) | ignore | step 7 compares the written tree with `HEAD^{tree}` and step 8 lists the staged and unstaged leftovers, which covers both |
| `references/commit-message-template.md`: three worked messages (a one-line fix, a refactor with a why body, a breaking change with `!` and footer) and a review checklist (prefer a concrete verb over `Update`; `Closes #123` only when merging should close the issue) | adapt | the local reference has rules but no worked message, and the baseline's only message-with-body sample (README Example 1) is dropped under s009. Port the three examples and the two checklist items (concrete verb; `Closes` only on merge) into `references/commit-message-template.md` in the local voice, with no `Co-authored-by` line since the local default is no trailers. Fits the s022 drop-pending interim restore |
| `references/conventional-commit-types.md` (meaning of each type) | ignore | one-line meanings of feat, fix, docs and the rest are generic model knowledge, and the list omits `style`, which the commitlint `type-enum` in the local reference includes |
| Trigger-first description ("Use when the user asks to...") | ignore | the local description already carries triggers, the scope and the exclusions |
| `agents/openai.yaml` (Codex UI metadata) | ignore | targets a different runtime |

Model-validity pass: not run (it needs an LLM probe lane, and this analysis forbids LLM judging). Candidates for the controller: the rule against trailers (`Co-Authored-By`, "Generated with") counters a default habit of Claude Code and is the likeliest to still be needed; the rules against `git add -A`, `--no-verify`, amend-on-failure and `git stash` counter common agent shortcuts. Do not propose removal of any of them without a probe.

## Docs pages used this session (all proposed `unversioned` rows above)

- https://www.conventionalcommits.org/en/v1.0.0/ (spec, read in full)
- https://commitlint.js.org/reference/rules.html (rule semantics and bare defaults)
- https://github.com/conventional-changelog/commitlint/blob/master/%40commitlint/config-conventional/src/index.ts (preset values)
- https://github.com/conventional-changelog/commitlint/blob/master/docs/reference/configuration.md (config file names)
- https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository (PR template paths)
- the installed `git --help <command>` pages, git 2.56.0 (the Git row)
