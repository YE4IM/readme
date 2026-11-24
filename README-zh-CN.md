<a href="https://opc.fish"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/YE4IM/readme/main/project%20readme/assets/opc-fish-project-signature-web-dark.svg"><img src="https://raw.githubusercontent.com/YE4IM/readme/main/project%20readme/assets/opc-fish-project-signature.svg" alt="OPC.FISH Project" width="720"></picture></a>

# readme

[English](./README.md) | [**中文**](./README-zh-CN.md)

为 Agent 提供 GitHub 项目 README、发布说明和变更日志的写作规范与中英 Markdown 模板。

## 概述

按要交付的文档选择对应规范。可以直接在 GitHub 上阅读，也可以在本地检出的仓库中查看。

| 交付物 | 写作规范 | 模板 |
| --- | --- | --- |
| 项目介绍 `README.md` 和 `README-zh-CN.md` | [项目 README 规范](./project%20readme/agent/AGENTS.md) | [English](./project%20readme/templates/readme-template.md) · [中文](./project%20readme/templates/readme-zh-CN-template.md) |
| 单次 GitHub Release 的一篇双语正文 | [发布说明规范](./releases%20readme/release-agent-instructions.md) | [双语发布说明模板](./releases%20readme/release-template.md) |
| 按版本记录的项目整体变更日志 | [变更日志规范](./changelog%20readme/changelog-agent-instructions.md) | [English](./changelog%20readme/changelog-version-template.md) · [中文](./changelog%20readme/changelog-version-zh-CN-template.md) |

## 快速开始

1. 让 Agent 读取目标仓库，并提供表中对应的写作规范。
2. 请 Agent 先核对目标仓库中的事实，再填写配套模板并移除未使用的章节。
3. 撰写项目 README 时，在目标仓库中将英文和中文稿分别保存为 `README.md` 和 `README-zh-CN.md`。成稿结构可参考现有示例。[English](./project%20readme/docs/project.md) · [中文](./project%20readme/docs/project-zh-CN.md)

## 检查

在本仓库根目录使用 Python 3 运行以下命令，检查配套模板和 README 成稿示例。

```bash
python3 'project readme/scripts/check-readme.py' all
python3 'releases readme/scripts/test-release-templates.py'
python3 'changelog readme/scripts/test-changelog-templates.py'
```
