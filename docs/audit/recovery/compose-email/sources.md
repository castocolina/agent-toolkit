# Sources: compose-email (command)

Checked 2026-11-13. Review only: no `track` call, no registry or README edit made by this analyst.

## Origins found

1. softaworks/agent-toolkit, `commands/compose-email.md` (author Leonardo Flores, @leonardocouy). Verified: `git diff 3027f20f dbff837f -- commands/compose-email.md` is empty, so the baseline text is the softaworks original byte for byte, and the repo's only commit for that path is `673fe769` (2026-01-18, "add 6 agents and 4 commands from claude-plugins"). `gh api repos/softaworks/agent-toolkit/contents/commands/compose-email.md` still resolves (blob 6841c962, 3764 bytes), so a `github-path` row is checkable.
2. Possible earlier origin, unverified: the softaworks commit message says the commands came "from claude-plugins", and the baseline Example Usage names `/soft-skills:draft-email`. A search finds a `draft-email` skill in the `soft-skills` plugin of melodic-software/claude-code-plugins (MIT, per `gh api repos/melodic-software/claude-code-plugins/license`) with the same What-Why-How wording and anti-pattern list (listing at agent-skills.md and aimcp.info). `plugins/soft-skills` is not in that repo's current tree and has no commit history under that path, and I could not read its SKILL.md, so the link rests on listings and the old command name. No registry row and no credit line are proposed for it; the controller may add one if the user wants it recorded.

## Registry rows to add (docs/audit/upstream-sources.json)

The existing `compose-email` row is `kind: local`, which says "no upstream"; origin 1 makes it wrong. Replace it with the rows below (same pattern as the `viral-tweet`, `codex-plan` and `explain-changes-mental-model` rows).

```json
{
  "skill": "compose-email",
  "kind": "github-path",
  "source": "softaworks/agent-toolkit:commands/compose-email.md",
  "ref": "main",
  "credit": "Leonardo Flores (@leonardocouy), via softaworks/agent-toolkit",
  "artifact_kind": "command"
}
```

```json
{
  "skill": "compose-email",
  "kind": "unversioned",
  "source": "Claude Code, Extend Claude with skills (command frontmatter and $ARGUMENTS): https://code.claude.com/docs/en/slash-commands",
  "ref": null,
  "credit": "Anthropic",
  "artifact_kind": "command"
}
```

```json
{
  "skill": "compose-email",
  "kind": "unversioned",
  "source": "Claude Code, Tools reference: https://code.claude.com/docs/en/tools-reference",
  "ref": null,
  "credit": "Anthropic",
  "artifact_kind": "command"
}
```

```json
{
  "skill": "compose-email",
  "kind": "unversioned",
  "source": "Claude Code, Plugins reference (plugin name namespacing, commands layout): https://code.claude.com/docs/en/plugins-reference",
  "ref": null,
  "credit": "Anthropic",
  "artifact_kind": "command"
}
```

## Missing credit line

The root README "Command credits" paragraph has no compose-email entry. Add this sentence at the end of that paragraph, in the existing style (a command has no README, so the credit goes in the root README):

`compose-email is adapted from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit/blob/main/commands/compose-email.md) by Leonardo Flores (@leonardocouy), via softaworks/agent-toolkit.`

## skill-updater style review (review only)

- Rows: only the `local` row exists, so per step 2 the review goes to step 6 and a source-less call; with the new `github-path` row the controller would run `upstreams` and then `track` (the controller's call, not made here).
- Upstream change since the baseline: none. The softaworks file has a single commit (`673fe769`), identical to the baseline text, so there is nothing to adopt, adapt or ignore from upstream.
- Model-validity pass: not run. It needs the tool-less probe lane (`pi-cmd runner`), and the analyst rails forbid dispatching an LLM lane. Candidate rules for the controller: "no throat-clearing opener" (restore row s004), the never-claim-sent rule, and the "NEVER add recipients or CC" rule. Keep all of them unless a probe shows the habit is absent.
- Items for the restore brief (adopt means port the baseline rule as the record rows say):
  - adopt (s004): per-part caps, WHAT in 1-2 sentences and WHY in 2-3 sentences, and "no throat-clearing" (for example "I hope this email finds you well..."), as one short line in the output step; keep the current rule that an escalation or request puts the ask first.
  - adopt (s005, subject): subject of 5-8 words, with an action tag such as "[Action Required]", "[FYI]" or "[Decision Needed]" and a deadline tag such as "[Due Friday]" when urgent; adapt: apply it only when the subject already names the action or deadline (current Step 5), and keep the three bad-subject examples ("Quick question", "Update", "FYI") from s010 as counterexamples.
  - adopt (s005, body): bullets for 3-5 points at most, bold the key fact, short paragraphs of 2-3 sentences; adapt: the current under-150-words default and "No response needed" rule for FYI stay as they are.
  - ignore (s005 tone/jargon table): the audience-to-jargon mapping is covered by `skills/professional-communication/references/jargon-simplification.md` and by Step 2's "audience only adjusts length and order".
  - ignore (s006, s009, s008): fixed "## Email Draft" heading, labelled WHAT/WHY/HOW sections plus subject rationale, and the `/soft-skills:draft-email` examples; recorded in record.md.
- Destination skill: none. The `command-compose-email` plugin bundles no skill, so restores go into `commands/compose-email.md` (47 lines now, far under the 200-line threshold). The sibling `professional-communication` skill is not bundled with this plugin, so nothing may point to it as a load path (a command's bundled skills are not auto-loaded).
