# Batch 29

## meme-factory (skill)

### meme-factory#D8-1
- severity: medium
- dimension: D8
- location: skills/meme-factory/scripts/meme_generator.py:160
- fix: Resolve negation and uncertainty before positive or negative outcome keywords, use token-aware matching, and fall back to a neutral template when the outcome is ambiguous. Add regression cases for negated success, negated failure, and substring collisions.

### meme-factory#D7-1
- severity: low
- dimension: D7
- location: skills/meme-factory/evals/trigger-queries.json:39
- fix: Rebalance to 8-10 positives (drop or relabel the weakest positive) and add a near-miss negative such as a caption request for a photo with no URL or template.

### meme-factory#D8-1
- severity: low
- dimension: D8
- location: skills/meme-factory/SKILL.md:12
- fix: State the fallback when Python or the repo-relative path is unavailable: build the URL directly from the Quick reference pattern using the encoding table.

### meme-factory#D1-1
- severity: medium
- dimension: D1
- location: skills/meme-factory/SKILL.md:17
- fix: Compress the generic joke-writing steps and familiar template explanations into a short selector. Preserve the useful actual template IDs, two-caption capacity constraint, encoding rules, privacy boundary, and uncertain-outcome handling.

### meme-factory#D5-1
- severity: medium
- dimension: D5
- location: skills/meme-factory/SKILL.md:12
- fix: Reference the helper as `python3 scripts/meme_generator.py generate <template> '<top>' '<bottom>'`, relative to the skill root.

### meme-factory#D1-1
- severity: low
- dimension: D1
- location: skills/meme-factory/SKILL.md:18
- fix: Compress steps 1-2 into one line (name the contrast; draft the payoff first, then the setup) and drop the role taxonomy the model can improvise.

### meme-factory#D2-1
- severity: low
- dimension: D2
- location: skills/meme-factory/SKILL.md:44
- fix: Add the retry loop: if captions crop or wrap, shorten them and regenerate once, then present or report the template's limit.

### meme-factory#D3-1
- severity: low
- dimension: D3
- location: skills/meme-factory/SKILL.md:10
- fix: Note that an omitted caption must be the literal `_` placeholder in a hand-built URL (the helper substitutes it automatically); an empty segment breaks the URL.

### meme-factory#D5-1
- severity: medium
- dimension: D5
- location: skills/meme-factory/references/examples.md:1
- fix: Gate the file from SKILL.md (read references/examples.md only when the user asks for integration or CLI examples) or delete it, trim the Slack/Discord/PR-comment pseudo-code the model does not need, and remove the scripts/__pycache__ build artifacts.

### meme-factory#D6-1
- severity: low
- dimension: D6
- location: skills/meme-factory/SKILL.md:10
- fix: Name the parameters (`width`, `height`, `layout`, `font`) or point to the helper's --width/--height/--layout flags so sizing is not guessed.
