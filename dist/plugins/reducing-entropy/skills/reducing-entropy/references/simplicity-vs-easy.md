---
description: Use when a smaller implementation risks increasing coupling or hiding complexity in a harder-to-change form.
---

# Simplicity vs. ease: decision prompts

Choose the design with fewer entangled decisions, not merely fewer keystrokes. Use these questions to compare options:

- Can consumers change independently, or must unrelated code coordinate?
- Is a tiny abstraction reducing repeated knowledge, or adding indirection without a stable concept?

The smallest line count is not automatically simplest if it couples independent change or obscures a correctness boundary. Name that cost and compare it with the measured reduction.

## External References

- [Simple Made Easy](https://www.infoq.com/presentations/Simple-Made-Easy/) - Rich Hickey's canonical talk on this distinction
- [The Value of Values](https://www.infoq.com/presentations/Value-Values/) - Related talk on immutability and simplicity
