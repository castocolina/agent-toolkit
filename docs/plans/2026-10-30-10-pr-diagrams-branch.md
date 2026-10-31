# Plan 10 — pr-diagrams Single-Branch Fallback and CI Triggers

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Diagrams can be published for a PR on servers whose `gh` does not support `--attach` (some GitHub Enterprise instances), through ONE branch named exactly `pr-diagrams` holding one folder per PR number; agents cannot create `pr-diagrams/<N>`-style branches by mistake; and the deterministic CI checks run on every PR regardless of its base branch.

**Architecture:** `pr-diagrams.sh` gains `capability` (prints `attach` or `branch`) and `publish` (commits PNGs to `pr-diagrams` under `<N>/` using a throwaway worktree, never force-pushes, prints image URLs). `explain-pr-changes` picks the mode from `capability`; in `attach` mode a partial `--attach` failure (the PR exists) is retried through `publish` before the Mermaid body is restored, and in `branch` mode the gh version no longer skips `render`. The skill states the branch rule first, with a wrong/right table, and evals pin it. `main.yaml` drops its base-branch filter.

**Tech Stack:** Bash, git, gh, `skills/pr-diagrams`, `commands/explain-pr-changes.md`, `.github/workflows/main.yaml`.

**Spec:** the user's original request (2026-10-30): one branch `pr-diagrams` with folders named by PR number, because some GHE instances lack `gh --attach`; agents previously created `pr-diagrams/N` branches and multiplied them; the server may later gain `--attach`, so the mode is re-checked each run. [Known issues](2026-10-30-00-known-issues.md) section 7; Roadmap Global Constraints apply.

Branch: `feat/<yy-mm-dd>-pr-diagrams-branch`. Depends on plan 8 Task 4 merged (it edits the same command file); rebase onto it.

## Global Constraints

- Exactly one branch name: `pr-diagrams`. No `pr-diagrams/<N>`, `pr-diagrams-<N>` or any other `pr-diagrams*` ref, local or remote. A git ref cannot be both `pr-diagrams` and `pr-diagrams/x`, so the script also fails loudly when it finds one.
- Files live at `<N>/<name>.png` on that branch; the branch is an orphan that holds only such folders.
- Never force-push `pr-diagrams`; publish by fast-forward commits only.
- `attach` stays the default on github.com when `gh` is 2.101 or newer; `branch` is the default on any other host, and either can be forced with `PR_DIAGRAMS_MODE=attach|branch`.
- **Host rule** (defined only here): take the URL `gh repo view --json url --jq .url` prints, drop the `scheme://` prefix, keep the text up to the first `/` and lowercase it; the repository is on github.com iff that text equals `github.com` exactly. `https://github.com/o/r` and `https://GitHub.com/o/r/` are github.com; `https://github.company.com/o/r`, `https://ghe.example.com/o/r`, `https://github.com.evil.example/o/r`, `https://www.github.com/o/r` and `https://github.com:8443/o/r` are not; empty output, `github.com/o/r` (no scheme) and `https:///o/r` have no host. Ruling: exact equality, because any Enterprise host may lack `--attach` and `branch` is the safe side.
- The command stays source-agnostic about diagram content (plan 8 Task 4 rules unchanged).
- This plan reverses Decision 12 of the 2026-10-24 roadmap ("there is no `pr-diagrams` branch") for servers without `--attach`; Task 0 records it there.

## Review Focus

1. An agent creates `pr-diagrams/<N>` or `pr-diagrams-<N>` → the SKILL.md opening states the single name with a wrong/right table; `publish` takes the PR number as a path argument only and never as a branch component; a stray ref makes `publish` exit 2 naming it. Pinned in Tasks 1 and 2.
2. `publish` rewrites history of the shared branch → fast-forward only; a non-fast-forward push is retried once after `git fetch`, then fails. Pinned in Task 1.
3. A GHE server upgrade adds `--attach` but the skill keeps using the branch → mode is computed on every run, `PR_DIAGRAMS_MODE=attach` forces it, and a partial `--attach` failure retries through `publish` before the Mermaid fallback. Pinned in Tasks 1 and 3.
4. The PR number is unknown for a new PR → create the PR without the image, publish under the returned number, then edit the body. Pinned in Task 3.
5. CI never runs on stacked PRs → `pull_request` has no base filter. Pinned in Task 4.

---

### Task 0: Record the reversal of Decision 12

**Files:** Modify `docs/plans/2026-10-24-00-roadmap.md` (Decision 12 and the PLAN 3 line that says images go "never to a branch").

- [ ] **Step 1:** Edit Decision 12's closing clause "there is no `pr-diagrams` branch" to say that `attach` stays the default where `gh` supports it and ONE branch `pr-diagrams` (folders `<N>/`) is the fallback elsewhere (plan 10, user request 2026-10-30), and the PLAN 3 line "never to a branch (Decision 12, revised after the spike)" to "to a branch only as the plan 10 fallback". Verify `rg -n 'no .pr-diagrams. branch|never to a branch' docs/plans/2026-10-24-00-roadmap.md` prints nothing.
- [ ] **Step 2:** Commit `docs(plan): record the pr-diagrams single-branch fallback`.

### Task 1: `capability` and `publish` in `pr-diagrams.sh`

**Files:**
- Modify: `skills/pr-diagrams/scripts/pr-diagrams.sh`, `tests/skills/pr-diagrams/test-pr-diagrams.sh`
- Create: `tests/skills/pr-diagrams/fixtures/png-1x1.png` if absent

**Interfaces:**
- Produces: `pr-diagrams.sh capability` prints `attach` or `branch` on stdout (rule in Global Constraints; reads `gh --version` and the host of `gh repo view --json url` per the Host rule, each probe under `timeout 10`; a stub `gh` on `PATH` drives the tests). Failure contract: `capability` always prints exactly one of `attach` or `branch` and exits 0. When either probe fails, times out, prints a `gh --version` it cannot parse, or prints a URL with no host, it prints `branch` and writes the reason on stderr. Ruling: `branch`, because it needs no `gh` feature beyond what the probes could not confirm and a failed `publish` still falls back to the Mermaid body, whereas a wrong `attach` fails the PR step. An invalid `PR_DIAGRAMS_MODE` value (anything but `attach` or `branch`) exits 2 with a usage line and prints nothing on stdout. `pr-diagrams.sh publish <N> <png>...` (N is digits only, else exit 2): fetches `origin pr-diagrams` (absent means create the orphan), copies each PNG to `<N>/<basename>` in a temporary worktree, commits `docs: diagrams for PR <N>`, pushes `HEAD:refs/heads/pr-diagrams` without force, removes the worktree, and prints one `{png, url}` JSON line per file where `url` is `https://<host>/<owner>/<repo>/blob/pr-diagrams/<N>/<basename>?raw=true` (UNVERIFIED for private repositories and GHE; the spike in Step 6 decides).

- [ ] **Step 1: Failing tests** against a local bare repository used as `origin`: (a) `capability` prints `attach` for a stub `gh version 2.101.0` on github.com, `branch` for `2.100.0`, with `gh` 2.101.0 `attach` for the two github.com URLs of the Host rule and `branch` for its five other hosts, and honors `PR_DIAGRAMS_MODE`; with a stub `gh` that exits non-zero, one that hangs past the timeout (the stub sleeps; run the test with the probe timeout lowered through `PR_DIAGRAMS_PROBE_TIMEOUT`, default 10), one printing `gh version banana`, and `gh repo view` printing each of the Host rule's three no-host outputs, `capability` prints `branch`, exits 0 and names the reason on stderr; `PR_DIAGRAMS_MODE=bogus` exits 2 with empty stdout; (b) first `publish 12 a.png` creates the orphan branch with only `12/a.png`; (c) a second `publish 13 b.png` leaves `12/a.png` and adds `13/b.png` as a fast-forward; (d) `publish abc x.png` and `publish 12/../x y.png` exit 2; (e) with a stray remote ref `pr-diagrams-5` or `pr-diagrams/5`, or a local `pr-diagrams-5` or `pr-diagrams/5`, `publish` exits 2 and names the ref; (f) the user's working tree and current branch are unchanged afterwards; (g) a concurrent non-fast-forward push is retried once.
- [ ] **Step 2: Run** `bash tests/skills/pr-diagrams/test-pr-diagrams.sh` → FAIL.
- [ ] **Step 3: Implement** `capability` and `publish` (`set -euo pipefail`, `trap` removes the temporary worktree; add a `usage` line for both).
- [ ] **Step 4: Run** the test → PASS; `shellcheck` clean if installed.
- [ ] **Step 5: Commit** `feat(pr-diagrams): publish diagrams to the single pr-diagrams branch`.
- [ ] **Step 6 (spike, needs the user's GHE or a repository to try):** push one PNG with `publish` and confirm the URL renders in a PR body on github.com (public and private repository). Record the result in `skills/pr-diagrams/README.md`; anything not observed stays UNVERIFIED. Skip with a note when no server is available.

### Task 2: Skill rules and evals

**Files:**
- Modify: `skills/pr-diagrams/SKILL.md`, `skills/pr-diagrams/README.md`, `skills/pr-diagrams/evals/evals.json`, `skills/pr-diagrams/evals/trigger-queries.json`
- Create: `skills/pr-diagrams/evals/files/{branch-names.txt,ghe-gh-version.txt}`

**Interfaces:** Consumes Task 1. Produces the rule text and evals the command relies on.

- [ ] **Step 1: Failing evals** (add before editing): (a) the fixture `branch-names.txt` lists `pr-diagrams/41`, `pr-diagrams-41`, `pr-diagrams` and `diagrams/41`; the question asks which one an agent may create for PR 41 → assert only `pr-diagrams` (with the file under `41/`) and that the others are refused; (b) `ghe-gh-version.txt` shows `gh version 2.98.0` on a non-github.com host → assert the answer uses `publish` and the single branch, not `--attach`; (c) a prompt asking to "create a branch per PR for the diagrams" → assert the answer refuses the per-PR branch and offers the folder; (d) with `gh` 2.101+ on github.com → assert `--attach`.
- [ ] **Step 2: Run** `run-evals --skills pr-diagrams` → the new scenarios FAIL.
- [ ] **Step 3: Edit `SKILL.md`**: the first paragraph states the branch rule (exactly `pr-diagrams`, folders by PR number, never a branch per PR) and the wrong/right table (`pr-diagrams/41` wrong, `pr-diagrams-41` wrong, `pr-diagrams` + `41/diagram.png` right); add the two modes with `capability`; keep the file under 100 lines (move the URL details into `README.md`).
- [ ] **Step 4: Run** `run-evals --skills pr-diagrams --fail-under 0.9`, the same with `--triggers`, and `check --strict --skills pr-diagrams` → all exit 0; judge with two lanes to 90 or more.
- [ ] **Step 5: Commit** `feat(pr-diagrams): state the single-branch rule and pin it with evals`.

### Task 3: Command wiring

**Files:**
- Modify: `commands/explain-pr-changes.md` (Phase 4 steps 1-2 and the warning list, the Phase 5 Failure bullet for a partial `--attach` failure, the final-message ordering paragraph, and the line "There is no `pr-diagrams` branch"), `commands/evals/explain-pr-changes.json`

**Interfaces:** Consumes `pr-diagrams.sh capability|publish`. The command treats the mode as `attach` only when `capability` printed exactly `attach` and exited 0; empty output, any other output or a non-zero exit means `branch`, so Phase 5 always takes one of the two paths.

- [ ] **Step 1: Failing eval scenarios:** `branch-mode-publish` (`capability` prints `branch`, `--diagrams=drawio`, gh 2.98.0, new PR: `render` still runs, the PR is created with `$AD/body-fallback.md` and no `--attach`, then `publish <N> "$AD/diagram.drawio.png"`, then one `gh pr edit <N> --body-file "$AD/body.md"` whose image reference is the printed URL); `branch-mode-publish-fails` (the same, `publish` exits non-zero: the Mermaid body stays, the final message begins with a warning quoting publish's stderr, the command continues to reviewers); `attach-partial-failure-publish` (attach mode; `gh pr create ... --attach` exits non-zero and prints a PR URL ending in `/42`: N=42 is taken from the URL, `publish 42` runs, then one body edit with the printed URL and no Mermaid fallback edit; the final message begins with gh's stderr verbatim, names the partial attach failure and says the diagram was published through the `pr-diagrams` branch); `single-branch-name` (the command never builds a branch name from the PR number); `capability-probe-fails` (the stubbed `capability` output is empty with a non-zero exit: the command takes `branch` mode, `render` runs, the PR is created without `--attach` and `publish` is used). The existing `attach-partial-failure` scenario becomes the case where `publish` also fails: it keeps its assertions and gains "`publish 42` is attempted first" and "the warning also quotes publish's stderr". `drawio-old-gh` gains `PR_DIAGRAMS_MODE=attach` in its prompt (the old-gh skip now applies only to attach mode), and a sibling `drawio-old-gh-branch-mode` (unforced, gh 2.100.0: `capability` prints `branch`, `render` runs, no old-gh warning, `publish` is used). `attach-total-failure` and `attach-create-failure-no-url` (no PR URL: terminal) stay unchanged.
- [ ] **Step 2: Edit the command.** (1) Phase 4 step 1 runs `bash "$PRD" capability` (or honors `PR_DIAGRAMS_MODE`); the `gh --version` comparison with 2.101 applies only when the mode is `attach`. In `branch` mode the gh version no longer skips `render`, and the "old gh" warning is emitted only in `attach` mode (that is, when forced with `PR_DIAGRAMS_MODE=attach`); a missing `PRD` or a failed `render` still falls back to the inline Mermaid block in both modes. (2) Phase 5, `branch` mode: the flow `branch-mode-publish` and `branch-mode-publish-fails` pin, with `gh pr edit <N> --repo "$REPO" --body-file "$AD/body.md"` and `N=<number>` appended to `$AD/state.env` at once, as today; an existing PR runs `publish` first and edits once. (3) Phase 5, `attach` mode: only the partial `--attach` failure bullet changes, to the flow `attach-partial-failure-publish` and `attach-partial-failure` pin; a failure with no PR URL stays terminal. (4) Update the final-message ordering paragraph, and replace the line "There is no `pr-diagrams` branch" with the single-branch rule.
- [ ] **Step 3: Run** the new and re-pointed scenarios, then the command gate exactly as plan 8 Task 4 Step 4 defines it (every id in the file at run time, this task's six included; no `--triggers`, which `run-evals` rejects for a command eval file) → every scenario passes (the previous set with the re-pointed scenarios counted by their new assertions, plus the new ones).
- [ ] **Step 4: Commit** `feat(explain-pr-changes): fall back to the pr-diagrams branch without --attach`.

### Task 4: CI triggers

**Files:**
- Modify: `.github/workflows/main.yaml`
- Create: `tests/audit/test-ci-triggers.sh`

**Interfaces:** Produces: the CI workflow runs on `pull_request` for any base, on `push` to `main`, and on `workflow_dispatch`.

- [ ] **Step 1: Failing test** `test-ci-triggers.sh [FILE]` (default `.github/workflows/main.yaml`; no YAML library, so `rg` text checks): (1) `rg -q '^  pull_request:[ ]*$'` matches (block form, no inline filter); (2) `rg -U -q '^  pull_request:[ ]*\n(( {4,}.*)?\n)* {4}branches(-ignore)?:'` does NOT match (it spans only blank or deeper-indented lines under `pull_request:`, so a `branches:` under `push:` cannot match); (3) `rg -U -q '^  push:[ ]*\n(( {4,}.*)?\n)* {4}branches: \[main\]'` matches; (4) `rg -q '^  workflow_dispatch:'` matches. The script also runs checks (1)-(4) on two inline fixtures in a temp file: today's block (`pull_request:` with `branches: [main]`) must fail check (2), and a block with `branches: [main]` only under `push:`, then `pull_request:` and `workflow_dispatch:`, must pass all four. `scripts/audit/run-script-tests.sh` already runs every `tests/audit/test-*.sh`, so creating the file under that name is enough.
- [ ] **Step 2: Run** → FAIL. **Step 3: Edit** `main.yaml`. **Step 4: Run** → PASS; `actionlint .github/workflows/main.yaml`.
- [ ] **Step 5: Document** in `README.md` one line: deterministic checks (`main.yaml`) run on every PR push and on manual dispatch.
- [ ] **Step 6: Commit** `ci: run the deterministic checks on pull requests of any base`.

### Task 5: Ship

- [ ] **Step 1:** `python3 scripts/build_plugins.py`; `python3 -m unittest discover -s tests/audit`; `bash scripts/audit/run-script-tests.sh`; `audit.py check --strict`.
- [ ] **Step 2:** Dual-lane code review of the diff (two lanes when available, one is enough), one fix wave, one scoped re-review; judge `pr-diagrams` again if its files changed after Task 2.
- [ ] **Step 3:** Compact to 3-6 commits, push (`--force-with-lease` if already pushed), open the PR with `commands/explain-pr-changes.md` stacked on the previous plan's PR.
