import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TABLE = ROOT / "skills/draw-io/references/aws-icons.md"
FIXTURE = ROOT / "tests/skills/draw-io/fixtures/aws-icon-rows.before.txt"
SCRIPT = ROOT / "skills/draw-io/scripts/find_aws_icon.py"
ROW_RE = re.compile(r"\|\s*([^|]+?)\s*\|\s*(mxgraph\.aws4\.[a-z0-9_]+)\s*\|")
NON_LATIN_RE = re.compile(
    "[" + "".join(f"{chr(a)}-{chr(b)}" for a, b in [
        (0x3400, 0x4DBF), (0x4E00, 0x9FFF), (0xF900, 0xFAFF), (0x20000, 0x2EBEF),
        (0x3040, 0x309F), (0x30A0, 0x30FF), (0x31F0, 0x31FF),
        (0x1100, 0x11FF), (0x3130, 0x318F), (0xAC00, 0xD7AF),
        (0x0400, 0x052F), (0x0600, 0x06FF), (0x0750, 0x077F),
        (0x0590, 0x05FF), (0x0E00, 0x0E7F), (0x0900, 0x097F),
        (0x0370, 0x03FF), (0x1F00, 0x1FFF),
    ]) + "]"
)
EXPECTED_RENAMES = {
    "mxgraph.aws4.elb", "mxgraph.aws4.iam",
    "mxgraph.aws4.elasticsearch_service", "mxgraph.aws4.machine_learning",
}
# 2026-11-15 corrections from the draw.io AWS4 palette (Sidebar-AWS4.js lines 265-299): the fixture keeps
# the old names, so the test maps them. Five group rows left the table: subnets and the Availability Zone
# are recipes or plain rectangles in section 4.3, and two names have no palette equivalent.
GROUP_FIXES = {
    "mxgraph.aws4.group_vpc": "mxgraph.aws4.group_vpc2",
    "mxgraph.aws4.group_aws_account": "mxgraph.aws4.group_account",
    "mxgraph.aws4.group_elastic_beanstalk_container": "mxgraph.aws4.group_elastic_beanstalk",
    "mxgraph.aws4.group_auto_scaling": "mxgraph.aws4.group_auto_scaling_group",
    "mxgraph.aws4.group_step_functions_workflow": "mxgraph.aws4.group_aws_step_functions_workflow",
}
GROUP_ROWS_LEFT = {
    "mxgraph.aws4.group_availability_zone", "mxgraph.aws4.group_public_subnet",
    "mxgraph.aws4.group_private_subnet", "mxgraph.aws4.group_generic", "mxgraph.aws4.group_server_contents",
}
MARK = " [unverified]"


def rows(text):
    return [(name.strip(), icon.strip()) for name, icon in ROW_RE.findall(text)]


class FindAwsIconTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = TABLE.read_text(encoding="utf-8")
        cls.current = rows(cls.text)
        cls.before = [tuple(line.split("\t", 1)) for line in FIXTURE.read_text().splitlines()]

    def test_all_rows_survive_translation(self):
        self.assertEqual(len(self.before), 475)
        expected = [(name, GROUP_FIXES.get(icon, icon)) for name, icon in self.before if icon not in GROUP_ROWS_LEFT]
        self.assertEqual(len(self.current), 470)
        self.assertEqual([icon for _, icon in self.current], [icon for _, icon in expected])
        renamed = {icon for name, icon in self.before if name == "<renamed>"}
        self.assertEqual(renamed, EXPECTED_RENAMES)
        for (name, icon), (old_name, old_icon) in zip(self.current, expected):
            if old_name != "<renamed>":
                # a row may gain a legacy note or the unverified mark, but keeps its name and icon
                self.assertTrue(name.removesuffix(MARK).startswith(old_name), (name, old_name))
                self.assertEqual(icon, old_icon)

    def test_unverified_rows_are_marked(self):
        marked = {icon for name, icon in self.current if name.endswith(MARK)}
        self.assertEqual(len(marked), 84)
        for icon in ("ebs", "efs", "iam", "elb", "laptop", "qldb", "msk", "opensearch"):
            self.assertIn(f"mxgraph.aws4.{icon}", marked)
        for icon in ("lambda", "s3", "dynamodb", "cloudfront", "api_gateway"):
            self.assertNotIn(f"mxgraph.aws4.{icon}", marked)

    def test_group_icon_names_are_the_palette_forms(self):
        icons = {icon for _, icon in self.current}
        for gone in GROUP_ROWS_LEFT | set(GROUP_FIXES):
            self.assertNotIn(gone, icons)
        for icon in GROUP_FIXES.values():
            self.assertIn(icon, icons)
        self.assertIn("grIcon=mxgraph.aws4.group_security_group;grStroke=0;strokeColor=#7AA116;fillColor=#F2F6E8;", self.text)
        self.assertIn("grIcon=mxgraph.aws4.group_security_group;grStroke=0;strokeColor=#00A4A6;fillColor=#E6F6F7;", self.text)

    def test_legacy_services_are_labelled(self):
        by_icon = {icon: name for name, icon in self.current}
        self.assertIn("legacy", by_icon["mxgraph.aws4.codewhisperer"])
        self.assertIn("legacy", by_icon["mxgraph.aws4.qldb"])

    def test_script_prints_the_unverified_mark(self):
        output = subprocess.run([sys.executable, str(SCRIPT), "Amazon EBS"], capture_output=True, text=True, check=True).stdout
        self.assertIn("Service: Amazon EBS [unverified]\nresIcon: mxgraph.aws4.ebs\n", output)

    def test_expected_renames_are_english(self):
        by_icon = {icon: name for name, icon in self.current}
        for icon in EXPECTED_RENAMES:
            self.assertIn(icon, by_icon)
            self.assertNotEqual(by_icon[icon], "<renamed>")
            self.assertTrue(by_icon[icon].isascii(), by_icon[icon])

    def test_no_non_latin_in_table_rows(self):
        for line in self.text.splitlines():
            if line.startswith("|"):
                self.assertIsNone(NON_LATIN_RE.search(line), line)

    def test_script_output_matches_table_rows(self):
        output = subprocess.run([sys.executable, str(SCRIPT), "mxgraph"], capture_output=True, text=True, check=True).stdout
        found = re.findall(r"Service: (.+)\n(?:resIcon|grIcon): (mxgraph\.aws4\.[a-z0-9_]+)", output)
        self.assertEqual(len(found), len(self.current))
        self.assertEqual({(name, icon) for name, icon in found}, set(self.current))

    def test_no_non_latin_in_output(self):
        output = subprocess.run([sys.executable, str(SCRIPT), "mxgraph"], capture_output=True, text=True, check=True).stdout
        self.assertIsNone(NON_LATIN_RE.search(output))

    def test_group_searches_preserve_group_styles(self):
        for query, icon in [("AWS Cloud", "mxgraph.aws4.group_aws_cloud"), ("VPC", "mxgraph.aws4.group_vpc2")]:
            with self.subTest(query=query):
                output = subprocess.run([sys.executable, str(SCRIPT), query], capture_output=True, text=True, check=True).stdout
                self.assertIn(f"Style: shape=mxgraph.aws4.group;grIcon={icon};", output)
                self.assertNotIn(f"Style: shape=mxgraph.aws4.resourceIcon;resIcon={icon};", output)

    def test_auto_scaling_group_uses_group_center_shape(self):
        output = subprocess.run([sys.executable, str(SCRIPT), "Auto Scaling"], capture_output=True, text=True, check=True).stdout
        icon = "mxgraph.aws4.group_auto_scaling_group"
        self.assertIn(f"Style: shape=mxgraph.aws4.groupCenter;grIcon={icon};", output)
        self.assertNotIn(f"Style: shape=mxgraph.aws4.group;grIcon={icon};", output)
        result = subprocess.run([sys.executable, str(SCRIPT), "--json", icon], capture_output=True, text=True, check=True)
        self.assertEqual([d["style"] for d in json.loads(result.stdout)], [f"shape=mxgraph.aws4.groupCenter;grIcon={icon};"])

    def test_duplicate_names_retain_distinct_variants(self):
        output = subprocess.run([sys.executable, str(SCRIPT), "Generic database"], capture_output=True, text=True, check=True).stdout
        icons = re.findall(r"Service: Generic Database\nresIcon: (mxgraph\.aws4\.[a-z0-9_]+)", output)
        self.assertEqual(icons, ["mxgraph.aws4.database", "mxgraph.aws4.generic_database"])

    def test_identical_duplicate_rows_are_both_kept(self):
        output = subprocess.run([sys.executable, str(SCRIPT), "Amazon API Gateway"], capture_output=True, text=True, check=True).stdout
        self.assertEqual(output.count("Service: Amazon API Gateway\nresIcon: mxgraph.aws4.api_gateway\n"), 2)

    def test_help_exits_zero_and_documents_json(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "--help"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("usage: find_aws_icon.py", result.stdout)
        self.assertIn("--json", result.stdout)

    def test_missing_query_is_usage_error(self):
        result = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")

    def test_json_mode_returns_rows_with_styles(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "--json", "VPC"], capture_output=True, text=True, check=True)
        rows_out = json.loads(result.stdout)
        self.assertIn({"name": "VPC", "icon": "mxgraph.aws4.group_vpc2", "kind": "group",
                       "style": "shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_vpc2;"}, rows_out)
        self.assertIn("icon(s) for 'VPC'", result.stderr)

    def test_no_match_reports_on_stderr_and_exits_1(self):
        for extra in ([], ["--json"]):
            with self.subTest(extra=extra):
                result = subprocess.run([sys.executable, str(SCRIPT), *extra, "no-such-service-xyz"], capture_output=True, text=True)
                self.assertEqual(result.returncode, 1)
                self.assertIn("No icons found for: no-such-service-xyz", result.stderr)
                self.assertEqual(result.stdout.strip(), "[]" if extra else "")


if __name__ == "__main__":
    unittest.main()
