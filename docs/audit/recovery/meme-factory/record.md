# Recovery record: meme-factory

Baseline dbff837f. Analyst triage for plan 14 batch 4 (2026-11-07). Facts were checked live against api.memegen.link and the vendor docs listed in facts.md. Three groups of rows drive the restore brief:

- Text-meme catalog (guide s080-s101, s113-s115, s117-s120, s124-s125): restore into `references/` as one rewritten text-meme reference (the 15 formats keep their requirement, sample and tips; blog-platform tricks verified in facts.md; the profane Navy Seals sample is not restored).
- Image-meme details (s008, s016, s028, s038, s045, s107): restore as small verified tables or lines, with template IDs taken from the live catalog.
- Examples (README, SKILL, examples.md): one deduplicated, verified set if the drop-pending rows are restored in the interim.

| item | fate | value | decision | reason class | reason |
| --- | --- | --- | --- | --- | --- |
| s003 When to Use | not-lost | low | none | text-present | README When it triggers and the SKILL description list the same request types (Slack, PR, docs, social, image URL) |
| s005 1. Popular Templates | not-lost | real | none | text-present | SKILL Templates table lists the popular set; changemind and distracted were 404 IDs, now cmm and db |
| s006 2. Text Formatting | not-lost | real | none | text-present | SKILL escape table is a superset (adds ~a ~b ~l ~g); bare hyphen as space is covered by the -- row |
| s007 3. Customization Options | not-lost | low | none | text-present | SKILL Query parameters and step 5 flags cover formats, size, font, background; layout bottom was never valid (see s039) |
| s008 4. Textual Memes | removed-to-fit | real | restore-references | users-ask-by-name | README promised 15+ text formats and the guide shrank to 3; README line returns with the restored catalog |
| s010 Code Review Context | removed-to-fit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-07, call delegated to the controller): repeats a SKILL.md rule or table row, or contradicts a current rule (pre-escaped captions, unconfirmed success, buzz fallback) |
| s011 Deployment Success | removed-to-fit | low | drop | generic-model-knowledge | success deploy URL; SKILL success row already limits it to confirmed wins |
| s013 Production Issues | removed-on-merit | low | drop | wrong | example writes memory_usage_at_99~ with a bare tilde; percent is ~p (memegen README, probed live) |
| s015 Natural Language | removed-on-merit | low | drop | stale | invented "meme-factory:" prefix syntax; triggering is by description and the name |
| s016 Quick Start | removed-to-fit | real | restore-references | users-ask-by-name | the /meme-factory template caption form and curl -I check are user-facing usage; put them in README usage with the redaction step first |
| s018 Validation Checklist | not-lost | low | none | text-present | SKILL steps 3-6 cover template fit, escaping, fetch check and wrap check |
| s019 Platform Dimensions | removed-on-merit | low | intended-change | fact-update | Slack/Discord 800x600 and GitHub default have no vendor source; 1200x630 kept in SKILL (Meta sharing docs, facts.md) |
| s020 Common Pitfalls | not-lost | real | none | text-present | SKILL Gotchas, step 4 length rule and the 404 note cover it; the missing-extension row was wrong (API redirects to .jpg) |
| s021 Additional Resources | not-lost | low | none | text-present | README Resources and File structure list the same links; examples.md link returns only if examples are restored |
| s022 In Code Review | removed-to-fit | low | drop | generic-model-knowledge | markdown image inside a review comment; SKILL step 6 already says present as Markdown image with alt text |
| s023 In Deployment Notification | removed-to-fit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-07, call delegated to the controller): repeats a SKILL.md rule or table row, or contradicts a current rule (pre-escaped captions, unconfirmed success, buzz fallback) |
| s024 In Bug Report | removed-to-fit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-07, call delegated to the controller): repeats a SKILL.md rule or table row, or contradicts a current rule (pre-escaped captions, unconfirmed success, buzz fallback) |
| s026 (preamble) | not-lost | low | none | text-present | rewritten description carries purpose and triggers; the 100+ templates claim is not kept (catalog has 209, pointer in facts.md) |
| s028 Triggers | removed-to-fit | real | restore-references | users-ask-by-name | documented /meme-factory and /meme-factory template top bottom forms are gone; restore as README usage plus a one-line SKILL note that args skip to step 5 after redaction |
| s029 Quick Reference | not-lost | low | none | text-present | URL shape, sizing and the templates link are in SKILL; the style=URL custom background row was wrong (s040) |
| s031 Text Formatting | not-lost | real | none | text-present | SKILL escape table is a superset; double quote is '' not "" (memegen README) |
| s033 Template Selection Guide | not-lost | real | none | text-present | SKILL Templates table Use for column maps context to template; the Why column is low value |
| s034 Validation | not-lost | low | none | text-present | same checklist as README s018, covered by SKILL steps 3-6 |
| s035 Platform Dimensions | removed-on-merit | low | intended-change | fact-update | duplicate of s019; unsourced sizes dropped, Open Graph 1200x630 kept |
| s036 Anti-Patterns | not-lost | real | none | text-present | SKILL Gotchas and steps 4-6 cover each row; missing-extension row was wrong (probed 302 to .jpg) |
| s037 Verification | not-lost | low | none | text-present | SKILL step 6 expects HTTP 200 and an image; HEAD request also works live |
| s038 Image Formats | removed-to-fit | real | restore-references | reusable-template | which extension to pick (png default, jpg smaller, webp or gif animate only with an animated background or animated text) is lost; memegen README table verified |
| s039 Layout Options | removed-on-merit | low | intended-change | fact-update | layout=bottom is not a valid value (200 but ignored, not in OpenAPI); SKILL states only default and top |
| s040 Custom Images | removed-on-merit | real | intended-change | fact-update | style=URL with custom returns 422; SKILL uses background=URL (memegen README, probed live) |
| s041 Successful Deploy | removed-to-fit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-07, call delegated to the controller): repeats a SKILL.md rule or table row, or contradicts a current rule (pre-escaped captions, unconfirmed success, buzz fallback) |
| s043 Dynamic Generation (Python) | redistributed skills/meme-factory/scripts/meme_generator.py | low | none | moved-to skills/meme-factory/scripts/meme_generator.py | status to template map became the suggest command with negation and uncertainty handling; old snippet also built unescaped captions |
| s045 Endpoints | removed-to-fit | real | restore-references | reusable-template | /templates/{id} (lines and styles per template), /fonts/ and the image path were a verified table; SKILL names only the list endpoints |
| s046 API Characteristics | removed-to-fit | real | restore-references | users-ask-by-name | user rejected the drop (2026-11-07, call delegated to the controller): answers whether the API needs a key |
| s047 Error Handling | not-lost | real | none | text-present | SKILL step 6 maps 404 and 422 to causes, a stronger version of the five-step list |
| s048 References | not-lost | low | none | text-present | README File structure and Resources replace the link table |
| s050 Summary | not-lost | low | none | text-present | golden rule (concise, match template) is SKILL step 3-4 |
| s051 Meme Generation Examples | removed-to-fit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-07, call delegated to the controller): repeats a SKILL.md rule or table row, or contradicts a current rule (pre-escaped captions, unconfirmed success, buzz fallback) |
| s053 Example 2: Drake Comparison Meme | removed-to-fit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-07, call delegated to the controller): repeats a SKILL.md rule or table row, or contradicts a current rule (pre-escaped captions, unconfirmed success, buzz fallback) |
| s054 Example 3: Success Meme | removed-to-fit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-07, call delegated to the controller): repeats a SKILL.md rule or table row, or contradicts a current rule (pre-escaped captions, unconfirmed success, buzz fallback) |
| s055 Python Script Example | redistributed skills/meme-factory/scripts/meme_generator.py | low | none | moved-to skills/meme-factory/scripts/meme_generator.py | module docstring shows the import and generate call; top_text and bottom_text keywords in the old snippet no longer exist (file row) |
| s057 Code Review Context | removed-to-fit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-07, call delegated to the controller): repeats a SKILL.md rule or table row, or contradicts a current rule (pre-escaped captions, unconfirmed success, buzz fallback) |
| s058 Deployment Context | removed-to-fit | low | drop | generic-model-knowledge | success deploy example, same as s011 |
| s059 Incident Response Context | removed-to-fit | low | drop | generic-model-knowledge | fine production-down example; SKILL fine row covers it |
| s063 Multiple Format Generation | removed-to-fit | low | drop | generic-model-knowledge | loop over png jpg webp; --extension flag covers it |
| s064 Slack Bot Integration | removed-to-fit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-07, call delegated to the controller): repeats a SKILL.md rule or table row, or contradicts a current rule (pre-escaped captions, unconfirmed success, buzz fallback) |
| s065 GitHub PR Comments | removed-to-fit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-07, call delegated to the controller): repeats a SKILL.md rule or table row, or contradicts a current rule (pre-escaped captions, unconfirmed success, buzz fallback) |
| s066 Discord Bot Integration | removed-to-fit | real | restore-references | procedure-depends | user rejected the drop (2026-11-07, call delegated to the controller): Slack and Discord want the plain image URL, not Markdown image syntax |
| s067 Generate Multiple Memes for a Topic | removed-to-fit | low | drop | generic-model-knowledge | loop over four generate calls |
| s068 Generate Memes for Documentation | removed-on-merit | low | drop | wrong | uses template ancient, which returns 404 (aag is the real ID) |
| s069 Check Template Validity | removed-on-merit | low | drop | superseded-by SKILL.md rule to look IDs up in the live catalog | user accepted the drop (2026-11-07, call delegated to the controller): repeats a SKILL.md rule or table row, or contradicts a current rule (pre-escaped captions, unconfirmed success, buzz fallback) |
| s071 Good Examples | not-lost | low | none | text-present | concise text and fitting template are SKILL step 3-4 |
| s072 Bad Examples | removed-to-fit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-07, call delegated to the controller): repeats a SKILL.md rule or table row, or contradicts a current rule (pre-escaped captions, unconfirmed success, buzz fallback) |
| s073 Testing Your Memes | removed-to-fit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-07, call delegated to the controller): repeats a SKILL.md rule or table row, or contradicts a current rule (pre-escaped captions, unconfirmed success, buzz fallback) |
| s074 Real-World Workflow Example | removed-to-fit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-07, call delegated to the controller): repeats a SKILL.md rule or table row, or contradicts a current rule (pre-escaped captions, unconfirmed success, buzz fallback) |
| s075 Summary | removed-to-fit | low | drop | generic-model-knowledge | recap bullets |
| s076 The Complete Practical Guide to Memes in Markdown Blog Posts | removed-to-fit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-07, call delegated to the controller): repeats a SKILL.md rule or table row, or contradicts a current rule (pre-escaped captions, unconfirmed success, buzz fallback) |
| s077 Table of Contents | removed-on-merit | low | drop | stale | anchors point at a guide structure that no longer exists; a restored reference builds its own |
| s078 Why Markdown for Memes? | removed-to-fit | low | drop | generic-model-knowledge | six generic advantages; the guide intro keeps the one that matters (code fences preserve spacing) |
| s080 Blockquotes | removed-to-fit | real | restore-references | users-ask-by-name | nested blockquote chains for Tumblr and reply threads are lost; the old claim of blockquote greentext stays out (current rule: fence greentext) |
| s081 Hard Line Breaks | removed-to-fit | real | restore-references | reusable-template | two trailing spaces or br for poetry timing, plus the theme-strips-whitespace caveat |
| s082 Horizontal Rules | removed-to-fit | real | restore-references | procedure-depends | user rejected the drop (2026-11-07, call delegated to the controller): a line directly above --- turns into a setext heading |
| s083 Emphasis | removed-to-fit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-07, call delegated to the controller): repeats a SKILL.md rule or table row, or contradicts a current rule (pre-escaped captions, unconfirmed success, buzz fallback) |
| s084 Choose a Meme Container | removed-to-fit | real | restore-references | reusable-template | format to block-type map (code block, blockquote, heading, list, paragraph) is a decision aid the catalog depends on |
| s085 Aim for Three Layers | removed-to-fit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-07, call delegated to the controller): repeats a SKILL.md rule or table row, or contradicts a current rule (pre-escaped captions, unconfirmed success, buzz fallback) |
| s086 Use Spacing as a Comedic Tool | removed-to-fit | low | drop | generic-model-knowledge | whitespace as timing is generic craft advice |
| s088 Copypasta (Dramatic Walls of Text) | removed-to-fit | real | restore-references | reusable-template | tips (long on purpose, overblown emotion, preserve format, collapse long ones) come back with a neutral original sample; the profane Navy Seals sample is not restored |
| s089 Shitpost Poetry & Micro-poems | removed-to-fit | real | restore-references | users-ask-by-name | poetry format with hard-break technique, sample and tips is missing from the guide |
| s090 ASCII Art & ASCII Storytelling | removed-to-fit | real | restore-references | users-ask-by-name | fence language text, font testing and centering tips and sample dropped from the one-paragraph version |
| s091 Surreal / Absurdist Text Memes | removed-to-fit | real | restore-references | users-ask-by-name | named format with sample and tips is absent |
| s092 Tumblrisms (Multi-Speaker Chains) | removed-to-fit | real | restore-references | users-ask-by-name | named format: nested blockquotes with bold speakers, peak at five levels |
| s093 Twitter / X-style Micro-memes | removed-to-fit | real | restore-references | users-ask-by-name | named format: 2-4 lines, me versus also me pattern |
| s094 Reddit AITA / TIFU / Narrative Memes | removed-to-fit | real | restore-references | users-ask-by-name | named format with heading and bold-label template |
| s095 Wojak-style Dialogues (Text-Only) | removed-to-fit | real | restore-references | users-ask-by-name | named format: bold archetype names and short lines |
| s096 Discord / Chat Log Memes | removed-to-fit | real | restore-references | users-ask-by-name | named format: fenced timestamped log with system messages |
| s097 Emojicore Memes | removed-to-fit | real | restore-references | users-ask-by-name | named format: emoji as syntax, vertical stacking |
| s098 Fake Wiki / Manual Pages | removed-to-fit | real | restore-references | users-ask-by-name | named format: heading plus bold-label infobox, known issues and workarounds |
| s099 Slang-Mutation Text Memes | removed-to-fit | real | restore-references | users-ask-by-name | named format: stylized spelling mixed with list structure |
| s100 ELI5 But Wrong | removed-to-fit | real | restore-references | users-ask-by-name | named format: confident wrong explanation with follow-up |
| s101 Corporate / Legalese Satire | removed-to-fit | real | restore-references | users-ask-by-name | named format: notice with checkbox actions, consequences, footer disclaimer |
| s105 Text Encoding Cheatsheet | not-lost | real | none | text-present | SKILL escape table is a superset; %0A still works (301 to ~n, probed) but ~n is the canonical form SKILL uses |
| s106 Common Options (Query String) | removed-on-merit | low | intended-change | fact-update | watermark=none is not an API parameter (302 strips it, absent from OpenAPI); font, size and background are in SKILL Query parameters |
| s107 Popular Templates | removed-to-fit | real | restore-references | users-ask-by-name | the use-case list lost working entries: gru (4 lines), spongebob, pigeon (3 lines) exist; two-buttons, surprised-pikachu and uno-draw-25 have no API ID and stay out |
| s108 Blank Sides & One-Sided Captions | not-lost | real | none | text-present | SKILL gotcha: _ for a blank line, empty segment returns 404; helper inserts _ |
| s109 Multiline Captions | not-lost | low | none | text-present | SKILL Hand-built URLs says line break in a caption is ~n; the %0A form is accepted but non-canonical |
| s111 Accessibility & SEO | not-lost | real | none | text-present | SKILL step 6 and --alt require alt text that describes picture and joke |
| s112 Quick Copy-Paste Recipes | removed-on-merit | low | intended-change | fact-update | recipes use 404 IDs (two-buttons, change-my-mind, surprised-pikachu) and watermark=none; working ones (drake, custom background) are in SKILL worked examples |
| s113 Mixing Text + Image Memes | removed-to-fit | real | restore-references | reusable-template | section intro for the text-image rhythm material below; fold into the restored mixing section |
| s114 Rhythm Pattern | removed-to-fit | real | restore-references | reusable-template | text setup, image punchline, text resolution with a worked snippet |
| s115 Strategic Placement | removed-to-fit | real | restore-references | reusable-template | good sequences and what to avoid (five images in a row, back-to-back copypastas) |
| s116 Complementary Pairs | removed-to-fit | low | drop | generic-model-knowledge | five subjective pairings, one with a nonexistent template |
| s117 Custom CSS for Greentext (MkDocs / Hugo) | removed-to-fit | real | restore-references | reusable-template | CSS class plus HTML wrapper with blank lines so Markdown renders inside; ready to paste |
| s118 Admonitions (MkDocs Material, Docusaurus) | removed-to-fit | real | restore-references | reusable-template | !!! syntax is MkDocs Material only (needs admonition extension); Docusaurus uses ::: (both verified, facts.md) |
| s119 Collapsible Sections | removed-to-fit | real | restore-references | reusable-template | details and summary for long copypasta and chains, blank line before Markdown content |
| s120 Tabs (Docusaurus, MkDocs) | removed-to-fit | real | restore-references | reusable-template | === syntax is MkDocs Material (pymdownx.tabbed); Docusaurus tabs are JSX Tabs and TabItem, so restore with that correction |
| s121 Performance | removed-to-fit | low | drop | generic-model-knowledge | webp 30-50 percent claim has no source; lazy loading and consistent width are generic web advice |
| s122 Accessibility | removed-to-fit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-07, call delegated to the controller): repeats a SKILL.md rule or table row, or contradicts a current rule (pre-escaped captions, unconfirmed success, buzz fallback) |
| s123 SEO | removed-to-fit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-07, call delegated to the controller): repeats a SKILL.md rule or table row, or contradicts a current rule (pre-escaped captions, unconfirmed success, buzz fallback) |
| s124 Complete Blog Example | removed-to-fit | real | restore-references | tested-example | only end-to-end sample mixing formats; rebuild image URLs on verified IDs (no watermark param, no two-buttons) and re-check HTTP 200 |
| s125 Complete Blog Example | removed-to-fit | real | restore-references | tested-example | second chunk of the same sample (chat log, incident report, success image, ELI5, poem); same URL fixes |
| s126 Summary | removed-to-fit | low | drop | generic-model-knowledge | recap list; the resource links return with the restored sections (memegen docs, MkDocs Material) |
| file:skills/meme-factory/scripts/meme_generator.py | removed-on-merit | real | intended-change | fact-update | CLI printed nothing (print calls were stubbed to pass); 7 dead template IDs removed; generate now takes positional captions (top_text and bottom_text keywords gone); heuristic made word-based, humor and reaction keyword hits dropped |
| s001 Meme Factory | not-lost | low | none | text-present | README opening line still says image memes via memegen.link plus text-only memes |
| s002 Purpose | not-lost | low | none | text-present | README intro states the same purpose; deploy-celebration wording was dropped on purpose (confirmed outcomes only) |
| s004 How It Works | not-lost | low | none | text-present | URL shape is in SKILL; stateless and free are in README; 100+ templates became a pointer (catalog has 209, facts.md); no API key needed verified live |
| s009 Basic Meme | not-lost | low | none | text-present | URL form and buzz example are in SKILL worked examples; the slash invocation is covered by the s028 restore row |
| s012 Comparing Options | not-lost | low | none | text-present | drake row in SKILL Templates; slash form covered by s028 |
| s014 With Custom Dimensions | not-lost | low | none | text-present | SKILL Query parameters give width and height padding and the 1200x630 Open Graph example |
| s017 Template Selection Guide | not-lost | real | none | text-present | SKILL Templates table; changemind and distracted rows were 404 IDs, now cmm and db |
| s025 Summary | not-lost | low | none | text-present | golden rule is SKILL steps 3-4; the celebrate-a-deploy line conflicts with the confirmed-wins gotcha |
| s027 Meme Factory | not-lost | low | none | text-present | one-line intro replaced by the rewritten description |
| s030 Basic Meme Structure | not-lost | low | none | text-present | SKILL Hand-built URLs gives the shape and two live-checked worked examples |
| s032 Popular Templates | not-lost | real | none | text-present | SKILL Templates table with line counts; example caption column dropped, changemind and distracted corrected |
| s042 Generating Memes in Response | not-lost | low | none | text-present | SKILL step 6 presents a Markdown image with descriptive alt text |
| s044 Using the Helper Script | not-lost | low | none | text-present | SKILL step 5 CLI line and the script docstring show the import and generate call |
| s049 Scripts | not-lost | low | none | text-present | README File structure lists scripts/meme_generator.py |
| s052 Example 1: Simple Meme | not-lost | low | none | text-present | buzz request to URL pair; the alt text Bugs Everywhere was weaker than the current alt rule |
| s056 CLI Example | not-lost | low | none | text-present | SKILL step 5 and the script docstring cover generate, list-templates and suggest; --markdown and size flags are in the usage line |
| s060 Documentation Context | not-lost | low | none | text-present | yodawg is in the helper list-templates output; the docs joke is a one-off caption |
| s061 Custom Dimensions for Social Media | not-lost | low | none | text-present | SKILL Query parameters names 1200x630 for an Open Graph card |
| s062 Custom Layout | not-lost | low | none | text-present | SKILL Query parameters documents layout=top |
| s070 Context-Based Template Selection | not-lost | low | none | text-present | the suggest subcommand implements context to template, with fry for unconfirmed outcomes |
| s079 Code Fences | not-lost | low | none | text-present | current guide says to fence spacing-sensitive text and greentext |
| s087 Greentext | removed-to-fit | real | restore-references | reusable-template | tips lost (keep fragments, anticlimax, monospace signals anon culture, good for technical narratives); fold into the restored catalog |
| s102 Image Memes via Pure URL | not-lost | low | none | text-present | intro sentence; the SKILL description and step 5 build image memes by URL |
| s103 Quick Start | not-lost | low | none | text-present | Drake sample is the same URL form as the SKILL worked examples |
| s104 URL Anatomy | not-lost | low | none | text-present | SKILL Hand-built URLs has the anatomy; format guidance returns under s038; watermark option was invalid (s106) |
| s110 Custom Backgrounds (Brand or Screenshot) | removed-to-fit | real | restore-references | reusable-template | lost: background must be publicly reachable (unreachable URL returns 415, probed) and the screenshot-as-background tip; SKILL step 6 lists only 404 and 422 |
| para:5078382b removed since dbff837f (skills/meme-factory/SKILL.md) | removed-to-fit | low | drop | generic-model-knowledge | interesting template deploy-test joke; the template stays in the helper catalog |
| para:2aa4e70e removed since dbff837f (skills/meme-factory/SKILL.md) | removed-to-fit | low | drop | generic-model-knowledge | yodawg docs joke URL; one-off caption |
| para:c7fb482a removed since dbff837f (skills/meme-factory/SKILL.md) | removed-on-merit | low | drop | wrong | memory_usage_at_99~ uses a bare tilde; percent is ~p |
| para:fb276465 removed since dbff837f (skills/meme-factory/SKILL.md) | removed-to-fit | low | drop | generic-model-knowledge | fry code-review example URL; fry row exists in SKILL |
| para:845c3516 removed since dbff837f (skills/meme-factory/SKILL.md) | not-lost | low | none | text-present | SKILL Query parameters says setting both width and height pads to the exact size |
| para:43e7a018 removed since dbff837f (skills/meme-factory/SKILL.md) | not-lost | low | none | text-present | SKILL font bullet points at https://api.memegen.link/fonts/ |
| para:a46efb43 removed since dbff837f (skills/meme-factory/SKILL.md) | removed-on-merit | low | drop | wrong | impact is not the universal default font; each template has its own (memegen README); font IDs come from /fonts/ |
| para:31992a51 removed since dbff837f (skills/meme-factory/references/markdown-memes-guide.md) | removed-to-fit | low | drop | generic-model-knowledge | one-line lead-in to the core techniques list; restored techniques get their own intro |
| para:12b38ef0 | removed-on-merit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-07, call delegated to the controller): restored text under 'Alt text and search' in references/blog-posts.md, removed in the accepted-drop follow-up (see the section rows marked drop) |
| para:76de55ce | removed-on-merit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-07, call delegated to the controller): restored text under 'Where the URL goes' in references/image-memes.md, removed in the accepted-drop follow-up (see the section rows marked drop) |
| para:2f23aa4b | removed-on-merit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-07, call delegated to the controller): restored text under 'Checks and diagnosis' in references/image-memes.md, removed in the accepted-drop follow-up (see the section rows marked drop) |
| para:4dbaaa20 | removed-on-merit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-07, call delegated to the controller): restored text under 'Pick a container' in references/text-memes.md, removed in the accepted-drop follow-up (see the section rows marked drop) |
| para:567365ba | removed-on-merit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-07, call delegated to the controller): restored text under 'Worked requests' in references/image-memes.md, removed in the accepted-drop follow-up (see the section rows marked drop) |
| para:7a8afca6 | removed-on-merit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-07, call delegated to the controller): restored text under 'Building blocks' in references/text-memes.md, removed in the accepted-drop follow-up (see the section rows marked drop) |
| para:44c418e7 | removed-on-merit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-07, call delegated to the controller): restored text under 'Worked requests' in references/image-memes.md, removed in the accepted-drop follow-up (see the section rows marked drop) |
| para:8c6ad7bb | removed-on-merit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-07, call delegated to the controller): restored text under 'Checks and diagnosis' in references/image-memes.md, removed in the accepted-drop follow-up (see the section rows marked drop) |
| para:7e0d9a33 | removed-on-merit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-07, call delegated to the controller): restored text under 'Alt text and search' in references/image-memes.md, removed in the accepted-drop follow-up (see the section rows marked drop) |
| para:f89004bd | removed-on-merit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-07, call delegated to the controller): restored text under 'Alt text and search' in references/image-memes.md, removed in the accepted-drop follow-up (see the section rows marked drop) |
| para:0bf2eeeb | removed-on-merit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-07, call delegated to the controller): restored text under 'Worked requests' in references/image-memes.md, removed in the accepted-drop follow-up (see the section rows marked drop) |
| para:3c596943 | removed-on-merit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-07, call delegated to the controller): restored text under 'Worked requests' in references/image-memes.md, removed in the accepted-drop follow-up (see the section rows marked drop) |
| para:00d019d8 | removed-on-merit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-07, call delegated to the controller): restored text under 'Where the URL goes' in references/image-memes.md, removed in the accepted-drop follow-up (see the section rows marked drop) |
| para:f970ca03 | removed-on-merit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-07, call delegated to the controller): restored text under 'Alt text and search' in references/image-memes.md, removed in the accepted-drop follow-up (see the section rows marked drop) |
| para:05519ed0 | removed-on-merit | low | drop | generic-model-knowledge | user accepted the drop (2026-11-07, call delegated to the controller): restored text under 'Alt text and search' in references/image-memes.md, removed in the accepted-drop follow-up (see the section rows marked drop) |
