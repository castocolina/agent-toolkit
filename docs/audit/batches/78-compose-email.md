# Batch 78

## compose-email (command)

### compose-email#D8-1
- severity: medium
- dimension: D8
- location: commands/compose-email.md:18
- fix: In step 5, say how to output several drafts. For example: 'For multiple drafts, number them (Draft 1/2), give each its own **Subject:** line and body, and add one line on the order to send them.' Step 5 currently describes only a single draft, so this branch has no defined output.

### compose-email#D1-1
- severity: low
- dimension: D1
- location: commands/compose-email.md:25
- fix: Shorten this to one line: 'Body order: decision/impact, minimum context, ask+owner+deadline (or "No response needed")'. The model already knows BLUF and What-Why-How, so spend the saved lines on audience-specific failure cases.

### compose-email#D2-1
- severity: medium
- dimension: D2
- location: commands/compose-email.md:19
- fix: Split this into separate strategies. Request/approval: put the ask and the options in the first sentence. Status: give the delta since the last update, then the risk. FYI: say no action is needed. Each purpose then gets its own procedure, as Escalation and Follow-up already do.

### compose-email#D3-1
- severity: low
- dimension: D3
- location: commands/compose-email.md:33
- fix: Swap this generic etiquette item for a hard-won one. For example: 'NEVER reply-all summarise a thread that includes external parties without checking for internal-only details quoted lower in the thread: clients include the quoted history.'
