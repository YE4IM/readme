<!--
可复用模板：仓库变更日志中「单个已发布版本」的中文稿。
只用已核实的事实填写，然后将本节粘贴进 CHANGELOG.zh-CN.md，或仓库既有的中文变更日志。
不要把本模板文件名写进变更日志正文。
结构、分类集合、条目数量、编号、命令和链接必须与英文稿对等。
OPTIONAL 块的用法与英文模板相同：启用则去掉包围注释并删除说明文字，不需要则整块删除（含空标题）。
除有意留下的 {{TODO: ...}} 外，不要残留未替换占位符。
范围、证据、双语对齐与清理规则见同目录 changelog-agent-README.md。
-->

## [{{VERSION}}] - {{RELEASE_DATE}}

{{RELEASE_SUMMARY}}

<!-- 预发布或重要提示：规则同英文稿。 -->

### 破坏性变更

- **{{BREAKING_CHANGE_AREA}}**：{{BREAKING_CHANGE}}

**迁移步骤：**

1. {{MIGRATION_STEP_1}}
2. {{MIGRATION_STEP_2}}

### 新增功能

- {{ADDED_1}}

### 优化与改进

- {{CHANGED_1}}

### 问题修复

- {{FIXED_1}}

### 安全修复

- {{SECURITY_1}}

### 弃用与移除

- {{DEPRECATED_1}}

### 维护与依赖更新

- {{MAINTENANCE_1}}

### 安装与升级

```bash
{{UPGRADE_COMMAND}}
```

### 已知问题

- {{KNOWN_ISSUE_1}}

### 贡献者

感谢 {{CONTRIBUTORS}} 对本版本的贡献。

### 完整变更日志

- [完整变更日志]({{COMPARE_URL}})
