#!/usr/bin/env python3
"""Assemble the body-only PR body prompt (and its plain fallback) for the apply job.

The read-only Copilot body generator cannot run git or gh, so the caller passes
it the diff stat, a trimmed diff and the decision rationale as prompt evidence
and collects the body from stdout. The diff is capped (--diff-cap bytes, ~60KB
in the workflow) so one oversized audit commit cannot blow up the prompt. The
fallback subcommand renders a plain summary for the case where Copilot fails or
returns an empty body; it never calls Copilot itself.

Usage:
  pr-body-prompt.py prompt --template T --decision D --diagrams mermaid --diff-cap N --out F
  pr-body-prompt.py fallback --decision D [--diff-cap N] --out F
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

PLACEHOLDER = re.compile(r"\{\{([A-Z_][A-Z0-9_]*)\}\}")


def run_git(*args: str) -> str:
    proc = subprocess.run(["git", *args], capture_output=True, text=True)
    if proc.returncode:
        raise SystemExit(f"pr-body-prompt: git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout


def diff_stat() -> str:
    return run_git("show", "--stat=120", "--format=commit %h %s", "HEAD").strip()


def full_diff() -> str:
    return run_git("show", "--format=", "--no-color", "HEAD")


def trim(text: str, cap: int) -> str:
    data = text.encode("utf-8")
    if len(data) <= cap:
        return text
    cut = data[:cap]
    newline = cut.rfind(b"\n")
    if newline > 0:
        cut = cut[:newline]
    return cut.decode("utf-8", errors="replace") + \
        f"\n... [diff truncated at {cap} bytes; see the audit commit in the repository] ...\n"


def load_decision(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise SystemExit(f"pr-body-prompt: cannot read decision {path}: {exc}")
    for key in ("title", "rationale", "targets"):
        if key not in data:
            raise SystemExit(f"pr-body-prompt: decision {path} is missing {key}")
    if not isinstance(data["targets"], list) or any(not isinstance(t, str) for t in data["targets"]):
        raise SystemExit(f"pr-body-prompt: decision {path} has invalid targets")
    return data


def fill(template: str, values: dict[str, str]) -> str:
    """Substitute once over the template only.

    The template's own placeholders are validated before substituting, so
    evidence text containing literal {{LIKE_THIS}} markers (diff lines,
    rationale) survives unchanged instead of aborting the render.
    """
    unresolved = sorted(set(PLACEHOLDER.findall(template)) - set(values))
    if unresolved:
        raise SystemExit("pr-body-prompt: unresolved placeholders: " + ", ".join(unresolved))
    return PLACEHOLDER.sub(lambda match: values[match.group(1)], template)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    prompt = sub.add_parser("prompt", help="render the body-only Copilot prompt")
    prompt.add_argument("--template", type=Path, required=True)
    prompt.add_argument("--decision", type=Path, required=True)
    prompt.add_argument("--diagrams", choices=["none", "mermaid"], required=True,
                        help="drawio is normalized to mermaid by the caller")
    prompt.add_argument("--diff-cap", type=int, default=61440)
    prompt.add_argument("--out", type=Path, required=True)
    fallback = sub.add_parser("fallback", help="render the plain summary fallback body")
    fallback.add_argument("--decision", type=Path, required=True)
    fallback.add_argument("--diff-cap", type=int, default=61440)
    fallback.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    decision = load_decision(args.decision)
    targets = ", ".join(decision["targets"]) or "none"
    if args.cmd == "prompt":
        values = {
            "TITLE": str(decision["title"]),
            "TYPE": decision.get("type", "unknown"),
            "TARGETS": targets,
            "RATIONALE": str(decision["rationale"]).strip(),
            "DIFF_STAT": diff_stat(),
            "DIFF": trim(full_diff(), args.diff_cap),
            "DIAGRAMS": args.diagrams,
        }
        template = args.template.read_text(encoding="utf-8")
        args.out.write_text(fill(template, values), encoding="utf-8")
    else:
        body = (
            f"# PR Summary: {decision['title']}\n\n"
            "Automated scheduled skill audit; the generated body was unavailable, "
            "so this is the plain decision summary.\n\n"
            f"- Type: {decision.get('type', 'unknown')}\n"
            f"- Targets: {targets}\n\n"
            "## Rationale\n\n"
            f"{str(decision['rationale']).strip()}\n\n"
            "## Diff stat\n\n"
            f"```\n{diff_stat()}\n```\n"
        )
        args.out.write_text(body, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
