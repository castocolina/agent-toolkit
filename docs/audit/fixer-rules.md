# Fixer rules and the recovery record

This file holds the rules every fixer follows (plan 14, plan 9, the scheduled audit) and the record format that explains a removal. `skills/skill-judge/references/rubric.md` (§ Removals and sources) judges removals against it. A fixer prompt pastes the Rules section or points at this file.

## Rules

1. Never delete content to raise a score or to fit a size target. When size is the problem, move content to `references/` (for a command or agent, into a skill its plugin bundles).
2. Record every removal or move of a rule, step, fact, template, example, paragraph, line or file in `docs/audit/recovery/<name>/record.md` (format below).
3. Edit only the sentence the finding names. Then re-read the lines and paragraphs around the edit and confirm nothing else changed.
4. Never change a version-sensitive fact without a source read in this session. Without one, either replace the hardcoded value with an instruction that reads the live value, or leave it and say so.
5. Never remove, shorten or reword a credit, attribution or license line.
6. Waiving an intended removal:
   - Inside a `batches` queue (plan 8 or plan 14), an intended removal may instead be waived with the full call `python3 scripts/audit/audit.py batches waive --id N --out DIR --merged FILE[,FILE] --artifact NAME --dimension D1 --file F --reason R`.
   - Outside a queue (the scheduled audit) the record row is the only way. There a fixer never writes `drop` or `drop-pending` with value `real`: content of real value is moved to `references/`, not dropped, because no user gate reviews the drop.
7. The judge rejects a `drop` row for content it rates substantive (rubric § Removals and sources).
8. Every edit serves the artifact's purpose. Meet the judge's and the Agent Skills spec's rules by changes that fit what the artifact is for; never add a section, list item, example, eval or keyword only to satisfy the judge or an eval (the rubric gives it no credit, § Removals and sources, Purpose fidelity), and never rewrite beyond what the finding asks.

## Recovery record

File: `docs/audit/recovery/<name>/record.md`. It is one markdown table with exactly this header:

```text
| item | fate | value | decision | reason class | reason |
```

A writer adds rows and never deletes or rewrites another writer's row, except in the drop and purpose-change rewrites below.

### Fields

| Field | Values |
| --- | --- |
| `item` | A section id with its heading (`s012 Meeting templates`, from a plan 14 inventory), `para:<id>`, or `file:<path>`. The id is copied from a digest or an inventory, never computed by hand. |
| `fate` | `redistributed <destination path>`; `removed-to-fit`; `removed-on-merit` (stale, wrong or low-value); `not-lost` (a reviewer rejects a presence verdict). |
| `value` | `real` or `low`. |
| `decision` | `restore-references`, `restore-main`, `drop`, `drop-pending`, `intended-change`, `purpose-change-pending`, `none`. |
| `reason class` | See the next table; it depends on the decision. |
| `reason` | One line, never empty. |

Reason classes by decision:

| Decision | Reason classes |
| --- | --- |
| `restore-references`, `restore-main` | `users-ask-by-name`, `reusable-template`, `tested-example`, `procedure-depends` |
| `drop`, `drop-pending` | `generic-model-knowledge`, `stale`, `wrong`, `out-of-scope`, `superseded-by <rule>` |
| `intended-change`, `purpose-change-pending` | `safety-fix`, `fact-update`, `scope-change` |
| `none` | `moved-to <path>`, `text-present` |

### Allowed (fate, value, decision) combinations

| Decision | Needs |
| --- | --- |
| `restore-references`, `restore-main` | fate `removed-to-fit` with value `real` |
| `drop`, `drop-pending` | fate `removed-on-merit` (any value), or fate `removed-to-fit` with value `low` |
| `intended-change` | fate `removed-on-merit` |
| `purpose-change-pending` | any fate except `not-lost` and `redistributed` |
| `none` | fate `not-lost` or `redistributed` |

A fixer never writes `removed-to-fit`: that is the loss the rules forbid. Those rows come only from plan 14's triage of past losses. A `drop-pending` row's interim restore to `references/` is not a `restore-*` decision.

### Rewrites on a user answer

A row is rewritten whole only in these cases:

- **Rejected drop.** The whole row becomes: fate `removed-to-fit`, value `real`, decision `restore-references`, a restore reason class taken from the user's answer, and reason "user rejected the drop (<date>)".
- **Accepted drop.** The `drop-pending` row's decision becomes `drop` and its reason becomes "user accepted the drop (<date>)"; the other fields are kept.
- **`purpose-change-pending` row** (restoring it would bring back a baseline purpose the current version dropped), rewritten on the user's answer:
  - Accepted: fate `removed-to-fit`, value `real`, decision `restore-references` (or `restore-main` when the procedure depends on it), a restore reason class taken from the user's answer, and reason "user accepted the purpose change (<date>)".
  - Rejected: fate `removed-on-merit`, value kept, decision `intended-change`, reason class `scope-change`, and reason "user kept the current purpose (<date>)".
