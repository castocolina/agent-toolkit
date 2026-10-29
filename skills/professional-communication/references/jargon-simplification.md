# Translate technical work without changing its claims

## Procedure

1. Identify what changed, who is affected, and what evidence supports the claimed impact.
2. Keep the technical term when precision matters (security, legal/compliance, incident response, engineering specs); otherwise explain the consequence in audience language.
3. Separate observed results from intent or hypothesis. Do not convert an implementation choice into an unmeasured benefit.

## Fact-preserving rewrites

- “We containerized the application.” → “The application now runs in a container, a packaged environment with its runtime dependencies.” Do not claim faster or more reliable deployments without measurements.
- “We added monitoring and alerting.” → “The system now monitors these signals and sends alerts when configured thresholds are crossed.” Do not promise detection before customers report a problem.
- “We upgraded to Node 20.” → “The service now runs on Node 20.” Mention security fixes or capabilities only when verified and relevant.
- “The service is timing out.” → “Some requests are taking longer than the configured limit and are failing.” Keep scope and frequency only as supplied evidence supports.

Use impact-first wording only when impact is known. Preserve numbers with their source and timeframe; if evidence is absent, say the outcome is not yet measured.
