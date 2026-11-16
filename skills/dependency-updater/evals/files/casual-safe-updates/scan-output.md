# Candidate scan (fixture data standing in for the output of `scripts/run-taze.sh`)

Resolver and lockfile: npm, package-lock.json. No workspace. No peer, ABI or runtime-floor conflict is reported by `npm install --dry-run` for any candidate below.

| Package | Current | Candidate | Change |
|---------|---------|-----------|--------|
| express | 4.17.1 | 4.21.2 | MINOR |
| eslint | 8.0.0 | 8.57.1 | MINOR |
| axios | 0.21.4 | 0.27.2 | MINOR |
| react | 17.0.2 | 18.3.1 | MAJOR |
| react-dom | 17.0.2 | 18.3.1 | MAJOR |

`lodash` is declared as the exact version 4.17.20 and `typescript` has no candidate.
