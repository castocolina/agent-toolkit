"""Tests for daily-meeting-update/scripts/claude_digest.py with fake HOME logs."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
SCRIPT=ROOT/"skills/daily-meeting-update/scripts/claude_digest.py"
FIXTURE=Path(__file__).parent/"fixtures/session-log.jsonl"

class ClaudeDigestTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(dir=os.path.realpath("/tmp")); self.home=Path(self.tmp.name)/"home"
        project=self.home/".claude/projects/-home-user-payments"; project.mkdir(parents=True)
        shutil.copyfile(FIXTURE,project/"12345678-1234-4abc-8def-123456789abc.jsonl")
        (project/"agent-11111111-2222-4333-8444-555566667777.jsonl").write_text('{"type":"user","timestamp":"2026-01-20T10:00:00Z","message":{"content":"agent data must be skipped"}}\n')
        (project/"session-other-day.jsonl").write_text('{"type":"user","timestamp":"2026-01-21T10:00:00Z","message":{"content":"different day"}}\n')
        self.blog_path=Path(self.tmp.name)/"blog"
        encoded="-"+str(self.blog_path)[1:].replace("/","-")
        blog=self.home/".claude/projects"/encoded; blog.mkdir(parents=True)
        (blog/"session-blog1234.jsonl").write_text('{"type":"user","timestamp":"2026-01-20T12:00:00Z","message":{"content":"Update the blog homepage"}}\n')
    def tearDown(self): self.tmp.cleanup()
    def run_cli(self,*args):
        env=os.environ.copy(); env["HOME"]=str(self.home)
        return subprocess.run([sys.executable,str(SCRIPT),*args],capture_output=True,text=True,env=env)
    def test_json_digest_filters_date_and_reports_session_details(self):
        r=self.run_cli("--date","2026-01-20","--format","json"); self.assertEqual(r.returncode,0,r.stderr)
        data=json.loads(r.stdout); self.assertEqual(data["date"],"2026-01-20"); self.assertEqual(data["session_count"],2)
        s=data["sessions"][0]; self.assertEqual(s["id"],"12345678"); self.assertEqual(s["title"],"Session 12345678")
        self.assertEqual(s["project"],"[unresolved project: -home-user-payments]"); self.assertEqual(s["branch"],"feature/payments"); self.assertEqual(s["files"],["client.py","integration_test.py"]); self.assertEqual(s["commands_count"],2)
        self.assertNotIn("agent data",r.stdout); self.assertNotIn("different day",r.stdout)
    def test_project_filter_selects_only_requested_project(self):
        r=self.run_cli("--date","2026-01-20","--project",str(self.blog_path),"--format","json"); self.assertEqual(r.returncode,0,r.stderr)
        data=json.loads(r.stdout); self.assertEqual(data["session_count"],1); self.assertEqual(data["sessions"][0]["project"].split(": ", 1)[0],"[unresolved project"); self.assertEqual(data["sessions"][0]["id"],"session-"); self.assertEqual(data["sessions"][0]["title"],"Session session-")
    def test_text_output_includes_title_branch_files_and_command_count(self):
        r=self.run_cli("--date","2026-01-20"); self.assertEqual(r.returncode,0,r.stderr)
        self.assertIn("## January 20, 2026 - 2 sessions",r.stdout); self.assertIn("### 1. Session 12345678",r.stdout); self.assertIn("Branch: `feature/payments`",r.stdout); self.assertIn("Files: client.py, integration_test.py",r.stdout); self.assertIn("Commands: 2 executed",r.stdout)
    def test_title_never_exposes_secrets_or_private_urls_from_user_messages(self):
        project=self.home/".claude/projects/-home-user-payments"
        secret="sk-live-secret-value"
        private_url="https://private.example.internal/path?token=hidden"
        line={"type":"user","timestamp":"2026-01-20T13:00:00Z","message":{"content":f"{secret} {private_url}"}}
        (project/"sensitive-title.jsonl").write_text(json.dumps(line)+"\n")
        r=self.run_cli("--date","2026-01-20","--format","json"); self.assertEqual(r.returncode,0,r.stderr)
        self.assertNotIn(secret,r.stdout); self.assertNotIn(private_url,r.stdout)
        item=next(s for s in json.loads(r.stdout)["sessions"] if s["id"] == "sensitiv")
        self.assertEqual(item["title"],"Session sensitiv")
    def test_no_projects_produces_empty_digest(self):
        shutil.rmtree(self.home/".claude/projects")
        r=self.run_cli("--date","2026-01-20","--format","json"); self.assertEqual(r.returncode,0,r.stderr); self.assertEqual(json.loads(r.stdout)["session_count"],0)
    def test_invalid_date_fails_with_usage_message(self):
        r=self.run_cli("--date","not-a-date"); self.assertNotEqual(r.returncode,0); self.assertIn("Invalid date",r.stderr)
    def test_help_lists_supported_options(self):
        r=self.run_cli("--help"); self.assertEqual(r.returncode,0,r.stderr)
        for option in ("--date", "--project", "--format"):
            self.assertIn(option, r.stdout)
    def test_corrupt_jsonl_line_does_not_discard_other_activity(self):
        project=self.home/".claude/projects/-home-user-payments"
        (project/"corrupt-session.jsonl").write_text('not json\n{"type":"user","timestamp":"2026-01-20T12:00:00Z","cwd":"/home/user/my-app","message":{"content":"Work on app"}}\n')
        r=self.run_cli("--date","2026-01-20","--format","json"); self.assertEqual(r.returncode,0,r.stderr)
        data=json.loads(r.stdout); item=next(s for s in data["sessions"] if s["project"] == "/home/user/my-app")
        self.assertEqual(item["title"],"Session corrupt-")
    def test_cross_day_session_filters_activity_and_prefers_recorded_cwd(self):
        project=self.home/".claude/projects/-home-user-payments"
        (project/"cross-day.jsonl").write_text('''{"type":"user","timestamp":"2026-01-19T20:55:00-05:00","cwd":"/home/user/my-app","message":{"content":"Prior day work"}}\n{"type":"assistant","timestamp":"2026-01-20T01:05:00-05:00","cwd":"/home/user/my-app","message":{"content":[{"type":"tool_use","name":"Bash","input":{"command":"test"}},{"type":"tool_use","name":"Read","input":{"file_path":"/home/user/my-app/today.py"}}]}}\n{"type":"user","timestamp":"2026-01-20T01:06:00-05:00","cwd":"/home/user/my-app","message":{"content":"Investigate today"}}\n''')
        r=self.run_cli("--date","2026-01-20","--format","json"); self.assertEqual(r.returncode,0,r.stderr)
        item=next(s for s in json.loads(r.stdout)["sessions"] if s["id"] == "cross-da")
        self.assertEqual(item["project"],"/home/user/my-app"); self.assertEqual(item["commands_count"],1)
        self.assertEqual(item["files"],["today.py"]); self.assertEqual(item["title"],"Session cross-da")
if __name__=="__main__": unittest.main()
