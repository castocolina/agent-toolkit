# Test Case Templates

One base format, the extra fields each case type needs, and ID prefixes. Oracles, priority and the isolation rules live in SKILL.md; this file only shapes the output.

## Base format

```markdown
## TC-[AREA]-[NNN]: [Behavior] when [condition]

**Priority:** P0 | P1 | P2 | P3   **Type:** Functional | UI | Integration | Regression | Security | Performance
**Requirement:** [REQ-ID or R1 from the request]   **Risk:** [failure mode this case catches]
**Status:** Not Run

### Preconditions
- [state seeded for this case only: account, records, flags]
- [environment: build, browser/device, timezone or frozen clock if time matters]

### Steps
1. [action with exact input]
   **Expected:** [observable result: text, record, status code, count]
2. [action]
   **Expected:** [observable result]

### Test Data
| Field | Value | Why this value |
| :- | :- | :- |
| amount | 0.01 | smallest accepted value |

### Cleanup
- [delete or reset what this case created, so a rerun starts clean]

### Evidence
- [what to capture on failure: screenshot, request ID, order ID]
```

Put the "Why this value" column to work: a value with no reason is usually a duplicate of another case. One case covers one partition or boundary; split a case whose steps test two independent outcomes, because one failure then hides the other.

## Extra fields by type

| Type | Add to the base | Watch for |
| :- | :- | :- |
| Functional | Boundary and negative rows in Test Data, one row per partition | A negative case must also assert the absence of a side effect (no record, no email) |
| UI / visual | Figma frame link and version, viewport, theme, device-pixel ratio, measured values | Measure computed values against the frame; do not compare by eye |
| Integration | Both systems' versions, the contract or payload, what each side must record | Check both ends: a 200 from A does not prove B stored the data |
| Regression | The change this case guards (ticket or commit), the last passing build | Keep the guarded change in the case so selection by change can find it |
| Security | Control under test, role used, expected refusal, what must not leak | Use a dedicated test account; never a real user's data |
| Performance | Metric, percentile, data size, load profile, baseline build | Record p95/p99 against the same data size as the baseline; an average hides the tail |

## ID prefixes

`TC-FUNC-`, `TC-UI-`, `TC-INT-`, `TC-REG-`, `TC-SEC-`, `TC-PERF-`, `TC-API-`, and `SMOKE-` for the smoke core. Keep the area in the ID (`TC-CHK-001`) when the team files cases by feature; reuse the requester's scheme if one exists.
