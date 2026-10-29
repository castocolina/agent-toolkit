import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[3] / "skills/session-handoff/scripts/validate_handoff.py"

VALID = """# Handoff: Fixture

## Current State Summary
The implementation is complete and the project is ready for the next development session with relevant context documented.

## Context for Resuming Agent

### Important Context
Use the existing project conventions and verify current state before making changes. The working tree and requirements have been reviewed.

## Pending Work

### Immediate Next Steps
1. Review the repository status before continuing.
2. Run the relevant tests.

## Codebase Understanding

### Architecture Overview
A small fixture project.

### Critical Files
None.

## Work Completed

### Files Modified
None.

### Decisions Made
No decisions pending.

### Assumptions Made
The fixture represents the project state.

### Potential Gotchas
No known issues.
"""


class ValidateHandoffTests(unittest.TestCase):
    def test_accepts_complete_handoff_without_secrets(self):
        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp) / "handoff.md"
            file.write_text(VALID)
            result = subprocess.run(["python3", str(SCRIPT), str(file)], text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Quality Score: 100/100", result.stdout)
            self.assertIn("[PASS] All required sections complete", result.stdout)
            self.assertIn("[PASS] No TODO placeholders remaining", result.stdout)
            self.assertIn("Verdict: READY for handoff", result.stdout)

    def test_rejects_high_scoring_handoff_with_missing_required_sections(self):
        with tempfile.TemporaryDirectory() as tmp:
            handoff = Path(tmp) / "handoff.md"
            handoff.write_text("# Notes\\n\\n" + "Useful detail. " * 100)
            result = subprocess.run(["python3", str(SCRIPT), str(handoff)], text=True, capture_output=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn("NEEDS WORK", result.stdout)

    def test_rejects_handoff_containing_secret(self):
        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp) / "handoff.md"
            file.write_text(VALID + '\napi_key = "abcdefghijklmnop"\n')
            result = subprocess.run(["python3", str(SCRIPT), str(file)], text=True, capture_output=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn("API key", result.stdout)
            self.assertIn("Verdict: BLOCKED", result.stdout)


if __name__ == "__main__":
    unittest.main()
