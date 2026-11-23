# readme

[**English**](./README.md) | [中文](./README.zh-CN.md)

Rules and bilingual templates an agent follows when writing a GitHub README, plus the OPC.FISH signature those READMEs keep at the end.

## Overview

This repository is the source for that workflow. Read it here or clone it. There is nothing to install.

| File | Role |
|---|---|
| `README-AGENT-INSTRUCTIONS.md` | Instructions for the agent. This is not a project README. |
| `README.template.md` | English template. Write the result to `README.md` in the target repository. |
| `README.zh-CN.template.md` | Chinese template. Write the result to `README.zh-CN.md` in the target repository. |
| `assets/` | Signature images. |

## Signature

Generated READMEs end with the wide mark below. The image links to [opc.fish](https://opc.fish). Use the same image and the same link in both languages. Do not treat it as a project logo or move it onto the first screen.

In another repository, use this address:

```html
<a href="https://opc.fish"><img src="https://raw.githubusercontent.com/YE4IM/readme/main/assets/opc-fish-project-signature-readme-2400x800-on-cream.png" alt="OPC.FISH Project" width="720"></a>
```

`assets/opc-fish-project-signature-on-cream.png` is a tighter crop of the same mark. The README default is the 2400×800 image.

This repository is public. That address loads in other repositories without signing in.

<a href="https://opc.fish"><img src="./assets/opc-fish-project-signature-readme-2400x800-on-cream.png" alt="OPC.FISH Project" width="720"></a>
