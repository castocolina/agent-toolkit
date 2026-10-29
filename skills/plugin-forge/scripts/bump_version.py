#!/usr/bin/env python3
"""
Bump plugin version in both plugin.json and marketplace.json.
"""

import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Literal


VersionPart = Literal["major", "minor", "patch"]


def parse_version(version: str) -> tuple[int, int, int]:
    """Parse semantic version string into tuple."""
    try:
        parts = version.split(".")
        return int(parts[0]), int(parts[1]), int(parts[2])
    except (ValueError, IndexError):
        print(f"❌ Invalid version format: {version}")
        sys.exit(1)


def bump_version(version: str, part: VersionPart) -> str:
    """Bump semantic version."""
    major, minor, patch = parse_version(version)

    if part == "major":
        return f"{major + 1}.0.0"
    elif part == "minor":
        return f"{major}.{minor + 1}.0"
    elif part == "patch":
        return f"{major}.{minor}.{patch + 1}"
    else:
        print(f"❌ Invalid version part: {part}")
        sys.exit(1)


def update_plugin_version(plugin_name: str, marketplace_root: Path, part: VersionPart) -> None:
    """Update both manifests after validating names, paths, and contents."""
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", plugin_name):
        raise ValueError("plugin_name must be a kebab-case identifier")
    plugins_root = (marketplace_root / "plugins").resolve()
    plugin_dir = (plugins_root / plugin_name).resolve()
    if not plugin_dir.is_relative_to(plugins_root):
        raise ValueError("plugin_name escapes plugins directory")

    # Load and validate both manifests before any write.
    plugin_json_path = marketplace_root / "plugins" / plugin_name / ".claude-plugin" / "plugin.json"

    if not plugin_json_path.exists():
        print(f"❌ Plugin manifest not found: {plugin_json_path}")
        sys.exit(1)

    with open(plugin_json_path, "r") as f:
        plugin_data = json.load(f)

    old_version = plugin_data.get("version", "0.0.0")
    new_version = bump_version(old_version, part)
    plugin_data["version"] = new_version

    # Validate marketplace prerequisites before writing either manifest.
    marketplace_json_path = marketplace_root / ".claude-plugin" / "marketplace.json"

    if not marketplace_json_path.exists():
        print(f"❌ Marketplace manifest not found: {marketplace_json_path}")
        sys.exit(1)

    with open(marketplace_json_path, "r") as f:
        marketplace_data = json.load(f)

    plugin_found = False
    for plugin in marketplace_data.get("plugins", []):
        if plugin.get("name") == plugin_name:
            plugin["version"] = new_version
            plugin_found = True
            break

    if not plugin_found:
        print(f"❌ Plugin '{plugin_name}' not found in marketplace manifest")
        sys.exit(1)

    replacements = {plugin_json_path: json.dumps(plugin_data, indent=2) + "\n", marketplace_json_path: json.dumps(marketplace_data, indent=2) + "\n"}
    originals = {path: path.read_bytes() for path in replacements}
    staged = {}
    try:
        for path, content in replacements.items():
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as temp:
                temp.write(content)
                staged[path] = Path(temp.name)
        # Validate staged JSON before replacing either target.
        for temp in staged.values():
            json.loads(temp.read_text())
        try:
            for path, temp in staged.items():
                os.replace(temp, path)
        except OSError:
            for path, original in originals.items():
                path.write_bytes(original)
            raise
    finally:
        for temp in staged.values():
            temp.unlink(missing_ok=True)
    print(json.dumps({"status": "updated", "plugin": plugin_name, "old_version": old_version, "new_version": new_version, "paths": [str(p) for p in replacements]}))


def main():
    parser = argparse.ArgumentParser(description="Bump plugin version")
    parser.add_argument("plugin_name", help="Plugin name")
    parser.add_argument("part", choices=["major", "minor", "patch"], help="Version part to bump")
    parser.add_argument("--marketplace-root", default=".", help="Path to marketplace root directory")

    args = parser.parse_args()

    marketplace_root = Path(args.marketplace_root).resolve()

    update_plugin_version(
        plugin_name=args.plugin_name,
        marketplace_root=marketplace_root,
        part=args.part
    )


if __name__ == "__main__":
    try:
        main()
    except (ValueError, FileNotFoundError, FileExistsError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)
