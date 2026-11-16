#!/usr/bin/env python3
"""Look up draw.io AWS icon styles by service name in references/aws-icons.md.

Prints only the matching rows, so the full table never enters the context.
Results go to stdout; counts and errors go to stderr.
"""

import argparse
import json
import re
import sys
from pathlib import Path

TABLE = Path(__file__).resolve().parent.parent / "references" / "aws-icons.md"
# | Amazon EC2 | mxgraph.aws4.ec2 |
ROW_RE = re.compile(r"\|\s*([^|]+?)\s*\|\s*(mxgraph\.aws4\.[a-z0-9_]+)\s*\|")


def load_icon_data(table: Path = TABLE) -> list[dict[str, str]]:
    """Every table row, keeping duplicate names (variants) and group icons."""
    icons = []
    for name, icon in ROW_RE.findall(table.read_text(encoding="utf-8")):
        kind = "group" if icon.rsplit(".", 1)[-1].startswith("group_") else "resourceIcon"
        attribute = "grIcon" if kind == "group" else "resIcon"
        icons.append({"name": name.strip(), "icon": icon, "kind": kind,
                      "style": f"shape=mxgraph.aws4.{kind};{attribute}={icon};"})
    return icons


def search_icon(query: str, icons: list[dict[str, str]]) -> list[dict[str, str]]:
    """Case-insensitive substring match on the service name or the icon id."""
    q = query.lower()
    return [d for d in icons if q in d["name"].lower() or q in d["icon"].lower()]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Find draw.io AWS icon styles (mxgraph.aws4.*) by service name.",
        epilog="examples:\n  find_aws_icon.py lambda\n  find_aws_icon.py --json \"API Gateway\"\n"
               "exit: 0 found, 1 no match, 2 usage error or missing table",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("query", help="service name or icon id fragment, case-insensitive")
    parser.add_argument("--json", action="store_true",
                        help="print a JSON array of {name, icon, kind, style}")
    args = parser.parse_args()

    if not TABLE.is_file():
        print(f"icon table not found: {TABLE}", file=sys.stderr)
        return 2
    results = search_icon(args.query, load_icon_data())

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            attribute = "grIcon" if r["kind"] == "group" else "resIcon"
            print(f"Service: {r['name']}\n{attribute}: {r['icon']}\nStyle: {r['style']}\n")
    if not results:
        print(f"No icons found for: {args.query}", file=sys.stderr)
        return 1
    print(f"Found {len(results)} icon(s) for '{args.query}'", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
