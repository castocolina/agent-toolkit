# Test Case Templates

One base format, the extra fields each case type needs, and ID prefixes. Oracles, priority and the isolation rules live in SKILL.md; this file only shapes the output.

## Base format

```markdown
## TC-[AREA]-[NNN]: [Behavior] when [condition]

**Priority:** P0 | P1 | P2 | P3   **Type:** Functional | UI | Integration | Regression | Security | Performance
**Requirement:** [REQ-ID or R1 from the request]   **Risk:** [failure mode this case catches]
**Status:** Not Run   **Estimated time:** [minutes / Unknown]

### Objective
[what this case validates and why it matters]

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

### Post-conditions
- [system state after a passing run, observable: session created, record count, ledger entry]

### Cleanup
- [delete or reset what this case created, so a rerun starts clean]

### Evidence
- [what to capture on failure: screenshot, request ID, order ID]

### Edge cases and variations
| Variation | Input | Expected result |
| :- | :- | :- |
| Empty input | (empty) | Validation error shown, nothing saved |
| Length at and beyond the documented maximum | [N and N+1 characters] | [accepted / rejected as the requirement says] |
| Special characters | [the characters in play] | Handled, no side effect |

### Related cases
- [TC-..: related scenario or prerequisite]

### Execution history
| Date | Tester | Build | Result | Bug ID | Notes |
| :- | :- | :- | :- | :- | :- |
| | | | Not Run | | |

### Notes
[known issues, context; write none when there are none]
```

The rows of the edge-case table are examples: replace them with the partitions the requirement implies. A variation that needs its own steps becomes its own case (one case, one partition).

Put the "Why this value" column to work: a value with no reason is usually a duplicate of another case. One case covers one partition or boundary; split a case whose steps test two independent outcomes, because one failure then hides the other.

## Extra fields by type

| Type | Add to the base | Watch for |
| :- | :- | :- |
| Functional | Boundary and negative rows in Test Data, one row per partition | A negative case must also assert the absence of a side effect (no record, no email) |
| UI / visual | Figma frame link and version, viewport, theme, device-pixel ratio, measured values | Measure computed values against the frame; do not compare by eye. The per-component visual case is in `references/figma_validation.md` section 5 |
| Integration | Both systems' versions, the contract or payload, what each side must record | Check both ends: a 200 from A does not prove B stored the data |
| Regression | The change this case guards (ticket or commit), the last passing build | Keep the guarded change in the case so selection by change can find it |
| Security | Control under test, role used, expected refusal, what must not leak | Use a dedicated test account; never a real user's data |
| Performance | Metric, percentile, data size, load profile, baseline build | Record p95/p99 against the same data size as the baseline; an average hides the tail |

## Type blocks

Add the block for the case's type to the base format.

**Integration:**

```markdown
### Data validation
| Field | Source value | Transformed value (expected) | Status |
| :- | :- | :- | :- |
| [field] | [value in system A] | [value in system B] | [ ] |

### Error scenarios
- [ ] Network timeout: the caller shows the stated error and keeps its data
- [ ] Invalid response: rejected, no partial record
- [ ] Authentication failure: refused, no data returned
- [ ] Rate limiting: retried or reported as the contract says
```

Each scenario is a case or a step with its own observable result; a checked box is not a result.

**Security:**

```markdown
### Control under test
**OWASP category:** [category name, with the edition stated / Unknown]   **Risk level:** [Critical | High | Medium | Low | Untriaged]

### Attack vectors (one case or step per vector that applies)
- [ ] Injection (SQL, command, template)
- [ ] Cross-site scripting (stored, reflected)
- [ ] Cross-site request forgery
- [ ] Authentication bypass
- [ ] Authorization escalation (a role reaches another role's data or action)

### Assertions
- The response is the stated refusal and gives no information (generic message, no stack trace)
- The audit log records the attempt (entry, actor, time), or the check is `Blocked` with the log owner
- The test account is not compromised and no data changed

### Compliance check
- [ ] [the regulation or policy the team names] requirement met, with its evidence
- [ ] Audit trail complete
- [ ] Data encrypted at rest and in transit, checked where the team can see it
```

Name the OWASP edition as in `references/bug_report_templates.md` (Security bug template); never write a bare id. Run attack inputs only on a dedicated test account and a disposable environment.

**Performance:**

```markdown
### Performance criteria (set from the team's baseline; the values below are placeholders)
| Metric | Target | Acceptable | Actual | Status |
| :- | :- | :- | :- | :- |
| Response time (p95) | [ms] | [ms] | | [ ] |
| Throughput | [requests/s] | [requests/s] | | [ ] |
| Error rate | [%] | [%] | | [ ] |
| CPU use | [%] | [%] | | [ ] |
| Memory use | [%] | [%] | | [ ] |

### Load scenarios
1. Normal load: [N] concurrent users for [duration]; all metrics within target
2. Peak load: [N] concurrent users for [duration]; all metrics within acceptable
3. Stress: [N] concurrent users until failure; the system degrades gracefully, with no data loss
```

Never copy a number from this block as a recommendation: targets come from the requirement or the recorded baseline, and a missing one is `Unknown` under Open Questions. Run on an isolated environment with the same data size as the baseline.

## ID prefixes

`TC-FUNC-`, `TC-UI-`, `TC-INT-`, `TC-REG-`, `TC-SEC-`, `TC-PERF-`, `TC-API-`, and `SMOKE-` for the smoke core. Keep the area in the ID (`TC-CHK-001`) when the team files cases by feature; reuse the requester's scheme if one exists.
