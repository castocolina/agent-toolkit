# Agent MD Refactor

A Claude Code skill that transforms bloated agent instruction files into clean, organized documentation using progressive disclosure principles.

Based on https://x.com/mattpocockuk/status/2012906065856270504 (Matt Pocock's Prompt Idea)

## Purpose

Over time, agent instruction files like `CLAUDE.md`, `AGENTS.md`, or `.github/copilot-instructions.md` tend to grow into unwieldy documents containing hundreds of lines of mixed instructions. This creates several problems:

- **Context waste**: Every task loads the entire file, even when most instructions are irrelevant
- **Maintenance burden**: Finding and updating specific instructions becomes difficult
- **Contradictions**: Conflicting guidelines accumulate without being noticed
- **Signal-to-noise ratio**: Important rules get buried among obvious or vague statements

This skill solves these problems by applying **progressive disclosure** - keeping only essential, universal instructions in the root file while organizing everything else into focused, linked documentation files.

## When to Use

Use this skill when you need to clean up agent instruction files. Common trigger phrases include:

- "refactor my AGENTS.md" / "refactor my CLAUDE.md"
- "split my agent instructions"
- "organize my CLAUDE.md file"
- "my AGENTS.md is too long"
- "progressive disclosure for my instructions"
- "clean up my agent config"

**Good candidates for refactoring:**

- Root agent files that have grown long (the Claude Code docs target under 200 lines per `CLAUDE.md`: https://code.claude.com/docs/en/memory, checked 2026-11-15)
- Files mixing multiple unrelated topics (testing, code style, architecture, etc.)
- Documents that have grown organically without structure
- Files containing contradictory or redundant instructions

## How It Works

The skill follows a systematic 5-phase process:

### Phase 1: Find Contradictions

Before restructuring, the skill identifies conflicting instructions that need resolution. Examples include contradictory style guidelines ("use semicolons" vs "no semicolons") or incompatible workflow instructions. Each contradiction is surfaced with a question for the user to resolve.

### Phase 2: Identify the Essentials

Extracts only what truly belongs in the root file - information that applies to every single task:

| Keep in Root | Move Out |
|-------------|----------|
| One-sentence project description | Language-specific conventions |
| Non-standard package manager | Testing guidelines |
| Custom build/test commands | Code style details |
| Critical overrides | Framework patterns |
| Universal rules (100% of tasks) | Documentation standards |

### Phase 3: Group the Rest

Organizes remaining instructions into focused topic files, keeping each rule's source scope and exceptions and creating only the topics the file actually contains. For example:

- `typescript.md` - Type patterns, strict mode rules
- `testing.md` - Test frameworks, coverage, mocking
- `code-style.md` - Formatting, naming, structure
- `git-workflow.md` - Commits, branches, PRs
- `architecture.md` - Patterns, folder structure

### Phase 4: Create the File Structure

Generates the new file hierarchy with properly linked documentation:

```
project-root/
├── CLAUDE.md              # Minimal root with read conditions
└── .claude/               # Categorized instructions
    ├── typescript.md
    ├── testing.md
    ├── code-style.md
    └── architecture.md
```

### Phase 5: Flag for Deletion

Reports only rules proven redundant, obsolete or non-actionable, for your review. A project-specific safety override is never deleted as a presumed default:

- **Redundant**: The same rule stated twice with the same scope
- **Too vague**: "Write clean code" without specifics
- **Overly obvious**: "Don't introduce bugs"
- **Presumed default**: "Use descriptive variable names" is reported for review, and kept if the project relies on it
- **Outdated**: References to deprecated APIs

## Key Features

- **Contradiction detection**: Surfaces conflicting instructions before restructuring
- **Intelligent categorization**: Groups related instructions into logical files
- **Root file minimization**: Keeps only universal rules in the main file; universal constraints stay even when the result is longer than a suggested length
- **Removal report**: Lists only rules proven redundant, obsolete or non-actionable, for your review
- **Template-driven output**: Consistent structure across all generated files
- **Link verification**: Ensures all references between files are valid

## Usage Examples

### Basic Refactoring

```
User: refactor my CLAUDE.md

Claude: I'll analyze your CLAUDE.md file and refactor it using progressive
disclosure principles...
```

### Specific File

```
User: my AGENTS.md is too long, can you split it up?

Claude: I'll review your AGENTS.md and organize it into focused, linked files...
```

### After a Project Grows

```
User: organize my agent config - it's gotten out of control

Claude: I'll apply the 5-phase refactoring process to clean up your
agent instructions...
```

## Output

After running the skill, you get:

**Minimal root file (universal rules only, with read conditions):**
```markdown
# Project Name

One-sentence description of the project.

## Quick Reference

- **Package Manager:** pnpm
- **Build:** `pnpm build`
- **Test:** `pnpm test`

## Detailed Instructions

- Read [TypeScript Conventions](.claude/typescript.md) before editing TypeScript code.
- Read [Testing Guidelines](.claude/testing.md) before changing or writing tests.
- Read [Code Style](.claude/code-style.md) before changing formatting or naming.
```

**Organized linked files with only actionable rules, their scope and exceptions:**
```markdown
# Testing Guidelines

Applies when: changing or writing tests. Exception: scripts/ has its own rules.

## Rules

- Specific, actionable instruction
- Another specific instruction
```

**Deletion report:**
```markdown
## Flagged for Review

| Instruction | Reason |
|-------------|--------|
| "Write clean, maintainable code" | Too vague to be actionable |
| "Run tests before committing" (also in .claude/testing.md) | Redundant - same rule and scope stated twice |
```

## Best Practices

### Before Refactoring

1. **Commit current state** - Have a clean git state so you can review changes
2. **Identify your goals** - Know what problems you want to solve
3. **Gather all instruction files** - Some projects have instructions scattered across multiple locations

### During Refactoring

1. **Resolve contradictions first** - Do not proceed until conflicts are addressed
2. **Keep the root to universal rules** - Move out what is not needed for nearly every task, but keep safety constraints in the root
3. **Let the topics decide the file count** - Not too granular, not too broad; a concise guide may need no split
4. **Remove only what is proven** - Redundant, obsolete or non-actionable rules; never delete a project-specific safety override as a presumed default

### After Refactoring

1. **Verify all links work** - Test that referenced files exist
2. **Check for lost instructions** - Ensure nothing important was dropped
3. **Test with real tasks** - Run a few typical tasks to verify the agent can find needed instructions

## Anti-Patterns to Avoid

| Avoid | Why | Instead |
|-------|-----|---------|
| Keeping everything in root | Bloated, hard to maintain | Split into linked files |
| Too many categories | Fragmentation, navigation overhead | Consolidate related topics |
| Vague instructions | Wastes tokens, no value | Be specific, or flag for review |
| Deleting overrides as presumed defaults | A project-specific rule may be essential even if another environment treats it as default | Verify before pruning |
| Deep nesting | Hard to navigate | Flat structure with links |

## Verification Checklist

After refactoring, verify:

- [ ] Root contains ONLY universal information (preserved universal constraints may exceed a suggested length)
- [ ] All links to sub-files work correctly and say when to read them
- [ ] No conditional topic file sits in `.claude/rules/` without `paths:` frontmatter (it would load at launch)
- [ ] No contradictions remain between files
- [ ] Every instruction is specific and actionable
- [ ] No instructions were lost (unless intentionally deleted)
- [ ] Each linked file is self-contained for its topic

## Credits

Originally from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) by @leonardocouy.

Prompt text: https://www.aihero.dev/a-complete-guide-to-agents-md (Matt Pocock). Platform facts: Anthropic, [How Claude remembers your project](https://code.claude.com/docs/en/memory); GitHub, [Support for different types of custom instructions](https://docs.github.com/en/copilot/reference/custom-instructions-support).

## License

MIT
