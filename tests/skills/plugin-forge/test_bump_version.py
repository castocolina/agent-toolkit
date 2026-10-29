"""Tests for plugin-forge/scripts/bump_version.py using temporary marketplace fixtures."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills/plugin-forge/scripts/bump_version.py"

class BumpVersionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "plugins/demo/.claude-plugin").mkdir(parents=True)
        (self.root / ".claude-plugin").mkdir()
        (self.root / "plugins/demo/.claude-plugin/plugin.json").write_text(json.dumps({"name":"demo","version":"1.2.3"}))
        (self.root / ".claude-plugin/marketplace.json").write_text(json.dumps({"plugins":[{"name":"demo","version":"1.2.3"},{"name":"other","version":"9.0.0"}]}))
    def tearDown(self): self.tmp.cleanup()
    def run_cli(self, *args): return subprocess.run([sys.executable,str(SCRIPT),*args,"--marketplace-root",str(self.root)],capture_output=True,text=True)
    def versions(self):
        p=json.loads((self.root/"plugins/demo/.claude-plugin/plugin.json").read_text())
        m=json.loads((self.root/".claude-plugin/marketplace.json").read_text())
        return p["version"],next(x["version"] for x in m["plugins"] if x["name"]=="demo")
    def test_patch_updates_both_manifests(self):
        r=self.run_cli("demo","patch"); self.assertEqual(r.returncode,0,r.stderr); self.assertEqual(self.versions(),("1.2.4","1.2.4"))
        result=json.loads(r.stdout); self.assertEqual(result["status"],"updated"); self.assertEqual(result["new_version"],"1.2.4")
    def test_rejects_path_traversal(self):
        r=self.run_cli("../escape","patch"); self.assertNotEqual(r.returncode,0); self.assertIn("kebab-case",r.stderr)
    def test_minor_updates_both_manifests_and_preserves_other_plugin(self):
        r=self.run_cli("demo","minor"); self.assertEqual(r.returncode,0); self.assertEqual(self.versions(),("1.3.0","1.3.0")); self.assertIn('"version": "9.0.0"',(self.root/".claude-plugin/marketplace.json").read_text())
    def test_major_updates_both_manifests(self):
        r=self.run_cli("demo","major"); self.assertEqual(r.returncode,0); self.assertEqual(self.versions(),("2.0.0","2.0.0"))
    def test_invalid_part_is_rejected_by_cli(self):
        r=self.run_cli("demo","invalid"); self.assertNotEqual(r.returncode,0)
    def test_missing_plugin_manifest_fails(self):
        (self.root/"plugins/demo/.claude-plugin/plugin.json").unlink(); r=self.run_cli("demo","patch"); self.assertNotEqual(r.returncode,0); self.assertIn("Plugin manifest not found",r.stdout)
    def test_missing_marketplace_entry_fails(self):
        plugin_path = self.root/"plugins/demo/.claude-plugin/plugin.json"
        original_plugin = plugin_path.read_text()
        (self.root/".claude-plugin/marketplace.json").write_text('{"plugins":[]}')
        original_marketplace = (self.root/".claude-plugin/marketplace.json").read_text()
        r=self.run_cli("demo","patch")
        self.assertNotEqual(r.returncode,0)
        self.assertIn("not found in marketplace manifest",r.stdout)
        self.assertEqual(plugin_path.read_text(), original_plugin)
        self.assertEqual((self.root/".claude-plugin/marketplace.json").read_text(), original_marketplace)
if __name__ == "__main__": unittest.main()
