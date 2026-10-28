---
name: pr-diagrams
description: Render draw.io diagrams to PNGs with the diagram embedded, attach them to a pull request with gh --attach, find the merged PRs a promotion should reuse, and collect their human reviewers. Use when attaching a diagram to a PR, reusing diagrams in a promotion PR, finding related merged PRs, or reusing reviewers, even without the words "pr-diagrams". Not for drawing a diagram of a module, creating a pull request, or editing draw.io XML (draw-io).
---

# PR Diagrams

`pr-diagrams` never pushes images to a branch: a draw.io diagram is rendered to a PNG with the diagram embedded and uploaded with `gh pr create/edit --attach` (gh >= 2.101).

The helper is `bash ${CLAUDE_SKILL_DIR}/scripts/pr-diagrams.sh`. A harness that does not substitute `${CLAUDE_SKILL_DIR}` uses `bash ~/.claude/skills/pr-diagrams/scripts/pr-diagrams.sh`. `render` needs `skills/draw-io` installed beside `pr-diagrams` (or `$DRAWIO_CONVERTER`) and the `drawio` CLI on `PATH`.

## Attach

One call. The body holds `![alt](<path>)` where `<path>` is character-for-character the string given to `--attach`. gh uploads the file and rewrites that reference to the uploaded asset.

```bash
gh pr create --repo "$REPO" --base "$BASE" --head "$HEAD" \
  --title "$TITLE" --body-file "$AD/body.md" --attach "$PNG"
gh pr edit "$N" --repo "$REPO" --body-file "$AD/body.md" --attach "$PNG"
```

`$PNG` is the path `render` printed. Do not push the PNG to a branch and do not rewrite the reference yourself.

## Reuse

A promotion copies the image URLs already in the source PR bodies. It does not render or attach again. Drop one leading `[<from> → <to>] ` prefix from a source title, then prefix `[<head> → <base>] `.

## Rendering

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/pr-diagrams.sh render path/to/diagram.drawio
```

Stdout is `[{"drawio","png"}]`. The PNG sits next to the source, is non-empty, starts with the PNG signature, and embeds the diagram because the converter passes `drawio -e`. Two inputs with the same basename fail before conversion. A missing `drawio` CLI, a missing PNG, or a non-PNG fails with nothing copied. Status lines stay on stderr.

## Promotion discovery

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/pr-diagrams.sh related <base> <head> [--exclude-pr N]
```

Fetches `origin/<base>` and `origin/<head>`, then asks GitHub which pull requests touch each commit in the range (one paginated call per commit, no cap). Stdout is `[{"pr","title","head_ref","base_ref","merged_at"}]`, only merged PRs, without PR `N`, sorted by `merged_at` descending then PR number descending. No related PR prints `[]`. A `(HTTP 403)` or `(HTTP 429)` failure exits 1 with `rate limited` and the commit; any other failure names the commit. Nothing is printed on stdout when a call fails.

Sources for a promotion are the related PRs whose `base_ref` equals the current head.

## Reviewers

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/pr-diagrams.sh reviewers <PR>... [--exclude LOGIN]
```

Stdout is a sorted JSON array of human logins (`type` `User` only). Bots such as `copilot-pull-request-reviewer`, reviews whose `user` is null, and teams are dropped. `LOGIN` is removed case-insensitively, and duplicate logins collapse case-insensitively. A failed read exits 1 naming the PR, with nothing on stdout.

## Repository

`repo` prints `<owner>/<repo>` parsed from `origin` (https, `git@github.com:`, and `ssh://`, optional `.git`). A non-GitHub or unparsable origin exits 1 naming the URL. `related` and `reviewers` call `gh api repos/<owner>/<repo>/...` with those names.

## Failures

- `render` exits 1: report its stderr. `drawio CLI not found` means install the draw.io desktop CLI. A converter or PNG error means the diagram was not attached; do not copy a partial PNG.
- `related` exits 1 with `rate limited`: stop. Do not keep calling GitHub for the rest of the range.
- `related` or `reviewers` exits 1 otherwise: report the commit or PR it names and stop. stdout is empty on every failure.
- Never stage the PNG into the caller's git index. `render` converts in its own scratch repository.
