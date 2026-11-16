# Batch 44

## qa-test-planner (skill)

### qa-test-planner#D7-1
- severity: low
- dimension: D7
- location: skills/qa-test-planner/evals/trigger-queries.json
- fix: Trim the negatives to 10 and keep the strongest near-misses (the unnamed plan, smoke, bug and release-decision prompts). Rewrite the terse positives with realistic context: file paths, builds, rates.

### qa-test-planner#D8-1
- severity: medium
- dimension: D8
- location: skills/qa-test-planner/SKILL.md:61
- fix: Add the branch for an Unknown rate, which the grid has no row for (the 'sometimes does nothing, can't reliably repro' case): 'If the rate is Unknown, set priority from the intermittent row as a provisional value, or write Untriaged, and list the rate under Open Questions. Security or data-loss bugs stay P0.'

### qa-test-planner#D8-1
- severity: high
- dimension: D8
- location: skills/qa-test-planner/SKILL.md:59
- fix: Assess potential money, data and security harm before reproducing a bug. Require authorized disposable data and a safe environment for potentially harmful reruns; if those prerequisites are unavailable, preserve the existing evidence and observed rate, record an unmeasured rate as Unknown or a single unreproduced occurrence, and request the missing prerequisites. Keep the original environment distinct from any later sandbox reproduction.

### qa-test-planner#D7-1
- severity: medium
- dimension: D7
- location: skills/qa-test-planner/evals/evals.json:89
- fix: Add an assertion that every supplied reproduction-context fact, including staging, survives in the command and saved report. Update the logged --description and report fixture to retain staging without altering the exact build value, or explicitly make the omission a defect the evaluator must detect and report.

### qa-test-planner#D1-1
- severity: low
- dimension: D1
- location: skills/qa-test-planner/SKILL.md:86
- fix: Drop the textbook P0-P3 definitions the model already knows. Keep only the non-obvious part: overlap shown by evidence, never assumed, and the tie-break by cost.

### qa-test-planner#D2-1
- severity: low
- dimension: D2
- location: skills/qa-test-planner/SKILL.md:59
- fix: Add one thinking prompt before step 3, such as 'before setting severity, ask what the failure costs (money, data, recovery) and whether it is product or environment'. That makes the branch a decision framework and not only a four-step checklist.

### qa-test-planner#D1-1
- severity: low
- dimension: D1
- location: skills/qa-test-planner/SKILL.md:61
- fix: Remove the duplicate missing-fact instruction from the bug-report branch, retaining the global output convention and the final validation check. Keep branch-specific guidance focused on evidence preservation, safe reproduction and triage.
