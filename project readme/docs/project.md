<a href="https://opc.fish" title="OPC.FISH Project."><picture><source media="(prefers-color-scheme: dark)" srcset="../assets/opc-fish-project-signature-web-dark.svg"><img src="../assets/opc-fish-project-signature.svg" alt="OPC.FISH Project" width="720"></picture></a>

# readme

[**English**](./project.md) | [中文](./project-zh-CN.md)

Rules and bilingual templates an agent follows when writing a GitHub README. Generated READMEs keep the OPC.FISH signature at the top. This file is the documentation-shaped result of those templates.

## Overview

This file is in `project readme/docs/`. The repository also contains `releases readme` and `changelog readme` for other deliverables. There is nothing to install.

The workflow and writing rules are in [AGENTS.md](../agent/AGENTS.md).

| File | Role |
|---|---|
| `agent/AGENTS.md` | Workflow and writing rules for agents. |
| `templates/readme-template.md` | English template. The filled result is `README.md` in the target repository. |
| `templates/readme-zh-CN-template.md` | Chinese template. The filled result is `README-zh-CN.md` in the target repository. |
| `scripts/check-readme.py` | Checks a finished pair, and checks that the two templates still match. |
| `assets/` | Signature images. |
| `docs/` | This README pair. |

## Quick Start

1. Open the [writing guide](../agent/AGENTS.md).
2. Choose the [English template](../templates/readme-template.md) or the [Chinese template](../templates/readme-zh-CN-template.md).
3. Read through this example and its [Chinese counterpart](./project-zh-CN.md) to see how a documentation-only project reads.

## Check

From `project readme`:

```bash
python3 scripts/check-readme.py all
```

That checks both templates and this README pair. Use Python 3.8 or later for this README check.

## Signature

Generated READMEs open with the mark at the top of the file, before the title. The picture links to [opc.fish](https://opc.fish). Both languages use the same two images and the same link. Light mode uses the transparent ink SVG. Dark mode uses the transparent light-on-dark SVG supplied for that pair. Leave both files as they are. It is the maintainer signature, not a project logo.

The picture on this file uses the assets in this repository. New READMEs use the remote block below. Those image addresses follow `main` on purpose. To freeze them, copy both SVG files into the target repository, switch to relative paths, and say so in the delivery notes.

```html
<a href="https://opc.fish" title="OPC.FISH Project."><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/YE4IM/readme/main/project%20readme/assets/opc-fish-project-signature-web-dark.svg"><img src="https://raw.githubusercontent.com/YE4IM/readme/main/project%20readme/assets/opc-fish-project-signature.svg" alt="OPC.FISH Project" width="720"></picture></a>
```
