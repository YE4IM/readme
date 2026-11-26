<a href="https://opc.fish" title="OPC.FISH Project."><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/YE4IM/readme/main/project%20readme/assets/opc-fish-project-signature-web-dark.svg"><img src="https://raw.githubusercontent.com/YE4IM/readme/main/project%20readme/assets/opc-fish-project-signature.svg" alt="OPC.FISH Project" width="720"></picture></a>

# readme

[**English**](./README.md) | [中文](./README-zh-CN.md)

Writing guides and bilingual Markdown templates for agents preparing GitHub project READMEs, release notes, and changelogs.

[Go to Quick Start](#quick-start)

## Overview

Choose a guide for what you want to publish. You can read the guides and templates on GitHub or in a local checkout. No installation is required.

The README guide and templates apply to every GitHub project maintained by this repository’s owner, including projects under a personal account. Put the OPC.FISH project signature before the title in every README. Third-party projects follow their own attribution rules.

| Deliverable | Writing guide | Templates |
| --- | --- | --- |
| Project introduction in `README.md` and `README-zh-CN.md` | [Project README guide](./project/project-agent-instructions.md) | [English](./project/templates/readme-template.md) · [中文](./project/templates/readme-zh-CN-template.md) |
| A single bilingual description for one GitHub Release | [Release notes guide](./releases/release-agent-instructions.md) | [Bilingual release template](./releases/release-template.md) |
| A project-wide changelog with version entries | [Changelog guide](./changelog/changelog-agent-instructions.md) | [English](./changelog/changelog-version-template.md) · [中文](./changelog/changelog-version-zh-CN-template.md) |

## Quick Start

1. Open the guide for your deliverable and share it with an agent that can read the target repository.
2. Ask the agent to verify the project facts, use the matching template, and remove unused sections.
3. Save a project README as `README.md` and `README-zh-CN.md`, paste a single bilingual release note into GitHub Releases, or add the version entry to your project changelog.

See the finished project README examples for the expected layout. [English](./project/docs/project.md) · [中文](./project/docs/project-zh-CN.md)

See the examples for a stable patch and an initial release. [Stable patch](./releases/examples/patch.md) · [Initial release](./releases/examples/initial.md)

The CHANGELOG examples show an unreleased entry, a maintenance-line patch, and an initial release. [English](./changelog/examples/CHANGELOG.md) · [中文](./changelog/examples/CHANGELOG-zh-CN.md)

The same set of releases illustrates which baseline to use for the stable Release and for a changelog that records RCs individually. [Stable Release](./releases/examples/stable-after-rc.md) · [English CHANGELOG](./changelog/examples/CHANGELOG-rc-history.md) · [中文 CHANGELOG](./changelog/examples/CHANGELOG-rc-history-zh-CN.md)

## Checks

Run these commands from the repository root. The first checks the README templates, the repository README pair, and the bundled README examples. The other three run regression tests for the README checker and render the Release and CHANGELOG templates against fixtures.

```bash
python3 project/scripts/check-readme.py all
python3 -B project/scripts/test-readme-checks.py
python3 releases/scripts/test-release-templates.py
python3 changelog/scripts/test-changelog-templates.py
```

Point these commands at your own Markdown files when reviewing a delivery. Add `--prerelease` to check for the Release warning, or `--draft` to allow editorial TODOs in a draft. Review release evidence, comparison ranges, links, and commands separately, and preview special anchors and layout on GitHub.


```bash
python3 project/scripts/check-readme.py pair /path/to/README.md /path/to/README-zh-CN.md --signature remote
python3 releases/scripts/check-release-docs.py release /path/to/release.md
python3 changelog/scripts/check-release-docs.py changelog /path/to/CHANGELOG.md /path/to/CHANGELOG-zh-CN.md
```

For a single-language changelog, pass one path. For one file containing both languages separated by a standalone `---`, add `--bilingual`. For an established layout outside those formats, review the existing structure manually. Published entries support dash or parenthesized ISO dates and use newest-first order, with ties allowed. A bilingual changelog in one file shares one set of Markdown reference definitions across languages. Define a reused version link once.

The release checks require Breaking Changes before other change categories, and compare the category set, list counts, visible alerts, issue references, and recognizable shared download or comparison links, including a Highlights image when that section is enabled. They do not enforce the full Added, Fixed, or Security order. Review that order against the template, and review custom category translations, localized documentation destinations, commands, and factual equivalence against the release evidence. A changelog that groups versions by release line instead of global publication date fails the newest-first date check. Before publication, record copy readiness separately from publication status. For targeted README edits, run the same check before and after and report existing failures separately.
