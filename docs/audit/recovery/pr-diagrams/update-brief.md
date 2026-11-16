# pr-diagrams: fix list for the update brief (2026-11-15)

Every item below was verified by reading the file and by a read-only run (no PR write, no network write). Line numbers are in the tree at d7a61091. The artifact was not edited. Facts and sources are in `facts.md` and `sources.md`.

## (a) `capability`: exit code and the `--attach` floor

Verified runs (stub `GH`, `bash skills/pr-diagrams/scripts/pr-diagrams.sh capability`):

| input | stdout | stderr | exit |
| --- | --- | --- | --- |
| `capability extra` | empty | `pr-diagrams: usage: pr-diagrams.sh capability` | 2 |
| `PR_DIAGRAMS_MODE=bogus` | empty | `PR_DIAGRAMS_MODE must be attach or branch, got: bogus` | 2 |
| stub gh 2.99.0 | `branch` | `gh 2.99 has no --attach, using branch` | 0 |
| stub gh 2.100.0 | `branch` | `gh 2.100 has no --attach, using branch` | 0 |
| stub gh 2.101.0 | `attach` | none | 0 |

Real history (`gh api repos/cli/cli/releases/tags/<tag>`): `gh pr create --attach` and `gh pr edit --attach` first shipped in v2.99.0 (2026-09-01); v2.100.0 and v2.101.0 add only attachment telemetry. The code in v2.99.0 already matches references by absolute path and caps 50 files, the same as v2.101.0. So the message is false for 2.99 and 2.100 and true only below 2.99.

Edits (one decision first, see the end of this section):

1. `scripts/pr-diagrams.sh` help line 346: `capability   print attach or branch; exit 0 for every probe outcome, 2 for a usage error (stray argument or invalid PR_DIAGRAMS_MODE)`. The `exit:` help lines (356-357) already say exit 2 covers a usage error of `capability`; keep them.
2. `skills/pr-diagrams/SKILL.md` line 29: replace "It always exits 0" with "It exits 0 for every probe outcome and 2 only for a usage error (a stray argument or an invalid `PR_DIAGRAMS_MODE`)".
3. `README.md` line 23: replace "`capability` always exits 0 and prints" with "`capability` prints"; the same paragraph already says "another value exits 2", so add "a stray argument also exits 2" and "every probe outcome exits 0".
4. Message at `scripts/pr-diagrams.sh` line 272, depending on the decision below.
5. Tests: `test_capability_rule` (lines 588-589, 596) asserts `2.100.0 -> branch`; update with the decision. Add a `capability extra` case to `test_capability_probe_failures_print_branch` (exit 2, empty stdout). Evals: `evals/files/ghe-gh-version.txt` uses gh 2.98.0, which stays `branch` under either decision; `evals/evals.json` (2 mentions of 2.101) and `evals/trigger-queries.json` (1) follow the decision.

Decision for the controller (the floor appears in SKILL.md description and step 1, README.md (5), the script, tests, evals, and `commands/explain-pr-changes.md` (4) with 14 mentions in `commands/evals/explain-pr-changes.json`):

- Option A (recommended): lower the floor to gh 2.99 (`-lt 99`), message `gh X.Y predates --attach (added in 2.99), using branch`. It matches the vendor release notes. Cost: command, evals and tests change together; behavior of 2.99 and 2.100 was not run live, only their source and release notes were read.
- Option B: keep 2.101 as the project's tested floor and make the message true: `gh X.Y is older than 2.101, the tested floor for --attach, using branch`, and say "tested floor" instead of "has no --attach" everywhere. No behavior change.

## (b) none-mode filter strips an ordinary inline image

Confirmed with the real chain: `references/pr-body.md` first ````bash block, run on the fixture below with `AD` set to a scratch directory and `REPO=owner/repo`. Current output turns `![diagram](https://example.com/shots/ui.png)` into `(https://example.com/shots/ui.png)`: the final awk matches `![diagram]`, sees label `diagram` in the diagram-label set (collected from `[diagram]: https://github.com/user-attachments/...`) and drops it, leaving the URL suffix.

Fix (one added test in the final awk loop, line 34-41 of the file; the sed step before it already removed inline diagram images, so any inline image still present there is ordinary):

```awk
  while (match(rest, /!\[[^]]*\](\[[^]]*\])?/)) {
    t = substr(rest, RSTART, RLENGTH); lab = t; sub(/^!\[/, "", lab)
    if (lab ~ /\]\[/) { alt = lab; sub(/\]\[.*$/, "", alt); sub(/^.*\]\[/, "", lab); sub(/\]$/, "", lab); if (lab == "") lab = alt }
    else sub(/\]$/, "", lab)
    inl = (t !~ /^!\[[^]]*\]\[/) && substr(rest, RSTART + RLENGTH, 1) == "("
    out = out substr(rest, 1, RSTART - 1)
    if (inl || !(norm(lab) in att)) out = out t
    rest = substr(rest, RSTART + RLENGTH)
  }
```

`inl` is true only for `![alt](...)`: no second bracket group and `(` right after the closing `]`. Reference images (`![alt][label]`, `![alt][]`, `![label]`) still resolve through the label set. Also update the prose under the block: "The last awk step ... keeps an inline image (`![alt](url)`, already handled by the sed step) even when its alt text equals a diagram label." Verified with the patched chain (scratch copy `tmp/pd-filter-fixed.sh`): output below.

Fixture `tests/skills/pr-diagrams/fixtures/none-filter-body.md`:

```markdown
# PR Summary: Add the flow

Real diagram: ![diagram][diagram]

Ordinary screenshot, alt equals a diagram label: ![diagram](https://example.com/shots/ui.png)

Collapsed reference to the diagram: ![diagram][]

Another ordinary image with a different alt: ![ui](https://example.com/shots/ui2.png "title")

[diagram]: https://github.com/user-attachments/assets/11111111-2222-3333-4444-555555555555
```

Expected `tests/skills/pr-diagrams/fixtures/none-filter-body.expected.md` (the two reference images vanish and leave their trailing space; the inline images and the definition stay):

```markdown
# PR Summary: Add the flow

Real diagram: 

Ordinary screenshot, alt equals a diagram label: ![diagram](https://example.com/shots/ui.png)

Collapsed reference to the diagram: 

Another ordinary image with a different alt: ![ui](https://example.com/shots/ui2.png "title")

[diagram]: https://github.com/user-attachments/assets/11111111-2222-3333-4444-555555555555
```

Test (heredoc-free; extracts the first fenced block of pr-body.md so the test cannot drift from the documented code):

```bash
test_none_filter_keeps_ordinary_inline_image() {
  local ad; ad=$(mktemp -d); TMPS+=("$ad")
  sed -n '/^````bash$/,/^````$/p' "$HERE/../../../skills/pr-diagrams/references/pr-body.md" | sed '1d;$d' > "$ad/filter.sh"
  cp "$HERE/fixtures/none-filter-body.md" "$ad/body.md"
  AD="$ad" REPO=owner/repo bash "$ad/filter.sh"
  check filter_exit "$?" 0
  check filtered "$(cat "$ad/body.md")" "$(cat "$HERE/fixtures/none-filter-body.expected.md")"
}
```

Run the same test against the unpatched block first: it must fail on the `ui.png` line (it prints `(https://example.com/shots/ui.png)`).

Related, lower severity (reading only): the sed and awk steps also strip diagram image syntax inside non-mermaid fenced code blocks and inline code spans, where gh itself leaves code alone (gh source: "A path inside a code fence or an inline code span is left alone"). A PR body that quotes `![x](https://github.com/user-attachments/assets/1)` in a code sample loses it in none mode. Either note the limit in pr-body.md or skip fenced lines in the sed step (reuse the fence state of the first awk).

## (c) Other findings

1. Attach path rule is overstated (facts.md): gh matches the absolute path, not the string. SKILL.md Gotchas and step 4: keep "use the identical string" as the safe rule, drop "gh rewrites only a reference that matches the argument exactly" and the `./x.png` versus `/tmp/ad/x.png` example, and add: pass an absolute path (`realpath "$PNG"`) both to `--attach` and in the body; on gh >= 2.103 a relative reference is resolved in the body file's directory first.
2. Failure with no PR URL is not covered: when no attachment uploads, `gh pr create` creates no PR (gh source: "no pull request was created") and prints no URL. Add to SKILL.md Failures: no URL on stdout means no PR exists; quote stderr; for a new PR follow the branch path (create with `body-fallback.md`, `publish`, one `gh pr edit`); for `gh pr edit` keep the old body. Likely causes (pointer, live stderr is authoritative): a token type that cannot attach (for example an Actions `GITHUB_TOKEN`), no write access, a file over the image size limit.
3. `render` has no size check. The 2x draw.io PNG can exceed GitHub's 10 MB image limit (changelog). Either add a note under Rendering ("a PNG over the host's image limit fails the upload with no PR created; render smaller or use branch mode") or a warning on stderr when the PNG exceeds 10 MB (`[ "$(wc -c < "$png")" -gt 10485760 ]`). Do not write the number as a promise: it is a pointer to the changelog.
4. `git ls-remote --heads` in `cmd_publish` (two calls) is deprecated since git 2.46: use `git ls-remote origin 'refs/heads/pr-diagrams-*' 'refs/heads/pr-diagrams/*'` and `git ls-remote origin refs/heads/pr-diagrams`, with no flag. The first call currently pipes through `sed 's|.*refs/heads/||'`, which keeps working.
5. README line 25 and SKILL.md Gotchas call the `publish` URL "unverified for private repositories": GitHub Docs documents the relative `blob/...?raw=true` form for images in PRs, working in a private repository for a viewer with read access. Reword to "documented on github.com for the relative form; the absolute form and GHE are unverified; open the PR and check".
6. The existing test file uses heredocs (`cat > "$root/bin/gh" << 'EOF'` at line 55 and `cat > "$path" << EOF` at line 84), which the user's shell rules forbid in scripts. Replace with `printf '%s\n' ...` lines or committed fixture files (the cap stub already lives in `fixtures/gh-cap-stub.sh`).
7. Credits and registry: add the README Credits paragraph and the 15 proposed rows from `sources.md`. The controller adds the rows to `docs/audit/upstream-sources.json` (this analyst may not); the credit text must appear verbatim in the skill's README or references or `check --strict` fails with `missing_credit`.
8. The 65,536-character PR body limit: pr-diagrams itself states none; keep it that way. If a restored section needs a bound, point to the sibling command's 65,000 composition bound and the live 422 text; facts.md records that no official page states the limit.
