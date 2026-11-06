# Humanizer

A Claude Code skill that removes signs of AI-generated writing from text, making it sound more natural and human.

## Installation

### From this repository

```bash
cp -r skills/humanizer ~/.claude/skills/
```

Copy the whole directory: `SKILL.md` loads `references/pattern-catalog.md` on demand.

### Upstream original

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/blader/humanizer.git ~/.claude/skills/humanizer
```

## Usage

In Claude Code, invoke the skill:

```
/humanizer

[paste your text here]
```

Or ask Claude to humanize text directly:

```
Please humanize this text: [your text]
```

## Overview

Based on [Wikipedia's "Signs of AI writing"](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) guide, maintained by WikiProject AI Cleanup. This comprehensive guide comes from observations of thousands of instances of AI-generated text.

### Key Insight from Wikipedia

> "LLMs use statistical algorithms to guess what should come next. The result tends toward the most statistically likely result that applies to the widest variety of cases."

## Contents

`SKILL.md` owns the workflow, the core diagnostics (evidence, inflation, superficial analysis, promotion, structure), the evidence rules and the catalog load condition. `references/pattern-catalog.md` holds the additional cues (correspondence, disclaimers, conclusions, hedging, vocabulary by model era, mechanics), each labelled current or older-model. This README only describes the package.

`evals/evals.json` holds the output evals; `evals/trigger-queries.json` holds the trigger queries.

## References

- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) - Primary source
- [WikiProject AI Cleanup](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup) - Maintaining organization

## Version History

- **2026-11-04 (agent-toolkit)** - Catalog adapted to Wikipedia:Signs of AI writing revision 1383638008 (2026-11-03): era labels, new current-model cues, false ranges dropped
- **2.1.1** - Fixed pattern #18 example (curly quotes vs straight quotes)
- **2.1.0** - Added before/after examples for all 24 patterns
- **2.0.0** - Complete rewrite based on raw Wikipedia article content
- **1.0.0** - Initial release

## License

MIT. `references/pattern-catalog.md` is adapted from [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (revision 1383638008) by its contributors (WikiProject AI Cleanup), licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/); see the page history for authors
