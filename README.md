<a href="https://opc.fish" title="OPC.FISH Project."><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/YE4IM/readme/main/project%20readme/assets/opc-fish-project-signature-web-dark.svg"><img src="https://raw.githubusercontent.com/YE4IM/readme/main/project%20readme/assets/opc-fish-project-signature.svg" alt="OPC.FISH Project" width="720"></picture></a>

# readme

[**English**](./README.md) | [中文](./README-zh-CN.md)

Writing guides and bilingual Markdown templates for agents preparing GitHub project READMEs, release notes, and changelogs.

[Go to Quick Start](#quick-start)

## Overview

Choose a guide for what you want to publish. You can read the guides and templates on GitHub or in a local checkout. No installation is required.

| Deliverable | Writing guide | Templates |
| --- | --- | --- |
| Project introduction in `README.md` and `README-zh-CN.md` | [Project README guide](./project%20readme/agent/AGENTS.md) | [English](./project%20readme/templates/readme-template.md) · [中文](./project%20readme/templates/readme-zh-CN-template.md) |
| A single bilingual description for one GitHub Release | [Release notes guide](./releases%20readme/release-agent-instructions.md) | [Bilingual release template](./releases%20readme/release-template.md) |
| A project-wide changelog with version entries | [Changelog guide](./changelog%20readme/changelog-agent-instructions.md) | [English](./changelog%20readme/changelog-version-template.md) · [中文](./changelog%20readme/changelog-version-zh-CN-template.md) |

## Quick Start

1. Open the guide for your deliverable and share it with an agent that can read the target repository.
2. Ask the agent to verify the project facts, use the matching template, and remove unused sections.
3. Save a project README as `README.md` and `README-zh-CN.md`, paste a single bilingual release note into GitHub Releases, or add the version entry to your project changelog.

See the finished project README examples for the expected layout. [English](./project%20readme/docs/project.md) · [中文](./project%20readme/docs/project-zh-CN.md)

## Checks

Run these commands with Python 3 from the root of this repository to check the bundled templates and README examples.

```bash
python3 'project readme/scripts/check-readme.py' all
python3 'releases readme/scripts/test-release-templates.py'
python3 'changelog readme/scripts/test-changelog-templates.py'
```
