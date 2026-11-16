# Decompose before abstracting

- Name each responsibility and the state it reads/writes; boundaries should reduce coordination, not merely introduce files or interfaces.
- Split a component when parts change for independent reasons or can be tested/replaced independently.
- Keep tightly coupled steps together when separation would require callbacks, shared mutable state, or pass-through abstractions.
- Prefer deleting needless coordination over replacing it with a new framework.

## External References

- [Simple Made Easy](https://www.infoq.com/presentations/Simple-Made-Easy/) - Rich Hickey on complecting vs composing
- [Out of the Tar Pit](https://curtclifton.net/papers/MosesleyMarks06a.pdf) - Moseley & Marks on essential vs accidental complexity
- [A Philosophy of Software Design](https://www.amazon.com/dp/173210221X) - John Ousterhout on deep vs shallow modules
