# Additional humanization diagnostics

Every cue here is contextual, not a ban; SKILL.md owns the workflow, the core diagnostics and the evidence rules. Era labels: **current** means still common in 2025-2026 model output; **older-model** means mostly 2022-2025 output. Older-model cues still show up in older text and pasted drafts, so check for them, but their absence says nothing about recent text.

In every example below, the after-text keeps only facts already in the before-text.

## Correspondence and disclaimers

### Chatbot correspondence (all eras)

Wrappers such as "Certainly!", "Let me know if...", "Is there anything else", "Here is a more detailed breakdown", "verify before publishing": delete them and never fill the gap with content the original did not contain.

### Sycophancy (all eras)

Praise of the reader or their question. Delete the praise and keep any substance it carried.

> Before: Great question! You're absolutely right that this is a complex topic. That's an excellent point about the economic factors.
>
> After: This is a complex topic, and you raised a point about the economic factors.

### Corrective-framing disclaimers (current, mid-2026)

Cues: "should be treated as X rather than Y", "the available information does not establish...", and the weakest variant, "should not be confused with...". Near-absent before mid-2026. Keep a real, sourced limitation, stated once and plainly, with its evidence scope: "the available information does not establish X" never becomes "X is unknown".

> Before: The listing should be treated as a local directory entry rather than an official registry, and the available information does not establish when the shop opened.
>
> After: The listing is a local directory entry, not an official registry. The available information does not establish the shop's opening date.

### Didactic disclaimers (older-model, 2023-2024)

Cues: "It's important to note/remember that...", telling an imagined reader to check local rules or avoid confusion. Delete the frame and keep the fact; keep a warning only when the source makes it.

> Before: It is important to note that the data shows a 4% drop.
>
> After: The data shows a 4% drop.

### Knowledge-cutoff disclaimers (older-model, 2022-2023)

Cues: "as of my last training update", "while specific details are limited/scarce", "based on available information". Delete the disclaimer, keep the uncertainty the sentence carries.

> Before: While specific details about the company's founding are not extensively documented in readily available sources, it appears to have been established sometime in the 1990s.
>
> After: The company's founding is not well documented in available sources; it appears to date from the 1990s.

### Prompt refusal (older-model)

Cues: "As an AI language model, I cannot...". Delete it; if the refusal stands where content should be, flag the gap to the user instead of writing the missing content.

## Conclusions and hedging

### Generic positive conclusions and section summaries (older-model)

Cues: "The future looks bright", "Exciting times lie ahead", "a step in the right direction", "In summary", "Overall". The current form is the "Despite... faces challenges" outline ending in SKILL.md. Delete a closer that adds no fact; never replace it with an event.

> Before: The company opened a second office in Lyon in 2024. The future looks bright, and exciting times lie ahead as it continues its journey toward excellence.
>
> After: The company opened a second office in Lyon in 2024.

### Excessive hedging (all eras)

Collapse stacked qualifiers ("could potentially possibly") to one that matches the source's certainty; never upgrade a hedge to certainty. A single "perhaps" or "tends to" reads human, so leave it.

### Wordy phrases (concision only, not an AI sign)

"In order to", "the fact that", "due to the fact that": these lean human rather than AI, so tighten them only when the brief asks for concision, and never cite them as AI patterns in the change note.

## Vocabulary by model era

Read the lists literally: the listed word is the cue, not its synonyms, and a literal sense (a typographic underscore, a steady pulse) is fine. Only a dense cluster counts.

- 2023-mid 2024 (older-model): additionally, crucial, delve (now rare), garner, interplay, intricate, key, landscape, meticulous, pivotal, tapestry, testament, vibrant.
- Mid 2024-mid 2025 (older-model): align with, enhance, fostering, highlighting, showcasing, underscore.
- Mid 2025-mid 2026 (current): emphasizing, enhance, highlighting, showcasing.
- Mid 2026 onward (current): leverage, multifaceted, foster, prioritize, practical, dependable, steady, quietly, universally, echoed, "matters".

## Style and mechanics (checklist; house style wins)

- **Em dashes (older-model, 2022-September 2026):** weak, so count them only alongside other cues; AI dashes are often spaced. Newer models suppress them, though Claude models still use more than professional writers do. Replacing each one with a comma or period risks the uniform-rhythm cue SKILL.md warns about.
- **Synonym cycling (older-model):** protagonist, main character, central figure for one person. A side effect of older repetition penalties, and non-native writers do it too: repeat the clearest term.
- **Formatting:** mechanical boldface, inline-header bullets ("**Performance:** Performance improved..."), title case in headings, emoji bullets, curly quotes, two-noun headings ("Awards and recognition"), unfilled placeholders ("[Company Name]"). Change them only when house style does not use them, and never inside protected text.

## License

Adapted from [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (revision 1383638008, 2026-11-03) by its contributors (WikiProject AI Cleanup), licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/); paraphrased, condensed and reorganised for prose editing, with rewritten examples. See the page history for authors.
