# Data, wrappers, and shared rules

> "It is better to have 100 functions operate on one data structure than 10 functions on 10 data structures." - Alan Perlis, Epigrams in Programming, no. 9 (ACM SIGPLAN, September 1982)

Generic operations on generic data structures beat specialized operations on specialized structures. Before keeping or creating a wrapper, class or custom type, ask:

- Could this be a map or dict with well-known keys?
- Could this be a simple tuple or record?
- Do I need custom behavior, or just data? If just data, use a data structure; keep a custom type for behavior that cannot be a function.

The two points below set the limit of that rule.

- Compare the real maintenance cost, not category labels: plain data is a default, not an absolute.
- Keep records, discriminated unions, or domain/value types when they enforce validated invariants, prevent invalid states, or clarify a boundary; remove a wrapper only when its behavior and contract add no needed protection.

## External References

- [The Value of Values](https://www.infoq.com/presentations/Value-Values/) - Rich Hickey on data vs objects
- [Data-Oriented Design](https://www.dataorienteddesign.com/dodbook/) - Richard Fabian's book on DOD
- [CppCon 2014: Mike Acton "Data-Oriented Design and C++"](https://www.youtube.com/watch?v=rX0ItVEVjHc) - Practical DOD in game engines
- [Epigrams in Programming, no. 9](https://cs.yale.edu/homes/perlis-alan/quotes.html) - Alan Perlis (ACM SIGPLAN, September 1982), source of the "100 functions on one data structure" line
