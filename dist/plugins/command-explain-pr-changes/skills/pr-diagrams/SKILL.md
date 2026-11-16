---
name: pr-diagrams
description: Render draw.io diagrams to PNGs with the diagram embedded, attach them to a pull request with gh --attach or, on GitHub Enterprise or gh older than 2.101, publish them to the single pr-diagrams branch, find the merged PRs a promotion should reuse, and collect those source PRs' human reviewers for the promotion. Use when attaching or hosting a diagram image in a PR body, choosing where diagram images live, reusing diagrams in a promotion PR, finding related merged PRs, or reusing reviewers from merged source PRs, even without the words "pr-diagrams". Not for drawing a diagram of a module, creating a pull request, listing the reviewers already requested on a PR (gh pr view), or editing draw.io XML (draw-io).
---

# PR Diagrams

Gets a rendered draw.io diagram into a PR body on any GitHub host, and lets a promotion PR reuse the diagrams and reviewers of the PRs it promotes.

## Setup

`PRD` is `${CLAUDE_SKILL_DIR}/scripts/pr-diagrams.sh`; a harness that does not substitute `${CLAUDE_SKILL_DIR}` uses the absolute path of `scripts/pr-diagrams.sh` under the directory this SKILL.md was loaded from. `bash "$PRD" help` prints every subcommand, its stdout JSON and the exit codes (1 failure, 2 usage error or refusal). `render` needs `skills/draw-io` installed beside `pr-diagrams` (or `$DRAWIO_CONVERTER`) and the `drawio` CLI on `PATH`.

A standalone caller sets these once; the `explain-pr-changes` command sets its own:

```bash
AD=$(mktemp -d)                 # scratch directory for bodies
REPO=$(bash "$PRD" repo)        # <owner>/<repo> of origin
BASE=main HEAD=feature/login    # target and source branch of the PR
TITLE="Add the login flow"
# N: number of an existing PR; for a new PR it exists only after gh pr create
#    prints the PR URL (N is the last path segment of that URL).
```

On a host other than github.com (GHE), `repo` exits 1: set `REPO=<host>/<owner>/<repo>` by hand, a form every `gh pr --repo` call accepts. `capability`, `render` and `publish` work there; `related` and `reviewers` support github.com only, so promotion reuse is unavailable on GHE.

## Workflow

1. Mode: `MODE=$(bash "$PRD" capability)` prints `attach` (github.com and gh >= 2.101) or `branch` (any other host, older gh, failed or timed-out probe; the reason goes to stderr). It always exits 0; `PR_DIAGRAMS_MODE=attach|branch` forces it.
2. Render: `PNG=$(bash "$PRD" render path/to/diagram.drawio | jq -r '.[0].png')` (contract below). Exit 1 means no PNG: skip step 4 and use the fallback body.
3. Fallback: write `$AD/body-fallback.md`, the same prose with an inline Mermaid block in place of the PNG reference (omit the diagram only when it has no Mermaid equivalent). Every failure path below restores it.
4. Put the image in the body:
   - `attach`: `$AD/body.md` holds `![diagram](<PNG>)` where `<PNG>` is character-for-character the string given to `--attach`. One call; gh uploads the file and rewrites that reference. No branch is pushed.
     ```bash
     gh pr create --repo "$REPO" --base "$BASE" --head "$HEAD" \
       --title "$TITLE" --body-file "$AD/body.md" --attach "$PNG"
     gh pr edit "$N" --repo "$REPO" --body-file "$AD/body.md" --attach "$PNG"   # existing PR
     ```
   - `branch`, existing PR: `bash "$PRD" publish "$N" "$PNG"` commits the PNG as `<N>/<name>` on the single branch `pr-diagrams` and prints one `{"png","url"}` JSON line per file. Put `![diagram](<url>)` in `$AD/body.md`, then run one `gh pr edit "$N" --repo "$REPO" --body-file "$AD/body.md"` (no `--attach`).
   - `branch`, new PR: `publish` needs `N`, so the order is fixed: `gh pr create ... --body-file "$AD/body-fallback.md"` (no `--attach`), take `N` from the printed URL, `publish "$N" "$PNG"`, then one `gh pr edit` with the printed url. Read the reference section below for the exact calls.
5. Promotion PR: skip steps 2-4 and follow Promotion.

## Rendering

Stdout is a JSON list of `{drawio, png}`. `render a/diagram.drawio` writes `a/diagram.drawio.png` next to its source (conversion runs on a scratch copy, then the PNG is copied back). The PNG is non-empty, starts with the PNG signature and embeds the diagram because the converter passes drawio `-e` (`--embed-diagram`), so draw.io reopens it as an editable diagram. Two inputs with the same basename fail before conversion. A missing `drawio` CLI, a missing PNG or a non-PNG fails with nothing copied. Status lines stay on stderr.

## Promotion

A promotion PR (`$HEAD` → `$BASE`, for example `staging` → `production`) copies the image URLs already in its source PR bodies. It does not render, upload or attach again.

1. `bash "$PRD" related "$BASE" "$HEAD" [--exclude-pr "$N"]` fetches `origin/$BASE` and `origin/$HEAD`, then asks GitHub which PRs touch each commit in the range (one paginated call per commit, no cap). Stdout is `[{"pr","title","head_ref","base_ref","merged_at"}]`: merged PRs only, without PR `N`, sorted by `merged_at` descending then PR number descending; no related PR prints `[]`.
2. Sources are the entries whose `base_ref` equals `$HEAD`, in that order.
3. Check the merge-commit assumption: `git rev-list --merges "origin/$BASE..origin/$HEAD"`. Empty output means the history was squashed or rebased (see Gotchas): stop and ask for an explicit merged source PR (the command's `--reuse-from=<PR>`) instead of reusing the list.
4. Read each source with `gh pr view <pr> --repo "$REPO" --json title,body` and copy its image references byte for byte. Title: drop one leading `[<from> → <to>] ` prefix from the source title, then prefix `[$HEAD → $BASE] ` (`[main → staging] Add X` becomes `[staging → production] Add X`, never two prefixes).
5. Reviewers: `bash "$PRD" reviewers <source PRs>... --exclude "$(gh api user --jq .login)"` prints a sorted JSON array of human logins (`type` `User` only): bots such as `copilot-pull-request-reviewer`, reviews whose `user` is null, and teams are dropped; `--exclude` and duplicates match case-insensitively. Request them with `gh pr edit "$N" --repo "$REPO" --add-reviewer <login>,...`.

`repo` prints `<owner>/<repo>` parsed from `origin` (https, `git@github.com:` and `ssh://`, optional `.git` or trailing slash); a non-github.com or unparsable origin exits 1 naming the URL (GHE: see Setup).

## Failures

stdout is empty on every failure.

- `render` exits 1: report its stderr; there is no PNG to attach. `drawio CLI not found` means install the draw.io desktop CLI. Never copy a partial PNG.
- `related` exits 1 with `rate limited` (an `HTTP 403` or `HTTP 429` on the named commit): stop; do not keep calling GitHub for the rest of the range, and never read the empty stdout as "no related PRs".
- `related` or `reviewers` exits 1 otherwise: report the commit or PR it names and stop.
- `publish` exits non-zero: the body keeps or gets `$AD/body-fallback.md` (one `gh pr edit` for an existing PR); quote publish's stderr. Exit 2 naming two repositories (host and `<owner>/<repo>` each) means gh resolves a different repository than `origin`: fix the gh default or the remote before publishing again.
- `gh pr create --attach` exits non-zero after printing a PR URL: a partial attach, the PR exists. Take `N` from that URL and follow "Partial `--attach` failure" in the reference: publish through the branch, else restore `$AD/body-fallback.md`; if that edit fails too, report it with the PR URL. Quote gh's stderr.

## Gotchas

- NEVER create a branch per PR: the only image branch is exactly `pr-diagrams`, one folder per PR number. `publish` refuses (exit 2) while any `pr-diagrams-*` or `pr-diagrams/*` branch exists locally or on origin, and the `explain-pr-changes` none-mode filter strips only `/<owner>/<repo>/blob/pr-diagrams/<digits>/` URLs, so images on any other branch leak into promotions.

  | Wrong | Right |
  |---|---|
  | branch `pr-diagrams/41` | branch `pr-diagrams`, file `41/diagram.drawio.png` |
  | branch `pr-diagrams-41` | branch `pr-diagrams`, file `41/diagram.drawio.png` |

- NEVER rewrite the `--attach` reference yourself or change its path (`./x.png` is not `/tmp/ad/x.png`): gh rewrites only a reference that matches the argument exactly; otherwise it appends the uploaded image at the end of the body and leaves your reference as written, so the body shows a broken image plus a stray copy.
- NEVER stage or commit the PNG in the caller's repository: `render` converts in its own scratch repository so the caller's index stays as it was, and a staged PNG lands in the feature PR's diff.
- NEVER re-create a PR after a partial `--attach` failure: gh created the PR before the upload failed, so a second `gh pr create` fails on the existing head or opens a duplicate.
- NEVER retry `publish` after exit 2: it is a refusal (bad argument, stray branch, gh and `origin` naming different repositories) that a retry cannot change, and pushing anyway would put the image in one repository and its URL in another.
- `related` assumes merge commits. With squash or rebase merges an older cycle's commits stay in `origin/$BASE..origin/$HEAD`, so already-promoted PRs come back as sources; that is why step 3 stops.
- The `publish` URL (`https://<host>/<owner>/<repo>/blob/pr-diagrams/<N>/<name>?raw=true`) is unverified for private repositories and GHE: after the edit, open the PR and check that the image renders.

## Reference

`references/pr-body.md`, read only the section the case needs:

- Branch mode with a new PR, or after a partial `--attach` failure: section "Branch publish and attach recovery" (exact gh calls and warning lines).
- Building a promotion title or body in shell: section "Title normalization and body assembly" (quoting-safe prefix code).

Do NOT load it for `capability`, `render`, `related`, `reviewers` or an `--attach` call that succeeded. Its other sections (none-mode filter, body templates) belong to the `explain-pr-changes` command.
