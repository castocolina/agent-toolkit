# Why a shared branch

Diagram images need a host before a PR body or comment can render them. This spike probed — read-only, nothing created or modified on GitHub — whether GitHub offers a supported way to attach images to a PR body. If none existed, publishing images to a shared `pr-diagrams` branch (one folder per PR number) and referencing the raw URLs would be the only option.

## Probe 1: GitHub CLI

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

## Probe 2: GraphQL mutation list

```console
$ gh api graphql -f query='{ __schema { mutationType { fields { name } } } }' --jq '.data.__schema.mutationType.fields[].name' | rg -i 'upload|attach|image'
no match
```

The GitHub GraphQL schema exposes no upload, attach, or image mutation.

## Probe 3: REST reference articles

```console
$ curl -sL 'https://docs.github.com/api/article/body?pathname=/en/rest/issues/issues' | rg -i 'upload|attach|image'
no match

$ curl -sL 'https://docs.github.com/api/article/body?pathname=/en/rest/pulls/pulls' | rg -i 'upload|attach|image'
no match
```

Neither REST reference article documents an upload, attach, or image endpoint.

## What this means

No supported REST or GraphQL API uploads images to a PR. However, the official GitHub CLI ships a supported client feature for exactly this use case: `gh pr edit --attach` uploads an image and appends it to an existing PR body, rewriting `![alt](./file.png)` references to the uploaded asset. That is a viable alternative to the shared `pr-diagrams` branch, with the caveat that every publish run mutates the PR body (appending the image) instead of only updating a comment.

Conclusion: supported API: gh pr edit --attach (gh CLI; no REST/GraphQL upload endpoint)
