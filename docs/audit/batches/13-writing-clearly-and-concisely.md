# Batch 13

## writing-clearly-and-concisely (skill)

### writing-clearly-and-concisely#D7-1
- severity: medium
- dimension: D7
- location: skills/writing-clearly-and-concisely/evals/evals.json:26
- fix: Keep technical diagnosis as a trigger negative and add in-scope output cases covering must/should/may, an unless condition, embedded quotations or identifiers, an unknown actor, and already-minimal text. Assert preservation of each semantic invariant rather than requiring particular wording.

### writing-clearly-and-concisely#D7-1
- severity: medium
- dimension: D7
- location: skills/writing-clearly-and-concisely/evals/evals.json:1
- fix: Add an eval with a multi-paragraph README fixture and a brand-voice prompt asserting suggestions are flagged, not silently rewritten

### writing-clearly-and-concisely#D8-1
- severity: low
- dimension: D8
- location: skills/writing-clearly-and-concisely/SKILL.md:16
- fix: The output format is described but never shown; add a three-line worked example (original, rewrite, check line) so the format is unambiguous

### writing-clearly-and-concisely#D1-1
- severity: medium
- dimension: D1
- location: skills/writing-clearly-and-concisely/SKILL.md:13
- fix: Consolidate ordinary preserve-meaning and remove-repetition reminders into one short checkpoint. Keep the technical semantic exceptions prominent and demonstrate the decisions with a few difficult before/after cases rather than repeating the general policy.

### writing-clearly-and-concisely#D1-2
- severity: low
- dimension: D1
- location: skills/writing-clearly-and-concisely/SKILL.md:30
- fix: Remove the generic delegation instruction. Retain only the writing-specific fallback: preserve a compact invariant list and consult the relevant reference section.

### writing-clearly-and-concisely#D2-1
- severity: medium
- dimension: D2
- location: skills/writing-clearly-and-concisely/SKILL.md:12
- fix: Add a short original-draft branch: identify the reader and intended action, establish supported facts and required terminology, organize information around that action, draft, then apply the existing semantic and concision checks.

### writing-clearly-and-concisely#D6-1
- severity: medium
- dimension: D6
- location: skills/writing-clearly-and-concisely/SKILL.md:16
- fix: Check meaning and length internally by default and return only the requested prose. Permit unchanged or longer wording when fidelity or clarity requires it, explain that exception briefly, and show counts or comparison excerpts only when requested or materially useful.

### writing-clearly-and-concisely#D1-1
- severity: low
- dimension: D1
- location: skills/writing-clearly-and-concisely/SKILL.md:33
- fix: Tautological harness restatement; replace with the actual constraint: 'when context is tight, read only the relevant reference section and edit locally'

### writing-clearly-and-concisely#D2-1
- severity: low
- dimension: D2
- location: skills/writing-clearly-and-concisely/SKILL.md:13
- fix: No default when the user cannot supply evidence mid-edit; default to preserving scope and flag the missing evidence at the end rather than blocking

### writing-clearly-and-concisely#D3-1
- severity: low
- dimension: D3
- location: skills/writing-clearly-and-concisely/SKILL.md:28
- fix: Safeguards omit dialect/house-spelling consistency; add 'Never switch dialect (en-US/en-GB) or house spelling while tightening; keep the source's convention'

### writing-clearly-and-concisely#D6-1
- severity: low
- dimension: D6
- location: skills/writing-clearly-and-concisely/SKILL.md:16
- fix: The count check is defined only for sentence-sized rewrites; extend it to documents with total or per-section word counts
