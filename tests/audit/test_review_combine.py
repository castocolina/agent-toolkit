"""Unit tests for .github/audit/review-combine.py (the PR review outcome).

The outcome is a pure function of the gate results, the reviewer answer, the
reviewer step outcome, the model knob and AUDIT_ON_POSITIVE. These tests pin
the precedence from the Phase 1 brief (Task A2, 'Outcomes').
"""
import importlib.util
import io
import itertools
import json
import contextlib
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("review_combine", ROOT / ".github/audit/review-combine.py")
rc = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(rc)

GATES = ("scope", "check", "evals", "ci", "diff-size")
PASS = {g: 0 for g in GATES}
POSITIVE_LABEL = "audit-review:positive"


def gates(**overrides):
    value = dict(PASS)
    for key, code in overrides.items():
        value[key.replace("_", "-")] = code
    return value


def review(verdict="approve", findings=None):
    return {"verdict": verdict, "findings": findings or []}


FINDING = {"id": "f1", "file": "skills/a/SKILL.md", "line": 3, "severity": "low", "summary": "typo"}


class CombineMatrixTests(unittest.TestCase):
    def test_combine_matrix(self):
        cases = [
            # (gates, review, reviewer outcome, model, on_positive, expected outcome, status, label)
            (PASS, review("approve"), "success", "m", "label", "positive", "success", POSITIVE_LABEL),
            (PASS, review("approve"), "success", "m", "none", "positive", "success", ""),
            (PASS, review("changes"), "success", "m", "label", "changes", "failure", "audit-review:changes"),
            (PASS, review("approve", [FINDING]), "success", "m", "label", "changes", "failure", "audit-review:changes"),
            (PASS, review("unsure"), "success", "m", "label", "needs-human", "failure", "audit-review:needs-human"),
            (PASS, None, "success", "m", "label", "needs-human", "failure", "audit-review:needs-human"),
            (PASS, review("approve"), "failure", "m", "label", "needs-human", "failure", "audit-review:needs-human"),
            (PASS, review("approve"), "skipped", "m", "label", "needs-human", "failure", "audit-review:needs-human"),
            (gates(scope=1), review("approve"), "skipped", "m", "label", "changes", "failure", "audit-review:changes"),
            (gates(check=1), review("approve"), "success", "m", "label", "changes", "failure", "audit-review:changes"),
            (gates(evals=1), review("changes"), "success", "m", "label", "changes", "failure", "audit-review:changes"),
            (gates(ci=2), review("approve"), "success", "m", "label", "needs-human", "failure", "audit-review:needs-human"),
            (gates(diff_size=2), review("approve"), "success", "m", "label", "needs-human", "failure", "audit-review:needs-human"),
            (gates(evals=2), review("changes"), "success", "m", "label", "needs-human", "failure", "audit-review:needs-human"),
            (PASS, review("approve"), "success", "", "label", "skipped", "none", ""),
            (gates(scope=1), None, "skipped", "", "label", "skipped", "none", ""),
        ]
        for case in cases:
            gate_set, rev, reviewer, model, on_positive, outcome, status, label = case
            with self.subTest(case=case):
                got = rc.decide(gate_set, rev, reviewer, model, on_positive)
                self.assertEqual(got, {"outcome": outcome, "status": status, "label": label})

    def test_full_product_never_positive_unless_clean(self):
        """Exhaustive over gate codes, verdicts, findings and reviewer outcomes."""
        codes = (0, 1, 2)
        verdicts = ("approve", "changes", "unsure", None)
        finding_sets = ([], [FINDING])
        reviewers = ("success", "failure", "skipped")
        for combo in itertools.product(codes, codes, codes, codes, codes, verdicts, finding_sets, reviewers):
            gate_codes, verdict, findings, reviewer = combo[:5], combo[5], combo[6], combo[7]
            gate_set = dict(zip(GATES, gate_codes))
            rev = None if verdict is None else review(verdict, findings)
            got = rc.decide(gate_set, rev, reviewer, "m", "label")
            if got["outcome"] == "positive":
                self.assertEqual(set(gate_codes), {0})
                self.assertEqual(verdict, "approve")
                self.assertEqual(findings, [])
                self.assertEqual(reviewer, "success")


class PrecedenceTests(unittest.TestCase):
    def test_positive_needs_zero_findings(self):
        self.assertEqual(rc.decide(PASS, review("approve"), "success", "m", "label")["outcome"], "positive")
        self.assertEqual(rc.decide(PASS, review("approve", [FINDING]), "success", "m", "label")["outcome"], "changes")

    def test_unsure_is_needs_human(self):
        got = rc.decide(PASS, review("unsure"), "success", "m", "label")
        self.assertEqual(got["outcome"], "needs-human")
        self.assertEqual(got["status"], "failure")

    def test_empty_model_is_skipped(self):
        for model in ("", "   "):
            got = rc.decide(gates(scope=1), None, "skipped", model, "label")
            self.assertEqual(got, {"outcome": "skipped", "status": "none", "label": ""})

    def test_missing_review_json_is_needs_human(self):
        self.assertEqual(rc.decide(PASS, None, "success", "m", "label")["outcome"], "needs-human")
        self.assertEqual(rc.decide(PASS, {"verdict": "approve"}, "success", "m", "label")["outcome"], "needs-human")

    def test_reviewer_failure_still_publishes(self):
        """A failed reviewer is a normal outcome: needs-human with a failure status, not an exception."""
        got = rc.decide(PASS, review("approve"), "failure", "m", "label")
        self.assertEqual(got, {"outcome": "needs-human", "status": "failure", "label": "audit-review:needs-human"})

    def test_on_positive_none_adds_no_label(self):
        got = rc.decide(PASS, review("approve"), "success", "m", "none")
        self.assertEqual(got, {"outcome": "positive", "status": "success", "label": ""})
        self.assertEqual(rc.decide(PASS, review("changes"), "success", "m", "none")["label"], "audit-review:changes")

    def test_gate_failure_dominates_missing_review(self):
        got = rc.decide(gates(check=1), None, "skipped", "m", "label")
        self.assertEqual(got["outcome"], "changes")

    def test_gate_needs_human_beats_approve(self):
        got = rc.decide(gates(ci=2), review("approve"), "success", "m", "label")
        self.assertEqual(got["outcome"], "needs-human")

    def test_absent_or_malformed_gate_is_needs_human(self):
        bad_gates = [
            None,
            {},
            {g: 0 for g in GATES if g != "ci"},
            dict(PASS, extra=0),
            dict(PASS, ci="0"),
            dict(PASS, ci=True),
            dict(PASS, ci=3),
            dict(PASS, ci=None),
            dict(PASS, ci=-1),
        ]
        for value in bad_gates:
            with self.subTest(gates=value):
                got = rc.decide(value, review("approve"), "success", "m", "label")
                self.assertEqual(got["outcome"], "needs-human")

    def test_invalid_on_positive_is_rejected(self):
        with self.assertRaises(ValueError):
            rc.decide(PASS, review("approve"), "success", "m", "always")


class ValidateReviewTests(unittest.TestCase):
    def test_valid_answers(self):
        self.assertIsNotNone(rc.validate_review(review("approve")))
        self.assertIsNotNone(rc.validate_review(review("changes", [FINDING])))

    def test_schema_violations_are_rejected(self):
        bad = [
            "not an object",
            [],
            {"verdict": "approve"},
            {"verdict": "approve", "findings": [], "confidence": 0.9},
            {"verdict": "maybe", "findings": []},
            {"verdict": "approve", "findings": {}},
            {"verdict": "approve", "findings": [dict(FINDING, severity="critical")]},
            {"verdict": "approve", "findings": [dict(FINDING, line="3")]},
            {"verdict": "approve", "findings": [dict(FINDING, line=True)]},
            {"verdict": "approve", "findings": [dict(FINDING, line=-1)]},
            {"verdict": "approve", "findings": [{k: v for k, v in FINDING.items() if k != "summary"}]},
            {"verdict": "approve", "findings": [dict(FINDING, extra=1)]},
            {"verdict": "approve", "findings": [dict(FINDING, summary="  ")]},
            {"verdict": "approve", "findings": [dict(FINDING, id="")]},
        ]
        for value in bad:
            with self.subTest(value=value):
                self.assertIsNone(rc.validate_review(value))


class GatesFileTests(unittest.TestCase):
    def test_gates_json_built_from_exit_codes(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            for name, text in {"scope": "0\n", "check": "1\n", "evals": "0", "ci": "2", "diff-size": "0"}.items():
                (tmp / name).write_text(text)
            built = rc.gates_from_dir(tmp)
            self.assertEqual(built, {"scope": 0, "check": 1, "evals": 0, "ci": 2, "diff-size": 0})

    def test_missing_or_unreadable_gate_file_is_needs_human(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "scope").write_text("0")
            (tmp / "check").write_text("banana")
            (tmp / "evals").write_text("7")
            built = rc.gates_from_dir(tmp)
            self.assertEqual(built["scope"], 0)
            self.assertEqual(built["check"], 2)
            self.assertEqual(built["evals"], 2)
            self.assertEqual(built["ci"], 2)
            self.assertEqual(built["diff-size"], 2)


class CliTests(unittest.TestCase):
    def run_cli(self, argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = rc.main(argv)
        return code, out.getvalue()

    def test_cli_gates_prints_run_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            gdir = tmp / "gates"
            gdir.mkdir()
            for name in GATES:
                (gdir / name).write_text("0")
            (gdir / "ci").write_text("1")
            code, out = self.run_cli(["gates", "--dir", str(gdir), "--out", str(tmp / "gates.json")])
            self.assertEqual(code, 0)
            self.assertIn("run_review=false", out.split())
            self.assertEqual(json.loads((tmp / "gates.json").read_text())["ci"], 1)

    def test_cli_validate_writes_only_valid_answers(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "raw.json").write_text(json.dumps(review("approve")))
            code, _ = self.run_cli(["validate", "--in", str(tmp / "raw.json"), "--out", str(tmp / "review.json")])
            self.assertEqual(code, 0)
            self.assertTrue((tmp / "review.json").is_file())
            (tmp / "bad.json").write_text("Sure! {\"verdict\": \"approve\"}")
            code, _ = self.run_cli(["validate", "--in", str(tmp / "bad.json"), "--out", str(tmp / "bad-out.json")])
            self.assertNotEqual(code, 0)
            self.assertFalse((tmp / "bad-out.json").exists())

    def test_cli_outcome_handles_missing_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "gates.json").write_text(json.dumps(PASS))
            code, out = self.run_cli([
                "outcome", "--gates", str(tmp / "gates.json"), "--review", str(tmp / "absent.json"),
                "--reviewer-outcome", "skipped", "--model", "m", "--on-positive", "label",
            ])
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(out)["outcome"], "needs-human")
            code, out = self.run_cli([
                "outcome", "--gates", str(tmp / "absent-gates.json"), "--review", str(tmp / "absent.json"),
                "--reviewer-outcome", "success", "--model", "m", "--on-positive", "label",
            ])
            self.assertEqual(json.loads(out)["outcome"], "needs-human")

    def test_cli_outcome_never_raises_and_publishes_needs_human(self):
        # An invalid knob or a crash in decide must still yield an outcome (always exits 0).
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "gates.json").write_text(json.dumps(PASS))
            (tmp / "review.json").write_text(json.dumps(review("approve")))
            code, out = self.run_cli([
                "outcome", "--gates", str(tmp / "gates.json"), "--review", str(tmp / "review.json"),
                "--reviewer-outcome", "success", "--model", "m", "--on-positive", "always",
            ])
            self.assertEqual(code, 0)
            result = json.loads(out)
            self.assertEqual(result["outcome"], "needs-human")
            self.assertEqual(result["status"], "failure")
            self.assertEqual(result["label"], "audit-review:needs-human")


if __name__ == "__main__":
    unittest.main()
