# Marp for VS Code

Official extension: https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode (id `marp-team.marp-vscode`, source https://github.com/marp-team/marp-vscode). Facts checked 2026-11-13 against the extension README and `package.json`.

The extension needs no command line. Where another reference of this skill writes `marp ...`, it means `npx --yes @marp-team/marp-cli`.

## Preview

Marp features turn on for a Markdown file when its frontmatter has `marp: true`; the preview then works like VS Code's built-in Markdown preview. Open it with Ctrl+Shift+V (Cmd+Shift+V on macOS), or side by side with Ctrl+K V (Cmd+K V). Shortcuts are VS Code's own Markdown preview keys (https://code.visualstudio.com/docs/languages/markdown).

## Export

Click the Marp icon in the editor toolbar and choose "Export slide deck..." (command `markdown.marp.export`; the Command Palette also lists it as "Export Slide Deck..."). Formats: HTML, PDF, PPTX, PNG, JPEG and TXT. PNG and JPEG export only the first slide, and TXT holds the speaker notes only. PDF, PPTX and image export need Chrome, Chromium, Edge or Firefox installed.

## Settings

| Setting | Use |
|---|---|
| `markdown.marp.themes` | Register custom theme CSS: remote URLs or paths relative to the workspace. The way to use a custom theme file in VS Code. |
| `markdown.marp.html` | Which HTML renders (`all` allows every element, so only for decks you trust; untrusted workspaces always ignore HTML). Replaces `markdown.marp.enableHtml`, deprecated since extension v2: never write the old name. |
| `markdown.marp.exportType` | Default export format. |
| `markdown.marp.browser`, `markdown.marp.browserPath` | Browser and custom binary for PDF, PPTX and image export. |

The settings go in the workspace's `.vscode/settings.json`, for example:

```json
{
  "markdown.marp.themes": ["themes/name.css"]
}
```
