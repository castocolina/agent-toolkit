# Sources: professional-communication

Checked 2026-11-07. Review only: no `track` call, no registry edit, no artifact edit.

## Origins found

1. **softaworks/agent-toolkit, `skills/professional-communication`** (origin of the whole skill). At the fork point `3027f20f` the skill's six files (`SKILL.md`, `README.md`, four `references/` files) are byte-identical to the baseline `dbff837f` (`git diff 3027f20f dbff837f -- skills/professional-communication` is empty). The upstream path's last commit is `ebb0419d` (2026-01-19, "fix: correct skill naming and cross-references"), so upstream has not changed since the fork point; `gh api` on `main` (HEAD `3027f20f`, 2026-03-05) lists the same three entries (`README.md`, `SKILL.md`, `references`). The upstream author is Leonardo Flores (@leonardocouy), per the git history and the fork notice in the root `README.md` line 5. No registry row names this skill today (the only softaworks row for the repo is the `repo` row with `skill: null`).
2. **The "No Hello" principle** (README.md Example 2, baseline SKILL.md section "The 'No Hello' Principle"): the name and idea come from https://nohello.net (the page is a one-line "no hello" statement with no named author). The skill adapts it; it does not copy text.
3. No other distinctive uncredited text: a web search on "Effective communication isn't about proving how much you know ... ensuring your message is received and understood" found only paraphrases of a common idea, no source to credit. The templates, retro formats and glossary are standard industry material; the retro format names are credited to the vendor pages in facts.md only where the restore prints them.

No credit line exists anywhere in the skill's files (`grep` for credit, based on, http, inspired, adapted in `README.md` and `SKILL.md` finds nothing). Skills of the same origin with a per-skill README credit (`gemini`, `database-schema-designer`) carry the line below.

## Missing credit line

Add to `skills/professional-communication/README.md`, a new `## Credits` section before the `## Version` section (never reword it later):

```text
## Credits

Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy. The "No Hello" principle is from [nohello.net](https://nohello.net).
```

## Proposed registry rows (docs/audit/upstream-sources.json)

Origin rows (`credit` follows the `database-schema-designer` precedent):

```json
{"skill": "professional-communication", "kind": "github-path", "source": "softaworks/agent-toolkit:skills/professional-communication", "ref": "main", "credit": "softaworks/agent-toolkit"}
{"skill": "professional-communication", "kind": "unversioned", "source": "No Hello: https://nohello.net", "ref": null, "credit": "nohello.net"}
```

Docs pages used for facts.md (each `unversioned`, as plan 14 Step 5 says; `upstreams` never reports these stale, so only a `skill-updater` run re-reads them):

```json
{"skill_not_applied": "professional-communication", "kind": "unversioned", "source": "Slack Help Center, Use threads to organize discussions: https://slack.com/help/articles/115000769927-Use-threads-to-organize-discussions-", "ref": null, "credit": "Slack"}  <- not applied: the restored text does not cite this page
{"skill_not_applied": "professional-communication", "kind": "unversioned", "source": "Slack Help Center, Notify a channel or workspace: https://slack.com/help/articles/202009646-Notify-a-channel-or-workspace", "ref": null, "credit": "Slack"}  <- not applied: the restored text does not cite this page
{"skill_not_applied": "professional-communication", "kind": "unversioned", "source": "Microsoft Learn, Introduction to Microsoft Teams for admins: https://learn.microsoft.com/en-us/microsoftteams/teams-overview", "ref": null, "credit": "Microsoft"}  <- not applied: the restored text does not cite this page
{"skill": "professional-communication", "kind": "unversioned", "source": "Atlassian Team Playbook, The 4 Ls Retrospective Technique: https://www.atlassian.com/team-playbook/plays/4-ls-retrospective-technique", "ref": null, "credit": "Atlassian"}
{"skill": "professional-communication", "kind": "unversioned", "source": "Atlassian Team Playbook, Sprint Retrospective: https://www.atlassian.com/team-playbook/plays/retrospective", "ref": null, "credit": "Atlassian"}
{"skill": "professional-communication", "kind": "unversioned", "source": "Atlassian, Start-Stop-Continue template: https://www.atlassian.com/software/confluence/templates/start-stop-continue", "ref": null, "credit": "Atlassian"}
{"skill": "professional-communication", "kind": "unversioned", "source": "Agile Retrospectives, 2nd edition (Derby, Larsen, Horowitz), O'Reilly listing: https://www.oreilly.com/library/view/agile-retrospectives-2nd/9798888650868/f_0010.xhtml", "ref": null, "credit": "Esther Derby and Diana Larsen"}
{"skill": "professional-communication", "kind": "unversioned", "source": "The Scrum Guide: https://scrumguides.org/scrum-guide.html", "ref": null, "credit": "Ken Schwaber and Jeff Sutherland"}
{"skill": "professional-communication", "kind": "github-path", "source": "nodejs/Release:schedule.json", "ref": "main", "credit": "Node.js Release Working Group"}
```

The last row (Node.js schedule) is only worth adding if the Step 6 fix for the "Node 20" example cites it in a pointer; if the example becomes the placeholder "Node [version]" with no citation, drop that row. The retro-format rows are needed only if the restored `references/meeting-structures.md` text prints the Atlassian wording or phase names; keep them when it does.

## skill-updater style review (review only)

Procedure followed from `skills/skill-updater/SKILL.md`, without the `track` call:

- Scope: `skills/professional-communication/` exists, not a synced skill.
- Rows: none for this name, and there is a credit-less upstream (item 1). Per step 2 the row is proposed above, no `track` call is made (`track` cannot create a source row).
- Upstream change: `gh api 'repos/softaworks/agent-toolkit/commits?path=skills/professional-communication'` returns only `ebb0419d` (2026-01-19) and `043b41cb` (2026-01-18), both before the fork point `3027f20f` (2026-03-05). Nothing newer to adopt or adapt.
- Adopt / adapt / ignore list for the restore brief:
  - adopt: none (no upstream change).
  - adapt: the baseline email templates, retro formats, 1:1 and standup structures, and Team Norms template restored from the baseline (which equals upstream) in the current guarded style: placeholders instead of invented dates, metrics or commitments; "Proposed:" labels; the urgent line routed to the documented escalation path.
  - ignore: the baseline glossary tables, analogies and generic best-practice bullets (see the drop-pending verdicts in the report), and every baseline example that invents a metric, an EOD deadline or an update promise (the contradicted sections).
- Model-validity pass: not run. It sends prompts to an LLM lane, which the analyst rails forbid for this task. Candidates for the controller to probe at the Step 7 gate: "do not invent urgency or deadlines" and "do not convert an implementation choice into an unmeasured benefit" (both counter a model habit; the evals `unknown-delay` and `stakeholder-delay` already exercise them).
- Companions in the plugin: `agents/communication-excellence-coach.md` and `commands/compose-email.md` have `kind: local` registry rows (no upstream) although both exist at `3027f20f` (`agents/communication-excellence-coach.md` blob `35a822b5` on upstream `main`); a credit and `github-path` row for them belongs to those artifacts' own turn, not here.
