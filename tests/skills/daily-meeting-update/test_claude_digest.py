"""Tests for daily-meeting-update/scripts/claude_digest.py with fake HOME logs."""
import json
import os
import re
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
        encoded=re.sub(r"[^A-Za-z0-9]","-",str(self.blog_path))  # tmp names may hold "_"
        blog=self.home/".claude/projects"/encoded; blog.mkdir(parents=True)
        (blog/"session-blog1234.jsonl").write_text(json.dumps({"type":"user","timestamp":"2026-01-20T12:00:00Z","cwd":str(self.blog_path),"message":{"content":"Update the blog homepage"}})+"\n")
    def tearDown(self): self.tmp.cleanup()
    def run_cli(self,*args,tz="America/New_York"):
        env=os.environ.copy(); env["HOME"]=str(self.home); env["TZ"]=tz
        return subprocess.run([sys.executable,str(SCRIPT),*args],capture_output=True,text=True,env=env)
    def test_json_digest_filters_date_and_reports_session_details(self):
        r=self.run_cli("--date","2026-01-20","--format","json"); self.assertEqual(r.returncode,0,r.stderr)
        data=json.loads(r.stdout); self.assertEqual(data["date"],"2026-01-20"); self.assertEqual(data["session_count"],2)
        s=data["sessions"][0]; self.assertEqual(s["id"],"12345678"); self.assertEqual(s["title"],"Session 12345678")
        self.assertEqual(s["project"],"[unresolved project: -home-user-payments]"); self.assertEqual(s["branch"],"feature/payments"); self.assertEqual(s["files"],["client.py","integration_test.py"]); self.assertEqual(s["commands_count"],2)
        self.assertNotIn("agent data",r.stdout); self.assertNotIn("different day",r.stdout)
    def test_project_filter_selects_only_requested_project(self):
        r=self.run_cli("--date","2026-01-20","--project",str(self.blog_path),"--format","json"); self.assertEqual(r.returncode,0,r.stderr)
        data=json.loads(r.stdout); self.assertEqual(data["session_count"],1); self.assertEqual(data["sessions"][0]["project"],str(self.blog_path)); self.assertEqual(data["sessions"][0]["id"],"session-"); self.assertEqual(data["sessions"][0]["title"],"Session session-")
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
    def test_local_day_follows_dst_rules_on_both_sides_of_transition(self):
        # US DST starts 2026-03-08; a captured fixed offset misfiles one of these whatever "now" is.
        project=self.home/".claude/projects/-home-user-payments"
        (project/"dst-before.jsonl").write_text('{"type":"user","timestamp":"2026-03-07T04:30:00Z","message":{"content":"x"}}\n')  # Mar 6 23:30 EST
        (project/"dst-after0.jsonl").write_text('{"type":"user","timestamp":"2026-03-09T04:30:00Z","message":{"content":"x"}}\n')  # Mar 9 00:30 EDT
        ids=lambda d:[s["id"] for s in json.loads(self.run_cli("--date",d,"--format","json").stdout)["sessions"]]
        self.assertEqual(ids("2026-03-06"),["dst-befo"]); self.assertEqual(ids("2026-03-07"),[])
        self.assertEqual(ids("2026-03-09"),["dst-afte"]); self.assertEqual(ids("2026-03-08"),[])
    def test_metadata_comes_from_day_messages_and_splits_on_project_or_branch_change(self):
        project=self.home/".claude/projects/-home-user-payments"
        lines=[{"type":"user","timestamp":"2026-01-19T15:00:00Z","cwd":"/old","gitBranch":"old-branch","message":{"content":"x"}},
               {"type":"assistant","timestamp":"2026-01-20T15:00:00Z","cwd":"/home/user/api","gitBranch":"feat-a","message":{"content":[{"type":"tool_use","name":"Edit","input":{"file_path":"/home/user/api/a.py"}}]}},
               {"type":"assistant","timestamp":"2026-01-20T16:00:00Z","cwd":"/home/user/api","gitBranch":"feat-b","message":{"content":[{"type":"tool_use","name":"Edit","input":{"file_path":"/home/user/api/b.py"}}]}}]
        (project/"switcher.jsonl").write_text("".join(json.dumps(l)+"\n" for l in lines))
        items=[s for s in json.loads(self.run_cli("--date","2026-01-20","--format","json").stdout)["sessions"] if s["id"]=="switcher"]
        self.assertEqual([(s["project"],s["branch"],s["files"]) for s in items],[("/home/user/api","feat-a",["a.py"]),("/home/user/api","feat-b",["b.py"])])
    def test_project_filter_matches_claude_code_encoding_of_dotted_paths(self):
        path=Path(self.tmp.name)/"repo"/".claude"/"worktrees"/"wt"; path.mkdir(parents=True)
        d=self.home/".claude/projects"/re.sub(r"[^A-Za-z0-9]","-",str(path)); d.mkdir(parents=True)
        (d/"dotted00.jsonl").write_text(json.dumps({"type":"user","timestamp":"2026-01-20T12:00:00Z","cwd":str(path),"message":{"content":"x"}})+"\n")
        r=self.run_cli("--date","2026-01-20","--project",str(path),"--format","json"); self.assertEqual(r.returncode,0,r.stderr)
        self.assertEqual([s["id"] for s in json.loads(r.stdout)["sessions"]],["dotted00"])
    def test_project_filter_drops_messages_whose_cwd_is_outside_the_project(self):
        blog=self.home/".claude/projects"/re.sub(r"[^A-Za-z0-9]","-",str(self.blog_path))
        lines=[{"type":"assistant","timestamp":"2026-01-20T14:00:00Z","cwd":"/home/user/private","message":{"content":[{"type":"tool_use","name":"Edit","input":{"file_path":"/home/user/private/diary.md"}}]}},
               {"type":"assistant","timestamp":"2026-01-20T14:05:00Z","message":{"content":[{"type":"tool_use","name":"Bash","input":{"command":"ls"}}]}},
               {"type":"assistant","timestamp":"2026-01-20T14:10:00Z","cwd":str(self.blog_path/"posts"),"message":{"content":[{"type":"tool_use","name":"Edit","input":{"file_path":"/x/post.md"}}]}}]
        (blog/"outside0.jsonl").write_text("".join(json.dumps(l)+"\n" for l in lines))
        r=self.run_cli("--date","2026-01-20","--project",str(self.blog_path),"--format","json"); self.assertEqual(r.returncode,0,r.stderr)
        items=[s for s in json.loads(r.stdout)["sessions"] if s["id"]=="outside0"]
        self.assertNotIn("diary.md",r.stdout); self.assertNotIn("/home/user/private",r.stdout)
        self.assertEqual([(s["project"],s["files"],s["commands_count"]) for s in items],[(str(self.blog_path/"posts"),["post.md"],0)])
    def test_project_filter_finds_sessions_launched_from_a_subdirectory(self):
        child=self.blog_path/"themes"; sibling=Path(str(self.blog_path)+"-old")
        for cwd,sid in ((child,"childses"),(sibling,"siblings")):
            d=self.home/".claude/projects"/re.sub(r"[^A-Za-z0-9]","-",str(cwd)); d.mkdir(parents=True)
            (d/f"{sid}.jsonl").write_text(json.dumps({"type":"user","timestamp":"2026-01-20T12:00:00Z","cwd":str(cwd),"message":{"content":"x"}})+"\n")
        r=self.run_cli("--date","2026-01-20","--project",str(self.blog_path),"--format","json"); self.assertEqual(r.returncode,0,r.stderr)
        self.assertEqual(sorted(s["id"] for s in json.loads(r.stdout)["sessions"]),["childses","session-"])
if __name__=="__main__": unittest.main()
