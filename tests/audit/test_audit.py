import contextlib
import io
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "audit"))
import audit  # noqa: E402

SHA = "a" * 40
RUBRIC = "rubric_version: 1\nspec_sha: {sha}\n\n| id | name | max | source |\n|----|------|-----|--------|\n{rows}\n"
ROWS = "\n".join(f"| D{i} | n | {m} | s |" for i, m in enumerate([20, 15, 15, 15, 15, 15, 15, 15], 1))
C5 = "Validation failed for /t/s:\n  - Unexpected fields in frontmatter: {f}. Only ['allowed-tools', 'compatibility', 'description', 'license', 'metadata', 'name'] are allowed.\n"


class Base(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name) / "root"
        refs = self.root / "skills" / "skill-judge" / "references"
        (refs / "agentskills").mkdir(parents=True)
        (refs / "agentskills" / "SOURCE.json").write_text(json.dumps({"sha": SHA}))
        (refs / "rubric.md").write_text(RUBRIC.format(sha=SHA, rows=ROWS))
        (self.root / "scripts" / "audit").mkdir(parents=True)
        (self.root / "scripts" / "audit" / "non_latin_allowlist.txt").write_text("")

    def write(self, rel, text="", mode="w"):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(text, bytes):
            p.write_bytes(text)
        else:
            p.write_text(text, encoding="utf-8")
        return p

    def skill(self, name="x", body_lines=3, desc="d", fm_name=None, readme=True, evals=True):
        fm = f"---\nname: {fm_name or name}\ndescription: {desc}\n---\n"
        self.write(f"skills/{name}/SKILL.md", fm + "\n".join("l" for _ in range(body_lines - 4)) + "\n")
        if readme:
            self.write(f"skills/{name}/README.md", "r\n")
        if evals:
            self.write(f"skills/{name}/evals/evals.json", "{}")
            self.write(f"skills/{name}/evals/trigger-queries.json", "[]")

    def check(self, *extra, stub=(0, ""), skills="x"):
        argv = ["--root", str(self.root), "check", *extra]
        if skills:
            argv += ["--skills", skills]
        out = io.StringIO()
        with mock.patch("audit.run_skills_ref", return_value=stub), contextlib.redirect_stdout(out):
            code = audit.main(argv)
        return code, json.loads(out.getvalue())["skills"]

    def codes(self, *extra, **kw):
        _, skills = self.check(*extra, **kw)
        return [i["code"] for i in skills[0]["issues"]]


class UpstreamsTests(Base):
    def setup_registry(self, entries):
        path = self.write("registry.json", json.dumps(entries))
        return path

    def run_upstreams(self, entries, **stubs):
        path = self.setup_registry(entries)
        out, err = io.StringIO(), io.StringIO()
        with mock.patch("audit.fetch_source_updated", side_effect=stubs.get("fetch", ["2025-01-02T00:00:00Z"] * len(entries))), \
             mock.patch("audit.ours_updated", side_effect=stubs.get("ours", ["2025-01-01T00:00:00Z"] * len(entries))), \
             contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = audit.main(["--root", str(self.root), "upstreams", "--registry", str(path)])
        return code, json.loads(out.getvalue()), err.getvalue()

    def test_upstreams_stale_when_source_newer(self):
        self.skill("x")
        entry = {"skill":"x", "kind":"github", "source":"o/r", "ref":"main"}
        code, rows, _ = self.run_upstreams([entry])
        self.assertEqual((code, rows[0]["stale"]), (0, True))

    def test_staleness_compares_instants_across_offsets_and_equal_instants(self):
        self.skill("x")
        entry = {"skill": "x", "kind": "github", "source": "o/r", "ref": "main"}
        for upstream, ours, stale in (
            ("2025-01-01T12:00:00Z", "2025-01-01T13:00:00+02:00", True),
            ("2025-01-01T12:00:00+00:00", "2025-01-01T14:00:00+02:00", False),
        ):
            with self.subTest(upstream=upstream, ours=ours):
                code, rows, _ = self.run_upstreams([entry], fetch=[upstream], ours=[ours])
                self.assertEqual((code, rows[0]["stale"]), (0, stale))

    def test_upstreams_unversioned_never_stale(self):
        self.skill("x")
        e = {"skill":"x", "kind":"unversioned", "source":"citation", "ref":None}
        code, rows, _ = self.run_upstreams([e])
        self.assertEqual((code, rows[0]["stale"], rows[0]["source_updated"]), (0, False, None))

    def test_upstreams_repo_kind_uses_merge_base(self):
        self.skill("x")
        e = {"skill":None, "kind":"repo", "source":"o/r", "ref":"main"}
        with mock.patch("audit.fetch_source_updated", return_value="2025-01-02T00:00:00Z"), \
             mock.patch("audit.ours_updated", return_value="2025-01-01T00:00:00Z"):
            code, rows, _ = self.run_upstreams([e])
        self.assertEqual((code, rows[0]["stale"]), (0, True))

    def test_upstreams_repo_kind_uses_shared_ancestor_committer_date(self):
        self.skill("x")
        self._git_init(self.root)
        self._commit(self.root, "base.txt", "common\n", "2025-01-01T00:00:00+00:00")
        upstream = Path(self._tmp.name) / "upstream.git"
        subprocess.run(["git", "clone", "--bare", str(self.root), str(upstream)], check=True, capture_output=True)
        seed = Path(self._tmp.name) / "seed"
        subprocess.run(["git", "clone", str(upstream), str(seed)], check=True, capture_output=True)
        self._git_config(seed)
        self._commit(self.root, "local.txt", "local later\n", "2025-01-03T00:00:00+00:00")
        self._commit(seed, "upstream.txt", "upstream later\n", "2025-01-02T00:00:00+00:00")
        subprocess.run(["git", "push", "origin", "HEAD:main"], cwd=seed, check=True, capture_output=True)
        subprocess.run(["git", "symbolic-ref", "HEAD", "refs/heads/main"], cwd=upstream, check=True)
        entry = {"skill": None, "kind": "repo", "source": "o/r", "ref": "main"}
        before_refs = subprocess.run(["git", "show-ref"], cwd=self.root, capture_output=True, text=True).stdout
        with mock.patch("audit.upstream_repo_url", return_value=str(upstream)):
            self.assertEqual(audit.ours_updated(self.root, entry), "2025-01-01T00:00:00Z")
        refs = subprocess.run(["git", "show-ref"], cwd=self.root, capture_output=True, text=True).stdout
        self.assertEqual(refs, before_refs)

    def _git_config(self, path):
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=path, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=path, check=True)

    def _git_init(self, path):
        subprocess.run(["git", "init", "-q"], cwd=path, check=True)
        self._git_config(path)

    def _commit(self, path, rel, content, timestamp):
        target = path / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
        subprocess.run(["git", "add", rel], cwd=path, check=True)
        env = {**os.environ, "GIT_AUTHOR_DATE": timestamp, "GIT_COMMITTER_DATE": timestamp}
        subprocess.run(["git", "commit", "-m", "fixture"], cwd=path, env=env, check=True, capture_output=True)

    def test_upstreams_invalid_timestamp_errors_and_unversioned_needs_history(self):
        self.skill("x")
        entry = {"skill": "x", "kind": "github", "source": "o/r", "ref": "main"}
        code, rows, _ = self.run_upstreams([entry], fetch=["not-a-date"])
        self.assertEqual((code, rows[0]["stale"]), (1, None))
        unversioned = {"skill": "x", "kind": "unversioned", "source": "citation", "ref": None}
        empty = self.root / "empty"
        subprocess.run(["git", "init", "-q", str(empty)], check=True)
        path = self.setup_registry([unversioned])
        out = io.StringIO()
        with mock.patch("audit.ours_updated", return_value=None), contextlib.redirect_stdout(out):
            code = audit.main(["--root", str(self.root), "upstreams", "--registry", str(path)])
        self.assertEqual((code, json.loads(out.getvalue())[0]["stale"]), (1, None))

    def test_upstreams_repo_unrelated_history_uses_oldest_root_commit(self):
        self.skill("x")
        self._git_init(self.root)
        self._commit(self.root, "skills/x/SKILL.md", "first\n", "2025-01-01T00:00:00+00:00")
        self._commit(self.root, "later.txt", "later\n", "2025-01-03T00:00:00+00:00")
        branch = subprocess.run(["git", "branch", "--show-current"], cwd=self.root,
                                check=True, capture_output=True, text=True).stdout.strip()
        subprocess.run(["git", "checkout", "--orphan", "older-root"], cwd=self.root,
                       check=True, capture_output=True)
        self._commit(self.root, "older-root.txt", "old root\n", "2024-12-31T00:00:00+00:00")
        subprocess.run(["git", "checkout", branch], cwd=self.root, check=True, capture_output=True)
        subprocess.run(["git", "merge", "--allow-unrelated-histories", "--no-commit", "older-root"],
                       cwd=self.root, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "join roots"], cwd=self.root, check=True, capture_output=True)
        upstream = Path(self._tmp.name) / "unrelated.git"
        subprocess.run(["git", "init", "--bare", str(upstream)], check=True, capture_output=True)
        seed = Path(self._tmp.name) / "unrelated-seed"
        subprocess.run(["git", "clone", str(upstream), str(seed)], check=True, capture_output=True)
        self._git_config(seed)
        self._commit(seed, "remote.txt", "remote\n", "2025-01-02T00:00:00+00:00")
        subprocess.run(["git", "push", "origin", "HEAD:main"], cwd=seed, check=True, capture_output=True)
        entry = {"skill": None, "kind": "repo", "source": "o/r", "ref": "main"}
        with mock.patch("audit.upstream_repo_url", return_value=str(upstream)):
            self.assertEqual(audit.ours_updated(self.root, entry), "2024-12-31T00:00:00Z")

    def test_upstreams_real_repo_fetch_failure_is_unavailable(self):
        self.skill("x")
        entry = {"skill": None, "kind": "repo", "source": "o/r", "ref": "main"}
        with mock.patch("audit.upstream_repo_url", return_value=str(Path(self._tmp.name) / "missing.git")):
            with self.assertRaises(audit.SourceUnavailable):
                audit.ours_updated(self.root, entry)

    def test_upstreams_fetch_failure_is_error_not_stale(self):
        self.skill("x")
        e = {"skill":"x", "kind":"github", "source":"o/r", "ref":"main"}
        code, rows, _ = self.run_upstreams([e], fetch= audit.SourceUnavailable("offline"))
        self.assertEqual((code, rows[0]["stale"]), (1, None))
        self.assertTrue(rows[0]["error"])

    def test_upstreams_evals_only_commit_does_not_reset_staleness(self):
        self.skill("x")
        def git(*args):
            return subprocess.run(["git", *args], cwd=self.root, check=True, capture_output=True, text=True).stdout.strip()
        git("init", "-q")
        git("config", "user.email", "test@example.com")
        git("config", "user.name", "Test")
        git("add", "skills/x/SKILL.md")
        env = {**os.environ, "GIT_AUTHOR_DATE": "2025-01-01T12:00:00+00:00", "GIT_COMMITTER_DATE": "2025-01-01T12:00:00+00:00"}
        subprocess.run(["git", "commit", "-qm", "skill"], cwd=self.root, env=env, check=True)
        initial = git("log", "-1", "--format=%cI", "--", "skills/x/SKILL.md")
        self.assertEqual(audit.ours_updated(self.root, {"kind":"github", "skill":"x"}), initial)
        self.write("skills/x/evals/evals.json", "later")
        git("add", "skills/x/evals/evals.json")
        env = {**os.environ, "GIT_AUTHOR_DATE": "2025-01-02T12:00:00+00:00", "GIT_COMMITTER_DATE": "2025-01-02T12:00:00+00:00"}
        subprocess.run(["git", "commit", "-qm", "evals only"], cwd=self.root, env=env, check=True)
        entry = {"skill":"x", "kind":"github", "source":"o/r", "ref":"main"}
        self.assertEqual(audit.ours_updated(self.root, entry), initial)

    def test_registry_failure_cases_are_independent_subtests(self):
        for text in (None, "not json", "{}"):
            with self.subTest(registry=text):
                path = self.root / "bad-registry.json"
                if text is None:
                    path.unlink(missing_ok=True)
                else:
                    path.write_text(text)
                err = io.StringIO()
                with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
                    code = audit.main(["--root", str(self.root), "upstreams", "--registry", str(path)])
                self.assertEqual(code, 2)
                self.assertIn("cannot read registry", err.getvalue())

    def test_upstreams_empty_local_history_is_error(self):
        self.skill("x")
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        entry = {"skill":"x", "kind":"github", "source":"o/r", "ref":"main"}
        path = self.setup_registry([entry])
        out, err = io.StringIO(), io.StringIO()
        with mock.patch("audit.fetch_source_updated", return_value="2025-01-02T00:00:00Z"), \
             contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = audit.main(["--root", str(self.root), "upstreams", "--registry", str(path)])
        rows = json.loads(out.getvalue())
        self.assertEqual((code, rows[0]["stale"]), (1, None))

    def test_fetch_source_updated_malformed_response_raises(self):
        entry = {"kind":"github", "source":"o/r", "ref":"main"}
        with mock.patch("audit.subprocess.run", return_value=mock.Mock(returncode=0, stdout="[]", stderr="")):
            with self.assertRaises(audit.SourceUnavailable):
                audit.fetch_source_updated(entry)

    def test_wikipedia_shapes_and_bad_kind_are_rejected(self):
        entry = {"skill": "x", "kind": "wikipedia", "source": "title", "ref": None}
        for payload in (
            {"query": {"pages": None}}, {"query": {"pages": []}},
            {"query": {"pages": {"1": {"revisions": None}}}},
            {"query": {"pages": {"1": {"revisions": {}}}}},
        ):
            with self.subTest(payload=payload), mock.patch("audit.urllib.request.urlopen") as urlopen:
                urlopen.return_value.__enter__.return_value.read.return_value = json.dumps(payload).encode()
                with self.assertRaises(audit.SourceUnavailable):
                    audit.fetch_source_updated(entry)
        for kind in ([], {}):
            with self.subTest(kind=kind):
                self.assertIsNotNone(audit.validate_entry(self.root, {"skill": "x", "kind": kind,
                                                                       "source": "citation", "ref": None}))

    def test_source_query_per_kind(self):
        for kind, source, ref, fragment in [
            ("github", "o/r", "main", "sha=main"), ("github-path", "o/r:a.md", "main", "path=a.md"),
            ("repo", "o/r", "main", "sha=main"), ("wikipedia", "Signs of AI writing", None, "Signs%20of%20AI%20writing"),
            ("unversioned", "citation", None, None)]:
            with self.subTest(kind=kind):
                q = audit.source_query({"kind":kind,"source":source,"ref":ref})
                if fragment is None:
                    self.assertIsNone(q)
                else:
                    self.assertIn(fragment, q)
                if kind == "github-path":
                    self.assertIn("path=a.md", q)
                    self.assertIn("sha=main", q)
        self.assertNotIn("path=", audit.source_query({"kind":"github","source":"o/r","ref":"main"}))
        self.assertNotIn("path=", audit.source_query({"kind":"repo","source":"o/r","ref":"main"}))

    def test_source_validation_accepts_github_component_and_path_characters(self):
        self.skill("x")
        base = {"skill": "x", "kind": "github", "source": "o/.github", "ref": "main"}
        self.assertIsNone(audit.validate_entry(self.root, base))
        self.assertIsNone(audit.validate_entry(self.root, {**base, "source": "o/_x"}))
        self.assertIsNone(audit.validate_entry(self.root, {
            **base, "kind": "github-path", "source": "o/r:folder/a file-é.md"
        }))
        self.assertIn("path=folder%2Fa%20file-%C3%A9.md", audit.source_query({
            "kind": "github-path", "source": "o/r:folder/a file-é.md", "ref": "main"
        }))
        self.assertIsNotNone(audit.validate_entry(self.root, {**base, "source": "o/.."}))

    def test_upstreams_invalid_entries_are_error_rows(self):
        self.skill("x")
        valid = {"skill":"x", "kind":"unversioned", "source":"citation", "ref":None}
        bads = [
            {"kind":"github","source":"o/r","ref":"main"},
            {**valid,"kind":"wat"}, {**valid,"skill":"missing"}, {**valid,"skill":"../x"},
            {**valid,"kind":"github","source":"bad","ref":"main"},
            {**valid,"kind":"github","source":"owner/../repo","ref":"main"},
            {**valid,"kind":"github-path","source":"o/r:path?x=1","ref":"main"},
            {**valid,"kind":"wikipedia","source":"line\nfeed","ref":None},
            {**valid,"kind":"wikipedia","source":"carriage\rreturn","ref":None},
            {**valid,"kind":"github-path","source":"o/r:a/../b","ref":"main"},
            {**valid,"kind":"repo","skill":"x","source":"o/r","ref":"main"},
            {**valid,"kind":"github","source":"o/r","ref":None},
            {**valid,"kind":"wikipedia","ref":"x"},
        ]
        valid = {"skill": "x", "kind": "github", "source": "o/r", "ref": "main"}
        for bad in bads:
            fetched = []
            def fetch_stub(entry):
                fetched.append(entry)
                return "2024-01-02T00:00:00Z"
            with self.subTest(bad=bad):
                code, rows, _ = self.run_upstreams([bad, valid], fetch=fetch_stub)
                self.assertEqual(fetched, [valid])
                self.assertEqual(code, 1)
                self.assertIsNone(rows[0]["stale"])
                self.assertTrue(rows[0]["error"].startswith("invalid entry"))
                self.assertFalse(rows[1]["stale"])

    def test_upstreams_unreadable_registry_exits_2(self):
        for text in (None, "nope", "{}"):
            path = self.root / "bad.json"
            if text is None: path.unlink(missing_ok=True)
            else: path.write_text(text)
            err = io.StringIO()
            with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
                code = audit.main(["--root", str(self.root), "upstreams", "--registry", str(path)])
            self.assertEqual(code, 2)


class CheckTests(Base):
    def test_check_flags_over_500_lines(self):
        self.skill(body_lines=499)
        self.assertNotIn("lines_over_500", self.codes())
        self.skill(body_lines=500)
        self.assertIn("lines_over_500", self.codes())

    def test_check_lines_over_500_ignores_nested_skill_md(self):
        self.skill(body_lines=10)
        self.write("skills/x/evals/files/big/SKILL.md", "l\n" * 600)
        self.assertNotIn("lines_over_500", self.codes())

    def test_check_flags_description_too_long(self):
        self.skill(desc="a" * 1025)
        self.assertIn("description_too_long", self.codes())
        self.skill(desc="a" * 1024)
        self.assertNotIn("description_too_long", self.codes())

    def test_frontmatter_block_scalars_and_empty_values(self):
        fm = audit.parse_frontmatter("---\nname: x\nmetadata:\n  a: b\ndescription: |\n  one\n  two\n---\n")
        self.assertEqual(fm["description"], "one\ntwo")
        self.assertEqual(fm["name"], "x")

    def test_frontmatter_deeply_nested_quoted_value_falls_back(self):
        with mock.patch.object(audit.json, "loads", side_effect=RecursionError):
            fm = audit.parse_frontmatter('---\ndescription: "x"\n---\n')
        self.assertEqual(fm["description"], "x")

    def test_check_deeply_nested_eval_file_is_an_issue_not_a_traceback(self):
        self.skill()
        self.write("skills/x/evals/evals.json", "[" * 200000)
        self.assertIn("missing_evals", self.codes())

    def test_check_flags_missing_readme(self):
        self.skill(readme=False)
        self.assertIn("missing_readme", self.codes())

    def test_check_name_mismatch(self):
        self.skill(fm_name="other")
        self.assertIn("name_mismatch", self.codes())

    def test_check_rejects_unknown_or_traversal_skill_name(self):
        self.skill()
        for name in ("nope", "../x", "/tmp/x", "a/b", "Foo"):
            with self.subTest(name=name):
                err = io.StringIO()
                with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
                    code = audit.main(["--root", str(self.root), "check", "--skills", name])
                self.assertEqual(code, 1)
                self.assertIn("invalid skill", err.getvalue())

    def test_check_flags_missing_evals(self):
        self.skill(evals=False)
        self.assertIn("missing_evals", self.codes())
        self.write("skills/x/evals/evals.json", "{not json")
        self.assertIn("missing_evals", self.codes())

    def evals_detail(self):
        _, skills = self.check()
        return [i["detail"] for i in skills[0]["issues"] if i["code"] == "missing_evals"]

    def test_check_missing_evals_requires_both_files(self):
        self.skill(evals=False)
        self.write("skills/x/evals/evals.json", "{}")
        d = self.evals_detail()
        self.assertEqual(len(d), 1)
        self.assertIn("trigger-queries.json", d[0])
        self.assertNotIn("evals/evals.json", d[0])
        (self.root / "skills/x/evals/evals.json").unlink()
        self.write("skills/x/evals/trigger-queries.json", "[]")
        d = self.evals_detail()
        self.assertEqual(len(d), 1)
        self.assertIn("evals/evals.json", d[0])
        self.write("skills/x/evals/evals.json", "{}")
        self.assertEqual(self.evals_detail(), [])

    def test_check_flags_missing_script_tests(self):
        self.skill()
        self.write("skills/x/scripts/run.sh", "#!/bin/bash\n")
        self.assertIn("missing_script_tests", self.codes())

    def test_check_script_tests_present_ok(self):
        self.skill()
        self.write("skills/x/scripts/run.sh", "#!/bin/bash\n")
        self.write("tests/skills/x/test-run.sh", "#!/bin/bash\n")
        self.assertNotIn("missing_script_tests", self.codes())
        self.write("skills/y/scripts/run.py", "")
        self.write("tests/skills/y/test_run.py", "")
        self.skill("y")
        self.assertNotIn("missing_script_tests", self.codes(skills="y"))

    def test_check_script_test_inside_skill_evals_does_not_count(self):
        self.skill()
        self.write("skills/x/scripts/run.sh", "#!/bin/bash\n")
        self.write("skills/x/evals/test-run.sh", "#!/bin/bash\n")
        detail = [i["detail"] for i in self.check()[1][0]["issues"] if i["code"] == "missing_script_tests"]
        self.assertEqual(detail, ["scripts/ has files but no tests/skills/x/test-*.sh or test_*.py"])

    def test_check_flags_non_latin(self):
        self.skill()
        self.write("skills/x/a.md", "hello\n中文\n")
        _, skills = self.check()
        hit = [i for i in skills[0]["issues"] if i["code"] == "non_latin"]
        self.assertEqual(len(hit), 1)
        self.assertIn("skills/x/a.md:2", hit[0]["detail"])

    def test_check_non_latin_skips_binary(self):
        self.skill()
        self.write("skills/x/b.bin", b"\xff\xfe\x00\xe3\x83")
        self.assertNotIn("non_latin", self.codes())

    def test_check_non_latin_skips_verbatim_references(self):
        self.skill()
        self.write("skills/x/references/agentskills/a.md", "ノ\n")
        self.assertNotIn("non_latin", self.codes())
        self.write("skills/x/references/b.md", "ノ\n")
        self.assertIn("non_latin", self.codes())

    def test_check_non_latin_ignores_fullwidth_and_compat_forms(self):
        self.skill()
        self.write("skills/x/f.md", "（╯°□°）╯︵ ┻━┻\n")
        self.assertNotIn("non_latin", self.codes())
        self.write("skills/x/f.md", "┬─┬ノ( º _ ºノ)\n")
        self.assertIn("non_latin", self.codes())

    def test_check_allowlist_suppresses(self):
        self.skill()
        self.write("skills/x/f.md", "a\nb\nノ\n")
        al = self.root / "scripts" / "audit" / "non_latin_allowlist.txt"
        al.write_text("# comment\nskills/x/f.md:3\nskills/x/gone.md:9\n")
        self.assertNotIn("non_latin", self.codes())
        al.write_text("skills/x/f.md:4\n")
        self.assertIn("non_latin", self.codes())

    def test_check_allowlist_flag(self):
        self.skill()
        self.write("skills/x/f.md", "ノ\n")
        other = self.write("other.txt", "skills/x/f.md:1\n")
        self.assertNotIn("non_latin", self.codes("--allowlist", str(other)))

    def test_check_ignores_c5_fields(self):
        self.skill()
        _, skills = self.check(stub=(1, C5.format(f="user-invocable")))
        self.assertTrue(skills[0]["ok"])
        self.assertEqual(skills[0]["issues"], [])

    def test_check_keeps_non_c5_unexpected_fields(self):
        self.skill()
        _, skills = self.check(stub=(1, C5.format(f="user-invocable, version")))
        issue = skills[0]["issues"][0]
        self.assertEqual(issue["code"], "skills_ref")
        self.assertIn("version", issue["detail"])

    def test_check_mixed_c5_and_other_error(self):
        self.skill()
        text = C5.format(f="user-invocable") + "  - Missing required field in frontmatter: name\n"
        _, skills = self.check(stub=(1, text))
        d = skills[0]["issues"][0]["detail"]
        self.assertEqual(d, "Missing required field in frontmatter: name")

    def test_check_unparseable_failure_is_issue(self):
        self.skill()
        _, skills = self.check(stub=(1, "boom\n"))
        self.assertEqual(skills[0]["issues"][0]["detail"], "boom")

    def test_check_joins_multiple_skills_ref_errors(self):
        self.skill()
        text = "Validation failed for /t/s:\n  - first problem\n  - second problem\n"
        _, skills = self.check(stub=(1, text))
        issues = [i for i in skills[0]["issues"] if i["code"] == "skills_ref"]
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]["detail"], "first problem; second problem")

    def test_check_non_latin_line_numbers_use_newline_only(self):
        self.skill()
        self.write("skills/x/f.md", "a\x0bb\x0cc\nノ\n")  # VT/FF are not line breaks
        _, skills = self.check()
        hit = [i for i in skills[0]["issues"] if i["code"] == "non_latin"]
        self.assertIn("skills/x/f.md:2", hit[0]["detail"])

    def test_check_missing_explicit_allowlist_exits_1(self):
        self.skill()
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            code = audit.main(["--root", str(self.root), "check", "--allowlist", str(self.root / "nope.txt")])
        self.assertEqual(code, 1)
        self.assertIn("nope.txt", err.getvalue())

    def test_check_missing_source_json_exits_1(self):
        self.skill()
        (self.root / "skills/skill-judge/references/agentskills/SOURCE.json").unlink()
        err = io.StringIO()
        with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
            code = audit.main(["--root", str(self.root), "check", "--skills", "x"])
        self.assertEqual(code, 1)
        self.assertIn("SOURCE.json", err.getvalue())

    def test_check_exit_zero_always_ok(self):
        self.skill()
        _, skills = self.check(stub=(0, "  - something\n"))
        self.assertEqual(skills[0]["issues"], [])

    def test_skills_ref_timeout_is_an_issue_not_a_crash(self):
        self.skill()
        bindir = Path(self._tmp.name) / "bin"
        bindir.mkdir()
        uvx = bindir / "uvx"
        uvx.write_text("#!/bin/bash\nexec sleep 5\n")
        uvx.chmod(0o755)
        with mock.patch.dict(os.environ, {"PATH": f"{bindir}:{os.environ['PATH']}"}), \
                mock.patch("audit.SKILLS_REF_TIMEOUT", 0.5):
            code, text = audit.run_skills_ref(self.root, self.root / "skills/x")
        self.assertNotEqual(code, 0)
        self.assertIn("timed out", text)
        self.assertEqual(audit.parse_skills_ref(code, text), [text])

    def test_check_strict_ignores_synced(self):
        self.skill("gepetto", fm_name="other")
        code, skills = self.check("--strict", skills="gepetto")
        self.assertTrue(skills[0]["synced"])
        self.assertEqual(code, 0)
        self.assertNotIn("missing_readme", [i["code"] for i in skills[0]["issues"]])
        self.skill("x", fm_name="other")
        code, _ = self.check("--strict")
        self.assertEqual(code, 1)

    def test_check_ignore_flag(self):
        self.skill(fm_name="other")
        code, skills = self.check("--strict", "--ignore", "name_mismatch")
        self.assertEqual(code, 0)
        self.assertTrue(skills[0]["ok"])
        self.assertEqual([(i["code"], i["ignored"]) for i in skills[0]["issues"]], [("name_mismatch", True)])


class RubricTests(Base):
    def run_rubric(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            code = audit.main(["--root", str(self.root), "rubric-check"])
        return code, err.getvalue()

    def test_rubric_check_ok(self):
        self.assertEqual(self.run_rubric(), (0, ""))
        r = audit.load_rubric(self.root / "skills/skill-judge/references/rubric.md")
        self.assertEqual(r["version"], 1)
        self.assertEqual(r["max"]["D1"], 20)

    def test_rubric_check_rejects_missing_dimension(self):
        rows = "\n".join(ROWS.splitlines()[:-1])
        (self.root / "skills/skill-judge/references/rubric.md").write_text(RUBRIC.format(sha=SHA, rows=rows))
        code, err = self.run_rubric()
        self.assertEqual(code, 1)
        self.assertIn("D8", err)

    def test_rubric_check_non_object_source_json_is_a_reason(self):
        (self.root / "skills/skill-judge/references/agentskills/SOURCE.json").write_text("[]")
        code, err = self.run_rubric()
        self.assertEqual(code, 1)
        self.assertIn("cannot read sha", err)

    def test_rubric_check_rejects_stale_spec_sha(self):
        (self.root / "skills/skill-judge/references/rubric.md").write_text(RUBRIC.format(sha="b" * 40, rows=ROWS))
        code, err = self.run_rubric()
        self.assertEqual(code, 1)
        self.assertIn("spec_sha", err)

    def test_rubric_check_rejects_duplicated_dimension_row(self):
        rows = ROWS + "\n| D3 | n | 15 | s |"
        (self.root / "skills/skill-judge/references/rubric.md").write_text(RUBRIC.format(sha=SHA, rows=rows))
        code, err = self.run_rubric()
        self.assertEqual(code, 1)
        self.assertIn("D3", err)


class NoJudgeSkillTests(Base):
    """The audit tooling ships before skills/skill-judge: every command ends cleanly without it."""

    RUBRIC_MSG = "audit.py: rubric not found: skills/skill-judge/references/rubric.md (pass --rubric)"

    def setUp(self):
        super().setUp()
        shutil.rmtree(self.root / "skills" / "skill-judge")
        self.skill("x")

    def run_cli(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = audit.main(["--root", str(self.root), *argv])
        self.assertNotIn("Traceback", err.getvalue())
        return code, out.getvalue(), err.getvalue()

    def test_rubric_check_names_the_missing_rubric(self):
        self.assertEqual(self.run_cli("rubric-check"), (1, "", self.RUBRIC_MSG + "\n"))

    def test_rubric_check_explicit_missing_rubric_omits_the_hint(self):
        missing = self.root / "nope.md"
        self.assertEqual(self.run_cli("rubric-check", "--rubric", str(missing)),
                         (1, "", f"audit.py: rubric not found: {missing}\n"))

    def test_validate_verdict_names_the_missing_rubric(self):
        path = self.write("in/j1/x.json", "{}")
        self.assertEqual(self.run_cli("validate-verdict", str(path)), (1, "", self.RUBRIC_MSG + "\n"))

    def test_merge_names_the_missing_rubric(self):
        argv = ["merge", "--in", str(self.root / "in"), "--out", str(self.root / "out"), "--judges", "j1"]
        self.assertEqual(self.run_cli(*argv), (1, "", self.RUBRIC_MSG + "\n"))

    def test_check_skips_the_skills_ref_pin_and_still_checks_skills(self):
        self.skill("y", readme=False)
        with mock.patch("audit.run_skills_ref", side_effect=AssertionError("must not run")):
            code, out, err = self.run_cli("check", "--strict")
        self.assertEqual(code, 1)  # y has no README
        self.assertEqual({s["name"]: [i["code"] for i in s["issues"]] for s in json.loads(out)["skills"]},
                         {"x": [], "y": ["missing_readme"]})
        self.assertEqual(err.count("\n"), 1)
        self.assertIn("skills-ref skipped", err)
        self.assertIn("skills/skill-judge/references/agentskills/SOURCE.json", err)

    def test_other_commands_do_not_need_the_judge_skill(self):
        self.assertEqual(self.run_cli("slug", "A B"), (0, "a-b\n", ""))
        self.assertEqual(self.run_cli("pi-cmd", "judge")[0], 0)
        code, _, err = self.run_cli("run-evals", "--skills", "x", "--runner", "true")
        self.assertEqual((code, "skill-judge" in err), (2, False))  # x has empty evals: a harness error, not a crash


class SlugTests(Base):
    def test_slug(self):
        self.assertEqual(audit.slug("router-env/my-referee-one"), "router-env-my-referee-one")
        self.assertEqual(audit.slug("opus"), "opus")
        self.assertEqual(audit.slug("GPT 5.2"), "gpt-5-2")

    def test_slug_empty_exits_1(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(audit.main(["slug", "///"]), 1)
        with contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(audit.main(["slug", "Opus"]), 0)
        self.assertEqual(out.getvalue().strip(), "opus")


class SplitTests(Base):
    def split(self, stdin):
        out = Path(self._tmp.name) / "out"
        err = io.StringIO()
        with mock.patch("sys.stdin", io.StringIO(stdin)), contextlib.redirect_stderr(err):
            code = audit.main(["split-verdicts", "--judge", "Router/Env One", "--out", str(out)])
        return code, out, err.getvalue()

    def test_split_verdicts_writes_per_skill_files(self):
        code, out, _ = self.split('{"skill":"a-b","score":1}\n{"skill":"c"}\n')
        self.assertEqual(code, 0)
        self.assertEqual(sorted(os.listdir(out / "router-env-one")), ["a-b.json", "c.json"])
        self.assertEqual(json.loads((out / "router-env-one" / "a-b.json").read_text())["score"], 1)

    def test_split_verdicts_skips_non_json(self):
        code, out, err = self.split('not json\n{"skill":"ok"}\n')
        self.assertEqual(code, 0)
        self.assertIn("not json", err)
        self.assertEqual(os.listdir(out / "router-env-one"), ["ok.json"])

    def test_split_verdicts_rejects_untrusted_skill(self):
        bad = ['{"skill":"/tmp/evil"}', '{"skill":"../escape"}', '{"skill":"a/b"}', "[1]", '"str"', '{"x":1}']
        before = sorted(os.listdir(self._tmp.name))
        code, out, err = self.split("\n".join(bad) + "\n")
        self.assertEqual(code, 0)
        self.assertFalse(out.exists())
        self.assertEqual(sorted(os.listdir(self._tmp.name)), before)
        for line in bad:
            self.assertIn(line, err)

    def test_split_verdicts_skips_too_deep_line(self):
        code, out, err = self.split("[" * 200000 + '\n{"skill":"ok"}\n')
        self.assertEqual(code, 0)
        self.assertIn("skipped", err)
        self.assertEqual(os.listdir(out / "router-env-one"), ["ok.json"])

    def test_split_verdicts_duplicate_skill_keeps_last_with_note(self):
        code, out, err = self.split('{"skill":"a","n":1}\n{"skill":"a","n":2}\n')
        self.assertEqual(code, 0)
        self.assertEqual(json.loads((out / "router-env-one" / "a.json").read_text())["n"], 2)
        self.assertIn("duplicate", err)


MAXES = [20, 15, 15, 15, 15, 15, 15, 15]
FINDING = {"id": "f1", "dimension": "D1", "severity": "high", "file": "SKILL.md", "line": 3, "evidence": "e", "fix": "Do it"}


def make_verdict(skill="x", judge="j1", total=100, findings=None, **over):
    """A valid verdict whose scores add up to `total` out of 125."""
    left, scores = total, {}
    for d, m in zip(audit.DIMENSIONS, MAXES):
        scores[d] = min(m, left)
        left -= scores[d]
    pct = round(total / 125 * 100, 1)
    grade = "A" if pct >= 90 else "B" if pct >= 80 else "C" if pct >= 70 else "D" if pct >= 60 else "F"
    v = {
        "skill": skill, "judge": judge, "rubric_version": 1, "spec_sha": SHA,
        "scores": scores, "max": dict(zip(audit.DIMENSIONS, MAXES)),
        "total": total, "max_total": 125, "percent": pct, "grade": grade,
        "findings": findings if findings is not None else [],
    }
    v.update(over)
    return v


class ValidateTests(Base):
    def validate(self, data, judge="j1", skill="x", raw=None):
        path = self.write(f"in/{judge}/{skill}.json", raw if raw is not None else json.dumps(data))
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            code = audit.main(["--root", str(self.root), "validate-verdict", str(path)])
        return code, err.getvalue()

    def rejects(self, data=None, expect="", **kw):
        code, err = self.validate(data, **kw)
        self.assertEqual(code, 1)
        self.assertIn(expect, err)

    def test_validate_accepts_valid(self):
        self.assertEqual(self.validate(make_verdict(findings=[FINDING])), (0, ""))
        self.assertEqual(self.validate(make_verdict(findings=[{**FINDING, "line": None}])), (0, ""))

    def test_validate_accepts_integral_percent(self):
        self.assertEqual(self.validate(make_verdict(total=100, percent=80)), (0, ""))
        self.rejects(make_verdict(total=100, percent=True), "percent")

    def test_validate_rejects_non_json(self):
        self.rejects(expect="x.json", raw="{nope")

    def test_validate_rejects_nan(self):
        self.rejects(expect="x.json: not valid JSON", raw=json.dumps(make_verdict()).replace('"percent": 80.0', '"percent": NaN'))

    def test_validate_rejects_infinity(self):
        self.rejects(expect="x.json: not valid JSON", raw=json.dumps(make_verdict()).replace('"percent": 80.0', '"percent": Infinity'))

    def test_validate_unhashable_finding_values_do_not_abort(self):
        paths = []
        for i, bad in enumerate(({"severity": ["x"]}, {"dimension": {}})):
            paths.append(str(self.write(f"in/j{i}/x.json", json.dumps(make_verdict(judge=f"j{i}", findings=[{**FINDING, **bad}])))))
        paths.append(str(self.write("in/j9/x.json", json.dumps(make_verdict(judge="j9", skill="y")))))  # path mismatch, reported last
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            code = audit.main(["--root", str(self.root), "validate-verdict", *paths])
        self.assertEqual(code, 1)
        lines = err.getvalue().splitlines()
        self.assertTrue(lines[0].startswith(paths[0] + ": findings[0]"))
        self.assertTrue(lines[1].startswith(paths[1] + ": findings[0]"))
        self.assertTrue(any(ln.startswith(paths[2] + ": ") for ln in lines))

    def test_validate_rejects_huge_percent(self):
        raw = json.dumps(make_verdict()).replace('"percent": 80.0', '"percent": 1' + "0" * 400)
        self.rejects(expect="percent", raw=raw)
        self.rejects(expect="percent", raw=raw.replace("1" + "0" * 400, "1e999"))

    def test_validate_rejects_missing_dimension(self):
        v = make_verdict()
        del v["scores"]["D8"]
        self.rejects(v, "scores")

    def test_validate_rejects_score_over_max(self):
        v = make_verdict()
        v["scores"]["D1"] = 21
        self.rejects(v, "D1")

    def test_validate_rejects_inflated_max(self):
        v = make_verdict()
        v["max"]["D1"] = 25
        self.rejects(v, "max")

    def test_validate_rejects_wrong_total(self):
        v = make_verdict(total=100)
        v["total"] = 99
        self.rejects(v, "total")

    def test_validate_rejects_wrong_percent_or_grade(self):
        self.rejects(make_verdict(percent=81.0), "percent")
        self.rejects(make_verdict(grade="A"), "grade")

    def test_validate_rejects_stale_rubric_version(self):
        self.rejects(make_verdict(rubric_version=2), "rubric_version")

    def test_validate_rejects_stale_spec_sha(self):
        self.rejects(make_verdict(spec_sha="b" * 40), "spec_sha")

    def test_validate_rejects_path_mismatch(self):
        self.rejects(make_verdict(skill="y"), "skill")
        self.rejects(make_verdict(judge="j2"), "judge")

    def test_validate_rejects_bad_finding_types(self):
        for bad in ({"line": "3"}, {"line": True}, {"line": 0}, {"fix": ""}, {"dimension": "D9"}, {"severity": "urgent"}):
            with self.subTest(bad=bad):
                self.rejects(make_verdict(findings=[{**FINDING, **bad}]), "findings")
        f = dict(FINDING)
        del f["evidence"]
        self.rejects(make_verdict(findings=[f]), "findings")

    def test_validate_rejects_extra_keys(self):
        self.rejects(make_verdict(note="n"), "note")
        self.rejects(make_verdict(findings=[{**FINDING, "note": "n"}]), "findings[0]")

    def test_validate_rejects_duplicate_finding_ids(self):
        self.rejects(make_verdict(findings=[FINDING, {**FINDING, "fix": "Other"}]), "duplicate")

    def test_validate_rejects_too_deep_json(self):
        self.rejects(expect="x.json: not valid JSON", raw="[" * 200000)

    @unittest.skipUnless((audit.judge_refs(audit.default_root()) / "verdict.schema.json").is_file(),
                         "skill-judge ships in a later PR")
    def test_verdict_key_sets_match_schema(self):
        schema = json.loads((audit.judge_refs(audit.default_root()) / "verdict.schema.json").read_text())
        self.assertEqual(set(schema["properties"]), audit.VERDICT_KEYS)
        self.assertEqual(set(schema["properties"]["findings"]["items"]["properties"]), audit.FINDING_KEYS)


class MergeTests(Base):
    def setUp(self):
        super().setUp()
        self.skill("x")
        self.inp = Path(self._tmp.name) / "in"
        self.out = Path(self._tmp.name) / "out"

    def put(self, judge="j1", skill="x", **kw):
        v = make_verdict(skill=skill, judge=judge, **kw)
        self.write(f"../in/{judge}/{skill}.json", json.dumps(v))

    def merge(self, *extra, judges="j1", skills="x"):
        argv = ["--root", str(self.root), "merge", "--in", str(self.inp), "--out", str(self.out), "--judges", judges]
        if skills:
            argv += ["--skills", skills]
        with contextlib.redirect_stderr(io.StringIO()):
            code = audit.main(argv + list(extra))
        merged = json.loads((self.out / "merged.json").read_text())
        return code, merged, (self.out / "report.md").read_text()

    def entry(self, *extra, name="x", **kw):
        return {s["name"]: s for s in self.merge(*extra, **kw)[1]["skills"]}[name]

    def upstream(self):
        return self.root / "docs" / "audit" / "upstream-findings.md"

    def check_file(self, entries):
        return str(self.write("../check.json", json.dumps({"skills": entries})))

    def waivers(self, percent):
        return str(self.write("../waivers.json", json.dumps([{"skill": "x", "percent": percent, "reason": "r", "date": "2026-10-24"}])))

    def merge_code(self, *extra):
        self.put("j1")
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            code = audit.main(["--root", str(self.root), "merge", "--in", str(self.inp), "--out", str(self.out),
                               "--judges", "j1", "--skills", "x", *extra])
        return code, err.getvalue()

    def test_merge_deeply_nested_check_file_exits_1(self):
        code, err = self.merge_code("--check", str(self.write("../deep-check.json", "[" * 200000)))
        self.assertEqual(code, 1)
        self.assertIn("cannot read", err)

    def test_merge_deeply_nested_waivers_file_exits_1(self):
        code, err = self.merge_code("--waivers", str(self.write("../deep-waivers.json", "[" * 200000)))
        self.assertEqual(code, 1)
        self.assertIn("cannot read", err)

    def test_merge_means_and_disagreement(self):
        self.put("j1", total=115)  # 92.0
        self.put("j2", total=100)  # 80.0
        e = self.entry(judges="j1,j2")
        self.assertEqual(e["percent"], 86.0)
        self.assertEqual(e["judges"], {"j1": 92.0, "j2": 80.0})
        self.assertTrue(e["disagreement"])
        self.put("j2", total=110)  # 88.0
        self.assertFalse(self.entry(judges="j1,j2")["disagreement"])

    def test_merge_grade_from_mean_percent(self):
        self.put("j1", total=119)  # 95.2, A
        self.put("j2", total=106)  # 84.8, B
        e = self.entry(judges="j1,j2")
        self.assertEqual(e["percent"], 90.0)
        self.assertEqual(e["grade"], "A")

    def test_merge_skips_invalid_verdict(self):
        self.put("j1", total=100)
        self.write("../in/j2/x.json", "{bad")
        e = self.entry(judges="j1,j2")
        self.assertEqual(e["judges"], {"j1": 80.0})
        self.assertEqual(e["missing_judges"], ["j2"])

    def test_merge_marks_synced_skills(self):
        self.skill("gepetto")
        self.put(skill="gepetto")
        e = self.entry(name="gepetto", skills="gepetto")
        self.assertTrue(e["synced"])
        self.assertFalse(self.entry()["synced"])

    def test_merge_needs_update_on_high_finding(self):
        self.put(total=115, findings=[FINDING])
        self.assertTrue(self.merge()[1]["needs_update"])
        self.put(total=115, findings=[{**FINDING, "severity": "medium"}])
        self.assertFalse(self.merge()[1]["needs_update"])

    def test_merge_synced_findings_go_to_upstream_file_only(self):
        self.skill("gepetto")
        self.put(total=115)
        crit = {**FINDING, "severity": "critical", "fix": "UNIQUE-FIX-TEXT"}
        self.put(skill="gepetto", total=62, findings=[crit])  # 49.6%
        chk = self.check_file([{"name": "gepetto", "ok": False, "synced": True,
                                "issues": [{"code": "non_latin", "detail": "UNIQUE-CHECK-DETAIL", "ignored": False}]}])
        code, merged, report = self.merge("--check", chk, skills="x,gepetto")
        self.assertEqual(code, 0)
        self.assertFalse(merged["needs_update"])
        g = {s["name"]: s for s in merged["skills"]}["gepetto"]
        self.assertEqual((g["findings"], g["check_issues"], g["skills_ref_valid"]), ([], [], None))
        up = self.upstream().read_text()
        self.assertIn("UNIQUE-FIX-TEXT", up)
        self.assertIn("UNIQUE-CHECK-DETAIL", up)
        self.assertIn(str(self.out), up)
        for text in (json.dumps(merged), report):
            self.assertNotIn("UNIQUE-FIX-TEXT", text)
            self.assertNotIn("UNIQUE-CHECK-DETAIL", text)
        self.assertIn("gepetto", report)

    def test_merge_rerun_does_not_duplicate_upstream_section(self):
        self.skill("gepetto")
        self.put(total=115)
        self.put(skill="gepetto", total=62, findings=[{**FINDING, "severity": "critical"}])
        self.merge(skills="x,gepetto")
        first = self.upstream().read_text()
        self.merge(skills="x,gepetto")
        self.assertEqual(self.upstream().read_text(), first)
        self.assertEqual(first.count(f"## {self.out}\n"), 1)

    def test_merge_without_synced_findings_leaves_upstream_file_absent(self):
        self.put()
        self.merge()
        self.assertFalse(self.upstream().exists())

    def test_merge_reports_unjudged_skill(self):
        code, merged, report = self.merge("--allow-incomplete")
        e = merged["skills"][0]
        self.assertEqual((e["percent"], e["grade"]), (None, "UNJUDGED"))
        self.assertIn("x", report)

    def test_merge_lists_missing_judges(self):
        self.put("j1")
        self.assertEqual(self.entry(judges="j1,j2")["missing_judges"], ["j2"])

    def test_merge_exit2_when_below_min_judges(self):
        self.put("j1")
        code, merged, _ = self.merge("--min-judges", "2", judges="j1,j2")
        self.assertEqual(code, 2)
        self.assertFalse(merged["complete"])

    def test_merge_min_judges_met_with_missing_judge_is_complete(self):
        self.put("j1")
        code, merged, _ = self.merge("--min-judges", "1", judges="j1,j2")
        self.assertEqual(code, 0)
        self.assertTrue(merged["complete"])
        self.assertEqual(merged["skills"][0]["missing_judges"], ["j2"])

    def test_merge_allow_incomplete_exits_0(self):
        code, merged, _ = self.merge("--allow-incomplete")
        self.assertEqual(code, 0)
        self.assertFalse(merged["complete"])

    def test_merge_subset_skills_complete(self):
        self.skill("y")
        self.put(skill="x")
        code, merged, _ = self.merge(skills="x")
        self.assertEqual((code, merged["complete"]), (0, True))
        self.assertEqual([s["name"] for s in merged["skills"]], ["x"])

    def test_merge_defaults_skills_to_all_skill_dirs(self):
        _, merged, _ = self.merge("--allow-incomplete", skills=None)
        self.assertEqual([s["name"] for s in merged["skills"]], ["skill-judge", "x"])

    def test_merge_carries_rubric_identity(self):
        self.put()
        merged = self.merge()[1]
        self.assertEqual((merged["rubric_version"], merged["spec_sha"]), (1, SHA))

    def test_merge_judges_are_slugged(self):
        self.put("router-env-my-judge")
        e = self.entry(judges="Router-Env/My Judge")
        self.assertEqual(list(e["judges"]), ["router-env-my-judge"])

    def test_merge_copies_check_results(self):
        self.put()
        issue = {"code": "missing_readme", "detail": "d", "ignored": True}
        chk = self.check_file([{"name": "x", "ok": True, "synced": False, "issues": [issue]}])
        self.assertEqual(self.entry("--check", chk)["check_issues"], [issue])

    def test_merge_without_check_leaves_skills_ref_valid_null(self):
        self.put()
        self.assertIsNone(self.entry()["skills_ref_valid"])

    def test_merge_skills_ref_valid_derived(self):
        self.skill("a"), self.skill("b"), self.skill("c"), self.skill("d")
        def iss(code, ignored=False):
            return [{"code": code, "detail": "d", "ignored": ignored}]
        chk = self.check_file([
            {"name": "a", "ok": False, "synced": False, "issues": iss("skills_ref")},
            {"name": "b", "ok": False, "synced": False, "issues": iss("missing_evals")},
            {"name": "c", "ok": True, "synced": False, "issues": iss("skills_ref", True)},
        ])
        merged = self.merge("--check", chk, skills="a,b,c,d", judges="j1")[1]
        by = {s["name"]: s for s in merged["skills"]}
        self.assertEqual([by[n]["skills_ref_valid"] for n in "abcd"], [False, True, True, None])
        self.assertEqual(by["d"]["check_issues"], [])

    def test_merge_skips_verdict_with_unhashable_finding_values(self):
        self.put("j1", findings=[{**FINDING, "severity": ["x"]}])
        self.put("j2", findings=[{**FINDING, "dimension": {}}])
        self.put("j3", total=115)
        code, merged, _ = self.merge(judges="j1,j2,j3")
        self.assertEqual(code, 0)
        e = merged["skills"][0]
        self.assertEqual((e["judges"], e["missing_judges"]), ({"j3": 92.0}, ["j1", "j2"]))

    def test_merge_rejects_min_judges_below_one(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            code = audit.main(["--root", str(self.root), "merge", "--in", str(self.inp), "--out", str(self.out),
                               "--judges", "j1", "--min-judges", "0"])
        self.assertEqual(code, 1)
        self.assertIn("--min-judges", err.getvalue())

    def test_merge_waiver_any_entry_matches(self):
        self.put(total=94)  # 75.2
        w = self.write("../waivers2.json", json.dumps([
            {"skill": "x", "percent": 70, "reason": "r", "date": "d"},
            {"skill": "x", "percent": 90, "reason": "r", "date": "d"}]))
        self.assertTrue(self.entry("--waivers", str(w))["waived"])

    def test_merge_dedups_findings(self):
        self.put("j1", findings=[FINDING])
        self.put("j2", findings=[{**FINDING, "id": "z", "fix": "DO IT"}])
        self.assertEqual(len(self.entry(judges="j1,j2")["findings"]), 1)

    def test_merge_dedup_keeps_higher_severity(self):
        for first, second in (("medium", "high"), ("high", "medium")):
            with self.subTest(first=first):
                self.put("j1", total=115, findings=[{**FINDING, "severity": first}])
                self.put("j2", total=115, findings=[{**FINDING, "id": "z", "severity": second}])
                merged = self.merge(judges="j1,j2")[1]
                self.assertTrue(merged["needs_update"])
                self.assertEqual([f["severity"] for f in merged["skills"][0]["findings"]], ["high"])

    def test_merge_disagreement_of_exactly_ten_is_not_flagged(self):
        self.put("j1")
        self.put("j2")
        data = {"j1": make_verdict(judge="j1", percent=70.4), "j2": make_verdict(judge="j2", percent=60.4)}
        with mock.patch("audit.read_verdict", side_effect=lambda p, r: (data[p.parent.name], [])):
            self.assertFalse(self.entry(judges="j1,j2")["disagreement"])

    def test_merge_ignored_check_issue_not_needs_update(self):
        self.put(total=115)
        mk = lambda ignored: self.check_file([{"name": "x", "ok": ignored, "synced": False,
                                                "issues": [{"code": "non_latin", "detail": "d", "ignored": ignored}]}])
        self.assertFalse(self.merge("--check", mk(True))[1]["needs_update"])
        self.assertTrue(self.merge("--check", mk(False))[1]["needs_update"])

    def test_merge_waived_skill_not_needs_update(self):
        self.put(total=90)  # 72.0
        code, merged, report = self.merge("--waivers", self.waivers(70))
        self.assertTrue(merged["skills"][0]["waived"])
        self.assertFalse(merged["needs_update"])
        self.assertIn("Waived", report)

    def test_merge_waiver_void_when_percent_dropped(self):
        self.put(total=81)  # 64.8
        merged = self.merge("--waivers", self.waivers(70))[1]
        self.assertFalse(merged["skills"][0]["waived"])
        self.assertTrue(merged["needs_update"])

    def test_merge_waived_skill_with_high_finding_needs_update(self):
        self.put(total=90, findings=[FINDING])
        merged = self.merge("--waivers", self.waivers(70))[1]
        self.assertTrue(merged["skills"][0]["waived"])
        self.assertTrue(merged["needs_update"])

    def test_merge_unjudged_sets_needs_update(self):
        self.assertTrue(self.merge("--allow-incomplete")[1]["needs_update"])


STUB = Path(__file__).resolve().parent / "fixtures" / "stub-runner.sh"


def alive(pid):
    """True while pid runs; a zombie waiting to be reaped counts as gone."""
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    stat = Path(f"/proc/{pid}/stat")
    return not (stat.exists() and stat.read_text().rsplit(")", 1)[1].split()[0] == "Z")


def evals_file(skill="s", evals=None):
    return {"skill_name": skill, "evals": evals if evals is not None else [
        {"id": "e1", "prompt": "do the thing", "assertions": ["A one", "A two"]}]}


def grade(assertions, passed=(True,), evidence="because"):
    return json.dumps({"results": [
        {"assertion": a, "passed": passed[i % len(passed)], "evidence": evidence}
        for i, a in enumerate(assertions)]})


class ValidateGradingTests(unittest.TestCase):
    def test_validate_grading_accepts_quoting_and_whitespace_drift(self):
        assertions = ['the body holds "pr-pending" image', "A  second\tassertion"]
        data = {"results": [
            {"assertion": "  the body holds 'pr-pending' image ", "passed": True, "evidence": "e"},
            {"assertion": "`A` second   assertion", "passed": True, "evidence": "e"},
        ]}
        self.assertEqual(audit.validate_grading(data, assertions), [])

    def test_validate_grading_accepts_curly_quote_normalization(self):
        self.assertEqual(audit.normalize_assertion("keep ‘the’ “diagram”"), "keep the diagram")

    def test_validate_grading_rejects_genuinely_different_assertion(self):
        data = {"results": [{"assertion": "a different claim entirely", "passed": True, "evidence": "e"}]}
        self.assertTrue(audit.validate_grading(data, ["the declared assertion"]))

    def test_validate_grading_keeps_count_check(self):
        data = {"results": [{"assertion": "A", "passed": True, "evidence": "e"}]}
        self.assertTrue(audit.validate_grading(data, ["A", "B"]))


class EvalBase(Base):
    def setUp(self):
        super().setUp()
        tmp = Path(self._tmp.name)
        self.answers, self.state, self.out = tmp / "answers", tmp / "state", tmp / "out"
        self.answers.mkdir()
        patcher = mock.patch.dict(os.environ, {"STUB_ANSWERS": str(self.answers), "STUB_STATE": str(self.state)})
        patcher.start()
        self.addCleanup(patcher.stop)
        os.environ.pop("STUB_SLEEP", None)

    def mk(self, name="s", evals="default", triggers=None, fixtures=None, skill_files=None):
        self.write(f"skills/{name}/SKILL.md", f"---\nname: {name}\ndescription: Does {name} things\n---\nBODY-OF-{name}\n")
        if evals == "default":
            evals = evals_file(name)
        if evals is not None:
            self.write(f"skills/{name}/evals/evals.json", json.dumps(evals))
        if triggers is not None:
            self.write(f"skills/{name}/evals/trigger-queries.json", json.dumps(triggers))
        for rel, text in (fixtures or {}).items():
            self.write(f"skills/{name}/evals/files/{rel}", text)
        for rel, text in (skill_files or {}).items():
            self.write(f"skills/{name}/{rel}", text)

    def answer(self, mode, key, *lines):
        (self.answers / f"{mode}-{key.replace('/', '__')}.txt").write_text("".join(f"{ln}\n" for ln in lines))

    def raw_answer(self, mode, key, text):
        (self.answers / f"{mode}-{key.replace('/', '__')}.raw").write_text(text)

    def ok_answers(self, key="s/e1", assertions=("A one", "A two"), passed=(True,)):
        self.answer("output", key, "model output")
        self.answer("grade", key, grade(list(assertions), passed))

    def run_evals(self, *extra, skills="s", runner=None, out=None):
        argv = ["--root", str(self.root), "run-evals", "--skills", skills,
                "--runner", runner or shlex.quote(str(STUB)), "--out", str(out or self.out), *extra]
        o, e = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(o), contextlib.redirect_stderr(e):
            code = audit.main(argv)
        return code, (json.loads(o.getvalue()) if o.getvalue().strip() else None), e.getvalue()

    def calls(self, ext="stdin"):
        d = self.state / "calls"
        files = sorted(d.glob(f"*.{ext}"), key=lambda f: int(f.stem)) if d.is_dir() else []
        return [f.read_text() for f in files]

    def cli(self, argv):
        err = io.StringIO()
        with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
            try:
                code = audit.main(["--root", str(self.root), *argv])
            except SystemExit as exc:
                code = exc.code
        return code, err.getvalue()

    def command_eval(self, data=None, name="explain-pr-changes"):
        return self.write(f"commands/evals/{name}.json", json.dumps(data or {
            "skill_name": name, "subject": "commands/explain-pr-changes.md",
            "context": ["skills/pr-diagrams/SKILL.md"],
            "evals": [{"id": "e1", "prompt": "TASK", "assertions": ["A"], "files": ["input.txt"]}],
        }))

    def eval_file_cli(self, path=None, *extra):
        return self.cli(["run-evals", "--eval-file", str(path or self.command_eval()), "--runner",
                         shlex.quote(str(STUB)), "--out", str(self.out), *extra])


class EvalFileTests(EvalBase):
    def test_run_evals_eval_file_only_selects_ids_and_uses_separate_summary(self):
        self.mk()
        self.write("commands/explain-pr-changes.md", "SUBJECT")
        self.write("commands/evals/files/input.txt", "INPUT")
        eval_path = self.command_eval({"skill_name": "explain-pr-changes", "subject": "commands/explain-pr-changes.md",
                                       "context": [], "evals": [
                                           {"id": "one", "prompt": "P1", "assertions": ["A"]},
                                           {"id": "two", "prompt": "P2", "assertions": ["B"]}]})
        self.answer("output", "explain-pr-changes/one", "output")
        self.answer("grade", "explain-pr-changes/one", grade(["A"]))
        code, err = self.eval_file_cli(eval_path, "--only", "one")
        self.assertEqual((code, err), (0, ""))
        self.assertEqual(len(self.calls()), 2)
        scoped = self.out / "explain-pr-changes/summary-output.only.json"
        self.assertEqual(json.loads(scoped.read_text())["total"], 1)
        self.assertFalse((self.out / "explain-pr-changes/summary-output.json").exists())

    def test_run_evals_eval_file_only_rejects_unknown_id(self):
        self.mk()
        self.write("commands/explain-pr-changes.md", "SUBJECT")
        self.command_eval()
        code, err = self.eval_file_cli(None, "--only", "missing")
        self.assertEqual(code, 2)
        self.assertIn("unknown eval id", err)

    def test_run_evals_eval_file_only_rejects_empty_list(self):
        self.mk()
        self.write("commands/explain-pr-changes.md", "SUBJECT")
        self.command_eval()
        code, err = self.eval_file_cli(None, "--only", ",")
        self.assertEqual(code, 2)
        self.assertIn("no eval ids", err)

    def test_run_evals_only_rejected_with_skills(self):
        self.mk()
        code, err = self.cli(["run-evals", "--skills", "s", "--runner", shlex.quote(str(STUB)),
                              "--only", "one"])
        self.assertEqual(code, 2)
        self.assertIn("--only is supported only with --eval-file", err)

    def test_run_evals_eval_file_inlines_subject_context_and_files(self):
        self.mk()
        self.write("commands/explain-pr-changes.md", "SUBJECT-TEXT")
        self.write("skills/pr-diagrams/SKILL.md", "CONTEXT-TEXT")
        self.write("commands/evals/files/input.txt", "FILE-TEXT")
        self.answer("output", "explain-pr-changes/e1", "output")
        self.answer("grade", "explain-pr-changes/e1", grade(["A"]))
        code, err = self.eval_file_cli()
        self.assertEqual((code, err), (0, ""))
        prompt = self.calls()[0]
        for text in ("SUBJECT-TEXT", "CONTEXT-TEXT", "FILE-TEXT"):
            self.assertIn(text, prompt)

    def test_run_evals_eval_file_grades_and_writes_summary(self):
        self.mk()
        self.write("commands/explain-pr-changes.md", "SUBJECT")
        self.write("skills/pr-diagrams/SKILL.md", "CONTEXT")
        self.write("commands/evals/files/input.txt", "INPUT")
        self.answer("output", "explain-pr-changes/e1", "output")
        self.answer("grade", "explain-pr-changes/e1", grade(["A"]))
        self.assertEqual(self.eval_file_cli()[0], 0)
        summary = self.out / "explain-pr-changes/summary-output.json"
        self.assertEqual(json.loads(summary.read_text())["skill"], "explain-pr-changes")
        self.assertEqual(self.eval_file_cli(None, "--fail-under", "1.1")[0], 1)
        summary.write_text("stale")
        data = {"skill_name": "explain-pr-changes", "subject": "missing.md",
                "evals": [{"id": "e1", "prompt": "P", "assertions": ["A"]}]}
        code, err = self.eval_file_cli(self.command_eval(data))
        self.assertEqual(code, 2)
        self.assertIn("does not exist", err)
        self.assertFalse(summary.exists())

    def test_run_evals_eval_file_rejects_triggers(self):
        self.command_eval()
        code, err = self.eval_file_cli(None, "--triggers")
        self.assertEqual(code, 2)
        self.assertIn("trigger queries are not supported for command eval files", err)

    def test_run_evals_eval_file_rejects_escape(self):
        cases = [
            ("files", {"files": ["../escape"]}, "outside the root"),
            ("subject", {"subject": "../escape.md"}, "outside the root"),
            ("context", {"context": ["../escape.md"]}, "outside the root"),
            ("missing subject", {"subject": "missing.md"}, "does not exist"),
            ("missing context", {"context": ["missing.md"]}, "does not exist"),
            ("name", {"skill_name": "wrong"}, "skill_name must equal the file stem"),
        ]
        for label, override, message in cases:
            with self.subTest(label=label):
                data = {"skill_name": "explain-pr-changes", "subject": "commands/explain-pr-changes.md",
                        "context": [], "evals": [{"id": "e1", "prompt": "P", "assertions": ["A"], "files": []}]}
                data.update(override)
                if "files" in override:
                    data["evals"][0]["files"] = override["files"]
                path = self.command_eval(data)
                (self.root / "commands/explain-pr-changes.md").write_text("SUBJECT")
                self.assertEqual(self.eval_file_cli(path)[0], 2)
                self.assertIn(message, self.eval_file_cli(path)[1])
        outside = self.write("elsewhere.json", "{}")
        code, err = self.eval_file_cli(outside)
        self.assertEqual(code, 2)
        self.assertIn("eval file must be under commands/evals/", err)

    def test_run_evals_eval_file_rejects_symlinked_evals_dir(self):
        # commands/evals itself must resolve inside the repo: a symlinked
        # evals directory pointing outside must be rejected (exit 2) before
        # any runner call.
        self.mk()
        self.write("commands/explain-pr-changes.md", "SUBJECT")
        external = Path(self._tmp.name) / "external-evals"
        external.mkdir()
        (external / "explain-pr-changes.json").write_text(json.dumps({
            "skill_name": "explain-pr-changes", "subject": "commands/explain-pr-changes.md",
            "context": [], "evals": [{"id": "e1", "prompt": "P", "assertions": ["A"]}]}))
        (self.root / "commands" / "evals").symlink_to(external, target_is_directory=True)
        code, err = self.eval_file_cli("commands/evals/explain-pr-changes.json")
        self.assertEqual(code, 2)
        self.assertIn("eval file must be under commands/evals/", err)
        self.assertEqual(self.calls(), [])

    def test_run_evals_eval_file_rejects_stem_escape(self):
        out = Path(self._tmp.name) / "out"
        out.mkdir()
        sentinel = out.parent / "summary-output.json"
        sentinel.write_text("safe")
        bad = Path(str(self.root / "commands/evals") + "/...")
        code, err = self.cli(["run-evals", "--eval-file", str(bad), "--runner", "true", "--out", str(out)])
        self.assertEqual(code, 2)
        self.assertIn("outside --out", err)
        self.assertTrue(sentinel.is_file())

    def test_run_evals_skills_and_eval_file_are_exclusive(self):
        for args, expected in ((["--skills", "x", "--eval-file", "x.json"], "not allowed with argument"),
                               ([], "one of the arguments --skills --eval-file is required")):
            code, err = self.cli(["run-evals", *args, "--runner", "true"])
            self.assertEqual(code, 2)
            self.assertIn(expected, err)

    def test_build_output_prompt_skills_unchanged(self):
        self.mk()
        ev = {"id": "e1", "prompt": "do the thing", "assertions": ["A one", "A two"]}
        expected = ("MODE: output\nKEY: s/e1\n\n" + audit.SANDBOX_PREAMBLE + "\n\n"
                    + "=== SKILL.md of s ===\n---\nname: s\ndescription: Does s things\n---\nBODY-OF-s\n\n"
                    + "=== TASK ===\ndo the thing\n")
        self.assertEqual(audit.build_output_prompt(self.root, "s", ev, ""), expected)


class RunEvalsTests(EvalBase):
    def test_run_evals_grades_assertions(self):
        self.mk()
        self.ok_answers(passed=(True, False))
        code, res, _ = self.run_evals()
        self.assertEqual(code, 1)  # 0.5 < default 0.8
        self.assertEqual(res[0]["pass_rate"], 0.5)
        self.assertEqual((res[0]["passed"], res[0]["total"]), (1, 2))
        self.assertEqual(res[0]["failures"][0]["assertion"], "A two")
        g = json.loads((self.out / "s/output/e1/grading.json").read_text())
        self.assertEqual(len(g["results"]), 2)

    def test_run_evals_fail_under_exits_1(self):
        self.mk()
        self.ok_answers(passed=(True, False))
        self.assertEqual(self.run_evals("--fail-under", "0.5")[0], 0)
        self.assertEqual(self.run_evals("--fail-under", "0.6")[0], 1)

    def test_run_evals_harness_error_exits_2(self):
        self.mk()  # no answer files: stub exits 1
        code, res, err = self.run_evals()
        self.assertEqual((code, res), (2, None))
        self.assertIn("runner exited 1", err)

    def test_run_evals_missing_file_exits_2(self):
        self.mk(evals=None)
        self.assertEqual(self.run_evals()[0], 2)

    def test_run_evals_skips_synced(self):
        self.mk("gepetto", evals=None)
        code, res, _ = self.run_evals(skills="gepetto")
        self.assertEqual((code, res), (0, [{"skill": "gepetto", "skipped": "synced"}]))
        self.assertEqual(self.calls(), [])

    def test_run_evals_output_and_triggers_keep_separate_summaries(self):
        self.mk(triggers=[{"query": "q", "should_trigger": True}])
        self.ok_answers()
        self.answer("trigger", "s/q0", '{"skill":"s"}')
        self.assertEqual(self.run_evals()[0], 0)
        self.assertEqual(self.run_evals("--triggers", "--runs", "1")[0], 0)
        o = json.loads((self.out / "s/summary-output.json").read_text())
        t = json.loads((self.out / "s/summary-triggers.json").read_text())
        self.assertEqual((o["mode"], t["mode"]), ("output", "triggers"))

    def test_run_evals_partial_run_removes_stale_summary(self):
        self.mk()
        self.ok_answers()
        self.assertEqual(self.run_evals()[0], 0)
        summary = self.out / "s/summary-output.json"
        self.assertTrue(summary.is_file())
        (self.answers / "grade-s__e1.txt").unlink()  # runner now fails mid-run
        self.assertEqual(self.run_evals()[0], 2)
        self.assertFalse(summary.exists())

    def test_run_evals_rejects_bad_skill_name(self):
        self.mk()
        for name in ("../x", "/tmp/x", "a/b", "Foo", "nodir"):
            with self.subTest(name=name):
                self.assertEqual(self.run_evals(skills=name)[0], 2)
                self.assertFalse(self.out.exists())
                self.assertFalse((self.root.parent / "x").exists())
        self.assertEqual(self.calls(), [])

    def test_run_evals_artifact_locations(self):
        self.mk()
        self.ok_answers()
        self.assertEqual(self.run_evals()[0], 0)
        self.assertTrue((self.out / "s/output/e1/output.txt").is_file())
        self.assertTrue((self.out / "s/output/e1/grading.json").is_file())
        self.assertTrue((self.out / "s/summary-output.json").is_file())
        self.assertEqual(sorted(p.name for p in (self.out / "s/output").rglob("*") if p.is_file()),
                         ["grading.json", "output.txt"])

    def test_run_evals_default_out_under_root(self):
        self.mk()
        self.ok_answers()
        argv = ["--root", str(self.root), "run-evals", "--skills", "s", "--runner", shlex.quote(str(STUB))]
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(audit.main(argv), 0)
        self.assertTrue((self.root / "docs/audit/evals/s/summary-output.json").is_file())

    def test_run_evals_runs_in_sandbox_cwd(self):
        self.mk(skill_files={"extra.txt": "x"})
        self.ok_answers()
        self.assertEqual(self.run_evals()[0], 0)
        pwds, lss = self.calls("pwd"), self.calls("ls")
        self.assertEqual((len(pwds), len(lss)), (2, 2))  # output call + grade call
        for pwd, ls in zip(pwds, lss):
            self.assertFalse(Path(pwd.strip()).resolve().is_relative_to(self.root.resolve()))
            self.assertEqual(ls, "")

    def test_run_evals_prompt_contains_skill_and_files(self):
        ev = {"id": "e1", "prompt": "THE-TASK", "files": ["in.txt", "sub/fx.txt"], "expected_output": "EXPECTED-TEXT",
              "assertions": ["A one", "A two"]}
        self.mk(evals=evals_file(evals=[ev]), skill_files={"in.txt": "IN-TEXT"}, fixtures={"sub/fx.txt": "FX-TEXT"})
        self.ok_answers()
        self.assertEqual(self.run_evals()[0], 0)
        out_p, grade_p = self.calls()
        self.assertTrue(out_p.startswith("MODE: output\nKEY: s/e1\n"))
        for needle in ("BODY-OF-s", "=== SKILL.md of s ===", "=== FILE in.txt ===\nIN-TEXT",
                       "=== FILE sub/fx.txt ===\nFX-TEXT", "=== TASK ===\nTHE-TASK", audit.SANDBOX_PREAMBLE):
            self.assertIn(needle, out_p)
        self.assertNotIn("EXPECTED-TEXT", out_p)

    def test_grade_prompt_contains_files_and_expected_output(self):
        ev = {"id": "e1", "prompt": "P", "files": ["in.txt"], "expected_output": "EXPECTED-TEXT", "assertions": ["A one", "A two"]}
        self.mk(evals=evals_file(evals=[ev]), skill_files={"in.txt": "IN-TEXT"})
        self.ok_answers()
        self.run_evals()
        g = self.calls()[1]
        self.assertTrue(g.startswith("MODE: grade\nKEY: s/e1\n"))
        for needle in ("=== FILE in.txt ===\nIN-TEXT", "=== EXPECTED_OUTPUT ===\nEXPECTED-TEXT", "ASSERTIONS:",
                       "1. A one", "2. A two", "OUTPUT:\nmodel output", audit.SANDBOX_PREAMBLE):
            self.assertIn(needle, g)

    def test_eval_files_bad_paths_exit_2(self):
        for bad in ("../x", "/etc/passwd", "missing.txt"):
            with self.subTest(bad=bad):
                ev = {"id": "e1", "prompt": "P", "files": [bad], "assertions": ["A"]}
                self.mk(evals=evals_file(evals=[ev]))
                self.assertEqual(self.run_evals()[0], 2)

    def test_eval_files_symlink_escape_exits_2(self):
        secret = Path(self._tmp.name) / "secret.txt"
        secret.write_text("SECRET-MARKER")
        ev = {"id": "e1", "prompt": "P", "files": ["link.txt"], "assertions": ["A"]}
        self.mk(evals=evals_file(evals=[ev]))
        link = self.root / "skills/s/evals/files/link.txt"
        link.parent.mkdir(parents=True, exist_ok=True)
        link.symlink_to(secret)
        self.ok_answers(assertions=("A",))
        self.assertEqual(self.run_evals()[0], 2)
        self.assertFalse(any("SECRET-MARKER" in c for c in self.calls()))

    def test_eval_integer_ids_accepted(self):
        self.mk(evals=evals_file(evals=[{"id": 1, "prompt": "P", "assertions": ["A"]}]))
        self.ok_answers(key="s/1", assertions=("A",))
        self.assertEqual(self.run_evals()[0], 0)
        self.assertTrue((self.out / "s/output/1/output.txt").is_file())

    def test_eval_bad_ids_exit_2(self):
        for bad in ("/tmp/escape", "../../x", "a/b", "..", "", True):
            with self.subTest(bad=bad):
                self.mk(evals=evals_file(evals=[{"id": bad, "prompt": "P", "assertions": ["A"]}]))
                self.assertEqual(self.run_evals()[0], 2)
                self.assertFalse(self.out.exists())
        self.mk(evals=evals_file(evals=[{"id": 1, "prompt": "P", "assertions": ["A"]},
                                        {"id": "1", "prompt": "P", "assertions": ["A"]}]))
        self.assertEqual(self.run_evals()[0], 2)

    def test_eval_with_no_assertions_exits_2(self):
        for bad in ([], [""], "x", None):
            with self.subTest(bad=bad):
                self.mk(evals=evals_file(evals=[{"id": "e", "prompt": "P", "assertions": bad}]))
                self.assertEqual(self.run_evals()[0], 2)

    def test_empty_evals_list_exits_2(self):
        self.mk(evals=evals_file(evals=[]))
        self.assertEqual(self.run_evals()[0], 2)

    def test_run_evals_symlinked_skill_out_dir_exits_2(self):
        self.mk()
        self.ok_answers()
        elsewhere = Path(self._tmp.name) / "elsewhere"
        elsewhere.mkdir()
        self.out.mkdir()
        (self.out / "s").symlink_to(elsewhere)
        self.assertEqual(self.run_evals()[0], 2)
        self.assertEqual(list(elsewhere.rglob("*")), [])

    def test_run_evals_crashes_exit_2_not_1(self):
        self.mk()
        self.ok_answers()
        (self.root / "skills/s/SKILL.md").unlink()
        self.assertEqual(self.run_evals()[0], 2)
        self.mk()
        blocker = Path(self._tmp.name) / "afile"
        blocker.write_text("x")
        self.assertEqual(self.run_evals(out=blocker)[0], 2)
        (self.root / "skills/s/SKILL.md").write_bytes(b"\xff\xfe")
        self.assertEqual(self.run_evals()[0], 2)

    def test_fail_under_uses_unrounded_rate(self):
        self.mk(evals=evals_file(evals=[{"id": "e1", "prompt": "P", "assertions": ["a", "b", "c"]}]))
        self.ok_answers(assertions=("a", "b", "c"), passed=(True, True, False))  # 2/3 = 0.6667
        self.assertEqual(self.run_evals("--fail-under", "0.66667")[0], 1)
        self.assertEqual(self.run_evals("--fail-under", "0.6666")[0], 0)

    def test_eval_skill_name_mismatch_exits_2(self):
        self.mk(evals=evals_file("other"))
        self.assertEqual(self.run_evals()[0], 2)

    def test_run_evals_too_deep_answer_exits_2(self):
        self.mk()
        self.answer("output", "s/e1", "model output")
        self.answer("grade", "s/e1", "[" * 200000)
        code, res, err = self.run_evals()
        self.assertEqual((code, res), (2, None))
        self.assertIn("harness error", err)


class RunnerTests(EvalBase):
    def setUp(self):
        super().setUp()
        self.mk()
        self.ok_answers()

    def test_runner_timeout_exits_2(self):
        os.environ["STUB_SLEEP"] = "3"
        code, _, err = self.run_evals("--timeout", "1")
        self.assertEqual(code, 2)
        self.assertIn("timed out", err)

    def test_runner_timeout_kills_wrapper_children(self):
        pidfile = Path(self._tmp.name) / "child.pid"
        wrapper = self.write("wrapper.sh", f"#!/bin/bash\nsleep 30 </dev/null >/dev/null 2>&1 &\necho $! > {pidfile}\nwait\n")
        wrapper.chmod(0o755)
        code, _, err = self.run_evals("--timeout", "1", runner=str(wrapper))
        self.assertEqual(code, 2)
        self.assertIn("timed out", err)
        pid = int(pidfile.read_text())
        self.addCleanup(lambda: alive(pid) and os.kill(pid, 9))
        deadline = time.monotonic() + 5
        while alive(pid) and time.monotonic() < deadline:
            time.sleep(0.05)
        self.assertFalse(alive(pid))

    def test_runner_killed_when_communicate_is_interrupted(self):
        made = []
        real = audit.subprocess.Popen

        def popen(*a, **k):
            p = real(*a, **k)
            p.communicate = mock.Mock(side_effect=KeyboardInterrupt)
            made.append(p)
            return p

        sleeper = self.write("sleeper.sh", "#!/bin/bash\nsleep 30\n")
        sleeper.chmod(0o755)
        with mock.patch.object(audit.subprocess, "Popen", popen), self.assertRaises(KeyboardInterrupt):
            audit.call_runner([str(sleeper)], "p", 5)
        self.addCleanup(lambda: alive(made[0].pid) and os.kill(made[0].pid, 9))
        self.assertFalse(alive(made[0].pid))

    def test_runner_post_kill_drain_is_bounded(self):
        pidfile = Path(self._tmp.name) / "daemon.pid"
        # the setsid child escapes killpg yet keeps the stdout pipe open
        wrapper = self.write("wrapper.sh", f"#!/bin/bash\nsetsid sleep 30 &\necho $! > {pidfile}\nwait\n")
        wrapper.chmod(0o755)
        t0 = time.monotonic()
        with mock.patch.object(audit, "KILL_DRAIN_TIMEOUT", 0.5, create=True), self.assertRaises(audit.HarnessError) as cm:
            audit.call_runner([str(wrapper)], "p", 1)
        self.addCleanup(lambda: alive(int(pidfile.read_text())) and os.kill(int(pidfile.read_text()), 9))
        self.assertIn("timed out", str(cm.exception))
        self.assertLess(time.monotonic() - t0, 10)

    def test_runner_not_executable_exits_2(self):
        p = self.write("noexec.sh", "#!/bin/bash\n")
        p.chmod(0o644)
        self.assertEqual(self.run_evals(runner=str(p))[0], 2)

    def test_runner_relative_path_resolves(self):
        tmp = Path(self._tmp.name)
        (tmp / "bin").mkdir()
        shutil.copy2(STUB, tmp / "bin" / "stub-runner.sh")
        old = os.getcwd()
        os.chdir(tmp)
        self.addCleanup(os.chdir, old)
        self.assertEqual(self.run_evals(runner="./bin/stub-runner.sh")[0], 0)

    def test_runner_bare_name_uses_path(self):
        bindir = Path(self._tmp.name) / "pathbin"
        bindir.mkdir()
        (bindir / "stub-runner").symlink_to(STUB)
        with mock.patch.dict(os.environ, {"PATH": f"{bindir}:{os.environ['PATH']}"}):
            self.assertEqual(self.run_evals(runner="stub-runner")[0], 0)

    def test_runner_args_tokenised(self):
        bindir = Path(self._tmp.name) / "pathbin"
        bindir.mkdir()
        (bindir / "stub-runner").symlink_to(STUB)
        with mock.patch.dict(os.environ, {"PATH": f"{bindir}:{os.environ['PATH']}"}):
            self.assertEqual(self.run_evals(runner="stub-runner --model 'a b'")[0], 0)
        self.assertEqual(self.calls("argv")[0], "--model\na b\n")

    def test_runner_not_found_exits_2(self):
        self.assertEqual(self.run_evals(runner="no-such-runner-xyz")[0], 2)
        self.assertEqual(self.run_evals(runner="./no/such/runner")[0], 2)


class ParseObjectTests(Base):
    def test_parse_object_accepts(self):
        obj = {"results": [{"assertion": "a", "passed": True, "evidence": "e"}]}
        raw = json.dumps(obj)
        inner = {"results": [{"assertion": "a", "passed": True,
                              "evidence": "the body has a ```mermaid\nflow TD\n``` block"}]}
        fenced_inner = f"```json\n{json.dumps(inner)}\n```"
        for text, want in ((raw, obj), (f"```\n{raw}\n```", obj),
                           (f"```json\n{raw}\n```", obj), (fenced_inner, inner)):
            with self.subTest(text=text[:20]):
                self.assertEqual(audit.parse_object(text, "t"), want)

    def test_parse_object_rejects(self):
        raw = '{"results":[]}'
        for text in (f"Sure:\n```json\n{raw}\n```", f"```json\n{raw}\n```.\nHope that helps",
                     f"```json\n{raw}\n```\n```json\n{raw}\n```", "```json\nnot json\n```"):
            with self.subTest(text=text[:20]):
                with self.assertRaises(audit.HarnessError) as cm:
                    audit.parse_object(text, "t")
                self.assertIn("answer is not JSON", str(cm.exception))


class GraderTests(EvalBase):
    def check_bad(self, answer, err_contains=None):
        self.mk()
        self.answer("output", "s/e1", "model output")
        self.raw_answer("grade", "s/e1", answer)
        code, res, err = self.run_evals()
        self.assertEqual((code, res), (2, None), err)
        self.assertFalse((self.out / "s/summary-output.json").exists())
        if err_contains is not None:
            self.assertIn(err_contains, err)

    def entry(self, a="A one", passed=True, evidence="because"):
        return {"assertion": a, "passed": passed, "evidence": evidence}

    def test_grader_missing_assertion(self):
        self.check_bad(json.dumps({"results": [self.entry("A one")]}))

    def test_grader_empty_results(self):
        self.check_bad('{"results":[]}')

    def test_grader_duplicate_assertion(self):
        self.check_bad(json.dumps({"results": [self.entry("A one"), self.entry("A one")]}))

    def test_grader_unknown_assertion(self):
        self.check_bad(json.dumps({"results": [self.entry("A one"), self.entry("A three")]}))

    def test_grader_non_bool_passed(self):
        self.check_bad(json.dumps({"results": [self.entry("A one", "true"), self.entry("A two")]}))

    def test_grader_empty_evidence(self):
        self.check_bad(json.dumps({"results": [self.entry("A one"), self.entry("A two", evidence="")]}))

    def test_grader_not_json_or_object(self):
        for bad in ("oops", "[]", '{"results":3}'):
            with self.subTest(bad=bad):
                self.check_bad(bad)

    def test_grader_accepts_raw_answer(self):
        self.mk()
        self.answer("output", "s/e1", "model output")
        self.raw_answer("grade", "s/e1", grade(["A one", "A two"]))
        code, res, err = self.run_evals()
        self.assertEqual((code, res[0]["passed"]), (0, 2), err)

    def test_grader_accepts_one_fenced_answer(self):
        body = grade(["A one", "A two"])
        for fenced in (f"```json\n{body}\n```", f"```\n{body}\n```", f"\n```json\n{body}\n```\n"):
            with self.subTest(fenced=fenced[:12]):
                self.mk()
                self.answer("output", "s/e1", "model output")
                self.raw_answer("grade", "s/e1", fenced)
                code, res, err = self.run_evals()
                self.assertEqual((code, res[0]["passed"]), (0, 2), err)

    def test_grader_accepts_fence_with_backticks_in_strings(self):
        body = json.dumps({"results": [
            self.entry("A one", evidence="the body has a ```mermaid\nflow TD\n``` block"),
            self.entry("A two"),
        ]})
        self.mk()
        self.answer("output", "s/e1", "model output")
        self.raw_answer("grade", "s/e1", f"```json\n{body}\n```")
        code, res, err = self.run_evals()
        self.assertEqual((code, res[0]["passed"]), (0, 2), err)

    def test_grader_fence_only_when_it_wraps_the_whole_answer(self):
        body = grade(["A one", "A two"])
        self.check_bad(f"Here you go:\n```json\n{body}\n```", err_contains="answer is not JSON")
        self.check_bad(f"```json\n{body}\n```\n```json\n{body}\n```", err_contains="answer is not JSON")

    def test_grader_fence_with_invalid_json_exits_2(self):
        for bad in ("```json\nnot json\n```", "```\n{'results': []}\n```"):
            with self.subTest(bad=bad):
                self.check_bad(bad, err_contains="answer is not JSON")


class TriggerTests(EvalBase):
    Q = [{"query": "q", "should_trigger": True}]

    def trig(self, *extra, skills="s"):
        return self.run_evals("--triggers", *extra, skills=skills)

    def test_triggers_rate_over_runs(self):
        self.mk(triggers=[{"query": "yes", "should_trigger": True}, {"query": "no", "should_trigger": False}])
        self.answer("trigger", "s/q0", '{"skill":"s"}', '{"skill":"s"}', '{"skill":"none"}')
        self.answer("trigger", "s/q1", '{"skill":"s"}', '{"skill":"s"}', '{"skill":"none"}')
        code, res, _ = self.trig("--runs", "3")
        self.assertEqual(code, 1)
        self.assertEqual((res[0]["passed"], res[0]["total"]), (1, 2))  # q0 rate 0.67 passes, q1 rate 0.67 fails
        self.assertEqual(res[0]["failures"], [{"query": "no", "should_trigger": False, "rate": 0.67}])

    def test_triggers_rate_exactly_half_fails_both(self):
        self.mk(triggers=[{"query": "yes", "should_trigger": True}, {"query": "no", "should_trigger": False}])
        for k in ("s/q0", "s/q1"):
            self.answer("trigger", k, '{"skill":"s"}', '{"skill":"none"}')
        code, res, _ = self.trig("--runs", "2")
        self.assertEqual((code, res[0]["passed"], len(res[0]["failures"])), (1, 0, 2))
        self.assertEqual(res[0]["pass_rate"], 0)

    def test_triggers_catalog_excludes_synced(self):
        self.mk("a", triggers=self.Q)
        self.mk("gepetto", evals=None)
        self.answer("trigger", "a/q0", '{"skill":"a"}')
        self.assertEqual(self.trig("--runs", "1", skills="a")[0], 0)
        p = self.calls()[0]
        self.assertTrue(p.startswith("MODE: trigger\nKEY: a/q0\n"))
        for needle in ("CATALOG:", "- a: Does a things", "REQUEST:\nq", audit.SANDBOX_PREAMBLE):
            self.assertIn(needle, p)
        self.assertNotIn("- gepetto:", p)

    def test_catalog_collapses_block_scalar_newlines(self):
        self.write("skills/s/SKILL.md", "---\nname: s\ndescription: |\n  first line\n\n  second   line\n---\nB\n")
        self.assertEqual(audit.catalog(self.root)["s"], "first line second line")

    def test_catalog_keys_on_directory_name(self):
        self.write("skills/s/SKILL.md", "---\nname: other\ndescription: d\n---\nB\n")
        self.assertEqual(list(audit.catalog(self.root)), ["s"])

    def test_trigger_malformed_answer_exits_2(self):
        self.mk(triggers=self.Q)
        for bad in ("oops", "[]", "{}", '{"skill":3}', '{"skill":"unknown"}', '{"skill":"s","x":1}'):
            with self.subTest(bad=bad):
                self.answer("trigger", "s/q0", bad)
                self.assertEqual(self.trig("--runs", "1")[0], 2)
                self.assertFalse((self.out / "s/summary-triggers.json").exists())

    def test_trigger_accepts_one_fenced_answer(self):
        self.mk(triggers=self.Q)
        self.raw_answer("trigger", "s/q0", '```json\n{"skill":"s"}\n```')
        self.assertEqual(self.trig("--runs", "1")[0], 0)

    def test_trigger_prose_or_two_fences_exit_2(self):
        self.mk(triggers=self.Q)
        for bad in ('Answer:\n```json\n{"skill":"s"}\n```', '```json\n{"skill":"s"}\n```\n```json\n{"skill":"s"}\n```'):
            with self.subTest(bad=bad):
                self.raw_answer("trigger", "s/q0", bad)
                self.assertEqual(self.trig("--runs", "1")[0], 2)

    def test_trigger_file_invalid_exits_2(self):
        for bad in ([], [{"query": "", "should_trigger": True}], [{"query": "q", "should_trigger": "yes"}], {"a": 1}):
            with self.subTest(bad=bad):
                self.mk(triggers=bad)
                self.assertEqual(self.trig("--runs", "1")[0], 2)


class PiCmdTests(Base):
    def pi(self, *args):
        o = io.StringIO()
        with contextlib.redirect_stdout(o):
            self.assertEqual(audit.main(["pi-cmd", *args]), 0)
        return o.getvalue()

    def test_pi_commands_disable_tools_mcp_skills(self):
        runner = self.pi("runner").split()
        for flag in ("--no-tools", "--no-mcp", "--no-extensions", "--no-skills", "--no-context-files"):
            self.assertIn(flag, runner)
        self.assertNotIn("--tools", runner)
        self.assertEqual(runner[-2:], ["--model", "router-env/my-referee-one"])
        judge = self.pi("judge").split()
        for flag in ("--no-mcp", "--no-extensions", "--no-skills", "--no-context-files"):
            self.assertIn(flag, judge)
        self.assertEqual(judge[judge.index("--tools") + 1], "read,grep,find,ls")
        for bad in ("--no-tools", "bash", "edit", "write"):
            self.assertNotIn(bad, judge)
        toks = self.pi("judge", "--print0", "--model", "a b").split("\0")
        self.assertEqual(toks.pop(), "")  # NUL-terminated for mapfile -d ''
        self.assertIn("a b", toks)
        self.assertEqual(toks, audit.pi_cmd("judge", "a b"))
        self.assertEqual(shlex.split(self.pi("judge", "--model", "a b")), toks)


if __name__ == "__main__":
    unittest.main()
