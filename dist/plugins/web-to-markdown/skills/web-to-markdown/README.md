# web-to-markdown

Convert web pages to clean Markdown using local browser automation with Puppeteer and Readability.

## Purpose

This skill enables Claude Code to convert web pages (including JavaScript-rendered content) into clean, readable Markdown format by leveraging the `web2md` CLI tool. It's particularly useful for extracting article content, documentation, or any web content that needs to be processed, archived, or analyzed in Markdown format.

## When to Use

Use this skill when you need to:

- Extract article content from news sites, blogs, or documentation
- Convert JavaScript-heavy pages that simple HTTP fetching can't handle
- Archive web content in a readable, portable format
- Process web content for analysis or documentation
- Handle pages with login walls or human verification (using interactive mode)
- Batch convert multiple URLs to Markdown files

**Important:** This skill must be explicitly invoked by the user with phrases like:
- "use the skill web-to-markdown ..."
- "use a skill web-to-markdown ..."

This is a hard requirement to prevent accidental usage when simpler tools might suffice.

## How It Works

The skill uses the `web2md` CLI tool which:

1. **Launches a real browser** (Chrome/Chromium/Brave/Edge) via Puppeteer
2. **Renders the page** including all JavaScript and dynamic content
3. **Extracts main content** using Mozilla's Readability library
4. **Converts to Markdown** using Turndown with cleaned links
5. **Outputs** to stdout or saves to file(s) with optional YAML frontmatter

This approach handles modern single-page applications and JavaScript-rendered content that simple HTTP fetchers cannot process.

## Key Features

- **JavaScript Support**: Renders pages with Puppeteer, capturing dynamically loaded content
- **Smart Content Extraction**: Uses Readability to identify and extract main article content
- **Flexible Output**: Print to stdout, save to specific files, or auto-name files in a directory
- **Interactive Mode**: Handle login walls and human verification challenges
- **Batch Processing**: Convert multiple URLs in one operation
- **Wait Strategies**: Multiple options to ensure content is fully loaded before extraction
- **Browser Profiles**: Support for persistent user data directories (sessions, logins)
- **Clean Markdown**: Produces readable, well-formatted Markdown with optional metadata

## Prerequisites

The `web2md` CLI tool must be installed. The skill checks for it and, if it is missing, points to the install instructions. Follow the Installation section of https://github.com/leonardocouy/web2md (package `@leoflores/web2md`, Node.js >= 20; checked 2026-11-15) with the package manager you prefer.

## Usage Examples

The commands below are the plain `web2md` invocations. When the agent runs them through this skill it stages file output: it passes `--out` a unique temporary file reserved beside the requested file with `mktemp`, validates the result (SKILL.md step 5), and moves it onto the requested name only after any required overwrite authorization.

### Basic Conversion

Convert a single URL and save to a file:

```bash
use the skill web-to-markdown to convert https://example.com/article to article.md
```

This will run:
```bash
web2md 'https://example.com/article' --out ./article.md
```

### Auto-Named Output

Convert a URL and let the tool name the file based on page title:

```bash
use the skill web-to-markdown to convert https://example.com/article and save to ./output/
```

The CLI creates the parent directory itself (`src/cli.ts` of https://github.com/leonardocouy/web2md, checked 2026-11-15) and auto-names the file from the page title:
```bash
web2md 'https://example.com/article' --out ./output/
```

### Print to Console

Convert and display the Markdown (useful for quick inspection):

```bash
use the skill web-to-markdown to convert https://example.com/article and print the result
```

This will run:
```bash
web2md 'https://example.com/article' --print
```

### Interactive Mode (Login Walls)

Handle pages requiring login or human verification:

```bash
use the skill web-to-markdown to convert https://example.com/protected-article in interactive mode
```

This will run:
```bash
mkdir -p ./tmp/web2md-profile
web2md 'https://example.com/protected-article' --interactive --user-data-dir ./tmp/web2md-profile --out ./output/
```

The browser window will appear, allowing you to complete login or verification, then press Enter to continue. The CLI creates `./output/` itself.

### Batch Conversion

Convert multiple URLs:

```bash
use the skill web-to-markdown to convert these URLs:
- https://example.com/article1
- https://example.com/article2
- https://example.com/article3
Save them to ./articles/
```

This will run separate commands for each URL; the CLI creates `./articles/` itself (`src/cli.ts`, checked 2026-11-15). Page titles can repeat, so the skill checks for two pages resolving to the same auto-named path before writing:
```bash
web2md 'https://example.com/article1' --out ./articles/
web2md 'https://example.com/article2' --out ./articles/
web2md 'https://example.com/article3' --out ./articles/
```

### Advanced Wait Strategies

For heavy JavaScript applications:

```bash
use the skill web-to-markdown to convert https://app.example.com/dashboard
Wait for the main selector to appear
```

This will run:
```bash
web2md 'https://app.example.com/dashboard' --wait-until domcontentloaded --wait-for 'main' --print
```

## Advanced Options

The skill supports various options to handle tricky pages:

- `--chrome-path <path>`: Specify Chrome/Chromium location if auto-detection fails
- `--interactive`: Show browser and pause for manual intervention
- `--wait-until <event>`: Wait for `load`, `domcontentloaded`, `networkidle0`, or `networkidle2`; `web2md --help` shows the live default, and the Puppeteer lifecycle page defines each event, including `networkidle2` (checked 2026-11-15: https://github.com/leonardocouy/web2md src/cli.ts, https://pptr.dev/api/puppeteer.puppeteerlifecycleevent)
- `--wait-for '<selector>'`: Wait for specific CSS selector to appear
- `--wait-ms <milliseconds>`: Additional wait time in milliseconds
- `--headful`: Show browser window (useful for debugging)
- `--no-sandbox`: Disable Chromium's sandbox, including the setuid sandbox (sometimes required in containers/CI). Never the default: untrusted page JavaScript then runs unsandboxed, so only an explicit isolated environment may use it (the same rule as in SKILL.md; flags checked 2026-11-15, source: src/lib/render.ts of https://github.com/leonardocouy/web2md and https://pptr.dev/troubleshooting)
- `--user-data-dir <dir>`: Use persistent browser profile (for sessions/logins)

## Output Format

The generated Markdown includes:

- **YAML Frontmatter** (on by default; `--no-frontmatter` omits it): run `web2md --help` for the options and see src/lib/frontmatter.ts of https://github.com/leonardocouy/web2md for the field list (checked 2026-11-15)
- **Main Content**: Article text with preserved formatting
- **Clean Links**: Properly formatted Markdown links
- **Images**: Preserved with alt text and captions where available

## Technical Details

- **Browser Automation**: Uses `puppeteer-core` with local Chrome/Chromium
- **Content Extraction**: Mozilla Readability library
- **Markdown Conversion**: Turndown library
- **Supported Browsers**: Chrome, Chromium, Brave, Edge (Chromium-based)

## Troubleshooting

**Chrome not found:**
- Install Chrome/Chromium or specify path with `--chrome-path`

**Page content incomplete:**
- Try `--wait-until networkidle2` (what it waits for is defined on the Puppeteer lifecycle page linked under Advanced Options)
- Use `--wait-for '<selector>'` to wait for specific elements
- Add `--wait-ms 2000` for additional delay

**Login required:**
- Use `--interactive` mode to manually login
- Use `--user-data-dir` to persist session across runs

**Verification/CAPTCHA:**
- Use `--interactive` mode to complete verification manually

## Version

Current version: 0.1.0

## Related Tools

For simpler use cases without JavaScript, consider using Claude Code's built-in `WebFetch` tool instead.

## Credits

Adapted from the `claude/web-to-markdown` skill of [leonardocouy/web2md](https://github.com/leonardocouy/web2md) (MIT) by Leonardo Flores (@leonardocouy), through [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit). The `web2md` CLI it drives is that repository's tool, published as `@leoflores/web2md`.

Documentation owners credited (official pages listed in `docs/audit/upstream-sources.json`, checked 2026-11-15): Puppeteer (navigation wait events, sandbox troubleshooting), Anthropic (Claude Code tools reference).
