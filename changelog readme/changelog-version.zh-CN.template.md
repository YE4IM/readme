<!--
可复用模板：仓库变更日志中「单个已发布版本」的中文稿。
只用已核实的事实填写，然后将本节粘贴进 CHANGELOG.zh-CN.md，或仓库既有的中文变更日志。
不要把本模板文件名写进变更日志正文。
结构、分类集合、条目数量、编号、命令和链接必须与英文稿对等。
启用 OPTIONAL 块时，去掉包围注释、保留正文并删除说明文字。不需要的块应连同标题和正文整块删除。
除有意留下的 {{TODO: ...}} 外，不要残留未替换占位符。
范围、证据、双语对齐与清理规则见同目录 changelog-agent-instructions.md。
-->

## [{{VERSION}}] - {{RELEASE_DATE}}

{{RELEASE_SUMMARY}}

<!--
OPTIONAL: 预发布或重要提示。双语变更日志的两种语言都必须为预发布启用 WARNING。
写明当前为预发布，主要用于测试与反馈，且不建议用于生产环境（除非维护者另有可核实的书面说明）。
正式版仅在确有必须先说明的破坏性变更或升级风险时保留一种适用提示。

> [!WARNING]
> {{IMPORTANT_WARNING}}

> [!IMPORTANT]
> {{IMPORTANT_NOTE}}
-->

<!--
OPTIONAL: 破坏性变更。必须紧跟摘要及必要警示。
迁移步骤无法完全核实时，保留 {{TODO: ...}} 并在交付说明中列出。

### 破坏性变更

- **{{BREAKING_CHANGE_AREA}}**：{{BREAKING_CHANGE}}

**迁移步骤：**

1. {{MIGRATION_STEP_1}}
2. {{MIGRATION_STEP_2}}
-->

<!--
OPTIONAL: 仅当确有已落地的用户可见新能力时启用。

### 新增功能

- {{ADDED_1}}
-->

<!--
OPTIONAL: 仅当确有行为、性能、体验或可靠性改进时启用。不要编造数据。

### 优化与改进

- {{CHANGED_1}}
-->

<!--
OPTIONAL: 仅当确有修复时启用。写清现象与触发条件，有编号则引用。

### 问题修复

- {{FIXED_1}}
-->

<!--
OPTIONAL: 仅当确有安全修复或已公开公告时启用。不写利用步骤，不编造 CVE。

### 安全修复

- {{SECURITY_1}}
-->

<!--
OPTIONAL: 仅当确有弃用或移除时启用。

### 弃用与移除

- {{DEPRECATED_1}}
-->

<!--
OPTIONAL: 仅当维护性变更对使用者或集成方有必要知晓时启用。

### 维护与依赖更新

- {{MAINTENANCE_1}}
-->

<!--
OPTIONAL: 仅当升级途径需要单独说明时启用。主命令必须展开。未验证须标明。

### 安装与升级

```bash
{{UPGRADE_COMMAND}}
```
-->

<!--
OPTIONAL: 仅当该版本已确认仍有未解决问题时启用。

### 已知问题

- {{KNOWN_ISSUE_1}}
-->

<!--
OPTIONAL: 仅当能核实某 handle 在该版本范围内确有贡献时启用。

### 贡献者

感谢 {{CONTRIBUTORS}} 对本版本的贡献。
-->

<!--
OPTIONAL: 仅当上一 Tag 存在且 Compare URL 可核实时启用。
典型形式为 https://github.com/<owner>/<repo>/compare/<previous-tag>...<current-tag>。
可见文字不要编造区间。首次发布不要虚构上一版本。

### 完整变更日志

- [完整变更日志]({{COMPARE_URL}})
-->
