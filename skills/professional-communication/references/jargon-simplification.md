# Translate technical work without changing its claims

## Procedure

1. Identify what changed, who is affected, and what evidence supports the claimed impact.
2. Keep the technical term when precision matters (security, legal/compliance, incident response, engineering specs); otherwise explain the consequence in audience language.
3. Separate observed results from intent or hypothesis. Do not convert an implementation choice into an unmeasured benefit.

## Fact-preserving rewrites

- “We containerized the application.” → “The application now runs in a container, a packaged environment with its runtime dependencies.” Do not claim faster or more reliable deployments without measurements.
- “We added monitoring and alerting.” → “The system now monitors these signals and sends alerts when configured thresholds are crossed.” Do not promise detection before customers report a problem.
- “We upgraded to Node [version].” → “The service now runs on Node [version].” Mention security fixes or capabilities only when verified and relevant. Before calling a version current or supported, read the live release table ([Node.js release schedule](https://github.com/nodejs/Release/blob/main/schedule.json); [previous releases](https://nodejs.org/en/about/previous-releases)): checked 2026-11-07, Node 20 had reached end of life on 2026-04-30.
- “The service is timing out.” → “Some requests are taking longer than the configured limit and are failing.” Keep scope and frequency only as supplied evidence supports.

Use impact-first wording only when impact is known. Preserve numbers with their source and timeframe; if evidence is absent, say the outcome is not yet measured.

## Common phrases in plain language

Use these for the meaning of the phrase; keep scope, frequency, and cause only as far as the evidence supplied supports. The last column lists what not to add.

| Technical phrase | Plain language | Do not add without evidence |
| --- | --- | --- |
| “We need to optimize the query.” | “We need to make this query faster or lighter.” | How much faster |
| “There's a bug in production.” | “There's an error in the live system.” | Who is affected, or how many |
| “We're experiencing degraded performance.” | “Things are slower than normal.” | A cause, or a recovery time |
| “The service is timing out.” | “Requests are failing because they take too long.” | Scope and frequency |
| “We need to scale horizontally.” | “We need to add more servers or instances to handle the load.” | A capacity or cost figure |
| “There's a regression in the latest release.” | “The new update broke something that used to work.” | Which users, or a fix date |
| “We're doing a hotfix.” | “We're making a quick fix for a problem in the live system.” | When it will ship |
| “That's a breaking change.” | “Existing integrations will stop working unless they are updated.” | Who must act, unless known |
| “We need to deprecate this endpoint.” | “We're phasing out this feature; please move to [replacement].” | A replacement or an end date that was not supplied |
