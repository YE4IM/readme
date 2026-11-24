<!--
Reusable template: one published-version section for a repository CHANGELOG (English).
Fill only verified facts, then paste the section into CHANGELOG.md or the repo's existing English changelog file.
Do not copy this filename into the changelog body.
To enable an OPTIONAL block: remove the surrounding comment markers, keep the section content, and delete the instruction text. Otherwise delete the entire block (including any empty heading).
Do not leave unreplaced placeholders except an intentional {{TODO: ...}}.
Follow changelog-agent-instructions.md in this directory for scope, evidence, bilingual alignment, and cleanup rules.
-->

## [{{VERSION}}] - {{RELEASE_DATE}}

{{RELEASE_SUMMARY}}

<!--
OPTIONAL: Pre-release or important notice. For a pre-release, keep WARNING in both language versions of a bilingual changelog. Explain that this is a pre-release for testing and feedback and advise against production use unless the maintainer has verified written guidance stating otherwise. For a stable release, keep one alert only if users need to see a breaking-change or upgrade caution first.

> [!WARNING]
> {{IMPORTANT_WARNING}}

> [!IMPORTANT]
> {{IMPORTANT_NOTE}}
-->

<!--
OPTIONAL: 破坏性变更。必须紧跟摘要（及必要警示）之后。
迁移步骤无法完全核实时，保留 {{TODO: ...}} 并在交付说明中列出。

### Breaking Changes

- **{{BREAKING_CHANGE_AREA}}**: {{BREAKING_CHANGE}}

**Migration:**

1. {{MIGRATION_STEP_1}}
2. {{MIGRATION_STEP_2}}
-->

<!--
OPTIONAL: 仅当确有已落地的用户可见新能力时启用。

### Added

- {{ADDED_1}}
-->

<!--
OPTIONAL: 仅当确有行为、性能、体验或可靠性改进时启用。不要编造数据。

### Changed

- {{CHANGED_1}}
-->

<!--
OPTIONAL: 仅当确有修复时启用。写清现象与触发条件，有编号则引用。

### Fixed

- {{FIXED_1}}
-->

<!--
OPTIONAL: 仅当确有安全修复或已公开公告时启用。不写利用步骤，不编造 CVE。

### Security

- {{SECURITY_1}}
-->

<!--
OPTIONAL: 仅当确有弃用或移除时启用。

### Deprecated & Removed

- {{DEPRECATED_1}}
-->

<!--
OPTIONAL: 仅当维护性变更对使用者或集成方有必要知晓时启用。

### Maintenance & Dependencies

- {{MAINTENANCE_1}}
-->

<!--
OPTIONAL: 仅当升级途径需要单独说明时启用。主命令必须展开。未验证须标明。

### Installation & Upgrade

```bash
{{UPGRADE_COMMAND}}
```
-->

<!--
OPTIONAL: 仅当该版本已确认仍有未解决问题时启用。

### Known Issues

- {{KNOWN_ISSUE_1}}
-->

<!--
OPTIONAL: 仅当能核实某 handle 在该版本范围内确有贡献时启用。

### Contributors

Thanks to {{CONTRIBUTORS}} for contributing to this release.
-->

<!--
OPTIONAL: 仅当上一 Tag 存在且 Compare URL 可核实时启用。
典型形式：https://github.com/<owner>/<repo>/compare/<previous-tag>...<current-tag>
可见文字不要编造区间。首次发布不要虚构上一版本。

### Full Changelog

- [Full Changelog]({{COMPARE_URL}})
-->
