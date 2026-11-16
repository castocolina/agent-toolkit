# Candidate scan (fixture data standing in for the output of `scripts/run-taze.sh`)

Resolver and lockfile: npm, package-lock.json. No workspace. The project runs on Node 20.

| Package | Current | Candidate | Change as the scanner labels it |
|---------|---------|-----------|---------------------------------|
| reflect-metadata | 0.1.13 | 0.2.2 | MINOR |
| tslib | 2.6.0 | 2.8.1 | MINOR |
| vue | 3.5.0-rc.1 | 3.5.0-rc.4 | PRERELEASE |

Target-specific dry runs (fixture data, one per candidate):

- `npm install reflect-metadata@0.2.2 --dry-run`: no peer conflict; declared `engines.node` range covers the project's Node 20 (a 0.x version, so it is still asked per target)
- `npm install tslib@2.8.1 --dry-run`: no peer conflict; declared `engines.node` range covers the project's Node 20
- `npm install vue@3.5.0-rc.4 --dry-run`: no peer conflict; declared `engines.node` range covers the project's Node 20 (a prerelease, so it is still asked per target)

Native or prebuilt binary (fixture data, one per candidate):

- reflect-metadata: none, pure JavaScript
- tslib: none, pure JavaScript
- vue: none, pure JavaScript
