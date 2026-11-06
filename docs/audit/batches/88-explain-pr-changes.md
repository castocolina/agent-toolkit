# Batch 88

## explain-pr-changes (command)

### explain-pr-changes#D8-1
- severity: medium
- dimension: D8
- location: commands/explain-pr-changes.md:169
- fix: Before automatic promotion-body reuse, require confirmation that the merge-commit assumption holds. If it does not hold or cannot be established, stop before any PR write and request an explicit merged source through --reuse-from, rather than publishing potentially stale source bodies.

### explain-pr-changes#D1-1
- severity: medium
- dimension: D1
- location: commands/explain-pr-changes.md:192
- fix: Keep the single-source assembly implementation only in section 2.5. Have section 2.1 and phase 3 refer to that implementation, retaining their distinct source-selection and validation rules rather than repeating extraction and assembly instructions.

### explain-pr-changes#D5-1
- severity: medium
- dimension: D5
- location: commands/explain-pr-changes.md:237
- fix: Move the diagram-stripping implementation and detailed body templates into references under the bundled pr-diagrams skill. Add explicit plugin-root and personal-install read paths: load the filter reference only for none-mode copied or consolidated bodies, and load the fresh-body template only for feature or consolidated composition. Keep mode routing, invariants and the ordered phases in the command.
