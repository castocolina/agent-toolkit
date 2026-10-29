---
name: crafting-effective-readmes
description: Write, update, or audit README.md files using audience-appropriate guidance for open-source, internal, personal, and config repositories. Use for project introductions, quick-start paths, capability updates, or checking claims against repository behavior, even when asked to fix the docs. Not for standalone API references, user manuals, changelogs, contributor guides, or general prose outside a README.
---

# Crafting Effective READMEs

A README should get its intended reader to a supported first success, then route secondary readers to the right detail.

## Workflow

1. Infer task from the request: create/write → Creating; add → Adding; update → Updating; review/audit → Reviewing. Ask only if ambiguity materially changes the result.
2. Identify project type from evidence: target under `~/.config` or dotfiles repo → Config; LICENSE and CI → likely OSS; private employer remote → Internal; no remote → Personal. If signals conflict, ask rather than assuming.
3. Identify reader roles and each role's first successful outcome. Derive prerequisites from repository evidence (manifests, scripts, CI, source, configuration); present the shortest supported path first. Move maintainer/operator detail out of the first-use path.
4. For type-specific sections, read `references/section-checklist.md`; choose the corresponding `templates/` file only when creating or substantially restructuring. Before presenting a draft, read `references/style-guide.md`. Read `references/using-references.md` only when deeper guidance is requested.
5. Verify all commands, versions, badges, links, and capability claims against source. Do not invent missing facts. Creating: fill each chosen template section or mark it N/A. Updating: show the changed sections/diff. Reviewing: flag each unsupported or stale claim with evidence and a suggested correction.
6. Ask a closing question only when a consequential fact remains unresolved; otherwise deliver the result directly.

## Boundaries

Never use badges or links to projects/packages that do not exist. Select badges for the actual ecosystem, verify license before stating it, and include contribution links only if their targets exist. Do not document install steps you have not run or verified against project configuration. Check generated-region markers before editing; preserve regions maintained by another tool.

## References

- `references/section-checklist.md`: after identifying project type, when choosing sections.
- `references/style-guide.md`: before presenting a draft or audit.
- `references/using-references.md`: only for deeper README guidance requested or needed.
- `templates/oss.md`, `templates/personal.md`, `templates/internal.md`, `templates/xdg-config.md`: only when creating or restructuring that project type.
