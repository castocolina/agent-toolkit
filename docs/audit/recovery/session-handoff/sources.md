# session-handoff: sources (checked 2026-11-15)

## Origin found

- Whole skill: `softaworks/agent-toolkit:skills/session-handoff` (MIT, default branch `main`). `git -C WT ls-tree 3027f20f skills/session-handoff` lists the same twelve files as `dbff837f`, and `git diff --stat 3027f20f dbff837f -- skills/session-handoff` is empty, so the baseline is the upstream text unchanged.
- Upstream history of the path (`gh api repos/softaworks/agent-toolkit/commits?path=skills/session-handoff&sha=main`): `ebb0419d` (2026-01-19, "fix: correct skill naming and cross-references") and `06825f04` (2026-01-18). Both are in this repo's history (`git log --follow` shows them), and upstream `main` is `3027f20f` (2026-03-05), the registered fork point. Contents test: `gh api --silent 'repos/softaworks/agent-toolkit/contents/skills/session-handoff?ref=main'` exits 0.
- No other origin found. A web search on the distinctive phrase ("Solves long-running agent context exhaustion ... zero ambiguity") returns only copies of the softaworks skill (tessl.io, playbooks.com, mirrors), no earlier source.

## Credit line: missing

Neither the baseline nor the current `skills/session-handoff/README.md` credits softaworks, and the registry has no `session-handoff` row. Add this line at the end of `skills/session-handoff/README.md`, the form 6 sibling skills use (`difficult-workplace-conversations`, `marp-slide`, `c4-architecture`, ...):

```text
Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy.
```

The row's `credit` text `softaworks/agent-toolkit` appears verbatim in that line, so `check --strict` `missing_credit` passes. A vendor-docs sentence is not needed in the README beyond that line; the registry carries the vendor rows.

## Proposed registry rows (docs/audit/upstream-sources.json)

```json
{
  "skill": "session-handoff",
  "kind": "github-path",
  "source": "softaworks/agent-toolkit:skills/session-handoff",
  "ref": "main",
  "credit": "softaworks/agent-toolkit"
}
```

```json
{
  "skill": "session-handoff",
  "kind": "unversioned",
  "source": "GitHub Docs, About authentication to GitHub (token prefixes): https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-authentication-to-github",
  "ref": null,
  "credit": "GitHub"
}
```

```json
{
  "skill": "session-handoff",
  "kind": "unversioned",
  "source": "Slack developer docs, Tokens: https://docs.slack.dev/authentication/tokens",
  "ref": null,
  "credit": "Slack"
}
```

```json
{
  "skill": "session-handoff",
  "kind": "unversioned",
  "source": "Python documentation, What's New In Python 3.10 (PEP 604 union types): https://docs.python.org/3/whatsnew/3.10.html",
  "ref": null,
  "credit": "Python Software Foundation"
}
```

```json
{
  "skill": "session-handoff",
  "kind": "unversioned",
  "source": "Git documentation, git-status: https://git-scm.com/docs/git-status",
  "ref": null,
  "credit": "Git project"
}
```

```json
{
  "skill": "session-handoff",
  "kind": "unversioned",
  "source": "Git documentation, git-merge-base (--is-ancestor): https://git-scm.com/docs/git-merge-base",
  "ref": null,
  "credit": "Git project"
}
```

```json
{
  "skill": "session-handoff",
  "kind": "unversioned",
  "source": "Git documentation, git-branch (--show-current): https://git-scm.com/docs/git-branch",
  "ref": null,
  "credit": "Git project"
}
```

OpenAI: no official page defining the API key format was found, so no OpenAI row is proposed (see facts.md).

## skill-updater review (review only, no `track` call)

- Step 2: no registry row exists for this artifact and no credit line names an upstream; the rows above are proposed and no `track` call is possible until they exist (`track` cannot create a source row).
- Steps 3-4 on the proposed row (read by `gh api`, since `upstreams` has no row to report): contents test exits 0; the path's newest upstream commit is `ebb0419d` (2026-01-19), already in our history, and upstream `main` has not moved since the fork point `3027f20f`. No upstream change to classify: nothing to adopt, adapt or ignore from softaworks. The first `track` after the row exists should record `current` with `--sha ebb0419d...` (the controller reads the full SHA from `gh`).
- Unversioned rows: read for the facts in facts.md; their outcome is recorded there. `upstreams` always reports `stale: false` for them, as the plan notes.
- Model-validity pass: no rule counters a model writing habit (an em-dash style ban or the like). The rules are task rules: never write secret values, write `Unknown` for unknown facts, validate until READY. No probe needed; none run.

### Items for the restore brief

| item | decision | reason |
| --- | --- | --- |
| Add the credit line above to `skills/session-handoff/README.md` | adopt (provenance) | the artifact is unchanged upstream text at the baseline and carries no credit |
| Add the seven registry rows above | adopt | origin and vendor docs behind the facts |
| Widen the secret patterns in `scripts/validate_handoff.py`: `github_pat_[A-Za-z0-9_]{20,}`, `gh[ousr]_[A-Za-z0-9_]{20,}`, drop the fixed 36 on `ghp_`, `sk-[A-Za-z0-9_-]{20,}`, add `xapp-`, `xwfp-`, `xoxe.xapp-`; adjust the SKILL.md scanner sentence to name prefix families; add a test that fails on the old patterns (the existing `test_secret_patterns_cover_postgresql_and_skip_bearer_prose` is the model) | adapt | facts.md rows "GitHub token prefixes", "Slack token prefixes", "OpenAI API key shape": the scanner's own output shows modern keys pass as clean, which defeats the BLOCKED verdict for the skill's most important rule |
| Optional: flag Bearer values shorter than 20 characters and passwords containing "/" | ignore | deliberate false-positive trade-off documented in the script; not a lost capability users relied on |
| Restore any removed README or checklist section | ignore | record.md: every section is present in new words, redistributed, or a drop with low value; only s059 and s062 are `drop-pending` and need the user's answer |
