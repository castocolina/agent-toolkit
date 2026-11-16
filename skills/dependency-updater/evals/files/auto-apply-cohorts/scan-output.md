# Candidate scan (fixture data standing in for the output of `scripts/run-taze.sh`)

Resolver and lockfile: npm, package-lock.json. No workspace. No peer, ABI or runtime-floor conflict is reported by `npm install --dry-run` for any candidate below.

| Package | Current | Candidate | Change |
|---------|---------|-----------|--------|
| express | 4.17.1 | 4.21.2 | MINOR |
| dayjs | 1.11.7 | 1.11.13 | PATCH |
| chalk | 4.1.2 | 5.4.1 | MAJOR |

`uuid` is declared as the exact version 9.0.0 and `typescript` has no candidate.
