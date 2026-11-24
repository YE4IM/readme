<a href="https://opc.fish"><picture><source media="(prefers-color-scheme: dark)" srcset="../assets/opc-fish-project-signature-web-dark.svg"><img src="../assets/opc-fish-project-signature.svg" alt="OPC.FISH Project" width="720"></picture></a>

# readme

[**English**](./README.md) | [中文](./README.zh-CN.md)

Rules and bilingual templates an agent follows when writing a GitHub README. Generated READMEs keep the OPC.FISH signature at the top. This file is the documentation-shaped result of those templates.

## Overview

Instruction version 1.5.0. This file is in `project readme/docs/`. The repository also contains `releases readme` and `changelog readme` for other deliverables. There is nothing to install.

An agent writing someone else's README starts at [AGENTS.md](../agent/AGENTS.md), then follows [README-AGENT-INSTRUCTIONS.md](../agent/README-AGENT-INSTRUCTIONS.md).

| File | Role |
|---|---|
| `agent/AGENTS.md` | Short entry for an agent. |
| `agent/README-AGENT-INSTRUCTIONS.md` | The rules. This is not a project README. |
| `templates/README.template.md` | English template. The filled result is `README.md` in the target repository. |
| `templates/README.zh-CN.template.md` | Chinese template. The filled result is `README.zh-CN.md` in the target repository. |
| `scripts/check_readme.py` | Checks a finished pair, and checks that the two templates still match. |
| `examples/sample-cli/` | A finished CLI pair beside a one-file command that runs. |
| `assets/` | Signature images. |
| `docs/` | This README pair. |

## Check

From `project readme`:

```bash
python3 scripts/check_readme.py all
```

That checks the templates, this README pair, and `examples/sample-cli/`. Python 3 is enough.

## Signature

Generated READMEs open with the mark at the top of the file, before the title. The picture links to [opc.fish](https://opc.fish). Both languages use the same two images and the same link. Light mode uses the transparent ink SVG. Dark mode uses the transparent light-on-dark SVG supplied for that pair. Leave both files as they are. It is the maintainer signature, not a project logo.

The picture on this file uses the assets in this repository. New READMEs use the remote block below. Those image addresses follow `main` on purpose. To freeze them, copy both SVG files into the target repository, switch to relative paths, and say so in the delivery notes.

```html
<a href="https://opc.fish"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/YE4IM/readme/main/project%20readme/assets/opc-fish-project-signature-web-dark.svg"><img src="https://raw.githubusercontent.com/YE4IM/readme/main/project%20readme/assets/opc-fish-project-signature.svg" alt="OPC.FISH Project" width="720"></picture></a>
```
