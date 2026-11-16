# Candidate scan (fixture data standing in for the output of `scripts/run-taze.sh`)

Resolver and lockfile: npm, package-lock.json. No workspace. No peer, ABI or runtime-floor conflict is reported by `npm install --dry-run` for any candidate below.

| Package | Current | Candidate | Change as the scanner labels it |
|---------|---------|-----------|---------------------------------|
| reflect-metadata | 0.1.13 | 0.2.2 | MINOR |
| tslib | 2.6.0 | 2.8.1 | MINOR |
| vue | 3.5.0-rc.1 | 3.5.0-rc.4 | PRERELEASE |
