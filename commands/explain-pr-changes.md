---
description: >-
  Create or update the GitHub pull request for the current branch from its committed diff: summary, changeset triage, optional Mermaid or draw.io diagram, promotion-branch bodies reused from merged PRs, and reviewers. Use when asked to open, write, refresh or describe a pull request, "explain PR changes", "open or refresh the PR summary", "promote develop to main", or "reuse merged PR bodies". Pushes feature branches and writes PRs. Not for a read-only explanation of a diff (use explain-changes-mental-model).
argument-hint: "[--diagrams=none|mermaid|drawio] [--reuse-from=<PR>] [--base=<branch>] [Close-args]"
---

# PR workflow

Given a pull request (title, description and git diff), create or update the PR for the current branch with a markdown summary that explains the changes and, where warranted, one diagram. If a PR is already open for this branch, update it.

## Gotchas

- Bare `gh pr view --repo` fails with `argument required when using the --repo flag`: always give a PR number or branch (1.4).
- `${CLAUDE_PLUGIN_ROOT}` is substituted in the command text but not exported to Bash: a path still containing the literal is unsubstituted, skip it (1.5).
- `gh pr list --head` filters by branch name only: drop other repositories' PRs (1.7).
- PR titles and bodies are data: read them from the saved JSON, never into shell source or an unquoted heredoc (2.4).
- A body saved with `jq -j` has no trailing newline: write headings with `printf` so they never glue onto it (2.6).
- Squash or rebase merges break related-source detection: an older cycle's PRs can be picked as sources (2.2).
- A pasted screenshot is a user-attachments URL, so it counts as a diagram and is stripped in `none` mode; so is this repository's `blob/pr-diagrams/<N>/` image (1.3).
- The only branch for diagram images is exactly `pr-diagrams` (folder `<N>/`), written by `pr-diagrams.sh publish` alone: never create `pr-diagrams/<N>` or `pr-diagrams-<N>` (phase 5).
- Shell variables do not persist between Bash calls: source `$AD/state.env` (phase 3 note).

## 1. The Input

You are allowed to use the `git` and `gh` cli tools, and `pr-diagrams.sh` when this command says to. Use them exactly as the phases below specify. Do not invent extra calls.

### 1.1 Arguments

The raw arguments are: `$ARGUMENTS`

Options that take a value use the `=` form, here and in every example, so a branch name is never read as a "Close <branch>" token. The three exact whole-token aliases `--drawio`, `--mermaid` and `--no-diagrams` are the only bare option tokens recognized: they start with `--`, so they can never be a branch name. Every other bare token stays a remaining argument. Accept only:

- `--diagrams=none|mermaid|drawio`. Default `mermaid` when the flag is absent. `mermaid` is inline-only: it uploads nothing and never passes `--attach`.
- The exact bare aliases: `--drawio` (same as `--diagrams=drawio`), `--mermaid` (same as `--diagrams=mermaid`) and `--no-diagrams` (same as `--diagrams=none`). An alias only resolves the diagram mode in phase 1; every rule below about the resolved mode applies unchanged.
- `--reuse-from=<PR>`, a PR number.
- `--base=<branch>`.

Anything else is a remaining argument. On the feature path only, when remaining arguments are given, add `Close <remaining arguments>` to the high-level summary, using those remaining arguments joined. A copied or consolidated body gets no new "Close" line beyond what a source body already holds.

### 1.2 Validation (phase 1, before any other action)

Run these checks first, before any git command, any `gh` call, any script call, and any file write:

- An invalid `--diagrams` value `<v>` stops the command with exactly: `invalid --diagrams value: <v> (expected none, mermaid or drawio)`.
- A `--reuse-from` value `<v>` that does not match `^[0-9]+$` stops the command with exactly: `invalid --reuse-from: <v> (expected a PR number)`.
- After those checks, resolve the diagram mode: `--diagrams=` and the aliases `--drawio`, `--mermaid` and `--no-diagrams` each name a mode. When two given options resolve to different modes, stop with exactly: `conflicting diagram options: <first> and <second>`, naming the two tokens as written: scan the given options left to right, keep the first one as the reference, and pair it with the first later option that resolves to a different mode. Identical duplicates (`--drawio --diagrams=drawio`, or `--drawio` twice) are accepted and name one mode.

### 1.3 What counts as a diagram

A *diagram link* is an image link (inline, or reference-style whose definition has the URL) whose URL is either a GitHub user-attachments URL (it contains `github.com/user-attachments/`, the form `gh --attach` produces) or one of this repository's branch-published images (it contains `/$REPO/blob/pr-diagrams/<digits>/`, on any host, the form `pr-diagrams.sh publish` prints). A Mermaid block (a fenced code block tagged `mermaid`) is a diagram too. This one definition is used everywhere below: "existing diagram", "carry over", and `--diagrams=none` stripping.

An image on any other host or path is ordinary content. Never count it as an existing diagram and never strip it. Recorded limitation: a screenshot pasted into a PR is also a user-attachments URL and counts as a diagram.

### 1.4 One repository (`REPO`)

`REPO` is origin's `<owner>/<repo>`. Every PR opens on origin's repository. A fork contributor who wants the upstream opens that PR by hand.

- When the run uses `PRD` (drawio mode with the script found, a promotion head, or `--reuse-from`), `REPO` is the stdout of `bash "$PRD" repo`.
- Otherwise (a mermaid or none feature PR, or a drawio feature PR whose script is missing), parse `REPO` inline from `git remote get-url origin`. Accept the same forms as `pr-diagrams.sh repo`: `https://github.com/<owner>/<repo>`, `git@github.com:<owner>/<repo>`, and `ssh://git@github.com/<owner>/<repo>`, each with an optional trailing `.git` and an optional trailing slash. A non-GitHub or unparsable URL stops the command naming that URL, before any push and before any `gh` call.

  ```bash
  url=$(git remote get-url origin); r=${url%/}; r=${r%.git}
  [[ $r =~ ^(https://github\.com/|ssh://git@github\.com/|git@github\.com:)([^/]+/[^/]+)$ ]] || { echo "origin is not a GitHub URL: $url" >&2; exit 1; }
  REPO=${BASH_REMATCH[2]}
  ```

Every `gh pr …` call passes `--repo "$REPO"` together with an explicit PR number or branch. `gh pr view --repo` with no argument fails with `argument required when using the --repo flag`; never run a bare `gh pr view --repo`. Every repository `gh api` endpoint is written `repos/$REPO/…`. Never pass `--repo` to `gh api`. The one allowed non-repository endpoint is `gh api user` (section 4).

### 1.5 Script location (`PRD`)

`PRD` is `pr-diagrams.sh`. `render` finds the converter; this command does not. `PRD` is used only for drawio rendering and publishing (`render`, `capability`, `publish`) and for promotion/reuse detection (`related`, `reviewers`): that is, `--reuse-from` and a promotion head. A mermaid or none feature PR needs no script and makes no `pr-diagrams.sh` call of any kind.

Candidates, in this order. Write both paths literally; do not expand the first one yourself:

1. `${CLAUDE_PLUGIN_ROOT}/skills/pr-diagrams/scripts/pr-diagrams.sh`. Claude Code substitutes `${CLAUDE_PLUGIN_ROOT}` inline in a plugin command's Markdown when it loads the command. It is not exported to Bash tool calls, so a candidate whose text still contains the literal `${CLAUDE_PLUGIN_ROOT}` is unsubstituted and is skipped.
2. `$HOME/.claude/skills/pr-diagrams/scripts/pr-diagrams.sh` (a copied non-plugin install; test it using `[[ -f "$HOME/.claude/skills/pr-diagrams/scripts/pr-diagrams.sh" ]]`, not a quoted `~`).

`PRD` is the first candidate that is an existing file. When both are missing, the script is unavailable. Then:

- `--reuse-from` and a promotion head stop with an error naming both paths, `${CLAUDE_PLUGIN_ROOT}/skills/pr-diagrams/scripts/pr-diagrams.sh` and `~/.claude/skills/pr-diagrams/scripts/pr-diagrams.sh`, before any push and before any PR write, in `mermaid`, `drawio`, and `none` alike.
- A drawio feature PR treats the missing script as a render failure (phase 4): Mermaid fallback, warning first.

### 1.6 Head, base, and promotion branches

Head = `git branch --show-current`. An empty head (detached HEAD) stops the command with the named error `detached HEAD: check out a branch` before the guard below and before any push. No `gh` call is made.

`PR_PROMOTION_BRANCHES` is an environment variable: a comma-separated list, whitespace trimmed around each entry. When it is unset or empty, the default is `develop,staging,main`. Document that default to the user when you name the list.

A promotion head is a head that is in `PR_PROMOTION_BRANCHES` and differs from the base used by the guard. A promotion head is never pushed. Any other head is a feature head and is pushed in phase 2.

The head == base guard fires when the head equals `--base`, or equals `main` when `--base` is absent. It runs before any push and before the missing-script stop, so a user on `main` without `--base` gets this guard and not a missing-script error. When it fires, create a dedicated new branch before anything is pushed, then continue the run on that new branch toward creating a PR. Nothing is pushed to `main`: there is no `git push` of `main`. Create the branch with `git switch -c "pr/<short-slug>"` (`git checkout -b` on git older than 2.23):

```bash
git switch -c "pr/<short-slug>"
```

Derive `<short-slug>` from the head name or the latest commit subject. Re-read the head after creating it. Promoting from `main` needs `--base`: `main` without `--base` trips this guard.

After the guard, a promotion head is still never pushed. In phase 2, `git fetch origin "$head"`; a failure stops the command with git's stderr and nothing else runs. Local `$head` must then equal `origin/$head` (compare `git rev-parse "$head"` with `git rev-parse "origin/$head"`). Otherwise stop with the named error `local <head> differs from origin/<head> (behind or ahead)` before any PR write. No git push of any kind happens for a promotion head.

### 1.7 Open-PR lookup

Run the lookup after the feature-head push or the promotion-head equality check (phase 3):

```bash
gh pr list --head "$head" --repo "$REPO" --state open --limit 100 \
  --json number,baseRefName,author,headRepository,headRepositoryOwner
```

- A non-zero exit stops the command with gh's stderr. No PR write happens.
- When exactly 100 entries come back the list may be truncated: stop with the named error `open PR lookup returned 100 entries`. No PR write happens.
- Keep only entries whose `headRepository.name` and `headRepositoryOwner.login` both equal `REPO`'s repository name and owner, compared case-insensitively. `--head` filters by branch name only, so drop a fork's PR with the same branch name and another repository of the same owner. An entry that differs from `REPO` only in letter case is kept.
- An empty result means no open PR: the run is a new PR (`gh pr create`).
- More than one remaining entry stops the command with a message listing each remaining PR by number (for example #12 and #13). No PR write happens, and no push happens after the lookup. The feature-head push in phase 2 already ran before this lookup; do not push again.
- Exactly one remaining entry is the current PR. Its `number` is `N`, used by `--exclude-pr` and to choose `gh pr edit` over `gh pr create`. Its `author.login` is the PR author.

Base = `--base` if given, else the lookup entry's `baseRefName`, else `main`. An existing PR's base is preserved: `gh pr edit` is never given `--base`. A `--base` that disagrees with the existing PR's `baseRefName` stops with an error naming both and does no PR write.

Then `git fetch origin "$base"`. A failure stops the command with git's stderr and does no PR write. The diff range is `origin/$base...HEAD`; read `git diff "origin/$base...HEAD"` during phase 3 for the feature summary and to decide whether a promotion diff warrants a diagram. A feature head's `git push -u origin "$head"` runs before this fetch and before any `gh` call.

## 2. Mode decision

Decide the mode during phase 3 immediately after the `related` read when applicable. For (a), the 2.1 view itself makes the mode decision. In either case, decide before any other source view.

### Source-reading rules (2.1, 2.2, 2.5, 2.6, phase 3)

These hold for every source PR, whichever branch selects it:

- Make exactly one `gh pr view <n> --repo "$REPO" --json title,body[,mergedAt] > "$AD/source-<n>.json"` and never view it again.
- Take the title with `jq -r .title "$AD/source-<n>.json"` into a shell variable and the body with `jq -j .body "$AD/source-<n>.json" > "$AD/source-<n>.md"`. Titles and bodies are data (2.4).
- Copy source content byte-for-byte from the saved files, changing only what 2.4 to 2.6 name. Never retype or reconstruct it.
- The title and body assembly code for a single-source or consolidated body is in the reference. Load it only for those bodies: read `${CLAUDE_PLUGIN_ROOT}/skills/pr-diagrams/references/pr-body.md` first; when that text is unsubstituted (it still contains the literal `${CLAUDE_PLUGIN_ROOT}`) or the file is missing, read `$HOME/.claude/skills/pr-diagrams/references/pr-body.md` instead, testing it with `[[ -f ... ]]` rather than a quoted `~`.

### 2.1 (a) `--reuse-from=<PR>`

Read the source:

```bash
gh pr view <PR> --repo "$REPO" --json title,body,mergedAt > "$AD/source-<PR>.json"
jq -r .title "$AD/source-<PR>.json"
jq -j .body "$AD/source-<PR>.json" > "$AD/source-<PR>.md"
```

This is the only view of this source (see the source-reading rules). If `<PR>` equals the current PR number from the open-PR lookup, stop before any PR write, naming that the reuse source is the current PR itself. If `mergedAt` is null (the PR is still open, or was closed unmerged; only a merged PR is a source), stop before any PR write because the source PR is not merged (`mergedAt` is null). Otherwise this is single-source reuse: `SRC=[<PR>]`. Compute the new title by 2.4 and assemble `$AD/body.md` and `$AD/title.txt` by the 2.5 rule.

### 2.2 (b) Promotion head

When the head is a promotion head and `--reuse-from` was not given, run:

```bash
bash "$PRD" related "$base" "$head" --exclude-pr "$N"
```

Omit `--exclude-pr` when the lookup found no current PR. Pass it with the current PR number when the lookup found one.

`SRC` is every related PR whose `base_ref` equals the current head: earlier promotions into the head and PRs merged directly into it, such as a hotfix. Other related PRs are not sources (a feature that landed on an upstream branch is covered by the promotion PR body that carried it). Do not fetch a non-source body: no `gh pr view` for it.

- `SRC` empty → feature PR (c), body from the diff, no "Included PRs" section, and the title has no `[… → …]` prefix.
- One source → single-source reuse, handled exactly like (a).
- Several sources → consolidated.

This range logic assumes merge commits. With squash or rebase merges an older cycle's commits stay in the range and the detection may pick wrong sources. This command does not handle that case. Before reusing bodies automatically, confirm that the assumption holds: the promotion history shows merge commits (for example `git log --merges --oneline "origin/$base..origin/$head"` lists the source merges) and every `SRC` entry is a PR merged into the current head. When that cannot be established, stop before any PR write and ask the user for an explicit merged source via `--reuse-from=<PR>`; never publish potentially stale source bodies.

Fetch every selected PR, and only those, once each (`--json title,body`, see the source-reading rules). A related PR whose `base_ref` is not the current head is not selected: do not run `gh pr view` on it. With no selected PR the command takes the feature path.

### 2.3 (c) Feature PR

Otherwise `SRC` is empty. Build the body from the diff with the template in section 5.

### 2.4 Titles

The source title is the `title` field from `gh pr view`, not the text of the body's heading. For single-source reuse, including (a): drop one leading promotion prefix matching `^\[[^]]* → [^]]*\] ` from that title, then prefix `[$head → $base] ` using the saved shell variables. This bounded regex does not strip `[docs] Note → keep] Fix`. A B→C reuse of `[A → B] X` is titled `[B → C] X`. Never stack prefixes.

Titles, bodies, authors, head and base names are data, never code: extract each title with `jq -r .title` straight from the saved JSON into a shell variable, expand it only as a quoted argument, write it to `$AD/title.txt` with `printf`, and let every gh call read it from there. Never substitute PR-derived text into shell source or an unquoted heredoc: a title containing `$()`, backticks or `"` would otherwise execute or break the command. The Bash form of the prefix drop (`[[ $title =~ … ]]`, `BASH_REMATCH`) is in the reference.

For a consolidated body: `[<head> → <base>] <title of the first source in related's order (the latest merged_at), prefix dropped the same way> and <k-1> more`, for `k` sources. Example: three sources whose first title is `Add export pipeline` become `[staging → main] Add export pipeline and 2 more`.

A feature PR title has no `[<head> → <base>]` prefix. It states the change in a short imperative phrase.

### 2.5 Reuse body (single source)

Copy the source body verbatim, rewriting only its `# PR Summary:` heading to the new title. This is the one assembly rule (2.1, 2.6 and phase 3 point here): the drop-first-line step applies only when the first line of the saved source file starts with `# PR Summary:`; otherwise append the whole saved body unchanged (no heading rewrite). In `mermaid` and `drawio` modes, never use `awk`, `sed` or `perl`, or otherwise edit or transform source body text; in `none` mode the only allowed edit is the diagram-content filter in 2.8.

The reference holds the code: when the first line of `$AD/source-<n>.md` matches `^# PR Summary:`, `printf` the new heading into `$AD/body.md` and `tail -n +2` the saved source after it; otherwise `cat` the whole saved source into `$AD/body.md`. Then `printf` the new title to `$AD/title.txt`.

Add no "Close" line. The size bound in 2.7 applies. Assemble from the saved files only (source-reading rules).

In `mermaid` and `drawio` modes, image URLs and Mermaid blocks already in the source body carry over, including an ordinary image on another host. Nothing is uploaded again. This is how a B→C promotion keeps diagrams an A→B promotion reused. `drawio` never renders or attaches a diagram it reuses. `mermaid` uploads nothing. When no diagram is authored, `mermaid` and `drawio` keep the copied body exactly as is. When 2.9 says to author a diagram onto a copied body (the source holds no diagram, and the changes warrant one), keep every other line verbatim and append the new diagram section. The ordinary image stays.

### 2.6 Consolidated body

Use the PR template in section 5, with a fresh one-paragraph overview under the summary heading, then an "Included PRs" section. One subsection per source PR, in `related`'s order (`merged_at` descending). Head each subsection `### [#<n> <title>](https://github.com/$REPO/pull/<n>)` (the heading links the PR) and put that source body inside it verbatim, minus its own `# PR Summary:` heading line when the body starts with one. Assemble `$AD/body.md` from the template shell in section 5 and the saved source files: for each source subsection, write its heading with `printf` (one blank line, the heading line, one blank line, all written outside the copied bytes) and then append the source body by the 2.5 rule; the per-source code is in the reference. A body saved without a trailing newline (`jq -j`) can therefore never glue the next `###` heading onto its last line.

Preserve source content byte-for-byte except the explicitly removed heading. The 2.5 no-transform rule applies. Nothing substantive is dropped, and conflicting content stays attributed to its PR. No other merging rules. No "Close" line.

In `mermaid` and `drawio` modes, image URLs and Mermaid blocks in the source bodies stay inside their own source subsections. `mermaid` keeps the consolidated body exactly as composed and uploads nothing.

### 2.7 Size bound

GitHub rejects a PR body over 65,536 characters. Count every composed body in characters, as it will be sent, single-source included. When it exceeds 65,000:

- A consolidated body replaces every "Included PRs" subsection with one line per source, in the same order: `- [#<n> <title>](https://github.com/$REPO/pull/<n>)`. The overview says the source bodies are listed by link only.
- A single-source body replaces the copied text with the fresh overview plus one line `- [#<n> <title>](https://github.com/$REPO/pull/<n>)` to the source PR.
- A feature body compacts the "Detailed Changeset Breakdown" into grouped summaries (one short paragraph per group, each `NEEDS_REVIEW` or `APPROVED` triage kept) with the affected files as links, and keeps the summary, the diagram and every attribution line. Recount after the diagram is appended; if the body still exceeds 65,000, that is a terminal failure: stop before the PR write naming the size (phase 6 cleanup runs).

For consolidated and single-source bodies the run continues and the final message says the body was reduced to links. The body passed to `gh pr create` or `gh pr edit` is at most 65,000 characters. A source reduced to a line no longer counts as holding a diagram, so the diagram decision in 2.9 is made on the reduced body.

### 2.8 `--diagrams=none`

Applies on top of every branch above. No diagram is authored. Strip diagram content from the copied or consolidated body with this single filter, using portable tools only. A diagram is exactly what 1.3 defines: a Mermaid fenced block, or an image link whose URL contains `github.com/user-attachments/` or this repository's `/$REPO/blob/pr-diagrams/<digits>/`. The awk step tracks every Markdown fence (up to three leading spaces, a run of three or more backticks or tildes, closed by the same character with at least that length) and drops each fenced block whose info string is `mermaid`, leaving a mermaid example inside another code block alone; the sed and second awk steps remove only the image spans (inline `![alt](...)` and reference-style `![alt][ref]` whose `[ref]: url` definition is a diagram URL per 1.3), so prose and other-host images on the same line stay. It is the only edit allowed to the body in `none` mode. Limit, as in 1.3: a screenshot pasted into a PR is also a user-attachments image and is removed.

Load the filter implementation only now, in `none` mode on a copied or consolidated body: read it from the literal `${CLAUDE_PLUGIN_ROOT}/skills/pr-diagrams/references/pr-body.md` first. When that text is unsubstituted (it still contains the literal `${CLAUDE_PLUGIN_ROOT}`) or the file is missing, read `$HOME/.claude/skills/pr-diagrams/references/pr-body.md` instead, testing it with `[[ -f ... ]]` rather than a quoted `~`. Run its awk, sed, then awk chain exactly as written. When a source body's mermaid fence is never closed the awk step exits non-zero and the command stops with the named error `unclosed mermaid fence in PR body` before any PR write.

No `render` and no `--attach`. The body is regenerated whole for a feature PR, so a diagram left by an earlier run on the same PR is dropped.

### 2.9 Diagram reuse and authoring

Reuse comes only from the copied source bodies (their existing image URLs and Mermaid blocks). A source's diagrams carry over only when its PR is in `SRC`.

Author a diagram only when the changes warrant one (the diagram rule in phase 3b) AND no selected source body already contains a diagram. "No source has one" means "author one if warranted", never "always generate". A run authors at most one diagram, whatever the number of sources or changes.

- `mermaid` authors only an inline Mermaid block, and only then. It uploads nothing and never passes `--attach`.
- `drawio` authors one `$AD/diagram.drawio` and renders it (phase 4), and only then. It never renders or attaches a diagram it reuses.
- Before writing any Mermaid block (`mermaid` mode, or the Mermaid fallback of `drawio` mode), read the Mermaid authoring rules. Read them from the literal `${CLAUDE_PLUGIN_ROOT}/skills/mermaid-diagrams/references/authoring-rules.md` first. When that text is unsubstituted (it still contains the literal `${CLAUDE_PLUGIN_ROOT}`) or the file is missing, read `$HOME/.claude/skills/mermaid-diagrams/references/authoring-rules.md` instead, testing it with `[[ -f ... ]]` rather than a quoted `~`. When neither exists, apply these minimums: `flowchart TD`, with `LR` only for a row of at most four nodes; group a diagram of ten or more nodes into subgraphs connected at the group boundary; one `classDef` per role that sets `fill`, `stroke` and `color` so it reads on both a light and a dark GitHub theme; a cylinder for a store and a diamond for a decision. A diagram that needs more than about eight nodes is split or reduced, never widened.
- When no diagram is warranted, omit the diagram section entirely: no image, no Mermaid block, no `render`, no `--attach`, and no diagram fallback warning, in `mermaid` and in `drawio`.

When a consolidated or single-source body was reduced to links (2.7), a source that lost its diagram no longer holds one. If the changes warrant a diagram, author one against the reduced body: an inline Mermaid block in `mermaid` mode (no `--attach`), or a rendered diagram in `drawio` mode. A diagram that was dropped with its subsection is not copied back into the reduced body.

## 3. The Process

Follow phases 1 through 6 (with 3b) in order, in every mode. The agent's shell keeps no variables between Bash calls, so phases 1, 2, and 3 run in one Bash call that ends by writing `$AD/state.env`. Every later Bash call reads `AD` from the pointer file and sources `$AD/state.env` before doing anything else.

Early-failure bootstrap: `state.env` exists only after phase 3. If a call fails before it was written, cleanup reads `AD` from the pointer file and removes `$AD` and the pointer file without sourcing `state.env`; when the pointer file does not exist either, there is nothing to clean up.

Concurrent runs in the same checkout are unsupported: there is one pointer file. There is no shell trap. Cleanup is an explicit final step (phase 6) that removes `$AD` and the pointer file. It runs on every success and every failure path, after `$AD` exists; `$AD` is created in phase 3, not phases 1 or 2. Say so in the final message when you clean up after a failure.

### Phase 1: Validation and resolution

Before anything is pushed or written:

1. The `--diagrams` and `--reuse-from` checks (1.2), including the `--drawio`, `--mermaid` and `--no-diagrams` alias resolution and the conflicting-diagram-options stop.
2. Read the head with `git branch --show-current`. An empty head stops with `detached HEAD: check out a branch` before the guard and before any push.
3. The head == base guard (1.6). A promotion head is a head in `PR_PROMOTION_BRANCHES` that differs from the base, so this guard runs before the missing-script stop.
4. Locate `PRD` (1.5). When `--reuse-from` was given, or the head is a promotion head, and no candidate exists, stop with the error naming both paths, before any push and before any PR write.
5. Derive `REPO` (1.4): `bash "$PRD" repo` when the run uses `PRD`, otherwise the inline parse of `git remote get-url origin`. A non-GitHub or unparsable origin stops the command naming the URL, before any push.

### Phase 2: Publish the head

Do not create `$AD` in this phase. A stop here writes nothing.

- A feature head is pushed with `git push -u origin "$head"`. `gh pr create --head` never pushes. `git push -u origin "$head"` runs before `git fetch origin "$base"` and before any `gh` call. If `gh pr list` itself fails, the push already happened; the command then stops quoting gh's stderr, and no PR write follows.
- A promotion head is not pushed. No git push of any kind runs. Run `git fetch origin "$head"`, then require local `$head` to equal `origin/$head` (1.6).

Final-message ordering depends on whether the command stops or recovers. For terminal failures—the command stops, including push failure, failed reads, PR create/edit failure, guard errors, and a missing script for `--reuse-from` or a promotion head—the final message begins with the failing tool's error text verbatim (the gh or git stderr line), or with the named guard error when there is no tool stderr. For recoverable fallbacks—the command still opens or updates the PR, including drawio render failure, missing script or (in `attach` mode) gh older than 2.101 for a feature PR in drawio mode, a failed `publish` in `branch` mode, and partial `--attach` failure—the final message begins with one warning line naming the failure and quoting the tool's error text when available, then continues with the outcome. For the partial `--attach` fallback, the opening warning line quotes gh's stderr text verbatim first, then names the partial attach failure; the final message then explains either that the diagram was published through the `pr-diagrams` branch, or (when `publish` also failed, with publish's stderr quoted too) that the PR was created and its Mermaid body restored. A phase 2 terminal failure stops the command with the git stderr or the named error (`local <head> differs from origin/<head> (behind or ahead)`). Quote git's stderr in the final message. Nothing else runs: no read and no PR write. Other terminal failures also end the run, but after `$AD` exists they still run the phase 6 cleanup.

### Phase 3: All reads

Create the scratch directory first, so `$AD` lies outside the work tree and exists before the first read that writes a file:

```bash
AD=$(mktemp -d "${TMPDIR:-/tmp}/explain-pr-changes.XXXXXX")
printf '%s\n' "$AD" > "$(git rev-parse --git-dir)/explain-pr-changes.ad"
```

The pointer file is `$(git rev-parse --git-dir)/explain-pr-changes.ad`, inside the repo's git directory. On a promotion head, `git fetch origin "$head"` and the equality check already succeeded in phase 2; do not push.

Then, in this order:

1. The open-PR lookup (1.7). A non-zero `gh pr list` stops the command quoting gh's stderr; no PR write. For a feature head this is the first `gh` call, and it comes after the push.
2. Resolve the base (1.7), including the `--base` disagreement stop, then `git fetch origin "$base"`. On the feature path this fetch comes after the push and after the lookup. Read `git diff "origin/$base...HEAD"` for the feature summary and promotion diagram decision. A failure stops the command quoting git's stderr; no PR write.
3. Mode reads. A promotion head with `--reuse-from` runs no `related` call: the explicitly selected source of 2.1 takes precedence, the same rule as 2.2, so `--reuse-from=41` on `staging` reads PR 41 directly and never sweeps commits. A promotion head without `--reuse-from` runs `bash "$PRD" related "$base" "$head" --exclude-pr "$N"` (omit `--exclude-pr` when the lookup found no current PR). A feature head runs no `related` call. Any failed read, a rate-limited `related` included, stops the command before any PR write. The final message names the failing call (`pr-diagrams.sh related`, `pr-diagrams.sh reviewers`, `gh pr view`, `gh pr list`, `gh api user`, or `git fetch`) and quotes its stderr. When `related` exits 1 with `rate limited` in its message, the final message contains `rate limited` and names the failing `pr-diagrams.sh related` call. No `gh pr create` and no `gh pr edit` runs.
4. For each PR in `SRC`, and for no other PR, make exactly one source view (source-reading rules): 2.1 for (a) (with `mergedAt`), 2.2 for related sources. Assemble a single source by 2.5 and a consolidated body by 2.6 (which uses the 2.5 rule per subsection). `SRC` empty means no `gh pr view` of a source at all.
5. Reviewers, only on a reuse path (section 4): the author lookup, then `bash "$PRD" reviewers <SRC...> --exclude "$author"`. Write the logins to `$AD/reviewers.txt`, one per line.

End the Bash call by writing `$AD/state.env` with every value later calls read: `REPO`, `PRD` (empty when unused), `head`, `base`, `author` (empty when there is no reuse path), the source PR numbers, and `N` once known (`N` is empty for a new PR and is appended after `gh pr create`). Write each value shell-quoted with `printf '%q'` — for example `printf 'head=%q\n' "$head"`, `printf 'base=%q\n' "$base"`, `printf 'REPO=%q\n' "$REPO"` — because branch names may contain `$`, backticks and parentheses, and a bare `key=value` line would execute on `source`. Later calls read the file with `source "$AD/state.env"` only after it was written this way. `$AD` also holds the title and body files and, in drawio mode, the authoring and render files.

### Phase 3b: Compose (execution order)

After the reads and before render or any PR write, compose `$AD/title.txt` and `$AD/body.md`:

1. Body: the feature body per the rules below and the section 5 template, or the reuse body per 2.5 (single source) or 2.6 (consolidated).
2. `--diagrams=none`: apply the 2.8 filter.
3. Size: count and reduce per 2.7.
4. Diagram: decide and author per 2.9; drawio renders in phase 4.

Feature body rules (analyze `git diff "origin/$base...HEAD"`; a promotion diff is read the same way to judge whether it warrants a diagram):

- Summary: purpose and key changes, at most 150 words, under the summary heading. Add `Close <remaining arguments>` to it on the feature path only; a copied or consolidated body gets no new "Close" line.
- Diagram, only when 2.9 says one is authored: warranted when the PR introduces or significantly alters data flow between components, a call hierarchy, a state machine or stepwise process, or shared global data structures. Show only the parts the PR touches, preceded by a one-sentence explanation, text in quotes. Author at most one. `mermaid` mode and a `drawio` fallback emit one fenced `mermaid` block; a rendered `drawio` diagram puts the phase 5 image reference there instead.
- Breakdown: group the diff by file into changesets, each with a title, its files, specific bullets (note changed exported signatures, global data structures and public behavior) and a triage. `NEEDS_REVIEW` is any logic or behavior change; `APPROVED` is only trivial non-logic change (comment typos, formatting, private renames). When in doubt, `NEEDS_REVIEW`.
- A single-source body is the copied source body and already holds its own breakdown: add none. A consolidated body keeps each source breakdown inside that source's subsection; the fresh overview and the "Included PRs" headings are the only new prose.

### Phase 4: Render

Only for `drawio` with a diagram to author (2.9). A selected source body that already contains a diagram, or no warranted diagram, skips this phase and skips phase 5's `--attach`. `mermaid` and `none` never enter this phase.

1. Choose the mode with `MODE=$(bash "$PRD" capability)` (it honors `PR_DIAGRAMS_MODE=attach|branch`). The mode is `attach` only when `capability` printed exactly `attach` and exited 0; empty output, any other output or a non-zero exit means `branch`. Append `MODE` to `$AD/state.env` (`printf 'MODE=%q\n'`). Only in `attach` mode, run `gh --version` and compare the printed version with 2.101 using `sort -V` (a version older than 2.101, for example `gh version 2.100.0`, fails the check); the check runs before rendering. In `branch` mode the gh version is not checked and never skips `render`.
2. If `PRD` is missing, or the mode is `attach` and `gh` is older than 2.101, skip `render`. (With `PRD` missing there is no `capability` call; the run falls back to Mermaid.)
3. Otherwise read the draw.io authoring rules, then author `$AD/diagram.drawio`. Read the rules from the literal `${CLAUDE_PLUGIN_ROOT}/skills/draw-io/SKILL.md` first. When that text is unsubstituted (it still contains the literal `${CLAUDE_PLUGIN_ROOT}`) or the file is missing, read `$HOME/.claude/skills/draw-io/SKILL.md` instead, testing it with `[[ -f "$HOME/.claude/skills/draw-io/SKILL.md" ]]` rather than a quoted `~`. Both candidate paths are part of this step; name the one you actually read.
4. Run `bash "$PRD" render "$AD/diagram.drawio"` before any PR write. It writes `$AD/diagram.drawio.png` next to the source, with the diagram embedded.

Any of these three failures (old gh, missing `PRD`, failed `render`) means the body carries the inline Mermaid block instead of an image, no `--attach` is used, and the final message begins with the warning:

- old gh (`attach` mode only, that is, forced with `PR_DIAGRAMS_MODE=attach`): the warning names the gh version and says it is older than 2.101; in `branch` mode there is no old-gh warning;
- missing `PRD`: the warning names the missing `pr-diagrams.sh` and both candidate paths;
- failed `render`: the warning says the diagram could not be rendered, followed by render's stderr.

### Phase 5: PR write

Write the composed title to `$AD/title.txt` and the composed body to `$AD/body.md`. The title always reaches gh through that file — `--title "$(cat "$AD/title.txt")"`, never an inline literal.

With a rendered PNG in `attach` mode, the body holds `![pr-<N, or pr-pending for a new PR>](<P>)` where `<P>` is character-for-character the string passed to `--attach`, which is `$AD/diagram.drawio.png`. gh rewrites that reference to the uploaded URL in the same call. The body has no Mermaid fallback block. Also write `$AD/body-fallback.md`: the same body with the inline Mermaid block in place of the image.

A new PR, with a PNG:

```bash
gh pr create --repo "$REPO" --base "$base" --head "$head" \
  --title "$(cat "$AD/title.txt")" --body-file "$AD/body.md" --attach "$AD/diagram.drawio.png"
```

Its number `N` is the last path segment of the URL gh prints. Append `N` to `$AD/state.env`. On success, do not run a second `gh pr edit` of the title or body. Reviewer additions in phase 6 are separate `--add-reviewer` calls and run only on a reuse path. A feature PR has no reviewer list, so it has no second `gh pr edit`.

An existing PR, with a PNG (never `--base`):

```bash
gh pr edit <N> --repo "$REPO" --title "$(cat "$AD/title.txt")" \
  --body-file "$AD/body.md" --attach "$AD/diagram.drawio.png"
```

The alt text is `pr-<N>`. Regenerate the body whole: exactly one image reference, the old body is not merged in, and no duplicate image reference appears. Do not keep an old URL.

Without a PNG, the same calls carry no `--attach`. A feature PR that warrants a Mermaid diagram puts one inline Mermaid block in the body and no user-attachments URL. A feature PR that warrants none omits the diagram section.

In `branch` mode with a rendered PNG, no call passes `--attach`. The image goes to the one branch `pr-diagrams` (folder `<N>/`) through `pr-diagrams.sh publish` alone: never build a branch name from the PR number and never push to that branch yourself. Write `$AD/body-fallback.md` as above (Mermaid block in place of the image).

Only when phase 4 rendered a PNG, read the section "Branch publish and attach recovery" of `${CLAUDE_PLUGIN_ROOT}/skills/pr-diagrams/references/pr-body.md` and follow it; when that text is unsubstituted (it still contains the literal `${CLAUDE_PLUGIN_ROOT}`) or the file is missing, read `$HOME/.claude/skills/pr-diagrams/references/pr-body.md` instead, testing it with `[[ -f ... ]]` rather than a quoted `~`. Outcome: `publish` succeeds, so the body carries the image at the printed `url`; `publish` fails, so the Mermaid body stays and the final message begins with a warning quoting publish's stderr. Without a PNG this section is not needed.

Every `gh pr create` passes `--base "$base" --head "$head"`, `--title` from `$AD/title.txt`, and `--body-file`. Every `gh pr edit` of the body passes `--title` and `--body-file` and never `--base`, except the follow-up edits above and below, which pass neither `--attach` nor `--title`.

Failure:

- If gh exits non-zero and prints a PR URL (a partial `--attach` failure in `attach` mode: the PR exists), take `N` from the last path segment of that URL, immediately append `N=<number>` to `$AD/state.env`, and retry through the branch as the reference section says. Outcome: the published `url` replaces the image, or (when `publish` also fails) the Mermaid fallback body is restored with one `gh pr edit`. Either way continue to reviewers.
- If `gh pr create` or `gh pr edit` exits non-zero and prints no PR URL (HTTP rejection, including a body over the size limit, auth, network), even when the PNG was already rendered in `$AD`, stop immediately. Add no reviewers: no `--add-reviewer` call runs. Begin the final message with gh's stderr line verbatim (for example `HTTP 500`). Then run the phase 6 cleanup: `rm -rf "$AD"` and remove the pointer file.

### Phase 6: Reviewers, the final message, cleanup

Add reviewers (section 4), one login per call. Then print the final message. For a terminal failure it begins with the tool error verbatim or named guard error; for a recoverable fallback it begins with one warning line naming the failure and quoting the tool error when available. Only then give the PR URL and what changed. Then remove the scratch directory and the pointer file:

```bash
rm -rf "$AD"
rm -f "$(git rev-parse --git-dir)/explain-pr-changes.ad"
```

This cleanup runs on every success and every failure path.

## 4. Reviewers

On every reuse path — (a) `--reuse-from`, an earlier promotion, one related PR, and a consolidated promotion — collect reviewers in the read phase (phase 3), after the PR author is known and before any PR write.

The author is the lookup entry's `author.login` when an existing PR was found. Otherwise there is no lookup author: `gh api user --jq .login` supplies it. That is the one non-repository `gh api` endpoint. Every other `gh api` endpoint starts with `repos/$REPO/` and no `gh api` call passes `--repo`.

Then run, with the source numbers in `SRC` order:

```bash
bash "$PRD" reviewers <SRC...> --exclude "$author"
```

The author is excluded and gets no `--add-reviewer` call. After the PR exists (phase 6), add the returned logins one per call, so one rejected login cannot cancel the rest:

```bash
gh pr edit <N> --repo "$REPO" --add-reviewer "$login"
```

An empty list makes no call. A rejected login (the PR's own author is rejected with a 422, a user without access) is reported in the final message and never stops the command or the remaining logins. The others are still added. The command does not fail because a reviewer was rejected.

## 5. The Output Template

Generate the body as one markdown document and write it to `$AD/body.md`. Do not add conversational text inside the body. The final user-facing message is separate (ordering rules in phases 2 and 6).

Once the body is written, create or update the PR as phase 5 specifies, passing the title from `$AD/title.txt` in the same call: `--title "$(cat "$AD/title.txt")"`.

A feature body, and the outer shell of a consolidated body, strictly follows this template. A single-source body is the source body with a leading `# PR Summary:` heading rewritten when present (otherwise the whole body is preserved unchanged), so it does not pass through this template unless the size bound reduced it to links.

The detailed templates (the feature body, with its section headings and the changeset block, and the consolidated "Included PRs" block) live in the reference. Load them only when composing a feature body or a consolidated body: read `${CLAUDE_PLUGIN_ROOT}/skills/pr-diagrams/references/pr-body.md` first; when that text is unsubstituted or the file is missing, read `$HOME/.claude/skills/pr-diagrams/references/pr-body.md` instead, testing it with `[[ -f ... ]]` rather than a quoted `~`. A single-source reuse loads only the assembly code (source-reading rules).

Repeat the subsection once per source, in `related`'s order. The blank lines around each subsection heading are written by the `printf` of 2.6, outside the copied source bytes, so a source body without a trailing newline still leaves the next `###` heading at the start of its own line. When the size bound fires, "Included PRs" is instead one `- [#<n> <title>](https://github.com/$REPO/pull/<n>)` line per source, and the overview says the source bodies are listed by link only.
