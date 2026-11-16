# Batch 20

## domain-name-brainstormer (skill)

### domain-name-brainstormer#D7-1
- severity: low
- dimension: D7
- location: skills/domain-name-brainstormer/evals/evals.json:19
- fix: Require exactly 12 distinct candidates in this test and separately verify the requested grouping and top-three explanations.

### domain-name-brainstormer#D8-1
- severity: medium
- dimension: D8
- location: skills/domain-name-brainstormer/SKILL.md:16
- fix: Define failed or inconclusive lookups as unknown/unverified, never available. Explain when to retry through a registrar, and distinguish an authoritative registration result from confirmed purchase availability.

### domain-name-brainstormer#D7-1
- severity: low
- dimension: D7
- location: skills/domain-name-brainstormer/evals/evals.json
- fix: Add an eval with an RDAP-response fixture in evals/files/ asserting that the source and check time are recorded and unchecked candidates are labeled unverified

### domain-name-brainstormer#D8-1
- severity: low
- dimension: D8
- location: skills/domain-name-brainstormer/SKILL.md:16
- fix: Name a fallback for when RDAP is rate-limited or a TLD lacks it (registrar search page) and require recording which source was checked

### domain-name-brainstormer#D1-1
- severity: medium
- dimension: D1
- location: skills/domain-name-brainstormer/SKILL.md:13
- fix: Compress the common naming-pattern recipe and routine output guidance. Preserve the less-obvious multilingual, registration-status, renewal-cost, and deployment constraints.

### domain-name-brainstormer#D2-1
- severity: medium
- dimension: D2
- location: skills/domain-name-brainstormer/SKILL.md:15
- fix: Apply hard language, confusion, and budget constraints before ranking. Then rank surviving candidates using the user's stated priorities, explicitly explaining any trade-off between memorability, descriptiveness, spelling reliability, and recurring cost.

### domain-name-brainstormer#D1-1
- severity: low
- dimension: D1
- location: skills/domain-name-brainstormer/SKILL.md:13
- fix: Compress the naming-pattern catalog the model already knows to one line and spend the tokens on the screening, registry-status, and legal-risk rules that are the skill's real value

### domain-name-brainstormer#D2-1
- severity: low
- dimension: D2
- location: skills/domain-name-brainstormer/SKILL.md:13
- fix: Fold the derivable generate-then-screen steps 2-3 into a single generate-and-screen step and lead the procedure with the claim-discipline rules that distinguish the skill

### domain-name-brainstormer#D3-1
- severity: low
- dimension: D3
- location: skills/domain-name-brainstormer/SKILL.md:23
- fix: Replace the hand-wavy escape hatch (no audience expects homographs) with a hard rule: reject confusable characters outright, and if a lookalike is ever proposed require a confusables check before shortlisting

### domain-name-brainstormer#D6-1
- severity: low
- dimension: D6
- location: skills/domain-name-brainstormer/SKILL.md:12
- fix: State a default assumption set (short, English, .com-first) so a casual ask can proceed without questions, and ask only when a answer would change the shortlist
