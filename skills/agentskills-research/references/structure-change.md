# When upstream structure changes

Read this only when `fetch-spec.sh` reports `structure_changed: true` or `rubric-check` reports a broken source anchor. Step 4 needs network access: `--pages-dir DIR` downloads the raw pages. If the fetcher cannot download them, stop and tell the user to re-run with network access; do not edit `SOURCE.json` or the references by hand.

For each added or removed page, in this order:

1. Edit the `FILES` array in `scripts/fetch-spec.sh` (`"<name>.md|docs/<path>.mdx"`): add or delete the entry.
2. Added page: copy `<page>.mdx` from `DIR` (fill `DIR` first by running the step 4 command once) into `tests/skills/agentskills-research/fixtures/upstream/docs/<path>.mdx` (and add it to the fixture `docs.json`); removed page: delete that fixture file.
3. Run `bash tests/skills/agentskills-research/test-fetch-spec.sh` and fix the test until it passes.
4. Online step: pick an empty scratch `DIR` outside the repo and re-run `bash skills/agentskills-research/scripts/fetch-spec.sh --pages-dir DIR`. For a new page it prepends the standard verbatim-copy header and records the header-inclusive SHA-256 in `SOURCE.json`. For a removed page, the same run drops its `SOURCE.json` entry and deletes the reference file.
5. Keep the judge eval `files` lists aligned with the cited sources.
6. Do not finish here: the repair may have advanced the pin, and only the main workflow sets `spec_sha`, bumps `rubric_version` (once) and runs the build and `rubric-check`. Return the latest fetcher JSON to `SKILL.md` and resume Source 1 at step 3 (BASE comparison, rule classification including remapped `source` anchors and criteria of added or removed pages, `spec_sha`, build, `rubric-check`); the fetch-spec test must also pass.
