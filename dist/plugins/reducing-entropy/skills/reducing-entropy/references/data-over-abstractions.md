# Data, wrappers, and shared rules

- Compare the real maintenance cost, not category labels: plain data is a default, not an absolute.
- Keep records, discriminated unions, or domain/value types when they enforce validated invariants, prevent invalid states, or clarify a boundary; remove a wrapper only when its behavior and contract add no needed protection.
- Before consolidating similar code, identify the rule owner, compare input/output contracts, and compare why each consumer changes. Merge only when they must preserve the same invariant.
- Similar parsers with different compatibility rules should remain separate even when their code looks alike; duplicating a few lines may be cheaper than coupling release schedules.
