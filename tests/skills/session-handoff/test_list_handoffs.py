import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[3] / "skills/session-handoff/scripts/list_handoffs.py"


class ListHandoffsTests(unittest.TestCase):
    def test_lists_handoffs_sorted_with_title_and_completion_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            handoffs = Path(tmp) / ".claude/handoffs"
            handoffs.mkdir(parents=True)
            (handoffs / "2025-01-01-120000-old.md").write_text("# Handoff: Older task\n\n[TODO: finish]\n")
            (handoffs / "2025-02-01-120000-new.md").write_text("# Handoff: New task\n\nDone.\n")
            result = subprocess.run(["python3", str(SCRIPT), tmp], text=True, capture_output=True, check=True)
            self.assertIn("Found 2 handoff(s)", result.stdout)
            self.assertIn("Title: New task", result.stdout)
            self.assertIn("Status: Complete", result.stdout)
            self.assertIn("Status: In Progress (1 TODOs)", result.stdout)
            self.assertLess(result.stdout.index("File: 2025-02"), result.stdout.index("File: 2025-01"))

    def test_reports_empty_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(["python3", str(SCRIPT), tmp], text=True, capture_output=True, check=True)
            self.assertIn("No handoffs found", result.stdout)


if __name__ == "__main__":
    unittest.main()
