import json
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

    def test_json_flags_missing_root_file_and_resolves_existing_one(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("fixture\n")
            handoffs = root / ".claude/handoffs"
            handoffs.mkdir(parents=True)
            (handoffs / "2026-01-01-120000-prev.md").write_text("# Handoff: prev\n")
            file = handoffs / "2026-01-02-120000-next.md"
            file.write_text(VALID + "\n| README.md | docs |\n| Makefile.am | gone |\n"
                            "Continues `2026-01-01-120000-prev.md`; see `https://example.com/guide.md`.\n")
            result = subprocess.run(["python3", str(SCRIPT), "--json", str(file)], text=True, capture_output=True)
            data = json.loads(result.stdout)
            self.assertEqual(data["files_missing"], ["Makefile.am"])
            self.assertEqual(data["files_verified"], 2)
            self.assertEqual(data["verdict"], "READY")
            self.assertEqual(result.returncode, 0)

    def test_missing_file_exits_2_on_stderr(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(["python3", str(SCRIPT), "--json", str(Path(tmp) / "nope.md")], text=True, capture_output=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn("File not found", result.stderr)
            self.assertEqual(result.stdout, "")

    def test_secret_patterns_cover_postgresql_and_skip_bearer_prose(self):
        import importlib.util, sys
        sys.dont_write_bytecode = True
        spec = importlib.util.spec_from_file_location("validate_handoff", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertTrue(module.scan_for_secrets("postgresql://billing:Tr0ub4dor@db:5432/x"))
        self.assertTrue(module.scan_for_secrets("Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.abc"))
        self.assertEqual(module.scan_for_secrets("Send the Bearer token in the header."), [])
        for url in ("redis://:s3cretpw@cache:6379/0", "amqp://app:s3cretpw@mq:5672/", "mongodb+srv://u:pw@c.example.net"):
            self.assertTrue(module.scan_for_secrets(url), url)
        for url in ("redis://cache:6379/0", "amqp://app@mq:5672/", "postgresql://app:<password>@db/x", "postgres://app:$DB_PASSWORD@db/x"):
            self.assertEqual(module.scan_for_secrets(url), [], url)

    def test_blocks_pem_private_keys_with_or_without_type_prefix(self):
        for kind in ("", "ENCRYPTED ", "RSA ", "EC ", "OPENSSH "):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as tmp:
                file = Path(tmp) / "handoff.md"
                file.write_text(VALID + f"\n-----BEGIN {kind}PRIVATE KEY-----\nMIIEVGVzdEtleU1hdGVyaWFs\n")
                result = subprocess.run(["python3", str(SCRIPT), str(file)], text=True, capture_output=True)
                self.assertEqual(result.returncode, 1)
                self.assertIn("Verdict: BLOCKED", result.stdout)
                self.assertNotIn("MIIEVGVz", result.stdout)

    def test_deleted_predecessor_link_is_reported_by_validation_and_staleness(self):
        with tempfile.TemporaryDirectory() as tmp:
            handoffs = Path(tmp) / ".claude/handoffs"
            handoffs.mkdir(parents=True)
            prev = "2026-01-01-120000-prev.md"
            file = handoffs / "2026-01-02-120000-next.md"
            file.write_text(VALID + f"\n- **Continues from**: [{prev}](./{prev})\n- [docs](https://example.com/a.md)\n")
            data = json.loads(subprocess.run(["python3", str(SCRIPT), "--json", str(file)], text=True, capture_output=True).stdout)
            self.assertEqual(data["files_missing"], [f"./{prev}"])
            staleness = SCRIPT.with_name("check_staleness.py")
            import importlib.util, sys
            sys.dont_write_bytecode = True
            sys.path.insert(0, str(SCRIPT.parent))
            spec = importlib.util.spec_from_file_location("check_staleness", staleness)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.assertEqual(module.parse_handoff_metadata(str(file))["modified_files"], [f"./{prev}"])

    def test_help_documents_exit_codes(self):
        result = subprocess.run(["python3", str(SCRIPT), "--help"], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("exit codes:", result.stdout)


if __name__ == "__main__":
    unittest.main()
