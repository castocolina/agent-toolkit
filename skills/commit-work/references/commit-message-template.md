# Repository message rules

Read this when the repository sets its own commit-message rules, or a commit needs footers beyond `BREAKING CHANGE`. The shape and the no-trailers default live in SKILL.md step 6.

## Collect the repository's rules

Read every source that exists and apply all of them; ask when two conflict.

- commitlint: `commitlint.config.*`, `.commitlintrc*` or a `commitlint` key in `package.json`. Start from what `extends` pulls in (`@commitlint/config-conventional` means the defaults below), then apply the local `rules`, which override it.
- `git config commit.template` (often `.gitmessage`), `.czrc` or `cz.json` (Commitizen).
- `CONTRIBUTING.md` and PR templates (`.github/pull_request_template.md`, `.github/PULL_REQUEST_TEMPLATE/`): required footers or trailers (DCO `Signed-off-by`, issue refs), scope lists.
- None of these: copy the type and scope vocabulary of `git log --format=%s -30`, then check each scope against current paths.

## `@commitlint/config-conventional` defaults that reject plausible messages

- `type-enum`: build, chore, ci, docs, feat, fix, perf, refactor, revert, style, test. Anything else fails, even though the spec allows any type.
- `subject-case`: a subject in sentence, start, pascal or upper case fails (`fix: Handle nulls` is rejected).
- `header-max-length` 100; `body-max-line-length` and `footer-max-line-length` 100; `subject-full-stop`: no trailing `.`.

## Spec rules models get wrong (Conventional Commits 1.0.0)

- Only `feat` (minor) and `fix` (patch) carry meaning in the spec; other types come from the Angular convention.
- `!` sits immediately before the colon: `feat(api)!: drop v1 routes`. With `!` the `BREAKING CHANGE:` footer may be omitted; the subject must then describe the break.
- In a footer, `BREAKING CHANGE` must be upper case; `BREAKING-CHANGE` is a synonym. Every other footer token uses `-` for spaces (`Reviewed-by: name`, `Refs: #123`) and is separated by `: ` or ` #`.
- Footers start one blank line after the body; a footer value can continue over lines until the next token.
- For a revert, the spec suggests the `revert` type with a `Refs:` footer listing the reverted SHAs.
