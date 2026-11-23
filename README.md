# readme

[**English**](./README.md) | [中文](./README.zh-CN.md)

Rules and bilingual templates an agent follows when writing a GitHub README, plus the OPC.FISH signature those READMEs keep at the end. This file is the documentation-shaped result of those templates.

## Overview

Instruction version 1.1.0. Read it here or clone it. There is nothing to install.

An agent writing someone else's README starts at [AGENTS.md](./AGENTS.md), then follows [README-AGENT-INSTRUCTIONS.md](./README-AGENT-INSTRUCTIONS.md).

| File | Role |
|---|---|
| `AGENTS.md` | Short entry for an agent. |
| `README-AGENT-INSTRUCTIONS.md` | The rules. This is not a project README. |
| `README.template.md` | English template. The filled result is `README.md` in the target repository. |
| `README.zh-CN.template.md` | Chinese template. The filled result is `README.zh-CN.md` in the target repository. |
| `scripts/check_readme.py` | Checks a finished pair, and checks that the two templates still match. |
| `examples/sample-cli/` | A finished CLI pair beside a one-file command that runs. |
| `assets/` | Signature images. |

## Check

From this repository:

```bash
python3 scripts/check_readme.py all
```

That checks the templates, this README pair, and `examples/sample-cli/`. Python 3 is enough.

## Signature

Generated READMEs end with the mark below. The picture links to [opc.fish](https://opc.fish). Both languages use the same two images and the same link. Light mode uses the cream image. Dark mode uses the black image supplied for that pair. Leave both files as they are. It is not a project logo and does not belong on the first screen.

New READMEs use this block. The image addresses follow `main` on purpose. To freeze them, copy both PNG files into the target repository, switch to relative paths, and say so in the delivery notes.

```html
<a href="https://opc.fish"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/YE4IM/readme/main/assets/opc-fish-project-signature-readme-2400x800-web-dark.png"><img src="https://raw.githubusercontent.com/YE4IM/readme/main/assets/opc-fish-project-signature-readme-2400x800-on-cream.png" alt="OPC.FISH Project" width="720"></picture></a>
```

`assets/opc-fish-project-signature-on-cream.png` and `assets/opc-fish-project-signature-web-dark.png` are the same mark at 4569×2085. README signatures use the 2400×800 pair.

<a href="https://opc.fish"><picture><source media="(prefers-color-scheme: dark)" srcset="./assets/opc-fish-project-signature-readme-2400x800-web-dark.png"><img src="./assets/opc-fish-project-signature-readme-2400x800-on-cream.png" alt="OPC.FISH Project" width="720"></picture></a>
