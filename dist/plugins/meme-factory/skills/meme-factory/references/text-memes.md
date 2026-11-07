# Text meme catalog and techniques

Read this with `markdown-memes-guide.md` (greentext, copypasta and ASCII fence rules) when the user asks for a text-only meme or names one of the formats below. Each format lists what it needs, a sample to adapt (write a new joke, do not reuse the sample) and tips. For blog platforms, mixing text with image memes and a full post, read `blog-posts.md`.

## Building blocks

- **Code fence.** Use it for anything spacing-sensitive: greentext, ASCII art, chat logs. A fenced block keeps spaces, arrows and alignment exactly.
- **Blockquotes** carry multi-speaker chains (Tumblr threads, reply chains). Each extra `>` is one more reply level. Greentext still goes in a fence: a `>` line outside a fence becomes a blockquote and its prefix disappears.

  ```markdown
  > Person A: this is fine
  >> Person B: no it's not
  >>> Person C: *concern intensifies*
  ```

- **Hard line breaks.** Markdown joins consecutive lines into one paragraph. For poetry or timed lines end each line with two trailing spaces or `<br>`. Some themes strip trailing whitespace, so use `<br>` when the timing matters.
- **Horizontal rule.** `---` resets the pacing or marks an uncanny jump between bits. Put a blank line above it: text directly above `---` turns into a heading.
- **Emphasis as stage directions.** `**me:** i'm fine` then `*narrator:* he was not fine`. Bold labels name speakers, italics carry tone and emotional beats.

## Pick a container

| Format | Container |
|---|---|
| Greentext, ASCII art, chat logs | Fenced code block |
| Tumblr chains, Twitter-style replies | Blockquote |
| Reddit AITA/TIFU, fake documentation | Heading plus narrative |
| Corporate satire, fake legal notices | List |
| Emojicore, slang mutations | Plain paragraph |

Aim for three layers in every format: a setup that sets context, a pattern that builds expectation, then a punchline or twist that subverts or amplifies it. Write the payoff first, as SKILL.md step 4 says.

## The 15 formats

### 1. Greentext

Needs: a fenced block with literal `>` characters (fence rule in `markdown-memes-guide.md`).

Tips: keep sentence fragments, end on an anticlimax, remember the monospace look signals anon culture at once, and know it suits technical narratives.

### 2. Copypasta (dramatic walls of text)

Needs: a code fence so the formatting survives.

```text
I will have you know that I have reviewed over three hundred pull requests
this quarter and every single one of them contained the sentence "small
change". I have read the diffs. I know what small means. It does not mean
four thousand lines across eleven services, and I am not going to approve it
quietly on a Friday afternoon.
```

Tips: let it run long, that is the point. Overblown emotion is essential. Preserve the original formatting for authenticity. Collapse very long ones (see Collapsible sections in `blog-posts.md`). Keep it free of real names and sensitive details, and write an original text rather than reproducing a known copypasta that is abusive or profane.

### 3. Shitpost poetry and micro-poems

Needs: hard line breaks (two spaces or `<br>`).

```markdown
roses are red<br>
markdown is sly<br>
press two spaces<br>
to force a new line

violets are blue<br>
syntax highlighting is lit<br>
code fences preserve<br>
every last bit
```

Tips: lean into minimalism, use `<br>` if a theme strips trailing whitespace, break expectations with a sudden philosophical turn, and lowercase adds casual authenticity.

### 4. ASCII art and ASCII storytelling

Needs: a monospaced code fence.

````markdown
```text
(T_T)  \(^o^)/  (-_-)  (>_<)

    ___
   /   \
  | o o |  <- me reading documentation
   \___/
    |||
```
````

Tips: use `text` or no language so nothing is syntax-colored, test in more than one font, center with `<div align="center">` if the platform allows HTML, and keep it simple for broad compatibility. Never put information the reader needs only in ASCII art: screen readers read it character by character.

### 5. Surreal and absurdist text memes

Needs: Markdown plus strategic spacing.

```markdown
you awaken in the hallway of beans

the moon whispers: *not again*

---

**OPTION 1:** accept the beans
**OPTION 2:** become the beans

you choose Option 3

*there was no Option 3*
```

Tips: italics carry dream-logic emphasis, `---` makes uncanny jumps, play with lowercase and capitalization, and treat whitespace as tension.

### 6. Tumblrisms (multi-speaker chains)

Needs: nested blockquotes.

```markdown
> **Person A:** frogs are neat
>> **Person B:** frogs are powerful
>>> **Person C:** I aspire to frog
>>>> **Person D:** this post is making me lose my mind
>>>>> **Person A:** good
```

Tips: deeper `>` shows escalation, italics add emotional chaos, bold names keep speakers clear, and peak at five levels for readability.

### 7. Twitter / X-style micro-memes

Needs: a blockquote or plain Markdown.

```markdown
> me: i'm productive
> also me: alphabetizes rocks by emotional energy

---

**me at 3am:** what if bread could read

**bread:** *softly* "help"
```

Tips: keep it to 2-4 lines, use italics for stage directions, short exaggeration is the comedy, and an em dash works for "me: - also me:".

### 8. Reddit AITA / TIFU / narrative memes

Needs: Markdown headings plus paragraphs.

```markdown
### TIFU by enabling Markdown features too much

**Context:** I work in documentation.

**What Happened:** Today I formatted a shopping list with H3 headings,
bullet points, and citation links. My family staged an intervention.

**Update:** They've hidden the Markdown guide. I'm formatting this from memory.

**AITA?**
```

Tips: the heading is the post title, a sincere tone with mild absurdity works best, use the usual bold labels, and the more mundane the subject the funnier.

### 9. Wojak-style dialogues (text only)

Needs: bold archetype names plus minimal dialogue.

```markdown
**Doomer:** nothing matters
**Zoomer:** drink water bro
**Wojak:** *internal screaming*
**Chad:** have you tried not caring
**Doomer:** ...wait that's actually helpful
**Chad:** i know
```

Tips: keep lines short, rely on archetypes for instant recognition, aim for half-honest and half-ironic, and it also works inside a code block.

### 10. Discord / chat log memes

Needs: a code fence with a timestamp format.

````markdown
```text
[12:41] user123: you up?
[12:42] system: error: feelings.exe not found
[12:42] user123: same
[12:43] bot: did you try turning your emotions off and on again?
[12:44] user123: yes
[12:44] system: critical error: emotions.dll missing since 2019
```
````

Tips: timestamps add realism, usernames amplify the joke, system messages carry the comedy, and keep the delivery deadpan.

### 11. Emojicore memes

Needs: good spacing, nothing else.

```markdown
🚶💨 leaving my responsibilities

😔👉👈 wondering if coffee counts as a personality

🎯 hitting the target (the target is rock bottom)

✨ manifesting ✨ (chaos)
```

Tips: use emoji as syntax rather than decoration, stack them vertically, pair them with understated text, and less is more.

### 12. Fake wiki / manual pages

Needs: Markdown headings plus bold labels.

```markdown
## Bread.exe

**Category:** Deprecated Carbohydrate
**Status:** Unstable
**Introduced:** ~8000 BCE
**Last Update:** Never

### Known Issues

- Becomes stale without manual intervention
- Incompatible with lactose-intolerant systems
- Memory leak when toasted incorrectly

### Workarounds

See: `butter.dll` documentation
```

Tips: keep the tone pseudo-academic, use definition-style formatting, technical jargon for mundane objects is the joke, and cross-reference other fake docs.

### 13. Slang-mutation text memes

Needs: Markdown paragraphs with stylized spelling.

```markdown
how 2 markdown:

1. make text smol
2. add sparklez ✨
3. u done it

**congrations** u did a format

no take backsies
```

Tips: lean into childlike spelling, use emoji to exaggerate tone, mix formal structure (lists) with informal language, and "congrations" beats "congratulations" every time.

### 14. ELI5 but wrong

Needs: a heading plus a confident, incorrect explanation.

```markdown
### ELI5: Why do volcanoes erupt?

Volcanoes are mountains that get too excited and sneeze the earth.
The rocks fly out because they want to be birds but forgot how.
This is called "geology."

**Follow-up:** Why is lava hot?

Because it's embarrassed about the whole situation.
```

Tips: confidence plus incorrectness is the humor, keep the explanation plausible-sounding, use the real ELI5 structure, and it works for tech concepts too.

### 15. Corporate / legalese satire

Needs: lists plus bold labels.

```markdown
## Notice of Emotional Noncompliance

**Issued to:** You
**Date:** Whenever
**Reason:** Your vibe is irregular

### Required Actions

- [ ] Submit Form 42-B "Vibe Correction Protocol" within 5 business days
- [ ] Attend mandatory "Feeling Feelings Appropriately" training
- [ ] Provide written documentation of three (3) genuine smiles

**Failure to comply will result in:**

1. Passive-aggressive Slack messages
2. A pizza party (no pizza will be provided)
3. Being asked to "circle back" indefinitely

---

*This notice has been automatically generated by the Department of Vibes.*
```

Tips: use an official tone for trivial things, short bullets increase the contrast, checkboxes make good action items, and footer disclaimers are the best part.
