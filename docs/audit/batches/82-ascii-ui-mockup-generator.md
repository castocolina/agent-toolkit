# Batch 82

## ascii-ui-mockup-generator (agent)

### ascii-ui-mockup-generator#D8-1
- severity: medium
- dimension: D8
- location: agents/ascii-ui-mockup-generator.md:22
- fix: Resolve the ask branches for a subagent, which cannot wait for a reply mid-run. Add: 'Questions in steps 1 and 5 end the run; return them to the caller with the mockups. When re-invoked with a pick or answers, resume at step 6 or redraw.' Also say what 'if unanswered' in step 1 means: no answer in the delegating prompt.

### ascii-ui-mockup-generator#D1-1
- severity: low
- dimension: D1
- location: agents/ascii-ui-mockup-generator.md:23
- fix: Shorten step 6 to the handoff parts the model would not produce unprompted, such as mapping each ASCII label to a component name and using the user's stack. Drop the standard list of UI states and build priorities, which the model already includes in any handoff.

### ascii-ui-mockup-generator#D2-1
- severity: medium
- dimension: D2
- location: agents/ascii-ui-mockup-generator.md:18
- fix: Add a ranking rule. Example: 'Rank by how often the task is done and what an error costs; when the user gives neither, rank the task named first in the request highest and state that assumption above mockup 1.' This gives step 3's 'dominant task' a repeatable input.

### ascii-ui-mockup-generator#D3-1
- severity: low
- dimension: D3
- location: agents/ascii-ui-mockup-generator.md:35
- fix: Replace this general UI advice with an ASCII-specific gotcha the model gets wrong. Example: 'NEVER put a label wider than its column inside a table row: the border on the right shifts and every later row looks misaligned in the fence. Truncate with ...> first.'
