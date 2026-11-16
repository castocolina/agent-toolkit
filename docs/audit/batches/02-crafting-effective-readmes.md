# Batch 02

## crafting-effective-readmes (skill)

### crafting-effective-readmes#D8-1
- severity: medium
- dimension: D8
- location: skills/crafting-effective-readmes/SKILL.md:13
- fix: Treat an absent remote as unknown, not Personal. Prefer the user's stated audience and project purpose; inspect available evidence and ask one consequential clarification when the project type remains unresolved.

### crafting-effective-readmes#D8-1
- severity: medium
- dimension: D8
- location: skills/crafting-effective-readmes/SKILL.md:13
- fix: Add a monorepo branch: confirm whether the target is the root README or a package README before inferring type, since signals frequently conflict across packages

### crafting-effective-readmes#D1-1
- severity: medium
- dimension: D1
- location: skills/crafting-effective-readmes/SKILL.md:12
- fix: Delete the verb-classification router and trim generic style reminders and template boilerplate. Concentrate the skill on evidence-backed first-use paths, generated content ownership, published-versus-checkout instructions, and concrete documentation drift traps.

### crafting-effective-readmes#D2-1
- severity: medium
- dimension: D2
- location: skills/crafting-effective-readmes/SKILL.md:16
- fix: Add a clean-environment validation sequence: derive prerequisites from manifests and CI, exercise the documented first-use path without maintainer-local state, compare actual output with the README, and explicitly distinguish executed checks from static verification when execution is unavailable.

### crafting-effective-readmes#D3-1
- severity: medium
- dimension: D3
- location: skills/crafting-effective-readmes/SKILL.md:21
- fix: Add concise, reasoned README traps: repository-root commands may not target the published workspace package; default-branch examples may not match released APIs; generated regions are overwritten by their owning tool. Gate each warning on repository evidence.

### crafting-effective-readmes#D5-1
- severity: medium
- dimension: D5
- location: skills/crafting-effective-readmes/SKILL.md:27
- fix: Expose direct, scenario-gated links in SKILL.md: the formal specification for explicit Standard README compliance, its examples only when needed, and the reader-funnel article for audience-ordering problems. Keep supporting documents one navigation level from the entry point.

### crafting-effective-readmes#D1-1
- severity: medium
- dimension: D1
- location: skills/crafting-effective-readmes/templates/oss.md:1
- fix: Trim each template to the sections that differ per project type (the checklist matrix already carries the shared shape); full standard README skeletons are content the model already generates

### crafting-effective-readmes#D2-1
- severity: low
- dimension: D2
- location: skills/crafting-effective-readmes/SKILL.md:12
- fix: Replace the verb mapping with a decision question ('Will the reader's first success change?') and state that combined update+audit requests run the audit before edits

### crafting-effective-readmes#D3-1
- severity: medium
- dimension: D3
- location: skills/crafting-effective-readmes/SKILL.md:21
- fix: Add environment-specific gotchas: npm renders a subset of README HTML, GitHub anchor slugs differ from other renderers (punctuation stripping), and shields.io badges are blocked in some corporate networks

### crafting-effective-readmes#D5-1
- severity: low
- dimension: D5
- location: skills/crafting-effective-readmes/references/using-references.md:32
- fix: Fold the two example links into the standard-readme-spec entry and state 'load at most one guide'; the current chain routes two levels deep from SKILL.md with no load limit

### crafting-effective-readmes#D6-1
- severity: low
- dimension: D6
- location: skills/crafting-effective-readmes/SKILL.md:16
- fix: State the fallback for items source cannot confirm (e.g., external links, CI badges): label them 'unverified' in the output instead of asserting them
