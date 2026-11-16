# Open Source Project README Template

Use this template for projects intended for public use and contribution: an OSI-approved license and a public audience. It also serves publicly intended source-available and commercial projects (SKILL.md Workflow step 2): state their actual license and distribution terms, never assume an OSI license, and take the contribution policy from repository evidence (CONTRIBUTING.md, CLA, PR template) or the user.

Fill every placeholder from repository evidence (manifest, LICENSE, CI). A fact the repository does not show stays a visible placeholder; delete a line or a section that does not apply instead of keeping an invented one.

---

# <Project Name>

<One-line description of what this project does>

<!-- Keep only the badges that are true; every badge is a claim (see SKILL.md Gotchas):
     - License: use the SPDX id found in LICENSE or the manifest, never a hard-coded one.
     - Build: the workflow file must exist on the default branch.
     - Version: the package must be published to that registry. -->

[![License](https://img.shields.io/github/license/<user>/<repo>)](LICENSE)
[![Build Status](https://img.shields.io/github/actions/workflow/status/<user>/<repo>/<workflow-file>.yml)](https://github.com/<user>/<repo>/actions)
[![npm version](https://img.shields.io/npm/v/<package-name>)](https://www.npmjs.com/package/<package-name>)

## About

<2-3 sentences explaining what problem this solves and why someone would use it. Include what makes it different from alternatives if relevant.>

## Features

- <Key feature 1>
- <Key feature 2>
- <Key feature 3>

## Installation

```bash
<package manager install command, with the published name from the manifest>
```

### Requirements

- <Supported runtime range, taken from the manifest (for example `engines.node`) or the CI matrix>
- <Other dependencies if any>

## Usage

```<language>
<Minimal working example showing the most common use case, with its real output>
```

### More Examples

<Link to the examples directory or additional code samples>

## Contributing

<Invite contributions only if repository evidence allows it (CONTRIBUTING.md, CLA, PR template) or the user says so; otherwise state the real policy.> See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines (link it only if the file exists).

### Development Setup

```bash
<Commands to clone and set up for development>
```

### Running Tests

```bash
<The test command CI runs>
```

## Roadmap

- [ ] <Planned feature 1>
- [ ] <Planned feature 2>

## Acknowledgments

- <Credit to inspirations, contributors, or dependencies worth highlighting>

## License

<Project name> is licensed under the <SPDX license name from LICENSE> license. See the [`LICENSE`](LICENSE) file for more information.
