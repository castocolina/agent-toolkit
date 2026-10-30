#!/usr/bin/env python3
"""Deterministic path-scope gate for scheduled-audit model edits.

The audit workflows let model agents edit the checkout (the rubric repairs and
the apply-job fixer). This script re-checks the changed paths on the host. It
must run from a trusted copy outside the checkout (the workflows copy it to
$RUNNER_TEMP/trusted/ before the first model step), immediately after each model
step and before any repository code runs. Modes:

  fixer    the apply job's fixer output, checked with `git status
           --porcelain=v2`: only `skills/<target>/**`, `tests/skills/<target>/**`
           (targets from decision.json) and `docs/audit/**` may change. With
           `--final-stage` (the check runs after `scripts/build_plugins.py`),
           the regenerated `dist/**` is allowed too.
  decision the merge job's model output: only the root `decision.json` may
           appear (the caller stages the pre-model workspace first, so
           `--skip-staged` leaves only the model's own changes).
  repairs  the rubric repairs patches, checked from `git apply --numstat` (and
           with `--patch` straight from the patch text): only the Task 2a
           structural scope — `skills/agentskills-research/**`,
           `skills/skill-judge/references/**`, `skills/skill-judge/evals/**`,
           `tests/skills/agentskills-research/**` and `docs/audit/**` — may
           change; `dist/**` requires `--final-stage`.

  review   the PR review gate (`.github/workflows/skill-audit-review.yaml`), run
           from the trusted copy over `git diff` of the PR range: stdin is
           `git diff --numstat -z -M` (NUL-separated records, rename pairs
           included) and `--patch` is the same range's `git diff --binary -M`,
           so symlinks and mode changes are seen. Allowed: `skills/**`,
           `tests/skills/**`, `docs/audit/**`, `dist/**` and
           `.claude-plugin/marketplace.json`; everything else is out of scope.

In every mode, always rejected: the synced skills `skills/gepetto/**` and
`skills/datadog-cli/**` (maintained by their own sync workflows, never by the
audit), `.github/**`, `scripts/**`, `docs/plans/**`, `README.md`, path
traversal (`..` segments), absolute paths and control characters.

Mode transitions are refused independently of the path allowance, so an
in-scope path still fails when it: creates, converts or changes a symlink; sets
the executable bit (new executable file, or an executable-bit change).

Input: a path list on stdin, one path per line, in `--format paths` (default),
`numstat` (git apply --numstat output, including rename arrows and C-style
quoting), `numstat-z` (git diff --numstat -z, NUL-separated, unquoted, with the
rename brace form) or `porcelain-v2` (git status --porcelain=v2, whose mode fields expose
symlinks and mode changes; untracked `?` entries are lstat'ed under
`--worktree`). `--patch FILE` additionally parses a git patch directly for the
same properties. The patch parser is strict: an unrecognized header line fails
closed, quoted (C-style) header paths are decoded, and hunk bodies are counted
so that a body line that looks like a header is never misread. Offending paths
are printed on stderr; the exit code is 1 if anything is out of scope, 0
otherwise.
"""
import argparse
import json
import os
import re
import stat
import sys
from pathlib import Path

SYMLINK_MODE = "120000"
EXEC_MODE = "100755"
NULL_MODE = "000000"  # git's mode for an absent side (new or deleted path)
SYMLINK_REASON = "symlink (creation, conversion or change)"

# Never editable by the audit, in any mode, even when a target names them.
DENY_PREFIXES = ("skills/gepetto", "skills/datadog-cli", ".github", "scripts", "docs/plans")
DENY_EXACT = ("README.md",)

# Written by scripts/build_plugins.py and staged with dist/ before committing.
FINAL_STAGE_FILE = ".claude-plugin/marketplace.json"
DECISION_FILE = "decision.json"

# review mode: the whole PR allowance, each entry a directory (a path must sit inside it).
REVIEW_PREFIXES = ("skills", "tests/skills", "docs/audit", "dist")

REPAIRS_PREFIXES = (
    "skills/agentskills-research",
    "skills/skill-judge/references",
    "skills/skill-judge/evals",
    "tests/skills/agentskills-research",
    "docs/audit",
)

NUMSTAT_COUNT = re.compile(r"\d+|-")
HUNK_HEADER = re.compile(r"^@@ -\d+(?:,(\d+))? \+\d+(?:,(\d+))? @@")
BINARY_LINE = re.compile(r"^(?:literal|delta) \d+$")
BASE85_LINE = re.compile(r"^[0-9A-Za-z!#$%&()*+;<=>?@^_`{|}~-]+$")
SIMPLE_ESCAPES = {"a": 7, "b": 8, "f": 12, "n": 10, "r": 13, "t": 9, "v": 11, '"': 34, "\\": 92}


class ScopeError(Exception):
    """Bad input (decision, format, patch or quoting): fail closed."""


class Entry:
    """One changed path plus the mode problem (if any) visible for it."""

    __slots__ = ("path", "reason", "staged_only")

    def __init__(self, path, reason=None, staged_only=False):
        self.path = path
        # Why the path's mode transition is refused, or None when it is allowed.
        self.reason = reason
        # True for porcelain-v2 entries whose worktree matches the index (Y == '.').
        self.staged_only = staged_only


def c_unquote_token(text: str, start: int) -> tuple[str, int]:
    """Decode the C-quoted token starting at text[start] (a '"').

    Returns the decoded path and the index just past the closing quote. Git
    writes non-ASCII bytes as octal escapes of their UTF-8 encoding, so the
    escapes are collected as bytes and decoded as UTF-8.
    """
    if text[start:start + 1] != '"':
        raise ScopeError(f"expected a quoted path at: {text[start:]!r}")
    out = bytearray()
    i = start + 1
    while i < len(text):
        ch = text[i]
        if ch == '"':
            try:
                return out.decode("utf-8"), i + 1
            except UnicodeDecodeError as exc:
                raise ScopeError(f"quoted path is not UTF-8: {text[start:i + 1]!r}") from exc
        if ch == "\\":
            nxt = text[i + 1:i + 2]
            if nxt in SIMPLE_ESCAPES:
                out.append(SIMPLE_ESCAPES[nxt])
                i += 2
                continue
            digits = text[i + 1:i + 4]
            if len(digits) == 3 and all(d in "01234567" for d in digits) and int(digits, 8) < 256:
                out.append(int(digits, 8))
                i += 4
                continue
            raise ScopeError(f"unknown escape in quoted path: {text[i:i + 4]!r}")
        out.extend(ch.encode("utf-8"))
        i += 1
    raise ScopeError(f"unterminated quoted path: {text[start:]!r}")


def unquote(path: str) -> str:
    """Undo git's C-style path quoting (core.quotePath) for a whole field."""
    if not path.startswith('"'):
        return path
    value, end = c_unquote_token(path, 0)
    if end != len(path):
        raise ScopeError(f"text after a quoted path: {path!r}")
    return value


def validate_path(path: str) -> list[str]:
    """Structural problems that make a path unrecognizable or hostile."""
    p = path[2:] if path.startswith("./") else path
    p = p.rstrip("/")
    if not p:
        return ["empty path"]
    if p.startswith("/") or re.match(r"^[A-Za-z]:", p):
        return ["absolute path"]
    segments = p.split("/")
    if ".." in segments:
        return ["path traversal"]
    if any(segment in ("", ".") for segment in segments):
        return ["malformed path"]
    if "\x00" in p or any(ord(ch) < 32 and ch != "\t" for ch in p):
        return ["control characters"]
    return []


def mode_reason(old, new):
    """Why a path may not change from git mode `old` to `new` (None: allowed).

    None stands for an absent side. A deletion carries no new mode and is
    judged by its path alone.
    """
    if new is None:
        return None
    if SYMLINK_MODE in (old, new):
        return SYMLINK_REASON
    if old is None:
        return "executable bit set on a new file" if new == EXEC_MODE else None
    if old != new and EXEC_MODE in (old, new):
        return "executable bit change (mode change)"
    if old != new:
        return "mode change"
    return None


def git_mode(text: str):
    return None if text == NULL_MODE else text


def porcelain_reason(fields: list[str]):
    old, index, worktree = (git_mode(m) for m in fields[3:6])
    return mode_reason(old, index) or mode_reason(index, worktree)


def untracked_reason(worktree: Path, path: str):
    """Mode problem of an untracked file, read with lstat (never followed)."""
    try:
        st = os.lstat(worktree / path)
    except FileNotFoundError:
        return None
    except (OSError, ValueError):
        return "cannot inspect untracked path"
    if stat.S_ISLNK(st.st_mode):
        return mode_reason(None, SYMLINK_MODE)
    if stat.S_ISREG(st.st_mode) and st.st_mode & 0o111:
        return mode_reason(None, EXEC_MODE)
    return None


def prefix_match(path: str, base: str) -> bool:
    return path == base or path.startswith(base + "/")


def load_targets(decision_path: Path) -> list[str]:
    try:
        data = json.loads(decision_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ScopeError(f"cannot read decision {decision_path}: {exc}") from exc
    targets = data.get("targets") if isinstance(data, dict) else None
    if (not isinstance(targets, list) or not targets
            or any(not isinstance(t, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", t)
                   for t in targets)):
        raise ScopeError("decision targets must be a non-empty list of skill directory names")
    return targets


def allowed(path: str, mode: str, targets: list[str], final_stage: bool) -> bool:
    if mode == "decision":
        return path == DECISION_FILE
    if mode == "review":
        return path == FINAL_STAGE_FILE or any(path.startswith(p + "/") for p in REVIEW_PREFIXES)
    if final_stage and path == FINAL_STAGE_FILE:
        return True
    prefixes: list[str] = []
    if mode == "fixer":
        for target in targets:
            prefixes += [f"skills/{target}", f"tests/skills/{target}"]
        prefixes.append("docs/audit")
    else:
        prefixes = list(REPAIRS_PREFIXES)
    if final_stage:
        prefixes.append("dist")
    return any(prefix_match(path, prefix) for prefix in prefixes)


def parse_paths(text: str) -> list[Entry]:
    return [Entry(line.strip()) for line in text.splitlines() if line.strip()]


def parse_numstat(text: str) -> list[Entry]:
    entries = []
    for line in text.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t", 2)
        if len(parts) != 3:
            raise ScopeError(f"numstat line is not <added>\\t<deleted>\\t<path>: {line!r}")
        rest = unquote(parts[2])
        pair = rename_pair(rest)
        if pair is not None:
            entries += [Entry(pair[0]), Entry(pair[1])]
        else:
            entries.append(Entry(rest))
    return entries


def rename_pair(rest: str):
    """(old, new) for a numstat rename 'pre{old => new}post' or 'old => new'; None otherwise."""
    if " => " not in rest:
        return None
    if "{" in rest and "}" in rest:
        prefix, _, tail = rest.partition("{")
        brace, _, suffix = tail.rpartition("}")
        old_part, _, new_part = brace.partition(" => ")
        return prefix + old_part + suffix, prefix + new_part + suffix
    old_path, _, new_path = rest.partition(" => ")
    return old_path, new_path


def parse_numstat_z(text: str) -> list[Entry]:
    """git diff --numstat -z: '<added>\t<deleted>\t<path>\0' per entry.

    A rename or copy is '<added>\t<deleted>\t\0<old>\0<new>\0' (empty path, then
    both names as their own fields). Paths are raw in -z mode, so they are not
    unquoted. Each path is checked literally and also as a brace or arrow rename
    form (the union only adds checks, never removes one).
    """
    tokens = text.split("\0")
    if tokens and tokens[-1] == "":
        tokens.pop()  # the terminator after the last record
    entries = []
    i = 0
    while i < len(tokens):
        head = tokens[i]
        i += 1
        parts = head.split("\t", 2)
        if len(parts) != 3 or not NUMSTAT_COUNT.fullmatch(parts[0]) or not NUMSTAT_COUNT.fullmatch(parts[1]):
            raise ScopeError(f"numstat -z record is not <added>\\t<deleted>\\t<path>: {head!r}")
        path = parts[2]
        if path == "":
            if i + 2 > len(tokens) or not tokens[i] or not tokens[i + 1]:
                raise ScopeError("truncated or empty rename record in numstat -z input")
            names = [tokens[i], tokens[i + 1]]
            i += 2
        else:
            names = [path]
            pair = rename_pair(path)
            if pair is not None:
                names += list(pair)
        entries += [Entry(name) for name in names]
    return entries


def parse_porcelain_v2(text: str, worktree: Path) -> list[Entry]:
    entries = []
    for line in text.splitlines():
        if not line.strip():
            continue
        kind, _, rest = line.partition(" ")
        if kind == "1":
            fields = line.split(" ", 8)
            if len(fields) != 9:
                raise ScopeError(f"malformed porcelain-v2 record: {line!r}")
            entries.append(Entry(unquote(fields[8]), porcelain_reason(fields),
                                 staged_only=fields[1][1:] == "."))
        elif kind == "2":
            fields = line.split(" ", 9)
            if len(fields) != 10 or "\t" not in fields[9]:
                raise ScopeError(f"malformed porcelain-v2 rename record: {line!r}")
            new_path, _, orig_path = fields[9].partition("\t")
            staged_only = fields[1][1:] == "."
            entries += [Entry(unquote(new_path), porcelain_reason(fields), staged_only=staged_only),
                        Entry(unquote(orig_path), staged_only=staged_only)]
        elif kind == "?":
            path = unquote(rest)
            entries.append(Entry(path, untracked_reason(worktree, path)))
        else:
            # Includes 'u' (unmerged): a fresh checkout cannot produce one, so an
            # unknown record is refused rather than skipped.
            raise ScopeError(f"unrecognized porcelain-v2 record: {line!r}")
    return entries


def decode_side(raw: str) -> str:
    """One side of a diff header: a C-quoted token or a bare name."""
    if not raw.startswith('"'):
        return raw
    value, end = c_unquote_token(raw, 0)
    if end != len(raw):
        raise ScopeError(f"text after a quoted path: {raw!r}")
    return value


def diff_git_paths(line: str) -> list[str]:
    """Both paths named by a 'diff --git a/P b/P' header.

    Git quotes a side only when it needs quoting, so a space inside an unquoted
    name is ambiguous. Every split that yields a valid 'a/' and 'b/' pair is
    kept. The real paths are always among them, so an ambiguous header can only
    add paths to the check, never hide one.
    """
    rest = line[len("diff --git "):]
    if rest.startswith('"'):
        _, end = c_unquote_token(rest, 0)
        candidates = [(rest[:end], rest[end + 1:])] if rest[end:end + 1] == " " else []
    else:
        candidates = [(rest[:i], rest[i + 1:]) for i, ch in enumerate(rest) if ch == " "]
    paths = []
    for a_raw, b_raw in candidates:
        a, b = decode_side(a_raw), decode_side(b_raw)
        if a.startswith("a/") and b.startswith("b/") and len(a) > 2 and len(b) > 2:
            paths += [a[2:], b[2:]]
    if not paths:
        raise ScopeError(f"unrecognized diff header (expected a/ and b/ paths): {line!r}")
    return paths


def header_path(value: str):
    """Path from a '--- a/P' or '+++ b/P' line; None for /dev/null."""
    if value.endswith("\t"):
        # git appends a tab to names that contain a space, quoted or not; a literal
        # tab inside a quoted name is escaped as \t, so a raw trailing tab is git's.
        value = value[:-1]
    path = unquote(value)
    if path == "/dev/null":
        return None
    if path.startswith(("a/", "b/")) and len(path) > 2:
        return path[2:]
    raise ScopeError(f"unrecognized file header path: {value!r}")


def parse_patch(text: str) -> list[Entry]:
    entries: dict[str, Entry] = {}

    def add(path: str, reason=None) -> None:
        entry = entries.get(path)
        if entry is None:
            entries[path] = Entry(path, reason)
        elif reason and not entry.reason:
            entry.reason = reason

    def add_current(reason) -> None:
        for path in current:
            add(path, reason)

    current: list[str] = []
    pending_old = None
    state = "header"  # header | hunk | binary
    old_left = new_left = 0
    # git ends every line with "\n" only; splitlines() would also split on
    # "\r" inside file content and throw the hunk line count out of step.
    for line in text.split("\n"):
        if state == "binary":
            if not line.startswith("diff --git "):
                if line == "" or BINARY_LINE.match(line) or BASE85_LINE.match(line):
                    continue
                raise ScopeError(f"unrecognized line in a binary patch: {line!r}")
            state = "header"
        if state == "hunk":
            if line.startswith("\\"):
                continue  # "\ No newline at end of file"
            if old_left or new_left:
                if line.startswith(" "):
                    old_left -= 1
                    new_left -= 1
                elif line.startswith("-"):
                    old_left -= 1
                elif line.startswith("+"):
                    new_left -= 1
                else:
                    raise ScopeError(f"malformed hunk line: {line!r}")
                if old_left < 0 or new_left < 0:
                    raise ScopeError(f"hunk body longer than its header: {line!r}")
                continue
            state = "header"
        if line.startswith("diff --git "):
            current = diff_git_paths(line)
            for path in current:
                add(path)
            pending_old = None
        elif line.startswith("@@"):
            if not current:
                raise ScopeError(f"hunk outside a diff --git section: {line!r}")
            match = HUNK_HEADER.match(line)
            if match is None:
                raise ScopeError(f"malformed hunk header: {line!r}")
            old_left = int(match.group(1)) if match.group(1) is not None else 1
            new_left = int(match.group(2)) if match.group(2) is not None else 1
            state = "hunk"
        elif line.startswith(("--- ", "+++ ")):
            if not current:
                raise ScopeError(f"file header outside a diff --git section: {line!r}")
            path = header_path(line[4:])
            if path is not None:
                add(path)
        elif line.startswith("index "):
            parts = line.split()
            if len(parts) == 3 and parts[2] == SYMLINK_MODE:
                add_current(SYMLINK_REASON)  # an unchanged symlink still has its content edited
        elif line.startswith("new file mode "):
            add_current(mode_reason(None, line.split()[-1]))
        elif line.startswith("deleted file mode "):
            pass
        elif line.startswith("old mode "):
            pending_old = line.split()[-1]
        elif line.startswith("new mode "):
            add_current(mode_reason(pending_old, line.split()[-1]))
            pending_old = None
        elif line.startswith(("rename from ", "rename to ", "copy from ", "copy to ")):
            add(unquote(line.split(" ", 2)[2]))
        elif line.startswith(("similarity index ", "dissimilarity index ")):
            pass
        elif line.startswith("Binary files ") and line.endswith(" differ"):
            pass
        elif line == "GIT binary patch":
            state = "binary"
        elif line.strip() == "":
            pass
        else:
            raise ScopeError(f"unrecognized patch header line: {line!r}")
    return list(entries.values())


def check(mode: str, entries: list[Entry], targets: list[str], final_stage: bool) -> list[str]:
    # The same path may arrive from both the patch text and a numstat list;
    # keep the first mode problem seen for it so it is never downgraded.
    merged: dict[str, Entry] = {}
    for entry in entries:
        existing = merged.get(entry.path)
        if existing is None:
            merged[entry.path] = Entry(entry.path, entry.reason)
        elif entry.reason and not existing.reason:
            existing.reason = entry.reason
    violations: dict[str, str] = {}
    for entry in merged.values():
        structural = validate_path(entry.path)
        if structural:
            violations[entry.path] = structural[0]
            continue
        if any(prefix_match(entry.path, prefix) for prefix in DENY_PREFIXES) \
                or entry.path in DENY_EXACT:
            violations[entry.path] = "path is never editable by the audit"
            continue
        # Mode transitions are refused whatever the path allowance says.
        if entry.reason:
            violations[entry.path] = entry.reason
            continue
        if not allowed(entry.path, mode, targets, final_stage):
            violations[entry.path] = "out of scope"
    return [f"{path}: {reason}" for path, reason in sorted(violations.items())]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("mode", choices=("fixer", "repairs", "decision", "review"))
    parser.add_argument("--decision", type=Path,
                        help="decision.json whose targets define the fixer scope")
    parser.add_argument("--final-stage", action="store_true",
                        help="allow dist/** (the check runs after scripts/build_plugins.py)")
    parser.add_argument("--format", choices=("paths", "numstat", "numstat-z", "porcelain-v2"), default="paths",
                        help="shape of the stdin path list")
    parser.add_argument("--patch", type=Path,
                        help="also parse a git patch for paths, symlinks and mode changes")
    parser.add_argument("--worktree", type=Path, default=Path.cwd(),
                        help="root used to lstat untracked porcelain entries")
    parser.add_argument("--skip-staged", action="store_true",
                        help="porcelain-v2 only: ignore entries whose worktree matches the index "
                             "(already-validated, staged repairs); check only the fixer's edits")
    args = parser.parse_args(argv)
    if args.mode == "fixer" and args.decision is None:
        parser.error("fixer mode requires --decision")
    if args.mode == "review":
        if args.format != "numstat-z":
            parser.error("review mode reads --format numstat-z")
        if args.patch is None:
            parser.error("review mode requires --patch (symlink and mode checks)")
    try:
        targets = load_targets(args.decision) if args.mode == "fixer" else []
        entries: list[Entry] = []
        if args.patch is not None:
            try:
                entries += parse_patch(args.patch.read_text(encoding="utf-8"))
            except (OSError, UnicodeDecodeError) as exc:
                raise ScopeError(f"cannot read patch {args.patch}: {exc}") from exc
        # Always read stdin: callers pipe the path list (possibly empty).
        text = sys.stdin.read()
        if args.format == "numstat":
            entries += parse_numstat(text)
        elif args.format == "numstat-z":
            entries += parse_numstat_z(text)
        elif args.format == "porcelain-v2":
            entries += parse_porcelain_v2(text, args.worktree)
        else:
            entries += parse_paths(text)
        if args.skip_staged:
            if args.format != "porcelain-v2":
                raise ScopeError("--skip-staged needs --format porcelain-v2")
            entries = [entry for entry in entries if not entry.staged_only]
        violations = check(args.mode, entries, targets, args.final_stage)
    except (ScopeError, UnicodeDecodeError) as exc:
        print(f"scope-check: {exc}", file=sys.stderr)
        return 1
    if violations:
        print(f"scope-check: {len(violations)} change(s) outside the {args.mode} scope:", file=sys.stderr)
        for violation in violations:
            print(f"  {violation}", file=sys.stderr)
        return 1
    print(f"scope-check: {len(entries)} path(s) within the {args.mode} scope", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
