"""Tests for plugin-forge/scripts/create_plugin.py using temporary marketplaces."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills/plugin-forge/scripts/create_plugin.py"

class CreatePluginTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.root = Path(self.tmp.name)
        (self.root/".claude-plugin").mkdir()
        (self.root/".claude-plugin/marketplace.json").write_text('{"name":"market","plugins":[]}')
    def tearDown(self): self.tmp.cleanup()
    def run_cli(self, name="demo", **extra):
        args=[sys.executable,str(SCRIPT),name,"--marketplace-root",str(self.root),"--author-name","Jane Doe","--author-email","jane@example.test","--description","Demo plugin","--keywords","alpha,beta"]
        for key,value in extra.items(): args.extend(["--"+key.replace("_","-"),value])
        return subprocess.run(args,capture_output=True,text=True)
    def test_creates_structure_manifests_and_readme(self):
        r=self.run_cli(category="development"); self.assertEqual(r.returncode,0,r.stdout+r.stderr)
        plugin=self.root/"plugins/demo"
        self.assertTrue((plugin/".claude-plugin/plugin.json").is_file()); self.assertTrue((plugin/"commands").is_dir()); self.assertTrue((plugin/"skills").is_dir()); self.assertIn("# demo",(plugin/"README.md").read_text())
        manifest=json.loads((plugin/".claude-plugin/plugin.json").read_text()); self.assertEqual(manifest["version"],"0.1.0"); self.assertEqual(manifest["author"],{"name":"Jane Doe","email":"jane@example.test"}); self.assertEqual(manifest["keywords"],["alpha","beta"])
        marketplace=json.loads((self.root/".claude-plugin/marketplace.json").read_text()); self.assertEqual(marketplace["plugins"],[{"name":"demo","source":"./plugins/demo","description":"Demo plugin","version":"0.1.0","keywords":["alpha","beta"],"category":"development"}])
    def test_duplicate_directory_is_rejected(self):
        (self.root/"plugins/demo").mkdir(parents=True); r=self.run_cli(); self.assertNotEqual(r.returncode,0); self.assertIn("already exists",r.stderr)
    def test_duplicate_marketplace_entry_is_rejected(self):
        (self.root/".claude-plugin/marketplace.json").write_text('{"plugins":[{"name":"demo"}]}')
        r=self.run_cli()
        self.assertNotEqual(r.returncode,0)
        self.assertIn("already exists",r.stderr)
        self.assertFalse((self.root/"plugins/demo").exists())
    def test_rejects_path_traversal(self):
        r=self.run_cli("../escape"); self.assertNotEqual(r.returncode,0); self.assertIn("kebab-case",r.stderr)
        self.assertFalse((self.root.parent/"escape").exists())
    def test_missing_marketplace_manifest_fails(self):
        (self.root/".claude-plugin/marketplace.json").unlink(); r=self.run_cli(); self.assertNotEqual(r.returncode,0); self.assertIn("Marketplace manifest not found",r.stderr)
if __name__ == "__main__": unittest.main()
