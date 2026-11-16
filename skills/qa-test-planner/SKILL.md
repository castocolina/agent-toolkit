---
name: qa-test-planner
description: "Create manual QA test plans, executable test cases, regression and smoke suites, a ship-or-block release decision, Figma design-validation checklists and structured bug reports (repro rate, environment, Open Questions). Use when the user invokes qa-test-planner by name or /qa-test-planner, including a request that only implies the deliverable once the name is present: a password-reset or checkout plan, cases for a flow, a smoke or targeted suite, a ship-or-block decision, a Figma frame comparison, or a bug whose rate or browser is unknown. Not for Cypress, Playwright, unit or API automation, fixing implementation code, or any QA request that does not name this skill."
metadata:
  trigger: explicit
---

# QA Test Planner

Manual QA deliverables in which every case traces to a requirement and a risk, and every expected result is observable. Activate only on explicit invocation by name.

## 1. Route the request

| Request says | Deliverable | Read first | Do NOT load |
| :- | :- | :- | :- |
| "plan", release or feature scope, entry/exit criteria | Test plan (section 3) | `references/test_plan_template.md` at once when the request names entry or exit criteria, a risk table, an executive summary, deliverables or a full plan document, or the user asks for a plan example; a plan request that asks for none of these keeps the section 3 shape; `references/regression_testing.md` only if the plan schedules a regression run | bug template; test template unless cases are also requested (bullet below) |
| "cases", "test this flow", or unclear | Manual cases with a smoke core (section 4) | `references/test_case_templates.md`; add `references/test_case_examples.md` only when a complete worked case is requested | `references/bug_report_templates.md` |
| "regression", "smoke", "what to retest after X" | Prioritized suite and run report | `references/regression_testing.md`; add `references/figma_validation.md` only when a selected case compares against a design | `references/figma_validation.md` when no selected case is visual |
| release decision, "ship or not", waiver, run report | Release decision: apply the release gate (section 3, step 4) | `references/regression_testing.md` (Release decision, Run report) | test and bug templates |
| a defect, "X sometimes fails" | Bug report (section 3b) | `references/bug_report_templates.md` | `references/test_case_templates.md` |
| Figma, design, pixel comparison | Visual checklist and discrepancies | `references/figma_validation.md` | `references/regression_testing.md` |

- Plan plus cases in one request: write the plan first and pass its step 3 gate, then read `references/test_case_templates.md` and write the cases, each citing its K risk.
- Ask only when two rows fit and the choice changes the work (a bug report versus cases for the same symptom). Otherwise take the row and say which one you took.

## 2. Output convention

Every deliverable uses these IDs and fields, so traceability is checkable:

- Requirements `R1, R2...` (or the requester's IDs); risks `K1, K2...`; cases `TC-<AREA>-NNN`. Each case names its requirement and risk; each risk names its covering cases and its residual-risk owner.
- A fact the requester did not supply is written `Unknown` where it belongs and again under "Open Questions" at the end, and the reply asks the user for each one.

NEVER fill a gap with a plausible value (Chrome, "Always", build latest): a guessed environment sends the developer to the wrong reproduction, and a guessed "Always" hides that the bug is unconfirmed.

## 3. Test plan branch

1. **Scope by evidence:** exclude an area only when evidence you have (the diff, a dependency map, the owner's statement) shows the change cannot reach it, and cite that evidence as the reason. Missing information is not evidence of no impact: write the area's impact `Unknown`, name an owner and the question under Open Questions, and keep a minimal smoke check for it (or list that check as `Blocked` with the owner) until the answer arrives.
2. **Risks:** for each change, ask what money, data, permission, time or external boundary it touches; one risk per answer, written as `K1: <failure mode> | impact | cases TC-.. | owner <name or Unknown>`. The owner is the authorized release-risk owner for that risk.
3. **Cases per risk.** Gate: every K line lists at least one TC ID before you go on; a risk you cannot cover is a listed gap with its owner.
4. **The release gate** (the plan's exit gates and every release decision use this one rule): every critical requirement has an executed, passing case and no P0 failure is open, and each blocked case has an owner. The only exception is a specific failure covered by a written waiver from that failure's authorized release-risk owner, recording who approved, the case and affected scope, the residual risk and mitigation, and an expiry or follow-up date (record fields in `references/regression_testing.md`). The waived case keeps its failing status and evidence.
5. **Fit:** if the cases exceed the environments or time available, cut by the precedence in section 5 and list each cut case as residual risk.

Write the plan in this shape, with `Unknown` wherever a fact is missing:

```markdown
## Requirements   R1: <requirement> ...
## Scope          In: <area> (change: <ticket>) | Out: <area> (evidence: <diff/map/owner>) | Unknown: <area> (owner, question, smoke check)
## Risks          K1: <failure mode> | impact | cases TC-.. | owner
## Environments   <env, build, data, accounts>
## Schedule       <window, testers, time per suite>
## Exit gates     <the release gate of step 4, and any waiver in force>
## Residual risk  <risk> | owner | accepted in writing: yes / no / Unknown
## Open Questions <each Unknown, with who can answer>
```

For a full plan document, read `references/test_plan_template.md` and add its sections (executive summary, test types and approach, entry criteria, the risk table with probability and mitigation, deliverables) around this shape.

## 3b. Bug report branch

1. Keep the first failure's evidence, observed rate and environment as found: it is the evidence, so never rerun until green and report the pass. A later reproduction elsewhere (a sandbox, staging) is recorded as its own environment, never merged into the original one.
2. Before reproducing, ask: could a rerun move money, change or expose data, or touch a security control? If so, rerun only with authorized disposable data (test accounts, sandbox cards) in an environment where that harm cannot reach real users. If either prerequisite is missing, do not reproduce: record reproduction as `Blocked` with the missing prerequisite and its owner, and keep the rate as observed (`1 occurrence, not reproduced`, or `Unknown`).
3. When a safe rerun is possible, rerun under the same conditions only to measure the rate (n/10). NEVER write "Always" for an intermittent bug: the rate drives triage and tells the fixer how many attempts prove a fix.
4. Before setting severity, ask what the failure costs (money, data, recovery) and whether it is the product or the environment. Severity follows impact; priority follows the rate grid in `references/bug_report_templates.md`, including its Unknown-rate row.
5. Draft from `references/bug_report_templates.md`: its tracking fields when the bug will be followed through a fix, its quick template only for a minor issue with a known rate and no data or security impact, its security template for a vulnerability (confidential; name the OWASP edition with any category), and run its pre-submit checklist before delivering.

## 4. Cases: write the oracle before the steps

For each requirement, write the observable pass/fail result first, then the steps that reach it. Partitions that are easy to miss in money flows: an amount that rounds at the currency's minor unit (0.005, and zero-decimal currencies such as JPY), a zero-amount order (100% coupon), and a partial refund that leaves exactly 0.00. Use these oracles where a weak one hides the bug:

| Behavior | Oracle that catches the bug | Weak oracle |
| :- | :- | :- |
| Retry or double submit (pay, send, create) | After two clicks or a retried request, exactly one order or charge exists in the order list or ledger | "Payment succeeds" (the toast shows either way) |
| State transition (one-use link, draft to published) | The allowed transition lands in the stated state, and the forbidden one is rejected with no side effect (a reused reset link is refused and the password is unchanged) | "Status updates" |
| Expiry or scheduling | A controlled clock at both sides of the boundary (29:59 accepted, 30:01 refused), with the timezone stated | "Link expires after 30 minutes" |
| Irreversible action (delete, refund, email) | Confirmation before; after it, the record and its dependents are in the stated state; run only on disposable data | "Item deleted" |
| Permission | The denied role sees no control or gets the stated error, and the action leaves no record | "Admin only" |
| Unknown account or input (enumeration) | Known and unknown inputs get the same message and status. Timing: state the sampling plan (for example 30 alternating requests per input) and the agreed tolerance (for example medians within 50 ms) | "Shows an error" |

The timing figures in that last row (30 alternating requests per input, medians within 50 ms) are examples and placeholders the team replaces. With no agreed sampling plan or tolerance, write `Unknown` and add an Open Question; never copy 30 or 50 ms into a case as the recommended plan.

Two decisions the table does not make for you:

- **Asynchronous side effects** (webhook, email, queue): state the observation window in the expected result ("ledger shows one charge 10 minutes after Pay"); checking at once passes cases that fail a minute later.
- **Evidence or tooling you cannot reach** (no ledger access, no timing tool, no agreed tolerance): mark that check `Blocked` with the missing prerequisite and its owner. NEVER pass or fail it on the UI alone or on a guessed threshold.

Worked example. Requirement: "a coupon applies once per account." Oracle: a second discounted redemption cannot occur; after the attempt, account A's order records hold exactly one order with the SAVE10 discount. Case: precondition, account A has already redeemed SAVE10 once (seeded, not created by an earlier case); steps, apply SAVE10 and try to pay; expected, no second discounted order exists. The requirement does not say whether the code is refused with a message or checkout continues at full price, so write that behavior under Open Questions; assert a full-price charge only in a separate case for a specified flow in which the user confirms the undiscounted purchase.

For a complete worked case (a login case, a mobile navigation UI case), read `references/test_case_examples.md`. For the integration, security and performance case blocks, read the Integration, Security or Performance block of `references/test_case_templates.md` only when the case is that type; for a per-component visual case and its state checklist, read `references/figma_validation.md` section 5 only for a per-component visual case.

## 5. Prioritize cases and suites: the default precedence

1. **Failure impact:** P0 money, security or irreversible data; P1 blocked core journey; P2 workaround exists; P3 cosmetic.
2. **Then overlap with the change:** directly changed, then a dependency of the change or overlap `Unknown`, then untouched (shown untouched by evidence, never assumed).
3. **Then execution cost:** cheaper first within a tie.

Apply the steps in this order and state any departure the requester asks for, so two runs over the same input produce the same order. Bug priority follows `references/bug_report_templates.md` instead. How often each priority runs, the suite tiers and the run report template are in `references/regression_testing.md`.

## 6. Gotchas

- NEVER let one case depend on another's leftovers or share a mutable account with another tester: results then change with run order, selective reruns and concurrent edits. Seed its data in the preconditions and reset it in cleanup.
- NEVER take a sandbox payment result as proof about production. Provider sandboxes use special decline cards and send webhooks on their own schedule, or not at all; a passing sandbox decline does not prove that no charge or order is created when the real webhook arrives. Check the order record and ledger after the webhook window, and mark the production behavior `Unknown` if it was not tested.
- NEVER assume the clock or the timezone. Freeze time or state the timezone in the test data; otherwise expiry and "today" cases pass on one machine and fail at midnight UTC on another.
- Failed-case reruns, safe reproduction and the reproduction rate follow section 3b.
- NEVER judge a color or spacing by eye. Compare measured values or tokens under the matching frame version, viewport, theme and device-pixel ratio; near shades pass a casual look and the wrong DPR makes every size look wrong.
- NEVER treat a workaround (manual refund, support script) as a P0 waiver: the defect still reaches every user who does not get the workaround, and a waiver with no named owner leaves nobody accountable. Only the waiver defined by the release gate (section 3, step 4) lifts a P0 block.
- NEVER write a bare pass rate ("95% passing") as an exit gate: 95% can hide the one P0 failure. Use the release gate (section 3, step 4).

## 7. Optional scripts: files on disk

Use the scripts (bash and python3) only when the user wants a Markdown file written; otherwise draft in the reply. Each run writes one file and prints one JSON line on stdout; prompts and errors go to stderr.

```bash
bash <skill-dir>/scripts/create_bug_report.sh --title '[Checkout] Pay click sends no request' \
  --description 'Pay button stays enabled; no network request' \
  --step 'Add one item and open checkout' --step 'Click Pay' \
  --expected 'One order is created' --actual 'Nothing happens' \
  --build '2.4.0-rc2' --rate '3/10' --severity 'high' --priority 'P1' './bugs'
bash <skill-dir>/scripts/generate_test_cases.sh --id 'TC-CHK-002' --title 'Declined card keeps cart' \
  --priority 'P0' --type 'functional' --objective 'A declined card creates no order' \
  --requirement 'REQ-PAY-7' --risk 'A declined payment still creates an order' \
  --precondition 'Seeded account qa+decline@example.test with 1 item in cart' \
  --data 'The sandbox decline test card' \
  --step 'Pay with the decline card | Decline message; order list unchanged' \
  --cleanup 'Empty the cart of qa+decline@example.test' --time '10' './cases'
```

| Script | Required | Other flags |
| :- | :- | :- |
| `create_bug_report.sh` | `--title --description --expected --actual` | `--step` (repeat), `--build --os --browser --device --url --rate --severity --priority --type --console --impact --workaround --reporter --regression --test-case --figma --first-noticed --id` |
| `generate_test_cases.sh` (one case per run: a suite is one call per TC ID, each with a distinct `--id`) | `--id --title --priority --type --objective`, one or more `--step 'ACTION \| EXPECTED'`; `--type` is one of `functional`, `ui`, `integration`, `regression`, `performance`, `security` | `--requirement --risk`, `--precondition` and `--cleanup` (repeat), `--data --time --why --edge --related --notes --figma --visual` |

- Always pass at least one field flag. With none, the script waits for answers on stdin and an agent session hangs.
- Pass every value the source states, each in its flag, exactly as the source writes it: notes saying build 2.4.0-rc2 give `--build '2.4.0-rc2'`, never `'2.4.0-rc2 (staging)'`; put context such as the environment ("reproduced on staging") in `--description`, so every reproduction fact the source gives reaches the saved report. Omit only what the source does not state; the script then applies section 2 inside the file (`Unknown` in place, listed under its Open Questions).
- Single-quote every flag value and the output directory, even plain ones (`--priority 'P0'`, `--rate '2/10'`, `'./bugs'`).

Reading the result, in this order:

1. **A run log is supplied:**
   1. Do not run the script again. Report its exit code and JSON fields verbatim (`status`, `id`, `file`, or `error`/`missing`).
   2. List every flag in the logged command with its value, one per line, and check each against the source: for a bug `--title`, `--description` (environment context such as staging included), `--expected`, `--actual`, each `--step`, `--build`, `--rate`, `--severity`, `--priority`, and no flag the source does not support; for a case `--requirement`, `--risk`, each `--precondition` (seeded), `--data`, each `--cleanup`, each `--step` in `ACTION | EXPECTED` form, and `--priority` matching the section 5 impact rule.
   3. On exit 0, read the file and apply steps 2.1-2.3 and 2.5 below; step 2.4's edits wait for the user's authorization (see the fourth sub-step).
   4. For any other exit, read its step below, but as a reviewer: present the corrected command, or the directory remedy, without executing it. Step 2.4's edits and any run wait for the user's authorization: run or edit nothing unless the user authorizes it.
   5. In every supplied-log reply, end with one line on reading results: exit 0 the `file` path in the JSON line, exit 2 the `missing` flags or bad value, exit 1 the file exists (ask before `--overwrite`), exit 3 an I/O failure (fix the directory or pick a writable one).
2. **Exit 0:** take the path from the JSON line's `file`, then:
   1. read that file;
   2. quote each supplied field's actual value back (`Requirement: REQ-PAY-7`, `Build: 2.4.0-rc2`), never a summary such as "every field is set";
   3. confirm every gap reads `Unknown` and is under its Open Questions;
   4. run section 8 against the file and edit it to finish what the flags cannot express;
   5. ask the user for each Open Question.
3. **Exit 2:** the JSON lists the `missing` flags or names the bad value; fix the command and rerun it (only for a run you started in this task).
4. **Exit 1:** the file already exists; ask before rerunning with `--overwrite`.
5. **Exit 3:** the output directory is missing, is not a directory, or the file cannot be created or written (permission, disk). Report the JSON `error`; for a run you started in this task, create a missing directory and rerun, otherwise ask for a writable destination. NEVER answer exit 3 with `--overwrite`: it does not fix permissions and can truncate the file.

## 8. Check before delivering

- Every critical requirement maps to at least one case; uncovered requirements and blocked cases are listed.
- Every step's expected result is observable; none says "works as expected".
- Every case seeds and cleans its own data.
- Every unknown fact is `Unknown` and appears under "Open Questions", in the saved file as well as the reply.
- The release decision applies the release gate (section 3, step 4), naming any waiver and its owner.
- A plan passes the checklist in `references/test_plan_template.md`; a bug report passes the pre-submit checklist in `references/bug_report_templates.md`.
