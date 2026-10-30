#!/usr/bin/env python3
"""Truth-table tests for the scheduled-audit stamps (.github/workflows/skill-audit.yaml).

The workflow is YAML and this suite reads it as text (no YAML library is assumed).
The `if:` expressions of the checkpoint, attempt and state jobs and of the detect
publish/upload steps are taken from the file and evaluated against modelled job
results. That checks the rule behind the stamps as behaviour: checked_at is stamped
only by a clean, complete check, last_attempt_at only by an attempt that starts,
and nothing advances the state after a failed or skipped stage.
"""
import re
import unittest
from pathlib import Path

WORKFLOW = Path(__file__).resolve().parents[2] / ".github/workflows/skill-audit.yaml"


def workflow_text() -> str:
    return WORKFLOW.read_text(encoding="utf-8")


def jobs_text(text: str) -> str:
    return text.split("\njobs:\n", 1)[1]


def job_header(text: str, name: str) -> str:
    """The job's header block (everything before its steps), keyed by the job name."""
    match = re.search(rf"^  {re.escape(name)}:\n(.*?)(?=^  [a-z][a-z0-9-]*:\n|\Z)", jobs_text(text), re.M | re.S)
    if not match:
        raise AssertionError(f"job {name} is missing")
    return match.group(1).split("    steps:\n", 1)[0]


def job_if(text: str, name: str) -> str:
    match = re.search(r"^    if: \$\{\{ (.*) \}\}$", job_header(text, name), re.M)
    if not match:
        raise AssertionError(f"job {name} has no if")
    return match.group(1)


def step_if(text: str, job: str, step_name: str) -> str:
    body = jobs_text(text)
    section = re.search(rf"^  {re.escape(job)}:\n(.*?)(?=^  [a-z][a-z0-9-]*:\n|\Z)", body, re.M | re.S).group(1)
    blocks = re.split(r"^      - ", section.split("    steps:\n", 1)[1], flags=re.M)
    for block in blocks:
        if re.search(rf"^ *name: {re.escape(step_name)}$", block, re.M):
            match = re.search(r"^        if: \$\{\{ (.*) \}\}$", block, re.M)
            if not match:
                raise AssertionError(f"step {step_name!r} has no if")
            return match.group(1)
    raise AssertionError(f"step {step_name!r} is missing from {job}")


# ---- a small evaluator for the expression subset the workflow uses -----------------------

TOKEN = re.compile(r"""\s*(?:
    (?P<str>'[^']*')
  | (?P<op>&&|\|\||==|!=|!|\(|\))
  | (?P<fn>cancelled\(\))
  | (?P<id>[A-Za-z_][A-Za-z0-9_.-]*)
)""", re.X)


def tokenize(expr: str) -> list[tuple[str, str]]:
    tokens, pos, expr = [], 0, expr.strip()
    while pos < len(expr):
        match = TOKEN.match(expr, pos)
        if not match:
            raise AssertionError(f"cannot tokenize {expr!r} at {pos}")
        kind = match.lastgroup
        tokens.append((kind, match.group(kind)))
        pos = match.end()
    return tokens


def norm(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return ""
    return str(value).lower()


def truthy(value) -> bool:
    if isinstance(value, bool):
        return value
    return value not in ("", None)


class Evaluator:
    def __init__(self, tokens, ctx):
        self.t, self.i, self.ctx = tokens, 0, ctx

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else (None, None)

    def take(self):
        token = self.peek()
        self.i += 1
        return token

    def run(self):
        value = self.or_()
        if self.i != len(self.t):
            raise AssertionError(f"trailing tokens at {self.i}")
        return value

    def or_(self):
        value = self.and_()
        while self.peek() == ("op", "||"):
            self.take()
            right = self.and_()  # always consume the operand, even when the left side is already true
            value = truthy(value) or truthy(right)
        return value

    def and_(self):
        value = self.cmp()
        while self.peek() == ("op", "&&"):
            self.take()
            right = self.cmp()  # same rule: consume the operand even when the left side is false
            value = truthy(value) and truthy(right)
        return value

    def cmp(self):
        left = self.unary()
        if self.peek() in (("op", "=="), ("op", "!=")):
            op = self.take()[1]
            same = norm(left) == norm(self.unary())
            return same if op == "==" else not same
        return left

    def unary(self):
        if self.peek() == ("op", "!"):
            self.take()
            return not truthy(self.unary())
        return self.primary()

    def primary(self):
        kind, value = self.take()
        if kind == "op" and value == "(":
            inner = self.or_()
            if self.take() != ("op", ")"):
                raise AssertionError("missing )")
            return inner
        if kind == "str":
            return value[1:-1]
        if kind == "fn":
            if value != "cancelled()":
                raise AssertionError(f"unsupported status function {value}")
            return bool(self.ctx.get("cancelled", False))
        if kind == "id":
            if value in ("true", "false"):
                return value == "true"
            return self.ctx.get(value, "")
        raise AssertionError(f"unexpected token {value!r}")


def evaluate(expr: str, ctx: dict) -> bool:
    return truthy(Evaluator(tokenize(expr), ctx).run())


# ---- modelled runs ---------------------------------------------------------------------------

def detect_context(s: dict) -> dict:
    """The detect job's outputs given the scenario. The publish step is the only writer of
    full_check and run_needed: it runs only when detect's earlier steps succeeded, the
    interval is due and no audit PR is open. Otherwise the job output defaults apply."""
    publish_ran = s["detect"] == "success" and s["interval_skip"] != "true" and s["open_pr"] != "true"
    return {
        "needs.detect.result": s["detect"],
        "needs.detect.outputs.full_check": "true" if publish_ran else "false",
        "needs.detect.outputs.run_needed": s["run_needed"] if publish_ran else "false",
        "needs.detect.outputs.skills": s["skills"] if publish_ran else "",
        "needs.detect.outputs.upstream_new": s.get("upstream_new", "[]") if publish_ran else "",
    }


def base_context(s: dict) -> dict:
    return {
        "github.event_name": s["event"],
        "vars.AUDIT_ENABLED": s["enabled"],
        "cancelled": False,
    }


def run_jobs(s: dict, text: str) -> dict:
    """Which of checkpoint, attempt and state run for one scenario, evaluated from the workflow."""
    ctx = {**base_context(s), **detect_context(s)}
    out = {"checkpoint": evaluate(job_if(text, "checkpoint"), ctx),
           "attempt": evaluate(job_if(text, "attempt"), ctx)}
    attempt_result = ("success" if s["attempt_ok"] else "failure") if out["attempt"] else "skipped"
    ctx["needs.attempt.result"] = attempt_result
    ctx["needs.upstream-report.result"] = s.get("upstream", "skipped")
    ctx["needs.evals.result"] = s.get("evals", "skipped")
    ctx["needs.merge.result"] = s.get("merge", "skipped")
    ctx["needs.merge.outputs.update"] = s.get("merge_update", "")
    ctx["needs.apply.result"] = s.get("apply", "skipped")
    out["state"] = evaluate(job_if(text, "state"), ctx)
    return out


HAPPY = {"event": "schedule", "enabled": "true", "detect": "success", "interval_skip": "false",
         "open_pr": "false", "run_needed": "false", "skills": "[]", "attempt_ok": True}
CHANGED = {**HAPPY, "run_needed": "true", "skills": '["a"]', "attempt_ok": True,
           "upstream": "success", "evals": "success", "merge": "success", "merge_update": "true",
           "apply": "success"}


class StampTruthTable(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = workflow_text()

    def run_case(self, **changes):
        return run_jobs({**HAPPY, **changes}, self.text)

    def changed(self, **changes):
        return run_jobs({**CHANGED, **changes}, self.text)

    def test_checkpoint_stamps_only_a_clean_complete_check(self):
        cases = {
            "clean complete check": (self.run_case(), True),
            "interval not due": (self.run_case(interval_skip="true"), False),
            "audit PR already open": (self.run_case(open_pr="true"), False),
            "detect failed": (self.run_case(detect="failure"), False),
            "judging needed": (self.changed(), False),
            "schedule with the workflow disabled": (self.run_case(enabled=""), False),
            "dispatch with the workflow disabled": (self.run_case(event="workflow_dispatch", enabled=""), True),
        }
        for label, (got, want) in cases.items():
            with self.subTest(case=label):
                self.assertEqual(got["checkpoint"], want, label)

    def test_attempt_stamps_only_when_judging_is_needed(self):
        self.assertTrue(self.changed()["attempt"], "judging run must stamp last_attempt_at")
        for label, got in {
            "clean check": self.run_case(),
            "interval not due": self.changed(interval_skip="true"),
            "audit PR already open": self.changed(open_pr="true"),
            "detect failed": self.changed(detect="failure"),
        }.items():
            with self.subTest(case=label):
                self.assertFalse(got["attempt"], label)

    def test_state_never_advances_after_a_failed_or_skipped_stage(self):
        self.assertTrue(self.changed()["state"], "every stage green must advance the state")
        failures = {
            "attempt failed": self.changed(attempt_ok=False),
            "evals failed": self.changed(evals="failure"),
            "merge failed": self.changed(merge="failure"),
            "apply failed": self.changed(apply="failure"),
            "upstream failed": self.changed(upstream="failure"),
            "detect failed": self.changed(detect="failure"),
            "interval not due": self.changed(interval_skip="true"),
            "audit PR already open": self.changed(open_pr="true"),
            "merge failed without update": self.changed(merge="failure", merge_update="false", apply="skipped"),
            "apply failed without update": self.changed(merge_update="false", apply="failure"),
        }
        for label, got in failures.items():
            with self.subTest(case=label):
                self.assertFalse(got["state"], label)

    def test_state_advances_on_a_no_update_run_and_an_upstream_only_run(self):
        self.assertTrue(self.changed(merge_update="false", apply="skipped")["state"],
                        "no update needed: the state advances without an apply")
        upstream_only = {"upstream": "success", "skills": "[]", "run_needed": "true"}
        self.assertTrue(self.changed(**upstream_only)["state"], "upstream-only run advances the state")
        self.assertFalse(self.changed(skills="[]", run_needed="true", upstream="failure")["state"],
                         "upstream-only run with a failed upstream report must not advance")
        self.assertTrue(self.changed(upstream="skipped")["state"],
                        "skipped upstream report with skills advances when the rest is green")

    def test_publish_and_upload_steps_need_a_due_interval_and_no_open_pr(self):
        for name in ("Publish detect outputs after artifact upload",):
            expr = step_if(self.text, "detect", name)
            self.assertIn("steps.open-pr.outputs.open != 'true'", expr, name)
            self.assertIn("steps.interval.outputs.skip != 'true'", expr, name)
            for skip, open_pr, want in (("false", "false", True), ("true", "false", False),
                                        ("false", "true", False), ("true", "true", False)):
                ctx = {"steps.interval.outputs.skip": skip, "steps.open-pr.outputs.open": open_pr}
                with self.subTest(step=name, skip=skip, open=open_pr):
                    self.assertEqual(evaluate(expr, ctx), want)
        upload = step_if(self.text, "detect", "Publish detect outputs after artifact upload")
        self.assertIsNotNone(upload)


class UploadGateTests(unittest.TestCase):
    """U1(b): the spec upload and the detect publish both wait for the open-PR check."""

    def test_upload_and_publish_steps_are_gated_on_no_open_pr(self):
        text = workflow_text()
        for name in ("Publish detect outputs after artifact upload",):
            self.assertIn("steps.open-pr.outputs.open != 'true'", step_if(text, "detect", name), name)
        upload = re.search(r"- uses: actions/upload-artifact@\S+[^\n]*\n        if: \$\{\{ (.*) \}\}", jobs_text(text))
        self.assertIsNotNone(upload, "the detect upload-artifact step has no if")
        self.assertIn("steps.open-pr.outputs.open != 'true'", upload.group(1))


class EvaluatorSanity(unittest.TestCase):
    def test_evaluator_matches_github_rules(self):
        ctx = {"a": "x", "b": "", "github.event_name": "schedule"}
        self.assertTrue(evaluate("a == 'x'", ctx))
        self.assertFalse(evaluate("b == 'x'", ctx))
        self.assertTrue(evaluate("!cancelled()", ctx))
        self.assertTrue(evaluate("(github.event_name != 'workflow_dispatch') && a != ''", ctx))
        self.assertFalse(evaluate("github.event_name == 'workflow_dispatch' || b != ''", ctx))


if __name__ == "__main__":
    unittest.main()
