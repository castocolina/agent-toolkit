# Worked examples for writing a fix

Illustrations for the fix text of a finding. This file never sets a score, a band, a point value or a verdict field: scoring comes only from `rubric.md`. Every skill named below is an invented illustration unless the text says it lives in `anthropics/skills`. Read a live upstream file before quoting it; upstream text changes.

## Contents

- [D2 mindset and procedures](#d2-mindset-and-procedures): a thinking template, a domain procedure, a generic procedure
- [D3 NEVER items](#d3-never-items): an expert item and a weak one
- [D4 description](#d4-description): an annotated good and poor pair
- [D5 loading triggers](#d5-loading-triggers): a scenario trigger and a bare list
- [D2 pattern fit](#d2-pattern-fit-exemplars-and-selection-guide): one exemplar skill per pattern and a selection guide
- [D8 tools and fallbacks](#d8-tools-and-fallbacks): a decision table with common issues and a vague counter-example
- [Failure pattern root causes](#failure-pattern-root-causes): why each of the nine patterns happens
- [Closing check](#closing-check): the meta-question and the compressed expert brain

## D2 mindset and procedures

A skill should transfer how an expert thinks and the domain sequences the model would not derive. Three shapes:

A thinking pattern, the template to suggest when a skill has steps but no reasoning:

```markdown
Before [action], ask yourself:
- **Purpose**: What problem does this solve? Who uses it?
- **Constraints**: What are the hidden requirements?
- **Differentiation**: What makes this solution memorable?
```

A domain procedure, valuable because the order is not obvious (a redlining-style sequence):

```markdown
### Redlining workflow (the sequence is specific to this domain)
1. Convert the document to markdown and keep the tracked changes:
   `pandoc --track-changes=all` (the docx reader takes `accept`, `reject` or `all`;
   `all` keeps insertions, deletions and comments).
2. Map each changed text to its place in the XML: search the text in `word/document.xml`.
3. Apply the changes in small batches of 3 to 10, so a bad batch is easy to find.
4. Pack the file and verify that every change was applied.
```

The pandoc option was checked 2026-11-15 at https://pandoc.org/MANUAL.html. Read `pandoc --help` or the manual for the installed version before pinning a flag in a skill.

A generic procedure, redundant because the model already does this unprompted:

```markdown
Step 1: Open the file
Step 2: Find the section
Step 3: Make the change
Step 4: Save and test
```

The two checks behind these examples: does the skill tell the model what to think about, and how to do the things it would not know? A good skill gives both when both are needed.

## D3 NEVER items

Half of expert knowledge is what not to do, learned by stepping on landmines the model has not stepped on. A good NEVER item names the condition, the failure it prevents and a better action.

An expert item (specific, with its reason):

```markdown
- NEVER keep the default font stack and the default accent color when the brief names no brand.
  Condition: no brand guide in the request.
  Failure: every page looks like the same template, so the reader cannot tell this product from any other.
  Instead: choose a font pair and a palette from the product's subject and say why in one line.
- NEVER save recalculated formulas over the user's original workbook.
  Condition: the file is the only copy of the inputs.
  Failure: one bad recalculation destroys the source data.
  Instead: write the result to a new file and compare the cell counts with the original.
```

A weak item (vague, no reason, nothing to act on):

```markdown
Avoid making mistakes.
Be careful with edge cases.
Don't write bad code.
```

The test: would an expert read the list and say "yes, I learned that the hard way", or "that is obvious to everyone"?

## D4 description

The description is the only text an agent sees before it loads the skill, so it must answer three questions: WHAT the skill does, WHEN to use it, and which KEYWORDS a user would say. A boundary ("Not for ...") prevents wrong triggers.

A good description, annotated (an invented skill):

```yaml
description: >-
  Match bank-statement lines to open invoices and list the unmatched ones with a likely cause.
  Use when the user asks to reconcile payments, match a statement to invoices or find a missing
  payment, even if they do not say "reconcile". Reads CSV and OFX exports.
  Not for issuing invoices or filing taxes.
```

- WHAT: "Match bank-statement lines to open invoices and list the unmatched ones with a likely cause".
- WHEN: "Use when the user asks to reconcile payments, match a statement to invoices or find a missing payment", including the case where the user names no domain term.
- KEYWORDS: reconcile, payments, statement, invoices, missing payment, CSV, OFX.
- Boundary: "Not for issuing invoices or filing taxes".

Poor descriptions:

```yaml
description: "Handles document-related features"
description: "A helpful skill for various tasks"
```

- WHAT is vague: which features, on which documents?
- WHEN is missing: nothing says when to use it.
- KEYWORDS are missing: no file type, no domain term, no action verb.
- The second one is useless: the agent has no idea when to activate it.

## D5 loading triggers

Loading too little leaves references unused; loading too much dilutes the context. A good trigger sits in the workflow step that needs the file, names the scenario that calls for it, and says what not to load for that scenario.

Good (a scenario trigger plus "Do NOT load"):

```markdown
### Building a quarterly summary

Read `references/summary-layout.md` when the request asks for a one-page quarterly summary:
it holds the section order and the length limits.
Do NOT load `references/appendix-tables.md` or `references/export-formats.md` for this task.
```

Bad (a list at the end, with no scenario):

```markdown
## References
- summary-layout.md - layout
- appendix-tables.md - tables
- export-formats.md - exports
```

A skill with no references and a short body needs none of this; judge it on conciseness and self-containment.

## D2 pattern fit: exemplars and selection guide

An exemplar gives a judge a known skill to compare a pattern against. All seven directories exist under `skills/` in https://github.com/anthropics/skills (checked 2026-11-15; read the live file before comparing, since upstream edits them).

| Pattern | Exemplar skill | Key characteristics | When to use |
|---------|----------------|---------------------|-------------|
| Mindset | frontend-design | Thinking over technique, strong NEVER list, high freedom | Creative tasks that need taste |
| Navigation | internal-comms | Minimal SKILL.md that routes to sub-files | Several distinct scenarios |
| Philosophy | canvas-design | Philosophy first, then expression; craft quality | Art or creation that needs originality |
| Process | mcp-builder | Phased workflow with checkpoints, medium freedom | Complex multi-step projects |
| Tool | docx, pdf, xlsx | Decision trees, code examples, low freedom | Precise operations on a specific format |

Pattern selection guide:

| The task | Recommended pattern |
|----------|---------------------|
| Needs taste and creativity | Mindset |
| Needs originality and craft quality | Philosophy |
| Has several distinct sub-scenarios | Navigation |
| Is a complex multi-step project | Process |
| Is a precise operation on a specific format | Tool |

The pattern sizes in `rubric.md` are heuristics from the original author, not spec limits: the spec limit is 500 lines.

## D8 tools and fallbacks

A usable skill names the primary tool, the fallback and the condition that triggers the fallback, then lists the failures that really happen.

Good (a decision table plus common issues):

```markdown
| Task | Primary tool | Fallback | Use the fallback when |
|------|--------------|----------|-----------------------|
| Read text | `pdftotext` | PyMuPDF | The layout or the position of text matters |
| Extract tables | `camelot-py` | `tabula-py` | camelot finds no table or splits columns wrongly |

**Common issues**:
- Scanned PDF (image only): text extraction returns little or no text. Run OCR first.
- Encrypted PDF: opening or reading fails. With PyMuPDF check `Document.needs_pass`, then call
  `Document.authenticate(password)`; ask the user for the password and never guess it.
```

Checked 2026-11-15: `camelot-py` and `tabula-py` both exist on PyPI (https://pypi.org/project/camelot-py/, https://pypi.org/project/tabula-py/), and PyMuPDF documents `needs_pass` and `authenticate` at https://pymupdf.readthedocs.io/en/latest/document.html. The table is an illustration, not a tool recommendation: do not pin package versions in a skill, and read `pdftotext --help` for the installed flags. The scanned-PDF behavior was not re-run here.

Poor (vague):

```markdown
Use appropriate tools for PDF processing.
Handle errors properly.
Consider edge cases.
```

## Failure pattern root causes

`rubric.md` lists the nine patterns with their fixes. Each one has a root cause that tells you what to ask the author:

1. The Tutorial: the author assumes a skill should teach the model.
2. The Dump: no progressive disclosure design.
3. The Orphan References: no explicit loading triggers.
4. The Checkbox Procedure: the author thinks in procedures, not in thinking frameworks.
5. The Vague Warning: the author knows things can go wrong but has not articulated the specifics. The template to ask for: "NEVER do X because [the specific problem that experience teaches]".
6. The Invisible Skill: the description is vague, lacks keywords or has no trigger scenarios.
7. The Wrong Location: a misunderstanding of three-layer loading; the body is loaded only after the triggering decision, so trigger information in the body is never seen in time.
8. The Redundant Extras (also called The Over-Engineered): the author treats a skill like a software project. Symptom list: `README.md`, `CHANGELOG.md`, `INSTALLATION_GUIDE.md`, `CONTRIBUTING.md`. In this repository `README.md` is required, so it is never part of this pattern (see `rubric.md`).
9. The Freedom Mismatch: the author did not consider the fragility of the task.

## Closing check

When a judgment is close, return to one question: would an expert in this domain, looking at this skill, say "yes, this captures knowledge that took me years to learn"? If yes, the skill has real value. If no, it compresses what the model already knows.

The best skills are compressed expert brains: years of a designer's aesthetic judgment condensed into a short mindset, or a document expert's operational experience condensed into a decision tree. What gets compressed must be things the model does not have; otherwise it is garbage compression.

This is a mental model, not a scoring rule: it never adds or removes a point, and the bands in `rubric.md` decide the score.
