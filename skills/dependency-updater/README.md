# Dependency Updater

Smart dependency management for any programming language with automatic detection and approval-gated updates.

## Purpose

The Dependency Updater skill provides intelligent, language-agnostic dependency management that:

- **Auto-detects your project type** by scanning for package files (package.json, go.mod, Cargo.toml, etc.)
- **Asks for approval per target version** before any write; minor and patch updates are not applied automatically, because even a nominal minor update can break compatibility
- **Prompts for major updates individually** to prevent breaking changes
- **Respects intentionally pinned versions** by skipping fixed dependencies
- **Runs security audits** to identify vulnerabilities
- **Diagnoses and fixes** common dependency issues

This skill eliminates the manual work of checking for outdated packages across different ecosystems while maintaining safety through semantic versioning awareness.

## When to Use

Use this skill when you want to:

| Scenario | Trigger Phrases |
|----------|-----------------|
| Update dependencies | "update dependencies", "update deps", "update my packages" |
| Check for outdated packages | "check for outdated packages", "what packages need updating" |
| Fix dependency problems | "fix my dependency problems", "resolve dependency conflicts" |
| Security audit | "audit dependencies for vulnerabilities", "check for security issues" |
| Diagnose issues | "diagnose dependency issues", "why won't my dependencies install" |

**Quick Start:**
```
update my dependencies
```

The skill will auto-detect your project type and propose updates for your approval.

## Supported Languages

| Language | Package File | Update Tool | Audit Tool |
|----------|--------------|-------------|------------|
| Node.js | package.json | `taze` | `npm audit` |
| Python | requirements.txt, pyproject.toml, Pipfile | `pip-review` (see the note under Recommended Tools) | `safety scan`, `pip-audit` |
| Go | go.mod | `go get module@version`, then `go mod tidy` | `govulncheck` |
| Rust | Cargo.toml | `cargo update -p crate --precise version` | `cargo audit` |
| Ruby | Gemfile | set the Gemfile constraint, then `bundle update --conservative gem` | `bundle audit` |
| Java | pom.xml, build.gradle | `mvn versions:*` | `mvn org.owasp:dependency-check-maven:check` |
| .NET | *.csproj | `dotnet add package PackageName --version approved-version` (`dotnet outdated` only as optional discovery) | `dotnet list package --vulnerable` |

## How It Works

The skill follows a constraint-first 6-step workflow (the full rules are in SKILL.md):

```
1. INSPECT AND DETECT
   Preserve unrelated edits; identify the manifest, owning package manager,
   lockfile, runtime and workspace layout

2. CLASSIFY CONSTRAINTS
   Use the manager's own constraint grammar; exact pins stay unchanged

3. FORM COMPATIBLE COHORTS
   Group coupled workspace packages and peer/runtime constraints

4. SCAN AND ASK
   Scan candidates, read release notes, and apply only target versions the
   user approved (every breaking target needs approval)

5. UPDATE MANIFEST AND LOCKFILE TOGETHER
   Use the owning package manager only

6. VERIFY
   Run install, tests, type checks, build and security audit after each
   cohort; stop on the first failure and ask
```

### Update Classification

| Update Type | Version Change | Action |
|-------------|----------------|--------|
| **Fixed** | Exact constraint by ecosystem: npm and pnpm an exact version string (`1.2.3`, no range operator); Cargo `=1.2.3`; Python `==1.2.3`; Go modules use minimum version selection, so a `go.mod` requirement is a deliberate pin only when the user or a comment says so (https://go.dev/ref/mod#minimal-version-selection, checked 2026-11-15) | Skip (intentionally pinned); a Go requirement nobody marked as a pin needs approval for a proposed upgrade like any other |
| **PATCH** | `1.2.3` to `1.2.4` | Propose; apply only after approval of the target version |
| **MINOR** | `1.2.3` to `1.3.0` | Propose; apply only after approval (a 0.x or prerelease minor can still break) |
| **MAJOR** | `1.2.3` to `2.0.0` | Prompt user individually |

## Key Features

### Language-Agnostic Detection

The skill automatically identifies your project by scanning for common package files:

- `package.json` - Node.js (npm/yarn/pnpm)
- `requirements.txt` / `pyproject.toml` / `Pipfile` - Python
- `go.mod` - Go
- `Cargo.toml` - Rust
- `Gemfile` - Ruby
- `pom.xml` / `build.gradle` - Java/Kotlin
- `*.csproj` - .NET

### Safe-by-Default Updates

- Every update needs approval of its target version; minor and patch updates are not applied automatically
- Major updates require explicit approval (may contain breaking changes)
- Fixed/pinned versions are never modified

### Security Auditing

Built-in security vulnerability scanning for each ecosystem:
- Identifies vulnerabilities by severity (Critical, High, Moderate, Low)
- Recommends appropriate response times based on severity
- Integrates with ecosystem-specific audit tools

### Dependency Diagnosis

Troubleshoots common issues:
- Version conflicts
- Peer dependency problems
- Security vulnerabilities
- Unused dependencies
- Duplicate packages

## Usage Examples

### Basic Update

```
update my dependencies
```

The skill will scan your project, propose candidate updates, and apply only the target versions you approve.

### Security-Focused Audit

```
audit my dependencies for security issues
```

Runs security scanners and reports vulnerabilities by severity.

### Diagnose Problems

```
my npm install keeps failing, diagnose the issue
```

Analyzes dependency tree, identifies conflicts, and suggests fixes.

### Node.js Specific

The scripts live in this skill's directory, not in your project: resolve them from the directory that holds SKILL.md (for an installed skill, `${CLAUDE_PLUGIN_ROOT}/skills/dependency-updater/scripts/` or `$HOME/.claude/skills/dependency-updater/scripts/`, whichever exists) and run them with the target project as the working directory. In the examples, `$SKILL` stands for that skill directory.

```bash
# Check prerequisites
"$SKILL/scripts/check-tool.sh" taze "npm install -g taze"

# Run taze directly
"$SKILL/scripts/run-taze.sh"

# Run in monorepo mode
"$SKILL/scripts/run-taze.sh" -r
```

A candidate scan (no `--write`) prints `{"status":"ok","candidates":<taze JSON>}`; a write run, or taze output that is not valid JSON, prints the text report in an `output` field instead.

## Prerequisites

### General Requirements

Each language ecosystem requires its standard package manager:
- Node.js: npm, yarn, or pnpm
- Python: pip
- Go: go modules
- Rust: cargo
- Ruby: bundler
- Java: Maven or Gradle
- .NET: dotnet CLI

### Recommended Tools

For the best experience, install these optional but recommended tools:

| Language | Tool | Install Command |
|----------|------|-----------------|
| Node.js | taze | `npm install -g taze` |
| Python | pip-review | `pip install pip-review` |
| Python | pip-audit | `pip install pip-audit` |
| Go | govulncheck | `go install golang.org/x/vuln/cmd/govulncheck@latest` |
| Rust | cargo-audit | `cargo install cargo-audit` |
| Ruby | bundler-audit | `gem install bundler-audit` |
| .NET | dotnet-outdated | `dotnet tool install --global dotnet-outdated-tool` |

Notes (checked 2026-11-15):

- `pip-review` is a lightly maintained tool: its last release is 1.3.0 (2022-11-29) and its README asks for a new maintainer (https://pypi.org/pypi/pip-review/json, https://github.com/jgonggrijp/pip-review). Its `--auto` flag upgrades every outdated package, which the skill's one-package-at-a-time rule forbids; prefer `pip list --outdated` and update one approved package at a time.
- `safety scan` is the current Safety CLI command (it needs a login); `safety check` is the legacy command (https://github.com/pyupio/safety). `pip-audit` needs no account.

## Output

### Update Summary

After running, you will see:
- Candidate updates with the target version proposed for each
- The approval requested for each target, with every major update asked individually
- Final package count and versions
- Security audit results

### Security Audit Results

Vulnerabilities are reported with severity levels. The response times are suggestions subordinate to your own priorities, not SLAs:

| Severity | Recommended Response |
|----------|---------------------|
| Critical | Fix immediately |
| High | Fix within 24 hours |
| Moderate | Fix within 1 week |
| Low | Fix in next release |

## Best Practices

### Do

- **Commit lock files** - Always commit package-lock.json, yarn.lock, go.sum, etc.
- **Review major updates** - Check changelogs before approving major version bumps
- **Run tests after updates** - Verify your application still works
- **Address security issues promptly** - Prioritize by severity level
- **Use version ranges appropriately** - `^` for active libraries, `~` for stable ones, exact for critical dependencies

### Avoid

- **Don't auto-approve all majors** - Breaking changes require code modifications
- **Don't ignore security alerts** - Vulnerabilities can be exploited
- **Don't update fixed versions** - They were pinned for a reason
- **Don't skip the lock file** - It ensures reproducible builds

### Version Range Strategy

```json
{
  "dependencies": {
    "critical-lib": "1.2.3",      // Exact for critical dependencies
    "stable-lib": "~1.2.3",       // Patch only for stable libraries
    "modern-lib": "^1.2.3"        // Minor OK for actively maintained
  }
}
```

## Emergency Fixes

When dependencies are completely broken. These resets are destructive and are not a first-line fix: diagnose first with the manager's explain/tree command, get explicit approval and save a recoverable snapshot (see SKILL.md, Recovery and security).

### Node.js - Nuclear Reset

```bash
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

### Python - Clean Virtual Environment

```bash
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Go - Reset Modules

```bash
go mod tidy
```

`go mod tidy` already adds missing and removes unneeded `go.sum` entries, so deleting `go.sum` is unnecessary and discards recorded checksums (checked 2026-11-15, `go help mod tidy`).

## Verification Checklist

After running updates, verify:

- [ ] Updates scanned without errors
- [ ] Every applied update matches an approved target version
- [ ] Major updates prompted individually
- [ ] Fixed versions remained untouched
- [ ] Lock file updated
- [ ] Install command succeeded
- [ ] Security audit passed (or issues noted)
- [ ] Tests pass
- [ ] Application runs correctly

## Related Tools

| Tool | Language | Purpose | Link |
|------|----------|---------|------|
| taze | Node.js | Smart dependency updates | [GitHub](https://github.com/antfu-collective/taze) |
| npm-check-updates | Node.js | Alternative to taze | [GitHub](https://github.com/raineorshine/npm-check-updates) |
| pip-review | Python | Interactive pip updates | [GitHub](https://github.com/jgonggrijp/pip-review) |
| cargo-edit | Rust | Cargo dependency management | [GitHub](https://github.com/killercup/cargo-edit) |
| bundler-audit | Ruby | Security auditing | [GitHub](https://github.com/rubysec/bundler-audit) |

## Credits

Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy.

Tool commands and flags were checked on 2026-11-15 against the official documentation of each tool:

- taze: Anthony Fu (antfu-collective), https://github.com/antfu-collective/taze
- npm audit and overrides: npm (GitHub), https://docs.npmjs.com/cli/commands/npm-audit
- pnpm audit: pnpm, https://pnpm.io/11.x/cli/audit
- Yarn resolutions and `yarn npm audit`: Yarn, https://yarnpkg.com/configuration/manifest
- Go vulnerability management: The Go Authors, https://go.dev/doc/security/vuln/
- cargo update: The Rust Project, https://doc.rust-lang.org/cargo/commands/cargo-update.html
- cargo-audit: RustSec, https://github.com/rustsec/rustsec/tree/main/cargo-audit
- bundle update: Bundler team, https://guides.rubygems.org/command-reference/bundle-update/
- bundler-audit: RubySec, https://github.com/rubysec/bundler-audit
- versions:use-dep-version: MojoHaus, https://www.mojohaus.org/versions/versions-maven-plugin/use-dep-version-mojo.html
- dependency-check-maven: OWASP, https://github.com/dependency-check/DependencyCheck#maven-plugin
- dotnet package list and add: Microsoft, https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-list-package
- dotnet-outdated: dotnet-outdated contributors, https://github.com/dotnet-outdated/dotnet-outdated
- Safety CLI: Safety Cybersecurity, https://github.com/pyupio/safety
- pip-review: Joris Gonggrijp, https://github.com/jgonggrijp/pip-review

## License

MIT
