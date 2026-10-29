#!/usr/bin/env python3
"""AWS icon search script

Search for icon information by service name in references/aws-icons.md.
Extract only the information needed to improve token efficiency.

Usage:
    python find_aws_icon.py <service_name>
    python find_aws_icon.py ec2
    python find_aws_icon.py lambda
    python find_aws_icon.py s3
"""

import re
import sys
from pathlib import Path


def load_icon_data() -> list[dict[str, str]]:
    """Load icon data from aws-icons.md, preserving groups and variants."""
    icons = []
    script_dir = Path(__file__).parent
    aws_icons_path = script_dir.parent / "references" / "aws-icons.md"

    if not aws_icons_path.exists():
        return icons

    content = aws_icons_path.read_text(encoding="utf-8")

    # Extract the service name and resIcon from table rows
    # | Amazon EC2 | mxgraph.aws4.ec2 |
    pattern = r"\|\s*([^|]+?)\s*\|\s*(mxgraph\.aws4\.[a-z0-9_]+)\s*\|"
    for match in re.finditer(pattern, content):
        service_name = match.group(1).strip()
        res_icon = match.group(2).strip()
        kind = "group" if res_icon.rsplit(".", 1)[-1].startswith("group_") else "resourceIcon"
        icons.append({"name": service_name, "icon": res_icon, "kind": kind})

    return icons


def search_icon(query: str) -> list[dict]:
    """Search for icons matching the query"""
    icons = load_icon_data()
    query_lower = query.lower()
    results = []

    for data in icons:
        if query_lower in data["name"].lower() or query_lower in data["icon"].lower():
            results.append(data)

    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python find_aws_icon.py <service_name>")
        print("Example: python find_aws_icon.py ec2")
        sys.exit(1)

    query = sys.argv[1]
    results = search_icon(query)

    if not results:
        print(f"No icons found for: {query}")
        sys.exit(1)

    print(f"Found {len(results)} icon(s) for '{query}':\n")
    for result in results:
        print(f"Service: {result['name']}")
        print(f"{ 'grIcon' if result['kind'] == 'group' else 'resIcon' }: {result['icon']}")
        attribute = "grIcon" if result["kind"] == "group" else "resIcon"
        print(f"Style: shape=mxgraph.aws4.{result['kind']};{attribute}={result['icon']};")
        print()


if __name__ == "__main__":
    main()
