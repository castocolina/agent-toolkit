# Native manager commands

Use these only after confirming the manager owns the manifest and lockfile. Discovery commands do not apply changes. Select and approve exact targets before invoking update commands; inspect resulting diffs and run project gates after each cohort.

| Ecosystem | Discover | Apply an approved target |
|---|---|---|
| Go modules | `go list -m -u all` | `go get module@version`, then `go mod tidy` |
| Rust/Cargo | `cargo outdated` | Update the owning `Cargo.toml` dependency/workspace constraint to the approved target if it is outside the current range; then `cargo update -p crate --precise version` |
| Ruby/Bundler | `bundle outdated` | Set the approved target constraint in `Gemfile`, then run `bundle update --conservative gem` |
| Maven | `mvn versions:display-dependency-updates` | `mvn versions:use-dep-version -Dincludes=groupId:artifactId -DdepVersion=version -DforceVersion=true` |
| .NET | `dotnet list package --outdated` | `dotnet add package PackageName --version approved-version` |

For Cargo and Bundler, verify the lockfile resolves exactly to each approved target after the targeted update; if not, stop and report rather than accepting a nearby version. For Gradle, use the repository's configured version catalog/plugin and wrapper; do not substitute Maven commands. Security scanners are ecosystem-specific (`govulncheck`, `cargo audit`, `bundle audit`, Maven dependency-check, or `dotnet list package --vulnerable`). Do not use broad upgrade-all commands unless the user has approved their exact target scope and range behavior.
