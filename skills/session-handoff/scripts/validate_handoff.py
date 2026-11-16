#!/usr/bin/env python3
"""
Validate a handoff document for completeness and quality.

Checks:
- No TODO placeholders remaining
- Required sections present and populated
- No potential secrets detected
- Referenced files exist
- Quality scoring

Run with --help for usage, exit codes and examples.
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Secret detection patterns
SECRET_PATTERNS = [
    (r'["\']?[a-zA-Z_]*api[_-]?key["\']?\s*[:=]\s*["\'][^"\']{10,}["\']', "API key"),
    (r'["\']?[a-zA-Z_]*password["\']?\s*[:=]\s*["\'][^"\']+["\']', "Password"),
    (r'["\']?[a-zA-Z_]*secret["\']?\s*[:=]\s*["\'][^"\']{10,}["\']', "Secret"),
    (r'["\']?[a-zA-Z_]*token["\']?\s*[:=]\s*["\'][^"\']{20,}["\']', "Token"),
    (r'["\']?[a-zA-Z_]*private[_-]?key["\']?\s*[:=]', "Private key"),
    (r'-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY-----', "PEM private key"),
    # Any scheme://user:password@ (redis, amqp, mongodb+srv, ...); skips user@ and <pw>/$VAR/*** placeholders.
    (r'[a-z][a-z0-9+.\-]*://[^/\s:@]*:(?![<$*])[^@\s/]+@', "URL with embedded password"),
    (r'Bearer\s+[a-zA-Z0-9_\-\.]{20,}', "Bearer token"),  # 20+: prose "Bearer token" is not a credential
    (r'ghp_[a-zA-Z0-9]{36}', "GitHub personal access token"),
    (r'sk-[a-zA-Z0-9]{48}', "OpenAI API key"),
    (r'xox[baprs]-[a-zA-Z0-9-]+', "Slack token"),
]

# Required sections for a complete handoff
REQUIRED_SECTIONS = [
    "Current State Summary",
    "Important Context",
    "Immediate Next Steps",
]

# Recommended sections
RECOMMENDED_SECTIONS = [
    "Architecture Overview",
    "Critical Files",
    "Files Modified",
    "Decisions Made",
    "Assumptions Made",
    "Potential Gotchas",
]


def check_todos(content: str) -> tuple[bool, list[str]]:
    """Check for remaining TODO placeholders."""
    todos = re.findall(r'\[TODO:[^\]]*\]', content)
    return len(todos) == 0, todos


def check_required_sections(content: str) -> tuple[bool, list[str]]:
    """Check that required sections exist and have content."""
    missing = []
    for section in REQUIRED_SECTIONS:
        # Match section headings at any depth in the scaffold hierarchy.
        pattern = rf'(?:^|\n)#{{1,6}}\s*{re.escape(section)}'
        match = re.search(pattern, content, re.IGNORECASE)
        if not match:
            missing.append(f"{section} (missing)")
        else:
            # Check if section has meaningful content (not just placeholder)
            section_start = match.end()
            next_section = re.search(r'\n#{1,6}\s+', content[section_start:])
            section_end = section_start + next_section.start() if next_section else len(content)
            section_content = content[section_start:section_end].strip()

            # 50 chars minimum: roughly 1-2 sentences, enough to convey meaningful context
            if len(section_content) < 50 or '[TODO' in section_content:
                missing.append(f"{section} (incomplete)")

    return len(missing) == 0, missing


def check_recommended_sections(content: str) -> list[str]:
    """Check which recommended sections are missing."""
    missing = []
    for section in RECOMMENDED_SECTIONS:
        pattern = rf'(?:^|\n)#{{1,6}}\s*{re.escape(section)}'
        if not re.search(pattern, content, re.IGNORECASE):
            missing.append(section)
    return missing


def scan_for_secrets(content: str) -> list[tuple[str, str]]:
    """Scan content for potential secrets."""
    findings = []
    for pattern, description in SECRET_PATTERNS:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            findings.append((description, f"Found {len(matches)} potential match(es)"))
    return findings


FILE_REF_PATTERNS = [
    r'\|\s*([a-zA-Z0-9_\-./]+\.[a-zA-Z]+)\s*\|',  # Table cells
    r'`([a-zA-Z0-9_\-./]+\.[a-zA-Z]+(?::\d+)?)`',  # Inline code
    r'(?:^|\s)([a-zA-Z0-9_\-./]+\.[a-zA-Z]+:\d+)',  # path:line
    r'\]\(([a-zA-Z0-9_\-./]+\.[a-zA-Z]+)(?:#[^)]*)?\)',  # Markdown link; the colon-free charset skips URLs
]


def extract_file_references(content: str) -> set[str]:
    """Return file paths cited in tables, inline code, path:line or Markdown links.

    Root-level names (README.md) count too; URLs are skipped.
    """
    found = set()
    for pattern in FILE_REF_PATTERNS:
        for match in re.findall(pattern, content, re.MULTILINE):
            filepath = match.split(':')[0]
            if filepath and not filepath.startswith(('http', 'www.')) and '://' not in match:
                found.add(filepath)
    return found


def check_file_references(content: str, base_dirs: list[str]) -> tuple[list[str], list[str]]:
    """Split cited files into existing/missing; a file exists if any base dir holds it."""
    existing, missing = [], []
    for filepath in sorted(extract_file_references(content)):
        if any((Path(base) / filepath).exists() for base in base_dirs):
            existing.append(filepath)
        else:
            missing.append(filepath)
    return existing, missing


def calculate_quality_score(
    todos_clear: bool,
    required_complete: bool,
    missing_required: list,
    missing_recommended: list,
    secrets_found: list,
    files_missing: list
) -> tuple[int, str]:
    """Calculate overall quality score (0-100).

    Scoring rationale:
    - Start at 100, deduct for issues
    - TODOs remaining (-30): Indicates incomplete work, major blocker
    - Missing required sections (-10 each): Core context gaps
    - Secrets detected (-20): Security risk, must be fixed
    - Missing file refs (-5 each, max -20): Stale references
    - Missing recommended (-2 each): Nice-to-have completeness
    """
    score = 100

    # Deductions with justifications
    if not todos_clear:
        # -30: TODOs indicate unfinished work; next agent will lack critical info
        score -= 30
    if not required_complete:
        # -10 per section: Required sections are essential for handoff continuity
        score -= 10 * len(missing_required)
    if secrets_found:
        # -20: Security risk; handoffs may be shared or stored in repos
        score -= 20
    if files_missing:
        # -5 per file (max 4): Indicates stale refs; cap at -20 to avoid over-penalizing
        score -= 5 * min(len(files_missing), 4)

    # -2 per section: Recommended but not critical; minor impact on handoff quality
    score -= 2 * len(missing_recommended)

    score = max(0, score)

    # Rating thresholds based on handoff usability:
    # 90+: Comprehensive, ready to use immediately
    # 70-89: Usable with minor gaps
    # 50-69: Needs work before reliable handoff
    # <50: Too incomplete to be useful
    if score >= 90:
        rating = "Excellent - Ready for handoff"
    elif score >= 70:
        rating = "Good - Minor improvements suggested"
    elif score >= 50:
        rating = "Fair - Needs attention before handoff"
    else:
        rating = "Poor - Significant work needed"

    return score, rating


def validate_handoff(filepath: str) -> dict:
    """Run all validations on a handoff file."""
    path = Path(filepath)

    if not path.exists():
        return {"error": f"File not found: {filepath}"}

    content = path.read_text()
    # Project root (handoffs live in <root>/.claude/handoffs/) and the handoff's own directory for chain links.
    base_dirs = [str(path.parent.parent.parent), str(path.parent)]

    # Run checks
    todos_clear, remaining_todos = check_todos(content)
    required_complete, missing_required = check_required_sections(content)
    missing_recommended = check_recommended_sections(content)
    secrets_found = scan_for_secrets(content)
    existing_files, missing_files = check_file_references(content, base_dirs)

    # Calculate score
    score, rating = calculate_quality_score(
        todos_clear, required_complete, missing_required,
        missing_recommended, secrets_found, missing_files
    )

    if secrets_found:
        verdict = "BLOCKED"
    elif score >= 70 and todos_clear and required_complete:
        verdict = "READY"
    else:
        verdict = "NEEDS_WORK"

    return {
        "filepath": str(path),
        "verdict": verdict,
        "score": score,
        "rating": rating,
        "todos_clear": todos_clear,
        "remaining_todos": remaining_todos[:5],  # Limit output
        "todo_count": len(remaining_todos) if not todos_clear else 0,
        "required_complete": required_complete,
        "missing_required": missing_required,
        "missing_recommended": missing_recommended,
        "secrets_found": secrets_found,
        "files_verified": len(existing_files),
        "files_missing": missing_files[:5],  # Limit output
    }


def print_report(result: dict):
    """Print a formatted validation report."""
    print(f"\n{'='*60}")
    print(f"Handoff Validation Report")
    print(f"{'='*60}")
    print(f"File: {result['filepath']}")
    print(f"\nQuality Score: {result['score']}/100 - {result['rating']}")
    print(f"{'='*60}")

    # TODOs
    if result['todos_clear']:
        print("\n[PASS] No TODO placeholders remaining")
    else:
        print(f"\n[FAIL] {result['todo_count']} TODO placeholders found:")
        for todo in result['remaining_todos']:
            print(f"       - {todo[:50]}...")

    # Required sections
    if result['required_complete']:
        print("\n[PASS] All required sections complete")
    else:
        print("\n[FAIL] Missing/incomplete required sections:")
        for section in result['missing_required']:
            print(f"       - {section}")

    # Secrets
    if not result['secrets_found']:
        print("\n[PASS] No potential secrets detected")
    else:
        print("\n[WARN] Potential secrets detected:")
        for secret_type, detail in result['secrets_found']:
            print(f"       - {secret_type}: {detail}")

    # File references
    if result['files_missing']:
        print(f"\n[WARN] {len(result['files_missing'])} referenced file(s) not found:")
        for f in result['files_missing']:
            print(f"       - {f}")
    else:
        print(f"\n[INFO] {result['files_verified']} file reference(s) verified")

    # Recommended sections
    if result['missing_recommended']:
        print(f"\n[INFO] Consider adding these sections:")
        for section in result['missing_recommended']:
            print(f"       - {section}")

    print(f"\n{'='*60}")
    messages = {
        "READY": "Verdict: READY for handoff",
        "BLOCKED": "Verdict: BLOCKED - Remove secrets before handoff",
        "NEEDS_WORK": "Verdict: NEEDS WORK - Complete required sections",
    }
    print(messages[result["verdict"]])


def main():
    parser = argparse.ArgumentParser(
        description="Validate a handoff document: TODO placeholders, required sections, secrets, file references, score.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""exit codes:
  0  verdict READY (score >= 70, no TODOs, required sections complete, no secrets)
  1  verdict NEEDS_WORK or BLOCKED (fix the reported items and re-run)
  2  usage error or handoff file not found (message on stderr)

examples:
  python3 scripts/validate_handoff.py .claude/handoffs/2026-01-15-143022-auth.md
  python3 scripts/validate_handoff.py --json .claude/handoffs/2026-01-15-143022-auth.md""",
    )
    parser.add_argument("handoff_file", help="Path to the handoff markdown file")
    parser.add_argument("--json", action="store_true", help="Print the result as one JSON object on stdout")
    args = parser.parse_args()

    result = validate_handoff(args.handoff_file)
    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(2)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_report(result)
    sys.exit(0 if result["verdict"] == "READY" else 1)


if __name__ == "__main__":
    main()
