---
description: Draft or rewrite a professional email to a peer, stakeholder, manager or leadership using What-Why-How. Use for status updates, approval requests, escalations, follow-ups, or when the user only asks to make a message shorter, clearer or less defensive, even without the word email. Produces a subject and body to paste; never sends. Not for casual chat replies; a finished draft can be reformatted for Slack or Teams on request.
argument-hint: [context or paste existing draft]
allowed-tools: Read, AskUserQuestion
---

# Draft Professional Email

Draft (or rewrite) an email. This command only produces text and cannot send mail; never claim or imply a message was sent. If asked to send, give the draft and say they must send it.

## Arguments

`$ARGUMENTS` - topic, known facts, or an existing draft to rewrite.

## Workflow

1. **Gather only what is missing.** Reuse everything in `$ARGUMENTS` and the conversation. Blocking: no topic and no source draft. Not blocking: a missing recipient name, date or outcome; use placeholders such as `[recipient]` or `[date]` and infer audience and outcome from context. When the request or source gives a deadline, or a date it can be derived from (for example "by Friday" with the dates stated), write that date; use a placeholder only when no date is given or derivable. Ask only for blocking gaps, with AskUserQuestion (plain text if unavailable); never invent names, dates, causes, metrics or ticket numbers. If nothing at all is known, ask in one question for the topic or facts, the recipient and the desired outcome, then stop. A pasted email the user received is the prior thread, not a draft to rewrite: answer it, taking the purpose from the user's instruction.
2. **Pick the strategy by underlying purpose, not audience**, in this order:
   (a) Reader test: what will the reader do in their first 10 seconds, and what would make them reply with a question instead of a decision?
   (b) Split: independent asks with different owners or deadlines go in separate drafts; keep dependent actions and coupled alternatives together.
   (c) Purpose: choose from the list below. A status update that needs a decision, or an FYI that carries an ask, is a request: the ask goes first. Anything else (announcement, thank-you, introduction) uses FYI: lead with what changes or what is recognised; "No response needed" unless an ask exists.
   Rewriting is an operation, not a purpose: apply the matching purpose strategy, then keep the source facts, voice and length or format limits. For "less defensive": keep evidence-backed accountability and uncertainty, cut justifications that do not help the reader decide, and replace defensive framing with observed impact plus the next action.
   - Request/approval: the ask and the options in the first sentence.
   - Status: the delta since the last update, then the risk.
   - FYI: what changes, then "No response needed"; never invent an ask.
   - Escalation: separate observed impact, what is still uncertain, and the mitigation in place.
   - Follow-up: reference the prior thread and restate the open ask. If the earlier message is not in context, use `[prior email date/subject]` and do not paraphrase it.
   - Audience only adjusts length and order, never the strategy. Leadership: decision in the first sentence, at most 5 sentences (a mixed-audience technical paragraph does not count toward the cap).
3. **Close by purpose.** Requests, escalations needing action and follow-ups end with the concrete ask, owner and confirmed or explicitly proposed deadline. Informational updates never manufacture an ask, owner or deadline: say "No response needed" when that removes ambiguity, otherwise close naturally (thanks, welcome, next update) in the user's voice. Fresh drafts default to under 150 words unless the facts need more.
4. **Validate against the source** before output: every source fact kept, no new names, dates, causes or numbers, proposed dates labelled as proposals, qualifiers such as "suspected" kept, any length limit met. Fix and recheck. If the source facts cannot fit a stated word limit, keep every fact, report the overage and ask (blocking) whether to relax the limit or drop named items; then update the effective limit and kept-fact set, exempt user-authorised omissions from the keep-every-fact check, redraft and recheck.
5. **Output** a ready-to-paste draft: `**Subject:**` line (specific, names the action or deadline), then the body as What-Why-How: What = the decision or impact, Why = the minimum context needed to act, How = the ask, owner and deadline (or "No response needed"). For several drafts (step 2), number them Draft 1, Draft 2, each with its own `**Subject:**` and body, and add one line on why they are split. Then offer one line of refinements (tone, length, jargon level, Slack/Teams format).

## Gotchas

- NEVER present a proposed date as a commitment without confirmation: recipients treat it as an agreed deadline. Label it a proposal and say who must confirm.
- In extension or scope requests, offer the trade-off (new date, or cut scope to keep the date) so the reader can decide; a request without a trade-off forces another round of email.
- NEVER paste internal logs, incident links or stack traces into a message to external or wider recipients unless disclosure and access are confirmed: they may expose sensitive details or leave the reader unable to act. If unknown, use a safe summary or placeholder and name what was withheld (a deliberate redaction is exempt from step 4's keep-every-fact rule); ask only when no safe draft is possible.
- NEVER put the ask only in the subject line: many clients truncate subjects on mobile and the reader misses it.
- NEVER leave placeholders unflagged: users paste and send drafts with [date] or [recipient] still in; after the draft, list every remaining placeholder.
- NEVER add recipients or CC unless asked: an unexpected CC can escalate a thread or leak scope to the wrong audience.
- NEVER turn suspected causes, tentative estimates or unconfirmed impact into facts while cutting hedging. Keep qualifiers such as "suspected" or "not yet confirmed" while removing padding: recipients act on apparent certainty.
- Mixed audience (peers plus leadership): write for the least technical reader and put technical detail in a short final paragraph: leadership stops at the first unfamiliar term and the ask is lost.

## Example Usage

`/command-compose-email:compose-email <context or pasted draft>`.
