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
    """Parse a plain MAJOR.MINOR.PATCH version; prerelease/build suffixes are rejected."""
    if not isinstance(version, str) or not re.fullmatch(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)", version):
        raise ValueError(f"Invalid version {version!r}: expected MAJOR.MINOR.PATCH without prerelease or build suffix")
    major, minor, patch = (int(x) for x in version.split("."))
    return major, minor, patch


def bump_version(version: str, part: VersionPart) -> str:
    """Bump semantic version."""
    major, minor, patch = parse_version(version)
    if part == "major":
        return f"{major + 1}.0.0"
    if part == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


def update_plugin_version(plugin_name: str, marketplace_root: Path, part: VersionPart) -> None:
    """Bump the version where Claude Code reads it (plugin.json, else the marketplace entry) after validating both."""
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", plugin_name):
        raise ValueError("plugin_name must be a kebab-case identifier")
    plugins_root = (marketplace_root / "plugins").resolve()
    plugin_dir = (plugins_root / plugin_name).resolve()
    if not plugin_dir.is_relative_to(plugins_root):
        raise ValueError("plugin_name escapes plugins directory")

    # Load and validate both manifests before any write.
    plugin_json_path = marketplace_root / "plugins" / plugin_name / ".claude-plugin" / "plugin.json"

    if not plugin_json_path.exists():
        raise FileNotFoundError(f"Plugin manifest not found: {plugin_json_path}. bump_version.py requires plugin.json; "
                                "for a manifest-less plugin edit an existing marketplace-entry version by hand, or leave a SHA-versioned plugin unbumped.")

    with open(plugin_json_path, "r") as f:
        plugin_data = json.load(f)

    if not isinstance(plugin_data, dict):
        raise ValueError(f"Invalid plugin manifest {plugin_json_path}: top level must be a JSON object")

    marketplace_json_path = marketplace_root / ".claude-plugin" / "marketplace.json"
    if not marketplace_json_path.exists():
        raise FileNotFoundError(f"Marketplace manifest not found: {marketplace_json_path}")
    with open(marketplace_json_path, "r") as f:
        marketplace_data = json.load(f)
    plugins = marketplace_data.get("plugins") if isinstance(marketplace_data, dict) else None
    if not isinstance(plugins, list):
        raise ValueError(f"Invalid marketplace manifest {marketplace_json_path}: 'plugins' must be an array")
    entry = next((p for p in plugins if isinstance(p, dict) and p.get("name") == plugin_name), None)
    if entry is None:
        raise ValueError(f"Plugin '{plugin_name}' not found in marketplace manifest")

    # Claude Code resolves the version from plugin.json first, then the marketplace entry, then the commit SHA.
    pinned_in_manifest = "version" in plugin_data
    if pinned_in_manifest:
        old_version = plugin_data["version"]
    elif "version" in entry:
        old_version = entry["version"]
    else:
        raise ValueError(f"Neither {plugin_json_path} nor the '{plugin_name}' marketplace entry has a version: "
                         "the plugin is versioned by commit SHA, so there is nothing to bump. "
                         "Push the change, or add a version to plugin.json first to pin releases.")
    new_version = bump_version(old_version, part)
    replacements = {}
    if pinned_in_manifest:
        plugin_data["version"] = new_version
        replacements[plugin_json_path] = json.dumps(plugin_data, indent=2) + "\n"
    if "version" in entry:  # keep an existing entry version equal; never add one (docs: set version in one place)
        entry["version"] = new_version
        replacements[marketplace_json_path] = json.dumps(marketplace_data, indent=2) + "\n"

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
    parser = argparse.ArgumentParser(
        description="Bump a plugin version in plugin.json and/or its marketplace entry, wherever it is set",
        epilog="Prints one JSON object on stdout. Exit 0 on success; exit 2 on invalid input or manifest, "
        "with the message on stderr and both manifests unchanged.",
    )
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
