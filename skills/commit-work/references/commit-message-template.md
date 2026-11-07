# Repository message rules

Read this when the repository sets its own commit-message rules, a commit needs footers beyond `BREAKING CHANGE`, or you want worked messages and the report block of step 8. The shape and the no-trailers default live in SKILL.md step 6.

## Collect the repository's rules

Read every source that exists and apply all of them; ask when two conflict.

- commitlint: `commitlint.config.*`, `.commitlintrc*` or a `commitlint` key in `package.json`. Start from what `extends` pulls in (`@commitlint/config-conventional` means the defaults below), then apply the local `rules`, which override it.
- `git config commit.template` (often `.gitmessage`), `.czrc` or `cz.json` (Commitizen; read whichever Commitizen config the repository actually has, since the file name depends on its setup).
- `CONTRIBUTING.md` and PR templates (`.github/pull_request_template.md`, `.github/PULL_REQUEST_TEMPLATE/`): required footers or trailers (DCO `Signed-off-by`, issue refs), scope lists.
- None of these: copy the type and scope vocabulary of `git log --format=%s -30`, then check each scope against current paths.
- No history either (empty or brand-new repository): Conventional Commits 1.0.0 is the default.

## `@commitlint/config-conventional` defaults that reject plausible messages

Values from the [preset source](https://github.com/conventional-changelog/commitlint/blob/master/%40commitlint/config-conventional/src/index.ts), checked 2026-11-07. Read the installed preset when the repository pins a version. The repository's own commitlint config (`commitlint.config.*`, `.commitlintrc*`, or the `commitlint` key in `package.json`) overrides any of these rules, so read it first and use its values.

- `type-enum`: build, chore, ci, docs, feat, fix, perf, refactor, revert, style, test. Anything else fails, even though the spec allows any type.
- `subject-case`: a subject in sentence, start, pascal or upper case fails (`fix: Handle nulls` is rejected).
- `header-max-length` 100; `body-max-line-length` and `footer-max-line-length` 100; `subject-full-stop`: no trailing `.`.

## Spec rules models get wrong (Conventional Commits 1.0.0)

- Only `feat` (minor) and `fix` (patch) carry meaning in the spec; other types come from the Angular convention.
- `!` sits immediately before the colon: `feat(api)!: drop v1 routes`. With `!` the `BREAKING CHANGE:` footer may be omitted; the subject must then describe the break.
- In a footer, `BREAKING CHANGE` must be upper case; `BREAKING-CHANGE` is a synonym. Every other footer token uses `-` for spaces (`Reviewed-by: name`, `Refs: #123`) and is separated by `: ` or ` #`.
- Footers start one blank line after the body; a footer value can continue over lines until the next token.
- For a revert, the spec suggests the `revert` type with a `Refs:` footer listing the reverted SHAs.

## Message template

```text
<type>(<scope>): <summary>

<What changed.>
<Why it changed.>
```

- Keep the summary imperative and specific ("add", "fix", "remove", "extract"), lower case when commitlint's `subject-case` applies.
- Describe behavior and intent, not implementation minutiae.
- A real compatibility break: `!` in the header, a `BREAKING CHANGE:` footer, or both. No other footer is added unless the user or the repository requires it.

## Worked messages

A one-line fix, no body needed:

```text
fix(auth): treat a token at its expiry time as expired
```

A refactor whose body says why:

```text
refactor(ui): extract menu logic into a custom hook

The open, close and focus handling lived inline in Header and was
copied into Footer. One hook keeps the two in step; behavior is
unchanged.
```

A breaking change, marked in the header and explained in the footer:

```text
feat(api)!: drop the v1 routes

v1 doubled the test matrix and every client has a v2 equivalent.

BREAKING CHANGE: /v1/* now returns 404; use the /v2/* routes.
```

## Message checklist

- The summary starts with a concrete verb (`fix`, `add`, `remove`, `rename`) rather than `Update` or `Change`.
- `Closes #123` appears only when merging this commit should close the issue; otherwise use `Refs: #123`.

## Report block per commit

SKILL.md step 8 asks for a short block per commit, after the hash, subject and verification line:

```text
<hash> <subject>
what/why: <one line: what changed and why>
commands: <the staging, review and verification commands you ran, for example git add -- <paths>, git diff --cached, vitest run>
```
