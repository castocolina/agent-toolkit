#!/usr/bin/env python3
"""Build upstream-report evidence and the audit-upstream issue from detect's snapshot.

Consumes the upstreams.json rows that detect already produced (shipped in the
spec artifact), joined with the committed registry for each row's ref. The
`evidence` subcommand writes one evidence file per stale row into the excluded
workspace evidence directory: display dates, kind, source, ref, diff link and,
where cheap, the fetched change text (last 20 commits or revisions). Fetch
failures become "evidence unavailable: <reason>" and never abort the run.
`--keys` restricts the fetch to exactly those `skill|source` keys (used by
detect on an approval dispatch to fetch change evidence for the approved rows,
pinned to the registry ref, before upstream-report ever runs); a key that is
missing from the snapshot or not stale is rejected. The `issue` subcommand
renders the audit-upstream issue table from the same rows plus the Copilot
recommendations, escaping "|" in every cell.

Set AUDIT_UPSTREAM_FETCH to an executable path to override fetching: it reads a
row as JSON on stdin and prints the change text on stdout; a nonzero exit turns
stderr into the "evidence unavailable" reason. Tests use this instead of the
network. Set AUDIT_UPSTREAM_WIKI_FETCH to override only the Wikipedia transport
(it receives the API URL as argv[1] and prints the raw response body); without
it the default transport uses urllib.
"""
import argparse
import hashlib
import http.client
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

LIMIT_DEFAULT = 20


class EvidenceUnavailable(Exception):
    """The change text for a stale row could not be fetched."""


def key_of(row: dict) -> str:
    return f"{row.get('skill') or ''}|{row.get('source')}"


def escape_cell(value) -> str:
    """Make a value safe inside a Markdown table cell."""
    return str(value).replace("|", "\\|").replace("\n", " ")


def enc(value) -> str:
    """Fully percent-encode one URL component (refs embed slashes too)."""
    return urllib.parse.quote(str(value), safe="")


def enc_path(value: str) -> str:
    """Encode each path component while keeping the '/' separators structural."""
    return "/".join(urllib.parse.quote(part, safe="") for part in str(value).split("/"))


def diff_link(row: dict, ref) -> str | None:
    """Link each source kind by registry ref and source, never by timestamps.

    repo: compare/<merge-base>...<ref> when the producer recorded a merge base,
    otherwise commits/<ref>; github: commits/<ref>; github-path:
    commits/<ref>/<path>; wikipedia: the page history; unversioned: no link.
    Refs and every path component are percent-encoded; only the '/' separators
    stay structural.
    """
    kind = row.get("kind")
    source = enc_path(row.get("source") or "")
    if kind == "repo":
        base = row.get("merge_base")
        if base:
            return f"https://github.com/{source}/compare/{enc(base)}...{enc(ref)}"
        if ref:
            return f"https://github.com/{source}/commits/{enc(ref)}"
        return None
    if kind == "github":
        return f"https://github.com/{source}/commits/{enc(ref)}" if ref else None
    if kind == "github-path":
        repo, _, path = str(row.get("source") or "").partition(":")
        path = row.get("new_path") or path
        if not (ref and path):
            return None
        return f"https://github.com/{enc_path(repo)}/commits/{enc(ref)}/{enc_path(path)}"
    if kind == "wikipedia":
        return ("https://en.wikipedia.org/w/index.php?title="
                + enc(row.get("source") or "") + "&action=history")
    return None


def fetch_github_commits(row: dict, ref, limit: int) -> str:
    source = str(row["source"])
    if row["kind"] == "github-path":
        repo, _, path = source.partition(":")
        path = row.get("new_path") or path
        query = (f"repos/{repo}/commits?path={urllib.parse.quote(path, safe='')}"
                 f"&sha={urllib.parse.quote(str(ref), safe='')}&per_page={limit}")
    else:
        query = f"repos/{source}/commits?sha={urllib.parse.quote(str(ref), safe='')}&per_page={limit}"
    try:
        proc = subprocess.run(["gh", "api", query], stdin=subprocess.DEVNULL, capture_output=True,
                              text=True, timeout=30)
    except (OSError, subprocess.SubprocessError) as exc:
        raise EvidenceUnavailable(str(exc)) from exc
    if proc.returncode:
        raise EvidenceUnavailable(proc.stderr.strip() or f"gh api exited {proc.returncode}")
    try:
        commits = json.loads(proc.stdout)
        lines = [f"{(c.get('sha') or '')[:12]} {c['commit']['committer']['date']} "
                 f"{(c['commit'].get('message') or '').splitlines()[0]}"
                 for c in commits]
    except (ValueError, KeyError, TypeError, IndexError) as exc:
        raise EvidenceUnavailable(f"malformed commit list: {exc}") from exc
    if not lines:
        raise EvidenceUnavailable("commit list is empty")
    return "\n".join(lines)


def fetch_wikipedia_revisions(row: dict, limit: int, transport: str | None = None) -> str:
    query = ("https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles="
             + urllib.parse.quote(str(row["source"]), safe="")
             + f"&rvlimit={limit}&rvprop=timestamp%7Ccomment%7Cuser&format=json")
    if transport:
        try:
            proc = subprocess.run([transport, query], stdin=subprocess.DEVNULL, capture_output=True,
                                  text=True, timeout=60)
        except (OSError, subprocess.SubprocessError) as exc:
            raise EvidenceUnavailable(str(exc)) from exc
        if proc.returncode:
            raise EvidenceUnavailable(proc.stderr.strip() or f"wikipedia transport exited {proc.returncode}")
        raw = proc.stdout
    else:
        request = urllib.request.Request(query, headers={"User-Agent": "agent-toolkit-upstream-audit/1.0"})
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                raw = response.read().decode("utf-8")
        except (http.client.HTTPException, OSError, ValueError) as exc:
            # OSError covers URLError and socket timeouts; HTTPException covers
            # truncated responses such as IncompleteRead.
            raise EvidenceUnavailable(str(exc)) from exc
    try:
        data = json.loads(raw)
    except ValueError as exc:
        raise EvidenceUnavailable(f"malformed Wikipedia payload: {exc}") from exc
    try:
        pages = data["query"]["pages"]
        page = next(iter(pages.values()))
        revisions = page["revisions"]
        if not revisions or not isinstance(revisions[0], dict):
            raise TypeError("revision list is empty or not a list of objects")
        return "\n".join(
            f"{rev.get('timestamp', '')} {rev.get('user', '')} {rev.get('comment', '')}".strip()
            for rev in revisions)
    except (AttributeError, KeyError, TypeError, IndexError, StopIteration) as exc:
        raise EvidenceUnavailable(f"malformed Wikipedia revisions: {exc}") from exc


def fetch_changes(row: dict, ref, limit: int, override: str | None,
                  wiki_transport: str | None = None) -> str:
    if override:
        try:
            proc = subprocess.run([override], input=json.dumps(row), capture_output=True,
                                  text=True, timeout=60)
        except (OSError, subprocess.SubprocessError) as exc:
            raise EvidenceUnavailable(str(exc)) from exc
        if proc.returncode:
            raise EvidenceUnavailable(proc.stderr.strip() or f"override fetcher exited {proc.returncode}")
        if not proc.stdout.strip():
            raise EvidenceUnavailable("override fetcher produced no change text")
        return proc.stdout.strip()
    if row.get("kind") in ("github", "github-path", "repo"):
        return fetch_github_commits(row, ref, limit)
    if row.get("kind") == "wikipedia":
        return fetch_wikipedia_revisions(row, limit, wiki_transport)
    raise EvidenceUnavailable(f"no fetch for kind {row.get('kind')}")


def evidence_filename(key: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", key).strip("-") or "row"
    digest = hashlib.sha1(key.encode("utf-8")).hexdigest()[:8]
    return f"{slug}-{digest}.txt"


def write_evidence(rows: list[dict], refs: dict, evidence_dir: Path, override: str | None,
                   limit: int, wiki_transport: str | None = None,
                   keys: list[str] | None = None) -> list[str]:
    if keys is not None:
        rows = select_rows(rows, keys)
    evidence_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for row in rows:
        if row.get("stale") is not True:
            continue
        key = key_of(row)
        ref = refs.get(key)
        link = diff_link(row, ref)
        lines = [
            f"Stale upstream key: {key}",
            f"Kind: {row.get('kind')}",
            f"Source: {row.get('source')}",
            f"Ref: {ref if ref is not None else 'n/a'}",
            f"Our last update: {row.get('ours_updated') or 'unknown'}",
            f"Source last update: {row.get('source_updated') or 'unknown'}",
            f"Diff link: {link or 'n/a'}",
            "",
        ]
        try:
            lines.append(fetch_changes(row, ref, limit, override, wiki_transport))
        except EvidenceUnavailable as exc:
            lines.append(f"evidence unavailable: {exc}")
        dest = evidence_dir / evidence_filename(key)
        dest.write_text("\n".join(lines) + "\n", encoding="utf-8")
        written.append(dest.name)
    return written


def select_rows(rows: list[dict], keys: list[str]) -> list[dict]:
    """Pick exactly the requested keys; unknown or non-stale keys fail closed."""
    by_key: dict[str, dict] = {}
    for row in rows:
        if row.get("stale") is True:
            by_key.setdefault(key_of(row), row)
    missing = [key for key in keys if key not in by_key]
    if missing:
        raise ValueError(f"requested upstream keys are missing or not stale: {missing}")
    return [by_key[key] for key in dict.fromkeys(keys)]


def validate_recommendations(recommendations: dict, stale_keys: set[str]) -> None:
    if set(recommendations) != stale_keys:
        missing = sorted(stale_keys - set(recommendations))
        extra = sorted(set(recommendations) - stale_keys)
        raise ValueError(f"recommendations do not cover the stale rows exactly; missing={missing} extra={extra}")
    for key, rec in recommendations.items():
        if (not isinstance(rec, dict) or set(rec) != {"key", "recommendation", "reason"}
                or rec.get("recommendation") not in ("update", "ignore")
                or not isinstance(rec.get("reason"), str) or not rec["reason"].strip()):
            raise ValueError(f"invalid recommendation for {key}")


def render_issue(rows: list[dict], refs: dict, recommendations: dict) -> str:
    lines = [
        "| Key | Kind | Source | Our last update | Source last update | Diff | Recommendation | Reason |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        if row.get("stale") is not True:
            continue
        key = key_of(row)
        rec = recommendations[key]
        link = diff_link(row, refs.get(key))
        cells = (
            key,
            row.get("kind"),
            row.get("source"),
            row.get("ours_updated") or "unknown",
            row.get("source_updated") or "unknown",
            f"[diff]({link})" if link else "n/a",
            rec["recommendation"],
            rec["reason"],
        )
        lines.append("| " + " | ".join(escape_cell(cell) for cell in cells) + " |")
    lines += ["", "To apply approved updates dispatch skill-audit.yaml with approved_upstreams=<keys>;"
                  " ignored sources stay listed until the source or our skill changes"]
    return "\n".join(lines) + "\n"


def load_rows(path: Path, what: str) -> list[dict]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ValueError(f"cannot read {what} {path}: {exc}") from exc
    if not isinstance(data, list) or any(not isinstance(row, dict) for row in data):
        raise ValueError(f"{what} must be a JSON list of objects")
    if what == "upstreams snapshot":
        for row in data:
            if not row.get("source") or not row.get("kind"):
                raise ValueError(f"upstreams snapshot row is missing source or kind: {row}")
    return data


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    evidence = sub.add_parser("evidence", help="write one evidence file per stale row")
    evidence.add_argument("--upstreams", type=Path, required=True)
    evidence.add_argument("--registry", type=Path, required=True)
    evidence.add_argument("--evidence-dir", type=Path, required=True)
    evidence.add_argument("--limit", type=int, default=LIMIT_DEFAULT)
    evidence.add_argument("--keys", default="",
                          help="comma-separated skill|source keys to fetch "
                               "(approval dispatch); default: every stale row")
    issue = sub.add_parser("issue", help="render the audit-upstream issue table")
    issue.add_argument("--upstreams", type=Path, required=True)
    issue.add_argument("--registry", type=Path, required=True)
    issue.add_argument("--recommendations", type=Path, required=True)
    issue.add_argument("--issue-file", type=Path, required=True)
    args = parser.parse_args(argv)
    override = os.environ.get("AUDIT_UPSTREAM_FETCH") or None
    wiki_transport = os.environ.get("AUDIT_UPSTREAM_WIKI_FETCH") or None
    try:
        rows = load_rows(args.upstreams, "upstreams snapshot")
        refs = {f"{e.get('skill') or ''}|{e.get('source')}": e.get("ref")
                for e in load_rows(args.registry, "registry")}
        if args.cmd == "evidence":
            keys = [k.strip() for k in args.keys.split(",") if k.strip()] or None
            written = write_evidence(rows, refs, args.evidence_dir, override, args.limit,
                                     wiki_transport, keys=keys)
            print(json.dumps(written))
        else:
            try:
                rec_list = json.loads(args.recommendations.read_text(encoding="utf-8"))
            except (OSError, ValueError) as exc:
                raise ValueError(f"cannot read recommendations {args.recommendations}: {exc}") from exc
            if not isinstance(rec_list, list) or any(not isinstance(r, dict) for r in rec_list):
                raise ValueError("recommendations must be a JSON list of objects")
            recommendations = {r["key"]: r for r in rec_list}
            stale_keys = {key_of(row) for row in rows if row.get("stale") is True}
            validate_recommendations(recommendations, stale_keys)
            args.issue_file.write_text(render_issue(rows, refs, recommendations), encoding="utf-8")
    except ValueError as exc:
        print(f"upstream-evidence: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
