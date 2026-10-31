#!/usr/bin/env bash
# Structure tests for the scheduled-audit workflows: offline checks that pin the
# security-relevant wiring (token isolation, scope checks, prompt rendering,
# evidence artifacts and supply-chain pins) in place. They read the YAML as
# text; actionlint covers syntax separately.
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
WF="$ROOT/.github/workflows/skill-audit.yaml"
SELF="$ROOT/tests/audit/test-workflow.sh"

python3 - "$WF" "$ROOT" "$SELF" <<'PY'
import re
import sys
from pathlib import Path

text = Path(sys.argv[1]).read_text(encoding="utf-8")
ROOT = Path(sys.argv[2])
SELF = Path(sys.argv[3]).resolve()


def fail(message):
    print(f"workflow structure: {message}", file=sys.stderr)
    raise SystemExit(1)


def jobs_of(source):
    """Map job name -> (header text before 'steps:', list of step texts)."""
    lines = source.split("\njobs:\n", 1)[1].splitlines()
    jobs = {}
    name = None
    header = []
    steps = []
    in_steps = False
    current = None
    for line in lines:
        job = re.match(r"^  ([a-z][a-z0-9-]*):\s*$", line)
        if job:
            if name:
                if current is not None:
                    steps.append("\n".join(current))
                jobs[name] = ("\n".join(header), steps)
            name, header, steps, in_steps, current = job.group(1), [], [], False, None
            continue
        if name is None:
            continue
        if not in_steps:
            if line.strip() == "steps:":
                in_steps = True
            else:
                header.append(line)
            continue
        if re.match(r"^      - ", line):
            if current is not None:
                steps.append("\n".join(current))
            current = [line]
        elif current is not None:
            current.append(line)
    if name:
        if current is not None:
            steps.append("\n".join(current))
        jobs[name] = ("\n".join(header), steps)
    return jobs


def step_name(step):
    match = re.search(r"^      - name: (.+)$", step, re.M)
    return match.group(1).strip() if match else None


COPILOT_INVOCATION = re.compile(r"copilot -p|copilot-agent\.sh|copilot-runner\.sh|npm install -g @github/copilot|\| *copilot\b")

jobs = jobs_of(text)
expected_jobs = {"detect", "checkpoint", "attempt", "rubric", "research", "evals", "merge", "apply", "review",
                 "upstream-report", "state"}
if set(jobs) != expected_jobs:
    fail(f"unexpected job set {sorted(jobs)}")

# Finding 1: no checkout persists credentials, and no PAT sits in a job that runs copilot.
if "persist-credentials: true" in text:
    fail("persist-credentials: true found")
for name, (header, steps) in jobs.items():
    for step in steps:
        if "actions/checkout@" in step and "persist-credentials: false" not in step:
            fail(f"checkout in job {name} persists credentials")
    # A job-level PAT reaches every step, so it is forbidden in any job that
    # checks out the repository or runs a model. Every job here checks out
    # (state included), so the PAT must stay in its own step in each one.
    untrusted = any("actions/checkout@" in step or COPILOT_INVOCATION.search(step) for step in steps)
    if untrusted and "AUDIT_BOT_TOKEN" in header:
        fail(f"job {name} declares AUDIT_BOT_TOKEN at job level but runs repository or model code")
    # Per step: a step that invokes Copilot (or installs it) must not see the PAT.
    for step in steps:
        if "AUDIT_BOT_TOKEN" in step and COPILOT_INVOCATION.search(step):
            fail(f"job {name}: step {step_name(step)!r} runs copilot and sees AUDIT_BOT_TOKEN")

# Finding 1: in apply, the PAT is only in the trusted steps (push, PR create).
apply_header, apply_steps = jobs["apply"]
pat_steps = sorted(step_name(s) for s in apply_steps if "AUDIT_BOT_TOKEN" in s)
expected_pat = sorted(["Push the audit branch", "Open audit pull request"])
if pat_steps != expected_pat:
    fail(f"apply PAT steps are {pat_steps}, expected {expected_pat}")
if "AUDIT_BOT_TOKEN" in apply_header:
    fail("apply declares AUDIT_BOT_TOKEN at job level")
push = next(s for s in apply_steps if step_name(s) == "Push the audit branch")
# The token must reach git through a per-command, URL-scoped extraheader that
# is not persisted: env-based GIT_CONFIG_* (kept out of argv) or git -c.
if not ("GIT_CONFIG_KEY_0=http.https://github.com/.extraheader" in push or
        "git -c http.https://github.com/.extraheader" in push):
    fail("push step does not authenticate with a per-command URL-scoped extraheader")
if re.search(r"git (config|remote)\b", push) and "--local" not in push and "git config user" not in push:
    fail("push step persists git configuration")
if "git remote set-url" in text or "x-access-token:${{" in text:
    fail("token embedded in a remote URL or literal")
body = next(s for s in apply_steps if step_name(s) and "pr-body" in step_name(s).lower() or (step_name(s) or "").startswith("Render the audit PR body"))
if "copilot -p" not in body or "AUDIT_BOT_TOKEN" in body:
    fail("PR body generation must run copilot without the PAT")
pr = next(s for s in apply_steps if step_name(s) == "Open audit pull request")
if "gh pr create" not in pr or "gh label create" not in pr or "copilot" in pr:
    fail("PR step must only create the PR and labels")

# Finding 2: every repairs.patch application is scope-checked first, in every job that applies it.
# A no-op rubric refresh writes an EMPTY repairs.patch; git apply rejects empty input
# (exit 128), so every consumer must guard on a non-empty file, not mere existence.
for name, (_, steps) in jobs.items():
    for step in steps:
        if "git apply" in step and "repairs.patch" in step:
            if '[ -s "$RUNNER_TEMP/rubric/repairs.patch" ]' not in step:
                fail(f"job {name} applies repairs.patch without a non-empty guard (-s)")
            if 'trusted/scope-check.py" repairs' not in step:
                fail(f"job {name} applies repairs.patch without scope-check")
            if "--numstat" not in step:
                fail(f"job {name} scope-checks repairs without git apply --numstat")
            # The applying command is the one that is not the --numstat feed.
            apply_match = re.search(r'git apply (--index )?"\$RUNNER_TEMP/rubric/repairs\.patch"', step)
            if apply_match is None:
                fail(f"job {name}: repairs step has no applying git apply")
            apply_at = apply_match.start()
            if step.index('trusted/scope-check.py" repairs') > apply_at:
                fail(f"job {name} runs git apply before the scope check")
for name in ("research", "evals", "merge", "apply"):
    if not any("repairs.patch" in s and "git apply" in s for s in jobs[name][1]):
        fail(f"job {name} does not apply the repairs patch")

# Finding 2: the apply-job fixer changes are scope-checked before the commit stages them.
fixer_steps = [i for i, s in enumerate(apply_steps) if "trusted/scope-check.py\" fixer" in s]
commit_steps = [i for i, s in enumerate(apply_steps) if "git add -A" in s]
if not fixer_steps or not commit_steps:
    fail("apply must scope-check the fixer and run git add -A")
# Before the build: fixer edits only. After the build (dist/** regenerated): the final stage.
for i in fixer_steps:
    fixer = apply_steps[i]
    for marker in ("--decision \"$RUNNER_TEMP/decision/decision.json\"", "--format porcelain-v2", "--skip-staged"):
        if marker not in fixer:
            fail(f"fixer scope check lacks {marker}")
if "--final-stage" not in apply_steps[fixer_steps[-1]]:
    fail("the last fixer scope check must be the final stage (after build_plugins)")
if fixer_steps[-1] > commit_steps[0]:
    fail("fixer scope check runs after git add -A")
if 'trusted/scope-check.py" repairs' not in "".join(s for s in apply_steps if "repairs.patch" in s):
    fail("apply does not scope-check repairs before applying them")

# Findings 3+4+5: the rubric job renders its prompt, ships evidence and runs the host checks.
rubric = "\n".join(jobs["rubric"][1])
for marker in ('"$RUNNER_TEMP/trusted/render-prompt.py" .github/audit/rubric-prompt.md', "STRUCTURE_CHANGED=\"$STRUCTURE_CHANGED\"",
               "--text NEW_PAGES=", "--text REMOVED_PAGES=", "--path FETCH_RESULT=.audit-evidence/fetch-result.json",
               "--path SPEC_DIFF=.audit-evidence/spec.diff", "--path PAGES_JSON=audit-pages/pages.json",
               "spec/content/spec.diff", "spec/content/fetch-result.json",
               "bash tests/skills/agentskills-research/test-fetch-spec.sh",
               "python3 scripts/audit/audit.py rubric-check",
               "scope-check.py\" repairs --format porcelain-v2"):
    if marker not in rubric:
        fail(f"rubric job lost {marker!r}")
if "cat .github/audit/rubric-prompt.md" in text:
    fail("rubric prompt is still piped verbatim")
if rubric.index("bash tests/skills/agentskills-research/test-fetch-spec.sh") > rubric.index("git add -A"):
    fail("host checks run after the patch is captured")
if "STRUCTURE_CHANGED: ${{ needs.detect.outputs.structure_changed }}" not in rubric:
    fail("rubric job does not pass the structure flag")

# Finding 3: detect ships the complete fetch result (new/removed pages) in the spec artifact.
detect = "\n".join(jobs["detect"][1])
if "cp \"$RUNNER_TEMP/spec-fetch.json\" fetch-result.json" not in detect or "ZIP_PATHS=(" not in detect:
    fail("detect does not ship fetch-result.json")
if "fetch-result.json" not in detect.split("ZIP_PATHS=(")[1].split(")")[0]:
    fail("fetch-result.json is not in the spec zip")

# Finding 7: approved upstream evidence is fetched by detect, for exactly the approved keys.
if '--keys "$APPROVED_UPSTREAMS"' not in detect or "--evidence-dir approved-evidence" not in detect:
    fail("detect does not fetch approved upstream evidence with --keys")
if "approved-evidence" not in detect.split("ZIP_PATHS=(")[1].split(")")[0] and "ZIP_PATHS+=(approved-evidence)" not in detect:
    fail("approved evidence is not in the spec zip")
if "mkdir -p approved-evidence" not in detect:
    fail("approved-evidence must exist on every run (merge and apply render it with --path)")
if "approved-evidence" in detect.split("ZIP_PATHS=(")[1].split(")")[0] and "ZIP_PATHS+=(approved-evidence)" in detect:
    fail("approved-evidence must be zipped unconditionally, not only on approval dispatches")

# A failed remote query must stop the run, not look like "branch absent".
branch = next(s for s in apply_steps if step_name(s) == "Choose a unique branch")
if "rc=$?" not in branch or 'case $rc in' not in branch or "cannot query origin" not in branch:
    fail("branch selection treats a failed ls-remote as an absent branch")

# Finding 6: merge publishes the evidence bundle and apply restores it.
merge = "\n".join(jobs["merge"][1])
for marker in ("name: evidence-bundle", "merged.json", "check.json", "spec.diff", "upstreams.json",
               "evals-results", "approved-evidence", "--path APPROVED_EVIDENCE=.audit-evidence/approved-evidence"):
    if marker not in merge:
        fail(f"merge job lacks {marker!r}")
download_at = [i for i, s in enumerate(apply_steps) if "name: evidence-bundle" in s]
copy_at = [i for i, s in enumerate(apply_steps) if "cp -a \"$RUNNER_TEMP/bundle/.\" .audit-evidence/" in s]
if not download_at or not copy_at or download_at[0] > copy_at[0]:
    fail("apply does not download and then restore the evidence bundle")
for marker in ("--path MERGED_JSON=.audit-evidence/merged.json", "--path CHECK_JSON=.audit-evidence/check.json",
               "--path SPEC_DIFF=.audit-evidence/spec.diff",
               "--path APPROVED_EVIDENCE=.audit-evidence/approved-evidence",
               "--out-path DECISION_JSON"):
    if marker not in "\n".join(apply_steps) and marker != "--out-path DECISION_JSON":
        fail(f"fix prompt render lacks {marker}")
if '"$RUNNER_TEMP/trusted/render-prompt.py" .github/audit/fix-prompt.md' not in "\n".join(apply_steps):
    fail("fix prompt is not rendered through render-prompt.py")

# Finding 8: pins. Every setup-uv use is pinned by SHA; every Copilot install says it is UNVERIFIED and must be pinned.
pinned = "astral-sh/setup-uv@0c5e2b8115b80b4c7c5ddf6ffdd634974642d182 # v5.4.1"
if text.count(pinned) != 4:
    fail(f"expected 4 pinned setup-uv uses, found {text.count(pinned)}")
if re.search(r"setup-uv@v", text):
    fail("unpinned setup-uv tag still referenced")
for match in re.finditer(r"npm install -g @github/copilot", text):
    context = text[max(0, match.start() - 300):match.start()]
    if "pin the exact @github/copilot version" not in context or "UNVERIFIED" not in context:
        fail("a Copilot install lacks the UNVERIFIED pinning comment")
# One comment per install step: the pinning note must not be duplicated.
if text.count("# UNVERIFIED: pin the exact @github/copilot version") != text.count("npm install -g @github/copilot"):
    fail("Copilot pinning comments are not exactly one per install step")

# Item 3: the fixer and every post-model decision check use the untouched downloaded
# decision under $RUNNER_TEMP, never the model-writable workspace copy.
for i, s in enumerate(apply_steps):
    if "scope-check.py fixer" in s and "--decision .audit-evidence/decision.json" in s:
        fail(f"apply step {step_name(s)!r} trusts the workspace decision for the fixer scope")
fixer_decision = [s for s in apply_steps if 'scope-check.py" fixer' in s]
if not fixer_decision or not all("--decision \"$RUNNER_TEMP/decision/decision.json\"" in s for s in fixer_decision):
    fail("fixer scope check is not given the untouched downloaded decision under RUNNER_TEMP")

# Item 5: upload-artifact skips empty directories, so apply and merge recreate approved-evidence
# after restoring the bundle, before any --path render reads it.
for name in ("merge", "apply"):
    steps = jobs[name][1]
    restore = [i for i, s in enumerate(steps) if "approved-evidence" in s and ("cp -a" in s or "cp -a \"$RUNNER_TEMP/bundle" in s)]
    mk = [i for i, s in enumerate(steps) if "mkdir -p .audit-evidence/approved-evidence" in s]
    if not mk:
        fail(f"job {name} does not create .audit-evidence/approved-evidence after the bundle restore")
    if restore and mk[0] < restore[0]:
        fail(f"job {name} creates approved-evidence before the bundle restore")

# Model-tampering guard: every job that runs a write-capable model step (copilot-agent.sh)
# copies the scope and render tools into $RUNNER_TEMP/trusted/ and snapshots git state
# before the model runs, then verifies git state and scope-checks the model's output
# immediately afterwards, before any repository code runs.
WRITE_JOBS = ("rubric", "merge", "apply")
REPO_CODE = re.compile(r"python3 scripts/|bash tests/|python3 \.github/audit/|bash \.github/audit/|\bcopilot-runner\.sh\b|\bnpm install\b|\bpython3 -m\b")
for name in WRITE_JOBS:
    steps = jobs[name][1]
    names = [step_name(s) or "" for s in steps]
    model = [i for i, s in enumerate(steps) if "copilot-agent.sh" in s]
    if not model:
        fail(f"job {name} has no write-capable model step")
    first_model = model[0]
    trusted = [i for i, s in enumerate(steps) if "$RUNNER_TEMP/trusted" in s and "cp " in s]
    if not trusted or trusted[0] > first_model:
        fail(f"job {name} does not copy trusted tooling to $RUNNER_TEMP/trusted before its first model step")
    snapshot = [i for i, s in enumerate(steps) if 'git-state.sh" snapshot' in s]
    if not snapshot or snapshot[0] > first_model:
        fail(f"job {name} does not snapshot git state before its first model step")
    for m in model:
        after = [i for i in range(m + 1, len(steps)) if 'git-state.sh" verify' in steps[i]]
        if not after:
            fail(f"job {name} verifies git state nowhere after a model step")
        scope = [i for i in range(m + 1, len(steps)) if "scope-check.py" in steps[i]]
        if not scope:
            fail(f"job {name} scope-checks nothing after a model step")
        first_repo_code = [i for i in range(m + 1, len(steps)) if REPO_CODE.search(steps[i])]
        post_model_check = max(after[0], scope[0])
        if first_repo_code and first_repo_code[0] < post_model_check:
            fail(f"job {name}: repository code ({names[first_repo_code[0]]!r}) runs before the post-model check")
    # The trusted copy is what gets invoked, never the checkout's scope-check.py.
    for i, s in enumerate(steps):
        # Only invocations are checked: copying the checkout's tooling into the trusted directory is allowed.
        for tool in ("scope-check.py", "render-prompt.py", "git-state.sh"):
            if re.search(r"(python3|bash) \.github/audit/" + re.escape(tool), s):
                fail(f"job {name}: step {names[i]!r} runs {tool} from the checkout")

# The merge job applies the rubric repairs before the model runs. They must be staged into the
# baseline before the snapshot, and the decision scope check must skip staged paths: otherwise
# every run with non-empty repairs fails the check on the repairs themselves.
merge_steps = jobs["merge"][1]
snap_i = [i for i, s_ in enumerate(merge_steps) if 'git-state.sh" snapshot' in s_]
if not snap_i:
    fail("merge job has no git-state snapshot")
if "git add -A" not in merge_steps[snap_i[0]].split('git-state.sh" snapshot')[0]:
    fail("merge job does not stage the pre-model workspace (git add -A) before the git-state snapshot")
decision_check = [s_ for s_ in merge_steps if "scope-check.py\" decision" in s_]
if not decision_check or any("--skip-staged" not in s_ for s_ in decision_check):
    fail("merge job decision scope check must pass --skip-staged")

# ---- Phase 1 A1: interval gate, failure backoff and checkpoint ---------------------------------
def field(header, key):
    found = re.search(rf"^    {key}:(.*)$", header, re.M)
    return found.group(1).strip() if found else None


def needs_of(name):
    raw = field(jobs[name][0], "needs") or ""
    return [item.strip() for item in raw.strip("[]").split(",") if item.strip()]


def if_of(name):
    return field(jobs[name][0], "if")


GATE_EXPR = "(github.event_name != 'schedule' || vars.AUDIT_ENABLED == 'true')"

# test_cron_is_daily
if "cron: '0 6 * * *'" not in text or "1,16" in text:
    fail("the schedule is not daily (cron '0 6 * * *')")

# The constant workflow-level group is the serialized boundary for every writer.
if "group: skill-audit\n  cancel-in-progress: false" not in text:
    fail("the workflow concurrency boundary is not the constant serialized group")

# Workflow-level knob defaults (read by detect now and by review later).
workflow_env = text.split("\njobs:\n", 1)[0]
for knob, default in (("AUDIT_RESEARCH_MODELS", "'auto'"), ("AUDIT_MERGER_MODEL", "'auto'"),
                      ("AUDIT_INTERVAL_DAYS", "'15'"), ("AUDIT_REVIEW_EFFORT", "'high'"),
                      ("AUDIT_ON_POSITIVE", "'label'")):
    line = f"  {knob}: ${{{{ vars.{knob} || {default} }}}}"
    if line not in workflow_env:
        fail(f"workflow env lacks the default {line!r}")

# test_queued_run_reads_live_state: no job ever reads a snapshot of the variable; the read is a step.
if "vars.AUDIT_LAST_STATE" in text or "$AUDIT_LAST_STATE" in text:
    fail("a job reads a workflow-level snapshot of AUDIT_LAST_STATE instead of the live variable")

# test_interval_step_precedes_every_fetch_model_and_write and test_validate_knobs_runs_in_detect.
d_header, d_steps = jobs["detect"]
if "actions/checkout@" not in d_steps[0] or "Read the live audit state" not in d_steps[1] or "id: interval" not in d_steps[2]:
    fail("the first detect steps after the checkout are not the live read and then the interval step")
interval = d_steps[2]
if "audit.py validate-knobs" not in interval:
    fail("detect does not validate the knobs")
if "interval-due" not in interval or "live-state.json" not in interval:
    fail("the interval step does not decide from the saved live state with interval-due")
if "bash .github/audit/write-state.sh read" not in d_steps[1] or "live-state.json" not in d_steps[1]:
    fail("the live read step does not save write-state.sh read output")
if "AUDIT_BOT_TOKEN" in interval or [i for i, s in enumerate(d_steps) if "AUDIT_BOT_TOKEN" in s] != [1]:
    fail("the live read must carry AUDIT_BOT_TOKEN in its own step only, never in the interval step")
if "AUDIT_BOT_TOKEN" in d_header:
    fail("detect declares AUDIT_BOT_TOKEN at job level")
for i, s in enumerate(d_steps[3:], start=3):
    if "steps.interval.outputs.skip != 'true'" not in s:
        fail(f"detect step {step_name(s) or i!r} runs without the interval gate")
for needle in ("fetch-spec.sh", "audit.py upstreams", "audit.py detect", "gh pr list"):
    first = next(i for i, s in enumerate(d_steps) if needle in s)
    if first < 2:
        fail(f"{needle!r} runs before the interval step")

# detect outputs default to run_needed=false and full_check=false; full_check is written only by the final publish step.
for key, expr in (("run_needed", "steps.publish.outputs.run_needed || 'false'"),
                   ("full_check", "steps.publish.outputs.full_check || 'false'")):
    if f"      {key}: ${{{{ {expr} }}}}" not in d_header:
        fail(f"detect output {key} does not default to false")
if [step_name(s) for s in d_steps if "full_check=" in s] != ["Publish detect outputs after artifact upload"]:
    fail("full_check is written by a step other than the final publish step")

# test_checkpoint_condition_exact, test_attempt_job_stamps_before_judging, test_checkpoint_and_state_predicates_exclusive.
if if_of("checkpoint") != "${{ !cancelled() && " + GATE_EXPR + " && needs.detect.result == 'success' && needs.detect.outputs.full_check == 'true' && needs.detect.outputs.run_needed == 'false' }}":
    fail("checkpoint condition is not the exact contract condition")
if if_of("attempt") != "${{ !cancelled() && " + GATE_EXPR + " && needs.detect.result == 'success' && needs.detect.outputs.run_needed == 'true' }}":
    fail("attempt condition is not the exact contract condition")
if needs_of("checkpoint") != ["detect"] or needs_of("attempt") != ["detect"]:
    fail("checkpoint and attempt must need only detect")
cp_if, st_if = if_of("checkpoint"), if_of("state")
if "run_needed == 'false'" not in cp_if or "run_needed == 'true'" in cp_if:
    fail("checkpoint predicate is not run_needed == 'false' only")
if "run_needed == 'true'" not in st_if or "run_needed == 'false'" in st_if:
    fail("state predicate is not run_needed == 'true' only")

# test_writers_have_contents_read_and_step_scoped_pat and test_writers_use_write_state_helper.
for name, mode in (("checkpoint", "checkpoint"), ("attempt", "attempt"), ("state", "state")):
    header, steps = jobs[name]
    if "permissions:\n      contents: read" not in header or "permissions: {}" in header:
        fail(f"{name} is not contents: read")
    if "AUDIT_BOT_TOKEN" in header:
        fail(f"{name} declares AUDIT_BOT_TOKEN at job level")
    if "actions/checkout@" not in steps[0] or "persist-credentials: false" not in steps[0]:
        fail(f"{name} does not start with a credentialless checkout")
    token_steps = [s for s in steps if "AUDIT_BOT_TOKEN" in s]
    if len(token_steps) != 1 or f"bash .github/audit/write-state.sh {mode}" not in token_steps[0]:
        fail(f"{name}: AUDIT_BOT_TOKEN must sit only in the write step")
if "gh variable set" in text:
    fail("a job writes AUDIT_LAST_STATE directly instead of through write-state.sh")

# test_failed_attempt_starts_no_model and test_judging_jobs_need_attempt.
for name in ("rubric", "research", "evals", "upstream-report", "merge", "apply", "state"):
    if "attempt" not in needs_of(name):
        fail(f"{name} does not need attempt")
    if "needs.attempt.result == 'success'" not in (if_of(name) or ""):
        fail(f"{name} starts without a successful attempt")

# test_queued_run_reads_live_state: the live read happens inside the run, before the interval decision,
# and feeds both interval-due and detect from the same saved file (never the job-env snapshot).
live_read = d_steps[1]
if "GH_TOKEN: ${{ secrets.AUDIT_BOT_TOKEN }}" not in live_read or "write-state.sh read" not in live_read:
    fail("the live read step is not the PAT-scoped write-state.sh read")
for s in d_steps[2:]:
    if "AUDIT_LAST_STATE" in s and "live-state.json" not in s:
        fail(f"detect step {step_name(s)!r} reads AUDIT_LAST_STATE instead of the live read")
if text.count('--state "$(<"$RUNNER_TEMP/live-state.json")"') != 2:
    fail("interval-due and detect must both be fed the live read")

# test_attempt_job_stamps_before_judging: attempt is the only stamper before any model, and the
# judging jobs cannot start without it.
attempt_steps = jobs["attempt"][1]
if len(attempt_steps) != 2 or "write-state.sh attempt" not in attempt_steps[1]:
    fail("attempt job must do nothing but stamp last_attempt_at before judging")
# test_failed_or_early_stopped_check_never_stamps: only checkpoint (full_check, run_needed false) stamps
# checked_at; state stamps it only after a complete run; attempt stamps last_attempt_at only.
for name, mode in (("checkpoint", "checkpoint"), ("state", "state"), ("attempt", "attempt")):
    if f"write-state.sh {mode}" not in "".join(jobs[name][1]):
        fail(f"{name} does not call write-state.sh {mode}")
if "write-state.sh attempt" in "".join(jobs["checkpoint"][1]) or "write-state.sh checkpoint" in "".join(jobs["attempt"][1]):
    fail("checkpoint and attempt write the wrong marker")
if "full_check" not in if_of("checkpoint"):
    fail("checkpoint does not require a complete check")

# ---- Phase 1 A2: review call, apply status and the removed merge modes -------------------------
LEVEL = {"none": 0, "read": 1, "write": 2}


def block_at(lines, start):
    """Permission key -> level for the indented block that starts after lines[start]."""
    out = {}
    for line in lines[start + 1:]:
        match = re.match(r"^      ([a-z-]+): (read|write|none)$", line)
        if not match:
            break
        out[match.group(1)] = match.group(2)
    return out


def permissions_in(source):
    lines = source.splitlines()
    starts = [i for i, line in enumerate(lines) if line == "    permissions:"]
    return block_at(lines, starts[0]) if starts else None


# test_review_job_calls_the_workflow_with_permissions
if "review" not in jobs:
    fail("no review job calls the review workflow")
review_header, review_steps = jobs["review"]
if review_steps:
    fail("review is a reusable-workflow call and must have no steps of its own")
if needs_of("review") != ["apply"]:
    fail(f"review needs {needs_of('review')}, expected ['apply']")
if "uses: ./.github/workflows/skill-audit-review.yaml" not in review_header:
    fail("review does not call ./.github/workflows/skill-audit-review.yaml")
if if_of("review") != "${{ !cancelled() && " + GATE_EXPR + " && needs.apply.result == 'success' }}":
    fail("review condition is not the exact contract condition")
expected_review_perms = {"contents": "read", "checks": "read", "pull-requests": "write",
                         "statuses": "write", "issues": "write"}
if permissions_in(review_header) != expected_review_perms:
    fail(f"review permissions are {permissions_in(review_header)}, expected {expected_review_perms}")
for line in ("pr_number: ${{ needs.apply.outputs.pr_number }}", "head_sha: ${{ needs.apply.outputs.head_sha }}"):
    if line not in review_header:
        fail(f"review does not pass {line!r}")
if "COPILOT_GITHUB_TOKEN: ${{ secrets.COPILOT_GITHUB_TOKEN }}" not in review_header or "inherit" in review_header:
    fail("review must pass COPILOT_GITHUB_TOKEN explicitly and never inherit secrets")
if "AUDIT_BOT_TOKEN" in review_header:
    fail("review must not hold the bot token")
# The called workflow can only use what the caller grants: every called level must fit under the caller's.
called_lines = (ROOT / ".github/workflows/skill-audit-review.yaml").read_text(encoding="utf-8").splitlines()
called = {}
for i, line in enumerate(called_lines):
    if line == "    permissions:":
        for key, level in block_at(called_lines, i).items():
            if LEVEL[level] > LEVEL[called.get(key, "none")]:
                called[key] = level
for key, level in called.items():
    if LEVEL[expected_review_perms.get(key, "none")] < LEVEL[level]:
        fail(f"skill-audit-review.yaml needs {key}: {level}, which the review call does not grant")

# test_state_does_not_depend_on_review
if "review" in needs_of("state") or "needs.review" in (if_of("state") or ""):
    fail("state depends on review: the audit state must not wait for or read the review")

# test_apply_outputs_head_sha_and_eval_status_step
if "apply" not in jobs:
    fail("no apply job")
apply_header, apply_steps = jobs["apply"]
if "      head_sha: ${{ steps.commit.outputs.head_sha }}" not in apply_header:
    fail("apply does not output head_sha from the commit step")
commit_steps = [s for s in apply_steps if step_name(s) == "Commit the audit changes"]
if len(commit_steps) != 1 or "        id: commit\n" not in commit_steps[0]:
    fail("the commit step has no id: commit")
if 'echo "head_sha=$(git rev-parse HEAD)" >> "$GITHUB_OUTPUT"' not in commit_steps[0]:
    fail("the commit step does not write head_sha after committing")
if commit_steps[0].index("git commit") > commit_steps[0].index("head_sha="):
    fail("head_sha is written before the commit exists")
status = [i for i, s in enumerate(apply_steps) if "skill-audit/evals" in s]
if len(status) != 1:
    fail("apply must set the skill-audit/evals status in exactly one step")
status_step = apply_steps[status[0]]
if "GH_TOKEN: ${{ github.token }}" not in status_step or "AUDIT_BOT_TOKEN" in status_step or "COPILOT_GITHUB_TOKEN" in status_step:
    fail("the status step must use only the step-scoped workflow token")
if "GH_TOKEN" in apply_header:
    fail("apply declares GH_TOKEN at job level; the status token must be step-scoped")
if "state=success" not in status_step or "context=skill-audit/evals" not in status_step \
        or "repos/$GH_REPO/statuses/$HEAD_SHA" not in status_step:
    fail("the status step does not post success for skill-audit/evals on the head SHA")
if "HEAD_SHA: ${{ steps.commit.outputs.head_sha }}" not in status_step:
    fail("the status step is not bound to the committed head_sha")
step_at = {step_name(s): i for i, s in enumerate(apply_steps)}
evals_i = next(i for i, s in enumerate(apply_steps) if "run-evals" in s)
if not (evals_i < status[0] < step_at["Open audit pull request"]):
    fail("the eval status must follow the eval gate and precede PR creation")
if not step_at["Push the audit branch"] < status[0]:
    fail("the eval status must follow the push")

# test_apply_has_statuses_write
apply_perms = permissions_in(apply_header)
if apply_perms is None or apply_perms.get("statuses") != "write":
    fail(f"apply lacks statuses: write (permissions {apply_perms})")

# test_no_merge_mode_remains: no merge mode, merge label, gate or preflight wiring in any scanned file.
# README, plans and docs/ are not scanned: they hold historical audit data.
MERGE_TERMS = ("AUDIT_MERGE_MODE", "merge_mode", "audit-merge:", "merge-knob", "skill-audit-gate",
               "preflight", "AUDIT_REVIEW_BOT", "AUDIT_CLEAN_REVIEW_TEXT")
scanned = 0
for scope in (".github/workflows", ".github/audit", "scripts", "tests"):
    for path in sorted((ROOT / scope).rglob("*")):
        if not path.is_file() or path.resolve() == SELF:
            continue
        scanned += 1
        body = path.read_text(encoding="utf-8", errors="replace")
        for term in MERGE_TERMS:
            if term in body:
                fail(f"{path.relative_to(ROOT)} still contains {term!r}")
if scanned == 0:
    fail("test_no_merge_mode_remains scanned no files")

# test_no_merge_path_exists: no workflow and no trusted publisher merges a PR or arms auto-merge.
merge_scan = [p for p in sorted((ROOT / ".github/workflows").iterdir()) if p.is_file()]
merge_scan += sorted((ROOT / ".github/audit").glob("*.sh")) + sorted((ROOT / ".github/audit").glob("*.py"))
if not merge_scan:
    fail("test_no_merge_path_exists scanned no files")
for path in merge_scan:
    body = path.read_text(encoding="utf-8", errors="replace")
    for term in ("gh pr merge", "--auto"):
        if term in body:
            fail(f"{path.relative_to(ROOT)} contains the merge path {term!r}")

print("PASS workflow structure: token isolation, scope checks, prompts, evidence and pins")
PY
