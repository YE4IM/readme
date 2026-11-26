<p align="center">
<a href="https://opc.fish" title="OPC.FISH Project."><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/YE4IM/readme/main/project/assets/opc-fish-project-signature-dark.svg"><img src="https://raw.githubusercontent.com/YE4IM/readme/main/project/assets/opc-fish-project-signature.svg" alt="OPC.FISH 项目署名" width="720"></picture></a>
</p>

# readme

[English](./README.md) | [**中文**](./README-zh-CN.md)

为 Agent 提供 GitHub 项目 README、发布说明和变更日志的写作规范与中英 Markdown 模板。

[![License: MIT](https://img.shields.io/badge/License-MIT-2563EB?style=flat&labelColor=1F2A37)](./LICENSE)

[跳转到快速开始](#快速开始)

## 概述

按要发布的文档选择对应规范。可以直接在 GitHub 上阅读，也可以在本地检出的仓库中查看，无需安装。

本仓库的 README 规范和模板适用于仓库所有者维护的 GitHub 项目，包括个人账号下的项目。第三方项目遵循各自的署名规则。

| 交付物 | 写作规范 | 模板 |
| --- | --- | --- |
| 项目介绍 `README.md` 和 `README-zh-CN.md` | [项目 README 规范](./project/project-agent-instructions.md) | [English](./project/templates/readme-template.md) · [中文](./project/templates/readme-zh-CN-template.md) |
| 单次 GitHub Release 的一篇双语正文 | [发布说明规范](./releases/release-agent-instructions.md) | [双语发布说明模板](./releases/release-template.md) |
| 按版本记录的项目整体变更日志 | [变更日志规范](./changelog/changelog-agent-instructions.md) | [English](./changelog/changelog-version-template.md) · [中文](./changelog/changelog-version-zh-CN-template.md) |

## 快速开始

1. 打开对应的写作规范，交给能读取目标仓库的 Agent。
2. 请 Agent 先核对项目事实，再填写配套模板并删除未使用的章节。
3. 根据文档类型交付。项目 README 分别保存为 `README.md` 和 `README-zh-CN.md`，发布说明以一篇双语正文填入 GitHub Releases，变更日志则将版本条目加入项目的变更日志。

编写项目 README 时，两份文件都在标题上方居中显示 OPC.FISH 署名。简介下方使用同一行 1–4 枚可点击的 Shields.io 静态徽章，按 `License`、`Version`、`Language`、`Platform` 的顺序列出有依据的类别。四类均无法核实时，使用 `Source: Repository`。发布前检查双语成稿。[徽章规则](./project/project-agent-instructions.md#必填徽章) · [英文示例](./project/docs/project.md) · [中文示例](./project/docs/project-zh-CN.md)

**徽章配色示例**

![License: MIT](https://img.shields.io/badge/License-MIT-2563EB?style=flat&labelColor=1F2A37) ![Version: 1.0.0](https://img.shields.io/badge/Version-1.0.0-D9381E?style=flat&labelColor=1F2A37) ![Language: JavaScript](https://img.shields.io/badge/Language-JavaScript-0E8274?style=flat&labelColor=1F2A37) ![Platform: Web](https://img.shields.io/badge/Platform-Web-C6286B?style=flat&labelColor=1F2A37)

撰写 GitHub Release 时，先核对目标 Tag 或提交，以及同一发布线的对比范围。GitHub 标题默认使用已核实的发布标识，有既定命名惯例时沿用。正文从摘要起笔，先写英文，再用独立一行的 `---` 分隔中文。预发布时，两种语言都要有警示。[正式补丁](./releases/examples/patch.md) · [首次发布](./releases/examples/initial.md)

双语 CHANGELOG 示例展示了未发布项、维护线补丁和首次发布。[English](./changelog/examples/CHANGELOG.md) · [中文](./changelog/examples/CHANGELOG-zh-CN.md)

同一组版本的对照示例展示了正式版和逐版记录 RC 的 CHANGELOG 各自选择的基线。[正式版 Release](./releases/examples/stable-after-rc.md) · [English CHANGELOG](./changelog/examples/CHANGELOG-rc-history.md) · [中文 CHANGELOG](./changelog/examples/CHANGELOG-rc-history-zh-CN.md)

## 检查

从本仓库根目录运行以下命令，需要 Python 3.8 或更高版本，无需安装其他依赖。

### 项目 README

```bash
python3 project/scripts/check-readme.py all
python3 project/scripts/test-readme-checks.py
python3 project/scripts/check-readme.py pair /path/to/README.md /path/to/README-zh-CN.md --signature remote
```

第一条命令检查模板和仓库内的双语成稿，第二条运行回归测试。审阅自己的成稿时，共用远程署名图选 `--signature remote`，使用目标仓库中的副本选 `--signature local`，草稿可加 `--draft` 保留编辑用 TODO。检查器比较安装和快速开始的命令，检查相对链接、锚点、模板残留、常见密钥模式、双语一致的 1–4 枚必填徽章、署名和折叠的核心步骤。人工核对项目事实、命令和页面布局，并确认 `[指南][install]` 这类引用式链接有对应定义。局部更新前后运行相同命令，单列已有问题。

生成徽章图片地址时，将类别和已核实的值传给 `badge` 子命令。例如，`python3 project/scripts/check-readme.py badge License MIT` 会输出本页徽章的图片地址。请对照目标仓库核实徽章取值与点击目标。

### 发布说明

```bash
python3 releases/scripts/test-release-templates.py
python3 releases/scripts/check-release-docs.py release /path/to/release.md
```

测试用固定样本渲染 Release 模板。检查器强制「Breaking Changes / 破坏性变更」排在亮点展示和其他变更分类之前，并比较两侧分类集合、列表条数、可见警示、事项编号、贡献者 handle 和可识别的共享下载或比较链接；两侧都启用亮点展示时，还会比较该节的图片地址。Added、Fixed、Security 等的完整先后不由脚本强制。

预发布稿加上 `--prerelease`，检查两种语言的摘要后是否都有警示。事实或必要升级步骤待核对时，可加 `--draft` 保留编辑用 TODO，定稿时去掉该参数再检查。自定义分类译名、本地化指南、直接粘贴的 PR 地址、命令与事实含义仍需结合发布证据核对。可识别的直接下载链接（含无扩展名安装包）须指向相同产物。交付时记录文案就绪状态和实际公开状态。

### 变更日志

```bash
python3 changelog/scripts/test-changelog-templates.py
python3 changelog/scripts/check-release-docs.py changelog /path/to/CHANGELOG.md /path/to/CHANGELOG-zh-CN.md
```

单语言 CHANGELOG 只传一个文件路径。单篇双语且两部分用独立一行的 `---` 分隔时，再加 `--bilingual`；单篇双语的 CHANGELOG 两部分共用整篇文件的引用式链接定义，同一版本链接只需定义一次。待核对草稿可加 `--draft`，公开日期未核实而保留日期 TODO 时也要加。

检查器对分类、警示、贡献者 handle 和共享链接的比较与上面的发布说明检查相同，也不强制 Added、Fixed、Security 的完整先后。已发布版本支持短横线或括号包围的 ISO 日期，日期后可带 `Pre-release` 这类标签，按日期从新到旧排列，允许同日多个版本；按版本线分段、而不是按公开发布日全局从新到旧排列的变更日志，会报顺序错误。带显式预发布标签的自定义版本号也必须有警示，两种语言的发布状态须一致。`Unreleased` 不写日期。

版本标题、迁移步骤和日期仍需对照仓库人工核对。局部更新分别报告新条目和全文件的检查结果。发布前分列文案就绪状态和实际公开状态。

## 许可证

[MIT 许可证](./LICENSE)。
