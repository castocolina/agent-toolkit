import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[3] / "skills/session-handoff/scripts/create_handoff.py"
GIT_ENV = {**os.environ, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull}


class CreateHandoffTests(unittest.TestCase):
    def test_explicit_predecessor_requires_exact_filename(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            handoffs = root / ".claude/handoffs"
            handoffs.mkdir(parents=True)
            predecessor = handoffs / "2026-01-20-101112-auth.md"
            predecessor.write_text("# Handoff: Auth\n")
            sys_path = str(SCRIPT)
            result = subprocess.run(
                ["python3", sys_path, "next", "--continues-from", "auth.md"],
                cwd=root, text=True, capture_output=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("exact filename", result.stderr)
            self.assertEqual(len(list(handoffs.glob("*-next.md"))), 0)

    def test_creates_scaffold_with_project_git_metadata_and_slug(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-b", "test-branch"], cwd=root, check=True, capture_output=True, env={**GIT_ENV, "HOME": str(root)})
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True, env={**GIT_ENV, "HOME": str(root)})
            subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True, env={**GIT_ENV, "HOME": str(root)})
            (root / "README.md").write_text("fixture\n")
            subprocess.run(["git", "add", "README.md"], cwd=root, check=True, env={**GIT_ENV, "HOME": str(root)})
            subprocess.run(["git", "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null", "commit", "-m", "initial fixture commit"], cwd=root, check=True, capture_output=True, env={**GIT_ENV, "HOME": str(root)})

            result = subprocess.run(["python3", str(SCRIPT), "My_Task"], cwd=root, text=True, capture_output=True, check=True)
            matches = list((root / ".claude/handoffs").glob("*-my-task.md"))
            self.assertEqual(len(matches), 1)
            content = matches[0].read_text()
            self.assertIn(f"Project: {root}", content)
            self.assertIn("Branch: test-branch", content)
            self.assertIn("initial fixture commit", content)
            self.assertIn("Created handoff document:", result.stdout)
            self.assertRegex(matches[0].name, r"^\d{4}-\d{2}-\d{2}-\d{6}-my-task\.md$")
            self.assertIn("[TODO:", content)


if __name__ == "__main__":
    unittest.main()
