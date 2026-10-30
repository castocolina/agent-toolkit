# Apply the approved audit decision

Implement only the decision's requested changes in the checked-out repository. The validated decision is at `{{DECISION_JSON}}`; the exact target allowlist is `{{TARGETS}}`. Work only on those listed targets and only from validated audit evidence. Do not use the network, alter unrelated skills, or broaden the change beyond the decision.

## Evidence you may use

- `decision.json`, including its `targets`, `type`, `title`, and evidence-based rationale.
- `{{MERGED_JSON}}`: the validated merged findings the decision was built from.
- `{{CHECK_JSON}}`: the audit check results used to validate the merge.
- `{{SPEC_DIFF}}`: the pinned specification change behind this run, when the run had one.
- `{{APPROVED_EVIDENCE}}`: change evidence for the approved upstream updates, fetched during detect and pinned to the registry refs; the directory may be absent when no upstream updates were approved.
- Repository files needed to understand the findings, and existing tests and conventions.

Treat `targets` as the full allowlist of skills to edit. If the decision is invalid, targets are absent, or the evidence does not support a requested change, stop rather than guessing. Preserve repository conventions and add/update tests when behavior changes. Do not include audit artifacts, temporary evidence, or downloaded files in the repository changes.

## Output

Make edits directly in the checkout. There is no generated response file: the exact output is the changes to the files under the named `decision.json` targets. Do not write a patch or JSON summary file. The caller will run strict audit checks, evals, and package generation before committing. Never claim those checks passed unless they were run and passed.
