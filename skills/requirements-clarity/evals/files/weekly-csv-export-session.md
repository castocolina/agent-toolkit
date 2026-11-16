# Clarification notes: Weekly CSV export

Session date: 2026-11-03
Stakeholders: Dana (ops lead, requester), Luis (engineering lead)

## Repository facts (inspected)
- Next.js app in `apps/web`, Postgres via Prisma (`apps/web/prisma/schema.prisma`).
- Existing JSON endpoint `GET /api/reports/weekly` in `apps/web/app/api/reports/weekly/route.ts` returns hours per person for one team and one ISO week.
- Roles come from `session.user.role`: `manager`, `member`, `admin`.

## Round 1 (score 40/100)
Q: Who exports, and what problem does it solve?
A (Dana): Team managers. Today they ask finance to pull hours by hand, about 40 requests a month. We want that under 5 a month.

Q: Which data goes in the file?
A (Dana): One row per person per day: person name, email, date, project, hours. Only the manager's own team.

## Round 2 (score 74/100)
Q: Who must not be able to export?
A (Luis): Members get a 403. Admins can export any team.

Q: Performance limits?
A (Luis): The largest team is 120 people. The download must finish in under 30 seconds for that team.

Q: What happens for a week with no logged hours?
A (Dana): Still download a file with the header row only, no error.

## Round 3 (score 92/100)
Q: Time zone for the week boundary?
A (Dana): The team's configured time zone (`team.timezone`), Monday to Sunday.

Q: Where does the export start, and what is the file called?
A (Dana): An "Export CSV" button on the existing weekly report page. File name `{team-slug}-{iso-week}.csv`, for example `support-2026-W44.csv`. Admins pick the team with the team selector already on that page.

Q: What does the user see if the export fails or passes 30 seconds?
A (Luis): Stop at 30 seconds and show "Export failed, try again"; no partial file. Same message for a server error.

Q: Someone who moved teams mid-week?
A (Dana): Their rows go to the team they logged each entry under, so a person can appear in two teams' files for the same week.

Q: Names with commas, quotes or accents?
A (Luis): UTF-8 with standard CSV quoting (RFC 4180), so Excel and Google Sheets open it correctly.

Q: Anything explicitly out of scope?
A (Dana): Scheduled email delivery and Excel format are out for v1.

Open questions: none.
