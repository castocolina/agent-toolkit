# Memes in Markdown blog posts

A toolbox for putting textual and image memes into Markdown-based blogs and docs (MkDocs, Jekyll, Hugo, Astro and similar). Read it when the user wants memes inside a post or docs page, asks for an admonition, tab or collapsible meme, or wants text and image memes mixed. The formats themselves are in `text-memes.md`; image URL details are in `image-memes.md`.

Text memes stay in your content as plain text, and image memes are only a URL, so a post needs no uploads. Put anything spacing-sensitive in a code fence, which keeps spacing, arrows and alignment.

## Mixing text and image memes

Blend the two to pace a post. A rhythm that works:

1. Text sets up the context.
2. An image meme lands the punchline.
3. Another text format resolves it.

````markdown
### The Day I Realized Markdown Is Too Powerful

```text
>be me
>ship blog revamp
>marketing wants "fun"
>accidentally create meme culture
```

![Drake rejecting "make it fun", approving "make it accessible"](https://api.memegen.link/images/drake/make_it_fun/make_it_accessible.png)

**Status:** fun achieved
**Risk:** puns leaked to production
**Next Steps:** embrace chaos
````

Placement:

- Good sequences: greentext, then an image, then corporate satire; Tumblr chain, then ASCII art, then an image; chat log, then an image, then poetry.
- Avoid five images in a row (visual fatigue), three long copypastas back to back (reader exhaustion), and an image with no context (confusing).
- Template IDs in the examples are live ones. Look up any other in `https://api.memegen.link/templates/` rather than guessing (see `image-memes.md`).

## Alt text and search

Text memes are indexed as text and read well by screen readers. For image memes, write alt text that describes the picture and the joke, with the good and bad examples in `image-memes.md` (Alt text and search). The generated image URL carries no useful filename, so the alt text and an optional caption below the image carry the meaning.

## Platform tricks

Check each against the platform's own docs; syntax differs between platforms that look alike. Sources, checked 2026-11-07: Material for MkDocs [admonitions](https://squidfunk.github.io/mkdocs-material/reference/admonitions/) and [content tabs](https://squidfunk.github.io/mkdocs-material/reference/content-tabs/); Docusaurus [admonitions](https://docusaurus.io/docs/markdown-features/admonitions) and [tabs](https://docusaurus.io/docs/markdown-features/tabs); MDN Web Docs [`<details>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/details); Python-Markdown [md_in_html](https://python-markdown.github.io/extensions/md_in_html/).

### Custom CSS for greentext (MkDocs, Hugo)

Style a wrapper and keep the greentext in a fence inside it (without the fence the `>` lines become a blockquote):

```css
.greentext {
  color: #789922;
  font-family: 'Courier New', monospace;
  background-color: #f0f0f0;
  padding: 1rem;
  border-left: 4px solid #789922;
}
```

````html
<div class="greentext" markdown="1">

```text
>be you
>styling markdown like a pro
>mfw it actually looks good
```

</div>
````

The blank lines let a renderer treat the contents as Markdown. MkDocs (Python-Markdown) also needs the `md_in_html` extension and the `markdown="1"` attribute. Other renderers differ, so check yours.

### Admonitions

Official-looking mock alerts. The syntax depends on the platform.

Material for MkDocs uses `!!!` with an indented body. It needs the `admonition`, `pymdownx.details` and `pymdownx.superfences` extensions in `mkdocs.yml`:

```markdown
!!! warning "System Alert"
    Your snacks have been revoked pending performance review.

!!! danger "Critical Error"
    `feelings.exe` has stopped responding.
    Would you like to send an error report? [Yes] [Yes]
```

Docusaurus does not use `!!!`. It uses `:::` fences with the keywords `note`, `tip`, `info`, `warning` and `danger`, and an optional title in brackets:

```markdown
:::warning[System Alert]
Your snacks have been revoked pending performance review.
:::

:::danger[Critical Error]
`feelings.exe` has stopped responding.
:::
```

### Collapsible sections

For long copypasta and Tumblr chains, use a `<details>` block. Leave a blank line after `<summary>` so the Markdown inside is parsed (renderer behavior, so check yours):

```markdown
<details>
<summary>Click to expand the legendary copypasta</summary>

(the full copypasta goes here, in a fence if spacing matters)

</details>
```

### Tabs

Show variations side by side. Material for MkDocs uses `===` (extensions `pymdownx.tabbed` with `alternate_style: true`, and `pymdownx.superfences`):

````markdown
=== "Greentext"

    ```text
    >be me
    >tabs are cool
    ```

=== "Corporate"

    **Notice:** Tabs have been deemed acceptable for meme deployment.

=== "Image"

    ![Drake rejecting regular text, approving tabs](https://api.memegen.link/images/drake/regular_text/tabs.png)
````

Docusaurus has no `===` syntax. It uses MDX `Tabs` and `TabItem` components, imported from `@theme/Tabs` and `@theme/TabItem` in an `.mdx` file:

````mdx
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<Tabs>
  <TabItem value="greentext" label="Greentext" default>

```text
>be me
>tabs are cool
```

  </TabItem>
  <TabItem value="corporate" label="Corporate">

**Notice:** Tabs have been deemed acceptable for meme deployment.

  </TabItem>
</Tabs>
````

## Complete post example

A full post that mixes formats. Every image URL was checked with `curl -sI` on 2026-11-07 and returned HTTP 200. The success image appears only after the fix is confirmed, which is the same rule as in SKILL.md.

`````markdown
---
title: "The Deployment Chronicles"
date: 2025-01-11
tags: [devops, humor, deployments]
---

# The Deployment Chronicles

## Pre-Deployment Anxiety

```text
>be me
>friday afternoon
>manager: "quick deploy?"
>mfw "quick" and "deploy" in same sentence
```

**Narrator:** *It was not quick.*

---

## The Planning Phase

### Decision Matrix

![Drake rejecting "test thoroughly", approving "deploy on friday"](https://api.memegen.link/images/drake/test_thoroughly/deploy_on_friday.png)

**Status:** We chose poorly.

---

## During Deployment

```text
[15:42] devops_bot: deployment started
[15:43] engineer1: looks good
[15:44] engineer2: why is prod slow
[15:45] system: ERROR: connection timeout
[15:46] engineer1: this is fine
[15:47] system: CRITICAL: database locked
[15:48] engineer1: THIS IS NOT FINE
```

![This is Fine dog: production is down](https://api.memegen.link/images/fine/production_is_down/this_is_fine.png)

---

## Post-Mortem

### Incident Report #2847

**Issued to:** Engineering Team
**Date:** 2025-01-11 18:30 UTC
**Reason:** Premature optimization of deployment strategy

#### Required Actions

- [ ] Never deploy on Friday again
- [ ] Actually read the deployment checklist
- [ ] Stop trusting "it works on my machine"

**Consequences:**

1. Mandatory attendance at "Why Friday Deploys Are Bad" training
2. Team pizza party (cancelled due to incident)
3. Existential dread

---

*This incident report has been automatically generated by the Department of Preventable Disasters.*

---

## Lessons Learned

**me:** let's deploy carefully next time
*also me next Friday:* what could go wrong

---

## Success Metrics

After fixing everything:

![Success Kid: deployed successfully, only took 4 hours](https://api.memegen.link/images/success/deployed_successfully/only_took_4_hours.png)

🎯 hitting targets (the target was "don't break prod permanently")
✨ manifesting ✨ (working deployments)
😅 lessons learned (until next time)

---

## ELI5: What is a deployment?

A deployment is when you tell the computer to use your new code.
Sometimes the computer listens.
Sometimes the computer decides chaos is more fun.
This is called "DevOps."

**Follow-up:** Why do deployments fail?

Because the computer has feelings and Friday afternoon hurts those feelings.

---

## Conclusion

roses are red<br>
deploys cause pain<br>
test in production<br>
again and again

---

*Want more deployment horror stories? Subscribe to our RSS feed of suffering.*
`````
