import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import build_plugins  # noqa: E402


class BuildPluginExcludesTest(unittest.TestCase):
    def test_evals_tests_and_pycache_are_not_copied(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill = root / "skills" / "s"
            for rel in ("SKILL.md", "scripts/x.sh", "references/r.md",
                        "evals/evals.json", "evals/files/a.txt",
                        "tests/t.sh", "__pycache__/c.pyc"):
                f = skill / rel
                f.parent.mkdir(parents=True, exist_ok=True)
                f.write_text("x")
            dist = root / "dist" / "plugins"

            count = build_plugins.build_plugin(
                root, dist, {"name": "p", "skills": ["./skills/s"]})

            out = dist / "p" / "skills" / "s"
            for rel in ("SKILL.md", "scripts/x.sh", "references/r.md"):
                self.assertTrue((out / rel).is_file(), rel)
            for rel in ("evals", "tests", "__pycache__"):
                self.assertFalse((out / rel).exists(), rel)
            self.assertEqual(count, 3)


if __name__ == "__main__":
    unittest.main()
