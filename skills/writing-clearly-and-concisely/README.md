# Writing Clearly and Concisely

A skill that applies William Strunk Jr.'s writing principles to produce clearer, shorter prose while avoiding common AI writing patterns.

## Purpose

The skill drafts and copyedits reader-facing prose (READMEs, docs, commit messages, error messages, UI copy, policies, reports) so it gets shorter without changing what the reader may, must or should do. It draws from two sources:

1. **The Elements of Style** (Strunk, 1918) - rules for clear, forceful writing
2. **AI Pattern Avoidance** - Wikipedia editors' catalog of the generic, puffy language that LLMs tend to produce

`SKILL.md` owns the rules: the Edit, Structure, Draft and Flag branches, the claims and invariant checkpoints, hard before/after cases, the NEVER list and the reference load list. This README only describes the package.

**Trigger phrases:**
- "Make this more concise"
- "Edit this for clarity"
- "Write an error message for..."
- "Review this commit message"
- "Remove the puffery from this README"

## Reference Files

| Section | File | Content |
|---------|------|---------|
| Grammar & punctuation | `elements-of-style/02-elementary-rules-of-usage.md` | Comma rules, possessives, sentence structure |
| Composition principles | `elements-of-style/03-elementary-principles-of-composition.md` | Active voice, concision, paragraph structure |
| Formatting | `elements-of-style/04-a-few-matters-of-form.md` | Headings, quotations, formatting conventions |
| Word choice | `elements-of-style/05-words-and-expressions-commonly-misused.md` | Common errors, word selection |
| AI patterns | `signs-of-ai-writing.md` | Wikipedia editors' field guide to AI detection |

## Evals

`evals/evals.json` holds the output evals (fixtures in `evals/files/`); `evals/trigger-queries.json` holds the trigger queries.

## Directory Structure

```
writing-clearly-and-concisely/
  SKILL.md                 # Main skill definition
  README.md                # This file
  signs-of-ai-writing.md   # AI pattern detection guide
  evals/
    evals.json
    trigger-queries.json
    files/                 # eval fixtures
  elements-of-style/
    01-introductory.md
    02-elementary-rules-of-usage.md
    03-elementary-principles-of-composition.md
    04-a-few-matters-of-form.md
    05-words-and-expressions-commonly-misused.md
```

## Installation

**Claude Code:**
```bash
cp -r skills/writing-clearly-and-concisely ~/.claude/skills/
```

**Claude.ai:**
Add the skill to project knowledge or paste SKILL.md contents into your conversation.

## Attribution

- Original skill by @joshuadavidthomas from [joshuadavidthomas/agent-skills](https://github.com/joshuadavidthomas/agent-skills) (MIT)
- Adapted from [obra/the-elements-of-style](https://github.com/obra/the-elements-of-style)
- Writing principles from *The Elements of Style* by William Strunk Jr. (1918)
- AI pattern research from Wikipedia's field guide to AI-generated content detection: `signs-of-ai-writing.md` is adapted from [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) by its contributors (WikiProject AI Cleanup), licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/); see the page history for authors
