# Candidate scan (fixture data standing in for the output of `scripts/run-taze.sh`)

Resolver and lockfile: npm, package-lock.json. No workspace. The project runs on Node 20.

| Package | Current | Candidate | Change |
|---------|---------|-----------|--------|
| express | 4.17.1 | 4.21.2 | MINOR |
| eslint | 8.0.0 | 8.57.1 | MINOR |
| axios | 0.21.4 | 0.27.2 | MINOR |
| react | 17.0.2 | 18.3.1 | MAJOR |
| react-dom | 17.0.2 | 18.3.1 | MAJOR |

Target-specific dry runs (fixture data, one per candidate):

- `npm install express@4.21.2 --dry-run`: no peer conflict; declared `engines.node` range covers the project's Node 20
- `npm install eslint@8.57.1 --dry-run`: no peer conflict; declared `engines.node` range covers the project's Node 20
- `npm install axios@0.27.2 --dry-run`: no peer conflict; declared `engines.node` range covers the project's Node 20 (a 0.x version, so it is still asked per target)
- `npm install react@18.3.1 --dry-run`: no peer conflict; declared `engines.node` range covers the project's Node 20 (a MAJOR change, so it is still asked per target)
- `npm install react-dom@18.3.1 --dry-run`: no peer conflict; declared `engines.node` range covers the project's Node 20 (a MAJOR change, so it is still asked per target)

Native or prebuilt binary (fixture data, one per candidate):

- express: none, pure JavaScript
- eslint: none, pure JavaScript
- axios: none, pure JavaScript
- react: none, pure JavaScript
- react-dom: none, pure JavaScript

`lodash` is declared as the exact version 4.17.20 and `typescript` has no candidate.
