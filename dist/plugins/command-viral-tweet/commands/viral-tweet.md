---
description: Rewrite a tweet idea or draft into three X (Twitter) post variants with engagement trade-offs, character counts and a recommendation. Use when the user wants to sharpen a hook, make a post more shareable, turn a launch, lesson or announcement into a tweet, trim a long draft to 280 characters or split it into a thread, even without the word 'viral'. Drafting only; never publishes, schedules or manages an X account.
argument-hint: <tweet idea or topic>
---

# Viral Tweet Optimizer

Rewrite the user's idea into three post drafts, each aimed at a different engagement goal, then recommend one. Text only: never post, schedule or call any X API.

The user's tweet idea: $ARGUMENTS

If the argument is empty, ask for the idea or topic and stop. Invent nothing.

## Workflow

1. **Ground the facts.** List the facts the user supplied (what, numbers, names, timeframe). Only these may appear in a draft: never add a number, version, name, date or metric that is not in the input. Every variant keeps every one of them with its qualifiers (first, only, never, numbers, baselines); a variant may reorder or rephrase but never drops a qualifier. If a stronger hook would need an invented number, action or dramatic event, do not write it: propose it as a question for the user to confirm ("did you actually ...?"). If the argument is only a topic with no facts or stance, ask for one concrete fact or opinion and stop; if you cannot ask, write the three variants as clearly labelled templates with [placeholders] for the missing facts, never invented facts, and list the placeholders under BEFORE POSTING.
2. **Pick the payoff and objective.** Name what the reader gets (lesson, laugh, validation, news) and choose one primary objective: replies, reposts, dwell or clarity (sensitive posts). If the user states none: launch or announcement -> reposts, question or feedback request -> replies, lesson or story -> dwell; sensitive posts -> clarity, which overrides a requested replies or reposts objective (tell the user); any other post type (opinion, joke, personal milestone) -> dwell. State it in ANALYSIS. It decides which variant you RECOMMEND; the other two are deliberate contrasts.
3. **Write three variants** from the same factual core:
   - 3a. Levers, one each: (a) hook-led (lead with the concrete outcome if supplied; a contrast only when both sides are supported; else the author's concrete observation), (b) reply-led (end with one specific question tied to the supplied facts that the author genuinely wants answered, never a generic "thoughts?"), (c) repost-led (a self-contained, quotable statement).
   - 3b. If the user supplies a finished draft and asks only to shorten it, make VERSION 1 a minimal-edit trim that keeps their wording, then give the two other levers as optional contrasts.
   - 3c. **Sensitive posts** (grief, apology, factual updates): replace (b) and (c) with quieter variants (plain, reflective, minimal), label them "quiet variant" in the template, keep the author's emotion, and end none with a question or call to action; never add anger, FOMO or controversy.
4. **Check, then validate length**, in order:
   - 4a. Re-check each draft against the step 1 fact list (every qualifier kept, nothing invented) and the NEVER list; fix before counting.
   - 4b. Estimate the weighted count against the 280 limit of standard X posts: each URL or bare domain such as example.com/x counts 23, each CJK character and emoji 2. It is an estimate, not twitter-text: emoji sequences and Unicode normalisation can differ. In a thread count each post with its `1/n ` prefix.
   - 4c. Within 15 of the limit: trim further, or tell the user to confirm the count in X's composer. Shorten, recount.
   - 4d. Over the limit and the essential content cannot fit: ask whether to make a thread; on yes, or if you cannot ask, VERSION 1-3 become three alternative threads that keep every supplied fact and qualifier, each post counted with its `1/n ` prefix. Never return an over-limit standalone post. For a longer allowance, ask for the ceiling; if you cannot ask, keep 280.
5. **Recommend one** and say why. First check the candidate against the objective: replies needs one specific question the author wants answered; reposts needs a statement that makes sense without the author's context; dwell needs a concrete observation and a complete payoff with nothing withheld; clarity needs the least ambiguity and emotional spin. If it fails, revise it or pick another variant.

## Gotchas

- Compression can falsify: unchanged numbers lose meaning when the baseline, denominator, uncertainty or scope is cut, and a before/after becomes a causal claim. Keep the qualifier or use the thread.
- Unicode bold/italic "fancy text" costs 2 per glyph and screen readers read noise: never use it.

## NEVER

- Invent facts, numbers, customers or drama to make a hook punchier: readers and the author's reputation pay when the claim is false.
- Use engagement bait ("RT if you agree") or an unclosed curiosity loop ("you won't believe...", no payoff): readers feel manipulated and stop trusting the account. A real question the author wants answered is fine.
- Add hashtag stacks, "link in bio", or unrelated @mentions or links. Keep a link only if it substantiates the claim, and prefer it outside the main post text.
- Claim how X ranks or promotes posts; you cannot verify it. Explain trade-offs by what readers do.
- Write ragebait or in-group framing: it draws hostile replies and shuts out other readers.

## Output

**ORIGINAL:** the user's idea

**ANALYSIS:** facts kept, the intended reader and payoff, friction points, facts you would need confirmed

**VERSION 1 (hook):** draft, character count, one-line trade-off
**VERSION 2 (reply, or quiet variant for sensitive posts):** draft, character count, one-line trade-off
**VERSION 3 (repost, or quiet variant for sensitive posts):** draft, character count, one-line trade-off

In the three-thread case each VERSION block holds its thread, posts numbered `1/n`, each with its count; omit THREAD and let RECOMMENDED name the chosen VERSION's thread.

**RECOMMENDED:** exactly one version and why; never a second or interim pick (missing facts go under BEFORE POSTING instead)

**THREAD (only when a single-post run becomes a thread):** numbered posts `1/n ...`, each with its weighted count

**BEFORE POSTING:** thread or single post, media or none, and the questions to confirm any fact you could not verify
