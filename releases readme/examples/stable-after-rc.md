The CLI now uses the new output flag, and JSON output ends with a newline.

> [!IMPORTANT]
> If you are upgrading from the previous stable release, update scripts that set the output format.

## Breaking Changes

- **CLI**: Scripts using the removed output flag must switch flags.

**Migration:**

1. Replace `--format` with `--output` in scripts that select JSON output.

## Changed

- JSON output ends with a newline, so it displays cleanly in terminals.

## Full Changelog

[Full Changelog](https://example.com/example/compare/v1.9.3...v2.0.0)

---

CLI 现已使用新的输出参数，JSON 输出也会以换行符结尾。

> [!IMPORTANT]
> 从上一稳定版升级时，请更新指定输出格式的脚本。

## 破坏性变更

- **CLI**：使用已移除输出参数的脚本需要更换参数。

**迁移步骤：**

1. 在选择 JSON 输出的脚本中，将 `--format` 替换为 `--output`。

## 行为变更

- JSON 输出以换行符结尾，在终端中显示更清晰。

## 完整变更日志

[完整变更日志](https://example.com/example/compare/v1.9.3...v2.0.0)
