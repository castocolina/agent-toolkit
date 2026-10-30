#!/usr/bin/env bash
# Structure tests for .github/workflows/skill-audit-review.yaml. They read the
# YAML as text (no YAML library is assumed) and pin the security wiring of the
# PR review: event conditions, token placement, trusted copies, gate order and
# the head binding. actionlint covers syntax separately.
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
WF="$ROOT/.github/workflows/skill-audit-review.yaml"
[[ -f "$WF" ]] || { echo "workflow structure: $WF is missing" >&2; exit 1; }

python3 - "$WF" "$ROOT/.github/audit/review-prompt.md" <<'PY'
import re
import sys
from pathlib import Path

text = Path(sys.argv[1]).read_text(encoding="utf-8")


def fail(message):
    print(f"review workflow: {message}", file=sys.stderr)
    raise SystemExit(1)


def section(name):
    """The text of a top-level job, from its header to the next job."""
    match = re.search(rf"^  {re.escape(name)}:\n(.*?)(?=^  [a-z][a-z-]*:\n|\Z)", text, re.M | re.S)
    if not match:
        fail(f"job {name} is missing")
    return match.group(1)


def steps_of(job_text):
    """List of (name, block text) for each step of a job; a step with no name has an empty name."""
    body = job_text.split("    steps:\n", 1)[1]
    blocks = [b for b in re.split(r"^      - ", body, flags=re.M)[1:] if b.strip()]
    result = []
    for block in blocks:
        match = re.search(r"^ *name: (.+)$", block, re.M)
        result.append((match.group(1).strip() if match else "", block))
    return result


def step_text(job_text, name):
    for step_name, body in steps_of(job_text):
        if step_name == name:
            return "      - " + body
    fail(f"step {name!r} is missing")


def index_of(job_text, name):
    for position, (step_name, _) in enumerate(steps_of(job_text)):
        if step_name == name:
            return position
    fail(f"step {name!r} is missing")


def header(job_text):
    return job_text.split("    steps:\n", 1)[0]


# ---- top-level triggers and permissions -----------------------------------
on_block = text.split("\njobs:\n", 1)[0]
if "workflow_call:" not in on_block:
    fail("no workflow_call trigger")
if "workflow_dispatch:" not in on_block:
    fail("no workflow_dispatch trigger")
if "pull_request_target:" not in on_block:
    fail("no pull_request_target trigger")
if not re.search(r"pull_request_target:\n\s+types: \[synchronize\]", on_block):
    fail("pull_request_target must be limited to types: [synchronize]")
def input_block(trigger, name):
    """The YAML block of one input under a trigger (e.g. workflow_call / pr_number)."""
    trig = re.search(rf"^  {re.escape(trigger)}:\n(.*?)(?=^  [a-z_]+:\n|\Z)", on_block, re.M | re.S)
    if not trig:
        fail(f"trigger {trigger} is missing")
    block = re.search(rf"^      {re.escape(name)}:\n((?:        .*\n?)*)", trig.group(1), re.M)
    if not block:
        fail(f"{trigger} input {name} is missing")
    return block.group(1)


for typed in ("pr_number", "head_sha"):
    if not re.search(r"^        type: string$", input_block("workflow_call", typed), re.M):
        fail(f"workflow_call input {typed} must be typed string")
if not re.search(r"secrets:\n\s+COPILOT_GITHUB_TOKEN:\n\s+required: true", on_block):
    fail("COPILOT_GITHUB_TOKEN must be a required secret for workflow_call")
top = text.split("\njobs:\n", 1)[0]
if not re.search(r"^permissions: \{\}\s*$", text, re.M):
    fail("top-level permissions must be {}")
if not re.search(r"concurrency:\n\s+group: skill-audit-review-\$\{\{ inputs\.pr_number \|\| github\.event\.pull_request\.number \}\}\n\s+cancel-in-progress: true", text):
    fail("concurrency group must be skill-audit-review-${{ inputs.pr_number || github.event.pull_request.number }} with cancel-in-progress true")

# ---- jobs and event conditions ---------------------------------------------
JOBS = ("target", "review", "invalidate")
for job in JOBS:
    section(job)
for job in re.findall(r"^  ([a-z][a-z-]*):\n", text, re.M):
    if job not in JOBS:
        fail(f"unexpected job {job}")

target = section("target")
review = section("review")
invalidate = section("invalidate")
# Inside a called workflow github.event_name is the caller's event (schedule, workflow_dispatch),
# never workflow_call, so target and review must not name workflow_call at all.
for job_name, job_text in (("target", target), ("review", review)):
    cond = re.search(r"if: (.*)", job_text).group(1)
    if "workflow_call" in cond:
        fail(f"{job_name} must not test event_name == workflow_call (it is the caller's event in a called run)")
    if "pull_request_target" not in cond or "!=" not in cond:
        fail(f"{job_name} must exclude pull_request_target with event_name != 'pull_request_target'")
if "pull_request_target" not in re.search(r"if: (.*)", invalidate).group(1):
    fail("invalidate must run only on pull_request_target")
if "workflow_call" in re.search(r"if: (.*)", invalidate).group(1):
    fail("invalidate must not run on workflow_call")

# ---- target: validation, outputs, no checkout ----------------------------
if "actions/checkout" in target:
    fail("target must not check out repository code")
for output in ("pr_number", "head_sha", "base_sha", "default_branch", "model_empty"):
    if f"{output}:" not in header(target) and f"echo \"{output}=" not in target and f"{output}=" not in target:
        fail(f"target must output {output}")
if "GH_REPO: ${{ github.repository }}" not in target:
    fail("target must set GH_REPO")
if "AUDIT_REVIEW_MODEL" not in target:
    fail("target must decide the skipped path from AUDIT_REVIEW_MODEL")
if "audit-review:skipped" not in target:
    fail("target must label skipped PRs audit-review:skipped")
for check in ("state", "labels", "headRepository", "isCrossRepository"):
    if check not in target:
        fail(f"target must validate the PR {check}")
if "gh api repos/$GH_REPO" not in target and "gh api \"repos/$GH_REPO" not in target:
    fail("default_branch must come from gh api repos/$GH_REPO")
if "github.event.pull_request" in target or "github.event.repository.default_branch" in target:
    fail("target must not read the default branch or PR state from the event payload")
if re.search(r"^\s+- (uses: )?astral-sh/setup-uv", target, re.M) or "npm install" in target:
    fail("target must not install tools")

# ---- review: skipped path, trusted copies, gates -------------------------
if "needs.target.outputs.model_empty != 'true'" not in review:
    fail("review must skip when the model knob is empty")
if "timeout-minutes: 45" not in review:
    fail("review must set timeout-minutes: 45")
review_perms = header(review)
for permission in ("contents: read", "checks: read", "pull-requests: write", "statuses: write", "issues: write"):
    if permission not in review_perms:
        fail(f"review must grant {permission}")
if "COPILOT_GITHUB_TOKEN" in header(review):
    fail("the Copilot token must not be a job-level env in review")

names = [name for name, _ in steps_of(review)]
checkout_first = index_of(review, "Check out the default branch into trusted")
if checkout_first != 0:
    fail("the trusted checkout must be the first review step")
trusted_checkout = step_text(review, "Check out the default branch into trusted")
if "ref: ${{ needs.target.outputs.default_branch }}" not in trusted_checkout:
    fail("trusted checkout must pin the default branch from target")
if "path: trusted" not in trusted_checkout:
    fail("trusted checkout must write to trusted/")
pr_checkout = step_text(review, "Check out the pull request head into pr")
if "ref: ${{ needs.target.outputs.head_sha }}" not in pr_checkout:
    fail("PR checkout must use the head_sha from target")
if "path: pr" not in pr_checkout:
    fail("PR checkout must write to pr/")
for checkout in (trusted_checkout, pr_checkout):
    if "fetch-depth: 0" not in checkout or "persist-credentials: false" not in checkout:
        fail("both checkouts need fetch-depth: 0 and persist-credentials: false")

copy_step = step_text(review, "Copy the trusted tooling")
for path in (
    "scripts/audit/audit.py",
    ".github/audit/scope-check.py",
    ".github/audit/review-combine.py",
    ".github/audit/review-publish.sh",
    ".github/audit/review-gates.sh",
    ".github/audit/copilot-review.sh",
    ".github/audit/review-prompt.md",
    ".github/audit/expected-checks.txt",
    ".github/audit/render-prompt.py",
    "skills/skill-judge/references/agentskills/SOURCE.json",
):
    if path not in copy_step:
        fail(f"the trusted copy must include {path}")
if "$RUNNER_TEMP/trusted" not in copy_step:
    fail("trusted copies must land in $RUNNER_TEMP/trusted")

if index_of(review, "Validate the review knobs from the trusted copy") <= index_of(review, "Copy the trusted tooling"):
    fail("validate-knobs must run after the trusted copy")
knobs = step_text(review, "Validate the review knobs from the trusted copy")
if "validate-knobs" not in knobs:
    fail("validate-knobs must run from the trusted copy")
if "$RUNNER_TEMP/trusted/audit.py" not in knobs:
    fail("validate-knobs must run the trusted audit.py")

# install steps come before any step that uses the tools, and hold no secrets
install_index = [index_of(review, n) for n in names if n.startswith("Install ")]
if not install_index:
    fail("review must install the Copilot CLI and setup-uv")
setup_index = names.index("Install Copilot CLI (UNVERIFIED until Task 1 spike)") if "Install Copilot CLI (UNVERIFIED until Task 1 spike)" in names else None
if setup_index is None:
    fail("the Copilot CLI install step must carry the UNVERIFIED pin comment name")
for name, body in steps_of(review):
    if name.startswith("Install "):
        if "secrets." in body or "COPILOT_GITHUB_TOKEN" in body or "github.token" in body:
            fail(f"install step {name!r} must hold no secrets")
        if "UNVERIFIED" not in body and "UNVERIFIED" not in name:
            fail(f"install step {name!r} needs an UNVERIFIED pin comment")

scope_index = index_of(review, "Gate scope")
check_index = index_of(review, "Gate check")
if not (install_index and max(install_index) < scope_index):
    fail("install steps must precede the gates")
if not scope_index < check_index:
    fail("gates must run scope before check")
for gate_name in ("Gate scope", "Gate check",
                  "Gate evals", "Gate CI", "Build the capped reviewer diff and gate its size"):
    body = step_text(review, gate_name)
    if "working-directory: pr" in body or "cd pr" in body:
        fail(f"gate {gate_name!r} must not run inside pr/")

for gate_name in ("Gate scope", "Gate check"):
    body = step_text(review, gate_name)
    if "$RUNNER_TEMP/trusted" not in body:
        fail(f"gate {gate_name!r} must use the trusted copy")
if "numstat-z" not in step_text(review, "Gate scope"):
    fail("scope gate must read git diff --numstat -z")
if "--patch" not in step_text(review, "Gate scope"):
    fail("scope gate must pass --patch")
if "--validator-pin" not in step_text(review, "Gate check"):
    fail("the check gate must pass --validator-pin")
if "--root pr" not in step_text(review, "Gate check"):
    fail("the check gate must check the PR tree via --root pr")

evals_gate = step_text(review, "Gate evals")
if not re.search(r"review-gates\.sh\"? evals", evals_gate):
    fail("the evals gate must call review-gates.sh evals")
ci_gate = step_text(review, "Gate CI")
if not re.search(r"review-gates\.sh\"? ci", ci_gate):
    fail("the CI gate must call review-gates.sh ci")
if "secrets." in ci_gate:
    fail("the CI gate must not read secrets")
if "GH_TOKEN: ${{ github.token }}" not in ci_gate:
    fail("the CI gate must use github.token as step-scoped env")

# ---- reviewer: the Copilot token only in the reviewer step ---------------
reviewer = step_text(review, "Run the read-only PR reviewer")
if "COPILOT_GITHUB_TOKEN: ${{ secrets.COPILOT_GITHUB_TOKEN }}" not in reviewer:
    fail("the reviewer step must receive COPILOT_GITHUB_TOKEN")
if "github.token" in reviewer or "AUDIT_BOT_TOKEN" in reviewer:
    fail("the reviewer step must not receive a GitHub token")
for name, body in steps_of(review):
    if name != "Run the read-only PR reviewer" and "COPILOT_GITHUB_TOKEN" in body:
        fail(f"step {name!r} must not see COPILOT_GITHUB_TOKEN")
if "copilot-review.sh" not in reviewer:
    fail("the reviewer must run copilot-review.sh")

# ---- publish: github.token only in the publish steps, always() ---------------
combine = step_text(review, "Combine the gates and the reviewer answer")
if "if: ${{ !cancelled() }}" not in combine and "!cancelled()" not in combine:
    fail("combine must run unless cancelled")
publish = step_text(review, "Publish the review outcome")
if "if: ${{ !cancelled() }}" not in publish and "!cancelled()" not in publish:
    fail("publish must run unless cancelled")
if "GH_TOKEN: ${{ github.token }}" not in publish:
    fail("publish must use github.token as step-scoped env")
if "review-publish.sh" not in publish:
    fail("publish must call review-publish.sh")
for name, body in steps_of(review):
    if name in ("Publish the review outcome", "Gate CI", "Gate evals"):
        continue
    if "github.token" in body:
        fail(f"step {name!r} must not receive github.token")

# ---- invalidate: no checkout, labels only ---------------------------------
if "actions/checkout" in invalidate:
    fail("invalidate must not check out code")
for permission in ("pull-requests: write", "issues: write"):
    if permission not in header(invalidate):
        fail(f"invalidate needs {permission} to remove the labels (gh pr edit drives the issues labels API)")
if "audit-review:" not in invalidate:
    fail("invalidate must remove the audit-review:* labels")
if "synchronize" not in invalidate:
    fail("invalidate must act on synchronize")

# ---- the gate code and the checks must never run PR code ----------------
for name, body in steps_of(review):
    if re.search(r"(^|\s)(bash|python3?) pr/", body):
        fail(f"step {name!r} runs code from pr/")

diff_step = step_text(review, "Build the capped reviewer diff and gate its size")
if "head -c 61440" not in diff_step:
    fail("the reviewer diff must be capped at 61440 bytes")
if "':!dist'" not in diff_step:
    fail("the reviewer diff must exclude dist/**")
if "review-gates.sh\"? diff-size" not in diff_step and not re.search(r"review-gates\.sh\"? diff-size", diff_step):
    fail("the diff gate must measure the full diff with review-gates.sh diff-size")
render = step_text(review, "Render the reviewer prompt")
if "render-prompt.py" not in render or "PR_DIFF=.audit-evidence/pr.diff" not in render:
    fail("the reviewer prompt must render the capped PR diff")
prompt = Path(sys.argv[2]).read_text(encoding="utf-8")
if "{{PR_DIFF}}" not in prompt:
    fail("review-prompt.md must contain {{PR_DIFF}}")
if "validate-knobs" not in step_text(review, "Validate the review knobs from the trusted copy"):
    fail("review knobs must be validated")
# ---- the brief's named checks (Task A2, Step 1) ---------------------------
def test_synchronize_removes_review_labels():
    inv = section("invalidate")
    if "pull_request_target" not in re.search(r"if: (.*)", inv).group(1) or "synchronize" not in inv:
        fail("invalidate must run on pull_request_target synchronize")
    if "--remove-label" not in inv or "audit-review:" not in inv:
        fail("synchronize must remove the audit-review:* labels")
    if "contains(github.event.pull_request.labels.*.name, 'skill-audit')" not in re.search(r"if: (.*)", inv).group(1):
        fail("invalidate must act only on PRs labeled skill-audit")


def test_invalidate_has_no_checkout_and_runs_only_on_synchronize():
    inv = section("invalidate")
    if "actions/checkout" in inv:
        fail("invalidate must not check out code")
    cond = re.search(r"if: (.*)", inv).group(1)
    if "event_name == 'pull_request_target'" not in cond or "action == 'synchronize'" not in cond:
        fail("invalidate must be limited to pull_request_target synchronize")
    if "workflow_call" in cond or "workflow_dispatch" in cond:
        fail("invalidate must not run for workflow_call or workflow_dispatch")


def test_target_review_run_only_on_call_or_dispatch():
    # A called run reports event_name schedule or workflow_dispatch, never workflow_call.
    for job in ("target", "review"):
        cond = re.search(r"if: (.*)", section(job)).group(1)
        if "workflow_call" in cond:
            fail(f"{job} must not test for workflow_call (the caller's event is what runs)")
        if "event_name != 'pull_request_target'" not in cond:
            fail(f"{job} must exclude pull_request_target")


def test_concurrency_group_expression_covers_all_events():
    if "inputs.pr_number" not in text.split("concurrency:", 1)[1].split("\n\n", 1)[0]:
        fail("concurrency group must read inputs.pr_number")
    if "github.event.pull_request.number" not in text.split("concurrency:", 1)[1].split("\n\n", 1)[0]:
        fail("concurrency group must read github.event.pull_request.number")


def test_empty_model_skips_in_target_without_installs():
    tgt = section("target")
    if "actions/checkout" in tgt or "npm install" in tgt or "setup-uv" in tgt:
        fail("target must not checkout or install")
    if "model_empty=true" not in tgt:
        fail("target must set model_empty=true when AUDIT_REVIEW_MODEL is empty")
    if "audit-review:skipped" not in tgt:
        fail("target must label the skipped PR audit-review:skipped")


def test_gate_steps_run_outside_pr_dir():
    for gate_name in ("Gate scope", "Gate check", "Gate evals", "Gate CI", "Build the capped reviewer diff and gate its size"):
        body = step_text(section("review"), gate_name)
        if "working-directory: pr" in body or re.search(r"^\s*cd pr\b", body, re.M):
            fail(f"gate {gate_name!r} must not run inside pr/")
        if re.search(r"(^|\s)(bash|python3?) (\"?)\$?\{?[A-Z_]*\}?pr/", body):
            fail(f"gate {gate_name!r} must not execute pr/ code")


def test_inputs_typed_and_mismatched_head_rejected():
    for name in ("pr_number", "head_sha"):
        if not re.search(r"^        type: string$", input_block("workflow_call", name), re.M):
            fail(f"{name} must be a typed string input")
    if "is not the live head" not in section("target"):
        fail("target must reject a head_sha that differs from the live head")
    if "CALLER_HEAD" not in section("target"):
        fail("target must compare the caller head_sha with the live head")


def test_install_steps_precede_use_and_hold_no_secrets():
    rv = section("review")
    names = [n for n, _ in steps_of(rv)]
    installs = [i for i, n in enumerate(names) if n.startswith("Install ")]
    gates = [i for i, n in enumerate(names) if n.startswith("Gate ")]
    if not installs or not gates or max(installs) > min(gates):
        fail("install steps must precede the gates that use them")
    for name, body in steps_of(rv):
        if name.startswith("Install ") and ("secrets." in body or "github.token" in body):
            fail(f"install step {name!r} must hold no secrets")


def test_called_review_defaults_match_main_workflow():
    # The review's knob defaults must match skill-audit.yaml's (the main workflow owns them).
    main = Path(sys.argv[1]).with_name("skill-audit.yaml").read_text(encoding="utf-8")
    for knob, default in (("AUDIT_REVIEW_EFFORT", "'high'"), ("AUDIT_ON_POSITIVE", "'label'")):
        if f"{knob}: ${{{{ vars.{knob} || {default} }}}}" not in main:
            fail(f"main workflow default for {knob} is not {default}")
        if f"{knob}: ${{{{ vars.{knob} || {default} }}}}" not in text:
            fail(f"review default for {knob} differs from the main workflow")


for check in (test_synchronize_removes_review_labels, test_invalidate_has_no_checkout_and_runs_only_on_synchronize,
              test_target_review_run_only_on_call_or_dispatch, test_concurrency_group_expression_covers_all_events,
              test_empty_model_skips_in_target_without_installs, test_gate_steps_run_outside_pr_dir,
              test_inputs_typed_and_mismatched_head_rejected, test_install_steps_precede_use_and_hold_no_secrets,
              test_called_review_defaults_match_main_workflow):
    check()
# ---- combine and publish run only after the trusted tooling is in place -------
def test_combine_and_publish_gated_on_trusted_copy():
    rv = section("review")
    for name in ("Combine the gates and the reviewer answer", "Publish the review outcome"):
        cond = re.search(r"if: (.*)", step_text(rv, name)).group(1)
        if "steps.trusted.outcome == 'success'" not in cond:
            fail(f"{name!r} must be guarded by the trusted copy step outcome")
    if "id: trusted" not in step_text(rv, "Copy the trusted tooling"):
        fail("the trusted tooling copy step must have id: trusted")


def test_validate_knobs_runs_in_detect_and_review():
    # U1 ruling: validate-knobs runs at both sites. The review site is this file;
    # the detect site is read-only here (skill-audit.yaml belongs to another unit).
    main = Path(sys.argv[1]).with_name("skill-audit.yaml").read_text(encoding="utf-8")
    if "audit.py validate-knobs" not in main:
        fail("detect must run validate-knobs in skill-audit.yaml")
    rv = step_text(section("review"), "Validate the review knobs from the trusted copy")
    if "validate-knobs" not in rv or "$RUNNER_TEMP/trusted/audit.py" not in rv:
        fail("review must run validate-knobs from the trusted copy")


test_validate_knobs_runs_in_detect_and_review()

def test_gate_steps_record_their_exit_code_under_errexit():
    # GitHub's default shell is bash -e: each gate must turn errexit off around the
    # gate command, so a failing gate still records its code (1) instead of a crash.
    rv = section("review")
    for name in ("Gate scope", "Gate check", "Gate evals", "Gate CI"):
        body = step_text(rv, name)
        if "set +e" not in body:
            fail(f"gate {name!r} must run with set +e so its failure code is recorded")
        if "set -e" in body.replace("set +e", ""):
            fail(f"gate {name!r} must not re-enable errexit")
    if "code=2" not in step_text(rv, "Gate scope") or "case \"$code\" in 0|1" not in step_text(rv, "Gate scope"):
        fail("the scope gate must map anything other than 0 or 1 to needs-human (2)")


def test_gate_exit_code_overrides_the_printed_value():
    # A gate that prints 0 and then exits non-zero must be recorded as needs-human (2), not 0.
    rv = section("review")
    for name in ("Gate evals", "Gate CI"):
        body = step_text(rv, name)
        if "value=$(cat" not in body:
            fail(f"gate {name!r} must read its printed value into value")
        if not re.search(r'if \[ "\$code" -ne 0 \]; then value=2; fi', body) and \
           not re.search(r'if \[ "\$code" -ne 0 \]; then code=2; value=2; fi', body):
            fail(f"gate {name!r} must record 2 (needs-human) whenever its exit code is non-zero")


def test_diff_build_failure_is_needs_human():
    # A failed git diff must never leave an empty pr.diff that diff-size reads as a pass.
    rv = section("review")
    body = step_text(rv, "Build the capped reviewer diff and gate its size")
    if 'git -C pr diff --binary -M "$BASE_SHA...$HEAD_SHA" -- . \':!dist\' > "$RUNNER_TEMP/pr.diff"' not in body:
        fail("the diff build line changed; re-check the failure path")
    if "gates/diff-size" not in body:
        fail("the diff build must write the diff-size gate")
    if not re.search(r"if ! git -C pr diff[^\n]*pr\.diff\"?; then[^\n]*2 >", body) and \
       not re.search(r'if ! git -C pr diff.*\n.*echo 2 > "\$RUNNER_TEMP/gates/diff-size"', body) and \
       "echo 2 > \"$RUNNER_TEMP/gates/diff-size\"" not in body:
        fail("a failed git diff must write 2 to gates/diff-size")


def test_check_gate_uses_the_trusted_allowlist():
    # The check gate reads the allowlist from the trusted copy, never pr/scripts/audit (a PR file).
    rv = section("review")
    if "scripts/audit/non_latin_allowlist.txt" not in step_text(rv, "Copy the trusted tooling"):
        fail("the trusted copy must include scripts/audit/non_latin_allowlist.txt")
    if "--allowlist \"$RUNNER_TEMP/trusted/non_latin_allowlist.txt\"" not in step_text(rv, "Gate check"):
        fail("the check gate must pass --allowlist from the trusted copy")


def test_reviewer_prompt_names_the_trusted_rubric_path():
    # The rubric lives in the trusted copy; the working directory is the workspace root, not a skill tree.
    rv = section("review")
    render = step_text(rv, "Render the reviewer prompt")
    if "--path RUBRIC_PATH=trusted/skills/skill-judge/references" not in render:
        fail("the reviewer prompt must render RUBRIC_PATH from the trusted checkout")
    prompt = Path(sys.argv[2]).read_text(encoding="utf-8")
    if "{{RUBRIC_PATH}}" not in prompt:
        fail("review-prompt.md must take the rubric path from {{RUBRIC_PATH}}")
    if "skills/skill-judge/references, which is checked out in the working directory" in prompt:
        fail("review-prompt.md still points at a rubric path in the working directory")


def test_reviewer_has_a_deadline_below_the_job_timeout():
    # A hung reviewer must fail its own step, so combine and publish still run. The deadline must sit
    # well under the job's timeout-minutes, which cancels the whole job (and skips publish).
    rv = section("review")
    job_limit = re.search(r"timeout-minutes: (\d+)", rv)
    if not job_limit:
        fail("review must set timeout-minutes")
    body = step_text(rv, "Run the read-only PR reviewer")
    bound = re.search(r"^\s*timeout (?:--kill-after=\S+ )?(\d+)([mh])\b", body, re.M)
    if not bound:
        fail("the reviewer command must be bounded by timeout <N>m")
    minutes = int(bound.group(1)) * (60 if bound.group(2) == "h" else 1)
    if not 0 < minutes <= int(job_limit.group(1)) - 10:
        fail(f"the reviewer deadline ({minutes}m) must leave at least 10 minutes under the job timeout-minutes {job_limit.group(1)}")
    if "copilot-review.sh" not in body:
        fail("the bounded command must still run copilot-review.sh")


def test_no_leftover_review_workspace():
    # The prompt step made a review-workspace directory nothing used. It must stay removed.
    if "review-workspace" in text:
        fail("the unused review-workspace directory is back in the review workflow")


test_no_leftover_review_workspace()
test_reviewer_has_a_deadline_below_the_job_timeout()
test_reviewer_prompt_names_the_trusted_rubric_path()
test_check_gate_uses_the_trusted_allowlist()
test_diff_build_failure_is_needs_human()
test_gate_exit_code_overrides_the_printed_value()
test_gate_steps_record_their_exit_code_under_errexit()
test_combine_and_publish_gated_on_trusted_copy()
print("PASS review workflow structure")
PY

echo "PASS test-review-workflow.sh"
