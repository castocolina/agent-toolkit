# Batch 04

## naming-analyzer (skill)

### naming-analyzer#D7-1
- severity: medium
- dimension: D7
- location: skills/naming-analyzer/evals/evals.json:16
- fix: Supply implementations and call sites that establish meaning, or make focused clarification questions and explicitly tentative candidates acceptable outcomes. Add a verifiable case where retaining a name is correct because its external contract is established.

### naming-analyzer#D7-2
- severity: low
- dimension: D7
- location: skills/naming-analyzer/evals/trigger-queries.json:3
- fix: Replace several generic positives and easy negatives with realistic context-rich prompts, including misleading unit/time-basis names and requests that overlap naming review but actually authorize an automatic migration.

### naming-analyzer#D7-1
- severity: medium
- dimension: D7
- location: skills/naming-analyzer/evals/evals.json:6
- fix: Add a repo-level eval with a small file fixture containing a serialized-field identifier to test the compatibility rule, and vary prompt formality and context

### naming-analyzer#D8-1
- severity: low
- dimension: D8
- location: skills/naming-analyzer/SKILL.md:41
- fix: Add one filled example row (including a no-change row) so the confidence and compatibility values are unambiguous

### naming-analyzer#D1-1
- severity: medium
- dimension: D1
- location: skills/naming-analyzer/SKILL.md:19
- fix: Remove the elementary constant-naming example and consolidate repeated compatibility warnings. Spend the recovered space on concrete cases where units, lifecycle, nullability, or competing caller meanings change the correct naming decision.

### naming-analyzer#D2-1
- severity: medium
- dimension: D2
- location: skills/naming-analyzer/SKILL.md:27
- fix: Add an evidence-resolution procedure: trace definitions, transformations, callers, and contract boundaries; withhold a definitive rename when meanings conflict; distinguish a safe local alias from a contract change; tie confidence to the evidence actually established.

### naming-analyzer#D3-1
- severity: medium
- dimension: D3
- location: skills/naming-analyzer/SKILL.md:31
- fix: Add reasoned warnings for string-key access, reflection, dependency-injection names, framework-reserved file names, and generated identifiers: these consumers can evade ordinary static-reference searches, so an apparently private symbol may still be a runtime contract.

### naming-analyzer#D1-1
- severity: medium
- dimension: D1
- location: skills/naming-analyzer/SKILL.md:31
- fix: Cut widely-known review basics (compatibility checks before public renames are standard agent behavior); keep and expand only the behavior-calibrating rules the model does not apply by default (project convention precedence, boolean polarity over prefix, ask-don't-infer)

### naming-analyzer#D2-1
- severity: low
- dimension: D2
- location: skills/naming-analyzer/SKILL.md:23
- fix: Add one worked example walking a rename from evidence to compatibility verdict so the risk ordering is trained, not just listed

### naming-analyzer#D3-1
- severity: low
- dimension: D3
- location: skills/naming-analyzer/SKILL.md:29
- fix: Add environment-specific gotchas: identifiers referenced by ORM mappings, generated code, i18n message keys, or reflection that rename tooling silently misses

### naming-analyzer#D6-1
- severity: low
- dimension: D6
- location: skills/naming-analyzer/SKILL.md:17
- fix: State the fallback when no project convention exists (default to the language's dominant convention and say so in the report)
