# Reducing Entropy

A manual-only skill for minimizing total codebase size. It measures success by the final amount of first-party code, not by the effort of the change, and biases toward deletion while guarding behavior, public contracts and stored data. `SKILL.md` holds the runtime workflow; this file is for people maintaining the skill.

## Installation

**Claude Code:**

```bash
cp -r skills/reducing-entropy ~/.claude/skills/
```

**claude.ai:** add the skill to project knowledge or paste `SKILL.md` into the conversation.

## Files

- `SKILL.md` - trigger boundary, lens routing, procedure and NEVER rules.
- `references/` - one decision lens per file, each loaded only when `SKILL.md` routes to it.
- `evals/` - output evals, trigger queries, and fixtures in `evals/files/`.

## Adding a reference mindset

Add a reference only for a distinct decision lens that changes a real delete/consolidate judgment. Keep it brief, name it by concept (not by person or source), link it from the lens list in `SKILL.md` with its trigger, avoid restating general design philosophy, and end it with an External References list of its primary sources.

Primary sources for simplicity thinking, to draw from when creating new mindsets:

- [Simple Made Easy](https://www.infoq.com/presentations/Simple-Made-Easy/) - Rich Hickey
- [Hammock Driven Development](https://www.youtube.com/watch?v=f84n5oFoZBc) - Rich Hickey
- [The Value of Values](https://www.infoq.com/presentations/Value-Values/) - Rich Hickey
- [Out of the Tar Pit](https://curtclifton.net/papers/MosesleyMarks06a.pdf) - Moseley & Marks
- [No Silver Bullet](https://www.cs.unc.edu/techreports/86-020.pdf) - Fred Brooks
- [The Grug Brained Developer](https://grugbrain.dev/) - grugbrain.dev
- [Worse Is Better](https://www.dreamsongs.com/WorseIsBetter.html) - Richard Gabriel
- [A Philosophy of Software Design](https://www.amazon.com/dp/173210221X) - John Ousterhout
- [The Zen of Python](https://peps.python.org/pep-0020/) - Tim Peters

## Attribution

- Original skill by @joshuadavidthomas from [joshuadavidthomas/agent-skills](https://github.com/joshuadavidthomas/agent-skills) (MIT)
