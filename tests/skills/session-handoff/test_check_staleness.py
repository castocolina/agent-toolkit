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
            self.assertIn("Handoff file not found", result.stdout)


if __name__ == "__main__":
    unittest.main()
