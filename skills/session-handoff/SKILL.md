---
name: session-handoff
description: "Create, validate, and resume project-session handoff documents in .claude/handoffs/ using bundled Python scaffolding, secret checks, and staleness reports. Use when the user asks to pause coding, save session state, transfer work to another agent, load a handoff, or resume a handoff chain. Suggest a handoff at major milestones or near context limits. Not for ordinary status emails, ADRs, commit messages, or updates to persistent harness memory."
---

# Handoff

## Mode Selection

Determine which mode applies:

**Creating a handoff?** User wants to save current state, pause work, or context is getting full.
- Follow: CREATE Workflow below

**Resuming from a handoff?** User wants to continue previous work, load context, or mentions an existing handoff.
- Follow: RESUME Workflow below

**Proactive suggestion?** After substantial work (5+ file edits, complex debugging, major decisions), suggest:
> "We've made significant progress. Consider creating a handoff document to preserve this context for future sessions. Say 'create handoff' when ready."

## CREATE Workflow

### Step 1: Generate Scaffold

Run the smart scaffold script to create a pre-filled handoff document:

```bash
python "<resolved skill directory>/scripts/create_handoff.py" [task-slug]
```

Example: `python "<resolved skill directory>/scripts/create_handoff.py" implementing-user-auth`

**For continuation handoffs** (linking to previous work):
```bash
python "<resolved skill directory>/scripts/create_handoff.py" "auth-part-2" --continues-from 2024-01-15-auth.md
```

### Step 2: Complete the Handoff Document

Open the generated file. Before writing, ask what the next agent would waste time rediscovering. Record verified facts separately from proposals; prioritize state that cannot be reconstructed from the repository, exact reproduction commands and observed results, rejected hypotheses with reasons, and unresolved assumptions. Complete the three required sections (current state, important context, immediate next steps) plus task-relevant evidence; remove irrelevant optional scaffold sections or mark them not applicable. Scale depth to the remaining work.

1. **Current State Summary** - What's happening right now
2. **Important Context** - Critical info the next agent MUST know
3. **Immediate Next Steps** - Clear, actionable first steps
4. **Decisions Made** - Choices with rationale (not just outcomes)

Use the template structure in [references/handoff-template.md](references/handoff-template.md) for guidance.

### Step 3: Validate the Handoff

Run the validation script to check completeness and security:

```bash
python "<resolved skill directory>/scripts/validate_handoff.py" <handoff-file>
```

The validator checks:
- [ ] No `[TODO: ...]` placeholders remaining
- [ ] Required sections present and populated
- [ ] No potential secrets detected (API keys, passwords, tokens)
- [ ] Referenced files exist
- [ ] Quality score (0-100)

**Gotchas:** Secret scanning is heuristic, not proof; manually inspect the final handoff. Record environment variable names only, never secret values. Do not finalize with secrets, TODO placeholders, missing required sections, or a score below 70. The scaffold lists only ten modified-file rows and omits untracked files; inspect git status and include relevant untracked files yourself. `list_handoffs.py` marks Complete from TODO absence, not semantic validation.

### Step 4: Confirm Handoff

Report to user:
- Handoff file location
- Validation score and any warnings
- Summary of captured context
- First action item for next session

## RESUME Workflow

### Step 1: Find Available Handoffs

List handoffs in the current project:

```bash
python "<resolved skill directory>/scripts/list_handoffs.py"
```

This shows all handoffs with dates, titles, and completion status.

### Step 2: Check Staleness

Before loading, check how current the handoff is:

```bash
python "<resolved skill directory>/scripts/check_staleness.py" <handoff-file>
```

Staleness levels:
- **FRESH**: Safe to resume - minimal changes since handoff
- **SLIGHTLY_STALE**: Review changes, then resume
- **STALE**: Verify context carefully before resuming
- **VERY_STALE**: Consider creating a fresh handoff

The script checks:
- Time since handoff was created
- Git commits since handoff
- Files changed since handoff
- Branch divergence
- Missing referenced files

### Step 3: Load the Handoff

Read the relevant handoff document completely before taking any action.

If handoff is part of a chain, read the latest plus at most two predecessors. For older links, summarize the relevant lineage rather than loading an unbounded chain.

### Step 4: Verify Context

Follow the checklist in [references/resume-checklist.md](references/resume-checklist.md):

1. Verify project directory and git branch match
2. Check if blockers have been resolved
3. Validate assumptions still hold
4. Review modified files for conflicts
5. Check environment state

### Step 5: Begin Work

Start with "Immediate Next Steps" item #1 from the handoff document.

Reference these sections as you work:
- "Critical Files" for important locations
- "Key Patterns Discovered" for conventions to follow
- "Potential Gotchas" to avoid known issues

### Step 6: Update or Chain Handoffs

As you work:
- Mark completed items in "Pending Work"
- Add new discoveries to relevant sections
- For long sessions: create a new handoff with `--continues-from` to link the predecessor

## Storage Location

Handoffs are stored in: `.claude/handoffs/`

Naming convention: `YYYY-MM-DD-HHMMSS-[slug].md`

Example: `2024-01-15-143022-implementing-auth.md`

## Resources

### scripts/

| Script | Purpose |
|--------|---------|
| `create_handoff.py [slug] [--continues-from <file>]` | Generate new handoff with smart scaffolding |
| `list_handoffs.py [path]` | List available handoffs in a project |
| `validate_handoff.py <file>` | Check completeness, quality, and security |
| `check_staleness.py <file>` | Assess if handoff context is still current |

### references/

- [handoff-template.md](references/handoff-template.md) - Complete template structure with guidance
- [resume-checklist.md](references/resume-checklist.md) - Verification checklist for resuming agents
