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


def rows(text):
    return [(name.strip(), icon.strip()) for name, icon in ROW_RE.findall(text)]


class FindAwsIconTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = TABLE.read_text(encoding="utf-8")
        cls.current = rows(cls.text)
        cls.before = [tuple(line.split("\t", 1)) for line in FIXTURE.read_text().splitlines()]

    def test_all_rows_survive_translation(self):
        self.assertEqual(len(self.current), 475)
        self.assertEqual(len(self.before), len(self.current))
        self.assertEqual([icon for _, icon in self.current], [icon for _, icon in self.before])
        renamed = {icon for name, icon in self.before if name == "<renamed>"}
        self.assertEqual(renamed, EXPECTED_RENAMES)
        for (name, icon), (old_name, old_icon) in zip(self.current, self.before):
            if old_name != "<renamed>":
                self.assertEqual((name, icon), (old_name, old_icon))

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
        for query, icon in [("AWS Cloud", "mxgraph.aws4.group_aws_cloud"), ("VPC", "mxgraph.aws4.group_vpc")]:
            with self.subTest(query=query):
                output = subprocess.run([sys.executable, str(SCRIPT), query], capture_output=True, text=True, check=True).stdout
                self.assertIn(f"Style: shape=mxgraph.aws4.group;grIcon={icon};", output)
                self.assertNotIn(f"Style: shape=mxgraph.aws4.resourceIcon;resIcon={icon};", output)

    def test_duplicate_names_retain_distinct_variants(self):
        output = subprocess.run([sys.executable, str(SCRIPT), "Amazon API Gateway"], capture_output=True, text=True, check=True).stdout
        self.assertEqual(output.count("Service: Amazon API Gateway"), 2)
        self.assertIn("resIcon: mxgraph.aws4.api_gateway", output)
        self.assertIn("resIcon: mxgraph.aws4.api_gateway", output)


if __name__ == "__main__":
    unittest.main()
