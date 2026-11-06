# Sections by Project Type

Every type starts with a name, a one-sentence description of what it does and for whom, and the shortest supported first-use path. The matrix and the per-type notes cover only what differs.

| Section | OSS | Personal | Internal | Config |
|---------|-----|----------|----------|--------|
| Badges | Yes | Optional | No | No |
| Installation | Yes | Yes | Yes | No |
| Usage/Examples | Yes | Yes | Yes | Brief |
| What's Here | No | No | No | Yes |
| How to Extend | No | No | Optional | Yes |
| Contributing | Yes | Optional | Yes | No |
| License | Yes | Optional | No | No |
| Architecture | Optional | No | Yes | No |
| Gotchas/Notes | Optional | Optional | Yes | Yes |
| Last Reviewed | No | No | Optional | Yes |

## OSS

- Installation shows the published install first (registry name from the manifest), then "from source" only if users need it. Requirements state the supported runtime range from the manifest or CI matrix.
- Usage gives one complete, copy-pasteable example of the most common task, with its real output.
- Contributing splits into development setup and the test command CI runs; link `CONTRIBUTING.md` only if it exists.
- License names the SPDX identifier from LICENSE or the manifest, and links the file.

## Personal

- Audience is future-you plus portfolio viewers: what it does and why you built it, a demo link or screenshot if visual, the tech stack with a one-line reason per choice.
- "How it works" covers only the interesting part (an algorithm, a trick), and "what I learned" is optional.
- License is optional; say "personal project" if none.

## Internal

- Header lines: owning team or channel, and on-call contact.
- Dependencies: upstream services this needs and downstream services that need it.
- Environment variables as a table of variable, purpose, and where to get the value (vault path, secret manager); never real values.
- Prerequisites include access needs (VPN, groups, internal registries), not only tools.
- Key files table, deployment or a link to it, an environments table (URL per environment), runbooks for common operations, and troubleshooting as symptom, cause, fix.

## Config (dotfiles, `~/.config`, script folders)

- Audience is a confused future-you. Put `> Last reviewed: YYYY-MM-DD` under the title.
- "What's Here" is a path-to-purpose table; give a subdirectory its own paragraph only when it is complex.
- "How to Extend" is one numbered recipe per kind of addition (a new shell function, a new editor plugin).
- Gotchas record load order, files generated or managed by another tool that must not be edited by hand, and machine-specific overrides.
- Note how the directory is synced or backed up, if it is.
