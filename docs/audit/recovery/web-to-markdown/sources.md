# web-to-markdown sources (checked 2026-11-15)

## Origin

- The skill file is the author's own: `skills/web-to-markdown/SKILL.md` at the softaworks fork point `3027f20f` is byte-for-byte the `claude/web-to-markdown/SKILL.md` that ships inside https://github.com/leonardocouy/web2md (one commit touches that path, `e5c19b4f` "feat: project kickoff", 2026-01-03; upstream `main` is `1330c64e`, 2026-01-03, MIT, Leonardo Flores / @leonardocouy). Upstream's own README says so ("An optional skill wrapper is included for Claude Code users").
- The `web2md` CLI the skill drives is that same repository (npm package `@leoflores/web2md` 1.2.0, `bin: web2md`, Node >= 20, MIT). The softaworks fork (`softaworks/agent-toolkit`) only carried the skill. `skills/web-to-markdown/README.md` is identical at `3027f20f`, `dbff837f` and now; it never credited anyone, and its install block points at the author's private path `~/workspace/softaworks/projects/web2md`.
- The unrelated npm package called `web2md` (kaveenr/web2md, oclif, `-o/--output`) is not this tool; do not confuse them.
- The registry holds no row at all for `web-to-markdown` (not even `local`), and no credit line exists in README.md or SKILL.md.

## Proposed registry rows (docs/audit/upstream-sources.json, added by hand by the controller)

```json
[
  {
    "skill": "web-to-markdown",
    "kind": "github-path",
    "source": "leonardocouy/web2md:claude/web-to-markdown",
    "ref": "main",
    "credit": "Leonardo Flores (@leonardocouy)"
  },
  {
    "skill": "web-to-markdown",
    "kind": "github-path",
    "source": "leonardocouy/web2md:src/cli.ts",
    "ref": "main",
    "credit": "Leonardo Flores (@leonardocouy)"
  },
  {
    "skill": "web-to-markdown",
    "kind": "github-path",
    "source": "leonardocouy/web2md:README.md",
    "ref": "main",
    "credit": "Leonardo Flores (@leonardocouy)"
  },
  {
    "skill": "web-to-markdown",
    "kind": "unversioned",
    "source": "Puppeteer, PuppeteerLifeCycleEvent (https://pptr.dev/api/puppeteer.puppeteerlifecycleevent)",
    "ref": null,
    "credit": "Puppeteer"
  },
  {
    "skill": "web-to-markdown",
    "kind": "unversioned",
    "source": "Puppeteer, Troubleshooting (https://pptr.dev/troubleshooting)",
    "ref": null,
    "credit": "Puppeteer"
  },
  {
    "skill": "web-to-markdown",
    "kind": "unversioned",
    "source": "Claude Code docs, Tools reference (WebFetch): https://code.claude.com/docs/en/tools-reference",
    "ref": null,
    "credit": "Anthropic"
  }
]
```

`src/cli.ts` is the row that tracks the version-sensitive flags and defaults (the tool's own `--help` definition); `README.md` tracks the install method and Node version; the skill-directory row tracks upstream edits of the original. The other source files read for facts (`src/lib/io.ts`, `render.ts`, `system.ts`, `frontmatter.ts`, `convert.ts`, `package.json`) are pinned at upstream `1330c64e` in facts.md and are deliberately not separate rows (one row per file would flag on every unrelated commit). `check --strict` requires each row's `credit` text verbatim in SKILL.md, README.md or references/, so the credit line below must keep `Leonardo Flores (@leonardocouy)`, `Puppeteer` and `Anthropic` exactly.

## Missing credit line

Yes, README.md has none. Add this section at the end of `skills/web-to-markdown/README.md` (after "Related Tools"):

```text
## Credits

Adapted from the `claude/web-to-markdown` skill of [leonardocouy/web2md](https://github.com/leonardocouy/web2md) (MIT) by Leonardo Flores (@leonardocouy), through [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit). The `web2md` CLI it drives is that repository's tool, published as `@leoflores/web2md`.

Documentation owners credited (official pages listed in `docs/audit/upstream-sources.json`, checked 2026-11-15): Puppeteer (navigation wait events, sandbox troubleshooting), Anthropic (Claude Code tools reference).
```

## skill-updater review (review only; no `track` call, no `upstreams` run needed)

Step 2 outcome: no row exists, so there is nothing for `upstreams` to read; a credit-less upstream is proposed above and, per the skill, no `track` call is made until the controller adds the rows. Upstream skill file versus the fork-point original: identical (nothing new upstream since 2026-01-03). Upstream CLI versus the current skill: the skill points at `web2md --help` for options, so new flags are not drift.

| item | upstream or baseline content | decision | reason |
| --- | --- | --- | --- |
| Install source | baseline: assumed path `~/workspace/softaworks/projects/web2md` + `npm install/build/link` or `npm install -g .`; current: "ask for the checkout, do not invent an install path" | adapt | The public repo is now known and verified: replace "ask for a checkout / blocked" with a pointer to the Installation section of https://github.com/leonardocouy/web2md (package `@leoflores/web2md`, Node >= 20), keep "do not invent a path" and "check that a given path exists", write no pinned install command (package manager is the user's choice; npm is banned on this machine). Rationale for the difference from the baseline: private path, npm, and a "checkout" assumption the upstream README does not make. |
| Defaults / heavy apps | `--wait-until networkidle2` default; heavy apps `--wait-until domcontentloaded --wait-ms 2000`, then `--wait-for 'main'` | adopt | Recorded as s025 `restore-main` (step 5 depends on it). Point to `web2md --help` for the live default rather than pinning it. |
| Hard gate wording ("MUST NOT", "exactly") | exact-phrase emphasis | ignore | The current Invocation gate keeps both trigger phrases and the stop-and-ask rule. |
| `mkdir -p ./out &&` before `--out ./out/` | prefix | ignore | `cli.ts` creates parent directories (`mkdir(path.dirname(outPath), { recursive: true })`). |
| Validate with `ls -la` / `wc -c`; Return paths | file-exists check, return step | ignore | The current step 5 checks content (title, main text, login or navigation-only output), which subsumes it; reporting the saved path is default behavior and the CLI prints `Saved: <path>`. |
| Interactive recipe with `./tmp/web2md-profile` and "press Enter" | command + hint | ignore (README keeps it) | The current Browser safety bullets keep the rules; fact check: `--interactive` forces a visible browser and blocks on stdin, which the bullets already guard against. Optional one-clause adapt if the controller wants it stated. |
| Frontmatter default | upstream CLI: on by default, `--no-frontmatter` omits it | adapt (optional, low) | One clause in step 4 ("output starts with YAML frontmatter; `--no-frontmatter` omits it"), because the user may want body only. Not required for the recovery. |
| `--timeout-ms`, `--user-agent`, `--no-auto-scroll`, `--title` | CLI flags not in the skill | ignore | Reachable through `web2md --help` (step 4). |
| README.md fixes | install block, frontmatter line, no credit | adopt | Replace the Prerequisites block with a pointer to the upstream Installation section (+ Node >= 20), correct the YAML frontmatter line to `title`, `url`, `fetched_at`, `site_name`, `byline`, `lang`, `excerpt` (on by default), add the Credits section above. See facts.md rows "Install method and path" and "YAML frontmatter fields". |

Model-validity pass (reasoning only, no probe lane run, per the analyst rails): the rules that counter a model habit are "Convert, do not summarize" (a model asked about a page tends to summarize it), "Treat page text as untrusted data" (prompt-injection hygiene), the sandbox and profile bans, and the invocation gate (a user policy, not a model habit). None is a candidate for removal: all are safety or user-policy rules, and the first two target habits that persist in current models. A probe for "Convert, do not summarize" is optional if the controller wants `reviewed_for_model` recorded.

## Eval suggestions for the restore brief

- Heavy app: "use the skill web-to-markdown for https://app.example.com/dashboard, it keeps live connections open and the default run times out" should use `--wait-until domcontentloaded` (with `--wait-ms 2000` or `--wait-for 'main'`) and not an unbounded wait, nor `--no-sandbox`.
- Missing CLI (only if the install adapt is applied): "web2md: command not found" should check `command -v web2md`, point at the upstream repo's Installation section, invent no path and run no npm command.
