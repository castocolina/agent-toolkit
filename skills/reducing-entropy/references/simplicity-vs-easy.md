---
description: Use when a smaller implementation risks increasing coupling or hiding complexity in a harder-to-change form.
---

# Simplicity vs. ease: decision prompts

Choose the design with fewer entangled decisions, not merely fewer keystrokes. Use these questions to compare options:

- Does this combine concerns that change for different reasons?
- Can consumers change independently, or must unrelated code coordinate?
- Is a tiny abstraction reducing repeated knowledge, or adding indirection without a stable concept?
- Does the apparent deletion move complexity into dependency configuration, generated code, or operational behavior?

The smallest line count is not automatically simplest if it couples independent change or obscures a correctness boundary. Name that cost and compare it with the measured reduction.

Further reading: [Simple Made Easy](https://www.infoq.com/presentations/Simple-Made-Easy/).
