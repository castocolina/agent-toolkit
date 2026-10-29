#!/usr/bin/env python3
"""Audit helpers for skills: check, rubric-check, slug, split-verdicts, validate-verdict, merge, run-evals, pi-cmd.

Usage:
    python3 scripts/audit/audit.py [--root DIR] check [--strict] [--skills a,b] [--ignore CODE,...]
    python3 scripts/audit/audit.py rubric-check [--rubric FILE]
    python3 scripts/audit/audit.py slug MODEL
    python3 scripts/audit/audit.py split-verdicts --judge MODEL --out DIR < judge_stdout
    python3 scripts/audit/audit.py validate-verdict [--rubric FILE] FILE...
    python3 scripts/audit/audit.py merge --in DIR --out DIR --judges m1,m2 [--skills x,y] [--check FILE]
        [--waivers FILE] [--min-judges N] [--allow-incomplete] [--rubric FILE] [--upstream-findings FILE]
    python3 scripts/audit/audit.py run-evals --skills a,b --runner CMD [--timeout S] [--triggers] [--runs N]
        [--out DIR] [--fail-under 0.8]
    python3 scripts/audit/audit.py pi-cmd runner|judge [--model ID] [--print0]
"""

import argparse
import contextlib
import datetime
import json
import math
import os
import re
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

SYNCED = {"gepetto", "datadog-cli"}
C5_FIELDS = {"user-invocable", "disable-model-invocation", "argument-hint"}
DIMENSIONS = [f"D{i}" for i in range(1, 9)]
SKILL_NAME_RE = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")

# unicodedata has no script property, so the scripts are listed by codepoint range.
NON_LATIN_RANGES = [
    (0x3400, 0x4DBF), (0x4E00, 0x9FFF), (0xF900, 0xFAFF), (0x20000, 0x2EBEF),  # Han
    (0x3040, 0x309F),  # Hiragana
    (0x30A0, 0x30FF), (0x31F0, 0x31FF),  # Katakana
    (0x1100, 0x11FF), (0x3130, 0x318F), (0xAC00, 0xD7AF),  # Hangul
    (0x0400, 0x052F),  # Cyrillic
    (0x0600, 0x06FF), (0x0750, 0x077F),  # Arabic
    (0x0590, 0x05FF),  # Hebrew
    (0x0E00, 0x0E7F),  # Thai
    (0x0900, 0x097F),  # Devanagari
    (0x0370, 0x03FF), (0x1F00, 0x1FFF),  # Greek
]
NON_LATIN_RE = re.compile(
    "[" + "".join(f"{chr(a)}-{chr(b)}" for a, b in NON_LATIN_RANGES) + "]"
)
VERBATIM_DIR = Path("references") / "agentskills"
SEVERITIES = ("critical", "high", "medium", "low")  # most severe first
VERDICT_KEYS = {"skill", "judge", "rubric_version", "spec_sha", "scores", "max", "total", "max_total",
                "percent", "grade", "findings"}  # = verdict.schema.json properties
FINDING_KEYS = {"id", "dimension", "severity", "file", "line", "evidence", "fix"}
SKILLS_REF_TIMEOUT = 600
KILL_DRAIN_TIMEOUT = 5  # seconds to drain a killed runner's pipes
TARGET = 80
EVAL_ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
SANDBOX_PREAMBLE = (
    "You have no tools, network or shell. Do not try to run anything; "
    "show the exact commands, calls and file contents you would use instead."
)
PI_BASE = ["pi", "-p", "--no-mcp", "--no-extensions", "--no-skills", "--no-context-files", "--no-session"]
DEFAULT_JUDGE_MODEL = "router-env/my-referee-one"

C5_ERROR_RE = re.compile(
    r"^Unexpected fields in frontmatter: (.+?)\. Only \[.*\] are allowed\.$"
)
ERROR_LINE_RE = re.compile(r"^\s+- (.+)$")


def default_root() -> Path:
    return Path(__file__).resolve().parents[2]


def judge_refs(root: Path) -> Path:
    return root / "skills" / "skill-judge" / "references"


def resolve_rubric(root: Path, given: Path | None) -> Path:
    """The rubric to use; ValueError naming the path when absent (skill-judge ships in a later PR)."""
    path = given or judge_refs(root) / "rubric.md"
    if not path.is_file():
        raise ValueError(f"audit.py: rubric not found: {given or path.relative_to(root)}" + ("" if given else " (pass --rubric)"))
    return path


# ---------- skills-ref ----------


def source_sha(root: Path) -> str:
    """The pinned spec sha from SOURCE.json; ValueError when unreadable."""
    path = judge_refs(root) / "agentskills" / "SOURCE.json"
    try:
        return json.loads(path.read_text())["sha"]
    except (OSError, ValueError, KeyError, TypeError, RecursionError) as e:
        raise ValueError(f"cannot read sha from {path}: {e}") from e


def run_skills_ref(root: Path, skill_dir: Path) -> tuple[int, str]:
    """Run the pinned skills-ref validator; return (exit code, combined output)."""
    sha = source_sha(root)
    src = f"git+https://github.com/agentskills/agentskills@{sha}#subdirectory=skills-ref"
    try:
        p = subprocess.run(
            ["uvx", "--from", src, "skills-ref", "validate", str(skill_dir)],
            capture_output=True, text=True, timeout=SKILLS_REF_TIMEOUT,
        )
    except FileNotFoundError as e:
        return 127, str(e)
    except subprocess.TimeoutExpired:
        return 124, f"skills-ref timed out after {SKILLS_REF_TIMEOUT}s"
    return p.returncode, p.stdout + p.stderr


def parse_skills_ref(code: int, text: str) -> list[str]:
    """Return the skills-ref error details that count as issues (empty = ok)."""
    if code == 0:
        return []
    errors = [m.group(1) for ln in text.splitlines() if (m := ERROR_LINE_RE.match(ln))]
    if not errors:  # unparseable output is never silently ok
        return [text.strip()[:500] or f"skills-ref exited {code} with no output"]
    kept = []
    for e in errors:
        m = C5_ERROR_RE.match(e)
        if m and all(f in C5_FIELDS for f in re.split(r"[,\s]+", m.group(1).strip()) if f):
            continue
        kept.append(e)
    return kept


# ---------- frontmatter ----------


def parse_frontmatter(text: str) -> dict[str, str]:
    """Top-level scalar keys only (plain, quoted, or | / > block scalars)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    fm: dict[str, str] = {}
    i = 1
    while i < len(lines) and lines[i].strip() != "---":
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", lines[i])
        i += 1
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        block = []
        while i < len(lines) and lines[i].strip() != "---" and (
            not lines[i].strip() or lines[i][0] in " \t"
        ):
            block.append(lines[i].strip())
            i += 1
        if val.startswith(("|", ">")):
            sep = "\n" if val[0] == "|" else " "
            val = sep.join(block).strip()
        elif val[:1] == '"' and val.endswith('"') and len(val) > 1:
            try:
                val = json.loads(val)
            except (ValueError, RecursionError):
                val = val[1:-1]
        elif val[:1] == "'" and val.endswith("'") and len(val) > 1:
            val = val[1:-1].replace("''", "'")
        elif block:
            val = " ".join([val] + [b for b in block if b]).strip()
        fm[key] = val
    return fm


# ---------- check ----------


def load_allowlist(path: Path) -> set[str]:
    if not path.is_file():
        return set()
    return {
        ln.strip() for ln in path.read_text(encoding="utf-8").splitlines()
        if ln.strip() and not ln.lstrip().startswith("#")
    }


def non_latin_hits(root: Path, sdir: Path, allow: set[str]) -> list[str]:
    """One 'path:line,line' entry per file with non-allowlisted non-Latin lines."""
    out = []
    for f in sorted(p for p in sdir.rglob("*") if p.is_file()):
        if (sdir / VERBATIM_DIR) in f.parents:
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue  # binary
        rel = f.relative_to(root).as_posix()
        hits = [
            n for n, ln in enumerate(text.split("\n"), 1)
            if NON_LATIN_RE.search(ln) and f"{rel}:{n}" not in allow
        ]
        if hits:
            out.append(f"{rel}:{','.join(map(str, hits))}")
    return out


def valid_json_file(p: Path) -> bool:
    try:
        json.loads(p.read_text(encoding="utf-8"))
        return True
    except (OSError, ValueError, RecursionError):
        return False


def skill_issues(root: Path, name: str, allow: set[str]) -> list[tuple[str, str]]:
    sdir = root / "skills" / name
    synced = name in SYNCED
    found: list[tuple[str, str]] = []

    if judge_refs(root).is_dir():  # the spec pin lives in skill-judge; absent before that skill ships
        code, text = run_skills_ref(root, sdir)
        details = parse_skills_ref(code, text)
        if details:
            found.append(("skills_ref", "; ".join(details)))

    md = sdir / "SKILL.md"
    content = md.read_text(encoding="utf-8") if md.is_file() else ""
    n_lines = len(content.splitlines())
    if n_lines >= 500:
        found.append(("lines_over_500", f"SKILL.md has {n_lines} lines"))
    fm = parse_frontmatter(content)
    if len(fm.get("description", "")) > 1024:
        found.append(("description_too_long", f"{len(fm['description'])} chars"))
    if fm.get("name") != name:
        found.append(("name_mismatch", f"frontmatter name {fm.get('name')!r} != directory {name!r}"))
    if not (sdir / "README.md").is_file() and not synced:
        found.append(("missing_readme", "README.md absent"))
    for hit in non_latin_hits(root, sdir, allow):
        found.append(("non_latin", hit))
    if not synced:
        ev = sdir / "evals"
        bad = [f for f in ("evals.json", "trigger-queries.json") if not valid_json_file(ev / f)]
        if bad:
            found.append(("missing_evals", "absent or invalid: " + ", ".join(f"evals/{f}" for f in bad)))
        has_scripts = (sdir / "scripts").is_dir() and any(
            p.is_file() for p in (sdir / "scripts").rglob("*")
        )
        tdir = root / "tests" / "skills" / name
        if has_scripts and not (list(tdir.glob("test-*.sh")) + list(tdir.glob("test_*.py"))):
            found.append(("missing_script_tests", f"scripts/ has files but no tests/skills/{name}/test-*.sh or test_*.py"))
    return found


def check_skills(
    root: Path, skills: list[str] | None = None, strict: bool = False,
    ignore: set[str] | None = None, allowlist: Path | None = None,
) -> dict:
    ignore = ignore or set()
    allow = load_allowlist(allowlist or root / "scripts" / "audit" / "non_latin_allowlist.txt")
    if not judge_refs(root).is_dir():
        print(f"audit.py: skills-ref skipped: spec pin not found: {judge_refs(root).relative_to(root) / 'agentskills' / 'SOURCE.json'}",
              file=sys.stderr)
    names = skills or sorted(p.name for p in (root / "skills").iterdir() if p.is_dir())
    for name in names:
        if not SKILL_NAME_RE.fullmatch(name) or not (root / "skills" / name).is_dir():
            raise ValueError(f"invalid skill {name!r}: not a kebab-case directory under skills/")
    result = []
    for name in names:
        issues = [
            {"code": c, "detail": d, "ignored": c in ignore}
            for c, d in skill_issues(root, name, allow)
        ]
        result.append({
            "name": name,
            "ok": all(i["ignored"] for i in issues),
            "synced": name in SYNCED,
            "issues": issues,
        })
    return {"skills": result}


# ---------- rubric ----------


def load_rubric(path: Path) -> dict:
    """Parse the rubric front block and table; raise ValueError when malformed."""
    lines = path.read_text(encoding="utf-8").splitlines()
    m1 = re.fullmatch(r"rubric_version: (\d+)", lines[0]) if lines else None
    m2 = re.fullmatch(r"spec_sha: ([0-9a-f]{40})", lines[1]) if len(lines) > 1 else None
    if not m1 or not m2:
        raise ValueError("front block must start with 'rubric_version: <int>' and 'spec_sha: <40 hex>'")
    maxes: dict[str, int] = {}
    for ln in lines[2:]:
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) >= 3 and re.fullmatch(r"D\d+", cells[0]):
            if not cells[2].isdigit():
                raise ValueError(f"{cells[0]}: max {cells[2]!r} is not an integer")
            if cells[0] in maxes:
                raise ValueError(f"{cells[0]}: duplicated dimension row")
            maxes[cells[0]] = int(cells[2])
    return {"version": int(m1.group(1)), "spec_sha": m2.group(1), "max": maxes}


def rubric_check(root: Path, rubric: Path) -> list[str]:
    """Return reasons the rubric is invalid (empty = ok)."""
    try:
        r = load_rubric(rubric)
    except (OSError, ValueError) as e:
        return [str(e)]
    reasons = [f"{d}: missing or max <= 0" for d in DIMENSIONS if r["max"].get(d, 0) <= 0]
    try:
        sha = source_sha(root)
    except ValueError as e:
        return reasons + [str(e)]
    if r["spec_sha"] != sha:
        reasons.append(f"spec_sha {r['spec_sha']} != SOURCE.json sha {sha}")
    return reasons


# ---------- slug / split-verdicts ----------


def slug(model: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", model.lower()).strip("-")


def split_verdicts(model: str, out: Path, lines) -> None:
    base = out / slug(model)
    seen: set[str] = set()
    for raw in lines:
        raw = raw.rstrip("\n")
        if not raw.strip():
            continue
        try:
            obj = json.loads(raw)
        except (ValueError, RecursionError):
            print(f"skipped (not JSON): {raw[:500]}", file=sys.stderr)
            continue
        skill = obj.get("skill") if isinstance(obj, dict) else None
        if not isinstance(skill, str) or not SKILL_NAME_RE.fullmatch(skill):
            print(f"skipped (bad skill): {raw}", file=sys.stderr)
            continue
        dest = (base / f"{skill}.json").resolve()
        if not dest.is_relative_to(base.resolve()):
            print(f"skipped (outside output dir): {raw}", file=sys.stderr)
            continue
        if skill in seen:
            print(f"duplicate verdict for {skill}: keeping the last one", file=sys.stderr)
        seen.add(skill)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")


# ---------- validate-verdict ----------


def is_int(v) -> bool:
    return isinstance(v, int) and not isinstance(v, bool)


def grade_of(percent: float) -> str:
    return next((g for g, floor in (("A", 90), ("B", 80), ("C", 70), ("D", 60)) if percent >= floor), "F")


def _reject_constant(name: str):
    raise ValueError(f"{name} is not valid JSON")


def validate_verdict(data, path: Path, rubric: dict) -> list[str]:
    """Return the reasons a verdict is invalid (empty = ok)."""
    if not isinstance(data, dict):
        return ["not a JSON object"]
    errs: list[str] = [f"{k}: unexpected key" for k in sorted(set(data) - VERDICT_KEYS)]
    for key, ok in (
        ("skill", isinstance(data.get("skill"), str)), ("judge", isinstance(data.get("judge"), str)),
        ("spec_sha", isinstance(data.get("spec_sha"), str)), ("grade", isinstance(data.get("grade"), str)),
        ("rubric_version", is_int(data.get("rubric_version"))), ("total", is_int(data.get("total"))),
        ("max_total", is_int(data.get("max_total"))),
        ("percent", is_int(data.get("percent"))
         or (isinstance(data.get("percent"), float) and math.isfinite(data["percent"]))),
        ("findings", isinstance(data.get("findings"), list)),
    ):
        if not ok:
            errs.append(f"{key}: missing or wrong type")
    for key in ("scores", "max"):
        v = data.get(key)
        if not isinstance(v, dict) or set(v) != set(DIMENSIONS) or not all(is_int(x) for x in v.values()):
            errs.append(f"{key}: must hold exactly D1..D8 integers")
    if errs:
        return errs
    for d in DIMENSIONS:
        if data["max"][d] != rubric["max"].get(d):
            errs.append(f"max.{d}: {data['max'][d]} != rubric {rubric['max'].get(d)}")
        elif not 0 <= data["scores"][d] <= data["max"][d]:
            errs.append(f"scores.{d}: {data['scores'][d]} outside 0..{data['max'][d]}")
    if errs:
        return errs
    total, max_total = sum(data["scores"].values()), sum(data["max"].values())
    percent = round(total / max_total * 100, 1)
    for key, got, want in (
        ("total", data["total"], total), ("max_total", data["max_total"], max_total),
        ("percent", data["percent"], percent), ("grade", data["grade"], grade_of(percent)),
        ("rubric_version", data["rubric_version"], rubric["version"]),
        ("spec_sha", data["spec_sha"], rubric["spec_sha"]),
        ("skill", data["skill"], path.stem), ("judge", data["judge"], path.parent.name),
    ):
        if got != want:
            errs.append(f"{key}: {got!r} != expected {want!r}")
    for i, f in enumerate(data["findings"]):
        bad = (
            not isinstance(f, dict)
            or set(f) != FINDING_KEYS
            or any(not isinstance(f.get(k), str) or not f[k] for k in ("id", "file", "evidence", "fix"))
            or not isinstance(f.get("dimension"), str) or f["dimension"] not in DIMENSIONS
            or not isinstance(f.get("severity"), str) or f["severity"] not in SEVERITIES
            or "line" not in f or not (f["line"] is None or (is_int(f["line"]) and f["line"] >= 1))
        )
        if bad:
            errs.append(f"findings[{i}]: invalid or missing field")
    ids = [f["id"] for f in data["findings"] if isinstance(f, dict) and isinstance(f.get("id"), str)]
    errs += [f"findings: duplicate id {i!r}" for i, n in Counter(ids).items() if n > 1]
    return errs


def read_verdict(path: Path, rubric: dict) -> tuple[dict | None, list[str]]:
    """Parse and validate one verdict file; the data is None when invalid."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"), parse_constant=_reject_constant)
    except (OSError, ValueError, RecursionError) as e:
        return None, [f"not valid JSON: {e}"]
    errs = validate_verdict(data, path, rubric)
    return (None if errs else data), errs


# ---------- merge ----------


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, RecursionError) as e:
        raise ValueError(f"cannot read {path}: {e}") from e


def merge_verdicts(
    root: Path, in_dir: Path, out_dir: Path, judges: list[str], skills: list[str] | None,
    check: Path | None, waivers: Path | None, min_judges: int, allow_incomplete: bool,
    rubric: Path, upstream_findings: Path,
) -> int:
    r = load_rubric(rubric)
    names = skills or sorted(p.name for p in (root / "skills").iterdir() if p.is_dir())
    slugs = list(dict.fromkeys(slug(j) for j in judges))
    checks = {e["name"]: e for e in load_json(check)["skills"]} if check else None
    waived_at: dict[str, float] = {}
    for w in load_json(waivers) if waivers else []:  # several entries per skill: the lowest bar counts
        waived_at[w["skill"]] = min(w["percent"], waived_at.get(w["skill"], w["percent"]))

    entries, upstream, complete, needs_update = [], [], True, False
    for name in names:
        verdicts, missing = {}, []
        for j in slugs:
            path = in_dir / j / f"{name}.json"
            data, errs = read_verdict(path, r) if path.is_file() else (None, [])
            for e in errs:
                print(f"{path}: {e}", file=sys.stderr)
            if data:
                verdicts[j] = data
            else:
                missing.append(j)
        complete &= len(verdicts) >= min_judges
        percents = {j: v["percent"] for j, v in verdicts.items()}
        mean = round(sum(percents.values()) / len(percents), 1) if percents else None
        kept: dict[tuple, dict] = {}  # duplicate key: the most severe copy wins, first-seen order kept
        for v in verdicts.values():
            for f in v["findings"]:
                key = (f["dimension"], f["file"], f["fix"].lower())
                if key not in kept or SEVERITIES.index(f["severity"]) < SEVERITIES.index(kept[key]["severity"]):
                    kept[key] = f
        findings = list(kept.values())
        synced = name in SYNCED
        entry_check = checks.get(name) if checks is not None else None
        issues = entry_check["issues"] if entry_check else []
        waived = mean is not None and name in waived_at and waived_at[name] <= mean
        if synced:
            if findings or issues:
                upstream.append((name, findings, issues))
            findings, issues = [], []
        else:
            needs_update |= (
                (mean is None or mean < TARGET) and not waived
                or any(f["severity"] in ("critical", "high") for f in findings)
                or any(not i["ignored"] for i in issues)
            )
        entries.append({
            "name": name, "percent": mean, "grade": grade_of(mean) if mean is not None else "UNJUDGED",
            "judges": percents, "missing_judges": missing,
            "disagreement": bool(percents) and round(max(percents.values()) - min(percents.values()), 1) > 10,
            "synced": synced, "waived": waived,
            "skills_ref_valid": None if synced or entry_check is None else not any(
                i["code"] == "skills_ref" and not i["ignored"] for i in issues
            ),
            "check_issues": issues, "findings": findings,
        })

    merged = {
        "rubric_version": r["version"], "spec_sha": r["spec_sha"], "complete": complete,
        "skills": entries, "needs_update": needs_update,
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "merged.json").write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")
    (out_dir / "report.md").write_text(render_report(entries, upstream_findings), encoding="utf-8")
    heading = f"\n## {out_dir}\n"  # re-running on the same --out must not append the section twice
    if upstream and heading not in (upstream_findings.read_text(encoding="utf-8") if upstream_findings.is_file() else ""):
        upstream_findings.parent.mkdir(parents=True, exist_ok=True)
        with upstream_findings.open("a", encoding="utf-8") as fh:
            fh.write(render_upstream(out_dir, upstream))
    return 0 if complete or allow_incomplete else 2


def render_report(entries: list[dict], upstream_findings: Path) -> str:
    own = [e for e in entries if not e["synced"]]
    lines = ["# Audit report", "", "| Skill | Percent | Grade | Judges |", "|---|---|---|---|"]
    lines += [
        f"| {e['name']} | {'-' if e['percent'] is None else e['percent']} | {e['grade']} | {', '.join(e['judges']) or '-'} |"
        for e in own
    ]
    sections = [
        ("Disagreements", [f"- {e['name']}: {e['judges']}" for e in own if e["disagreement"]]),
        ("Missing verdicts", [f"- {e['name']}: {', '.join(e['missing_judges'])}" for e in own if e["missing_judges"]]),
        ("Below target", [f"- {e['name']}: {e['grade']} {e['percent']}" for e in own
                          if e["percent"] is None or e["percent"] < TARGET]),
        ("Waived", [f"- {e['name']}" for e in own if e["waived"]]),
        ("Synced", [f"- {e['name']}" for e in entries if e["synced"]]
         + [f"Findings for synced skills: see {upstream_findings}"] * any(e["synced"] for e in entries)),
    ]
    for title, items in sections:
        lines += ["", f"## {title}", ""] + (items or ["None."])
    return "\n".join(lines) + "\n"


def render_upstream(out_dir: Path, upstream: list) -> str:
    lines = ["", f"## {out_dir}", ""]
    for name, findings, issues in upstream:
        lines += [f"### {name}", ""]
        lines += [
            f"- [{f['severity']}] {f['dimension']} {f['file']}:{f['line'] or '-'}: {f['evidence']} Fix: {f['fix']}"
            for f in findings
        ]
        lines += [f"- check {i['code']}{' (ignored)' if i['ignored'] else ''}: {i['detail']}" for i in issues]
        lines.append("")
    return "\n".join(lines)


# ---------- run-evals / pi-cmd ----------


class HarnessError(Exception):
    """Anything that stops an eval run from being trusted (exit 2)."""


def pi_cmd(kind: str, model: str = DEFAULT_JUDGE_MODEL) -> list[str]:
    tools = ["--no-tools"] if kind == "runner" else ["--tools", "read,grep,find,ls"]
    return PI_BASE + tools + ["--model", model]


def resolve_runner(cmd: str) -> list[str]:
    """Tokenise CMD and pin its executable against the invocation cwd / PATH."""
    try:
        argv = shlex.split(cmd)
    except ValueError as e:
        raise HarnessError(f"bad --runner: {e}") from e
    if not argv:
        raise HarnessError("--runner is empty")
    found = os.path.abspath(argv[0]) if "/" in argv[0] else shutil.which(argv[0])
    if not found:
        raise HarnessError(f"runner {argv[0]!r} not found on PATH")
    return [os.path.abspath(found)] + argv[1:]


def kill_group(p: subprocess.Popen) -> None:
    """SIGKILL the runner's whole session: a wrapper runner's children share it."""
    with contextlib.suppress(ProcessLookupError):
        os.killpg(p.pid, signal.SIGKILL)


def call_runner(argv: list[str], prompt: str, timeout: float) -> str:
    with tempfile.TemporaryDirectory() as sandbox:  # fresh empty cwd: no repo files in reach
        try:
            p = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 text=True, cwd=sandbox, start_new_session=True)
        except (OSError, ValueError) as e:
            raise HarnessError(f"cannot launch runner {argv[0]!r}: {e}") from e
        try:
            out, err = p.communicate(prompt, timeout=timeout)
        except subprocess.TimeoutExpired as e:
            kill_group(p)
            try:
                p.communicate(timeout=KILL_DRAIN_TIMEOUT)
            except subprocess.TimeoutExpired:  # a child that left the session still holds the pipes
                for f in (p.stdin, p.stdout, p.stderr):
                    with contextlib.suppress(OSError):
                        f.close()
                p.wait()
            raise HarnessError(f"runner timed out after {timeout}s") from e
        except BaseException:  # e.g. KeyboardInterrupt: never leave the session running
            kill_group(p)
            p.wait()
            raise
    if p.returncode != 0:
        raise HarnessError(f"runner exited {p.returncode}: {err.strip()[:300]}")
    return out


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise HarnessError(f"cannot read {path}: {e}") from e


def nonempty_str(v) -> bool:
    return isinstance(v, str) and bool(v.strip())


def validate_evals(path: Path, data, expected_name: str) -> list[dict]:
    evals = data.get("evals") if isinstance(data, dict) else None
    if not isinstance(data, dict) or data.get("skill_name") != expected_name:
        raise HarnessError(f"{path}: skill_name must equal the file stem ({expected_name!r})")
    if not isinstance(evals, list) or not evals:
        raise HarnessError(f"{path}: evals must be a non-empty list")
    seen: set[str] = set()
    for i, ev in enumerate(evals):
        where = f"{path} evals[{i}]"
        if not isinstance(ev, dict):
            raise HarnessError(f"{where}: not an object")
        eid = ev.get("id")
        if not (is_int(eid) or nonempty_str(eid)) or not EVAL_ID_RE.fullmatch(str(eid)):
            raise HarnessError(f"{where}: id {eid!r} must be an int or match {EVAL_ID_RE.pattern}")
        if str(eid) in seen:
            raise HarnessError(f"{where}: duplicate id {eid!r}")
        seen.add(str(eid))
        a, files = ev.get("assertions"), ev.get("files", [])
        if not nonempty_str(ev.get("prompt")):
            raise HarnessError(f"{where}: prompt must be a non-empty string")
        if not isinstance(a, list) or not a or not all(nonempty_str(x) for x in a):
            raise HarnessError(f"{where}: assertions must be a non-empty list of non-empty strings")
        if not isinstance(files, list) or not all(isinstance(x, str) for x in files):
            raise HarnessError(f"{where}: files must be a list of strings")
        if not isinstance(ev.get("expected_output", ""), str):
            raise HarnessError(f"{where}: expected_output must be a string")
    return evals


def load_evals(root: Path, name: str) -> list[dict]:
    path = root / "skills" / name / "evals" / "evals.json"
    return validate_evals(path, read_json(path), name)


def load_eval_file(root: Path, eval_file: Path) -> tuple[dict, list[dict]]:
    root = root.resolve()
    commands_evals = (root / "commands" / "evals").resolve()
    path = (root / eval_file).resolve() if not eval_file.is_absolute() else eval_file.resolve()
    try:
        # The resolved eval file must sit inside the root AND inside the
        # resolved commands/evals directory, and that directory itself must
        # resolve inside the root (a symlinked commands/evals pointing
        # outside the repository is rejected here, before any runner call).
        contained = (path.is_relative_to(root) and path.is_relative_to(commands_evals)
                     and commands_evals.is_relative_to(root))
    except OSError:
        contained = False
    if not contained:
        raise HarnessError("eval file must be under commands/evals/ inside the root")
    data = read_json(path)
    name = path.name.rsplit(".", 1)[0]
    return data, validate_evals(path, data, name)


def load_trigger_queries(root: Path, name: str) -> list[dict]:
    path = root / "skills" / name / "evals" / "trigger-queries.json"
    data = read_json(path)
    if not isinstance(data, list) or not data or not all(
        isinstance(q, dict) and nonempty_str(q.get("query")) and isinstance(q.get("should_trigger"), bool)
        for q in data
    ):
        raise HarnessError(f"{path}: must be a non-empty list of {{query, should_trigger: bool}}")
    return data


def file_blocks(root: Path, name: str, files: list[str], base_dir: Path | None = None) -> str:
    """Read eval fixtures after a canonical containment check."""
    root = root.resolve()
    sdir = (base_dir or (root / "skills" / name)).resolve()
    out = []
    for f in files:
        if os.path.isabs(f) or ".." in Path(f).parts:
            raise HarnessError(f"eval file {f!r} resolves outside the root")
        candidates = [sdir / f] if base_dir is not None else [sdir / f, sdir / "evals" / "files" / f]
        for candidate in candidates:
            cand = candidate.resolve()
            if not cand.is_relative_to(root) or not cand.is_relative_to(sdir):
                raise HarnessError(f"eval file {f!r} resolves outside the root")
            if cand.is_file():
                break
        else:
            raise HarnessError(f"eval file {f!r} not found under {sdir}")
        try:
            out.append(f"=== FILE {f} ===\n{cand.read_text(encoding='utf-8')}\n")
        except (OSError, ValueError) as e:
            raise HarnessError(f"eval file {f!r}: {e}") from e
    return "".join(out)


def header(mode: str, key: str) -> str:
    return f"MODE: {mode}\nKEY: {key}\n\n{SANDBOX_PREAMBLE}\n\n"


def build_output_prompt(root: Path, name: str, ev: dict, blocks: str,
                        subject_label: str | None = None, extra_documents: list[tuple[str, str]] | None = None,
                        subject_text: str | None = None) -> str:
    content = subject_text if subject_text is not None else (root / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
    if subject_label is None:
        subject = f"=== SKILL.md of {name} ===\n{content}\n"
    else:
        subject = f"=== SUBJECT {subject_label} ===\n{content}\n"
    contexts = "".join(f"=== CONTEXT {label} ===\n{text}\n" for label, text in (extra_documents or []))
    return header("output", f"{name}/{ev['id']}") + subject + contexts + f"{blocks}=== TASK ===\n{ev['prompt']}\n"


def build_grade_prompt(name: str, ev: dict, blocks: str, output: str) -> str:
    expected = f"=== EXPECTED_OUTPUT ===\n{ev['expected_output']}\n" if ev.get("expected_output") else ""
    numbered = "".join(f"{i}. {a}\n" for i, a in enumerate(ev["assertions"], 1))
    return (
        header("grade", f"{name}/{ev['id']}") + blocks + expected
        + 'Return only JSON {"results":[{"assertion":<text copied exactly>,"passed":<true|false>,'
        + '"evidence":<one sentence quoting the output>}]} with exactly one result per assertion below.\n'
        + f"ASSERTIONS:\n{numbered}OUTPUT:\n{output}\n"
    )


def catalog(root: Path) -> dict[str, str]:
    """directory name -> description of every non-synced skill, from SKILL.md frontmatter."""
    out = {}
    for d in sorted(p for p in (root / "skills").iterdir() if p.is_dir() and p.name not in SYNCED):
        md = d / "SKILL.md"
        if md.is_file():
            fm = parse_frontmatter(md.read_text(encoding="utf-8"))
            out[d.name] = " ".join(fm.get("description", "").split())
    return out


def build_trigger_prompt(name: str, index: int, query: str, cat: dict[str, str]) -> str:
    return (
        header("trigger", f"{name}/q{index}")
        + 'Pick the one skill whose description matches the request, or none. Return only JSON {"skill":"<name>|none"}.\n'
        + "CATALOG:\n" + "".join(f"- {n}: {d}\n" for n, d in cat.items()) + f"REQUEST:\n{query}\n"
    )


def parse_object(text: str, what: str):
    body = text.strip()
    # One fenced block wrapping the whole answer, located by position (first
    # line up to the first newline, final three characters) so that triple
    # backticks inside JSON string values (e.g. quoted Mermaid fences) survive.
    m = re.match(r"```[\w-]*\n", body)
    if m and body.endswith("```") and len(body) - 3 > m.end():
        body = body[m.end():-3]
    try:
        return json.loads(body)
    except ValueError as e:
        raise HarnessError(f"{what}: answer is not JSON: {text.strip()[:200]!r}") from e


def normalize_assertion(text: str) -> str:
    """Casefold, drop quote/backtick characters and collapse whitespace runs.

    The grader echoes the assertions in its own words, so quoting and
    whitespace drift must not fail validation.
    """
    return " ".join("".join(ch for ch in text.casefold() if ch not in "'\"`’‘“”").split())


def validate_grading(data, assertions: list[str]) -> list[str]:
    """Reasons the grader's parsed answer is invalid (empty = ok)."""
    results = data.get("results") if isinstance(data, dict) else None
    if not isinstance(results, list):
        return ["answer must be an object with a 'results' list"]
    errs = []
    if len(results) != len(assertions):
        errs.append(f"{len(results)} results for {len(assertions)} assertions")
    for i, r in enumerate(results):
        if not (isinstance(r, dict) and isinstance(r.get("assertion"), str) and isinstance(r.get("passed"), bool)
                and nonempty_str(r.get("evidence"))):
            errs.append(f"results[{i}]: needs assertion (str), passed (bool), evidence (non-empty str)")
    if not errs and Counter(normalize_assertion(r["assertion"]) for r in results) != \
            Counter(normalize_assertion(a) for a in assertions):
        errs.append("assertion texts do not match the declared assertions exactly once each")
    return errs


def write_inside(base: Path, path: Path, text: str) -> None:
    if not path.resolve().is_relative_to(base):  # base is unresolved on purpose: a symlinked DIR/<s> must fail
        raise HarnessError(f"refusing to write {path} outside {base}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def summarise(skill: str, mode: str, passed: int, total: int, failures: list) -> dict:
    return {"skill": skill, "mode": mode, "pass_rate": round(passed / total, 4),
            "passed": passed, "total": total, "failures": failures}


def run_output_evals(name, evals, prompts, runner, timeout, out) -> dict:
    per_eval = out / name / "output"
    passed = total = 0
    failures = []
    for ev, blocks, prompt in prompts:
        output = call_runner(runner, prompt, timeout)
        write_inside(per_eval, per_eval / ev["id"] / "output.txt", output)
        answer = call_runner(runner, build_grade_prompt(name, ev, blocks, output), timeout)
        data = parse_object(answer, f"{name}/{ev['id']} grader")
        errs = validate_grading(data, ev["assertions"])
        if errs:
            raise HarnessError(f"{name}/{ev['id']} grader: " + "; ".join(errs))
        write_inside(per_eval, per_eval / ev["id"] / "grading.json", json.dumps(data, indent=2) + "\n")
        for r in data["results"]:
            total += 1
            if r["passed"]:
                passed += 1
            else:
                failures.append({"eval": ev["id"], "assertion": r["assertion"], "evidence": r["evidence"]})
    return summarise(name, "output", passed, total, failures)


def eval_output_mode(root, name, runner, timeout, out) -> dict:
    evals = load_evals(root, name)
    prompts = []  # everything that can fail on the host is built before the first model call
    for ev in evals:
        ev["id"] = str(ev["id"])
        blocks = file_blocks(root, name, ev.get("files", []))
        prompts.append((ev, blocks, build_output_prompt(root, name, ev, blocks)))
    return run_output_evals(name, evals, prompts, runner, timeout, out)


def run_eval_file(root: Path, eval_file: Path, runner: str, timeout: float, out: Path, fail_under: float,
                  only: list[str] | None = None) -> int:
    root = root.resolve()
    name = eval_file.name.rsplit(".", 1)[0]
    out = out.resolve()
    summary_name = "summary-output.only.json" if only is not None else "summary-output.json"
    stale = out / name / summary_name
    if not stale.resolve().is_relative_to(out):
        raise HarnessError(f"refusing to remove {stale} outside --out {out}")
    path = (root / eval_file).resolve() if not eval_file.is_absolute() else eval_file.resolve()
    stale.unlink(missing_ok=True)
    data, evals = load_eval_file(root, eval_file)
    if only is not None:
        if not only:
            raise HarnessError("--only selects no eval ids")
        available = {str(ev["id"]) for ev in evals}
        unknown = [eid for eid in only if eid not in available]
        if unknown:
            raise HarnessError(f"unknown eval id(s): {', '.join(unknown)}")
        selected = set(only)
        evals = [ev for ev in evals if str(ev["id"]) in selected]
    docs = []
    for key in ("subject", "context"):
        values = [data.get(key)] if key == "subject" else data.get(key, [])
        if key == "subject" and not isinstance(values[0], str):
            raise HarnessError(f"{path}: subject must be a repo-relative path")
        if key == "context" and (not isinstance(values, list) or not all(isinstance(v, str) for v in values)):
            raise HarnessError(f"{path}: context must be a list of repo-relative paths")
        for value in values:
            if os.path.isabs(value) or ".." in Path(value).parts:
                raise HarnessError(f"{path}: {key} path {value!r} resolves outside the root")
            document = (root / value).resolve()
            if not document.is_relative_to(root):
                raise HarnessError(f"{path}: {key} path {value!r} resolves outside the root")
            if not document.is_file():
                raise HarnessError(f"{path}: {key} document {value!r} does not exist")
            docs.append((key, value, document.read_text(encoding="utf-8")))
    subject = next((text for kind, _, text in docs if kind == "subject"), "")
    contexts = [(label, text) for kind, label, text in docs if kind == "context"]
    prompts = []
    fixtures = path.parent / "files"
    for ev in evals:
        ev["id"] = str(ev["id"])
        blocks = file_blocks(root, name, ev.get("files", []), fixtures)
        prompt = build_output_prompt(root, name, ev, blocks, data["subject"], contexts, subject)
        prompts.append((ev, blocks, prompt))
    argv = resolve_runner(runner)
    summary = run_output_evals(name, evals, prompts, argv, timeout, out)
    write_inside(out / name, stale, json.dumps(summary, indent=2) + "\n")
    print(json.dumps([summary], indent=2))
    return 1 if summary["passed"] / summary["total"] < fail_under else 0


def eval_trigger_mode(root, name, runner, timeout, runs) -> dict:
    queries, cat = load_trigger_queries(root, name), catalog(root)
    passed, failures = 0, []
    for i, q in enumerate(queries):
        prompt = build_trigger_prompt(name, i, q["query"], cat)
        hits = 0
        for _ in range(runs):
            data = parse_object(call_runner(runner, prompt, timeout), f"{name}/q{i} trigger")
            pick = data.get("skill") if isinstance(data, dict) and set(data) == {"skill"} else None
            if not isinstance(pick, str) or pick not in {*cat, "none"}:
                raise HarnessError(f"{name}/q{i}: invalid trigger answer {data!r}")
            hits += pick == name
        rate = hits / runs
        if (rate > 0.5) if q["should_trigger"] else (rate < 0.5):
            passed += 1
        else:
            failures.append({"query": q["query"], "should_trigger": q["should_trigger"], "rate": round(rate, 2)})
    return summarise(name, "triggers", passed, len(queries), failures)


def run_evals(
    root: Path, skills: list[str], runner: str, timeout: float, triggers: bool, runs: int,
    out: Path, fail_under: float,
) -> int:
    if not skills or runs < 1 or timeout <= 0:
        raise HarnessError("need --skills, --runs >= 1 and --timeout > 0")
    for name in skills:
        if not SKILL_NAME_RE.fullmatch(name) or not (root / "skills" / name).is_dir():
            raise HarnessError(f"invalid skill {name!r}: not a kebab-case directory under skills/")
    argv, out = resolve_runner(runner), out.resolve()
    summaries = []
    for name in skills:
        if name in SYNCED:
            summaries.append({"skill": name, "skipped": "synced"})
            continue
        stale = out / name / f"summary-{'triggers' if triggers else 'output'}.json"  # a failed run must not leave the last one
        if not stale.resolve().is_relative_to(out):
            raise HarnessError(f"refusing to remove {stale} outside {out}")
        stale.unlink(missing_ok=True)
        s = eval_trigger_mode(root, name, argv, timeout, runs) if triggers else eval_output_mode(root, name, argv, timeout, out)
        write_inside(out / name, out / name / f"summary-{s['mode']}.json", json.dumps(s, indent=2) + "\n")
        summaries.append(s)
    print(json.dumps(summaries, indent=2))
    return 1 if any(s["passed"] / s["total"] < fail_under for s in summaries if "total" in s) else 0


# ---------- upstream sources ----------


class SourceUnavailable(Exception):
    """An upstream source could not be checked reliably."""


def validate_entry(root: Path, entry) -> str | None:
    if not isinstance(entry, dict):
        return "entry must be an object"
    if set(entry) != {"skill", "kind", "source", "ref"}:
        return "entry must have exactly skill, kind, source, ref"
    kind, skill, source, ref = (entry[k] for k in ("kind", "skill", "source", "ref"))
    if not isinstance(kind, str) or kind not in {"github", "github-path", "wikipedia", "repo", "unversioned"}:
        return f"unsupported kind {kind!r}"
    if kind == "repo":
        if skill is not None:
            return "repo skill must be null"
    else:
        if not isinstance(skill, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", skill):
            return "skill must be a kebab-case name"
        skills = (root / "skills").resolve()
        sdir = root / "skills" / skill
        if not sdir.is_dir() or not sdir.resolve().is_relative_to(skills):
            return f"skill directory {skill!r} does not exist under skills/"
    component = r"[A-Za-z0-9._-]+"
    repo_pattern = rf"{component}/{component}"
    if kind in ("github", "repo"):
        source_ok = isinstance(source, str) and re.fullmatch(repo_pattern, source) and not any(
            part in (".", "..") for part in source.split("/")
        )
    elif kind == "github-path":
        match = re.fullmatch(rf"({component})/({component}):(.+)", source) if isinstance(source, str) else None
        source_ok = bool(match and match.group(1) not in (".", "..") and match.group(2) not in (".", "..")
                         and not match.group(3).startswith("/")
                         and not any(ord(char) < 32 or ord(char) == 127 or char in "\\\\?#%&=" for char in match.group(3))
                         and all(part not in ("", ".", "..") for part in match.group(3).split("/")))
    elif kind == "wikipedia":
        source_ok = isinstance(source, str) and bool(source.strip()) and "\n" not in source and "\r" not in source
    else:
        source_ok = isinstance(source, str) and bool(source.strip())
    if not source_ok:
        return f"invalid source for {kind}"
    if kind in ("github", "github-path", "repo"):
        if not isinstance(ref, str) or not ref.strip():
            return f"{kind} ref must be a non-empty string"
    elif ref is not None:
        return f"{kind} ref must be null"
    return None


def source_query(entry: dict) -> str | None:
    kind, source, ref = entry["kind"], entry["source"], entry["ref"]
    if kind in ("github", "repo"):
        owner, repo = source.split("/", 1)
        return f"repos/{owner}/{repo}/commits?sha={urllib.parse.quote(ref, safe='')}&per_page=1"
    if kind == "github-path":
        repo, path = source.split(":", 1)
        owner, name = repo.split("/", 1)
        return f"repos/{owner}/{name}/commits?path={urllib.parse.quote(path, safe='')}&sha={urllib.parse.quote(ref, safe='')}&per_page=1"
    if kind == "wikipedia":
        return "https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=" + urllib.parse.quote(entry["source"], safe="") + "&rvprop=timestamp&format=json"
    return None


def upstream_repo_url(entry: dict) -> str:
    """Build the repo fetch URL; overridable in tests for local fixture remotes."""
    return f"https://github.com/{entry['source']}.git"


def fetch_source_updated(entry: dict) -> str | None:
    query = source_query(entry)
    if query is None:
        return None
    try:
        if entry["kind"] == "wikipedia":
            request = urllib.request.Request(query, headers={"User-Agent": "agent-toolkit-upstream-audit/1.0"})
            with urllib.request.urlopen(request, timeout=10) as response:
                data = json.loads(response.read().decode("utf-8"))
            pages = data["query"]["pages"]
            if not isinstance(pages, dict) or not pages:
                raise SourceUnavailable("malformed Wikipedia pages")
            page = next(iter(pages.values()))
            revisions = page.get("revisions") if isinstance(page, dict) else None
            if not isinstance(revisions, list) or not revisions or not isinstance(revisions[0], dict):
                raise SourceUnavailable("malformed Wikipedia revisions")
            timestamp = revisions[0]["timestamp"]
        else:
            proc = subprocess.run(["gh", "api", query], capture_output=True, text=True, timeout=10)
            if proc.returncode:
                raise SourceUnavailable(proc.stderr.strip() or f"gh api exited {proc.returncode}")
            commits = json.loads(proc.stdout)
            timestamp = commits[0]["commit"]["committer"]["date"]
        if not isinstance(timestamp, str) or not timestamp:
            raise SourceUnavailable("response has no timestamp")
        return timestamp
    except SourceUnavailable:
        raise
    except (OSError, subprocess.SubprocessError, ValueError, KeyError, TypeError, IndexError, StopIteration, urllib.error.URLError) as e:
        raise SourceUnavailable(str(e) or "malformed upstream response") from e


def ours_updated(root: Path, entry: dict) -> str | None:
    if entry["kind"] == "repo":
        try:
            subprocess.run(["git", "fetch", "--quiet", "--", upstream_repo_url(entry), entry["ref"]],
                           cwd=root, check=True, capture_output=True, text=True)
        except (subprocess.CalledProcessError, OSError) as exc:
            raise SourceUnavailable(str(exc)) from exc
        try:
            base_proc = subprocess.run(["git", "merge-base", "HEAD", "FETCH_HEAD"], cwd=root,
                                       capture_output=True, text=True)
        except OSError as exc:
            raise SourceUnavailable(str(exc)) from exc
        if base_proc.returncode == 0:
            target = base_proc.stdout.strip()
        elif base_proc.returncode == 1:
            try:
                local = subprocess.run(["git", "rev-list", "--max-parents=0", "HEAD"], cwd=root,
                                       capture_output=True, text=True)
            except OSError as exc:
                raise SourceUnavailable(str(exc)) from exc
            if local.returncode:
                raise SourceUnavailable(local.stderr.strip() or "cannot locate earliest local commit")
            roots = local.stdout.split()
            if roots:
                dated = subprocess.run(["git", "show", "-s", "--format=%ct", *roots], cwd=root,
                                       capture_output=True, text=True)
                if dated.returncode:
                    raise SourceUnavailable(dated.stderr.strip() or "cannot date local root commits")
                dates = [int(date) for date in dated.stdout.splitlines()]
                target = roots[min(range(len(roots)), key=lambda index: dates[index])]
            else:
                target = ""
        else:
            raise SourceUnavailable(base_proc.stderr.strip() or f"git merge-base exited {base_proc.returncode}")
        if not target:
            return None
        args = ["git", "show", "-s", "--format=%cI", target]
    else:
        name = entry["skill"]
        paths = [f"skills/{name}/SKILL.md", f"skills/{name}/references/"]
        args = ["git", "log", "-1", "--format=%cI", "--", *paths]
    try:
        proc = subprocess.run(args, cwd=root, capture_output=True, text=True)
    except OSError as exc:
        raise SourceUnavailable(str(exc)) from exc
    if proc.returncode:
        raise SourceUnavailable(proc.stderr.strip() or "git query failed")
    return proc.stdout.strip() or None


def upstreams(root: Path, registry: Path) -> int:
    try:
        entries = json.loads(registry.read_text(encoding="utf-8"))
        if not isinstance(entries, list):
            raise ValueError("registry must be a JSON list")
    except (OSError, ValueError, RecursionError) as exc:
        print(f"cannot read registry {registry}: {exc}", file=sys.stderr)
        return 2
    rows, failed = [], False
    for entry in entries:
        skill = entry.get("skill") if isinstance(entry, dict) else None
        source = entry.get("source") if isinstance(entry, dict) else None
        kind = entry.get("kind") if isinstance(entry, dict) else None
        reason = validate_entry(root, entry)
        source_updated = ours = None
        error = None
        stale = None
        if reason:
            error = f"invalid entry: {reason}"
        else:
            try:
                if entry["kind"] != "unversioned":
                    source_updated = fetch_source_updated(entry)
                ours = ours_updated(root, entry)
                if ours is None:
                    error = "no local commit for source material"
                elif entry["kind"] == "unversioned":
                    stale = False
                else:
                    def instant(value):
                        if not isinstance(value, str):
                            raise ValueError("timestamp is not a string")
                        normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
                        parsed = datetime.datetime.fromisoformat(normalized)
                        if parsed.tzinfo is None:
                            raise ValueError("timestamp must include timezone")
                        return parsed.astimezone(datetime.timezone.utc)
                    try:
                        stale = instant(source_updated) > instant(ours)
                    except (TypeError, ValueError, OverflowError) as exc:
                        raise SourceUnavailable(f"invalid upstream timestamp: {exc}") from exc
            except SourceUnavailable as exc:
                error = str(exc)
        if error:
            failed = True
            stale = None
        rows.append({"skill": skill, "source": source, "kind": kind, "source_updated": source_updated,
                     "ours_updated": ours, "stale": stale, "error": error})
    print(json.dumps(rows, indent=2))
    return 1 if failed else 0


# ---------- CLI ----------


def csv(value: str) -> list[str]:
    return [v for v in value.split(",") if v]


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--root", type=Path, default=None)
    sub = p.add_subparsers(dest="cmd", required=True)
    up = sub.add_parser("upstreams")
    up.add_argument("--registry", type=Path, required=True)
    c = sub.add_parser("check")
    c.add_argument("--strict", action="store_true")
    c.add_argument("--skills", type=csv, default=None)
    c.add_argument("--ignore", type=csv, default=[])
    c.add_argument("--allowlist", type=Path, default=None)
    r = sub.add_parser("rubric-check")
    r.add_argument("--rubric", type=Path, default=None)
    s = sub.add_parser("slug")
    s.add_argument("model")
    v = sub.add_parser("split-verdicts")
    v.add_argument("--judge", required=True)
    v.add_argument("--out", type=Path, required=True)
    vv = sub.add_parser("validate-verdict")
    vv.add_argument("--rubric", type=Path, default=None)
    vv.add_argument("files", type=Path, nargs="+", metavar="FILE")
    m = sub.add_parser("merge")
    m.add_argument("--in", dest="in_dir", type=Path, required=True)
    m.add_argument("--out", type=Path, required=True)
    m.add_argument("--judges", type=csv, required=True)
    m.add_argument("--skills", type=csv, default=None)
    m.add_argument("--check", type=Path, default=None)
    m.add_argument("--waivers", type=Path, default=None)
    m.add_argument("--min-judges", type=int, default=1)
    m.add_argument("--allow-incomplete", action="store_true")
    m.add_argument("--rubric", type=Path, default=None)
    m.add_argument("--upstream-findings", type=Path, default=None)
    e = sub.add_parser("run-evals")
    group = e.add_mutually_exclusive_group(required=True)
    group.add_argument("--skills", type=csv)
    group.add_argument("--eval-file", type=Path)
    e.add_argument("--runner", required=True)
    e.add_argument("--timeout", type=float, default=600)
    e.add_argument("--triggers", action="store_true")
    e.add_argument("--runs", type=int, default=3)
    e.add_argument("--out", type=Path, default=None)
    e.add_argument("--fail-under", type=float, default=0.8)
    e.add_argument("--only", type=csv, default=None,
                   help="run only these comma-separated eval ids (command eval files only)")
    pc = sub.add_parser("pi-cmd")
    pc.add_argument("kind", choices=["runner", "judge"])
    pc.add_argument("--model", default=DEFAULT_JUDGE_MODEL)
    pc.add_argument("--print0", action="store_true")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = (args.root or default_root()).resolve()
    if args.cmd == "upstreams":
        return upstreams(root, args.registry)
    if args.cmd == "check":
        if args.allowlist and not args.allowlist.is_file():
            print(f"allowlist not found: {args.allowlist}", file=sys.stderr)
            return 1
        try:
            res = check_skills(root, args.skills, args.strict, set(args.ignore), args.allowlist)
        except ValueError as e:
            print(e, file=sys.stderr)
            return 1
        print(json.dumps(res, indent=2))
        bad = any(not s["ok"] for s in res["skills"] if not s["synced"])
        return 1 if args.strict and bad else 0
    if args.cmd == "rubric-check":
        try:
            reasons = rubric_check(root, resolve_rubric(root, args.rubric))
        except ValueError as e:
            print(e, file=sys.stderr)
            return 1
        for reason in reasons:
            print(reason, file=sys.stderr)
        return 1 if reasons else 0
    if args.cmd == "slug":
        s = slug(args.model)
        if not s:
            print(f"model {args.model!r} has an empty slug", file=sys.stderr)
            return 1
        print(s)
        return 0
    if args.cmd == "pi-cmd":
        tokens = pi_cmd(args.kind, args.model)
        sys.stdout.write("".join(t + "\0" for t in tokens) if args.print0 else shlex.join(tokens) + "\n")
        return 0
    if args.cmd == "run-evals":
        try:
            output = args.out or root / "docs" / "audit" / "evals"
            if args.eval_file is not None:
                if args.triggers:
                    raise HarnessError("trigger queries are not supported for command eval files")
                return run_eval_file(root, args.eval_file, args.runner, args.timeout, output, args.fail_under,
                                     args.only)
            if args.only is not None:
                raise HarnessError("--only is supported only with --eval-file")
            return run_evals(root, args.skills, args.runner, args.timeout, args.triggers, args.runs,
                             output, args.fail_under)
        except (HarnessError, OSError, ValueError, RecursionError) as e:  # UnicodeDecodeError is a ValueError; a crash must never read as exit 1
            print(f"harness error: {e}", file=sys.stderr)
            return 2
    if args.cmd in ("validate-verdict", "merge"):
        try:
            rubric = resolve_rubric(root, args.rubric)
            if args.cmd == "validate-verdict":
                r, bad = load_rubric(rubric), False
                for f in args.files:
                    for reason in read_verdict(f, r)[1]:
                        print(f"{f}: {reason}", file=sys.stderr)
                        bad = True
                return 1 if bad else 0
            if args.cmd == "merge" and args.min_judges < 1:
                raise ValueError("--min-judges must be at least 1")
            if any(not slug(j) for j in args.judges):
                raise ValueError("a judge has an empty slug")
            return merge_verdicts(
                root, args.in_dir, args.out, args.judges, args.skills, args.check, args.waivers,
                args.min_judges, args.allow_incomplete, rubric,
                args.upstream_findings or root / "docs" / "audit" / "upstream-findings.md",
            )
        except (OSError, ValueError, KeyError, TypeError) as e:
            print(e, file=sys.stderr)
            return 1
    if not slug(args.judge):
        print(f"judge {args.judge!r} has an empty slug", file=sys.stderr)
        return 1
    split_verdicts(args.judge, args.out, sys.stdin)
    return 0


if __name__ == "__main__":
    sys.exit(main())
