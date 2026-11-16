import json
import os
import subprocess
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[3] / "skills/session-handoff/scripts/check_staleness.py"
GIT_ENV = {**os.environ, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull}


class CheckStalenessTests(unittest.TestCase):
    def test_reports_fresh_handoff_for_current_git_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-b", "main"], cwd=root, check=True, capture_output=True, env={**GIT_ENV, "HOME": str(root)})
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True, env={**GIT_ENV, "HOME": str(root)})
            subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True, env={**GIT_ENV, "HOME": str(root)})
            (root / "src.py").write_text("fixture\n")
            subprocess.run(["git", "add", "src.py"], cwd=root, check=True, env={**GIT_ENV, "HOME": str(root)})
            subprocess.run(["git", "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null", "commit", "-m", "fixture"], cwd=root, check=True, capture_output=True, env={**GIT_ENV, "HOME": str(root)})
            handoff = root / "handoff.md"
            baseline = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, check=True, capture_output=True, text=True).stdout.strip()
            handoff.write_text(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nProject: {root}\nBranch: main\nBaseline commit: {baseline}\n")

            result = subprocess.run(["python3", str(SCRIPT), str(handoff)], text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Staleness Level: FRESH", result.stdout)
            self.assertIn("Branch matches: Yes", result.stdout)

    def test_stale_handoff_and_branch_mismatch_are_not_fresh(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-b", "main"], cwd=root, check=True, capture_output=True, env={**GIT_ENV, "HOME": str(root)})
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True, env={**GIT_ENV, "HOME": str(root)})
            subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True, env={**GIT_ENV, "HOME": str(root)})
            (root / "src").mkdir()
            (root / "src/src.py").write_text("fixture\n")
            subprocess.run(["git", "add", "src/src.py"], cwd=root, check=True, env={**GIT_ENV, "HOME": str(root)})
            subprocess.run(["git", "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null", "commit", "-m", "fixture"], cwd=root, check=True, capture_output=True, env={**GIT_ENV, "HOME": str(root)})
            handoff = root / "handoff.md"
            created = (datetime.now() - timedelta(days=40)).strftime("%Y-%m-%d %H:%M:%S")
            baseline = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, check=True, capture_output=True, text=True).stdout.strip()
            handoff.write_text(f"Created: {created}\nProject: {root}\nBranch: old-branch\nBaseline commit: {baseline}\n\n| src/src.py | Existing fixture |\n| src/missing.py | Removed file |\n")
            (root / "untracked.txt").write_text("pending\n")
            (root / "src/src.py").write_text("modified\n")
            result = subprocess.run(["python3", str(SCRIPT), str(handoff)], text=True, capture_output=True)
            self.assertNotEqual(result.returncode, 0, result.stdout)
            self.assertNotIn("Staleness Level: FRESH", result.stdout)
            self.assertEqual(result.returncode, 2)
            self.assertIn("Staleness Level: VERY_STALE", result.stdout)
            self.assertIn("Verdict: [WARNING] Consider creating fresh handoff", result.stdout)
            self.assertIn("Branch matches: No", result.stdout)
            self.assertIn("Files changed:", result.stdout)
            self.assertIn("Missing referenced files:", result.stdout)
            self.assertIn("- src/missing.py", result.stdout)

    def test_deleted_predecessor_link_is_reported_as_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            env = {**GIT_ENV, "HOME": str(root)}
            git = ["git", "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null", "-c", "user.email=t@example.com", "-c", "user.name=T"]
            subprocess.run(["git", "init", "-b", "main"], cwd=root, check=True, capture_output=True, env=env)
            (root / "a.txt").write_text("x\n")
            subprocess.run(["git", "add", "a.txt"], cwd=root, check=True, env=env)
            subprocess.run([*git, "commit", "-m", "fixture"], cwd=root, check=True, capture_output=True, env=env)
            baseline = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, check=True, capture_output=True, text=True).stdout.strip()
            handoffs = root / ".claude/handoffs"
            handoffs.mkdir(parents=True)
            handoff = handoffs / "2026-01-02-120000-next.md"
            handoff.write_text(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nProject: {root}\nBranch: main\nBaseline commit: {baseline}\n"
                               "- **Continues from**: [2026-01-01-120000-prev.md](./2026-01-01-120000-prev.md)\n")
            result = subprocess.run(["python3", str(SCRIPT), str(handoff)], text=True, capture_output=True)
            self.assertIn("- ./2026-01-01-120000-prev.md", result.stdout)

    def test_setup_test_env_fixtures_yield_fresh_and_stale(self):
        setup = Path(__file__).with_name("setup_test_env.py")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "proj"
            subprocess.run(["python3", str(setup), "--path", str(root)], check=True, capture_output=True, env={**GIT_ENV, "HOME": tmp})
            levels = {}
            for f in (root / ".claude/handoffs").glob("*.md"):
                if "incomplete" not in f.name:
                    out = subprocess.run(["python3", str(SCRIPT), str(f)], text=True, capture_output=True).stdout
                    levels[f.name.split("-", 4)[-1]] = out
            self.assertIn("Staleness Level: FRESH", levels["auth-implementation.md"])
            self.assertIn("Staleness Level: STALE", levels["database-setup.md"])

    def test_missing_baseline_is_unknown_not_fresh(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-b", "main"], cwd=root, check=True, capture_output=True, env={**GIT_ENV, "HOME": str(root)})
            handoff = root / "handoff.md"
            handoff.write_text(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\nProject: {root}\\nBranch: main\\n")
            result = subprocess.run(["python3", str(SCRIPT), str(handoff)], text=True, capture_output=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn("Staleness Level: UNKNOWN", result.stdout)

    def test_missing_handoff_is_reported_as_unknown_with_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(["python3", str(SCRIPT), str(Path(tmp) / "missing.md")], text=True, capture_output=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn("Handoff file not found", result.stderr)
            self.assertEqual(result.stdout, "")

    def _repo_with_commit(self, root):
        env = {**GIT_ENV, "HOME": str(root)}
        subprocess.run(["git", "init", "-b", "main"], cwd=root, check=True, capture_output=True, env=env)
        (root / "src.py").write_text("fixture\n")
        (root / "old.py").write_text("old\n")
        subprocess.run(["git", "add", "."], cwd=root, check=True, env=env)
        subprocess.run(["git", "-c", "user.email=t@example.com", "-c", "user.name=T", "-c", "commit.gpgsign=false",
                        "-c", "core.hooksPath=/dev/null", "commit", "-m", "fixture"], cwd=root, check=True, capture_output=True, env=env)
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, check=True, capture_output=True, text=True).stdout.strip()

    def test_json_keeps_exact_path_of_unstaged_modification_and_rename_source(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as notes:
            root = Path(tmp)
            baseline = self._repo_with_commit(root)
            (root / "src.py").write_text("modified\n")  # first status record is " M src.py"
            subprocess.run(["git", "mv", "old.py", "zz_new.py"], cwd=root, check=True, env={**GIT_ENV, "HOME": str(root)})
            raw = subprocess.run(["git", "status", "--porcelain=v1", "-z"], cwd=root, check=True, capture_output=True, text=True,
                                 env={**GIT_ENV, "HOME": str(root)}).stdout
            self.assertTrue(raw.startswith(" M src.py\0"), raw)  # the unstaged record must come first to hit the strip bug
            handoff = Path(notes) / "handoff.md"  # outside the repo so it is not a status record
            handoff.write_text(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nProject: {root}\nBranch: main\nBaseline commit: {baseline}\n\n| src.py | edited |\n| missing-root.md | gone |\n")
            result = subprocess.run(["python3", str(SCRIPT), "--json", str(handoff)], text=True, capture_output=True)
            data = json.loads(result.stdout)
            self.assertEqual(data["files_changed"], ["old.py", "src.py", "zz_new.py"])
            self.assertEqual(data["referenced_files_missing"], ["missing-root.md"])
            self.assertEqual(data["staleness_level"], "SLIGHTLY_STALE")
            self.assertEqual(result.returncode, 0)

    def test_help_documents_exit_codes(self):
        result = subprocess.run(["python3", str(SCRIPT), "--help"], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("exit codes:", result.stdout)
        self.assertIn("--json", result.stdout)


if __name__ == "__main__":
    unittest.main()
