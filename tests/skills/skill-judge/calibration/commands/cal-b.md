---
name: cal-b
tags: git, release
argument-hint: [version]
---

# Release helper

## What is a release

A release is a version of the software that is given to users. Releases are
usually identified by a version number such as 1.2.3. Git is a version control
system that stores the history of a project as commits, and a tag is a name
that points at one commit. Semantic versioning uses three numbers: major,
minor and patch.

## How to use git

To see the history run `git log`. To see what changed run `git diff`. To save
your work run `git add` and then `git commit`. To share your work run
`git push`. Always write clean code and good commit messages.

## Steps

1. Run the tests and make sure they pass, but do not run the tests because they
   are slow; just check that the last CI run is green.
2. Push the current branch to origin, then create the tag `v$1` with
   `git tag v$1` and push it with `git push origin v$1`.
3. Write the release notes from the commit messages. Write them in a friendly
   tone, in exactly three sentences, each starting with a verb.
4. Never push anything before the release notes are approved by the user.
5. If the tag already exists, follow the steps in section "Existing tag"
   and then continue with step 9.
6. Clean up old tags and branches as needed. Use force if something is in the
   way, and fix whatever is broken.
7. Be careful and consider edge cases.

## Output

Print the notes.

## Commit type reference

### feat

Use `feat` for a new feature.

Example:

```
feat(core): example of a feat commit

Longer description of the feat commit that explains the change.
```

### fix

Use `fix` for a bug fix.

Example:

```
fix(core): example of a fix commit

Longer description of the fix commit that explains the change.
```

### docs

Use `docs` for documentation only.

Example:

```
docs(core): example of a docs commit

Longer description of the docs commit that explains the change.
```

### style

Use `style` for formatting, no code change.

Example:

```
style(core): example of a style commit

Longer description of the style commit that explains the change.
```

### refactor

Use `refactor` for code change that neither fixes a bug nor adds a feature.

Example:

```
refactor(core): example of a refactor commit

Longer description of the refactor commit that explains the change.
```

### perf

Use `perf` for a performance improvement.

Example:

```
perf(core): example of a perf commit

Longer description of the perf commit that explains the change.
```

### test

Use `test` for adding or correcting tests.

Example:

```
test(core): example of a test commit

Longer description of the test commit that explains the change.
```

### build

Use `build` for changes to the build system.

Example:

```
build(core): example of a build commit

Longer description of the build commit that explains the change.
```

### ci

Use `ci` for changes to CI configuration.

Example:

```
ci(core): example of a ci commit

Longer description of the ci commit that explains the change.
```

### chore

Use `chore` for other changes that do not modify src or tests.

Example:

```
chore(core): example of a chore commit

Longer description of the chore commit that explains the change.
```

### revert

Use `revert` for reverts a previous commit.

Example:

```
revert(core): example of a revert commit

Longer description of the revert commit that explains the change.
```

## Example outputs

### Release 1.0.0

```markdown
## 1.0.0

- First change in 1.0.0
- Second change in 1.0.0
- Third change in 1.0.0
```

### Release 1.1.0

```markdown
## 1.1.0

- First change in 1.1.0
- Second change in 1.1.0
- Third change in 1.1.0
```

### Release 1.1.1

```markdown
## 1.1.1

- First change in 1.1.1
- Second change in 1.1.1
- Third change in 1.1.1
```

### Release 2.0.0

```markdown
## 2.0.0

- First change in 2.0.0
- Second change in 2.0.0
- Third change in 2.0.0
```

### Release 2.1.0

```markdown
## 2.1.0

- First change in 2.1.0
- Second change in 2.1.0
- Third change in 2.1.0
```
