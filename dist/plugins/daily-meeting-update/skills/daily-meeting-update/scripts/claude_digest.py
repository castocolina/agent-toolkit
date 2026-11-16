#!/usr/bin/env python3
"""
Get Claude Code conversation digest for daily standup integration.

Needs Python 3.9 or later (Path.is_relative_to).
Reads transcripts under $CLAUDE_CONFIG_DIR/projects (default ~/.claude/projects). Claude
Code's transcript format is internal and can change on any release; unparseable lines are
skipped, so a format change shows up as an empty digest.

Usage:
    claude_digest.py [--date DATE] [--project PATH] [--format json|text]

Examples:
    claude_digest.py                    # Yesterday's digest (default)
    claude_digest.py --date today       # Today's digest
    claude_digest.py --date 2026-01-20  # Specific date (local calendar day)
    claude_digest.py --format json      # JSON output for parsing

Titles never contain message text (logs can hold secrets): a session's title is
"Session <first 8 characters of its id>". Each message keeps its own recorded cwd and
git branch, and a session that switched project or branch that day is listed once per pair.
When no cwd was recorded, the project is "[unresolved project: <directory name>]" (the
directory name is never decoded into a path).

Output (JSON format):
{
  "date": "2026-01-21",
  "session_count": 1,
  "sessions": [
    {
      "id": "abc12345",
      "title": "Session abc12345",
      "project": "/home/user/my-app",
      "branch": "main",
      "files": ["auth.ts", "login.vue"],
      "commands_count": 3
    }
  ]
}
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional


@dataclass
class Session:
    """Represents a Claude Code session."""
    id: str
    title: str
    project: str
    branch: Optional[str]
    files: list
    commands_count: int
    timestamp: datetime


def get_claude_projects_dir() -> Path:
    """Get the Claude projects directory; CLAUDE_CONFIG_DIR moves it off ~/.claude."""
    config_dir = os.environ.get('CLAUDE_CONFIG_DIR')
    return (Path(config_dir).expanduser() if config_dir else Path.home() / '.claude') / 'projects'


def decode_project_path(encoded: str) -> str:
    """Return the encoded identifier without inventing path separators."""
    return f"[unresolved project: {encoded}]"


def parse_timestamp(timestamp: str) -> Optional[datetime]:
    """Parse ISO timestamp string to datetime."""
    if not timestamp:
        return None
    try:
        if 'T' in timestamp:
            value = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
        return datetime.strptime(timestamp[:10], '%Y-%m-%d').replace(tzinfo=timezone.utc)
    except (ValueError, IndexError):
        return None


def extract_tool_uses(content) -> list:
    """Extract tool_use blocks from message content."""
    if not isinstance(content, list):
        return []
    return [
        {'name': block.get('name'), 'input': block.get('input', {})}
        for block in content
        if isinstance(block, dict) and block.get('type') == 'tool_use'
    ]


def parse_session_file(file_path: Path) -> Optional[dict]:
    """Parse a JSONL session file; each message keeps its own cwd and branch."""
    messages = []
    session_id = file_path.stem
    cwd = decode_project_path(file_path.parent.name)
    git_branch = None

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue

                if entry.get('type') not in ('user', 'assistant'):
                    continue

                # Entries missing cwd/gitBranch inherit the last value seen in this session.
                cwd = entry.get('cwd') or cwd
                git_branch = entry.get('gitBranch') or git_branch
                content = entry.get('message', {}).get('content', '')
                messages.append({
                    'timestamp': entry.get('timestamp', ''),
                    'project': cwd,
                    'branch': git_branch,
                    'tool_uses': extract_tool_uses(content)
                })

    except Exception as e:
        print(f"Error parsing {file_path.name}: {e}", file=sys.stderr)
        return None

    if not messages:
        return None

    return {'session_id': session_id, 'messages': messages}


def extract_title(session_data: dict) -> str:
    """Return a metadata-only title; never expose session text as a title."""
    session_id = session_data.get('session_id', '')
    return f"Session {session_id[:8]}" if session_id else 'Untitled session'


def extract_files(messages: list) -> list:
    """Extract files touched during session."""
    files = set()
    for msg in messages:
        for tool in msg.get('tool_uses', []):
            name = tool.get('name', '')
            inp = tool.get('input', {})

            if name in ('Read', 'Write', 'Edit'):
                path = inp.get('file_path', '')
                if path:
                    files.add(Path(path).name)

    return sorted(files)[:10]


def count_commands(messages: list) -> int:
    """Count bash commands executed."""
    count = 0
    for msg in messages:
        for tool in msg.get('tool_uses', []):
            if tool.get('name') == 'Bash':
                count += 1
    return count


def in_scope(cwd: str, scope: Path) -> bool:
    """The project dir is only a candidate: each message's own recorded cwd must sit inside scope."""
    return os.path.isabs(cwd) and Path(cwd).resolve().is_relative_to(scope)


def get_sessions_for_date(
    target_date: datetime,
    project_path: Optional[str] = None
) -> list:
    """Get all sessions for a specific date."""
    sessions = []
    projects_dir = get_claude_projects_dir()

    if not projects_dir.exists():
        return []

    requested_day = target_date.date()

    # Get project directories
    scope = None
    if project_path:
        given = Path(project_path).expanduser()
        scope = given.resolve()
        # Claude Code names project dirs by replacing every non-alphanumeric character with '-';
        # try the path as given and resolved, since symlinks (e.g. /home -> /var/home) differ.
        # A prefix match also finds sessions launched from subdirectories; the encoding is lossy
        # (/app-old shares the prefix of /app/old), so in_scope() still filters every message.
        # Names over 200 characters are truncated to 200 and get a hash suffix, so match that prefix.
        names = {re.sub(r'[^A-Za-z0-9]', '-', str(p))[:200] for p in (given.absolute(), scope)}
        project_dirs = sorted(d for d in projects_dir.iterdir() if d.is_dir() and any(
            d.name == n or d.name.startswith(n if len(n) == 200 else n + '-') for n in names))
    else:
        project_dirs = [d for d in projects_dir.iterdir() if d.is_dir()]

    for project_dir in project_dirs:
        for jsonl_file in project_dir.glob('*.jsonl'):
            if jsonl_file.name.startswith('agent-'):
                continue

            session_data = parse_session_file(jsonl_file)
            if session_data is None:
                continue

            # Filter to the requested local day first; astimezone() with no argument applies
            # the local DST rule for each instant, unlike a captured fixed offset.
            groups = {}
            for message in session_data['messages']:
                timestamp = parse_timestamp(message['timestamp'])
                if timestamp is not None and timestamp.astimezone().date() == requested_day \
                        and (scope is None or in_scope(message['project'], scope)):
                    message['parsed'] = timestamp
                    groups.setdefault((message['project'], message['branch']), []).append(message)

            # A session that switches project or branch during the day yields one entry per pair.
            for (project, branch), day_messages in groups.items():
                sessions.append(Session(
                    id=session_data['session_id'][:8],
                    title=extract_title(session_data),
                    project=project,
                    branch=branch,
                    files=extract_files(day_messages),
                    commands_count=count_commands(day_messages),
                    timestamp=min(m['parsed'] for m in day_messages),
                ))

    sessions.sort(key=lambda s: s.timestamp)
    return sessions


def parse_date_arg(date_arg: str) -> datetime:
    """Parse date argument."""
    today = datetime.now()

    if date_arg == 'today':
        return today
    elif date_arg == 'yesterday':
        return today - timedelta(days=1)
    else:
        try:
            return datetime.strptime(date_arg, '%Y-%m-%d')
        except ValueError:
            print(f"Invalid date: {date_arg}. Use 'today', 'yesterday', or YYYY-MM-DD", file=sys.stderr)
            sys.exit(1)


def format_text(sessions: list, target_date: datetime) -> str:
    """Format sessions as text."""
    date_str = target_date.strftime('%B %d, %Y')

    if not sessions:
        return f"No sessions found for {date_str}"

    lines = [f"## {date_str} - {len(sessions)} session{'s' if len(sessions) != 1 else ''}", ""]

    for i, s in enumerate(sessions, 1):
        lines.append(f"### {i}. {s.title}")
        lines.append(f"   Session: `{s.id}`")
        if s.branch:
            lines.append(f"   Branch: `{s.branch}`")
        if s.files:
            lines.append(f"   Files: {', '.join(s.files[:5])}")
        if s.commands_count:
            lines.append(f"   Commands: {s.commands_count} executed")
        lines.append("")

    return '\n'.join(lines)


def format_json(sessions: list, target_date: datetime) -> dict:
    """Format sessions as JSON."""
    return {
        'date': target_date.strftime('%Y-%m-%d'),
        'session_count': len(sessions),
        'sessions': [
            {
                'id': s.id,
                'title': s.title,
                'project': s.project,
                'branch': s.branch,
                'files': s.files,
                'commands_count': s.commands_count
            }
            for s in sessions
        ]
    }


def main():
    parser = argparse.ArgumentParser(
        description='Get Claude Code conversation digest for daily standup'
    )
    parser.add_argument('--date', '-d', default='yesterday',
                       help='Date to get digest for (today, yesterday, or YYYY-MM-DD). Default: yesterday')
    parser.add_argument('--project', '-p', help='Filter to specific project path')
    parser.add_argument('--format', '-f', choices=['text', 'json'], default='text',
                       help='Output format (default: text)')

    args = parser.parse_args()

    target_date = parse_date_arg(args.date)
    sessions = get_sessions_for_date(target_date, args.project)

    if args.format == 'json':
        print(json.dumps(format_json(sessions, target_date), indent=2))
    else:
        print(format_text(sessions, target_date))


if __name__ == '__main__':
    main()
