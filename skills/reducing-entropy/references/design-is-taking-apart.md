# Decompose before abstracting

- Name each responsibility and the state it reads/writes; boundaries should reduce coordination, not merely introduce files or interfaces.
- Split a component when parts change for independent reasons or can be tested/replaced independently.
- Keep tightly coupled steps together when separation would require callbacks, shared mutable state, or pass-through abstractions.
- Prefer deleting needless coordination over replacing it with a new framework; preserve independently evolving rules even if the code is similar.
