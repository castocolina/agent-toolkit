---
name: writing-clearly-and-concisely
description: Draft or copyedit English prose for clarity and concision in READMEs, docs, commit messages, error messages, UI copy, help text, policies, reports and explanations. Use when asked to tighten, shorten, rewrite, make clearer, cut wordiness, passive voice or puffery, or write new reader-facing text, even a single sentence. Keeps must/should/may, conditions, quotations, identifiers and house style intact. Not for making a draft sound less AI-written or humanizing it (humanizer), technical diagnosis, code changes, translation, summarizing logs or data, word counting alone, or verbatim extraction.
---

# Writing Clearly and Concisely

Expository and technical prose. The hard part is not cutting words; it is cutting words without changing what a reader is allowed, required or told to do, and without stating a fact nobody supplied.

## Pick the branch

| The request | Branch |
|---|---|
| Tighten, copyedit or clarify supplied text, including "rewrite it but keep our brand voice" | Edit |
| "Restructure", "reorganize", "merge the duplicate sections", or a long document that repeats itself | Structure |
| Write new text, including new copy "in our brand voice" | Draft |
| "Point out", "suggest", "where is it wordy", "don't rewrite it" about supplied text | Flag |
| "Tighten this" with no text supplied | none: one line asking for the text; never invent a sample to rewrite |

Brand voice is an invariant, not a reason to Flag: in Edit keep the source's tone; in Draft copy the tone from samples the user supplied, and with no samples write plain copy and end with `Needs: a sample of the brand voice`.

Protected quoted material (a quotation, testimonial, quoted law or contract clause, a character's dialogue) is never rewritten in any branch. Edit the prose around it, keep the quoted text verbatim, and put any suggestion about it in the Output's suggestion list.

## Claims checkpoint

Task-specific claims need a source the user supplied or you verified (the prompt, a provided file, the repository): product behavior, button and menu names, metrics, limits, timeouts, versions, URLs, contacts, error codes, customer names and other operational details. When one is missing, write around it and add `Needs: <the fact>`; do not stop to ask. Established general knowledge (what HTTP 401 means, what a dry run is) needs no source in explanatory prose.

Before keeping any specific in a rewrite or draft, ask: could a reader act on this and be wrong? If yes and no source supplied it, it is invented. A fabricated figure, contact or step reads as fact and ships.

## Invariant checkpoint

Before changing a word, ask: would a reader act differently if this changed? Each "yes" survives with the same force. Check the result against this table before returning it; keeping an invariant beats saving a word, so a rewrite that is no shorter is still done.

| Invariant | Example | Why changing it fails |
|---|---|---|
| Normative force | `must`, `should`, `may`, "recommended" | An imperative ("Store keys in a vault") reads as `must`; an auditor treats a `should` turned `must` as a new requirement. |
| Conditions and qualifiers | `unless`, `except`, `only if`, `up to`, "wherever reasonably possible", `not`, `likely` | The shorter sentence states a broader or firmer rule that is false for the excluded case. |
| Outcomes | "and the download will not proceed" | Readers act on what happens next; cutting it as filler removes the consequence. |
| Verbatim material | quotations, code, identifiers, flags, schema keys, error strings, numbers, dates | Users copy and search them; a cleaned-up error string no longer matches the log. |
| The actor | only as far as the source names one | Active voice with an invented actor assigns responsibility nobody established (incident reports, legal text). |
| Dialect, house spelling, voice | en-GB `authorised`, product casing, a playful brand tone | The mixed result reads as a mistake and overrides a choice the author already made. |
| Markdown structure | heading levels and text, link targets, list markers, front matter, table columns | A heading's text is its anchor: changing it breaks inbound links and generated tables of contents. |

## Edit branch

1. Cut what carries no invariant: puffery ("groundbreaking", "seamless"), throat-clearing ("It is important to note that"), stacked hedges ("might potentially"), empty `-ing` tails ("ensuring a robust experience"), repetition.
2. Replace a vague phrase only with a specific that passes the claims checkpoint; otherwise keep the vague scope in neutral words.
3. Use active voice only when the source names the actor.
4. Run both checkpoints.

## Structure branch

1. Default, when the user did not authorise restructuring: keep every heading, its level and its text, and every anchor; consolidate only the prose inside each section, by the Edit branch.
2. Only when the user authorises it ("restructure", "merge", "remove sections"): diff near-duplicate sections line by line first, merge into one section, and carry every condition, limit and version note from either copy into the survivor. Then fix paragraph order, then edit sentences; rewording a section you later delete wastes the pass.
3. Keep explicit anchor IDs (`{#install}`, `<a id>`). List every heading you removed or renamed in the Output note, because its derived anchor (`#installation`) now points nowhere.

## Draft branch

1. Apply the claims checkpoint to every specific before writing it.
2. Error message: quote the failing identifier or value verbatim and name the exact command or setting that fixes it. If no fix was supplied, write what failed and add `Needs: remediation`. No apology or preamble.
3. Run the invariant checkpoint on the draft.

## Output

| Branch | Return |
|---|---|
| Edit, Structure | the rewritten text, then the applicable notes |
| Draft | the draft, then the applicable notes |
| Flag | numbered suggestions only, no rewritten text, not even of one section |

Notes, one short line each, only when they apply:

- the text is unchanged or longer because an invariant required it, or it is already minimal ("Kept `should` and the `409` exception; no shorter wording keeps both.", "Already minimal.", "Kept the passive: the source names no actor.");
- `Needs: <the missing fact>`;
- Structure: "Removed or renamed headings: ..." with the old anchors;
- counts, only when asked: one sentence gets "21 → 9 words"; a document gets the total and per-section counts.

Suggestions use `"<quoted original fragment>" → "<proposed text>" (reason)`. Order them: invariant risks and factual errors first, then cuts by the number of words they save. Stop at about 10 and name the sections where more occur. In Edit and Structure they come after the rewrite, and only for protected quoted material or when the user asks for an explanation of the changes (then at most 5 items); the one-line note limits above apply only when no explanation was asked for.

Worked example (Edit):

> Original: It is important to note that clients should retry failed requests, unless the server returns `409 Conflict`, in order to ensure robust reliability.
>
> Returned: Clients should retry failed requests unless the server returns `409 Conflict`.

No note follows, because nothing was kept for an invariant's sake and nothing is missing.

## Hard cases

| Original | Wrong rewrite | Right rewrite | Why |
|---|---|---|---|
| It is required that tokens be rotated every 90 days, and it is recommended that they be stored in a vault. | Rotate tokens every 90 days and store them in a vault. | Tokens must be rotated every 90 days and should be stored in a vault. | The bare imperative turns "recommended" into `must`. |
| The job will automatically attempt to retry any uploads that have failed, except in cases where the error is `403`, in which case it stops and sends an alert to the owner. | The job retries failed uploads automatically. | The job retries failed uploads automatically, except on `403`: then it stops and alerts the owner. | The cut states a rule that is false for `403`. |
| The production database was dropped at 03:12 UTC. | An engineer dropped the production database at 03:12 UTC. | Unchanged, with "Kept the passive: the source names no actor." | Active voice would invent the actor. |
| Go ahead and set the value of `retry_limit` to 3; at that point the log shows "Retry limit exceeded". | Set the retry limit to 3; the log then reports that the limit was exceeded. | Set `retry_limit` to 3; the log then shows "Retry limit exceeded". | Readers copy the key and search the log for the exact string. |
| This update significantly improves performance. | This update cuts latency by 40%. | This update improves performance. `Needs: a measured figure.` | The figure fails the claims checkpoint. |
| Run `make test` before you push. | Test before pushing. | Run `make test` before pushing. | The command and the ordering stay; only "you" goes. |
| Never force-push to `main`. | Don't force-push. | Unchanged, with "Already minimal." | Every word is an invariant: the negation, the action, the branch. |

## NEVER

The checkpoints own invariants and claims; these are the failures they do not catch.

- NEVER merge two near-duplicate sections without diffing them first: one copy often holds the only `unless`, limit or version note, and the merge silently drops it.
- NEVER swap a precise technical term for a plainer one that means something else ("deprecated" is not "old", "idempotent" is not "safe").
- NEVER treat a word ("delve") or a punctuation habit (em dashes) as proof that text is AI-written: humans use them too, and the accusation lands on a person.

## Reference load list

Load at most the one section that answers the open question; the rules above cover ordinary tightening without any reference. When context is tight, read only that section and edit locally.

| When | Read | Skip |
|---|---|---|
| A paragraph needs restructuring, or a sentence still sprawls after the Edit branch | `elements-of-style/03-elementary-principles-of-composition.md`, the matching rule (8-9 paragraphs, 10 active voice, 13 needless words, 16 related words, 18 emphasis) | the other rules |
| A specific comma, possessive or dangling-participle question | `elements-of-style/02-elementary-rules-of-usage.md`, the matching rule (1-7) | |
| Formatting numerals, parentheses, quotations or references | `elements-of-style/04-a-few-matters-of-form.md` | |
| A disputed word ("comprise", "due to", "less/fewer") | `elements-of-style/05-words-and-expressions-commonly-misused.md`; contemporary usage, singular "they" and house style win over its 1918 prescriptions | |
| A clarity edit where the user names a specific stock pattern to cut (rule of three, negative parallelism, "serves as a testament") | `signs-of-ai-writing.md`, only the section for that pattern under "Regression to the Mean", "Language and Grammar" or "Punctuation and Formatting" | its Markup, Citations and AFC sections: Wikipedia-only |

Do NOT load `signs-of-ai-writing.md` for ordinary copyediting, and never load `elements-of-style/01-introductory.md` (it holds no rules). A request only to make a draft sound less AI-written is the humanizer skill's job, not this one.
