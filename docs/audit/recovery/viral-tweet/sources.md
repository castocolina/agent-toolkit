# viral-tweet: sources (checked 2026-11-07)

## Origins found

1. **softaworks/agent-toolkit, `commands/viral-tweet.md`.** Added upstream by Leonardo Flores (@leonardocouy) in commit 12a687a9 on 2026-01-20/21 ("feat: add viral-tweet command for X post optimization"). It is the only commit upstream touches that path with; it is also in our history before the fork point `3027f20f`, where the file is identical in structure to our baseline `dbff837f`. Our current file is a heavy rewrite (137 -> 58 lines) of that text. The registry holds only a `local` row for it, so the origin is missing there. The root `README.md` credits the fork as a whole (line 5, "Fork of softaworks/agent-toolkit by @leonardocouy") but has no credit line for this command.
2. **Algorithm claims in the baseline text** (Grok-based transformer, P(action) list, weighted sum): the idea matches X's published repositories, https://github.com/xai-org/x-algorithm (For You feed, "Final Score = Σ (weight_i × P(action_i))") and https://github.com/twitter/the-algorithm. The baseline text is not copied from either; no verbatim match was found. The current file makes no such claim (NEVER list), so these are references for the facts check, not content origins.
3. Hook, emotion and repost lever lists: no distinctive phrase matches a published source (generic growth-marketing folklore); no origin to credit.

## Proposed registry rows (docs/audit/upstream-sources.json)

Replace the existing `kind: local` row for `viral-tweet` with the first row (a `local` row beside a sourced row would contradict it). Add the others as new rows.

```json
{"skill": "viral-tweet", "kind": "github-path", "source": "softaworks/agent-toolkit:commands/viral-tweet.md", "ref": "main", "credit": "Leonardo Flores (@leonardocouy), via softaworks/agent-toolkit", "artifact_kind": "command"}
{"skill": "viral-tweet", "kind": "unversioned", "source": "X Developer Platform, Counting characters: https://docs.x.com/fundamentals/counting-characters", "ref": null, "credit": "X Corp.", "artifact_kind": "command"}
{"skill": "viral-tweet", "kind": "unversioned", "source": "twitter-text configuration v3: https://github.com/twitter/twitter-text/blob/master/config/v3.json", "ref": null, "credit": "X Corp.", "artifact_kind": "command"}
{"skill": "viral-tweet", "kind": "unversioned", "source": "x-algorithm README, For You feed ranking: https://github.com/xai-org/x-algorithm", "ref": null, "credit": "xAI / X Corp.", "artifact_kind": "command"}
```

The `credit` of the first row must appear verbatim in the credit line below (`check --strict` fails with `missing_credit` otherwise, for a command in the root `README.md`).

## Missing credit line

Yes. Add to the root `README.md`, next to the existing line 181 "Agent credits: ...":

`Command credits: viral-tweet is adapted from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit/blob/main/commands/viral-tweet.md) by Leonardo Flores (@leonardocouy), via softaworks/agent-toolkit.`

(The row's `credit` string, "Leonardo Flores (@leonardocouy), via softaworks/agent-toolkit", appears in it verbatim.) No existing credit line is changed.

## skill-updater style review (review only, no `track` call, `upstreams` not needed)

- Upstream state: `gh api commits?path=commands/viral-tweet.md&sha=main` returns the single commit 12a687a9 (2026-01-21). Upstream has not changed the file since the fork, so there is no upstream change to adopt, adapt or ignore. A first `upstreams` run on the new row will report `stale` only relative to our own newer commits; that is expected and the row should be recorded `current`.
- Adopt/adapt/ignore for the restore brief:
  - **adapt** s008 (Repost Psychology): add the test "would the reader look smart, informed or funny sharing this, without needing the author's context" to step 3a(c) or step 5's reposts check; leave out "tribal signaling" (NEVER bans in-group framing).
  - **adapt** s012 (Style Guidelines): add a short voice rule to step 3: write like a human, not a marketer; short sentences; lowercase fine if it fits the voice; no corporate-speak; match the author's voice; specific over generic; confident over hedging. Bound "weird" by step 1 (no invented drama).
  - **adapt** s013 (Example): optionally add a fact-faithful weak/strong pair that uses only the supplied launch fact (the old STRONG OUTPUT invented events and must not return). The weak output (emoji, "AMAZING", "link in bio", hashtags) is a valid anti-pattern example. This is not a record restore (no restore row), only an optional improvement.
  - **ignore** s002, s004, s005, s006, s007 (algorithm framing, high-arousal emotion list, hot takes, incompleteness, polarizing framing): they contradict the current NEVER list; every one has an intended-change row.
  - **ignore** s009, para:6c44e7cd: generic.
  - **s011** `purpose-change-pending`: best time framing and follow-up engagement plays stay out until the user answers.
- Model-validity pass: not run (review only). Candidates for a later run by plan 9's cycle: the NEVER rule against invented facts and the "no engagement bait" rule counter model habits; the empty-argument rule does too.

## Official pages used (each proposed as an `unversioned` row above)

- https://docs.x.com/fundamentals/counting-characters (280, URL 23, emoji/CJK 2, twitter-text)
- https://github.com/twitter/twitter-text/blob/master/config/v3.json (weights and 280)
- https://github.com/xai-org/x-algorithm (README: transformer, formula, 25 actions, weights location)

Read but not proposed as rows: https://github.com/twitter/the-algorithm (README), https://github.com/twitter/the-algorithm-ml/blob/main/projects/home/recap/README.md (2023 weights, dated). help.x.com/en/using-x/how-to-post returned HTTP 403.
