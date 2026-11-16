# Batch 79

## ui-ux-designer (agent)

### ui-ux-designer#D8-1
- severity: medium
- dimension: D8
- location: agents/ui-ux-designer.md:53
- fix: Define the priority levels so the branch resolves: High means an accessibility blocker or a primary-task break, Medium means a fail that slows the task or affects one state or theme, and Low means any other fail. Then state that step 4 sorts the list by these levels.

### ui-ux-designer#D8-1
- severity: medium
- dimension: D8
- location: agents/ui-ux-designer.md:54
- fix: Give insufficient evidence explicit precedence: when there are no proven failures but any applicable criterion remains unverified, end with the next observation or test. Reserve "No change recommended" for verified passes with any remaining na rows explicitly inapplicable.

### ui-ux-designer#D1-1
- severity: low
- dimension: D1
- location: agents/ui-ux-designer.md:33
- fix: Shorten the checklist to the gates that appear nowhere else (evidence first when the preferred option loses on task success; screenshots hide touch-target scale, hover, focus, error and loading). Drop the items that repeat step 1, step 4 and the first NEVER line.

### ui-ux-designer#D2-1
- severity: medium
- dimension: D2
- location: agents/ui-ux-designer.md:53
- fix: Replace the dense prose bullet with a short output skeleton: verdict paragraph, then a review table per screen whose evidence cells end in ` — priority: <level>`, then the summary line, then a ranked list of `finding | evidence or judgment | priority | fix`, then `Biggest win:` and `Sources:`.

### ui-ux-designer#D3-1
- severity: low
- dimension: D3
- location: agents/ui-ux-designer.md:35
- fix: Add a gotcha for user-flow inputs (a flow, onboarding or several screenshots in sequence), for example: a screenshot sequence hides back navigation, state that persists across steps, and what happens on abandon and resume, so mark these unverified and do not call the flow broken from screenshots alone.
