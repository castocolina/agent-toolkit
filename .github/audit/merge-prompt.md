# Decide whether the audit should propose an update

Use only the evidence enumerated here. Do not independently judge skills or infer findings not supported by evidence. Produce a conservative decision, not edits.

## Evidence you may use

- `{{MERGED_JSON}}`: aggregated judge verdicts and their validated findings (`audit.py merge --out` writes `merged/merged.json`).
- `{{SPEC_DIFF}}`: the pinned specification change (including the specified base diff on a rubric-stale-only run).
- `{{UPSTREAMS_JSON}}`: upstream freshness rows and metadata.
- `{{EVALS_RESULTS}}`: output and trigger eval results, including `QUALITY_FAILED={{QUALITY_FAILED}}`.
- `{{CHECK_JSON}}`: the audit check results.
- `{{APPROVED_EVIDENCE}}`: change evidence fetched during detect for the approved upstream keys, pinned to the registry refs; the directory may be absent when no keys were approved.
- `APPROVED_UPSTREAMS={{APPROVED_UPSTREAMS}}`: literal comma-separated `skill|source` keys explicitly approved for this run.
- Existing repository paths only as needed to interpret the evidence; do not treat unrelated files or network information as evidence.

Upstream updates may be recommended/applied only for stale rows whose exact `skill|source` key appears in `APPROVED_UPSTREAMS`. Every unapproved stale row is report-only and must not cause an update decision or target. Do not mistake a recommendation in any evidence for user approval.

## Output

Write exactly `{{DECISION_JSON}}` as one JSON object with this shape:

```json
{"update":true,"type":"fix","title":"Concise title","targets":["skill-name"],"rationale":"Evidence-based explanation"}
```

Required keys are `update`, `type`, `title`, `targets`, and `rationale`. `update` is a JSON boolean. `type` is `feat` or `fix`; `title` is a non-empty string; `targets` is an array of skill directory names (empty when `update` is false); `rationale` is a non-empty string written as a single paragraph with no newlines or control characters. Set `update` true only when the evidence supports a concrete repository change. Do not include markdown fences, extra keys, comments, or prose outside the JSON file.

When touching or referring to rubric metadata, copy `rubric_version`, `spec_sha` and every `max` from `skills/skill-judge/references/rubric.md`; never recompute or invent them. The decision file itself does not contain those rubric values. The caller validates `decision.json` with `audit.py validate-decision`; do not claim validation unless it was run and passed.
