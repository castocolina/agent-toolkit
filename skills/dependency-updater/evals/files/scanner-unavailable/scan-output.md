# Candidate scan (fixture data standing in for the output of `scripts/run-taze.sh`)

Resolver and lockfile: npm, package-lock.json. No workspace. The project runs on Node 20.

| Package | Current | Candidate | Change |
|---------|---------|-----------|--------|
| express | 4.17.1 | 4.21.2 | MINOR |
| dayjs | 1.11.7 | 1.11.13 | PATCH |

Target-specific dry runs (fixture data, one per candidate):

- `npm install express@4.21.2 --dry-run`: no peer conflict; declared `engines.node` range covers the project's Node 20
- `npm install dayjs@1.11.13 --dry-run`: no peer conflict; declared `engines.node` range covers the project's Node 20

`uuid` is declared as the exact version 9.0.0 and `typescript` has no candidate.
