<a href="https://opc.fish" title="OPC.FISH Project."><picture><source media="(prefers-color-scheme: dark)" srcset="../assets/opc-fish-project-signature-web-dark.svg"><img src="../assets/opc-fish-project-signature.svg" alt="OPC.FISH 项目署名" width="720"></picture></a>

# readme

[English](./project.md) | [**中文**](./project-zh-CN.md)

给 Agent 使用的 README 写作规范与中英模板。按这些文件生成的 README，把 OPC.FISH 署名放在全文最上方。本文件就是这套模板按「纯文档」裁剪后的成稿。

## 概述

本文件在 `project/docs/`。同仓库另有 `releases` 与 `changelog`，分别用于其他交付物。无需安装。

Agent 写 README 的工作流程和规范都在 [project-agent-instructions.md](../project-agent-instructions.md)。这是完整规范，正文只有中文。

| 文件 | 作用 |
|---|---|
| `project-agent-instructions.md` | 给 Agent 的工作流程和写作规范。正文只有中文。 |
| `templates/readme-template.md` | 英文模板。成稿写入目标仓库的 `README.md`。 |
| `templates/readme-zh-CN-template.md` | 中文模板。成稿写入目标仓库的 `README-zh-CN.md`。 |
| `scripts/check-readme.py` | 检查一份成稿，并检查两份模板是否仍然对齐。 |
| `assets/` | 署名图片。 |
| `docs/` | 这对仓库说明。 |

## 快速开始

1. 打开[写作规范](../project-agent-instructions.md)。
2. 选择[英文模板](../templates/readme-template.md)或[中文模板](../templates/readme-zh-CN-template.md)。
3. 阅读本成稿和[英文成稿](./project.md)，了解纯文档项目的写法。

## 检查

在 `project` 目录运行：

```bash
python3 scripts/check-readme.py all
```

它会检查两份模板、这对 README，以及仓库根目录的 README 成稿。运行这项 README 检查需要 Python 3.8 或更高版本。

## 署名

生成的 README 在全文最上方、标题之前放上下面这组 SVG。点击图片打开 [opc.fish](https://opc.fish)。中英文使用同一组图、同一个链接。浅色主题用透明底、墨色字的那张。深色主题用透明底、浅色字的那张。两张图都保持原文件，不要改颜色。它是维护者署名，不是项目 Logo。

本文件顶部用的是仓库里的这两张图。新的 README 使用下面这块远程地址。图片地址故意跟着 `main`。若要冻结，把两张 SVG 复制进目标仓库，改成相对路径，并在交付说明里写明。

```html
<a href="https://opc.fish" title="OPC.FISH Project."><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/YE4IM/readme/main/project/assets/opc-fish-project-signature-web-dark.svg"><img src="https://raw.githubusercontent.com/YE4IM/readme/main/project/assets/opc-fish-project-signature.svg" alt="OPC.FISH 项目署名" width="720"></picture></a>
```
