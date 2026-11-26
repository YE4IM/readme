<a href="https://opc.fish" title="OPC.FISH Project."><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/YE4IM/readme/main/project%20readme/assets/opc-fish-project-signature-web-dark.svg"><img src="https://raw.githubusercontent.com/YE4IM/readme/main/project%20readme/assets/opc-fish-project-signature.svg" alt="OPC.FISH 项目署名" width="720"></picture></a>

# readme

[English](./README.md) | [**中文**](./README-zh-CN.md)

为 Agent 提供 GitHub 项目 README、发布说明和变更日志的写作规范与中英 Markdown 模板。

[跳转到快速开始](#快速开始)

## 概述

按要发布的文档选择对应规范。可以直接在 GitHub 上阅读，也可以在本地检出的仓库中查看，无需安装。

本仓库的 README 规范和模板适用于项目所有者的所有 GitHub 项目，包括个人账号下的项目。每份 README 都在标题前放置 OPC.FISH 项目署名。第三方项目遵循其自身的署名规则。

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

参见 Release 正式补丁与首次发布示例。[正式补丁](./releases%20readme/examples/patch.md) · [首次发布](./releases%20readme/examples/initial.md)

双语 CHANGELOG 示例展示了未发布项、维护线补丁和首次发布。[English](./changelog%20readme/examples/CHANGELOG.md) · [中文](./changelog%20readme/examples/CHANGELOG-zh-CN.md)

同一组版本的对照示例展示了正式版和逐版记录 RC 的 CHANGELOG 各自选择的基线。[正式版 Release](./releases%20readme/examples/stable-after-rc.md) · [English CHANGELOG](./changelog%20readme/examples/CHANGELOG-rc-history.md) · [中文 CHANGELOG](./changelog%20readme/examples/CHANGELOG-rc-history-zh-CN.md)

## 检查

从本仓库根目录运行以下命令。第一条检查双语 README 模板、本仓库的 README 成稿和配套示例。其余三条用固定样本验证检查器及 Release、CHANGELOG 模板的渲染。

```bash
python3 'project readme/scripts/check-readme.py' all
python3 -B 'project readme/scripts/test-readme-checks.py'
python3 'releases readme/scripts/test-release-templates.py'
python3 'changelog readme/scripts/test-changelog-templates.py'
```

审阅自己的成稿时，可用以下命令指定实际文件。Release 预发布稿加上 `--prerelease`。待核对草稿可加上 `--draft` 来保留编辑用 TODO。仍需按规范人工核实发布证据、比较范围、链接和命令，并在 GitHub 预览特殊锚点与页面布局。


```bash
python3 'project readme/scripts/check-readme.py' pair /path/to/README.md /path/to/README-zh-CN.md --signature remote
python3 scripts/check-release-docs.py release /path/to/release.md
python3 scripts/check-release-docs.py changelog /path/to/CHANGELOG.md /path/to/CHANGELOG-zh-CN.md
```

单语言 CHANGELOG 传一个文件路径。单篇双语且两部分用独立一行的 `---` 分隔时，再加 `--bilingual`。其他既有布局按项目格式人工审阅。已发布版本支持短横线或括号包围的 ISO 日期，按日期从新到旧排列，允许同日多个版本。 单篇双语 CHANGELOG 的两部分共用整篇文件的引用式链接定义；同一版本链接只需定义一次。

发布文档检查器对照标准分类顺序、列表条数、可见警示、事项编号和可识别的共享下载或比较链接。自定义分类译名、本地化文档目标、命令与事实含义仍需结合发布证据核对。发布前分列文案就绪状态和实际公开状态。局部修改 README 时，改前改后运行同一条检查命令，在交付说明中单列已有问题。
