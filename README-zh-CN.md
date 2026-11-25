<a href="https://opc.fish" title="OPC.FISH Project."><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/YE4IM/readme/main/project%20readme/assets/opc-fish-project-signature-web-dark.svg"><img src="https://raw.githubusercontent.com/YE4IM/readme/main/project%20readme/assets/opc-fish-project-signature.svg" alt="OPC.FISH 项目署名" width="720"></picture></a>

# readme

[English](./README.md) | [**中文**](./README-zh-CN.md)

为 Agent 提供 GitHub 项目 README、发布说明和变更日志的写作规范与中英 Markdown 模板。

[跳转到快速开始](#快速开始)

## 概述

按要发布的文档选择对应规范。可以直接在 GitHub 上阅读，也可以在本地检出的仓库中查看，无需安装。

| 交付物 | 写作规范 | 模板 |
| --- | --- | --- |
| 项目介绍 `README.md` 和 `README-zh-CN.md` | [项目 README 规范](./project%20readme/agent/AGENTS.md) | [English](./project%20readme/templates/readme-template.md) · [中文](./project%20readme/templates/readme-zh-CN-template.md) |
| 单次 GitHub Release 的一篇双语正文 | [发布说明规范](./releases%20readme/release-agent-instructions.md) | [双语发布说明模板](./releases%20readme/release-template.md) |
| 按版本记录的项目整体变更日志 | [变更日志规范](./changelog%20readme/changelog-agent-instructions.md) | [English](./changelog%20readme/changelog-version-template.md) · [中文](./changelog%20readme/changelog-version-zh-CN-template.md) |

## 快速开始

1. 打开对应的写作规范，交给能读取目标仓库的 Agent。
2. 请 Agent 先核对项目事实，再填写配套模板并删除未使用的章节。
3. 根据文档类型交付。项目 README 分别保存为 `README.md` 和 `README-zh-CN.md`，发布说明以一篇双语正文填入 GitHub Releases，变更日志则将版本条目加入项目的变更日志。

项目 README 的成稿结构可参考示例。[English](./project%20readme/docs/project.md) · [中文](./project%20readme/docs/project-zh-CN.md)

## 检查

在本仓库根目录使用 Python 3 运行以下命令，检查配套模板和 README 成稿示例。

```bash
python3 'project readme/scripts/check-readme.py' all
python3 'releases readme/scripts/test-release-templates.py'
python3 'changelog readme/scripts/test-changelog-templates.py'
```
