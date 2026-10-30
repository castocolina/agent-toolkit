"""Offline tests for scope-check.py: the deterministic path-scope gate.

The audit workflows let model agents edit the checkout; scope-check.py is the
host-side gate that rejects every change outside the audited scope before it is
applied or committed. These tests exercise the CLI end to end, never the
network. The generated-patch tests build their patches with real git.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / ".github" / "audit" / "scope-check.py"

DECISION = {"update": True, "type": "fix", "title": "t", "targets": ["x"], "rationale": "r"}


def write_decision(tmp: Path, targets) -> str:
    path = tmp / "decision.json"
    path.write_text(json.dumps({**DECISION, "targets": targets}), encoding="utf-8")
    return str(path)


def run_check(mode, input_text="", *extra, cwd=None):
    return subprocess.run([sys.executable, str(SCRIPT), mode, *extra],
                          input=input_text, capture_output=True, text=True, cwd=cwd)


class FixerScopeTests(unittest.TestCase):
    """fixer mode: only the decision targets, their tests and docs/audit."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)
        self.decision = write_decision(self.tmp, ["x"])

    def test_target_paths_are_accepted(self):
        paths = "skills/x/SKILL.md\ntests/skills/x/test-x.sh\ndocs/audit/notes.md\n"
        proc = run_check("fixer", paths, "--decision", self.decision)
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_out_of_scope_skill_is_rejected(self):
        proc = run_check("fixer", "skills/other/SKILL.md\n", "--decision", self.decision)
        self.assertEqual(proc.returncode, 1)
        self.assertIn("skills/other/SKILL.md", proc.stderr)

    def test_synced_skills_are_rejected_even_when_targeted(self):
        for targets, path in ((["gepetto"], "skills/gepetto/plugin/skill.md"),
                              (["x", "datadog-cli"], "skills/datadog-cli/scripts/sync.sh")):
            with self.subTest(targets=targets, path=path):
                decision = write_decision(self.tmp, targets)
                proc = run_check("fixer", path + "\n", "--decision", decision)
                self.assertEqual(proc.returncode, 1, path)
                self.assertIn(path, proc.stderr)

    def test_github_edit_is_rejected(self):
        proc = run_check("fixer", ".github/workflows/skill-audit.yaml\n", "--decision", self.decision)
        self.assertEqual(proc.returncode, 1)
        self.assertIn(".github/workflows/skill-audit.yaml", proc.stderr)

    def test_scripts_docs_plans_and_readme_are_rejected(self):
        for path in ("scripts/audit/audit.py", "docs/plans/5-scheduled-audit.md", "README.md"):
            with self.subTest(path=path):
                proc = run_check("fixer", path + "\n", "--decision", self.decision)
                self.assertEqual(proc.returncode, 1, path)

    def test_traversal_and_absolute_paths_are_rejected(self):
        for path in ("skills/x/../../etc/passwd", "/etc/passwd", "skills/x/../y.md"):
            with self.subTest(path=path):
                proc = run_check("fixer", path + "\n", "--decision", self.decision)
                self.assertEqual(proc.returncode, 1, path)

    def test_dist_requires_the_final_stage(self):
        proc = run_check("fixer", "dist/plugins/p/skills/x/SKILL.md\n", "--decision", self.decision)
        self.assertEqual(proc.returncode, 1)
        proc = run_check("fixer", "dist/plugins/p/skills/x/SKILL.md\n",
                         "--decision", self.decision, "--final-stage")
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_invalid_targets_are_rejected(self):
        for targets in (["../evil"], [], "x", ["ok", "a/b"]):
            with self.subTest(targets=targets):
                decision = write_decision(self.tmp, targets)
                proc = run_check("fixer", "skills/ok/a.md\n", "--decision", decision)
                self.assertEqual(proc.returncode, 1)

    def test_fixer_requires_a_decision_file(self):
        proc = run_check("fixer", "skills/x/a.md\n")
        self.assertEqual(proc.returncode, 2, proc.stderr)


class RepairsScopeTests(unittest.TestCase):
    """repairs mode: the Task 2a structural scope only."""

    def test_structural_paths_are_accepted(self):
        paths = "\n".join([
            "skills/agentskills-research/scripts/fetch-spec.sh",
            "skills/agentskills-research/SKILL.md",
            "skills/skill-judge/references/agentskills/specification.md",
            "skills/skill-judge/references/rubric.md",
            "skills/skill-judge/evals/evals.json",
            "tests/skills/agentskills-research/test-fetch-spec.sh",
            "docs/audit/ci-spike.md",
        ]) + "\n"
        proc = run_check("repairs", paths)
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_out_of_scope_paths_are_rejected(self):
        for path in ("skills/skill-judge/SKILL.md", "skills/x/SKILL.md", "scripts/audit/audit.py",
                     "docs/plans/5-scheduled-audit.md", "README.md", "merged/merged.json"):
            with self.subTest(path=path):
                proc = run_check("repairs", path + "\n")
                self.assertEqual(proc.returncode, 1, path)
                self.assertIn(path, proc.stderr)

    def test_dist_requires_the_final_stage(self):
        proc = run_check("repairs", "dist/plugins/p/skills/skill-judge/SKILL.md\n")
        self.assertEqual(proc.returncode, 1)
        proc = run_check("repairs", "dist/plugins/p/skills/skill-judge/SKILL.md\n", "--final-stage")
        self.assertEqual(proc.returncode, 0, proc.stderr)


class NumstatParsingTests(unittest.TestCase):
    """git apply --numstat output: renames, quoting, binary and mode-only rows."""

    def test_rename_checks_both_paths(self):
        numstat = "1\t0\tskills/x/{old.md => new.md}\n"
        proc = run_check("repairs", numstat, "--format", "numstat")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("skills/x/old.md", proc.stderr)
        self.assertIn("skills/x/new.md", proc.stderr)

    def test_rename_out_of_scope_only(self):
        numstat = ("2\t1\ttests/skills/agentskills-research/{a.sh => b.sh}\n"
                   "1\t0\tscripts/audit/audit.py\n")
        proc = run_check("repairs", numstat, "--format", "numstat")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("scripts/audit/audit.py", proc.stderr)
        self.assertNotIn("a.sh", proc.stderr)

    def test_quoted_and_binary_paths(self):
        numstat = '-\t-\t"skills/agentskills-research/weird \\"name\\twith tab.md"\n5\t2\tskills/agentskills-research/bin.md\n'
        proc = run_check("repairs", numstat, "--format", "numstat")
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_top_level_rename_form(self):
        numstat = "1\t1\tskills/agentskills-research/a.md => skills/agentskills-research/b.md\n"
        proc = run_check("repairs", numstat, "--format", "numstat")
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_malformed_quoting_fails_closed(self):
        numstat = '1\t0\t"skills/agentskills-research/bad\\q.md"\n'
        proc = run_check("repairs", numstat, "--format", "numstat")
        self.assertEqual(proc.returncode, 1)


class PatchParsingTests(unittest.TestCase):
    """--patch reads paths, symlink creations and mode changes from the patch."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)

    def patch(self, text: str) -> str:
        path = self.tmp / "patch.diff"
        path.write_text(text, encoding="utf-8")
        return str(path)

    def test_symlink_creation_is_rejected(self):
        patch = (
            "diff --git a/skills/x/link b/skills/x/link\n"
            "new file mode 120000\n"
            "index 0000000..cad2309\n"
            "--- /dev/null\n"
            "+++ b/skills/x/link\n"
            "@@ -0,0 +1 @@\n"
            "+/etc/passwd\n"
        )
        proc = run_check("repairs", "", "--patch", self.patch(patch))
        self.assertEqual(proc.returncode, 1)
        self.assertIn("symlink", proc.stderr)
        self.assertIn("skills/x/link", proc.stderr)

    def test_out_of_scope_mode_change_is_rejected(self):
        patch = (
            "diff --git a/docs/other/a.sh b/docs/other/a.sh\n"
            "old mode 100644\n"
            "new mode 100755\n"
        )
        proc = run_check("repairs", "", "--patch", self.patch(patch))
        self.assertEqual(proc.returncode, 1)
        self.assertIn("mode change", proc.stderr)
        self.assertIn("docs/other/a.sh", proc.stderr)

    def test_in_scope_executable_bit_is_rejected(self):
        cases = {
            "new file mode 100755": (
                "diff --git a/skills/agentskills-research/run.sh b/skills/agentskills-research/run.sh\n"
                "new file mode 100755\n"),
            "old mode 100644 / new mode 100755": (
                "diff --git a/skills/agentskills-research/run.sh b/skills/agentskills-research/run.sh\n"
                "old mode 100644\nnew mode 100755\n"),
        }
        for label, patch in cases.items():
            with self.subTest(label=label):
                proc = run_check("repairs", "", "--patch", self.patch(patch))
                self.assertEqual(proc.returncode, 1, proc.stderr)
                self.assertIn("executable bit", proc.stderr)

    def test_in_scope_regular_file_to_symlink_is_rejected(self):
        patch = (
            "diff --git a/skills/agentskills-research/conv.md b/skills/agentskills-research/conv.md\n"
            "old mode 100644\n"
            "new mode 120000\n"
        )
        proc = run_check("repairs", "", "--patch", self.patch(patch))
        self.assertEqual(proc.returncode, 1)
        self.assertIn("symlink", proc.stderr)

    def test_in_scope_clearing_the_executable_bit_is_rejected(self):
        patch = (
            "diff --git a/skills/agentskills-research/run.sh b/skills/agentskills-research/run.sh\n"
            "old mode 100755\nnew mode 100644\n"
        )
        proc = run_check("repairs", "", "--patch", self.patch(patch))
        self.assertEqual(proc.returncode, 1)
        self.assertIn("mode change", proc.stderr)

    def test_in_scope_content_edit_without_mode_change_is_accepted(self):
        patch = (
            "diff --git a/skills/agentskills-research/run.sh b/skills/agentskills-research/run.sh\n"
            "index 1111111..2222222 100755\n"
            "--- a/skills/agentskills-research/run.sh\n"
            "+++ b/skills/agentskills-research/run.sh\n"
            "@@ -1 +1 @@\n"
            "-echo a\n"
            "+echo b\n"
        )
        proc = run_check("repairs", "", "--patch", self.patch(patch))
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_rename_in_patch_checks_both_paths(self):
        patch = (
            "diff --git a/skills/agentskills-research/a.md b/skills/agentskills-research/b.md\n"
            "similarity index 100%\n"
            "rename from skills/agentskills-research/a.md\n"
            "rename to skills/agentskills-research/b.md\n"
        )
        proc = run_check("repairs", "", "--patch", self.patch(patch))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        patch = patch.replace("skills/agentskills-research/b.md", "skills/other/b.md")
        proc = run_check("repairs", "", "--patch", self.patch(patch))
        self.assertEqual(proc.returncode, 1)
        self.assertIn("skills/other/b.md", proc.stderr)

    def test_header_only_patch_paths_are_checked(self):
        patch = (
            "diff --git a/scripts/audit/audit.py b/scripts/audit/audit.py\n"
            "--- a/scripts/audit/audit.py\n"
            "+++ b/scripts/audit/audit.py\n"
            "@@ -1 +1 @@\n"
            "-x\n"
            "+y\n"
        )
        proc = run_check("repairs", "", "--patch", self.patch(patch))
        self.assertEqual(proc.returncode, 1)
        self.assertIn("scripts/audit/audit.py", proc.stderr)

    def test_patch_without_a_diff_header_fails_closed(self):
        patch = "--- a/skills/agentskills-research/a.md\n+++ b/skills/agentskills-research/a.md\n"
        proc = run_check("repairs", "", "--patch", self.patch(patch))
        self.assertEqual(proc.returncode, 1)

    def test_unrecognized_header_line_fails_closed(self):
        patch = (
            "diff --git a/skills/agentskills-research/a.md b/skills/agentskills-research/a.md\n"
            "frobnicate 1\n"
        )
        proc = run_check("repairs", "", "--patch", self.patch(patch))
        self.assertEqual(proc.returncode, 1)
        self.assertIn("unrecognized", proc.stderr)

    def test_header_without_a_b_prefixes_fails_closed(self):
        patch = "diff --git skills/agentskills-research/a.md skills/agentskills-research/a.md\n"
        proc = run_check("repairs", "", "--patch", self.patch(patch))
        self.assertEqual(proc.returncode, 1)

    def test_quoted_header_paths_are_decoded_both_sides(self):
        patch = (
            'diff --git "a/scripts/we\\tird.sh" "b/scripts/we\\tird.sh"\n'
            "old mode 100644\n"
            "new mode 100755\n"
        )
        proc = run_check("repairs", "", "--patch", self.patch(patch))
        self.assertEqual(proc.returncode, 1)
        self.assertIn("scripts/we\tird.sh", proc.stderr)

    def test_marketplace_json_is_allowed_only_in_the_final_stage(self):
        decision = write_decision(self.tmp, ["x"])
        proc = run_check("fixer", ".claude-plugin/marketplace.json\n", "--decision", decision)
        self.assertEqual(proc.returncode, 1)
        proc = run_check("fixer", ".claude-plugin/marketplace.json\n", "--decision", decision,
                         "--final-stage")
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_numstat_input_and_patch_are_combined(self):
        patch = (
            "diff --git a/skills/other/link b/skills/other/link\n"
            "new file mode 120000\n"
        )
        numstat = "1\t0\tskills/other/link\n"
        proc = run_check("repairs", numstat, "--format", "numstat", "--patch", self.patch(patch))
        self.assertEqual(proc.returncode, 1)
        self.assertIn("symlink", proc.stderr)


@unittest.skipUnless(shutil.which("git"), "git is required for the generated-patch tests")
class GitGeneratedPatchTests(unittest.TestCase):
    """Patches produced by real git, so the quoting and mode lines are git's own."""

    GIT = ["git", "-c", "core.quotePath=true", "-c", "diff.noprefix=false",
           "-c", "diff.mnemonicPrefix=false", "-c", "color.diff=never"]

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.repo = Path(self._tmp.name) / "repo"
        self.repo.mkdir()
        self.out = Path(self._tmp.name) / "out"
        self.out.mkdir()
        self.git("init", "-q")
        self.git("config", "user.name", "scope-test")
        self.git("config", "user.email", "scope-test@example.invalid")
        (self.repo / "skills" / "agentskills-research").mkdir(parents=True)
        (self.repo / "scripts").mkdir()
        (self.repo / "skills" / "agentskills-research" / "keep.md").write_text("keep\n", encoding="utf-8")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "base")

    def git(self, *args) -> str:
        return subprocess.run([*self.GIT, *args], cwd=self.repo, check=True,
                              capture_output=True, text=True).stdout

    def staged_patch(self) -> Path:
        self.git("add", "-A")
        text = self.git("diff", "--cached", "--binary", "--no-color", "--no-ext-diff")
        path = self.out / "staged.diff"
        path.write_text(text, encoding="utf-8")
        return path

    def check_repairs(self, patch: Path):
        return run_check("repairs", "", "--patch", str(patch))

    def test_quoted_path_symlink_addition_is_rejected(self):
        link = self.repo / "skills" / "agentskills-research" / "we\tird"
        os.symlink("/etc/passwd", link)
        patch = self.staged_patch()
        self.assertIn('"a/skills/agentskills-research/we\\tird"', patch.read_text(encoding="utf-8"),
                      "git must quote the tab in the header for this test to mean anything")
        proc = self.check_repairs(patch)
        self.assertEqual(proc.returncode, 1, proc.stderr)
        self.assertIn("symlink", proc.stderr)
        self.assertIn("skills/agentskills-research/we\tird", proc.stderr)

    def test_quoted_out_of_scope_path_is_reported_decoded(self):
        name = "caf\u00e9\tx.sh"
        (self.repo / "scripts" / name).write_text("echo\n", encoding="utf-8")
        patch = self.staged_patch()
        proc = self.check_repairs(patch)
        self.assertEqual(proc.returncode, 1, proc.stderr)
        self.assertIn(f"scripts/{name}: path is never editable", proc.stderr)

    def test_quoted_pure_mode_change_is_rejected(self):
        # A chmod with no content change produces no ---/+++ lines: only the
        # quoted header carries the path, which is exactly the fail-open case.
        target = self.repo / "skills" / "agentskills-research" / "ex\tec.sh"
        target.write_text("echo\n", encoding="utf-8")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "exec base")
        target.chmod(0o755)
        patch = self.staged_patch()
        self.assertIn("old mode 100644", patch.read_text(encoding="utf-8"))
        proc = self.check_repairs(patch)
        self.assertEqual(proc.returncode, 1, proc.stderr)
        self.assertIn("executable bit", proc.stderr)
        self.assertIn("skills/agentskills-research/ex\tec.sh", proc.stderr)

    def test_quoted_in_scope_content_edit_is_accepted(self):
        target = self.repo / "skills" / "agentskills-research" / "we\tird.md"
        target.write_text("first\n", encoding="utf-8")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "quoted base")
        target.write_text("second\n", encoding="utf-8")
        proc = self.check_repairs(self.staged_patch())
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_retargeting_an_existing_symlink_is_rejected(self):
        link = self.repo / "skills" / "agentskills-research" / "link.md"
        os.symlink("keep.md", link)
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "link base")
        link.unlink()
        os.symlink("/etc/passwd", link)
        patch = self.staged_patch()
        self.assertIn("120000", patch.read_text(encoding="utf-8"))
        proc = self.check_repairs(patch)
        self.assertEqual(proc.returncode, 1, proc.stderr)
        self.assertIn("symlink", proc.stderr)

    def test_regular_file_to_symlink_conversion_is_rejected(self):
        target = self.repo / "skills" / "agentskills-research" / "conv.md"
        target.write_text("text\n", encoding="utf-8")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "conv base")
        target.unlink()
        os.symlink("/etc/passwd", target)
        proc = self.check_repairs(self.staged_patch())
        self.assertEqual(proc.returncode, 1, proc.stderr)
        self.assertIn("symlink", proc.stderr)


class PorcelainTests(unittest.TestCase):
    """git status --porcelain=v2 input: modes, symlinks and untracked files."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.ws = Path(self._tmp.name)
        self.decision = write_decision(self.ws, ["x"])
        (self.ws / "skills" / "x").mkdir(parents=True)
        (self.ws / "skills" / "x" / "a.md").write_text("a\n", encoding="utf-8")

    def run_porcelain(self, status_text):
        return run_check("fixer", status_text, "--decision", self.decision,
                         "--format", "porcelain-v2", "--worktree", str(self.ws))

    def test_staged_symlink_is_rejected(self):
        status = ("1 A. N... 000000 120000 120000 "
                  "0000000000000000000000000000000000000000 cad23091 skills/x/escape\n")
        proc = self.run_porcelain(status)
        self.assertEqual(proc.returncode, 1)
        self.assertIn("symlink", proc.stderr)

    def test_worktree_symlink_is_rejected(self):
        status = ("1 .T N... 100644 100644 120000 "
                  "45b983be36b73c0788dc9cbcb76cbb80fc7bb057 45b983be36b73c0788dc9cbcb76cbb80fc7bb057 skills/x/a.md\n")
        proc = self.run_porcelain(status)
        self.assertEqual(proc.returncode, 1)
        self.assertIn("symlink", proc.stderr)

    def test_untracked_symlink_is_rejected(self):
        os.symlink("/etc/passwd", self.ws / "skills" / "x" / "evil")
        proc = self.run_porcelain("? skills/x/evil\n")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("symlink", proc.stderr)

    def test_out_of_scope_mode_change_is_rejected(self):
        status = ("1 .M N... 100644 100644 100755 "
                  "45b983be36b73c0788dc9cbcb76cbb80fc7bb057 45b983be36b73c0788dc9cbcb76cbb80fc7bb057 docs/other/x.md\n")
        proc = self.run_porcelain(status)
        self.assertEqual(proc.returncode, 1)
        self.assertIn("mode change", proc.stderr)

    def test_in_scope_mode_change_to_executable_is_rejected(self):
        status = ("1 .M N... 100644 100644 100755 "
                  "45b983be36b73c0788dc9cbcb76cbb80fc7bb057 45b983be36b73c0788dc9cbcb76cbb80fc7bb057 skills/x/a.md\n")
        proc = self.run_porcelain(status)
        self.assertEqual(proc.returncode, 1)
        self.assertIn("executable bit", proc.stderr)

    def test_in_scope_new_executable_file_is_rejected(self):
        status = ("1 A. N... 000000 100755 100755 "
                  "0000000000000000000000000000000000000000 cad23091 skills/x/run.sh\n")
        proc = self.run_porcelain(status)
        self.assertEqual(proc.returncode, 1)
        self.assertIn("executable bit", proc.stderr)

    def test_untracked_executable_file_is_rejected(self):
        path = self.ws / "skills" / "x" / "run.sh"
        path.write_text("#!/bin/sh\n", encoding="utf-8")
        path.chmod(0o755)
        proc = self.run_porcelain("? skills/x/run.sh\n")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("executable bit", proc.stderr)

    def test_in_scope_edit_of_an_existing_executable_is_accepted(self):
        status = ("1 .M N... 100755 100755 100755 "
                  "45b983be36b73c0788dc9cbcb76cbb80fc7bb057 45b983be36b73c0788dc9cbcb76cbb80fc7bb057 skills/x/run.sh\n")
        proc = self.run_porcelain(status)
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_rename_records_check_both_paths(self):
        status = ("2 R. N... 100644 100644 100644 "
                  "45b983be36b73c0788dc9cbcb76cbb80fc7bb057 45b983be36b73c0788dc9cbcb76cbb80fc7bb057 "
                  "R100 skills/x/other.md\tskills/x/a.md\n")
        proc = self.run_porcelain(status)
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_staged_baseline_is_skipped_with_skip_staged(self):
        # Repairs are staged and validated before the fixer runs; with
        # --skip-staged the index-only entries (worktree clean, Y == '.') are
        # the baseline, so only the fixer's own worktree edits are checked.
        status = ("1 M. N... 100644 100644 100644 "
                  "45b983be36b73c0788dc9cbcb76cbb80fc7bb057 78981922613b2afb6025042ff6bd878ac1994e85 skills/skill-judge/references/rubric.md\n")
        proc = run_check("fixer", status, "--decision", self.decision,
                         "--format", "porcelain-v2", "--worktree", str(self.ws), "--skip-staged")
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def run_decision(self, status_text, *extra):
        return run_check("decision", status_text, "--format", "porcelain-v2",
                         "--worktree", str(self.ws), *extra)

    STAGED_REPAIR = ("1 M. N... 100644 100644 100644 "
                     "45b983be36b73c0788dc9cbcb76cbb80fc7bb057 78981922613b2afb6025042ff6bd878ac1994e85 "
                     "skills/skill-judge/references/rubric.md\n")

    def test_merge_sequence_accepts_staged_repairs_plus_the_decision(self):
        # Non-empty repairs are staged before the snapshot; the model only writes decision.json.
        proc = self.run_decision(self.STAGED_REPAIR + "? decision.json\n", "--skip-staged")
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_merge_sequence_without_skip_staged_rejects_the_repairs(self):
        proc = self.run_decision(self.STAGED_REPAIR + "? decision.json\n")
        self.assertEqual(proc.returncode, 1)

    def test_merge_sequence_rejects_an_extra_model_edit(self):
        status = (self.STAGED_REPAIR + "? decision.json\n"
                  "1 .M N... 100644 100644 100644 "
                  "45b983be36b73c0788dc9cbcb76cbb80fc7bb057 45b983be36b73c0788dc9cbcb76cbb80fc7bb057 "
                  "skills/x/a.md\n")
        proc = self.run_decision(status, "--skip-staged")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("skills/x/a.md", proc.stderr)

    def test_staged_baseline_is_checked_without_skip_staged(self):
        status = ("1 M. N... 100644 100644 100644 "
                  "45b983be36b73c0788dc9cbcb76cbb80fc7bb057 78981922613b2afb6025042ff6bd878ac1994e85 skills/skill-judge/references/rubric.md\n")
        proc = run_check("fixer", status, "--decision", self.decision,
                         "--format", "porcelain-v2", "--worktree", str(self.ws))
        self.assertEqual(proc.returncode, 1)

    def test_fixer_edit_on_top_of_staged_repair_is_rejected(self):
        status = ("1 MM N... 100644 100644 100644 "
                  "45b983be36b73c0788dc9cbcb76cbb80fc7bb057 78981922613b2afb6025042ff6bd878ac1994e85 skills/skill-judge/references/rubric.md\n")
        proc = run_check("fixer", status, "--decision", self.decision,
                         "--format", "porcelain-v2", "--worktree", str(self.ws), "--skip-staged")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("skills/skill-judge/references/rubric.md", proc.stderr)

    def test_unknown_status_record_fails_closed(self):
        proc = self.run_porcelain("u UU N... 100644 100644 100644 100644 a b skills/x/a.md\n")
        self.assertEqual(proc.returncode, 1)

    def test_plain_edits_are_accepted(self):
        status = ("1 .M N... 100644 100644 100644 "
                  "45b983be36b73c0788dc9cbcb76cbb80fc7bb057 45b983be36b73c0788dc9cbcb76cbb80fc7bb057 skills/x/a.md\n"
                  "? skills/x/new.md\n"
                  "? docs/audit/note.md\n")
        proc = self.run_porcelain(status)
        self.assertEqual(proc.returncode, 0, proc.stderr)


class ReviewModeTests(unittest.TestCase):
    """review mode (PR review gate): NUL-separated numstat -z records, allowed and denied policy."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.empty_patch = Path(self._tmp.name) / "empty.diff"
        self.empty_patch.write_text("", encoding="utf-8")

    def review(self, text, *extra, patch=None):
        return run_check("review", text, "--format", "numstat-z",
                         "--patch", str(patch or self.empty_patch), *extra)

    def accepted(self, *paths):
        text = "".join(f"1\t0\t{p}\0" for p in paths)
        proc = self.review(text)
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def rejected(self, text, *needles):
        proc = self.review(text)
        self.assertEqual(proc.returncode, 1, proc.stderr)
        for needle in needles:
            self.assertIn(needle, proc.stderr)

    def test_scope_review_mode_allows_and_denies(self):
        self.test_allowed_paths_are_accepted()
        self.test_denied_paths_are_rejected()
        self.test_everything_else_is_out_of_scope()

    def test_allowed_paths_are_accepted(self):
        self.accepted("skills/x/SKILL.md", "skills/brand-new/evals/evals.json",
                      "tests/skills/x/test-x.sh", "docs/audit/ci-spike.md",
                      "dist/plugins/p/skills/x/SKILL.md", ".claude-plugin/marketplace.json")

    def test_denied_paths_are_rejected(self):
        for path in (".github/workflows/skill-audit.yaml", ".github/audit/scope-check.py",
                     "scripts/audit/audit.py", "README.md", "docs/plans/2026-10-24-05-scheduled-audit.md",
                     "skills/gepetto/plugin/skill.md", "skills/datadog-cli/scripts/sync.sh"):
            with self.subTest(path=path):
                self.rejected(f"1\t0\t{path}\0", path)

    def test_everything_else_is_out_of_scope(self):
        for path in ("docs/other.md", ".claude-plugin/plugin.json", "root.txt", "package.json"):
            with self.subTest(path=path):
                self.rejected(f"1\t0\t{path}\0", path)

    def test_numstat_z_rename_brace_form(self):
        self.accepted("skills/x/{old.md => new.md}")
        self.rejected("1\t0\tscripts/{a.sh => b.sh}\0", "scripts/a.sh", "scripts/b.sh")

    def test_rename_pair_checks_both_names(self):
        self.rejected("1\t0\t\0scripts/evil.sh\0skills/x/b.md\0", "scripts/evil.sh")
        self.rejected("1\t0\t\0skills/x/a.md\0.github/workflows/evil.yaml\0", ".github/workflows/evil.yaml")
        proc = self.review("1\t0\t\0skills/x/a.md\0skills/x/b.md\0")
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_quoting_is_not_applied_in_z_mode(self):
        self.rejected('1\t0\tscripts/"q\\tab.sh\0', 'scripts/"q\\tab.sh')
        self.rejected("1\t0\tscripts/we\tird.sh\0", "scripts/we\tird.sh")
        self.accepted("skills/x/caf\u00e9 \"q\".md")

    def test_truncated_or_malformed_records_fail_closed(self):
        for text in ("1\t0\t\0skills/x/a.md\0", "garbage\0", "1 0 skills/x/a.md\0", "x\t0\tskills/x/a.md\0"):
            with self.subTest(text=text):
                proc = self.review(text)
                self.assertEqual(proc.returncode, 1)

    def test_empty_input_is_in_scope(self):
        proc = self.review("")
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_review_mode_needs_no_decision(self):
        proc = self.review("1\t0\tskills/x/a.md\0")
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_review_requires_numstat_z_and_a_patch(self):
        proc = run_check("review", "1\t0\tskills/x/a.md\0", "--format", "numstat")
        self.assertEqual(proc.returncode, 2, proc.stderr)
        proc = run_check("review", "1\t0\tskills/x/a.md\0", "--format", "numstat-z")
        self.assertEqual(proc.returncode, 2, proc.stderr)

    def test_patch_symlink_and_mode_problems_are_rejected_in_review(self):
        patch = Path(self._tmp.name) / "p.diff"
        cases = {
            "symlink in dist": ("diff --git a/dist/p/l b/dist/p/l\nnew file mode 120000\n", "dist/p/l"),
            "exec bit in skills": ("diff --git a/skills/x/r.sh b/skills/x/r.sh\nold mode 100644\nnew mode 100755\n",
                                   "skills/x/r.sh"),
            "mode change in docs": ("diff --git a/docs/audit/d.md b/docs/audit/d.md\nold mode 100644\nnew mode 100755\n",
                                    "docs/audit/d.md"),
        }
        for label, (text, path) in cases.items():
            with self.subTest(label=label):
                patch.write_text(text, encoding="utf-8")
                proc = self.review(f"1\t0\t{path}\0", patch=patch)
                self.assertEqual(proc.returncode, 1, proc.stderr)
                self.assertIn(path, proc.stderr)

    def test_patch_quoted_header_is_decoded_in_review(self):
        patch = Path(self._tmp.name) / "q.diff"
        patch.write_text('diff --git "a/scripts/we\\tird.sh" "b/scripts/we\\tird.sh"\n'
                         "old mode 100644\nnew mode 100755\n", encoding="utf-8")
        proc = self.review("", patch=patch)
        self.assertEqual(proc.returncode, 1, proc.stderr)
        self.assertIn("scripts/we\tird.sh", proc.stderr)


@unittest.skipUnless(shutil.which("git"), "git is required for the generated-diff tests")
class GitGeneratedReviewTests(unittest.TestCase):
    """review mode fed by real `git diff` output, as the review workflow runs it."""

    GIT = ["git", "-c", "core.quotePath=true", "-c", "diff.noprefix=false",
           "-c", "diff.mnemonicPrefix=false", "-c", "color.diff=never"]

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.repo = Path(self._tmp.name) / "repo"
        self.repo.mkdir()
        self.out = Path(self._tmp.name) / "out"
        self.out.mkdir()
        self.git("init", "-q")
        self.git("config", "user.name", "scope-test")
        self.git("config", "user.email", "scope-test@example.invalid")
        files = {
            "skills/x/SKILL.md": "s\n",
            "skills/x/old.md": "old\n",
            "skills/x/run.sh": "echo a\n",
            "skills/x/tool.sh": "echo t\n",
            "skills/x/blob.bin": b"\x00\x01\x02",
            "skills/gepetto/plugin.md": "g\n",
            "skills/datadog-cli/cli.md": "d\n",
            "tests/skills/x/test-x.sh": "t\n",
            "docs/audit/a.md": "a\n",
            "docs/other.md": "o\n",
            "docs/plans/p.md": "p\n",
            "scripts/audit/run.sh": "r\n",
            "README.md": "readme\n",
            ".github/workflows/w.yaml": "w\n",
            ".claude-plugin/marketplace.json": "{}\n",
            "dist/plugins/p/a.md": "dist\n",
            "root.txt": "root\n",
        }
        for rel, content in files.items():
            path = self.repo / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content if isinstance(content, bytes) else content.encode())
        for rel in ("skills/x/run.sh", "skills/x/tool.sh"):
            (self.repo / rel).chmod(0o755)
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "base")
        self.base = self.git("rev-parse", "HEAD").strip()

    def git(self, *args) -> str:
        return subprocess.run([*self.GIT, *args], cwd=self.repo, check=True,
                              capture_output=True, text=True).stdout

    def commit(self, message="change"):
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message)

    def review(self):
        """Run review mode on the range base...HEAD, the way the workflow does."""
        numstat = subprocess.run([*self.GIT, "diff", "--numstat", "-z", "-M", f"{self.base}...HEAD"],
                                 cwd=self.repo, check=True, capture_output=True, text=True).stdout
        patch = subprocess.run([*self.GIT, "diff", "--binary", "-M", "--no-color", "--no-ext-diff",
                                f"{self.base}...HEAD"],
                               cwd=self.repo, check=True, capture_output=True, text=True).stdout
        path = self.out / "review.diff"
        path.write_text(patch, encoding="utf-8")
        return run_check("review", numstat, "--format", "numstat-z", "--patch", str(path))

    def test_in_scope_edits_are_accepted(self):
        (self.repo / "skills/x/SKILL.md").write_text("new\n", encoding="utf-8")
        (self.repo / "skills/brand-new/SKILL.md").parent.mkdir(parents=True)
        (self.repo / "skills/brand-new/SKILL.md").write_text("n\n", encoding="utf-8")
        (self.repo / "tests/skills/x/test-x.sh").write_text("t2\n", encoding="utf-8")
        (self.repo / "docs/audit/a.md").write_text("a2\n", encoding="utf-8")
        (self.repo / "dist/plugins/p/a.md").write_text("d2\n", encoding="utf-8")
        (self.repo / ".claude-plugin/marketplace.json").write_text("{\"a\": 1}\n", encoding="utf-8")
        (self.repo / "skills/x/blob.bin").write_bytes(b"\x09\x08\x07\x00")
        self.commit()
        proc = self.review()
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_in_scope_rename_is_accepted(self):
        self.git("mv", "skills/x/old.md", "skills/x/renamed.md")
        self.commit()
        proc = self.review()
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_rename_out_of_scope_is_rejected_on_either_side(self):
        self.git("mv", "skills/x/old.md", "scripts/evil.sh")
        self.commit()
        proc = self.review()
        self.assertEqual(proc.returncode, 1)
        self.assertIn("scripts/evil.sh", proc.stderr)
        self.assertIn("path is never editable", proc.stderr)

    def test_rename_from_out_of_scope_into_allowed_is_rejected(self):
        self.git("mv", "docs/other.md", "skills/x/moved.md")
        self.commit()
        proc = self.review()
        self.assertEqual(proc.returncode, 1)
        self.assertIn("docs/other.md", proc.stderr)

    def test_rename_into_github_is_rejected(self):
        self.git("mv", "skills/x/old.md", ".github/workflows/evil.yaml")
        self.commit()
        proc = self.review()
        self.assertEqual(proc.returncode, 1)
        self.assertIn(".github/workflows/evil.yaml", proc.stderr)

    def test_symlink_creation_is_rejected(self):
        os.symlink("/etc/passwd", self.repo / "skills/x/escape")
        self.commit()
        proc = self.review()
        self.assertEqual(proc.returncode, 1)
        self.assertIn("symlink", proc.stderr)
        self.assertIn("skills/x/escape", proc.stderr)

    def test_symlink_inside_dist_is_still_rejected(self):
        (self.repo / "dist/plugins/p/a.md").unlink()
        os.symlink("/etc/passwd", self.repo / "dist/plugins/p/a.md")
        self.commit()
        proc = self.review()
        self.assertEqual(proc.returncode, 1)
        self.assertIn("symlink", proc.stderr)

    def test_symlink_retarget_and_conversion_are_rejected(self):
        os.symlink("SKILL.md", self.repo / "skills/x/link.md")
        self.commit("link")
        self.base = self.git("rev-parse", "HEAD").strip()  # only the retarget is in range
        (self.repo / "skills/x/link.md").unlink()
        os.symlink("/etc/passwd", self.repo / "skills/x/link.md")
        self.commit("retarget")
        proc = self.review()
        self.assertEqual(proc.returncode, 1)
        self.assertIn("symlink", proc.stderr)

    def test_regular_file_to_symlink_is_rejected(self):
        (self.repo / "skills/x/old.md").unlink()
        os.symlink("/etc/passwd", self.repo / "skills/x/old.md")
        self.commit()
        proc = self.review()
        self.assertEqual(proc.returncode, 1)
        self.assertIn("symlink", proc.stderr)

    def test_executable_bit_set_is_rejected(self):
        (self.repo / "skills/x/old.md").chmod(0o755)
        self.commit()
        proc = self.review()
        self.assertEqual(proc.returncode, 1)
        self.assertIn("executable bit", proc.stderr)

    def test_executable_bit_cleared_is_rejected(self):
        (self.repo / "skills/x/tool.sh").chmod(0o644)
        self.commit()
        proc = self.review()
        self.assertEqual(proc.returncode, 1)
        self.assertIn("executable bit", proc.stderr)
        self.assertIn("skills/x/tool.sh", proc.stderr)

    def test_mode_change_outside_scope_is_rejected(self):
        (self.repo / "docs/other.md").chmod(0o755)
        self.commit()
        proc = self.review()
        self.assertEqual(proc.returncode, 1)
        self.assertIn("docs/other.md", proc.stderr)

    def test_quoted_names_are_decoded_for_denied_and_allowed_paths(self):
        for name in ("we\tird.sh", 'q"uote.sh', "caf\u00e9.sh"):
            with self.subTest(name=name):
                (self.repo / "scripts" / name).write_text("x\n", encoding="utf-8")
        self.commit()
        proc = self.review()
        self.assertEqual(proc.returncode, 1)
        self.assertIn("scripts/we\tird.sh", proc.stderr)
        self.assertIn('scripts/q"uote.sh', proc.stderr)
        self.assertIn("scripts/caf\u00e9.sh", proc.stderr)

    def test_quoted_in_scope_name_is_accepted(self):
        (self.repo / "skills/x/we\tird \"name\".md").write_text("x\n", encoding="utf-8")
        self.commit()
        proc = self.review()
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_denied_paths_are_rejected(self):
        (self.repo / "skills/gepetto/plugin.md").write_text("x\n", encoding="utf-8")
        (self.repo / "skills/datadog-cli/cli.md").write_text("x\n", encoding="utf-8")
        (self.repo / "scripts/audit/run.sh").write_text("x\n", encoding="utf-8")
        (self.repo / ".github/workflows/w.yaml").write_text("x\n", encoding="utf-8")
        (self.repo / "README.md").write_text("x\n", encoding="utf-8")
        (self.repo / "docs/plans/p.md").write_text("x\n", encoding="utf-8")
        self.commit()
        proc = self.review()
        self.assertEqual(proc.returncode, 1)
        for path in ("skills/gepetto/plugin.md", "skills/datadog-cli/cli.md", "scripts/audit/run.sh",
                     ".github/workflows/w.yaml", "README.md", "docs/plans/p.md"):
            self.assertIn(path, proc.stderr)

    def test_deleting_an_audit_script_is_rejected(self):
        self.git("rm", "-q", "scripts/audit/run.sh")
        self.commit()
        proc = self.review()
        self.assertEqual(proc.returncode, 1)
        self.assertIn("scripts/audit/run.sh", proc.stderr)

    def test_binary_edit_in_scope_is_accepted(self):
        (self.repo / "skills/x/blob.bin").write_bytes(bytes(range(256)) * 4)
        self.commit()
        proc = self.review()
        self.assertEqual(proc.returncode, 0, proc.stderr)


if __name__ == "__main__":
    unittest.main()
