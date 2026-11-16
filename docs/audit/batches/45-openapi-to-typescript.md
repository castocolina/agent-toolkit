# Batch 45

## openapi-to-typescript (skill)

### openapi-to-typescript#D7-1
- severity: low
- dimension: D7
- location: skills/openapi-to-typescript/evals/evals.json:9
- fix: Take references/guards.md out of the `files` input lists of the spec-types and shapes-guards evals. It is part of the skill, not an eval input, and listing it gives the without-skill baseline the guard rules, which hides how much the skill adds.

### openapi-to-typescript#D8-1
- severity: low
- dimension: D8
- location: skills/openapi-to-typescript/SKILL.md:150
- fix: Use the path actually chosen in step 4 instead of the fixed `types/api.ts` (for example `| grep -F "<output path>"`), and the same in the fallback command. When step 4 picks an existing location like src/api/types.ts, the grep fails or checks the wrong file.

### openapi-to-typescript#D8-1
- severity: high
- dimension: D8
- location: skills/openapi-to-typescript/SKILL.md:22
- fix: Validate that the version is 3.0.x before any Continue branch. Then check references and schema availability separately, so absent components cannot bypass rejection of unsupported versions.

### openapi-to-typescript#D8-2
- severity: medium
- dimension: D8
- location: skills/openapi-to-typescript/SKILL.md:150
- fix: Use the destination selected during emission in every validation command and check its resolved path against --listFilesOnly output. If the repository tsconfig excludes that file, validate it with a temporary config extending the repository config and explicitly including the destination; retain the documented standalone fallback when no repository config exists.

### openapi-to-typescript#D1-1
- severity: low
- dimension: D1
- location: skills/openapi-to-typescript/SKILL.md:33
- fix: Shorten this bullet to the one non-obvious rule ("keep the rest": existing capitals inside a part are kept). The model already knows how to PascalCase, so the rest of the explanation uses context without adding knowledge.
