# Text-only meme formats

Use these when the joke depends on typography or voice rather than an image. Preserve intentional line breaks, quote markers, indentation, and code formatting literally; do not normalize them into prose.

The 15 named formats with samples and tips, and the Markdown techniques behind them, are in `text-memes.md`. Blog-platform tricks, mixing with image memes and a full example post are in `blog-posts.md`.

## Greentext

```text
>be me
>ship the fix
>tests were already green
```

Always put greentext in a fenced ```text block. Outside a fence, Markdown turns the `>` lines into a blockquote and the prefixes disappear.

## Copypasta

Use repeated phrasing and escalation; preserve the rhythm and line breaks. Avoid adding identifying or sensitive details about real people.

## ASCII / formatting memes

Use a fenced block for spacing-sensitive ASCII. Verify monospaced alignment and avoid relying on runs of spaces outside a code fence.
