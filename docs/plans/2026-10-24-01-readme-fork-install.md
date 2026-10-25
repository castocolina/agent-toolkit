# Plan 1 — README Installs From This Fork

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Users install the skills from `castocolina/agent-toolkit` on Claude Code, Codex, Cursor, GitHub Copilot CLI, opencode and pi with copy-pasteable, non-interactive commands; agents and commands install only through the Claude Code marketplace (they are Claude Code-only).

**Architecture:** Documentation and marketplace metadata only. The marketplace keeps its name `agent-toolkit`, so `<plugin>@agent-toolkit` identifiers stay valid; only the owner and the repo references change. Two install routes, both verified headless on 2026-10-24: (a) the Claude Code marketplace (`claude plugin …`: skills, agents, commands) and (b) the `skills` CLI (`npx -y skills add … -a <agent> -y`: skills only, for every other harness; the first `-y` is npx's, the last is the skills CLI's). A manual `git clone` + `cp` is the no-tooling fallback, into the per-harness global skills directory that Step 6 records from each harness's own `-g` run (not a guessed shared directory). No per-harness native installers are documented: none was verified, so none is guessed.

**Tech Stack:** Markdown, `.claude-plugin/marketplace.json`, `scripts/build_plugins.py`, `claude` CLI, `skills` CLI (`npx skills`), `jq`, `gh`.

**Spec:** [Roadmap](2026-10-24-00-roadmap.md) — Decisions 10, 15; Global Constraints apply.

Branch: `docs/26-10-24-fork-install`, worktree `.claude/worktrees/fork-install`. Depends on nothing.

## Review Focus

1. A user who already added `softaworks/agent-toolkit` as `agent-toolkit` adds this fork → `claude plugin marketplace add castocolina/agent-toolkit` is refused (exit 1: "its source doesn't match its extraKnownMarketplaces entry"), so the README tells them to run `claude plugin marketplace remove agent-toolkit` first. Verified in Step 6: the refusal is asserted by exit code 1 plus the diagnostic text (a timeout or network error does not count). Plugins they already installed from the upstream marketplace: Step 6 records whether they survive the `remove` (`SWITCH-OUTCOME survives|gone`), emitted only from a `claude plugin list --json` call that exited 0 and returned a JSON array (a failed or timed-out call stops the script with `MARKETPLACE-FAIL`, never `gone`), and Step 7 writes that outcome into the README switching line. After the fork add and reinstall, Step 6 also asserts the installed `humanizer@agent-toolkit` version equals the fork marketplace clone's HEAD (12-char prefix), so the README's "reinstall takes this fork's version" is proven, not assumed.
2. A harness whose install path cannot be verified → left out, not guessed. "Verified" means one thing: the exact README command ran here, headless, exited 0, and the files it reports landed where its output says, checked per harness immediately after that harness's run, for both project scope and `-g` (landing dir named in that run's output, lock provenance `castocolina/agent-toolkit`). The landing dir is chosen deterministically: the skills CLI's default symlink mode also writes a canonical copy under `.agents/skills` for non-universal agents such as `pi`, so when several distinct dirs hold the skill, the one that is not `.agents/skills` is the agent's own; if that is still not exactly one, the script stops with `CHECK-FAIL` instead of guessing. A project-scope run that lands only in `.agents/skills` for a harness whose `-g` dir differs (the CLI skips the harness link when its dir, e.g. `.pi/`, is absent from the cwd) is a `HARNESS-FAIL`, not a verdict. Pinned in Step 6 (one `VERDICT <agent> project <dir> global <dir>` line per harness). The manual fallback uses only the per-harness `global <dir>` that the `skills` CLI itself wrote (`MANUAL <agent> ~/<dir>` lines), never an assumed shared directory. Any harness dropped from the README and the script's `AGENTS` list is recorded, with the reason, in the Step 9 commit body.
3. A copy-pasted command needs a TTY or hangs → not allowed. Every `npx` command in the README is written `npx -y skills add …` (npx's own `-y` suppresses npm's "Ok to proceed?" prompt, which appears on a terminal with an empty npm cache; the trailing `-y` belongs to the skills CLI). Every command (marketplace, `skills` CLI project scope, `-g`, `--skill '*'`, manual clone chains, manual Claude Code `cp`) runs with stdin closed (`</dev/null`) under `timeout 180` in a scratch `HOME` (so the npm cache is empty) and must exit 0. Because stdin-closed runs cannot show a TTY-only prompt, Step 8 also asserts statically that every `npx` in the README is `npx -y skills add`. Pinned in Steps 6 and 8.
4. `git clone` into a skills directory nests skills one level too deep (`skills/<name>`) → the fallback copies `skills/*` out of a temp clone, and Step 6 asserts `<dir>/humanizer/SKILL.md` exists and `<dir>/skills` does not, per harness.
5. A PR opened from the fork's `gh` defaults to the upstream parent → Step 9 names both repos explicitly and forbids `commands/explain-pr-changes.md` from creating or updating the PR.

---

### Task 1: Marketplace owner, install commands, attribution

**Files:**
- Modify: `.claude-plugin/marketplace.json` (`owner`)
- Modify: `README.md` (title `# Softaworks Agent Skills`; the intro paragraph under it; the Installation section; the Agents & Commands note; the Links entry). Line numbers below are pre-edit; read them from `git show HEAD:README.md`, because Step 3 changes the numbering. Later steps locate targets by quoted content.
- Modify: `CONTRIBUTING.md` (line 1 title; line 16 clone URL)

**Interfaces:**
- Produces: the README Installation section keeps its `## 🚀 Installation` heading, the "Available Plugins" and "Update Plugins" subsections, and the claude.ai note; `README.md` contains exactly one line with the text `softaworks/agent-toolkit` (the attribution); every `npx` in `README.md` is `npx -y skills add`; `CONTRIBUTING.md` contains none, case-insensitive `softaworks` included.

- [ ] **Step 1: Create the worktree and branch.** From the repo root: `git worktree add .claude/worktrees/fork-install -b docs/26-10-24-fork-install main`, then `cd .claude/worktrees/fork-install`. All later steps run there.
- [ ] **Step 2: Change the marketplace owner.** In `.claude-plugin/marketplace.json` set `owner` to `{"name":"castocolina","url":"https://github.com/castocolina"}`; leave `"name": "agent-toolkit"` unchanged.
- [ ] **Step 3: Rewrite the README Installation section.** Replace README (pre-edit) lines 15–87: the `## 🚀 Installation` heading through the closing fence of the Claude Code manual `cp` block at line 87. Keep lines 88–93 untouched: the blank line, the claude.ai note (`**For claude.ai** — Skills only` plus its sentence, lines 89–91), the blank line, and the `---` at 93. Re-emit the heading `## 🚀 Installation`, then these subsections in this order. Every command is non-interactive; the interactive `/plugin` UI appears only as one trailing sentence ("Interactive alternative: run `/plugin` inside Claude Code.").
  - **Claude Code (skills, agents, commands)** — `claude plugin marketplace add castocolina/agent-toolkit`; then per plugin `claude plugin install <plugin>@agent-toolkit` with the four examples `humanizer@agent-toolkit` (skill), `codex@agent-toolkit` (skill), `agent-codebase-pattern-finder@agent-toolkit` (agent), `command-codex-plan@agent-toolkit` (command).
  - **Switching from the upstream marketplace** — "Both marketplaces are named `agent-toolkit`, so remove the old one first: `claude plugin marketplace remove agent-toolkit`, then run the add command above." Step 7 appends one sentence on what happens to plugins already installed. The text must not contain the string `softaworks/agent-toolkit`.
  - **Codex, Cursor, GitHub Copilot CLI, opencode, pi (skills only)** — one table row per harness, using the `skills` CLI agent ids `codex`, `cursor`, `github-copilot`, `opencode`, `pi`, with the pattern `npx -y skills add castocolina/agent-toolkit --skill <skill-name> -a <agent-id> -y` (project scope) and `npx -y skills add castocolina/agent-toolkit --skill <skill-name> -a <agent-id> -g -y` (user scope). Add a one-line example installing all skills: `npx -y skills add castocolina/agent-toolkit --skill '*' -a codex -y`. Note below the table: agents and commands are Claude Code-only. A harness with a `HARNESS-FAIL` in Step 6 is removed from the table; if all five fail, replace the whole table with the single sentence "No non-Claude harness install path has been verified yet; use the Claude Code route above." and drop the `--skill '*'` example and the per-harness manual table.
  - **Available Plugins** — kept: re-emit README (pre-edit) lines 63–69 verbatim (the `agent-<name>@agent-toolkit` / `command-<name>@agent-toolkit` naming convention).
  - **Update Plugins** — kept, rewritten: `claude plugin marketplace update agent-toolkit`, then the existing sentence "You can also **Enable auto-update** to get the latest versions automatically." (pre-edit line 80); the four-step `/plugin` UI list (lines 75–78) is dropped.
  - **Manual install (skills only)** — two parts. (1) Claude Code: from a clone of the repo, `mkdir -p ~/.claude/skills && cp -r skills/<skill-name> ~/.claude/skills/`. (2) Other harnesses: the command `T=$(mktemp -d) && git clone --depth 1 https://github.com/castocolina/agent-toolkit.git "$T" && mkdir -p ~/<dir> && cp -r "$T"/skills/. ~/<dir>/ && rm -rf "$T"` plus a two-column table `Harness | <dir>` with one row per surviving harness. Do not invent the `<dir>` values and do not write a shared `~/.agents/skills` default: Step 7 fills the rows from the `MANUAL` lines of Step 6. Until Step 7, write the section with the command and an empty table body. The kept claude.ai note (lines 89–91) follows directly.
  - Removed entirely: "Quick Install", "Register as Plugin Marketplace", "Install Plugins" (Options 1–3, including "Option 3: Ask the Agent" and the `> Please install Skills from github.com/softaworks/agent-toolkit` quote at line 61); the interactive Option 3 cannot be verified headless.
- [ ] **Step 4: Resolve every remaining README line that names the upstream repo, by content.** Run `rg -n -i 'softaworks' README.md`; after Step 3 the old `npx skills add softaworks/agent-toolkit`, `/plugin marketplace add softaworks/agent-toolkit` (Installation) and `Please install Skills from github.com/softaworks/agent-toolkit` lines are gone. Resolve what is left, matching on the quoted text and not on line numbers:
  - In the Agents & Commands note's `bash` fence, the lines `> /plugin marketplace add softaworks/agent-toolkit` and `> /plugin install codex@agent-toolkit` become `> claude plugin marketplace add castocolina/agent-toolkit` and `> claude plugin install codex@agent-toolkit` (keep the fence).
  - `- [GitHub Repository](https://github.com/softaworks/agent-toolkit)` (Links) becomes `- [GitHub Repository](https://github.com/castocolina/agent-toolkit)`.
  - Retitle `# Softaworks Agent Skills` to `# Agent Toolkit`.
  - Insert directly after the intro paragraph that starts `Opinionated skills shared by` the single attribution line `Fork of [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy.` — the only README line allowed to contain `softaworks/agent-toolkit`.
- [ ] **Step 5: Update `CONTRIBUTING.md`.** Line 1 → `# Contributing to Agent Toolkit`; line 16 → `git clone https://github.com/castocolina/agent-toolkit.git`.
- [ ] **Step 6: Verify every README command headless in one scratch environment.** Save this as `${TMPDIR:-/tmp}/verify-install.sh` (outside the repo) and run it from the worktree root: `bash "${TMPDIR:-/tmp}/verify-install.sh"`. It uses scratch `HOME`s and cwds under one `mktemp -d`, unsets the env vars that redirect harness config (`CODEX_HOME`, `XDG_*`, `CLAUDE_CONFIG_DIR`) so nothing can reach the real config, and removes the scratch dir on exit. Each harness is checked right after its own run in its own empty directory, so one harness's files cannot satisfy another's check. Every failure, including the Claude Code manual fallback, prints a labelled line and the relevant output before exiting, because the scratch dir (and its `.out` files) is deleted on exit.

  ```bash
  set -e
  AGENTS="codex cursor github-copilot opencode pi"  # drop an id here AND from the README table only on HARNESS-FAIL
  REPO=castocolina/agent-toolkit; URL=https://github.com/$REPO.git
  SK="npx -y skills"  # exactly the README prefix; first -y is npx's, the trailing -y of each command is the skills CLI's
  MANUAL='T=$(mktemp -d) && git clone --depth 1 https://github.com/castocolina/agent-toolkit.git "$T" && mkdir -p ~/__DIR__ && cp -r "$T"/skills/. ~/__DIR__/ && rm -rf "$T"'
  ROOT=$(git rev-parse --show-toplevel)
  S=$(mktemp -d); trap 'cd /; rm -rf "$S"' EXIT
  unset CODEX_HOME XDG_CONFIG_HOME XDG_DATA_HOME XDG_CACHE_HOME CLAUDE_CONFIG_DIR
  export GIT_TERMINAL_PROMPT=0
  run() { timeout 180 "$@" </dev/null; }
  show() { bat --plain --paging=never "$1" || true; }
  mp() { run "$@" || { echo "MARKETPLACE-FAIL: $*"; exit 1; }; }  # Claude Code route: stop and report
  cm() { run "$@" || { echo "CLAUDE-MANUAL-FAIL: $*"; exit 1; }; }  # Claude Code manual fallback
  capture() { out=$(run "$@") || { echo "MARKETPLACE-FAIL: $* failed or timed out"; exit 1; }; }  # sets $out
  plist() { capture claude plugin list --json; printf '%s' "$out" | jq -e 'type=="array"' >/dev/null || { printf '%s\n' "$out"; echo "MARKETPLACE-FAIL: plugin list is not a JSON array"; exit 1; }; }
  check() { echo "CHECK-FAIL: $*"; exit 1; }                      # the script's own assertion is wrong: fix the script
  hfail() { echo "HARNESS-FAIL $1: $2"; show "$3"; exit 1; }       # agent, what, .out file
  allfail() { echo "ALL-SKILLS-FAIL: $*"; exit 1; }
  # landing dir of humanizer under root $1, relative to it: one dir or a non-zero return (1 none, 2 ambiguous).
  # Several dirs happen in symlink mode (canonical .agents/skills copy + the agent's own): the non-.agents one wins.
  land() {
    local c s; c=$(fd -HIL -E .npm -p 'humanizer/SKILL.md$' "$1" | while read -r p; do d=$(dirname "$(dirname "$p")"); echo "${d#"$1"/}"; done | sort -u)
    [ -n "$c" ] || return 1
    s=$(printf '%s\n' "$c" | { rg -vx '\.agents/skills' || true; }); [ -z "$s" ] || c=$s
    [ "$(printf '%s\n' "$c" | wc -l)" -eq 1 ] || { printf '%s\n' "$c" >&2; return 2; }
    printf '%s\n' "$c"
  }
  pick() {  # pick <root> <out-file> <agent> <scope> -> sets $PICKED
    PICKED=$(land "$1" 2>"$S/land.err") && return 0 || rc=$?
    [ "$rc" -eq 1 ] && hfail "$3" "$4: nothing landed" "$2"
    cat "$S/land.err"; check "$3 $4: ambiguous landing dirs above (decide which is the agent's own and fix land)"
  }
  names() { fd -HIL -g SKILL.md "$@" | while read -r p; do basename "$(dirname "$p")"; done | sort -u; }
  # --- Claude Code marketplace (HOME = scratch) ---
  export HOME="$S/home-claude"; mkdir -p "$HOME"; cd "$S"
  # Review Focus 1: upstream registered + one plugin installed -> fork add refused -> remove -> fork add works
  mp claude plugin marketplace add softaworks/agent-toolkit
  mp claude plugin install humanizer@agent-toolkit
  set +e; out=$(run claude plugin marketplace add $REPO 2>&1); rc=$?; set -e
  { [ "$rc" -eq 1 ] && printf '%s' "$out" | rg -qF "source doesn't match"; } || { printf '%s\n' "$out"; echo "MARKETPLACE-FAIL: conflict not refused as expected (rc=$rc)"; exit 1; }
  mp claude plugin marketplace remove agent-toolkit
  plist  # a failed list stops here; only a valid list decides the outcome
  if printf '%s' "$out" | jq -e 'any(.[]; .id == "humanizer@agent-toolkit")' >/dev/null; then echo "SWITCH-OUTCOME survives"; else echo "SWITCH-OUTCOME gone"; fi
  mp claude plugin marketplace add $REPO
  mp claude plugin marketplace update agent-toolkit
  for p in humanizer codex agent-codebase-pattern-finder command-codex-plan; do
    mp claude plugin install "$p@agent-toolkit"
  done
  # Provenance: marketplace source is the fork, four plugins installed, and humanizer (reinstalled over any survivor, exit 0 above) is the fork marketplace's commit
  capture claude plugin marketplace list --json
  printf '%s' "$out" | jq -e 'any(.[]; .name=="agent-toolkit" and .repo=="castocolina/agent-toolkit")' >/dev/null || { printf '%s\n' "$out"; check "marketplace source (fix the jq if the JSON shape differs)"; }
  loc=$(printf '%s' "$out" | jq -r '.[] | select(.name=="agent-toolkit") | .installLocation')
  want=$(git -C "$loc" rev-parse HEAD | cut -c1-12)
  plist
  printf '%s' "$out" | jq -e 'map(select(.id | endswith("@agent-toolkit"))) | length == 4' >/dev/null || { printf '%s\n' "$out"; check "plugin count"; }
  have=$(printf '%s' "$out" | jq -r '.[] | select(.id=="humanizer@agent-toolkit") | .version')
  { [ -n "$want" ] && [ -n "$have" ]; } || { printf '%s\n' "$out"; check "provenance: empty commit/version (fix the jq if the JSON shape differs)"; }
  [ "$have" = "$want" ] || { echo "MARKETPLACE-FAIL: humanizer@agent-toolkit is $have, fork marketplace clone is $want"; exit 1; }
  # --- skills CLI: per harness, project scope then -g, each checked immediately ---
  for a in $AGENTS; do
    D="$S/proj-$a"; mkdir -p "$D"; cd "$D"
    run $SK add $REPO --skill humanizer -a "$a" -y >"$S/$a.out" 2>&1 || hfail "$a" "project install" "$S/$a.out"
    pick "$D" "$S/$a.out" "$a" project; rel=$PICKED
    rg -qF "$rel" "$S/$a.out" || { show "$S/$a.out"; check "$a: output does not name $rel (wording or path rendering? fix the grep; if the files really landed elsewhere, treat as HARNESS-FAIL by hand)"; }
    rg -qF "\"source\": \"$REPO\"" "$D/skills-lock.json" || { show "$D/skills-lock.json"; check "$a: lock provenance (fix the grep if the lock format differs)"; }
    G="$S/home-g-$a"; mkdir -p "$G"
    HOME="$G" run $SK add $REPO --skill humanizer -a "$a" -g -y >"$S/$a-g.out" 2>&1 || hfail "$a" "-g install" "$S/$a-g.out"
    pick "$G" "$S/$a-g.out" "$a" "-g"; grel=$PICKED; echo "$grel" >"$S/grel-$a"
    rg -qF "$grel" "$S/$a-g.out" || { show "$S/$a-g.out"; check "$a -g: output does not name $grel (wording or path rendering? fix the grep; if the files really landed elsewhere, treat as HARNESS-FAIL by hand)"; }
    { [ "$rel" != .agents/skills ] || [ "$grel" = .agents/skills ]; } || hfail "$a" "project scope landed only in shared .agents/skills (harness dir absent from cwd?)" "$S/$a.out"
    fd -HIL -g '*lock*.json' "$G" | xargs -r rg -lF "$REPO" | rg -q . || check "$a -g: lock provenance (fix the search if the global lock format differs)"
    echo "VERDICT $a project $rel global $grel"
  done
  # --skill '*' form: every skill identity under skills/ must land
  D="$S/all"; mkdir -p "$D"; cd "$D"
  run $SK add $REPO --skill '*' -a codex -y >"$S/all.out" 2>&1 || { show "$S/all.out"; allfail "install"; }
  names -d 2 "$ROOT/skills" >"$S/want.txt"; names "$D" >"$S/got.txt"
  [ -s "$S/want.txt" ] || check "no skills found under $ROOT/skills"
  missing=$(comm -23 "$S/want.txt" "$S/got.txt"); [ -z "$missing" ] || { echo "$missing"; allfail "missing skills listed above"; }
  # --- manual fallbacks (exact README commands, fresh HOME each): non-Claude harnesses use the dir recorded from their own -g run ---
  for a in $AGENTS; do
    H="$S/home-manual-$a"; mkdir -p "$H"; grel=$(<"$S/grel-$a"); cd "$S"
    HOME="$H" run bash -c "${MANUAL//__DIR__/$grel}" || check "manual $a: clone chain"
    test -f "$H/$grel/humanizer/SKILL.md" || check "manual $a: not one level deep"
    test ! -e "$H/$grel/skills" || check "manual $a: nested skills/ dir"
    echo "MANUAL $a ~/$grel"
  done
  export HOME="$S/home-manual-claude"; mkdir -p "$HOME"; cd "$S"
  cm git clone --depth 1 $URL "$S/clone"; cd "$S/clone"
  cm bash -c 'mkdir -p ~/.claude/skills && cp -r skills/humanizer ~/.claude/skills/'
  test -f "$HOME/.claude/skills/humanizer/SKILL.md" || check "manual claude cp"
  echo VERIFY-OK
  ```

  Expected: one `SWITCH-OUTCOME survives|gone` line (from a successful `plugin list`), one `VERDICT <agent> project <dir> global <dir>` and one `MANUAL <agent> ~/<dir>` line per id in `AGENTS`, then `VERIFY-OK` as the last line, exit 0, no prompt (a hang is killed by `timeout` and fails).

  Recovery, by label (the failing line and its output are printed before the script exits):
  - `HARNESS-FAIL <agent>`: the harness's own install or landing failed (nothing landed, or project scope fell back to the shared `.agents/skills`; in the fallback case an alternative to excluding is to add `mkdir -p <harness-dir>` before the project command in both the script and the README row, only after a re-run proves it lands in the harness's own dir). Remove its id from `AGENTS` and its row from the README table, record "excluded: `<agent>`, `<reason from the printed output>`" for the Step 9 commit body, and re-run. If every id ends up removed, the README shows the single-sentence replacement from Step 3 (no table, no `--skill '*'` example, no per-harness manual table) and the commit body says all harnesses were excluded and why.
  - `CHECK-FAIL`: the script's own assertion (lock-file format, output wording or path rendering, JSON shape, ambiguous landing dirs) is wrong. Inspect the printed output, fix the script and re-run; a `CHECK-FAIL` never drops a harness by itself. If inspection shows the files landed somewhere the output does not name, record that as a `HARNESS-FAIL` by hand.
  - `ALL-SKILLS-FAIL`: remove the `--skill '*'` example from the README, record the reason, and re-run with that block removed from the script.
  - `MARKETPLACE-FAIL`: the Claude Code route cannot be dropped (includes a failed or timed-out `plugin list`, and an installed `humanizer@agent-toolkit` that is not the fork marketplace's commit). Stop, report the printed output to the user, and do not continue to Step 7.
  - `CLAUDE-MANUAL-FAIL`: the Claude Code manual `clone` or `cp` command failed. Fix the README command (and the script line that mirrors it) from the printed output and re-run; do not continue to Step 7 until it passes.

  `copilot` is not installed locally; its row is kept only if it passes, because the check proves the command and the landing directory, not the harness's own loading (the `skills` CLI owns that, and the manual table reuses exactly the directory that CLI wrote).
- [ ] **Step 7: Fill the two verified-outcome README spots from the Step 6 output.**
  - Manual table: for each `MANUAL <agent> ~/<dir>` line add one row `| <Harness display name> | ~/<dir> |` to the "Manual install" table from Step 3.
  - Switching line: append to the "Switching from the upstream marketplace" text exactly one sentence by `SWITCH-OUTCOME`. `gone`: "Plugins you installed from the old marketplace are uninstalled by the remove; reinstall the ones you want with `claude plugin install <plugin>@agent-toolkit`." `survives`: "Plugins you installed from the old marketplace stay listed after the remove; reinstall each with `claude plugin install <plugin>@agent-toolkit` to take this fork's version."
- [ ] **Step 8: Verify the text edits and rebuild**

  Run: `rg -c 'softaworks/agent-toolkit' README.md` — Expected: `1`.
  Run: `rg -n 'softaworks/agent-toolkit' README.md` — Expected: exactly the attribution line.
  Run: `rg -i -c 'softaworks' CONTRIBUTING.md` — Expected: no output, exit 1.
  Run: `rg -n 'npx' README.md | rg -v 'npx -y skills add'` — Expected: no output, exit 1 (every `npx` line is the verified `npx -y skills add` form).
  Run: `rg -n '~/\.agents/skills' README.md` — Expected: no output unless a `MANUAL` line recorded exactly that directory.
  Run: `python3 scripts/build_plugins.py && git status --short` — Expected: only `.claude-plugin/marketplace.json`, `README.md`, `CONTRIBUTING.md` and (if the build changes them) files under `dist/`.
- [ ] **Step 9: Commit, push, open the PR against the fork**

  ```bash
  git add dist .claude-plugin/marketplace.json README.md CONTRIBUTING.md
  git commit -m "docs(readme): install from castocolina fork with non-interactive commands" -m "<excluded harnesses and reasons from Step 6, or: none>"
  git push -u origin docs/26-10-24-fork-install
  ```

  Then follow `commands/explain-pr-changes.md` **only to produce the PR body text**, saved to the file `${TMPDIR:-/tmp}/pr-body-fork-install.md`, and append the Step 6 `SWITCH-OUTCOME`, `VERDICT` and `MANUAL` lines plus any excluded harnesses with reasons. Do NOT let that command create or update a PR (it says it will, and without `--repo` it would target the upstream parent). Only this call opens the PR: `gh pr create --repo castocolina/agent-toolkit --base main --head docs/26-10-24-fork-install --title "docs(readme): install from castocolina fork" --body-file "${TMPDIR:-/tmp}/pr-body-fork-install.md"`. `--repo` is mandatory: the fork has no `gh` default and its parent is `softaworks/agent-toolkit`. Expected: the printed URL starts with `https://github.com/castocolina/agent-toolkit/pull/`.
