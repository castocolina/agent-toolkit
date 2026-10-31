"""Offline unit tests for upstream-evidence.py: fetch containment and diff links."""

import http.client
import importlib.util
import json
import os
import stat
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[2] / ".github" / "audit" / "upstream-evidence.py"
_spec = importlib.util.spec_from_file_location("upstream_evidence", SCRIPT)
ue = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ue)

WIKI_ROW = {
    "skill": "humanizer", "source": "Wikipedia:Signs of AI writing", "kind": "wikipedia",
    "source_updated": "2026-01-05T00:00:00Z", "ours_updated": "2026-01-01T00:00:00Z",
    "stale": True, "error": None, "merge_base": None,
}
GITHUB_ROW = {
    "skill": "x", "source": "o/r", "kind": "github",
    "source_updated": "2026-01-05T00:00:00Z", "ours_updated": "2026-01-01T00:00:00Z",
    "stale": True, "error": None, "merge_base": None,
}


class FakeResponse:
    """Minimal urlopen result: a context manager with a canned read()."""

    def __init__(self, body: bytes):
        self.body = body

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def read(self):
        return self.body


class DiffLinkTests(unittest.TestCase):
    """Refs and every path component are percent-encoded; '/' stays structural."""

    def test_github_ref_is_fully_encoded(self):
        link = ue.diff_link({"kind": "github", "source": "o/r4"}, "feat/x#1")
        self.assertEqual(link, "https://github.com/o/r4/commits/feat%2Fx%231")

    def test_github_path_components_are_encoded(self):
        link = ue.diff_link({"kind": "github-path", "source": "o/r3:folder/a file-é.md"}, "feat/x#1")
        self.assertEqual(
            link, "https://github.com/o/r3/commits/feat%2Fx%231/folder/a%20file-%C3%A9.md")

    def test_new_path_replaces_the_path_in_the_diff_link(self):
        # Break: a moved source still links the stored path, so the review opens the old tree.
        row = {"kind": "github-path", "source": "joshuadavidthomas/agent-skills:old-dir",
               "new_path": "skills/old dir"}
        link = ue.diff_link(row, "main")
        self.assertTrue(link.endswith("/skills/old%20dir"), link)
        self.assertNotIn("old-dir", link)
        stored = ue.diff_link({"kind": "github-path", "source": "o/r:folder/a.md"}, "main")
        self.assertTrue(stored.endswith("/folder/a.md"), stored)

    def test_repo_compare_ref_is_encoded(self):
        link = ue.diff_link({"kind": "repo", "source": "o/r", "merge_base": "abc123"}, "feat/x#1")
        self.assertEqual(link, "https://github.com/o/r/compare/abc123...feat%2Fx%231")

    def test_repo_commit_ref_is_encoded(self):
        link = ue.diff_link({"kind": "repo", "source": "o/r2", "merge_base": None}, "feat/x#1")
        self.assertEqual(link, "https://github.com/o/r2/commits/feat%2Fx%231")


class NewPathFetchTests(unittest.TestCase):
    """A stub gh on PATH records the query; new_path replaces the path split off source."""

    def fetch(self, row):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        bindir = Path(tmp.name)
        argv_path = bindir / "argv.txt"
        stub = bindir / "gh"
        stub.write_text(
            "#!/bin/sh\nprintf '%s\\n' \"$@\" > \"" + str(argv_path) + "\"\n"
            "printf '%s\\n' '[{\"sha\":\"0123456789abcdef\",\"commit\":{\"committer\":{\"date\":\"2026-01-04T00:00:00Z\"},\"message\":\"m\"}}]'\n",
            encoding="utf-8")
        stub.chmod(stub.stat().st_mode | stat.S_IEXEC)
        env = {**os.environ, "PATH": str(bindir) + os.pathsep + os.environ.get("PATH", "")}
        with mock.patch.dict(os.environ, env, clear=True):
            text = ue.fetch_github_commits(row, "main", 1)
        return text, argv_path.read_text(encoding="utf-8")

    def test_query_uses_new_path_when_present_and_source_path_otherwise(self):
        # Break: the commits query keeps the stored path after the source moved.
        row = {"kind": "github-path", "source": "joshuadavidthomas/agent-skills:old-dir",
               "new_path": "skills/old-dir/SKILL.md"}
        _, argv = self.fetch(row)
        self.assertIn("path=skills%2Fold-dir%2FSKILL.md", argv)
        self.assertNotIn("path=old-dir", argv)
        _, argv = self.fetch({"kind": "github-path", "source": "o/r:folder/a.md"})
        self.assertIn("path=folder%2Fa.md", argv)


class WikipediaFetchTests(unittest.TestCase):
    """Best-effort fetching: every native failure becomes EvidenceUnavailable."""

    def fetch(self, payload: bytes, urlopen_side_effect=None):
        row = dict(WIKI_ROW)
        if urlopen_side_effect is not None:
            patcher = mock.patch.object(ue.urllib.request, "urlopen",
                                        side_effect=urlopen_side_effect)
        else:
            patcher = mock.patch.object(ue.urllib.request, "urlopen",
                                        return_value=FakeResponse(payload))
        with patcher:
            return ue.fetch_wikipedia_revisions(row, 20)

    def test_renders_revisions(self):
        body = json.dumps({"query": {"pages": {"1": {"revisions": [
            {"timestamp": "2026-01-06T00:00:00Z", "user": "Editor", "comment": "copyedit"}]}}}})
        self.assertEqual(self.fetch(body.encode()), "2026-01-06T00:00:00Z Editor copyedit")

    def test_child_processes_never_inherit_the_callers_stdin(self):
        # A transport stub that reads stdin would block on the caller's open pipe until the
        # timeout; the helper must hand its children a closed stdin.
        revisions = {"query": {"pages": {"1": {"revisions": [
            {"timestamp": "2026-01-06T00:00:00Z", "user": "Editor", "comment": "copyedit"}]}}}}
        commits = [{"sha": "0123456789abcdef", "commit": {
            "committer": {"date": "2026-01-04T12:00:00Z"}, "message": "Fix typo"}}]
        outputs = [json.dumps(revisions), json.dumps(commits)]
        procs = [mock.Mock(returncode=0, stdout=out, stderr="") for out in outputs]
        with mock.patch.object(ue.subprocess, "run", side_effect=procs) as run:
            ue.fetch_wikipedia_revisions(dict(WIKI_ROW), 20, transport="/bin/true")
            ue.fetch_github_commits(dict(GITHUB_ROW), "main", 20)
        self.assertEqual(run.call_count, 2)
        for call in run.call_args_list:
            self.assertIs(call.kwargs.get("stdin"), ue.subprocess.DEVNULL, call)

    def test_incomplete_read_is_contained(self):
        with self.assertRaises(ue.EvidenceUnavailable) as ctx:
            self.fetch(None, urlopen_side_effect=http.client.IncompleteRead(b"partial", 65536))
        self.assertIn("IncompleteRead", str(ctx.exception))

    def test_url_error_is_contained(self):
        with self.assertRaises(ue.EvidenceUnavailable) as ctx:
            self.fetch(None, urlopen_side_effect=urllib.error.URLError("connection refused"))
        self.assertIn("connection refused", str(ctx.exception))

    def test_timeout_is_contained(self):
        with self.assertRaises(ue.EvidenceUnavailable) as ctx:
            self.fetch(None, urlopen_side_effect=TimeoutError("timed out"))
        self.assertIn("timed out", str(ctx.exception))

    def test_json_decode_error_is_contained(self):
        with self.assertRaises(ue.EvidenceUnavailable) as ctx:
            self.fetch(b'{"query": {"pages": ')
        self.assertIn("malformed Wikipedia payload", str(ctx.exception))

    def test_missing_query_key_is_contained(self):
        with self.assertRaises(ue.EvidenceUnavailable) as ctx:
            self.fetch(json.dumps({"batchcomplete": ""}).encode())
        self.assertIn("malformed Wikipedia revisions", str(ctx.exception))

    def test_query_string_shape_is_contained(self):
        # {"query": "x"} raises AttributeError while walking the shape.
        with self.assertRaises(ue.EvidenceUnavailable) as ctx:
            self.fetch(json.dumps({"query": "not-an-object"}).encode())
        self.assertIn("malformed Wikipedia revisions", str(ctx.exception))

    def test_revision_list_of_non_objects_is_contained(self):
        body = json.dumps({"query": {"pages": {"1": {"revisions": ["oops"]}}}})
        with self.assertRaises(ue.EvidenceUnavailable) as ctx:
            self.fetch(body.encode())
        self.assertIn("malformed Wikipedia revisions", str(ctx.exception))

    def test_empty_revision_list_is_contained(self):
        body = json.dumps({"query": {"pages": {"1": {"revisions": []}}}})
        with self.assertRaises(ue.EvidenceUnavailable):
            self.fetch(body.encode())


class ContainmentTests(unittest.TestCase):
    """A broken Wikipedia fetch must not abort the remaining stale rows."""

    def test_later_rows_are_processed(self):
        commits = json.dumps([{"sha": "0123456789abcdef",
                               "commit": {"committer": {"date": "2026-01-04T12:00:00Z"},
                                          "message": "Fix typo"}}])
        fake_proc = mock.Mock(returncode=0, stdout=commits, stderr="")
        rows = [WIKI_ROW, GITHUB_ROW]
        refs = {f"{r.get('skill') or ''}|{r.get('source')}": "main" for r in rows}
        with tempfile.TemporaryDirectory() as tmp:
            evidence = Path(tmp) / "evidence"
            with mock.patch.object(ue.urllib.request, "urlopen",
                                   side_effect=urllib.error.URLError("connection refused")), \
                 mock.patch.object(ue.subprocess, "run", return_value=fake_proc):
                written = ue.write_evidence(rows, refs, evidence, None, 20)
            self.assertEqual(len(written), 2)
            wiki_text = (evidence / written[0]).read_text(encoding="utf-8")
            self.assertIn("evidence unavailable", wiki_text)
            self.assertIn("connection refused", wiki_text)
            github_text = (evidence / written[1]).read_text(encoding="utf-8")
            self.assertIn("0123456789ab 2026-01-04T12:00:00Z Fix typo", github_text)


class ApprovedKeysTests(unittest.TestCase):
    """--keys pins detect's approval-dispatch evidence to the approved rows."""

    def evidence(self, rows, keys=None):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        base = Path(tmp.name)
        rows_path = base / "upstreams.json"
        registry_path = base / "registry.json"
        rows_path.write_text(json.dumps(rows), encoding="utf-8")
        registry_path.write_text(json.dumps([
            {"skill": "x", "source": "o/r", "ref": "main"},
            {"skill": "humanizer", "source": "Wikipedia:Signs of AI writing", "ref": None},
        ]), encoding="utf-8")
        evidence_dir = base / "approved-evidence"
        commits = json.dumps([{"sha": "0123456789abcdef",
                               "commit": {"committer": {"date": "2026-01-04T12:00:00Z"},
                                          "message": "Fix typo"}}])
        fake_proc = mock.Mock(returncode=0, stdout=commits, stderr="")
        argv = ["evidence", "--upstreams", str(rows_path), "--registry", str(registry_path),
                "--evidence-dir", str(evidence_dir)]
        if keys is not None:
            argv += ["--keys", keys]
        # Offline: the Wikipedia row must fail inside the evidence path, not reach the network.
        with mock.patch.object(ue.subprocess, "run", return_value=fake_proc), \
             mock.patch.object(ue.urllib.request, "urlopen",
                               side_effect=urllib.error.URLError("offline")):
            code = ue.main(argv)
        return code, evidence_dir

    def test_writes_evidence_only_for_approved_keys(self):
        code, evidence_dir = self.evidence([WIKI_ROW, GITHUB_ROW], keys="x|o/r")
        self.assertEqual(code, 0)
        written = sorted(path.name for path in evidence_dir.iterdir())
        self.assertEqual(len(written), 1)
        self.assertIn("0123456789ab 2026-01-04T12:00:00Z Fix typo",
                      (evidence_dir / written[0]).read_text(encoding="utf-8"))

    def test_without_keys_all_stale_rows_are_written(self):
        code, evidence_dir = self.evidence([WIKI_ROW, GITHUB_ROW])
        self.assertEqual(code, 0)
        self.assertEqual(len(list(evidence_dir.iterdir())), 2)

    def test_unknown_approved_key_is_rejected(self):
        code, evidence_dir = self.evidence([GITHUB_ROW], keys="nope|missing")
        self.assertEqual((code, evidence_dir.exists()), (1, False))

    def test_unstale_approved_key_is_rejected(self):
        code, evidence_dir = self.evidence([dict(GITHUB_ROW, stale=False)], keys="x|o/r")
        self.assertEqual((code, evidence_dir.exists()), (1, False))

    def test_failed_fetch_still_writes_evidence(self):
        # Never abort: a fetch failure becomes an 'evidence unavailable' file.
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        base = Path(tmp.name)
        rows_path = base / "upstreams.json"
        registry_path = base / "registry.json"
        rows_path.write_text(json.dumps([GITHUB_ROW]), encoding="utf-8")
        registry_path.write_text(json.dumps([{"skill": "x", "source": "o/r", "ref": "main"}]),
                                 encoding="utf-8")
        evidence_dir = base / "approved-evidence"
        fake_proc = mock.Mock(returncode=1, stdout="", stderr="gh: rate limited")
        with mock.patch.object(ue.subprocess, "run", return_value=fake_proc):
            code = ue.main(["evidence", "--upstreams", str(rows_path), "--registry", str(registry_path),
                            "--evidence-dir", str(evidence_dir), "--keys", "x|o/r"])
        self.assertEqual(code, 0)
        written = list(evidence_dir.iterdir())
        self.assertEqual(len(written), 1)
        text = written[0].read_text(encoding="utf-8")
        self.assertIn("evidence unavailable", text)
        self.assertIn("rate limited", text)


if __name__ == "__main__":
    unittest.main()
