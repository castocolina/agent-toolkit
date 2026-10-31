#!/usr/bin/env python3
"""Pure outcome function for the PR review workflow (.github/workflows/skill-audit-review.yaml).

The review combines four inputs into one outcome: the gate exit codes, the
reviewer's answer, the reviewer step's own outcome and the model knob. No I/O
happens in `decide`; the CLI only reads and writes the small JSON files the
workflow passes around. Precedence, from the top (Phase 1 brief, Task A2):

  1. skipped       AUDIT_REVIEW_MODEL is empty (no gate runs, no status).
  2. changes       any gate is 1 (fail), whatever the review says.
  3. needs-human   any gate is 2 (needs-human), or a gate is absent or malformed.
  4. needs-human   the review is missing or invalid, the verdict is unsure, or
                   the reviewer step did not succeed.
  5. changes       the verdict is changes, or any finding exists.
  6. positive      every gate is 0, the verdict is approve and there are no findings.

The reviewer's self-reported confidence is never read: the answer schema has no
such field and an answer carrying extra keys is invalid.

Gate codes: 0 pass, 1 fail, 2 needs-human. Gate names are fixed.

Subcommands (CLI):
  gates     --dir DIR --out FILE       read the gate exit-code files, write gates.json,
                                       print run_review=true|false (the reviewer is skipped
                                       only when a gate failed, code 1; needs-human still
                                       runs it, so the publish step can carry its findings)
  validate  --in FILE --out FILE       validate a raw reviewer answer; write it only when valid
  outcome   --gates FILE --review FILE --reviewer-outcome X --model M --on-positive V
                                       print the outcome as JSON; always exits 0
"""
import argparse
import json
import sys
from pathlib import Path

GATES = ("scope", "check", "evals", "ci", "diff-size")
ON_POSITIVE = ("none", "label")
VERDICTS = ("approve", "changes", "unsure")
SEVERITIES = ("low", "medium", "high")
FINDING_KEYS = {"id", "file", "line", "severity", "summary"}
ANSWER_KEYS = {"verdict", "findings"}
POSITIVE_LABEL = "audit-review:positive"
LABELS = {
    "positive": POSITIVE_LABEL,
    "changes": "audit-review:changes",
    "needs-human": "audit-review:needs-human",
}
STATUS = {"positive": "success", "changes": "failure", "needs-human": "failure"}


def _nonempty_text(value) -> bool:
    return isinstance(value, str) and value.strip() != ""


def _is_int(value) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def validate_review(data):
    """Return the answer when it matches the schema, else None."""
    if not isinstance(data, dict) or set(data) != ANSWER_KEYS:
        return None
    if data["verdict"] not in VERDICTS:
        return None
    findings = data["findings"]
    if not isinstance(findings, list):
        return None
    for finding in findings:
        if not isinstance(finding, dict) or set(finding) != FINDING_KEYS:
            return None
        if not _nonempty_text(finding["id"]) or not _nonempty_text(finding["file"]):
            return None
        if not _nonempty_text(finding["summary"]):
            return None
        if not _is_int(finding["line"]) or finding["line"] < 0:
            return None
        if finding["severity"] not in SEVERITIES:
            return None
    return data


def _gate_codes(gate_set):
    """Return {name: code} when every gate is present and well-formed, else None."""
    if not isinstance(gate_set, dict) or set(gate_set) != set(GATES):
        return None
    for name in GATES:
        code = gate_set[name]
        if not _is_int(code) or code not in (0, 1, 2):
            return None
    return gate_set


def decide(gate_set, review, reviewer_outcome, model, on_positive):
    """Return {'outcome', 'status', 'label'} for one review. Pure: no I/O."""
    if on_positive not in ON_POSITIVE:
        raise ValueError(f"on_positive must be one of {ON_POSITIVE}, got {on_positive!r}")
    if not isinstance(model, str) or model.strip() == "":
        return _result("skipped")

    codes = _gate_codes(gate_set)
    if codes is None:
        return _result("needs-human", on_positive)
    if any(code == 1 for code in codes.values()):
        return _result("changes", on_positive)
    if any(code == 2 for code in codes.values()):
        return _result("needs-human", on_positive)

    answer = validate_review(review)
    if answer is None or reviewer_outcome != "success" or answer["verdict"] == "unsure":
        return _result("needs-human", on_positive)
    if answer["verdict"] == "changes" or answer["findings"]:
        return _result("changes", on_positive)
    if answer["verdict"] == "approve":
        return _result("positive", on_positive)
    return _result("needs-human", on_positive)


def _result(outcome, on_positive="label"):
    if outcome == "skipped":
        return {"outcome": "skipped", "status": "none", "label": ""}
    label = LABELS[outcome]
    if outcome == "positive" and on_positive == "none":
        label = ""
    return {"outcome": outcome, "status": STATUS[outcome], "label": label}


def gates_from_dir(directory: Path) -> dict:
    """Read one exit-code file per gate; anything absent or unreadable is needs-human (2)."""
    result = {}
    for name in GATES:
        code = 2
        try:
            text = (directory / name).read_text(encoding="utf-8").strip()
            if text in ("0", "1", "2"):
                code = int(text)
        except (OSError, UnicodeDecodeError):
            pass
        result[name] = code
    return result


def _load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, ValueError, RecursionError):
        return None


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("gates")
    g.add_argument("--dir", type=Path, required=True)
    g.add_argument("--out", type=Path, required=True)
    v = sub.add_parser("validate")
    v.add_argument("--in", dest="src", type=Path, required=True)
    v.add_argument("--out", type=Path, required=True)
    o = sub.add_parser("outcome")
    o.add_argument("--gates", type=Path, required=True)
    o.add_argument("--review", type=Path, required=True)
    o.add_argument("--reviewer-outcome", required=True)
    o.add_argument("--model", default="")
    o.add_argument("--on-positive", default="label")
    args = parser.parse_args(argv)

    if args.cmd == "gates":
        codes = gates_from_dir(args.dir)
        args.out.write_text(json.dumps(codes, sort_keys=True) + "\n", encoding="utf-8")
        run_review = all(code != 1 for code in codes.values())
        print(f"run_review={'true' if run_review else 'false'}")
        return 0

    if args.cmd == "validate":
        answer = validate_review(_load(args.src))
        if answer is None:
            print("review-combine: reviewer answer is not valid JSON or violates the schema", file=sys.stderr)
            return 1
        args.out.write_text(json.dumps(answer, sort_keys=True) + "\n", encoding="utf-8")
        return 0

    if args.cmd == "outcome":
        review = _load(args.review) if args.review.is_file() else None
        try:
            result = decide(_load(args.gates), review, args.reviewer_outcome, args.model, args.on_positive)
        except ValueError as exc:
            # The publish step must always get an outcome: an invalid input is needs-human, never a crash.
            print(f"review-combine: {exc}", file=sys.stderr)
            result = _result("needs-human")
        print(json.dumps(result, sort_keys=True))
        return 0

    return 2


if __name__ == "__main__":
    sys.exit(main())
