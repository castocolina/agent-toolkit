#!/usr/bin/env python3
"""Audit helpers for skills: check, rubric-check, slug, split-verdicts, validate-verdict, merge, run-evals, pi-cmd, judge-prompt.

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
    python3 scripts/audit/audit.py judge-prompt [--kind skill|command|agent] --artifact PATH [--artifact PATH ...]
        --judge SLUG [--root DIR] [--previous SRC ...] [--recovery-gate QUEUE] [--digest-dir DIR]
    python3 scripts/audit/audit.py interval-due --state JSON --days 15|30 [--now ISO] [--event NAME]
    python3 scripts/audit/audit.py validate-knobs   (reads AUDIT_* knobs from the environment)
    python3 scripts/audit/audit.py track --artifact NAME [--artifact-kind K] [--source SOURCE] --status S
        [--sha SHA] [--model MODEL] [--new-path PATH] [--today YYYY-MM-DD] [--registry FILE]
"""

import argparse
import contextlib
import copy
import datetime
import hashlib
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
import unicodedata
from collections import Counter
from pathlib import Path

SYNCED = {"gepetto", "datadog-cli"}
C5_FIELDS = {"user-invocable", "disable-model-invocation", "argument-hint"}
DIMENSIONS = [f"D{i}" for i in range(1, 9)]
SKILL_NAME_RE = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")
KIND_DIR = {"skill": "skills", "command": "commands", "agent": "agents"}

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


def source_sha(root: Path, pin: Path | None = None) -> str:
    """The pinned spec sha from SOURCE.json; ValueError when unreadable.

    `pin` names the trusted SOURCE.json; without it the data root's own pin is read.
    """
    path = pin or judge_refs(root) / "agentskills" / "SOURCE.json"
    try:
        return json.loads(path.read_text())["sha"]
    except (OSError, ValueError, KeyError, TypeError, RecursionError) as e:
        raise ValueError(f"cannot read sha from {path}: {e}") from e


def run_skills_ref(root: Path, skill_dir: Path, pin: Path | None = None) -> tuple[int, str]:
    """Run the pinned skills-ref validator; return (exit code, combined output).

    The executable dependency is selected by `pin` when given (the trusted copy),
    never by the data root's SOURCE.json, which a pull request can change.
    """
    sha = source_sha(root, pin)
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


def bad_flow_collection(v: str) -> bool:
    """True when a '['/'{' value has no matching close at depth 0 or text (not a ' #' comment) after it.

    v may span lines joined by newlines; a '#' at a line start or after a blank is a comment to the line end."""
    depth, quote, i = 0, "", 0
    while i < len(v):
        c = v[i]
        if quote:
            quote = "" if c == quote else quote
        elif c == "#" and (i == 0 or v[i - 1] in " \t\n"):
            nl = v.find("\n", i)
            i = len(v) if nl < 0 else nl
            continue
        elif c in "\"'":
            quote = c
        elif c in "[{":
            depth += 1
        elif c in "]}":
            depth -= 1
            if depth == 0:
                first, _, others = v[i + 1:].partition("\n")
                tail_ok = not first.strip() or re.match(r"[ \t]+#", first)
                return not (tail_ok and all(not ln.strip() or ln.lstrip().startswith("#") for ln in others.split("\n")))
        i += 1
    return True


def invalid_plain_scalars(text: str) -> list[str]:
    """Top-level keys whose unquoted one-line value a YAML parser rejects (no PyYAML here, so a line heuristic)."""
    lines = text.splitlines()
    bad = []
    if lines and lines[0].strip() == "---":
        fm = []
        for ln in lines[1:]:
            if ln.strip() == "---":
                break
            fm.append(ln)
        for i, ln in enumerate(fm):
            m = re.match(r"^([A-Za-z0-9_-]+):[ \t]+(\S.*)$", ln)
            if not m:
                continue
            val = m.group(2)
            if val[0] in "[{":
                if bad_flow_collection(val):
                    # a multiline flow collection: join the lines up to the next top-level key before judging it
                    cont = []
                    for nxt in fm[i + 1:]:
                        if re.match(r"^[A-Za-z0-9_-]+:", nxt):
                            break
                        cont.append(nxt.strip())
                    if not cont or bad_flow_collection("\n".join([val] + cont)):
                        bad.append(m.group(1))
            elif val[0] not in "\"'|>":
                plain = re.split(r"\s#", val, maxsplit=1)[0]  # a ' #' comment may hold ': '; quoted and block values are skipped above
                if ": " in plain or plain[0] in "@`%*&!":
                    bad.append(m.group(1))
    return bad


def yaml_issues(text: str) -> list[tuple[str, str]]:
    return [("frontmatter_yaml", f"{k}: unquoted value is not a valid YAML plain scalar (quote it or use >-)")
            for k in invalid_plain_scalars(text)]


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


def skill_issues(root: Path, name: str, allow: set[str], pin: Path | None = None) -> list[tuple[str, str]]:
    sdir = root / "skills" / name
    synced = name in SYNCED
    found: list[tuple[str, str]] = []

    # The spec pin lives in skill-judge; absent before that skill ships. A trusted pin
    # always runs the validator, so a data root without skill-judge cannot skip it.
    if pin is not None or judge_refs(root).is_dir():
        code, text = run_skills_ref(root, sdir, pin)
        details = parse_skills_ref(code, text)
        if details:
            found.append(("skills_ref", "; ".join(details)))

    md = sdir / "SKILL.md"
    content = md.read_text(encoding="utf-8") if md.is_file() else ""
    n_lines = len(content.splitlines())
    if n_lines >= 500:
        found.append(("lines_over_500", f"SKILL.md has {n_lines} lines"))
    fm = parse_frontmatter(content)
    found.extend(yaml_issues(content))
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
    found.extend(credit_issues(root, name, content))
    return found


def credit_issues(root: Path, name: str, skill_text: str) -> list[tuple[str, str]]:
    """Each registry `credit` for this skill must appear in SKILL.md, README.md or references/*.md; no registry, no check."""
    reg = root / "docs" / "audit" / "upstream-sources.json"
    try:
        rows = json.loads(reg.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    sdir = root / "skills" / name
    extra = [sdir / "README.md", *sorted((sdir / "references").glob("*.md"))]
    text = skill_text + "".join(f.read_text(encoding="utf-8") for f in extra if f.is_file())
    return [("missing_credit", f"credit {r['credit']!r} not in SKILL.md, README.md or references/*.md")
            for r in rows if isinstance(r, dict) and r.get("skill") == name
            and isinstance(r.get("credit"), str) and r["credit"] not in text]


def check_skills(
    root: Path, skills: list[str] | None = None, strict: bool = False,
    ignore: set[str] | None = None, allowlist: Path | None = None, pin: Path | None = None,
    kind: str = "skill",
) -> dict:
    if kind not in ARTIFACT_KINDS:
        raise ValueError(f"unknown artifact kind {kind!r}")
    ignore = ignore or set()
    if kind != "skill":
        return check_flat(root, kind, skills, ignore)
    allow = load_allowlist(allowlist or root / "scripts" / "audit" / "non_latin_allowlist.txt")
    if pin is not None:
        source_sha(root, pin)  # a missing or unreadable trusted pin fails before any skill is checked
    elif not judge_refs(root).is_dir():
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
            for c, d in skill_issues(root, name, allow, pin)
        ]
        result.append({
            "name": name,
            "ok": all(i["ignored"] for i in issues),
            "synced": name in SYNCED,
            "issues": issues,
        })
    return {"skills": result}


def artifact_names(root: Path, kind: str) -> list[str]:
    """Sorted names of one kind: skills/<dir>/, commands/<name>.md, agents/<name>.md (commands/evals/ is a dir)."""
    home = root / KIND_DIR[kind]
    if not home.is_dir():
        return []
    if kind == "skill":
        return sorted(p.name for p in home.iterdir() if p.is_dir())
    good = []
    for p, why in _flat_files(root, kind):
        if why:
            print(f"skipped {KIND_DIR[kind]}/{p.name}: {why}", file=sys.stderr)
        else:
            good.append(p.stem)
    return sorted(good)


FLAT_SKIPS = {"invalid_name": "name is not kebab-case", "uncontained_path": "not a file inside its kind directory"}


def _flat_files(root: Path, kind: str) -> list[tuple[Path, str | None]]:
    """*.md files of a flat kind (README excluded) with the reason each is skipped, or None when usable."""
    home = root / KIND_DIR[kind]
    if not home.is_dir():
        return []
    out = []
    for p in sorted(home.glob("*.md")):
        if p.stem == "README":
            continue
        why = None if SKILL_NAME_RE.fullmatch(p.stem) else FLAT_SKIPS["invalid_name"]
        if why is None and not artifact_exists(root, p.stem, kind):
            why = FLAT_SKIPS["uncontained_path"]
        out.append((p, why))
    return out


def list_artifacts(root: Path) -> list[dict]:
    found = [
        {"kind": k, "name": n, "path": f"skills/{n}" if k == "skill" else f"{KIND_DIR[k]}/{n}.md"}
        for k in ("agent", "command", "skill") for n in artifact_names(root, k)
    ]
    kinds: dict[str, list[str]] = {}
    for a in found:
        kinds.setdefault(a["name"], []).append(a["kind"])
    dupes = [f"{n} ({', '.join(k)})" for n, k in sorted(kinds.items()) if len(k) > 1]
    if dupes:
        raise ValueError("name used by more than one kind: " + "; ".join(dupes))
    return found


def flat_issues(root: Path, kind: str, name: str) -> list[tuple[str, str]]:
    """Command: non-empty description. Agent: also name == file stem (docs/audit/artifact-specs.md)."""
    # Stricter than the Claude Code docs (command description required, agent name == stem): plan 7 Task 1, verdict files are keyed by stem.
    text = (root / KIND_DIR[kind] / f"{name}.md").read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    found = []

    def plain(key: str) -> str:
        """In an unquoted single-line YAML value ' #' starts a comment; quoted and block values keep '#'."""
        val = fm.get(key, "")
        raw = re.search(rf"^{key}:[ \t]*(\S?)", text, re.M)
        if raw and raw.group(1) and raw.group(1) in "\"'|>":
            return val.strip()
        return re.sub(r"(^|\s)#.*$", "", val).strip()

    if kind == "agent" and plain("name") != name:
        found.append(("name_mismatch", f"frontmatter name {fm.get('name')!r} != file stem {name!r}"))
    if not plain("description"):
        found.append(("missing_description", "description absent or empty"))
    return found + yaml_issues(text)


def check_flat(root: Path, kind: str, names: list[str] | None, ignore: set[str]) -> dict:
    codes = {v: k for k, v in FLAT_SKIPS.items()}
    bad = [] if names else [(p.stem, codes[why]) for p, why in _flat_files(root, kind) if why]
    names = names or artifact_names(root, kind)
    for name in names:
        if not SKILL_NAME_RE.fullmatch(name) or not artifact_exists(root, name, kind):
            raise ValueError(f"invalid {kind} {name!r}: not a kebab-case file under {KIND_DIR[kind]}/")
    result = [
        {"name": n, "ok": c in ignore, "synced": False,
         "issues": [{"code": c, "detail": FLAT_SKIPS[c], "ignored": c in ignore}]}
        for n, c in bad
    ]
    for name in names:
        issues = [{"code": c, "detail": d, "ignored": c in ignore} for c, d in flat_issues(root, kind, name)]
        result.append({"name": name, "ok": all(i["ignored"] for i in issues), "synced": False, "issues": issues})
    return {"skills": sorted(result, key=lambda r: r["name"])}


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


PROFILE_BLOCK_RE = re.compile(r"\Aprofile_version: (\d+)\nsource_digest: ([0-9a-f]{64})\n\n")


def check_profiles(root: Path) -> list[str]:
    """Reasons the judge profiles do not match the pinned Claude Code sources."""
    refs = judge_refs(root)
    profiles = sorted((refs / "profiles").glob("*.md"))
    if not profiles:
        return []
    pin = refs / "claude-code" / "SOURCE.json"
    try:
        digests = json.loads(pin.read_text())["digests"]
        if not isinstance(digests, dict):
            raise TypeError("digests is not an object")
    except (OSError, ValueError, KeyError, TypeError, RecursionError) as e:
        return [f"profiles exist but cannot read digests from {pin.relative_to(root)}: {e}"]
    reasons = []
    for p in profiles:
        m = PROFILE_BLOCK_RE.match(p.read_text(encoding="utf-8"))
        if not m:
            reasons.append(f"{p.name}: front block must be 'profile_version: <int>', 'source_digest: <64 hex>' and a blank line")
        elif m.group(2) != digests.get(p.stem):
            reasons.append(f"{p.name}: source_digest {m.group(2)} != claude-code/SOURCE.json digest {digests.get(p.stem)}")
    specs = root / "docs" / "audit" / "artifact-specs.md"
    try:
        head = specs.read_text(encoding="utf-8").splitlines()[2:4]
    except OSError as e:
        return reasons + [f"profiles exist but docs/audit/artifact-specs.md is unreadable: {e}"]
    for kind, line in zip(("command", "agent"), head + [""] * (2 - len(head))):
        m = re.fullmatch(kind + r"_digest: ([0-9a-f]{64})", line)
        if not m:
            reasons.append(f"artifact-specs.md line {3 + (kind == 'agent')}: expected '{kind}_digest: <64 hex>'")
        elif m.group(1) != digests.get(kind):
            reasons.append(f"artifact-specs.md {kind}_digest {m.group(1)} != claude-code/SOURCE.json digest {digests.get(kind)}")
    return reasons


def check_source_anchors(rubric_path: Path, ref_dir: Path) -> list[str]:
    """Validate reference files and heading anchors cited by rubric source cells."""
    reasons = []
    skill_root = ref_dir.parent
    try:
        lines = rubric_path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return reasons
    for line in lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        for source in (part.strip() for part in cells[3].split(";")):
            if not source.startswith("references/agentskills/"):
                continue
            path_part, separator, anchor = source.partition("#")
            path = skill_root / path_part
            if not path.is_file():
                valid = False
            elif not separator:
                # File-only citation (e.g. the validator source a rubric refresh
                # adds): nothing to anchor, existence is enough.
                valid = True
            else:
                valid = True
                try:
                    text = path.read_text(encoding="utf-8")
                except (OSError, UnicodeDecodeError):
                    valid = False
                else:
                    headings = []
                    fenced = False
                    fence_char = None
                    fence_length = 0
                    for heading_line in text.splitlines():
                        fence = re.match(r"^ {0,3}(`{3,}|~{3,})(?:[^`~].*)?$", heading_line)
                        if fence:
                            marker = fence.group(1)[0]
                            length = len(fence.group(1))
                            if not fenced:
                                fenced, fence_char, fence_length = True, marker, length
                            elif marker == fence_char and length >= fence_length and not heading_line[fence.end(1):].strip():
                                fenced, fence_char, fence_length = False, None, 0
                            continue
                        if fenced:
                            continue
                        match = re.match(r"^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$", heading_line)
                        if match:
                            heading = match.group(1)
                            headings.append(re.sub(r"[^a-z0-9 -]", "", heading.lower()).replace(" ", "-"))
                    valid = anchor in headings
            if not valid:
                reasons.append(f"broken source anchor: {source}")
    return reasons


REMOVALS_HEADING = "## Removals and sources (every judgment)"


def rubric_check(root: Path, rubric: Path) -> list[str]:
    """Return reasons the rubric is invalid (empty = ok)."""
    try:
        r = load_rubric(rubric)
    except (OSError, ValueError) as e:
        return [str(e)]
    reasons = [f"{d}: missing or max <= 0" for d in DIMENSIONS if r["max"].get(d, 0) <= 0]
    if REMOVALS_HEADING not in rubric.read_text().splitlines():
        reasons.append(f"missing section: {REMOVALS_HEADING}")
    try:
        sha = source_sha(root)
    except ValueError as e:
        return reasons + [str(e)]
    if r["spec_sha"] != sha:
        reasons.append(f"spec_sha {r['spec_sha']} != SOURCE.json sha {sha}")
    reasons.extend(check_source_anchors(rubric, root / "skills" / "skill-judge" / "references"))
    reasons.extend(check_profiles(root))
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


JUDGE_KINDS = ("skill", "command", "agent")
SKILL_JUDGE_LINE = "Judge these skills: {SKILLS}"
SKILL_READ = (
    "Each skill in the list is a directory under `{ROOT}/skills/`. "
    "Read its `SKILL.md` and any other file in that directory the rubric needs and, "
    "when it has `scripts/`, its script tests under `{ROOT}/tests/skills/<name>/`."
)
SKILL_PER = "per listed skill"
SKILL_SET = "Set `skill` to the directory name."
ARTIFACT_READ = (
    "The artifact is the file `{ROOT}/<path>`. Read it and, for a command, its eval file "
    "`{ROOT}/commands/evals/<name>.json` when that exists; there is no `scripts/` directory "
    "or script test to read."
)


def artifact_label(kind: str, path: Path) -> str:
    """Skill directory name, or the command/agent file stem."""
    return path.parent.name if kind == "skill" else path.stem


# ---------- previous-version digest ----------

FENCE_RE = re.compile(r"^\s*(```|~~~)")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s")
ITEM_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
DIGEST_SHOWN, DIGEST_UNIT_CUT, DIGEST_LINE_CUT = 40, 300, 120
ARTIFACT_DIRS = {"command": "commands", "agent": "agents"}


def norm_tokens(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower())


def shingles(text: str, n: int = 5) -> set[tuple[str, ...]]:
    t = norm_tokens(text)
    return {tuple(t[i:i + n]) for i in range(len(t) - n + 1)}


def digest_units(text: str) -> list[str]:
    """Paragraphs, list items, table rows and fenced blocks of one markdown file; headings and units under 3 words are skipped."""
    units: list[str] = []
    cur: list[str] = []
    fence = None

    def flush() -> None:
        if cur:
            units.append("\n".join(cur))
            cur.clear()

    for line in text.splitlines():
        if fence:
            cur.append(line)
            if line.strip().startswith(fence):
                fence = None
                flush()
        elif m := FENCE_RE.match(line):
            flush()
            fence = m.group(1)
            cur.append(line)
        elif HEADING_RE.match(line) or not line.strip():
            flush()
        elif line.lstrip().startswith("|"):
            flush()
            units.append(line)
        else:
            if ITEM_RE.match(line):
                flush()
            cur.append(line)
    flush()
    return [u for u in units if len(norm_tokens(u)) >= 3]


def unit_id(text: str) -> str:
    return "para:" + hashlib.sha256(" ".join(norm_tokens(text)).encode()).hexdigest()[:8]


def snapshot_skips(name: str) -> list[str]:
    """Skill paths outside the digest: eval files, and the vendored spec mirror of skill-judge."""
    return [f"skills/{name}/evals/"] + (["skills/skill-judge/references/agentskills/"] if name == "skill-judge" else [])


def git_bytes(root: Path, *args: str) -> bytes | None:
    """stdout of `git -C root ARGS`, None on a non-zero exit (or no git)."""
    try:
        p = subprocess.run(["git", "-C", str(root), *args], capture_output=True)
    except OSError:
        return None
    return p.stdout if p.returncode == 0 else None


def artifact_snapshot(root: Path, kind: str, name: str, src: str | None) -> dict[str, bytes] | None:
    """Repo-relative path to bytes for the artifact's files in the working tree (src None), at a git ref, or in a directory."""
    skill = kind == "skill"
    single = f"{ARTIFACT_DIRS[kind]}/{name}.md" if not skill else ""
    found: dict[str, bytes] = {}
    if src is not None and Path(src).is_dir():
        base = Path(src)
        for f in sorted(base.rglob("*")) if skill else [base / f"{name}.md"]:
            if f.is_file():
                found[f"skills/{name}/{f.relative_to(base).as_posix()}" if skill else single] = f.read_bytes()
    elif src is not None:
        listing = git_bytes(root, "ls-tree", "-r", "--name-only", "-z", src, "--", f"skills/{name}/" if skill else single)
        for rel in (listing or b"").decode("utf-8", "replace").split("\0"):
            if rel and (blob := git_bytes(root, "show", f"{src}:{rel}")) is not None:
                found[rel] = blob
    else:
        base = root / (f"skills/{name}" if skill else single)
        for f in sorted(base.rglob("*")) if skill else [base]:
            if f.is_file():
                found[f.relative_to(root).as_posix()] = f.read_bytes()
    found = {p: b for p, b in found.items() if not any(p.startswith(s) for s in snapshot_skips(name))}
    return found if found and (not skill or f"skills/{name}/SKILL.md" in found) else None  # a skill needs its SKILL.md


def _text(data: bytes) -> str:
    return data.decode("utf-8", "replace")


def removed_units(prev: dict, cur: dict) -> list[dict]:
    """Units of the previous *.md files that no longer survive in any current file, longest first."""
    texts = [_text(b) for b in cur.values()]
    union = set().union(*(shingles(t) for t in texts))
    flat = [" " + " ".join(norm_tokens(t)) + " " for t in texts]
    out = []
    for path in sorted(p for p in prev if p.endswith(".md")):
        for unit in digest_units(_text(prev[path])):
            sh = shingles(unit)
            gone = 2 * len(sh & union) < len(sh) if sh else not any(" " + " ".join(norm_tokens(unit)) + " " in f for f in flat)
            if gone:
                out.append({"id": unit_id(unit), "path": path, "text": unit})
    return sorted(out, key=lambda u: -len(u["text"]))


def _lines(data: bytes) -> list[str] | None:
    try:
        return [s.strip() for s in data.decode("utf-8").splitlines() if s.strip()]
    except UnicodeDecodeError:
        return None


def removed_files(prev: dict, cur: dict, threshold: float = 0.5) -> list[dict]:
    """Previous non-markdown files that are gone, or that kept fewer than THRESHOLD of their non-blank lines."""
    out = []
    for path in sorted(p for p in prev if not p.endswith(".md")):
        old = _lines(prev[path])
        if path not in cur:
            out.append({"path": path, "status": "deleted", "lines": None if old is None else len(old), "kept": None if old is None else 0})
            continue
        new = _lines(cur[path])
        if old is None or new is None:
            if prev[path] != cur[path]:
                out.append({"path": path, "status": "changed", "lines": None, "kept": None})
        elif old:
            kept = len([s for s in old if s in set(new)])
            if kept < threshold * len(old):
                out.append({"path": path, "status": "changed", "lines": len(old), "kept": kept})
    return out


def render_digest(root: Path, name: str, src: str, prev: dict, cur: dict) -> str:
    units = removed_units(prev, cur)
    shown = units[:DIGEST_SHOWN]
    lines = [f"=== previous-version digest: {name} at {src} ===", "sections:"]
    for path in sorted(p for p in prev if p.endswith(".md")):
        text, fenced = _text(prev[path]).splitlines(), False
        for i, line in enumerate(text):
            fenced ^= bool(FENCE_RE.match(line))
            if not fenced and HEADING_RE.match(line):
                lines.append(f"- {path}: {line.strip()} | {next((s.strip() for s in text[i + 1:] if s.strip()), '')[:DIGEST_LINE_CUT]}")
    lines += ["- none"] if lines[-1] == "sections:" else []
    lines.append(f"removed units ({len(units)}, showing {len(shown)}):")
    lines += [f"- {u['id']} {u['path']}: {' '.join(u['text'].split())[:DIGEST_UNIT_CUT]}" for u in shown] or ["- none"]
    lines.append("removed or reduced files:")
    files = removed_files(prev, cur)
    for f in files:
        detail = "(binary)" if f["lines"] is None else f"({f['lines']} lines)" if f["status"] == "deleted" else f"({f['kept']}/{f['lines']} lines kept)"
        lines.append(f"- file:{f['path']} {f['status']} {detail}")
    lines += [] if files else ["- none"]
    record = root / "docs" / "audit" / "recovery" / name / "record.md"
    lines.append(f"record: {record.resolve() if record.is_file() else 'none'}")
    return "\n".join(lines) + "\n"


def resolves(root: Path, src: str) -> bool:
    """SRC names an existing directory or a git commit of ROOT."""
    return Path(src).is_dir() or (not src.startswith("-") and git_bytes(root, "rev-parse", "--verify", "--quiet", f"{src}^{{commit}}") is not None)


def default_ref(root: Path, kind: str, name: str) -> str | None:
    """Merge base with main when the branch has its own commits, else the parent of the artifact's newest commit."""
    head = (git_bytes(root, "rev-parse", "HEAD") or b"").decode().strip()
    base = "main" if git_bytes(root, "rev-parse", "--verify", "--quiet", "main") is not None else "origin/main"
    merge_base = (git_bytes(root, "merge-base", "HEAD", base) or b"").decode().strip()
    if merge_base and merge_base != head:
        return merge_base
    spec = [f"skills/{name}"] + [f":(exclude){s}" for s in snapshot_skips(name)] if kind == "skill" else [f"{ARTIFACT_DIRS[kind]}/{name}.md"]
    newest = (git_bytes(root, "log", "-1", "--format=%H", "--", *spec) or b"").decode().strip()
    parent = git_bytes(root, "rev-parse", "--verify", "--quiet", f"{newest}^") if newest else None
    return parent.decode().strip() if parent else None


def close_commit(root: Path, rel: str, batch_id) -> str | None:
    """The oldest commit at which the queue file shows the batch closed."""
    for sha in (git_bytes(root, "log", "--reverse", "--format=%H", "--", rel) or b"").decode().split():
        try:
            queue = json.loads(git_bytes(root, "show", f"{sha}:{rel}") or b"")
        except ValueError:
            continue
        if isinstance(queue, list) and any(isinstance(b, dict) and b.get("id") == batch_id and b.get("status") == "closed" for b in queue):
            return sha
    return None


def recovery_gate(root: Path, rel: str, name: str) -> tuple[bool, str | None]:
    """(deferred, close commit): deferred while a batch listing the artifact is not closed or the queue is absent."""
    path = root / rel
    if not path.is_file():
        return True, None
    try:
        queue = json.loads(path.read_text(encoding="utf-8"))
        batches = [b for b in queue if any((a.get("name") if isinstance(a, dict) else a) == name for a in b.get("artifacts", []))]
    except (ValueError, AttributeError, TypeError) as e:
        raise ValueError(f"--recovery-gate {rel}: not a batch queue ({e})") from e
    if any(b.get("status") != "closed" for b in batches):
        return True, None
    floor = None
    for b in batches:
        c = close_commit(root, rel, b.get("id"))
        if c and (floor is None or git_bytes(root, "merge-base", "--is-ancestor", floor, c) is not None):
            floor = c
    return False, floor


def digest_extras(root: Path, kind: str, names: list[str], previous: list[str], gate: str | None,
                  digest_dir: Path | None) -> str:
    """Text appended after the prompt: digest blocks (or digest-file lines) and notes; '' when none applies."""
    gate_rel = None
    if gate and not previous:  # an explicit --previous ignores the gate
        resolved = (root / gate).resolve()
        if not resolved.is_relative_to(root.resolve()):
            raise ValueError(f"--recovery-gate {gate} is outside the root")
        gate_rel = resolved.relative_to(root.resolve()).as_posix()
    for src in previous:
        if not resolves(root, src):
            raise ValueError(f"--previous {src} does not resolve")
        if Path(src).is_dir() and len(names) != 1:
            raise ValueError(f"--previous {src} is a directory: it needs exactly one --artifact")
    extra: list[str] = []
    blocks: dict[str, list[str]] = {}
    for src, name in [(s, n) for s in previous for n in names] if previous else [(None, n) for n in names]:
        ref, floor = src, None
        if src is None:
            if gate_rel:
                deferred, floor = recovery_gate(root, gate_rel, name)
                if deferred:
                    extra.append(f"removal check deferred for {name}: its content recovery has not closed ({gate})\n")
                    continue
            if not (root / ".git").exists():
                continue
            ref = default_ref(root, kind, name)
            if ref and floor and git_bytes(root, "merge-base", "--is-ancestor", ref, floor) is not None:
                ref = floor
        prev = artifact_snapshot(root, kind, name, ref) if ref else None
        if prev is None:
            extra.append(f"no previous version available for {name} at {ref or 'HEAD'}; the removal check was not run for it\n")
            continue
        block = render_digest(root, name, ref, prev, artifact_snapshot(root, kind, name, None) or {})
        if digest_dir is None:
            extra.append(block)
        else:
            if name not in blocks:
                extra.append(f"previous-version digest for {name}: {digest_dir.resolve() / (name + '.md')}\n")
            blocks.setdefault(name, []).append(block)
    if digest_dir is not None and blocks:
        digest_dir.mkdir(parents=True, exist_ok=True)
        for name, parts in blocks.items():
            (digest_dir / f"{name}.md").write_text("\n".join(parts), encoding="utf-8")
    return "\n".join(extra)


def render_judge_prompt(root: Path, kind: str, artifacts: list[Path], judge: str, previous: list[str] | None = None,
                        gate: str | None = None, digest_dir: Path | None = None) -> str:
    """Fill judge-prompt.md (command and agent: replace four sentences, append a profile), then append the digest."""
    text = judge_template_text(root, kind, artifacts, judge)
    extra = digest_extras(root, kind, [artifact_label(kind, p) for p in artifacts], previous or [], gate, digest_dir)
    return text.rstrip("\n") + "\n\n" + extra if extra else text


def judge_template_text(root: Path, kind: str, artifacts: list[Path], judge: str) -> str:
    if kind not in JUDGE_KINDS:
        raise ValueError(f"unknown kind {kind!r}")
    if kind != "skill" and len(artifacts) != 1:
        raise ValueError(f"--kind {kind} takes exactly one --artifact")
    if not artifacts:
        raise ValueError("need at least one --artifact")
    template = (judge_refs(root) / "judge-prompt.md").read_text(encoding="utf-8")
    names = ",".join(artifact_label(kind, p) for p in artifacts)
    root_s = str(root.resolve())
    if kind == "skill":
        return template.replace("{ROOT}", root_s).replace("{JUDGE}", judge).replace("{SKILLS}", names)
    text = (
        template
        .replace(SKILL_JUDGE_LINE, f"Judge this {kind}: {{SKILLS}}")
        .replace(SKILL_READ, ARTIFACT_READ)
        .replace(SKILL_PER, "per listed artifact")
        .replace(SKILL_SET, "Set `skill` to the file stem (the file name without `.md`).")
    )
    text = text.replace("{ROOT}/<path>", str(artifacts[0].resolve()))
    text = text.replace("{ROOT}", root_s).replace("{JUDGE}", judge).replace("{SKILLS}", names)
    profile = (judge_refs(root) / "profiles" / f"{kind}.md").read_text(encoding="utf-8")
    profile = PROFILE_BLOCK_RE.sub("", profile, count=1).rstrip("\n")
    return text.rstrip("\n") + "\n\n" + profile + "\n"


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
    except ValueError:
        pass
    # Graders quote shell code in evidence (a stray backslash before $ or .), which strict JSON
    # rejects. Retry once with every backslash that does not start a valid escape doubled.
    try:
        return json.loads(_double_invalid_escapes(body))
    except ValueError as e:
        raise HarnessError(f"{what}: answer is not JSON: {text.strip()[:200]!r}") from e


_JSON_ESCAPE = re.compile(r"\\(u[0-9a-fA-F]{4}|.)", re.S)


def _double_invalid_escapes(body: str) -> str:
    def fix(m):
        c = m.group(1)
        return m.group(0) if len(c) == 5 or c in '"\\/bfnrt' else "\\\\" + c
    return _JSON_ESCAPE.sub(fix, body)


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


def write_atomic(base: Path, path: Path, text: str) -> None:
    """write_inside, but via a same-directory temp file and os.replace so a crash never leaves a torn file."""
    if not path.resolve().is_relative_to(base):
        raise HarnessError(f"refusing to write {path} outside {base}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=path.name + ".", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    except BaseException:
        with contextlib.suppress(OSError):
            os.unlink(tmp)
        raise


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


def parse_trigger(text: str, what: str):
    """A trigger answer is one small object; accept it on the last line after a sentence of prose."""
    try:
        return parse_object(text, what)
    except HarnessError:
        last = (text.strip().splitlines() or [""])[-1].strip()
        try:
            data = json.loads(last)
        except ValueError:
            data = None
        if isinstance(data, dict) and set(data) == {"skill"}:
            return data
        raise


def eval_trigger_mode(root, name, runner, timeout, runs) -> dict:
    queries, cat = load_trigger_queries(root, name), catalog(root)
    passed, failures = 0, []
    for i, q in enumerate(queries):
        prompt = build_trigger_prompt(name, i, q["query"], cat)
        hits = 0
        for _ in range(runs):
            try:
                data = parse_trigger(call_runner(runner, prompt, timeout), f"{name}/q{i} trigger")
            except HarnessError:  # models sometimes wrap the answer in prose: ask once more
                data = parse_trigger(call_runner(runner, prompt, timeout), f"{name}/q{i} trigger")
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


REQUIRED_ENTRY_KEYS = {"skill", "kind", "source", "ref"}
OPTIONAL_ENTRY_KEYS = {"last_reviewed", "last_upstream_sha", "reviewed_for_model", "status", "new_path",
                       "artifact_kind", "credit"}
REVIEW_STATUSES = {"current", "stale", "path-moved", "unreachable"}
ARTIFACT_KINDS = set(KIND_DIR)
DATE_RE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")


def artifact_path(root: Path, name: str, artifact_kind: str) -> Path | None:
    """The on-disk path of an artifact, or None when the kind is unknown."""
    if artifact_kind == "skill":
        return root / "skills" / name
    if artifact_kind == "command":
        return root / "commands" / f"{name}.md"
    if artifact_kind == "agent":
        return root / "agents" / f"{name}.md"
    return None


def artifact_exists(root: Path, name: str, artifact_kind: str) -> bool:
    if os.sep in name or (os.altsep and os.altsep in name) or Path(name).name != name or name in (".", ".."):
        return False
    path = artifact_path(root, name, artifact_kind)
    if path is None:
        return False
    if artifact_kind == "skill":
        return path.is_dir() and path.resolve().is_relative_to((root / "skills").resolve())
    home = root / ("commands" if artifact_kind == "command" else "agents")
    return path.is_file() and path.resolve().is_relative_to(home.resolve())


def _calendar_date(value: str):
    try:
        return datetime.date.fromisoformat(value)
    except ValueError:
        return None


def valid_repo_path(value) -> bool:
    """A repository-relative path: no leading or trailing slash, no empty, '.' or '..' segment."""
    if not isinstance(value, str) or not value or value.startswith("/") or value.endswith("/"):
        return False
    return all(part.strip() not in ("", ".", "..") for part in value.split("/"))


def validate_entry(root: Path, entry) -> str | None:
    if not isinstance(entry, dict):
        return "entry must be an object"
    unknown = set(entry) - REQUIRED_ENTRY_KEYS - OPTIONAL_ENTRY_KEYS
    if not REQUIRED_ENTRY_KEYS.issubset(entry) or unknown:
        return "entry must have exactly skill, kind, source, ref"
    kind, skill, source, ref = (entry[k] for k in ("kind", "skill", "source", "ref"))
    if not isinstance(kind, str) or kind not in {"github", "github-path", "wikipedia", "repo", "unversioned", "local"}:
        return f"unsupported kind {kind!r}"
    if kind == "repo":
        if skill is not None:
            return "repo skill must be null"
    else:
        if not isinstance(skill, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", skill):
            return "skill must be a kebab-case name"
        artifact_kind = entry.get("artifact_kind", "skill")
        if artifact_kind not in ARTIFACT_KINDS:
            return f"unsupported artifact_kind {artifact_kind!r}"
        if not artifact_exists(root, skill, artifact_kind):
            label = "directory" if artifact_kind == "skill" else "file"
            return f"artifact {skill!r} does not exist as a {artifact_kind} {label}"
    if "artifact_kind" in entry and kind == "repo":
        return "artifact_kind is not valid on repo rows"
    if "credit" in entry:
        if kind in ("repo", "local"):
            return "credit is not valid on repo or local rows"
        if not isinstance(entry["credit"], str) or not entry["credit"].strip():
            return "credit must be a non-empty string"
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
    elif kind == "local":
        source_ok = source == ""
    else:
        source_ok = isinstance(source, str) and bool(source.strip())
    if not source_ok:
        return f"invalid source for {kind}"
    if kind in ("github", "github-path", "repo"):
        if not isinstance(ref, str) or not ref.strip():
            return f"{kind} ref must be a non-empty string"
    elif kind == "local":
        if ref != "":
            return "local ref must be empty"
    elif ref is not None:
        return f"{kind} ref must be null"
    reviewed = entry.get("last_reviewed")
    if "last_reviewed" in entry and (not isinstance(reviewed, str) or not DATE_RE.fullmatch(reviewed)
                                     or _calendar_date(reviewed) is None):
        return "last_reviewed must be YYYY-MM-DD"
    sha = entry.get("last_upstream_sha", None)
    if "last_upstream_sha" in entry and not (sha is None or isinstance(sha, str)):
        return "last_upstream_sha must be a string or null"
    model = entry.get("reviewed_for_model", None)
    if "reviewed_for_model" in entry and not (model is None or isinstance(model, str)):
        return "reviewed_for_model must be a string or null"
    status = entry.get("status", "current")
    if "status" in entry and status not in REVIEW_STATUSES:
        return f"status must be one of {', '.join(sorted(REVIEW_STATUSES))}"
    if "new_path" in entry:
        if kind != "github-path":
            return "new_path is valid only on github-path rows"
        if not valid_repo_path(entry["new_path"]):
            return "new_path must be a repository-relative path without a leading or trailing slash or '..'"
    return None


def source_query(entry: dict) -> str | None:
    kind, source, ref = entry["kind"], entry["source"], entry["ref"]
    if kind in ("github", "repo"):
        owner, repo = source.split("/", 1)
        return f"repos/{owner}/{repo}/commits?sha={urllib.parse.quote(ref, safe='')}&per_page=1"
    if kind == "github-path":
        repo, path = source.split(":", 1)
        path = entry.get("new_path") or path
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


def repo_ours_updated(root: Path, entry: dict) -> tuple[str | None, str | None]:
    """Return (our last-update timestamp, merge-base SHA) for a repo-kind entry.

    The merge-base SHA is None when the histories share no ancestor and only the
    oldest local root commit could be dated; consumers then link by ref alone.
    """
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
    merge_base = None
    if base_proc.returncode == 0:
        target = base_proc.stdout.strip()
        merge_base = target or None
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
        return None, None
    try:
        proc = subprocess.run(["git", "show", "-s", "--format=%cI", target], cwd=root,
                              capture_output=True, text=True)
    except OSError as exc:
        raise SourceUnavailable(str(exc)) from exc
    if proc.returncode:
        raise SourceUnavailable(proc.stderr.strip() or "git query failed")
    return (proc.stdout.strip() or None), merge_base


def ours_updated(root: Path, entry: dict) -> str | None:
    if entry["kind"] == "repo":
        return repo_ours_updated(root, entry)[0]
    name = entry["skill"]
    artifact_kind = entry.get("artifact_kind", "skill")
    if artifact_kind == "skill":
        paths = [f"skills/{name}/SKILL.md", f"skills/{name}/references/"]
    else:
        paths = [f"{'commands' if artifact_kind == 'command' else 'agents'}/{name}.md"]
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
        if isinstance(entry, dict) and entry.get("kind") == "local":
            continue
        skill = entry.get("skill") if isinstance(entry, dict) else None
        source = entry.get("source") if isinstance(entry, dict) else None
        kind = entry.get("kind") if isinstance(entry, dict) else None
        reason = validate_entry(root, entry)
        source_updated = ours = None
        error = None
        stale = None
        merge_base = None
        if reason:
            error = f"invalid entry: {reason}"
        else:
            try:
                if entry["kind"] != "unversioned":
                    source_updated = fetch_source_updated(entry)
                if entry["kind"] == "repo":
                    ours, merge_base = repo_ours_updated(root, entry)
                else:
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
        new_path = entry.get("new_path") if isinstance(entry, dict) else None
        rows.append({"skill": skill, "source": source, "kind": kind, "source_updated": source_updated,
                     "ours_updated": ours, "merge_base": merge_base, "stale": stale, "error": error,
                     "new_path": new_path})
    print(json.dumps(rows, indent=2))
    return 1 if failed else 0


def _track_fail(reason: str) -> tuple[int, dict | None]:
    print(f"track: {reason}", file=sys.stderr)
    return 2, None


def track(root: Path, registry: Path, artifact: str, status: str, source: str | None = None,
          artifact_kind: str = "skill", sha: str | None = None, model: str | None = None,
          new_path: str | None = None, today: str | None = None) -> tuple[int, dict | None]:
    """Upsert one artifact's review. Exit 2 writes nothing; the printed row is the addressed one.

    Without ``--source``, several ``local`` rows for the artifact are not an error: the first one
    in file order is the addressed row. Its per-source keys change; every other row of the artifact
    receives only ``last_reviewed`` and, when ``--model`` is given, ``reviewed_for_model``.
    """
    if status not in REVIEW_STATUSES:
        return _track_fail(f"invalid status {status!r}; expected one of {', '.join(sorted(REVIEW_STATUSES))}")
    if artifact in SYNCED:
        return _track_fail(f"artifact {artifact!r} is a synced skill and cannot be tracked")
    if not artifact_exists(root, artifact, artifact_kind):
        label = "directory" if artifact_kind == "skill" else "file"
        return _track_fail(f"artifact {artifact!r} does not exist as a {artifact_kind} {label}")
    try:
        loaded = json.loads(registry.read_text(encoding="utf-8"))
        if not isinstance(loaded, list):
            raise ValueError("registry must be a JSON list")
    except (OSError, ValueError, RecursionError) as exc:
        return _track_fail(f"cannot read registry {registry}: {exc}")
    entries = copy.deepcopy(loaded)
    if source is None:
        matches = [index for index, entry in enumerate(entries)
                   if isinstance(entry, dict) and entry.get("skill") == artifact and entry.get("kind") == "local"]
        if not matches:
            row = {"skill": artifact, "kind": "local", "source": "", "ref": "",
                   "last_upstream_sha": None, "reviewed_for_model": None}
            if artifact_kind != "skill":  # validate_entry looks for a skills/ directory unless told otherwise
                row["artifact_kind"] = artifact_kind
            entries.append(row)
            matches = [len(entries) - 1]
        index = matches[0]  # first local row in file order; later local rows stay per-source
    else:
        matches = [index for index, entry in enumerate(entries)
                   if isinstance(entry, dict) and entry.get("skill") == artifact and entry.get("source") == source
                   and entry.get("kind") != "repo"]
        if len(matches) != 1:
            return _track_fail(f"--source {source!r} matches {len(matches)} rows of {artifact!r}; expected one")
        index = matches[0]
    target = entries[index]
    if new_path is not None and target.get("kind") != "github-path":
        return _track_fail(f"--new-path is valid only on a github-path row, not {target.get('kind')!r}")
    reviewed = today or datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    for entry in entries:
        if isinstance(entry, dict) and entry.get("skill") == artifact and entry.get("kind") != "repo":
            entry["last_reviewed"] = reviewed
            if model is not None:
                entry["reviewed_for_model"] = model
    if sha is not None:
        target["last_upstream_sha"] = sha
    target["status"] = status
    if new_path is not None:
        target["new_path"] = new_path
    elif status != "path-moved":  # new_path names where a moved source lives: any other status drops it
        target.pop("new_path", None)
    for row_index, (before, entry) in enumerate(zip(loaded, entries)):
        if entry == before:
            continue
        if not isinstance(entry, dict):
            return _track_fail(f"invalid result: entry {row_index} must be an object")
        # A row this call rewrites must be valid before and after. Fixing a malformed sibling
        # by writing last_reviewed over it would hide a registry that upstreams already rejects.
        for candidate in (before, entry):
            if not isinstance(candidate, dict):
                return _track_fail(f"invalid result: entry {row_index} must be an object")
            reason = validate_entry(root, candidate)
            if reason:
                return _track_fail(f"invalid result: {reason}")
    for entry in entries[len(loaded):]:
        reason = validate_entry(root, entry)
        if reason:
            return _track_fail(f"invalid result: {reason}")
    text = json.dumps(entries, indent=2) + "\n"
    tmp_name = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False,
                                         dir=registry.parent, prefix=registry.name + ".") as tmp:
            tmp_name = tmp.name
            tmp.write(text)
        os.replace(tmp_name, registry)
        tmp_name = None
    except OSError as exc:
        return _track_fail(f"cannot write registry {registry}: {exc}")
    finally:
        if tmp_name is not None:
            try:
                os.unlink(tmp_name)
            except OSError:
                pass
    return 0, target


# ---------- scheduled audit ----------


def git_output(root: Path, *args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True)
    if proc.returncode:
        raise ValueError(proc.stderr.strip() or f"git {' '.join(args)} failed")
    return proc.stdout.strip()


def detect(state, spec_changed: bool, upstreams: list[dict], force: bool = False, root: Path | None = None) -> dict:
    """Compare committed skill trees and upstream timestamps with the saved audit state."""
    root = (root or default_root()).resolve()
    skills_dir = root / "skills"
    names = sorted(p.name for p in skills_dir.iterdir() if p.is_dir() and p.name not in SYNCED)
    judge_sha = git_output(root, "rev-parse", "HEAD:skills/skill-judge")
    trees = {name: git_output(root, "rev-parse", f"HEAD:skills/{name}") for name in names}
    old_valid = (isinstance(state, dict) and isinstance(state.get("judge_sha"), str)
                 and isinstance(state.get("skills"), dict)
                 and isinstance(state.get("upstreams", {}), dict)
                 and all(isinstance(v, str) for v in state["skills"].values()))
    old = state if old_valid else {}
    old_skills = old.get("skills", {})
    old_upstreams = old.get("upstreams", {})
    judge_changed = old_valid and old.get("judge_sha") != judge_sha
    changed_skills = sorted(name for name, sha in trees.items() if old_skills.get(name) != sha)
    expected_row_keys = {"skill", "source", "kind", "source_updated", "ours_updated", "stale"}
    for index, row in enumerate(upstreams):
        label = row.get("skill") if isinstance(row, dict) else None
        if (not isinstance(row, dict) or not expected_row_keys.issubset(row)
                or not isinstance(row.get("stale"), bool) or row.get("error") is not None
                or not isinstance(row.get("source"), str) or not row["source"]
                or not isinstance(row.get("kind"), str)
                or (row.get("skill") is not None and not isinstance(row.get("skill"), str))
                or (row.get("stale") is True and not isinstance(row.get("source_updated"), str))):
            raise ValueError(f"invalid upstream row {label or index}: malformed or contains an error")
    stale_rows = [row for row in upstreams if row["stale"] is True]
    upstream_new = []
    upstream_state = {}
    for row in stale_rows:
        key = f"{row.get('skill') or '-'}|{row.get('source')}"
        source_updated = row.get("source_updated")
        upstream_state[key] = source_updated
        if key not in old_upstreams or old_upstreams[key] != source_updated:
            upstream_new.append(row)
    reasons = []
    if spec_changed:
        reasons.append("spec_changed")
    if judge_changed:
        reasons.append("judge_changed")
    if changed_skills:
        reasons.append("skills_changed")
    if not old_valid:
        reasons.append("state_invalid")
    if force:
        reasons.append("force")
    if upstream_new:
        reasons.append("upstream_stale")
    full = spec_changed or judge_changed or not old_valid or force
    selected = names if full else changed_skills
    return {
        "run_needed": bool(reasons), "reasons": reasons, "spec_changed": bool(spec_changed),
        "skills": selected, "upstream_new": upstream_new,
        # Every other key of the input state (checked_at, last_attempt_at, Phase 2 fields) is carried verbatim;
        # the detect-owned keys always win.
        "state": {**(state if isinstance(state, dict) else {}),
                  "judge_sha": judge_sha, "skills": trees, "upstreams": upstream_state},
    }


INTERVAL_DAYS = (15, 30)
INTERVAL_SLACK = datetime.timedelta(hours=12)  # cron delay; checked_at is stamped at run end
FAILURE_BACKOFF_DAYS = 3
ON_POSITIVE = ("none", "label")
REVIEW_EFFORTS = ("none", "minimal", "low", "medium", "high", "xhigh", "max")  # CLI 1.0.103 help
MAX_JUDGE_LANES = 2


def parse_stamp(value):
    """Parse an ISO-8601 UTC stamp written as YYYY-MM-DDTHH:MM:SSZ; anything else is None."""
    if not isinstance(value, str):
        return None
    try:
        return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
    except ValueError:
        return None


def interval_days(value: str) -> int:
    """AUDIT_INTERVAL_DAYS: only 15 or 30 is accepted (fail-closed on anything else)."""
    if value.strip() not in [str(d) for d in INTERVAL_DAYS]:
        raise ValueError(f"AUDIT_INTERVAL_DAYS must be 15 or 30, got {value!r}")
    return int(value)


def interval_due(state, now: datetime.datetime, days: int, event: str) -> bool:
    """Whether a scheduled run should audit now. Only schedule events are gated by the interval.

    A missing or unparsable checked_at is due. A checked_at or last_attempt_at in the future is
    treated as absent, so a skewed clock cannot wedge the gate for longer than the cadence.
    """
    if days not in INTERVAL_DAYS:
        raise ValueError(f"AUDIT_INTERVAL_DAYS must be 15 or 30, got {days!r}")
    if event != "schedule":
        return True
    if not isinstance(state, dict):
        state = {}
    checked = parse_stamp(state.get("checked_at"))
    attempted = parse_stamp(state.get("last_attempt_at"))
    if checked is not None and checked > now:
        checked = None
    if attempted is not None and attempted > now:
        attempted = None
    interval_due_now = checked is None or now - checked >= datetime.timedelta(days=days) - INTERVAL_SLACK
    backoff_clear = attempted is None or now - attempted >= datetime.timedelta(days=FAILURE_BACKOFF_DAYS) - INTERVAL_SLACK
    return interval_due_now and backoff_clear


def validate_knobs(env: dict) -> list[str]:
    """Return the reasons the review and detect knobs are invalid; unset or empty knobs take their defaults."""
    errors = []
    raw_models = env.get("AUDIT_RESEARCH_MODELS") or "auto"
    lanes = [m.strip() for m in raw_models.split(",") if m.strip()]
    if not lanes:
        errors.append("AUDIT_RESEARCH_MODELS lists no judge lane")
    if len(lanes) > MAX_JUDGE_LANES:
        errors.append(f"AUDIT_RESEARCH_MODELS has {len(lanes)} lanes; at most two are allowed")
    seen_slugs = {}
    for lane in lanes:
        lane_slug = slug(lane)
        if not lane_slug:
            errors.append(f"judge lane {lane!r} has an empty slug")
        elif lane_slug in seen_slugs:
            errors.append(f"judge lanes {seen_slugs[lane_slug]!r} and {lane!r} collide (slug {lane_slug!r})")
        else:
            seen_slugs[lane_slug] = lane
    try:
        interval_days(env.get("AUDIT_INTERVAL_DAYS") or "15")
    except ValueError as e:
        errors.append(str(e))
    on_positive = env.get("AUDIT_ON_POSITIVE") or "label"
    if on_positive not in ON_POSITIVE:
        errors.append(f"AUDIT_ON_POSITIVE must be one of {', '.join(ON_POSITIVE)}, got {on_positive!r}")
    effort = env.get("AUDIT_REVIEW_EFFORT") or "high"
    if effort not in REVIEW_EFFORTS:
        errors.append(f"AUDIT_REVIEW_EFFORT must be one of {', '.join(REVIEW_EFFORTS)}, got {effort!r}")
    return errors


def branch_name(kind: str, title: str, date: str | None, suffix: str | None = None) -> str:
    """Build a dated, ASCII-safe audit branch name."""
    if date is None:
        date = datetime.datetime.now(datetime.timezone.utc).strftime("%y-%m-%d")
    if not re.fullmatch(r"[0-9]{2}-[0-9]{2}-[0-9]{2}", date):
        raise ValueError("date must match YY-MM-DD")
    try:
        datetime.datetime.strptime(date, "%y-%m-%d")
    except ValueError as exc:
        raise ValueError(f"invalid calendar date: {date}") from exc
    folded = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("ascii").lower()
    name = re.sub(r"[^a-z0-9]+", "-", folded).strip("-")[:50].rstrip("-")
    if suffix:
        tail = re.sub(r"[^a-z0-9]+", "-", suffix.lower()).strip("-")
        if tail:
            name = f"{name}-{tail}" if name else tail
    dated = f"{date}-{name}".rstrip("-")
    return f"{kind}/{dated}"


DECISION_KEYS = {"update", "type", "title", "targets", "rationale"}


def validate_decision(data, spec_changed: bool = False, structure_changed: bool = False,
                      root: Path | None = None) -> list[str]:
    """Return reasons a proposed audit decision violates its schema or target constraints."""
    root = (root or default_root()).resolve()
    if not isinstance(data, dict):
        return ["decision must be a JSON object"]
    errors = []
    missing = sorted(DECISION_KEYS - data.keys())
    unknown = sorted(data.keys() - DECISION_KEYS)
    if missing:
        errors.append(f"missing key(s): {', '.join(missing)}")
    if unknown:
        errors.append(f"unknown key(s): {', '.join(unknown)}")
    if not isinstance(data.get("type"), str) or data["type"] not in {"feat", "fix"}:
        errors.append("type must be feat or fix")
    if not isinstance(data.get("title"), str) or not data["title"].strip():
        errors.append("title must be non-empty")
    elif any(unicodedata.category(char) == "Cc" for char in data["title"]):
        errors.append("title must not contain control characters")
    rationale = data.get("rationale")
    if not isinstance(rationale, str) or not rationale.strip():
        errors.append("rationale must be a non-empty single-paragraph string")
    elif any(unicodedata.category(char) == "Cc" for char in rationale):
        errors.append("rationale must be a single paragraph without control characters")
    if not isinstance(data.get("update"), bool):
        errors.append("update must be a boolean")
    targets = data.get("targets")
    targets_ok = isinstance(targets, list) and all(isinstance(t, str) for t in targets)
    if not targets_ok:
        errors.append("targets must be a list of skill names")
        targets = []
    judge_skills = {p.name for p in (root / "skills").iterdir() if p.is_dir() and p.name not in SYNCED} \
        if (root / "skills").is_dir() else set()
    allowed_targets = judge_skills
    for target in targets:
        path = root / "skills" / target
        valid = (target in allowed_targets and target == Path(target).name
                 and target not in (".", "..")
                 and path.is_dir() and path.resolve().is_relative_to((root / "skills").resolve()))
        if not valid:
            errors.append(f"invalid target: {target}")
    update = data.get("update") is True
    if update and not targets:
        errors.append("targets must be non-empty when update is true")
    if data.get("update") is False and targets_ok and targets:
        errors.append("targets must be empty when update is false")
    if spec_changed and (not update or "skill-judge" not in targets):
        errors.append("spec_changed requires update=true and target skill-judge")
    if structure_changed and (not update or not {"agentskills-research", "skill-judge"}.issubset(targets)):
        errors.append("structure_changed requires update=true and targets agentskills-research and skill-judge")
    return errors


# ---------- CLI ----------


# ---------- batches ----------

BATCH_STATUSES = ("queued", "open", "closed", "requeued")
MAX_REQUEUES = 2


def finding_key(artifact: str, finding: dict) -> tuple:
    """Finding identity: merge's dedup key plus the artifact (verdict ids repeat and are renumbered)."""
    return (artifact, finding["dimension"], finding["file"], finding["fix"].lower())


def load_merged_entries(files: list[Path]) -> dict[str, dict]:
    """Artifact entries by name; later files win."""
    entries: dict[str, dict] = {}
    for f in files:
        data = load_json(f)
        if not isinstance(data, dict) or not isinstance(data.get("skills"), list):
            raise ValueError(f"{f}: no top-level skills array")
        for e in data["skills"]:
            entries[e["name"]] = e
    return entries


def batch_counts(entry: dict) -> dict:
    c = Counter(f["severity"] for f in entry.get("findings", []))
    return {s: c.get(s, 0) for s in SEVERITIES}


def brief_order(findings: list[dict]) -> list[dict]:
    """Critical, high and D7/D8 first, then the rest; report order inside each group."""
    first = [f for f in findings if f["severity"] in ("critical", "high") or f["dimension"] in ("D7", "D8")]
    return first + [f for f in findings if f not in first]


def render_brief(batch_id: int, artifacts: list[dict], entries: dict[str, dict]) -> str:
    lines = [f"# Batch {batch_id:02d}", ""]
    for a in artifacts:
        lines += [f"## {a['name']} ({a['kind']})", ""]
        for f in brief_order(entries[a["name"]].get("findings", [])):
            loc = f["file"] if f.get("line") is None else f"{f['file']}:{f['line']}"
            lines += [f"### {a['name']}#{f['id']}", f"- severity: {f['severity']}", f"- dimension: {f['dimension']}",
                      f"- location: {loc}", f"- fix: {f['fix']}", ""]
    return "\n".join(lines)


def batch_artifact(name: str, entry: dict, kinds: dict[str, str]) -> dict:
    if name not in kinds:
        raise ValueError(f"{name}: not a skill, command or agent in this repo")
    return {"kind": kinds[name], "name": name, "percent": entry.get("percent"), "findings": batch_counts(entry)}


def write_batch_brief(root: Path, out: Path, batch: dict, entries: dict[str, dict]) -> None:
    path = root / batch["brief"] if not Path(batch["brief"]).is_absolute() else Path(batch["brief"])
    write_inside(out, path, render_brief(batch["id"], batch["artifacts"], entries))


def brief_path(root: Path, out: Path, batch_id: int, artifacts: list[dict]) -> str:
    name = f"{batch_id:02d}-{'-'.join(a['name'] for a in artifacts)}.md"
    base = out.resolve()
    rel = base.relative_to(root) if base.is_relative_to(root) else base
    return str(rel / "batches" / name)


def is_queued(e: dict) -> bool:
    pct = e.get("percent")
    return not e.get("synced") and ((pct is None or pct < TARGET_CLOSE)
                                   or any(f["severity"] in ("critical", "high") for f in e.get("findings", [])))


TARGET_CLOSE = 90


def generate_batches(root: Path, out: Path, files: list[Path], max_art: int, max_find: int, exclude: set[str]) -> int:
    entries = load_merged_entries(files)
    path = out / "batches.json"
    queue = load_json(path) if path.is_file() else []
    present = {a["name"] for b in queue for a in b["artifacts"]}
    todo = sorted((e for n, e in entries.items() if n not in present and n not in exclude and is_queued(e)),
                  key=lambda e: -1 if e.get("percent") is None else e["percent"])  # stable: report order on ties
    kinds = {a["name"]: a["kind"] for a in list_artifacts(root)}
    groups: list[list[dict]] = []
    cur, size = [], 0
    for e in todo:
        n = len(e.get("findings", []))
        a = batch_artifact(e["name"], e, kinds)
        if n > max_find:
            groups += [g for g in (cur, [a]) if g]
            cur, size = [], 0
        elif cur and (len(cur) >= max_art or size + n > max_find):
            groups.append(cur)
            cur, size = [a], n
        else:
            cur.append(a)
            size += n
    if cur:
        groups.append(cur)
    next_id = max((b["id"] for b in queue), default=0) + 1
    new = []
    for i, g in enumerate(groups):
        bid = next_id + i
        new.append({"id": bid, "artifacts": g, "brief": brief_path(root, out, bid, g), "status": "queued",
                    "rounds": 0, "requeues": 0, "waived": []})
    for b in new:
        write_batch_brief(root, out, b, entries)
    save_queue(out, queue + new)
    return 0


def save_queue(out: Path, queue: list[dict]) -> None:
    write_atomic(out, out / "batches.json", json.dumps(queue, indent=2) + "\n")


def load_queue(out: Path) -> list[dict]:
    if not (out / "batches.json").is_file():
        raise ValueError(f"{out / 'batches.json'} does not exist")
    return load_json(out / "batches.json")


def find_batch(queue: list[dict], batch_id: int) -> dict:
    for b in queue:
        if b["id"] == batch_id:
            return b
    raise ValueError(f"no batch with id {batch_id}")


def batches_op(root: Path, args) -> int:
    out = Path(os.path.abspath(args.out)) if args.out else root / "docs" / "audit"  # absolute, unresolved: write_inside compares against it
    if args.op == "generate":
        return generate_batches(root, out, args.merged, args.max_artifacts, args.max_findings, set(args.exclude))
    queue = load_queue(out)
    if args.op == "set":
        if args.status not in BATCH_STATUSES:
            raise ValueError(f"status must be one of {', '.join(BATCH_STATUSES)}")
        find_batch(queue, args.id)["status"] = args.status
    elif args.op == "waive":
        batch = find_batch(queue, args.id)
        if not args.reason.strip():
            raise ValueError("waive needs a non-empty reason")
        hits = [f for f in load_merged_entries(args.merged).get(args.artifact, {}).get("findings", [])
                if f["dimension"] == args.dimension and f["file"] == args.file]
        if not hits:
            raise ValueError(f"no finding of {args.artifact} matches {args.dimension} {args.file}")
        have = {finding_key(w["artifact"], w) for w in batch["waived"]}
        for f in hits:
            if finding_key(args.artifact, f) not in have:
                batch["waived"].append({"artifact": args.artifact, "dimension": f["dimension"], "file": f["file"],
                                        "fix": f["fix"], "reason": args.reason})
    elif args.op == "requeue":
        batch = find_batch(queue, args.id)
        entries = load_merged_entries(args.merged)
        if args.artifact not in [a["name"] for a in batch["artifacts"]] or args.artifact not in entries:
            raise ValueError(f"{args.artifact} is not in batch {args.id} or has no verdict")
        if batch["requeues"] + 1 > MAX_REQUEUES:
            print(f"requeue: {args.artifact} was requeued {MAX_REQUEUES} times; waive or stop", file=sys.stderr)
            return 3
        kinds = {a["name"]: a["kind"] for a in list_artifacts(root)}
        art = batch_artifact(args.artifact, entries[args.artifact], kinds)
        batch["artifacts"] = [a for a in batch["artifacts"] if a["name"] != args.artifact]
        if not batch["artifacts"]:
            batch["status"] = "requeued"
        bid = max(b["id"] for b in queue) + 1
        new = {"id": bid, "artifacts": [art], "brief": brief_path(root, out, bid, [art]), "status": "queued",
               "rounds": 0, "requeues": batch["requeues"] + 1,
               "waived": [w for w in batch["waived"] if w["artifact"] == args.artifact]}  # waivers follow the artifact
        at = next((i for i, b in enumerate(queue) if b["status"] == "queued"), len(queue))
        queue.insert(at, new)
        write_batch_brief(root, out, new, entries)
    elif args.op == "check":
        entries = load_merged_entries(args.merged)
        bad = False
        for b in queue:
            if b["status"] != "closed":
                continue
            keys = {finding_key(w["artifact"], w) for w in b["waived"]}
            for a in b["artifacts"]:
                if a.get("mode") == "report-only":  # never judged (plan 14): its batch closes on sources and facts alone
                    continue
                e = entries.get(a["name"])
                if e is None or e.get("percent") is None or e["percent"] < TARGET_CLOSE:
                    print(f"batch {b['id']}: {a['name']} has no verdict or scores below {TARGET_CLOSE}")
                    bad = True
                if e is None:
                    continue
                for f in e.get("findings", []):
                    if f["severity"] == "low":
                        print(f"residual low: {a['name']}#{f['id']} {f['dimension']} {f['file']}")
                    elif finding_key(a["name"], f) not in keys:
                        print(f"batch {b['id']}: unwaived {f['severity']} {a['name']}#{f['id']} {f['dimension']} {f['file']}")
                        bad = True
        return 1 if bad else 0
    save_queue(out, queue)
    return 0


# ---------- content recovery (plan 14) ----------

RECOVERY = Path("docs/audit/recovery")
SECTION_MIN_WORDS, CHUNK_CHARS = 12, 1500
VERDICTS = ("present", "partial", "absent", "contradicted")
PRESENCE_QUESTION = (
    "Is this previous section's guidance in the current files? Answer on one line with two words: present, partial, "
    "absent or contradicted; then yes or no for whether the section is substantive (a template, procedure, rule or "
    "fact a user would miss)."
)
RECORD_HEADER = ["item", "fate", "value", "decision", "reason class", "reason"]
RESTORE_CLASSES = ("users-ask-by-name", "reusable-template", "tested-example", "procedure-depends")
REASON_CLASSES = {
    "restore-references": RESTORE_CLASSES, "restore-main": RESTORE_CLASSES,
    "drop": ("generic-model-knowledge", "stale", "wrong", "out-of-scope", "superseded-by "),
    "drop-pending": ("generic-model-knowledge", "stale", "wrong", "out-of-scope", "superseded-by "),
    "intended-change": ("safety-fix", "fact-update", "scope-change"),
    "purpose-change-pending": ("safety-fix", "fact-update", "scope-change"),
    "none": ("moved-to ", "text-present"),
}  # a trailing space marks a prefix class that needs an argument


def find_artifact(root: Path, name: str, kind: str | None = None) -> dict:
    found = [a for a in list_artifacts(root) if a["name"] == name and kind in (None, a["kind"])]
    if len(found) != 1:
        raise ValueError(f"{name}: not a unique skill, command or agent in this repo")
    return found[0]


def text_files(snap: dict) -> dict[str, str]:
    out = {}
    for p, b in snap.items():
        with contextlib.suppress(UnicodeDecodeError):
            out[p] = b.decode("utf-8")
    return out


def commit_of(root: Path, ref: str) -> str | None:
    got = git_bytes(root, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}") if not ref.startswith("-") else None
    return got.decode().strip() if got else None


def split_sections(text: str) -> list[tuple[str, list[str]]]:
    sections, heading, body, fenced = [], "(preamble)", [], False
    for line in text.splitlines():
        fenced ^= bool(FENCE_RE.match(line))
        if not fenced and HEADING_RE.match(line):
            sections.append((heading, body))
            heading, body = line.strip().lstrip("#").strip(), []
        else:
            body.append(line)
    return sections + [(heading, body)]


def chunk_units(body: str, units: list[str]) -> list[tuple[str, list[str]]]:
    """(text, unit ids) chunks of at most CHUNK_CHARS, cut at unit boundaries (one unit over the cap stays whole)."""
    if len(body) <= CHUNK_CHARS or not units:
        return [(body, [unit_id(u) for u in units])]
    chunks: list[list[str]] = [[]]
    for u in units:
        if chunks[-1] and len("\n\n".join(chunks[-1] + [u])) > CHUNK_CHARS:
            chunks.append([])
        chunks[-1].append(u)
    return [("\n\n".join(c), [unit_id(u) for u in c]) for c in chunks]


def inventory_sections(snap: dict) -> list[dict]:
    out = []
    for path in sorted(p for p in snap if p.endswith(".md")):
        for heading, lines in split_sections(_text(snap[path])):
            body = "\n".join(lines).strip()
            if len(norm_tokens(body)) < SECTION_MIN_WORDS:
                continue
            for text, ids in chunk_units(body, digest_units(body)):
                out.append({"id": f"s{len(out) + 1:03d}", "file": path, "heading": heading, "text": text,
                            "chars": len(text), "units": ids})
    return out


def phrase_fate(root: Path, prev: dict, cur: dict) -> dict:
    """Share of the baseline's 5-word shingles kept in the same file, moved to another file of any artifact, or gone."""
    owners: dict[tuple, set[str]] = {}
    for a in list_artifacts(root):
        for path, text in text_files(artifact_snapshot(root, a["kind"], a["name"], None) or {}).items():
            for sh in shingles(text):
                owners.setdefault(sh, set()).add(path)
    counts, total, old = Counter(), 0, set()
    for path, text in text_files({p: b for p, b in prev.items() if p.endswith(".md")}).items():
        for sh in shingles(text):
            total += 1
            old.add(sh)
            where = owners.get(sh, set())
            counts["kept" if path in where else "moved" if where else "gone"] += 1
    now = set().union(*(shingles(t) for t in text_files(cur).values()))
    pct = lambda n, d: round(100 * n / d, 2) if d else 0.0
    kept, moved = pct(counts["kept"], total), pct(counts["moved"], total)
    return {"kept": kept, "moved": moved, "gone": round(100 - kept - moved, 2) if total else 0.0,
            "new": pct(len(now - old), len(now))}


def recovery_inventory(root: Path, args) -> int:
    art = find_artifact(root, args.artifact, args.kind)
    if not resolves(root, args.base):
        raise ValueError(f"cannot resolve --base {args.base}")
    prev = artifact_snapshot(root, art["kind"], art["name"], args.base)
    if prev is None:
        raise ValueError(f"{art['name']} does not exist at {args.base}")
    cur = artifact_snapshot(root, art["kind"], art["name"], None) or {}
    fate = phrase_fate(root, prev, cur)
    if args.fate_only:
        print(json.dumps(fate, indent=2))
        return 0
    data = {"base": args.base, "sections": inventory_sections(prev), "files": removed_files(prev, cur, 1.0), "phrase_fate": fate}
    d = root / RECOVERY / art["name"]
    write_atomic(root / RECOVERY, d / "sections.json", json.dumps(data, indent=2) + "\n")
    (d / "presence.partial.json").unlink(missing_ok=True)  # its verdicts belong to the old sections
    return 0


def read_recovery(root: Path, name: str, what: str):
    path = root / RECOVERY / name / what
    if not path.is_file():
        raise ValueError(f"{path} does not exist")
    return load_json(path)


def parse_presence(out: str) -> tuple[str, bool]:
    line = next((x for x in out.splitlines() if x.strip()), "")
    tok = line.lower().split()
    if len(tok) != 2 or tok[0] not in VERDICTS or tok[1] not in ("yes", "no"):
        raise ValueError(f"malformed answer line {line[:80]!r}")
    return tok[0], tok[1] == "yes"


def recovery_presence(root: Path, args) -> int:
    art = find_artifact(root, args.artifact)
    name = art["name"]
    sections = read_recovery(root, name, "sections.json")["sections"]
    argv = resolve_runner(args.runner)
    state = "".join(f"=== {p} ===\n{t.rstrip(chr(10))}\n" for p, t in sorted(text_files(artifact_snapshot(root, art["kind"], name, None) or {}).items()))
    base, d = root / RECOVERY, root / RECOVERY / name
    partial = d / "presence.partial.json"
    done = {e["id"]: e for e in (load_json(partial) if partial.is_file() else [])}
    failed = []
    for s in sections:
        if s["id"] in done:
            continue
        prompt = (f"MODE: presence\nKEY: {name}/{s['id']}\n\n{state}\n=== previous section {s['id']}: {s['heading']} ===\n"
                  f"{s['text']}\n\n{PRESENCE_QUESTION}\n")
        try:
            verdict, substantive = parse_presence(call_runner(argv, prompt, args.timeout))
        except (HarnessError, ValueError) as e:
            failed.append(f"{s['id']}: {e}")
            continue
        done[s["id"]] = {"id": s["id"], "verdict": verdict, "substantive": substantive}
        write_atomic(base, partial, json.dumps(list(done.values()), indent=2) + "\n")
    if failed:
        print(f"presence: {len(failed)} section(s) failed, re-run to resume:\n" + "\n".join(failed), file=sys.stderr)
        return 1
    write_atomic(base, d / "presence.json", json.dumps([done[s["id"]] for s in sections], indent=2) + "\n")
    partial.unlink(missing_ok=True)
    return 0


def recovery_grep(root: Path, args) -> int:
    art = find_artifact(root, args.artifact)
    sections = {s["id"]: s for s in read_recovery(root, art["name"], "sections.json")["sections"]}
    others = {}
    for a in list_artifacts(root):
        if a["name"] != art["name"]:
            others.update(text_files(artifact_snapshot(root, a["kind"], a["name"], None) or {}))
    other_sh = {p: shingles(t) for p, t in others.items()}
    out = []
    for e in read_recovery(root, art["name"], "presence.json"):
        if e["verdict"] not in ("absent", "partial"):
            continue
        s = sections[e["id"]]
        sh = shingles(s["text"])
        hits = sorted(((len(sh & o) / len(sh), p) for p, o in other_sh.items() if sh), key=lambda m: (-m[0], m[1]))
        out.append({"id": s["id"], "heading": s["heading"], "verdict": e["verdict"],
                    "matches": [{"path": p, "share": round(sh_, 4)} for sh_, p in hits if sh_ >= args.min_share]})
    print(json.dumps(out, indent=2))
    return 0


def recovery_mode(root: Path, a: dict, base: str) -> str:
    if a["name"] in SYNCED:
        return "report-only"
    if artifact_snapshot(root, a["kind"], a["name"], base) is None:
        return "facts-only"
    return "facts-only" if git_bytes(root, "diff", "--quiet", base, "--", a["path"]) is not None else "full"


def parse_record(path: Path) -> tuple[list[dict], list[str]]:
    """Rows of a record.md table and the format problems found while reading it."""
    if not path.is_file():
        return [], []
    rows, problems, header = [], [], False
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip().strip("`").strip() for c in line.strip().strip("|").split("|")]
        if not header:
            header = True
            if cells != RECORD_HEADER:
                problems.append(f"record.md:{n}: header is not '| {' | '.join(RECORD_HEADER)} |'")
            continue
        if all(set(c) <= set("-: ") for c in cells):
            continue
        if len(cells) < 6:
            problems.append(f"record.md:{n}: row has {len(cells)} fields, needs 6")
            continue
        rows.append(dict(zip(RECORD_HEADER, cells[:5] + ["|".join(cells[5:])]), line=n))
    return rows, problems


def row_problems(row: dict) -> list[str]:
    item, fate, value, decision = row["item"], row["fate"], row["value"], row["decision"]
    where, out = f"record.md:{row['line']} {item}", []
    classes = REASON_CLASSES.get(decision)
    redistributed = fate.startswith("redistributed ") and bool(fate[len("redistributed "):].strip())
    if classes is None:
        return [f"{where}: unknown decision {decision!r}"]
    if not (fate in ("removed-to-fit", "removed-on-merit", "not-lost") or redistributed):
        out.append(f"{where}: unknown fate {fate!r}")
    if value not in ("real", "low"):
        out.append(f"{where}: value must be real or low, got {value!r}")
    rc = row["reason class"]
    if not any(rc == c or (c.endswith(" ") and rc.startswith(c) and rc[len(c):].strip()) for c in classes):
        out.append(f"{where}: reason class {rc!r} is not valid for decision {decision}")
    if not row["reason"]:
        out.append(f"{where}: empty reason")
    allowed = {
        "restore-references": fate == "removed-to-fit" and value == "real",
        "restore-main": fate == "removed-to-fit" and value == "real",
        "drop": fate == "removed-on-merit" or (fate == "removed-to-fit" and value == "low"),
        "drop-pending": fate == "removed-on-merit" or (fate == "removed-to-fit" and value == "low"),
        "intended-change": fate == "removed-on-merit",
        "purpose-change-pending": fate != "not-lost" and not redistributed,
        "none": fate == "not-lost" or redistributed,
    }[decision]
    if not allowed:
        out.append(f"{where}: ({fate}, {value}, {decision}) is not an allowed combination")
    return out


def has_row(rows: list[dict], key: str) -> bool:
    return any(r["item"] == key or (r["item"].startswith(key) and not re.match(r"\w", r["item"][len(key):])) for r in rows)


def recovery_record_check(root: Path, args) -> int:
    art = find_artifact(root, args.artifact)
    name = art["name"]
    inv = read_recovery(root, name, "sections.json")
    sections = inv["sections"]
    rows, problems = parse_record(root / RECOVERY / name / "record.md")
    for r in rows:
        problems += row_problems(r)
    pres_path = root / RECOVERY / name / "presence.json"
    verdicts = {e["id"]: e["verdict"] for e in load_json(pres_path)} if pres_path.is_file() else {}
    for s in sections:
        if s["id"] not in verdicts:
            problems.append(f"presence.json has no verdict for {s['id']} {s['heading']}")
        elif verdicts[s["id"]] != "present" and not has_row(rows, s["id"]):
            problems.append(f"{s['id']} {s['heading']} ({verdicts[s['id']]}) has no record row")
    for f in inv["files"]:
        if not has_row(rows, f"file:{f['path']}"):
            problems.append(f"file:{f['path']} ({f['status']}) has no record row")
    cur = artifact_snapshot(root, art["kind"], name, None) or {}
    for ref in args.previous:
        prev = artifact_snapshot(root, art["kind"], name, ref)
        if prev is None:
            problems.append(f"{name} does not exist at {ref}")
            continue
        at_base = (commit_of(root, ref) or ref) == (commit_of(root, inv["base"]) or inv["base"])
        reported: set[str] = set()
        for u in removed_units(prev, cur):
            owning = [s for s in sections if u["id"] in s["units"]] if at_base else []
            if any(has_row(rows, s["id"]) for s in owning) or has_row(rows, u["id"]):
                continue
            if owning:  # one report per section; a section with no verdict row is reported above already
                for s in owning:
                    if verdicts.get(s["id"]) == "present" and s["id"] not in reported:
                        reported.add(s["id"])
                        problems.append(f"{s['id']} {s['heading']} (present) has removed units and no record row")
            else:
                problems.append(f"{u['id']} removed since {ref} ({u['path']}) has no record row")
        for f in removed_files(prev, cur, 0.5):
            if not has_row(rows, f"file:{f['path']}"):
                problems.append(f"file:{f['path']} removed since {ref} has no record row")
    for p in dict.fromkeys(problems):
        print(p)
    return 1 if problems else 0


def recovery_brief(batch: dict, info: dict, pending: dict[str, list[dict]]) -> str:
    lines = [f"# Recovery batch {batch['id']:02d}", ""]
    for a in batch["artifacts"]:
        i = info[a["name"]]
        lines += [f"## {a['name']} ({a['kind']})", "", f"- mode: {a['mode']}"]
        if a["mode"] == "full":
            rel = (RECOVERY / a["name"]).as_posix()
            lines += [f"- sections: {rel}/sections.json", f"- presence: {rel}/presence.json", "", "### Sections to triage", ""]
            lines += [f"- {s['id']} {s['heading']} | {v} | {s['chars']} chars" for s, v in i["lost"]] or ["- none"]
            lines += ["", "### Files", ""]
            for f in i["files"]:
                lines.append(f"- file:{f['path']} {f['status']}" + ("" if f["lines"] is None else f" ({f['lines']} lines)"))
            lines += [] if i["files"] else ["- none"]
        rows = pending.get(a["name"], [])
        lines += ["", "### Pending purpose change", ""] if rows else []
        lines += [f"- {r['item']} | {r['fate']} | {r['value']} | {r['decision']} | {r['reason class']} | {r['reason']}" for r in rows]
        lines.append("")
    return "\n".join(lines)


def recovery_queue(root: Path, args) -> int:
    out = Path(os.path.abspath(args.out)) if args.out else root / RECOVERY
    if commit_of(root, args.base) is None:
        raise ValueError(f"cannot resolve --base {args.base}")
    path = out / "batches.json"
    if args.append is None and path.is_file():
        print(f"queue: {path} exists; the queue is built once (use --append NAME to add a batch)", file=sys.stderr)
        return 1
    if args.append is not None and not path.is_file():
        print(f"queue: {path} does not exist", file=sys.stderr)
        return 1
    arts = [find_artifact(root, args.append)] if args.append is not None else list_artifacts(root)
    info, missing = {}, []
    for a in arts:
        i = {"mode": recovery_mode(root, a, args.base), "share": 0.0, "lost": [], "files": []}
        if i["mode"] == "full":
            try:
                inv = read_recovery(root, a["name"], "sections.json")
                pres = {e["id"]: e["verdict"] for e in read_recovery(root, a["name"], "presence.json")}
            except (OSError, ValueError):
                missing.append(f"{a['name']}: needs sections.json and a complete presence.json")
                continue
            gap = [s["id"] for s in inv["sections"] if s["id"] not in pres]
            if gap:
                missing.append(f"{a['name']}: presence.json lacks {', '.join(gap)}")
                continue
            i["lost"] = [(s, pres[s["id"]]) for s in inv["sections"] if pres[s["id"]] != "present"]
            total = sum(s["chars"] for s in inv["sections"])
            i["share"] = sum(s["chars"] for s, _ in i["lost"]) / total if total else 0.0
            i["files"] = inv["files"]
        info[a["name"]] = i
    if missing:
        print("\n".join(missing), file=sys.stderr)
        return 1
    rank = {"full": 0, "facts-only": 1, "report-only": 2}
    ordered = sorted(arts, key=lambda a: (rank[info[a["name"]]["mode"]], -info[a["name"]]["share"], a["name"]))
    groups: list[list[dict]] = []
    for a in ordered:
        if groups and len(groups[-1]) < args.max_artifacts and info[groups[-1][0]["name"]]["mode"] == info[a["name"]]["mode"]:
            groups[-1].append(a)
        else:
            groups.append([a])
    queue = load_json(path) if args.append is not None else []
    next_id = max((b["id"] for b in queue), default=0) + 1
    pending = {}
    if args.append is not None:
        rows, _ = parse_record(root / RECOVERY / args.append / "record.md")
        pending = {args.append: [r for r in rows if r["decision"] == "purpose-change-pending"]}
    new = []
    for k, g in enumerate(groups):
        entries = [{"kind": a["kind"], "name": a["name"], "percent": None, "findings": batch_counts({}),
                    "mode": info[a["name"]]["mode"]} for a in g]
        new.append({"id": next_id + k, "artifacts": entries, "brief": brief_path(root, out, next_id + k, entries),
                    "status": "queued", "rounds": 0, "requeues": 0, "waived": []})
    for b in new:
        write_inside(out, root / b["brief"] if not Path(b["brief"]).is_absolute() else Path(b["brief"]),
                     recovery_brief(b, info, pending))
    save_queue(out, queue + new)
    return 0


def recovery_check(root: Path, args) -> int:
    out = Path(os.path.abspath(args.out)) if args.out else root / RECOVERY
    rounds = []
    for bd in (out / "batches").glob("*") if (out / "batches").is_dir() else []:
        for rd in bd.glob("r*") if bd.is_dir() and bd.name.isdigit() else []:
            if rd.name[1:].isdigit() and (rd / "merged.json").is_file():
                rounds.append((int(bd.name), int(rd.name[1:]), rd / "merged.json"))
    ns = argparse.Namespace(op="check", out=out, merged=[f for _, _, f in sorted(rounds)])
    return batches_op(root, ns)


def recovery_op(root: Path, args) -> int:
    ops = {"inventory": recovery_inventory, "presence": recovery_presence, "grep": recovery_grep,
           "queue": recovery_queue, "record-check": recovery_record_check, "check": recovery_check}
    return ops[args.op](root, args)


def csv(value: str) -> list[str]:
    return [v for v in value.split(",") if v]


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--root", type=Path, default=None)
    sub = p.add_subparsers(dest="cmd", required=True)
    detect_cmd = sub.add_parser("detect")
    detect_cmd.add_argument("--state", required=True)
    detect_cmd.add_argument("--spec-changed", choices=["true", "false"], required=True)
    detect_cmd.add_argument("--upstreams", type=Path, required=True)
    detect_cmd.add_argument("--force", action="store_true")
    interval = sub.add_parser("interval-due")
    interval.add_argument("--state", required=True)
    interval.add_argument("--now", default=None)
    interval.add_argument("--days", required=True)
    interval.add_argument("--event", default="schedule")
    sub.add_parser("validate-knobs")
    branch = sub.add_parser("branch-name")
    branch.add_argument("--type", choices=["feat", "fix"], required=True)
    branch.add_argument("--title", required=True)
    branch.add_argument("--date", default=None)
    branch.add_argument("--suffix", default=None)
    decision = sub.add_parser("validate-decision")
    decision.add_argument("file", type=Path)
    decision.add_argument("--spec-changed", action="store_true")
    decision.add_argument("--structure-changed", action="store_true")
    up = sub.add_parser("upstreams")
    up.add_argument("--registry", type=Path, required=True)
    tr = sub.add_parser("track", help="record a review of one artifact against its sources")
    tr.add_argument("--registry", type=Path, default=None)
    tr.add_argument("--artifact", required=True)
    tr.add_argument("--artifact-kind", choices=sorted(ARTIFACT_KINDS), default="skill")
    tr.add_argument("--source", default=None)
    tr.add_argument("--status", required=True)
    tr.add_argument("--sha", default=None)
    tr.add_argument("--model", default=None)
    tr.add_argument("--new-path", default=None)
    tr.add_argument("--today", default=None)
    c = sub.add_parser("check")
    c.add_argument("--strict", action="store_true")
    c.add_argument("--skills", type=csv, default=None)
    c.add_argument("--kind", choices=sorted(ARTIFACT_KINDS), default="skill")
    c.add_argument("--ignore", type=csv, default=[])
    c.add_argument("--allowlist", type=Path, default=None, help="skill kind only; ignored for command/agent")
    c.add_argument("--validator-pin", type=Path, default=None,
                   help="trusted SOURCE.json that selects the skills-ref validator (not the data root's); skill kind only")
    bt = sub.add_parser("batches", help="generate and track fix batches from merged verdicts")
    bt_sub = bt.add_subparsers(dest="op", required=True)
    for op in ("generate", "set", "waive", "requeue", "check"):
        o = bt_sub.add_parser(op)
        o.add_argument("--out", type=Path, default=None)
        if op in ("generate", "waive", "requeue", "check"):
            o.add_argument("--merged", type=lambda v: [Path(x) for x in csv(v)], required=True)
        if op != "generate" and op != "check":
            o.add_argument("--id", type=int, required=True)
    bg = bt_sub.choices["generate"]
    bg.add_argument("--max-artifacts", type=int, default=3)
    bg.add_argument("--max-findings", type=int, default=15)
    bg.add_argument("--exclude", type=csv, default=[])
    bt_sub.choices["set"].add_argument("--status", required=True)
    bw = bt_sub.choices["waive"]
    bw.add_argument("--artifact", required=True)
    bw.add_argument("--dimension", required=True)
    bw.add_argument("--file", required=True)
    bw.add_argument("--reason", required=True)
    bt_sub.choices["requeue"].add_argument("--artifact", required=True)
    rc = sub.add_parser("recovery", help="plan 14 content recovery: inventory, presence, grep, queue, record-check, check")
    rc_sub = rc.add_subparsers(dest="op", required=True)
    for op in ("inventory", "presence", "grep", "record-check"):
        rc_sub.add_parser(op).add_argument("--artifact", required=True)
    ri = rc_sub.choices["inventory"]
    ri.add_argument("--base", required=True)
    ri.add_argument("--kind", choices=sorted(ARTIFACT_KINDS), default=None)
    ri.add_argument("--fate-only", action="store_true")
    rp = rc_sub.choices["presence"]
    rp.add_argument("--runner", required=True)
    rp.add_argument("--timeout", type=float, default=300)
    rc_sub.choices["grep"].add_argument("--min-share", type=float, default=0.3)
    rc_sub.choices["record-check"].add_argument("--previous", action="append", default=[], metavar="REF")
    rq = rc_sub.add_parser("queue")
    rq.add_argument("--base", required=True)
    rq.add_argument("--out", type=Path, default=None)
    rq.add_argument("--max-artifacts", type=int, default=3)
    rq.add_argument("--append", default=None, metavar="NAME")
    rc_sub.add_parser("check").add_argument("--out", type=Path, default=None)
    ar = sub.add_parser("artifacts", help="list skills, commands and agents as JSON")
    ar.add_argument("--kind", choices=sorted(ARTIFACT_KINDS), default=None)
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
    jp = sub.add_parser("judge-prompt")
    jp.add_argument("--kind", default="skill")
    jp.add_argument("--artifact", type=Path, action="append", required=True)
    jp.add_argument("--judge", required=True)
    jp.add_argument("--previous", action="append", default=[], metavar="SRC",
                    help="git ref or directory holding the previous version (repeatable)")
    jp.add_argument("--recovery-gate", metavar="QUEUE", default=None,
                    help="batches queue: defer the default digest until the artifact's batch closes")
    jp.add_argument("--digest-dir", type=Path, default=None, help="write each artifact's digest to DIR/<name>.md")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = (args.root or default_root()).resolve()
    if args.cmd == "detect":
        try:
            try:
                state = json.loads(args.state) if args.state.strip() else None
            except (ValueError, RecursionError):
                state = None
            upstream_rows = load_json(args.upstreams)
            if not isinstance(upstream_rows, list):
                raise ValueError("upstreams must be a JSON list")
            result = detect(state, args.spec_changed == "true", upstream_rows, args.force, root)
        except (OSError, ValueError, TypeError) as e:
            print(f"detect: {e}", file=sys.stderr)
            return 1
        print(json.dumps(result))
        return 0
    if args.cmd == "interval-due":
        try:
            days = interval_days(args.days)
            now = datetime.datetime.now(datetime.timezone.utc) if args.now is None else parse_stamp(args.now)
            if now is None:
                raise ValueError(f"--now must be YYYY-MM-DDTHH:MM:SSZ, got {args.now!r}")
            try:
                state = json.loads(args.state)
            except (ValueError, RecursionError):
                state = None
        except ValueError as e:
            print(f"interval-due: {e}", file=sys.stderr)
            return 1
        print("true" if interval_due(state, now, days, args.event) else "false")
        return 0
    if args.cmd == "validate-knobs":
        errors = validate_knobs(dict(os.environ))
        for error in errors:
            print(f"validate-knobs: {error}", file=sys.stderr)
        return 1 if errors else 0
    if args.cmd == "branch-name":
        try:
            print(branch_name(args.type, args.title, args.date, args.suffix))
        except ValueError as e:
            print(f"branch-name: {e}", file=sys.stderr)
            return 1
        return 0
    if args.cmd == "validate-decision":
        try:
            decision = load_json(args.file)
        except ValueError as e:
            print(e, file=sys.stderr)
            return 1
        errors = validate_decision(decision, args.spec_changed, args.structure_changed, root)
        for error in errors:
            print(error, file=sys.stderr)
        return 1 if errors else 0
    if args.cmd == "upstreams":
        return upstreams(root, args.registry)
    if args.cmd == "track":
        registry = args.registry or root / "docs" / "audit" / "upstream-sources.json"
        code, row = track(root, registry, args.artifact, args.status, args.source, args.artifact_kind,
                          args.sha, args.model, args.new_path, args.today)
        if row is not None:
            print(json.dumps(row, indent=2))
        return code
    if args.cmd == "check":
        if args.kind == "skill" and args.allowlist and not args.allowlist.is_file():
            print(f"allowlist not found: {args.allowlist}", file=sys.stderr)
            return 1
        try:
            res = check_skills(root, args.skills, args.strict, set(args.ignore), args.allowlist,
                               args.validator_pin, args.kind)
        except ValueError as e:
            print(e, file=sys.stderr)
            return 1
        print(json.dumps(res, indent=2))
        bad = any(not s["ok"] for s in res["skills"] if not s["synced"])
        return 1 if args.strict and bad else 0
    if args.cmd == "batches":
        try:
            return batches_op(root, args)
        except (OSError, ValueError, KeyError, TypeError, HarnessError) as e:
            print(f"batches {args.op}: {e}", file=sys.stderr)
            return 2
    if args.cmd == "recovery":
        try:
            return recovery_op(root, args)
        except (OSError, ValueError, KeyError, TypeError, HarnessError) as e:
            print(f"recovery {args.op}: {e}", file=sys.stderr)
            return 2
    if args.cmd == "artifacts":
        try:
            found = list_artifacts(root)
        except ValueError as e:
            print(f"artifacts: {e}", file=sys.stderr)
            return 2
        print(json.dumps([a for a in found if args.kind in (None, a["kind"])], indent=2))
        return 0
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
    if args.cmd == "judge-prompt":
        try:
            sys.stdout.write(render_judge_prompt(root, args.kind, args.artifact, args.judge, args.previous,
                                                 args.recovery_gate, args.digest_dir))
        except (OSError, ValueError) as e:
            print(f"judge-prompt: {e}", file=sys.stderr)
            return 2
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
