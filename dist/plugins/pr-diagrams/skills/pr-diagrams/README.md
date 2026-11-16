# pr-diagrams

Render a draw.io diagram to a PNG with the diagram embedded, attach it to a pull request with `gh pr create` or `gh pr edit --attach` (gh >= 2.101), find the merged PRs a promotion should reuse, and collect their human reviewers.

`render` needs `skills/draw-io` installed beside `pr-diagrams` (or `$DRAWIO_CONVERTER`) and the `drawio` CLI on `PATH`. The default converter is `../../draw-io/scripts/convert-drawio-to-png.sh` relative to the script, which is where an installed plugin places both skills.

## Usage

```bash
bash skills/pr-diagrams/scripts/pr-diagrams.sh repo
bash skills/pr-diagrams/scripts/pr-diagrams.sh render path/to/diagram.drawio
bash skills/pr-diagrams/scripts/pr-diagrams.sh capability
bash skills/pr-diagrams/scripts/pr-diagrams.sh publish <N> <png>...
bash skills/pr-diagrams/scripts/pr-diagrams.sh related <base> <head> [--exclude-pr N]
bash skills/pr-diagrams/scripts/pr-diagrams.sh reviewers <PR>... [--exclude LOGIN]
bash skills/pr-diagrams/scripts/pr-diagrams.sh help
```

`repo` prints `<owner>/<repo>` from `origin`. `render` prints `[{"drawio","png"}]` and writes each PNG next to its source. `related` prints merged PRs for `origin/<base>..origin/<head>`, newest `merged_at` first. `reviewers` prints the sorted union of human reviewer logins. Status goes to stderr. A failure prints nothing on stdout.

Attach with one gh call. The body holds `![alt](<path>)` with the exact string given to `--attach`, as an absolute path (gh matches the absolute path; from gh 2.103.0 a relative reference in a `--body-file` body is tried against that file's directory first); gh rewrites the reference. A promotion copies the image URLs already in the source PR bodies instead of rendering again.

`capability` prints `attach` (github.com and `gh` >= 2.101, the tested floor) or `branch` (any other host, a `gh` older than 2.101, or a failed or timed-out probe; the reason goes to stderr). Every probe outcome exits 0; a stray argument exits 2. `PR_DIAGRAMS_MODE=attach|branch` forces it; another value also exits 2, with empty stdout and a usage message. `publish <N> <png>...` commits the PNGs as `<N>/<basename>` on the single branch `pr-diagrams` (an orphan branch, fast-forward pushes only, one retry after a fetch) from a temporary worktree, and prints one `{png, url}` JSON line per file. It exits 2 on a non-digit `N`, a bad PNG argument, or any stray `pr-diagrams-*` / `pr-diagrams/*` branch (local or remote).

The `publish` image URL (`https://<host>/<owner>/<repo>/blob/pr-diagrams/<N>/<name>?raw=true`) is the absolute form. GitHub Docs documents the relative `blob/...?raw=true` form for images in PRs on github.com, working in a private repository for a viewer with read access ([Basic writing and formatting syntax](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax), checked 2026-11-15); the absolute form and GHE are UNVERIFIED: open the PR and check that the image renders.

## Tests

```bash
bash tests/skills/pr-diagrams/test-pr-diagrams.sh
```

## Credits

The PR body templates in `references/pr-body.md` are adapted from the [`explain-pr-changes` command](https://github.com/softaworks/agent-toolkit/blob/main/commands/explain-pr-changes.md) of softaworks/agent-toolkit by Leonardo Flores (@leonardocouy), via softaworks/agent-toolkit. Its `gh` facts follow the GitHub CLI manual and the GitHub Docs (GitHub), its `git` facts follow the Git documentation (Git project), its `drawio` flags follow the draw.io CLI and the drawio-mcp skill (draw.io (JGraph)), and its PNG signature follows the PNG specification (W3C).

## Why gh --attach

Diagram images need a host before a PR body or comment can render them. This spike probed - read-only, nothing created or modified on GitHub - whether GitHub offers a supported way to attach images to a PR body. If none existed, publishing images to a shared `pr-diagrams` branch (one folder per PR number) and referencing the raw URLs would be the only option.

### Probe 1: GitHub CLI

```console
$ gh --version
gh version 2.101.0 (2026-09-15)
https://github.com/cli/cli/releases/tag/v2.101.0

$ gh pr create --help | rg -i 'image|attach|upload'
Use `--attach` to upload an image or video. The attachment is appended to the
body. If the body references an attached file, such as `![alt](./login.png)`, that
reference is rewritten to point at the uploaded asset instead.
You can attach up to 50 files per command.
Alt text for an image follows the path after `#`, as in
`--attach './login.png#The login error state'`. Without it the filename is used.
If some attachments upload and others fail, the pull request is still created with the
      --attach file          Attach an image or video file, in '<file>#<image alt text>' format
  $ gh pr create --attach './login.png#The login error state'
  $ gh pr create --attach ./before.png --attach ./after.png
```

Match: `gh pr create --attach` uploads an image when a PR is created.

The skill targets existing PRs, so a supplementary read-only probe checked the edit path too:

```console
$ gh pr edit --help | rg -i 'image|attach|upload'
Use `--attach` to upload an image or video. Without a body flag the pull
request keeps the body it already has and the attachment is appended to it. If the
body references an attached file, such as `![alt](./login.png)`, that reference is
rewritten to point at the uploaded asset instead.
You can attach up to 50 files per command.
Alt text for an image follows the path after `#`, as in
`--attach './login.png#The login error state'`. Without it the filename is used.
If some attachments upload and others fail, the pull request is still updated with the
      --attach file             Attach an image or video file, in '<file>#<image alt text>' format
  $ gh pr edit 23 --attach './login.png#The login error state'
  $ gh pr edit 23 --attach ./before.png --attach ./after.png
```

Match: `gh pr edit --attach` uploads an image onto an existing PR body.

### Probe 2: GraphQL mutation list

```console
$ gh api graphql -f query='{ __schema { mutationType { fields { name } } } }' --jq '.data.__schema.mutationType.fields[].name' | rg -i 'upload|attach|image'
no match
```

The GitHub GraphQL schema exposes no upload, attach, or image mutation.

### Probe 3: REST reference articles

```console
$ curl -sL 'https://docs.github.com/api/article/body?pathname=/en/rest/issues/issues' | rg -i 'upload|attach|image'
no match

$ curl -sL 'https://docs.github.com/api/article/body?pathname=/en/rest/pulls/pulls' | rg -i 'upload|attach|image'
no match
```

Neither REST reference article documents an upload, attach, or image endpoint.

### What this means

No supported REST or GraphQL API uploads images to a PR. The official GitHub CLI does: `gh pr create --attach` and `gh pr edit --attach` upload an image and rewrite a matching `![alt](<path>)` reference in the same call. The user chose `gh --attach` as the default: `attach` mode on github.com with gh >= 2.101. The shared `pr-diagrams` branch stays as the `branch`-mode fallback for other hosts (GHE) and older gh.

Version note: `--attach` first shipped in gh v2.99.0 ([release notes](https://github.com/cli/cli/releases/tag/v2.99.0), checked 2026-11-15). 2.101 is the version the probes above and this skill's tests were verified on, so it stays the tested floor; below it `capability` prints "gh X.Y is older than the tested floor 2.101: using branch mode".
