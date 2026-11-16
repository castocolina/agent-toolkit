# Update policy: what each update type gets

Load this when you classify scan results (procedure step 4 of SKILL.md). The auto-apply guardrails (map first, snapshot before any write, manifest and lockfile together, gates per cohort, restore on failure, report) are in SKILL.md steps 5, 7 and 8; this table only decides which targets reach them.

| Update type | Version change | Action |
|-------------|----------------|--------|
| **Fixed** | Exact constraint by ecosystem: npm and pnpm an exact version string (`1.2.3`, no range operator); Cargo `=1.2.3`; Python `==1.2.3`; Go modules use minimum version selection, so a `go.mod` requirement is a deliberate pin only when the user or a comment says so (https://go.dev/ref/mod#minimal-version-selection, checked 2026-11-15) | Skip (intentionally pinned); unchanged unless the user asks to move it. A Go requirement nobody marked as a pin is a minimum, not a pin, and is classified by the change size like any other |
| **PATCH** | `1.2.3` to `1.2.4` | Auto-apply when the dependency is stable (not 0.x, not a prerelease), not exact-pinned, the target-specific resolver output and the declared runtime range show no peer or runtime-floor conflict, and ABI compatibility is established (from the package's release notes when it ships a native or prebuilt binary); otherwise ask per target |
| **MINOR** | `1.2.3` to `1.3.0` | Same as PATCH: auto-apply the stable, unpinned ones with no peer or runtime-floor conflict and an established ABI compatibility; ask per target for the rest |
| **MAJOR** | `1.2.3` to `2.0.0` | Never auto-apply: ask individually, one question per package with current to target version and the release notes |
| **0.x** (any change) | `0.21.4` to `0.22.0` | Ask per target: in a 0.x version anything may change at any time (https://semver.org/#spec-item-4, checked 2026-11-16), so even a patch or minor change is not safe by its size |
| **Prerelease** (any change) | `2.0.0-rc.1` to `2.0.0-rc.2` | Ask per target; a prerelease carries no compatibility promise |
| **Failed peer, ABI or runtime check** | Any size | Ask per target: the target-specific resolver output and the declared runtime range (peer and runtime floor) and the release notes of a package with a native or prebuilt binary (ABI), not the version number, decide; an ABI compatibility that cannot be established is ask per target |

What stays unchanged unless the user asks: exact pins, and any target the user asked to be asked about. The user can always say "ask first", which turns every row into ask per target.

Package names never imply approval. An earlier "auto-approve list" of packages with frequent majors (an icon library, the `@types/*` packages) is not kept: a `@types/*` major tracks the runtime it describes and is not generally safe, so each major is asked on its own.
