# states

## Decisions

- Empty state has three jobs (NN/g, Designing Empty States): say why it is empty, say what belongs here, and give a direct path to the key task. A "no records" message replaced seconds later is "particularly harmful", so empty waits for a successful response.
- "Nothing exists yet" invites creation; "filters matched nothing" offers to clear the filters. They are different screens.
- Error (NN/g, Error-Message Guidelines; SC 3.3.1 A, 3.3.3 AA): place it next to its source, identify the field in text, state the correction when it is known, never rely on color or animation alone, keep what the user typed.
- Do not show a field error before the user leaves the field, unless it is a live rule such as password strength (NN/g: not too early).
- Severity picks the form: inline for a field, a banner for a section, a modal only for a severe case.
- A destructive action confirms or offers undo (NN/g heuristic 5, Error prevention).

## Gotchas

- `role="alert"` interrupts; use it for errors. Use `role="status"` for confirmations (SC 4.1.3 AA). A toast that disappears in seconds can be missed by assistive tech; keep an inline confirmation for important actions. How long it should stay is UNVERIFIED.

Fix pattern: the passing example in `SKILL.md`.
