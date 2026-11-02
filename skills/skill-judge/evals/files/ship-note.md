---
description: Append a one-line ship note to SHIP.md when the user says "ship note". Not for opening a pull request.
argument-hint: "[note]"
---

# Ship note

1. Read `SHIP.md`. If it is missing, create it with the heading `# Ship notes`.
2. Append one bullet: the date, then the note from `$ARGUMENTS`.
3. Stop. Do not commit, push, or open a pull request.

NEVER commit from this command: a note is not a release.
