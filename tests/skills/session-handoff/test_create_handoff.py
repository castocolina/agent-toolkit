import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime
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

    def test_same_timestamp_collision_never_overwrites(self):
        sys.dont_write_bytecode = True  # no __pycache__ inside the skill directory
        spec = importlib.util.spec_from_file_location("create_handoff", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        class FixedClock(datetime):
            @classmethod
            def now(cls, tz=None):
                return datetime(2026, 1, 2, 3, 4, 5)

        module.datetime = FixedClock
        with tempfile.TemporaryDirectory() as tmp:
            first = Path(module.generate_handoff(tmp, "auth"))
            first.write_text("filled in by the first agent\n")
            second = Path(module.generate_handoff(tmp, "auth"))
            self.assertEqual(first.name, "2026-01-02-030405-auth.md")
            self.assertEqual(second.name, "2026-01-02-030405-auth-2.md")
            self.assertEqual(first.read_text(), "filled in by the first agent\n")

    def test_json_output_and_help(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(["python3", str(SCRIPT), "--json", "task"], cwd=tmp, text=True, capture_output=True, check=True)
            data = json.loads(result.stdout)
            self.assertTrue(Path(data["path"]).is_file())
            self.assertIsNone(data["continues_from"])
        result = subprocess.run(["python3", str(SCRIPT), "--help"], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("exit codes:", result.stdout)


if __name__ == "__main__":
    unittest.main()
