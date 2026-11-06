# SBI Worked Examples

The Situation-Behavior-Impact (SBI) model was developed by the Center for Creative Leadership. The method and its rules live in `SKILL.md`; this file holds calibrated examples for the cases where a plain opener goes wrong.

## Observation versus interpretation

| Interpretation (do not say) | Observable (say) |
| --- | --- |
| "You don't care about quality." | "The last two PRs had no tests, and CI failed on both." |
| "You're not engaged." | "In the last three planning sessions you gave no estimates." |
| "You were being defensive." | "You said 'that's not my fault' before I finished the example." |
| "...which made Alex visibly frustrated." | "...Alex stopped before describing the dependency, and we only learned about it the next day." |
| "I know you're eager to help." | "What was going on for you when you jumped in?" |

The last two rows are the common slip: the feeling or motive sneaks in through the impact or the follow-up question.

## Interrupting in standup (constructive)

> **Situation:** "In yesterday's standup, while Alex was describing their blocker..."
>
> **Behavior:** "...you interrupted three times to suggest fixes before they finished..."
>
> **Impact:** "...Alex stopped before mentioning the dependency on the auth service, and we lost a day finding it."

**Follow-up:** "How did that exchange look from your side?" Then, if needed: "Going forward I'd like people to finish their update before we suggest fixes. Can you hold suggestions until then?"

## Recognition without an add-on

> "In Tuesday's review of the payment module, you caught the rounding edge case and added a test that reproduces it. That stopped a data-loss bug before release, and two juniors asked about the test in retro."

Stop there. Do not append "next time, also..."; save development points for a separate conversation.

## Disputed evidence

The user says a direct report pushed to `main` without review; the direct report says a reviewer approved in chat.

> "On Thursday the deploy log shows a push to `main` at 16:10 with no PR attached [situation, behavior]. The build broke for two hours [impact]. If it was approved somewhere else, I haven't seen it. Can you walk me through what happened?"

State the record, name the open question, and settle it with the chat history or the reviewer before treating the behavior as established. If it stays unresolved, the agreed step is about process ("approvals go on the PR"), not blame.

## Power gap

**Downward (manager to report), required change:**

> "...the API work landed Friday instead of Wednesday with no heads-up, and the frontend team was blocked two days. I need a message as soon as a date is at risk. What would make that easy to do?"

The expectation is stated as a requirement; the question is about how, not whether.

**Upward (report to manager):**

> "In Monday's planning, the release date was set before engineering estimated it. We've since dropped two stories. Could we get estimates in before dates are committed?"

An observation and a request, no verdict on the manager.

## Third-party report

A teammate told the user, in confidence, that a colleague's review comments feel dismissive. The user has not seen it.

Do not deliver it as "people have told me...". Either read the review threads and give feedback on what the user can see ("In PR #412 your comments were 'wrong' and 'redo' with no reason; the author asked twice what to change"), or encourage the teammate to raise it directly. Never reveal the source without consent.

## Recurring pattern

> "We talked on the 3rd about PRs failing CI before review. Since then, two of the last four have. The latest, on Monday, blocked Sam's merge for half a day. What's getting in the way of running the suite before opening a PR?"

One recent example plus a reference to the earlier conversation, not a list of every instance. If the earlier conversation never happened, say so: "I should have raised this sooner."
