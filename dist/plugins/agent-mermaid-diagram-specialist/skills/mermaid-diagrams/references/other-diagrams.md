# State, Git, Gantt, and Pie

One working example per type (none for pie) plus the constructs that fail. Styling levers per type are in [authoring-rules.md](authoring-rules.md) section 3 ("Type-native controls").

## State (`stateDiagram-v2`)

```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Review : submit
    state check <<choice>>
    Review --> check
    check --> Published : approved
    check --> Draft : changes requested
    Published --> [*]
```

- `<<choice>>` for a branch, `<<fork>>` and `<<join>>` for parallel paths, `state Name { ... }` for a composite state, `--` inside it for concurrent regions.
- `classDef` on `[*]` is a parse error. Every non-final state needs an outgoing transition, or the reader cannot tell a dead end from an omission.

## Git (`gitGraph`)

```mermaid
gitGraph TB:
    commit id: "init"
    branch release/1.2
    checkout release/1.2
    commit id: "rc1"
    branch hotfix
    checkout hotfix
    commit id: "fix-login" type: HIGHLIGHT
    checkout release/1.2
    merge hotfix id: "merge-fix" tag: "v1.2.1"
    checkout main
    cherry-pick id: "fix-login"
```

- `branch X` creates and switches to `X` (see the SKILL.md gotcha on `checkout`). The first branch is `main` unless `mainBranchName` is configured.
- `cherry-pick id: "..."` needs an `id:` set on that commit and fails if the commit is already on the current branch. Set an explicit `id:` on every commit you will merge, cherry-pick, or mention.
- `merge` takes the branch name; `id:`, `tag:`, and `type:` on a merge label the merge commit.

## Gantt (`gantt`)

```mermaid
gantt
    title Release plan
    dateFormat YYYY-MM-DD
    axisFormat %b %d
    excludes weekends
    section Build
    Implement      :a1, 2026-01-05, 10d
    Review         :crit, a2, after a1, 3d
    section Ship
    Test           :a3, after a1 a2, 5d
    Release        :milestone, m1, after a3, 0d
```

- Task line: `Name :[tags,] [id,] start, end-or-duration`. `start` is a date or `after id1 id2` (starts when the last listed task ends); with no start, a task follows the previous one.
- Every literal date must match `dateFormat` exactly (dayjs tokens: `YYYY-MM-DD`, `DD/MM/YYYY`, `YYYY-MM-DD HH:mm`). Convert "Jan 5" to the declared format.
- `axisFormat` uses d3 strftime tokens (`%Y-%m-%d`, `%b %d`), a different token set from `dateFormat`.
- A milestone is `:milestone, id, date-or-after, 0d`. `excludes weekends` stretches durations over weekends.

## Pie (`pie`)

Syntax: `pie showData`, an optional `title`, then `"Label" : value` lines. Quote every label (the documented form; Mermaid 11.17 also accepts unquoted labels, older hosts may not). A negative value is a parse error. Beyond about seven slices, or for values that are not parts of one whole, use a bar chart in a chart tool instead.
