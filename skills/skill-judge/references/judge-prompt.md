You are judge `{JUDGE}`. Judge these skills: {SKILLS}

1. Use the Read tool on `{ROOT}/skills/skill-judge/SKILL.md` and execute its mandatory protocol before judging anything: read `{ROOT}/skills/skill-judge/references/rubric.md` and each spec file it cites, in full.
2. Each skill in the list is a directory under `{ROOT}/skills/`. Read its `SKILL.md` and any other file in that directory the rubric needs and, when it has `scripts/`, its script tests under `{ROOT}/tests/skills/<name>/`. Use only read-only tools; never modify files.
3. Output contract rule 1 applies: print exactly one verdict JSON object per listed skill, one per line, in the order listed, and nothing else (no Markdown, no code fence, no commentary).
4. Set `judge` to `{JUDGE}` in every verdict. Set `skill` to the directory name. Set `file` in findings to the path relative to `{ROOT}`.
