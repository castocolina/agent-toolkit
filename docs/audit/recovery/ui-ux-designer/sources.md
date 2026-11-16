# Sources: ui-ux-designer (agent)

Checked 2026-11-07. No `track` call was made.

## Origins found

1. softaworks/agent-toolkit, `agents/ui-ux-designer.md`. The file at fork point `3027f20f` has blob `942c45fd6eea0ab3fbde385d9fce874b8c1392e6`; `gh api` on the upstream default branch `main` returns the same blob, so upstream has not changed the file since the baseline and the only upstream commit touching it is `673fe769` (2026-01-18).
2. Madina Gbotoe, the author named in the file's credit comment (https://madinagbotoe.com/, CC BY 4.0, portfolio project `madinagbotoe/portfolio`, path `.claude/agents`). The repository returned 404 on 2026-11-07 (private or removed), so it cannot be a registry row.
3. The aesthetic sections (fonts, colours, motion, backgrounds, layout) follow the public "avoid generic AI aesthetics" frontend prompt style; no exact upstream was found, so no row is proposed (no distinctive phrase search was conclusive).

## Current registry row

`docs/audit/upstream-sources.json` holds a `local` row (no source). The credit comment names an upstream, so a source row is proposed:

```json
{"skill": "ui-ux-designer", "kind": "github-path", "source": "softaworks/agent-toolkit:agents/ui-ux-designer.md", "ref": "main", "credit": "Madina Gbotoe (https://madinagbotoe.com/), via softaworks/agent-toolkit", "artifact_kind": "agent"}
```

The existing `local` row (`last_reviewed` 2026-11-04) should be replaced by it (a skill has one row per source; keep `last_reviewed`/`status` fields as the registry's other rows carry them). Note `ours_updated` reads `agents/ui-ux-designer.md`, which has a local commit, so the row will not hit `no local commit for source material`.

## Proposed `unversioned` rows (official pages used for facts)

```json
{"skill": "ui-ux-designer", "kind": "unversioned", "source": "Claude Code docs, Create custom subagents: https://code.claude.com/docs/en/sub-agents", "ref": null, "credit": "Anthropic", "artifact_kind": "agent"}
{"skill": "ui-ux-designer", "kind": "unversioned", "source": "Nielsen Norman Group, Horizontal Attention Leans Left: https://www.nngroup.com/articles/horizontal-attention-leans-left/", "ref": null, "credit": "Nielsen Norman Group", "artifact_kind": "agent"}
{"skill": "ui-ux-designer", "kind": "unversioned", "source": "Nielsen Norman Group, F-Shaped Pattern of Reading on the Web: https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/", "ref": null, "credit": "Nielsen Norman Group", "artifact_kind": "agent"}
{"skill": "ui-ux-designer", "kind": "unversioned", "source": "Nielsen Norman Group, How Users Read on the Web: https://www.nngroup.com/articles/how-users-read-on-the-web/", "ref": null, "credit": "Nielsen Norman Group", "artifact_kind": "agent"}
{"skill": "ui-ux-designer", "kind": "unversioned", "source": "Nielsen Norman Group, Banner Blindness: Old and New Findings: https://www.nngroup.com/articles/banner-blindness-old-and-new-findings/", "ref": null, "credit": "Nielsen Norman Group", "artifact_kind": "agent"}
{"skill": "ui-ux-designer", "kind": "unversioned", "source": "Nielsen Norman Group, Why You Only Need to Test with 5 Users: https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/", "ref": null, "credit": "Nielsen Norman Group", "artifact_kind": "agent"}
{"skill": "ui-ux-designer", "kind": "unversioned", "source": "UXmatters, How Do Users Really Hold Mobile Devices? (Steven Hoober, 2013): https://www.uxmatters.com/mt/archives/2013/02/how-do-users-really-hold-mobile-devices.php", "ref": null, "credit": "Steven Hoober", "artifact_kind": "agent"}
{"skill": "ui-ux-designer", "kind": "unversioned", "source": "W3C, Understanding SC 1.4.10 Reflow: https://www.w3.org/WAI/WCAG22/Understanding/reflow.html", "ref": null, "credit": "W3C", "artifact_kind": "agent"}
{"skill": "ui-ux-designer", "kind": "unversioned", "source": "Creative Commons, Attribution 4.0 International: https://creativecommons.org/licenses/by/4.0/", "ref": null, "credit": "Creative Commons", "artifact_kind": "agent"}
```

StatCounter is a pointer in the restored text (live page), not a row. The Lindgaard paper (publisher 403) is not proposed as a row because its page was not read.

## Credit lines

The credit comment (author, link, CC BY 4.0, GitHub link) is intact in the current file. Nothing is missing there. The root `README.md` has no credit line for any agent; one is optional for this agent. Exact line if the controller adds it: `ui-ux-designer: created by Madina Gbotoe (https://madinagbotoe.com/), CC BY 4.0, via softaworks/agent-toolkit.` No credit is added by this analyst (root README is off limits).

## skill-updater style review (review only)

- Rows: only `local`. `upstreams` skips local rows; the proposed `github-path` row's upstream is identical to the baseline, so there is no upstream change to adopt. Verified by blob sha equality; no `track` call.
- Model-validity pass: the rules that counter model habits are the NEVER bullets (no invented citations, no correlational causation, no desktop heuristic on touch). Not run (no probe lane was used); keep all, they target habits that appear without the rule.
- Adopt / adapt / ignore for the restore brief:
  - adopt: s003 attention research and s005 mobile research, with the corrected figures in `facts.md`; s013 research-check list; s020 trend list as judgment-labelled items.
  - adapt: s021 feedback pair (verified left-half figure, no uplift claim); an effort cue per finding (from s015/s016) as an optional word in the "fix" field; a "what is working" clause in the verdict paragraph (from s016); autoplay-without-controls as a fail candidate under the skill's a11y (from s019).
  - ignore: s001 and s022 persona text, s004 laws (wrong formula, textbook), s018 list (over-mapped), s023 "always code" and "ROI" rules, the CSS blocks of s006-s009.
  - pending the user: s002, s006-s010, s012, s017 (aesthetic-direction purpose).
- Placement note: the plugin `agent-ui-ux-designer` bundles `skills/ui-ux-principles`, and the agent preloads it. The agent file is 70 lines, so restores fit in its own file (under 200 lines). The skill's SKILL.md says judgment never moves a verdict, so a research catalog belongs in the agent, not the skill.
