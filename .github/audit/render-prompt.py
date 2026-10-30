#!/usr/bin/env python3
"""Render an audit prompt template with workspace-contained evidence paths.

The audit workflows hand Copilot prompts that reference evidence by absolute
path. The no-shell Copilot agent (read/write tools only) can only open paths
inside the workspace, so every path argument must live inside the current
working directory: `--path` values must already exist, `--out-path` values may
still be unwritten. Rendering fails closed on unknown or leftover `{{PLACEHOLDER}}`
markers so a typo never reaches the model.

Usage:
  render-prompt.py TEMPLATE OUTPUT [--path KEY=PATH]... [--out-path KEY=PATH]... [--text KEY=VALUE]...
"""
import argparse
import re
import sys
from pathlib import Path

PLACEHOLDER = re.compile(r"\{\{([A-Z_][A-Z0-9_]*)\}\}")


def parse_pairs(pairs: list[str], flag: str) -> dict[str, str]:
    parsed = {}
    for pair in pairs:
        key, sep, value = pair.partition("=")
        if not sep or not key:
            raise ValueError(f"{flag} expects KEY=VALUE, got: {pair}")
        if key in parsed:
            raise ValueError(f"{flag} key given twice: {key}")
        parsed[key] = value
    return parsed


def contained(path: Path, workspace: Path) -> bool:
    return path.resolve().is_relative_to(workspace)


def render(template: str, arguments: dict[str, str]) -> str:
    text = template
    for key, value in arguments.items():
        text = text.replace("{{" + key + "}}", value)
    leftovers = sorted(set(PLACEHOLDER.findall(text)))
    if leftovers:
        raise ValueError("unresolved placeholders: " + ", ".join("{{%s}}" % key for key in leftovers))
    return text


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("template", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--path", action="append", default=[], metavar="KEY=PATH",
                        help="replace {{KEY}} with an existing path inside the workspace")
    parser.add_argument("--out-path", action="append", default=[], metavar="KEY=PATH",
                        help="replace {{KEY}} with a path inside the workspace that may not exist yet")
    parser.add_argument("--text", action="append", default=[], metavar="KEY=VALUE",
                        help="replace {{KEY}} with a literal value")
    args = parser.parse_args(argv)
    workspace = Path.cwd().resolve()
    try:
        paths = parse_pairs(args.path, "--path")
        out_paths = parse_pairs(args.out_path, "--out-path")
        texts = parse_pairs(args.text, "--text")
        overlap = (set(paths) | set(out_paths)) & set(texts)
        if overlap:
            raise ValueError("key given as both path and text: " + ", ".join(sorted(overlap)))
        resolved: dict[str, str] = {}
        for key, value in paths.items():
            target = Path(value).resolve()
            if not contained(target, workspace):
                raise ValueError(f"{key}: path is outside the workspace ({value}); the no-shell agent cannot read it")
            if not target.exists():
                raise ValueError(f"{key}: evidence path does not exist ({value})")
            resolved[key] = str(target)
        for key, value in out_paths.items():
            target = Path(value).resolve()
            if not contained(target, workspace):
                raise ValueError(f"{key}: output path is outside the workspace ({value})")
            resolved[key] = str(target)
        resolved.update(texts)
        if not args.template.is_file():
            raise ValueError(f"template not found: {args.template}")
        text = render(args.template.read_text(encoding="utf-8"), resolved)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    except ValueError as exc:
        print(f"render-prompt: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
