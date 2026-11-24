# readme

[English](./README.md) | [**中文**](./README.zh-CN.md)

给 Agent 使用的 README 写作规范与中英模板。本文件就是这套模板按「纯文档」裁剪后的成稿。

## 概述

规范版本 1.2.0。在这里阅读或克隆即可，无需安装。

Agent 要给别的仓库写 README 时，先看 [AGENTS.md](./AGENTS.md)，再按 [README-AGENT-INSTRUCTIONS.md](./README-AGENT-INSTRUCTIONS.md) 执行。

| 文件 | 作用 |
|---|---|
| `AGENTS.md` | 给 Agent 的短入口。 |
| `README-AGENT-INSTRUCTIONS.md` | 执行规范，不是项目介绍。 |
| `README.template.md` | 英文模板。成稿写入目标仓库的 `README.md`。 |
| `README.zh-CN.template.md` | 中文模板。成稿写入目标仓库的 `README.zh-CN.md`。 |
| `scripts/check_readme.py` | 检查一份成稿，并检查两份模板是否仍然对齐。 |
| `examples/sample-cli/` | 一份 CLI 成稿，旁边有一条能运行的单文件命令。 |

## 检查

在本仓库运行：

```bash
python3 scripts/check_readme.py all
```

它会检查两份模板、这对 README，以及 `examples/sample-cli/`。有 Python 3 即可。
