---
description: Draft or rewrite a professional email to a peer, stakeholder, manager or leadership using What-Why-How. Use for status updates, approval requests, escalations, follow-ups, or when the user only asks to make a message shorter, clearer or less defensive, even without the word email. Produces a subject and body to paste; never sends. Not for casual chat replies; a finished draft can be reformatted for Slack or Teams on request.
argument-hint: "[context or paste existing draft]"
allowed-tools: Read, AskUserQuestion
---

# Draft Professional Email

Draft (or rewrite) an email. This command only produces text and cannot send mail; never claim or imply a message was sent. If asked to send, give the draft and say they must send it.

## Arguments

`$ARGUMENTS` - topic, known facts, or an existing draft to rewrite.

Three invocation forms:

- With context: `/command-compose-email:compose-email Ask my manager to extend the billing-export deadline by a week; the vendor's schema change blocked me.`
- With an existing draft to rewrite: `/command-compose-email:compose-email` followed by the pasted draft.
- With no argument: `/command-compose-email:compose-email`; the command asks once for the topic or facts, the recipient and the desired outcome, then stops.

## Workflow

1. **Gather only what is missing.** Reuse everything in `$ARGUMENTS` and the conversation. Blocking: no topic AND no source draft AND no received message: ask once and stop only then. A received message plus an instruction to answer it is the prior thread, so draft the reply (see the last sentence of this step). Not blocking: a missing recipient name, date or outcome; use placeholders such as `[recipient]` or `[date]` and infer audience and outcome from context. When the request or source gives a deadline, or a date it can be derived from (for example "by Friday" with the dates stated), write that date; use a placeholder only when no date is given or derivable. Ask only for blocking gaps, with AskUserQuestion; never invent names, dates, causes, metrics or ticket numbers. If nothing at all is known, ask in one question for the topic or facts, the recipient and the desired outcome, then stop. When AskUserQuestion is unavailable, ask that same single question in plain text and stop. A pasted email the user received is the prior thread, not a draft to rewrite: answer it, taking the purpose from the user's instruction.
2. **Pick the strategy by underlying purpose, not audience**, in this order:
   (a) Reader test: what will the reader do in their first 10 seconds, and what would make them reply with a question instead of a decision?
   (b) Split: independent asks with different owners or deadlines go in separate drafts; keep dependent actions and coupled alternatives together.
   (c) Purpose: choose from the list below. A status update that needs a decision, or an FYI that carries an ask, is a request: the ask goes first. Tie-breaks: if the reader must decide or approve, it is a Request even when it also reports status; if a prior unanswered ask exists, Follow-up wins and the escalation content (impact, uncertainty, mitigation) goes in Why; use Escalation only when impact, uncertainty and a mitigation are all present; otherwise Status when the message is a progress report without a decision request, and FYI for other informational messages; a thank-you, announcement or introduction that also contains an ask is a Request, and the recognition or announcement goes in Why. Anything else (announcement, thank-you, introduction) uses FYI. A thank-you and an introduction keep the FYI no-ask rule but use their own one-line closings instead of the FYI change-lead: thank-you closes with one line of thanks that names the person or effort; introduction closes with one line saying who follows up (for example "I will leave the two of you to take it from here"); the announcement keeps the "No response needed" closing.
   Rewriting is an operation, not a purpose: apply the matching purpose strategy, then keep the source facts, voice and length or format limits. For "less defensive": keep evidence-backed accountability and uncertainty, cut justifications that do not help the reader decide, and replace defensive framing with observed impact plus the next action.
   - Request/approval: the ask and the options in the first sentence.
   - Status: lead with the delta since the last update, then the risk.
   - FYI: lead with what changes or what is recognised, then "No response needed" unless an ask exists; never invent an ask.
   - Escalation: separate observed impact, what is still uncertain, and the mitigation in place.
   - Follow-up: reference the prior thread and restate the open ask. If the earlier message is not in context, use `[prior email date/subject]` and do not paraphrase it.
   - Default caps by purpose: Request, Escalation and Follow-up use the What 1-2 and Why 2-3 sentence caps (step 5); Status and FYI-type drafts (thank-you, announcement, introduction) follow the user's voice inside the 150-word default, within the user's limit if given. The What and Why sentence caps are flexible defaults and also apply to a draft the user gave a length limit, unless the user's own limit or format instruction replaces them.
   - Audience only adjusts length and order, never the strategy. Leadership: put the decision or approval request first when one exists; otherwise lead with the informational change, impact or recognition the purpose selects. Keep the five-sentence default: at most 5 sentences (a mixed-audience technical paragraph does not count toward the cap). Peer: under 150 words, jargon kept. Stakeholder and manager: business effect first, jargon translated. Leadership's 5-sentence cap is the one exception to the 150-word default.
3. **Close by purpose.** Requests, escalations needing action and follow-ups end with the concrete ask, owner and confirmed or explicitly proposed deadline. Informational updates never manufacture an ask, owner or deadline: say "No response needed" when that removes ambiguity, otherwise close naturally (thanks, welcome, next update) in the user's voice. Fresh drafts default to under 150 words unless the facts need more.
4. **Validate against the source** before output: every source fact kept, no new names, dates, causes or numbers, proposed dates labelled as proposals, qualifiers such as "suspected" kept, any length limit met. Fix and recheck. If the source facts cannot fit a stated word limit, keep every fact, report the overage and ask (blocking) whether to relax the limit or drop named items; then update the effective limit and kept-fact set, exempt user-authorised omissions from the keep-every-fact check, redraft and recheck.
5. **Output** a ready-to-paste draft: `**Subject:**` line (specific, names the action or deadline, 5-8 words), then the body as What-Why-How: What = the decision or impact (1-2 sentences), Why = the minimum context needed to act (2-3 sentences), How = the ask, owner and deadline (or "No response needed"; a thank-you or introduction uses its own closing from step 2 and never gets a manufactured ask). The 5-8 word subject rule applies to every draft. Apply the What and Why sentence caps as set by the default caps by purpose in step 2. Open with What: no throat-clearing such as "I hope this email finds you well". The subject length, bullet counts, paragraph lengths and sentence caps in this step and in Gotchas are defaults: an explicit user instruction about format or length takes precedence. Factual accuracy, disclosure protection and proposed-versus-confirmed commitments stay mandatory whatever the user's format. For several drafts (step 2), number them Draft 1, Draft 2, each with its own `**Subject:**` and body, and add one line on why they are split. Then offer one line of refinements (tone, length, jargon level, Slack/Teams format).

## Gotchas

- Subject: lead with an action tag when one applies, `[Action Required]`, `[Decision Needed]` or `[FYI]`, and add a deadline tag such as `[Due Friday]` only when the deadline is known and urgent; the tag counts toward the 5-8 words. NEVER write a vague subject such as "Quick question", "Update" or "FYI" alone: the reader cannot triage it and it is skipped or answered late.
- Body: bullets only for 3-5 parallel points (never more), bold the one key fact (the decision, the date or the ask), keep paragraphs to 2-3 sentences; a wall of text hides the ask.
- NEVER present a proposed date as a commitment without confirmation: recipients treat it as an agreed deadline. Label it a proposal and say who must confirm.
- In extension or scope requests, offer the trade-off (new date, or cut scope to keep the date) so the reader can decide; a request without a trade-off forces another round of email.
- NEVER paste internal logs, incident links or stack traces into a message to external or wider recipients unless disclosure and access are confirmed: they may expose sensitive details or leave the reader unable to act. If unknown, use a safe summary or placeholder and name what was withheld (a deliberate redaction is exempt from step 4's keep-every-fact rule); ask only when no safe draft is possible.
- NEVER put the ask only in the subject line: many clients truncate subjects on mobile and the reader misses it.
- NEVER leave placeholders unflagged: users paste and send drafts with [date] or [recipient] still in; after the draft, list every remaining placeholder.
- NEVER add recipients or CC unless asked: an unexpected CC can escalate a thread or leak scope to the wrong audience.
- NEVER turn suspected causes, tentative estimates or unconfirmed impact into facts while cutting hedging. Keep qualifiers such as "suspected" or "not yet confirmed" while removing padding: recipients act on apparent certainty.
- Replying to a message with disputed assertions: attribute the sender's claim to them ("you say the cutoff was 5 Nov") instead of adopting it as fact, and keep the user's own position distinct from the resolution you are requesting, so the reader sees what is disputed and what you want done.
- Mixed audience (peers plus leadership): write for the least technical reader and put technical detail in a short final paragraph: leadership stops at the first unfamiliar term and the ask is lost.

## Example Usage

`/command-compose-email:compose-email <context or pasted draft>`.

Input: `/command-compose-email:compose-email Ask my manager Dana Ruiz to extend the billing-export deadline from Friday 7 Nov to Friday 14 Nov. I am blocked on the vendor's schema change, which landed Tuesday. I can cut the CSV report to keep 7 Nov.`

Output:

**Subject:** [Decision Needed] Extend billing export deadline

Dana, can you approve moving the billing-export deadline from Friday 7 Nov to **Friday 14 Nov (proposed)**?

I am blocked on the vendor's schema change, which landed Tuesday, so the export cannot finish by 7 Nov. If you prefer to keep 7 Nov, I can cut the CSV report from scope.

Please reply by [reply-by date] with your choice. 14 Nov is my proposal and is not agreed until you confirm.

Thanks,
[your name]

Placeholders to fill before sending: `[reply-by date]`, `[your name]`.

Overflow, where the facts do not fit a stated word limit (step 4): the output reports the count, names the facts at risk, asks, and shows no draft until the user answers.

Input: `/command-compose-email:compose-email Tell the finance team the audit moves from Monday 3 Nov to Thursday 6 Nov in room B-204, and invoices for vendors A through M are due Wednesday 5 Nov. Keep it to 15 words at most.`

Output:

A body that keeps all three facts runs about 25 words (an example count, not a minimum), 10 over your limit of 15. The date change alone takes about 14 words, so these facts are at risk: the room (B-204) and the invoice deadline for vendors A through M (Wednesday 5 Nov).

Should I relax the limit to about 25 words, or drop a named item (the room, or the invoice deadline)? I will write the draft after you answer.
