# Text-only meme formats

Use these when the joke depends on typography or voice rather than an image. Preserve intentional line breaks, quote markers, indentation, and code formatting literally; do not normalize them into prose.

## Greentext

```text
>be me
>ship the fix
>tests were already green
```

Keep each `>` as a literal line prefix. Use a fenced text block when Markdown rendering might interpret the lines.

## Copypasta

Use repeated phrasing and escalation; preserve the rhythm and line breaks. Avoid adding identifying or sensitive details about real people.

## ASCII / formatting memes

Use a fenced block for spacing-sensitive ASCII. Verify monospaced alignment and avoid relying on runs of spaces outside a code fence.

For text-only requests, return the formatted text directly—no image URL or generation request.
