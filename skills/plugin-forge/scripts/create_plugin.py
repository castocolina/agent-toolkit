#!/usr/bin/env python3
"""
Create a new Claude Code plugin with proper directory structure and manifests.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path


RESERVED_PREFIXES = ("claude-", "anthropic-", "anthropics-", "cc-plugin-")
RESERVED_NAMES = {"claude", "anthropic", "anthropics", "claude-code", "claude-mods"}


def check_reserved_name(name: str) -> str | None:
    """Return why `claude plugin validate` would reject the name as passing for Anthropic's own, else None."""
    if name in RESERVED_NAMES or name.startswith(RESERVED_PREFIXES) or re.search(r"(^|-)official-(claude|anthropic)|(claude|anthropic)s?-official(-|$)", name):
        return (f"Plugin name '{name}' is reserved: claude plugin validate rejects names that pass as Anthropic's own "
                f"(exact claude/anthropic/claude-code/claude-mods, prefixes {', '.join(RESERVED_PREFIXES)}, or 'official' beside claude/anthropic). "
                "Choose another name, e.g. drop the prefix.")
    return None


def validate_marketplace(data, path: Path) -> None:
    """Reject a marketplace.json that Claude Code would refuse, before any write."""
    problems = []
    if not isinstance(data, dict):
        raise ValueError(f"Invalid marketplace manifest {path}: top level must be a JSON object")
    if not isinstance(data.get("name"), str) or not data["name"]:
        problems.append("'name' must be a non-empty string")
    owner = data.get("owner")
    if not isinstance(owner, dict) or not isinstance(owner.get("name"), str) or not owner["name"]:
        problems.append("'owner' must be an object with a non-empty 'name'")
    plugins = data.get("plugins")
    if not isinstance(plugins, list):
        problems.append("'plugins' must be an array")
    else:
        for i, entry in enumerate(plugins):
            if not isinstance(entry, dict) or not isinstance(entry.get("name"), str) or "source" not in entry:
                problems.append(f"plugins[{i}] must be an object with a string 'name' and a 'source'")
    if problems:
        raise ValueError(f"Invalid marketplace manifest {path}: " + "; ".join(problems))


def create_plugin_structure(plugin_name: str, marketplace_root: Path, author_name: str, author_email: str, description: str, keywords: list[str], category: str = "productivity", dry_run: bool = False) -> None:
    """Create complete plugin directory structure with manifests."""

    # Reject traversal and absolute paths before touching the filesystem.
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", plugin_name):
        raise ValueError("plugin_name must be a kebab-case identifier")
    plugins_root = (marketplace_root / "plugins").resolve()
    plugin_dir = (plugins_root / plugin_name).resolve()
    if not plugin_dir.is_relative_to(plugins_root):
        raise ValueError("plugin_name escapes plugins directory")
    if plugin_dir.exists():
        raise FileExistsError(f"Plugin directory already exists: {plugin_dir}")
    reserved = check_reserved_name(plugin_name)
    if reserved:
        raise ValueError(reserved)

    marketplace_json_path = marketplace_root / ".claude-plugin" / "marketplace.json"

    if not marketplace_json_path.exists():
        raise FileNotFoundError(f"Marketplace manifest not found: {marketplace_json_path}")

    with open(marketplace_json_path, "r") as f:
        marketplace_data = json.load(f)
    validate_marketplace(marketplace_data, marketplace_json_path)

    for plugin in marketplace_data["plugins"]:
        if plugin.get("name") == plugin_name:
            raise FileExistsError(f"Plugin '{plugin_name}' already exists in marketplace manifest")

    plugin_entry = {
        "name": plugin_name,
        "source": f"./plugins/{plugin_name}",
        "description": description,
        "keywords": keywords,
        "category": category
    }
    plugin_config_dir = plugin_dir / ".claude-plugin"
    plugin_json_path = plugin_config_dir / "plugin.json"
    readme_path = plugin_dir / "README.md"
    paths = [str(plugin_json_path), str(readme_path), str(marketplace_json_path)]
    if dry_run:
        print(json.dumps({"status": "dry-run", "plugin": plugin_name, "paths": paths, "marketplace_entry": plugin_entry}))
        return

    # Create directory structure
    commands_dir = plugin_dir / "commands"
    skills_dir = plugin_dir / "skills"

    plugin_config_dir.mkdir(parents=True, exist_ok=True)
    commands_dir.mkdir(parents=True, exist_ok=True)
    skills_dir.mkdir(parents=True, exist_ok=True)

    # Create plugin.json
    plugin_manifest = {
        "name": plugin_name,
        "version": "0.1.0",
        "description": description,
        "author": {
            "name": author_name,
            "email": author_email
        },
        "keywords": keywords
    }

    with open(plugin_json_path, "w") as f:
        json.dump(plugin_manifest, f, indent=2)

    print(f"Created plugin manifest: {plugin_json_path}", file=sys.stderr)

    # Create README.md
    readme_content = f"""# {plugin_name}

{description}

## Installation

```bash
/plugin marketplace add <marketplace-source>
/plugin install {plugin_name}@{marketplace_data.get('name', '<marketplace-name>')}
```

## Features

- TODO: List features here

## Usage

TODO: Add usage examples
"""

    with open(readme_path, "w") as f:
        f.write(readme_content)

    print(f"Created README: {readme_path}", file=sys.stderr)

    # Update marketplace.json
    marketplace_data["plugins"].append(plugin_entry)

    with open(marketplace_json_path, "w") as f:
        json.dump(marketplace_data, f, indent=2)

    print(f"Updated marketplace manifest: {marketplace_json_path}", file=sys.stderr)
    print(json.dumps({"status": "created", "plugin": plugin_name, "paths": paths, "version": "0.1.0"}))



def main():
    parser = argparse.ArgumentParser(
        description="Create a new Claude Code plugin under <marketplace-root>/plugins/ and register it",
        epilog="Prints one JSON object on stdout, progress on stderr. Exit 0 on success; exit 2 on invalid "
        "input, a missing marketplace manifest, or an existing plugin, with nothing written.",
    )
    parser.add_argument("plugin_name", help="Plugin name (kebab-case)")
    parser.add_argument("--marketplace-root", default=".", help="Path to marketplace root directory")
    parser.add_argument("--author-name", required=True, help="Plugin author name")
    parser.add_argument("--author-email", required=True, help="Plugin author email")
    parser.add_argument("--description", required=True, help="Plugin description")
    parser.add_argument("--keywords", required=True, help="Comma-separated keywords")
    parser.add_argument("--category", default="productivity", help="Plugin category (default: productivity)")
    parser.add_argument("--dry-run", action="store_true", help="Validate and print the planned paths and marketplace entry without writing")

    args = parser.parse_args()

    marketplace_root = Path(args.marketplace_root).resolve()
    keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]

    create_plugin_structure(
        plugin_name=args.plugin_name,
        marketplace_root=marketplace_root,
        author_name=args.author_name,
        author_email=args.author_email,
        description=args.description,
        keywords=keywords,
        category=args.category,
        dry_run=args.dry_run
    )


if __name__ == "__main__":
    try:
        main()
    except (ValueError, FileNotFoundError, FileExistsError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)
