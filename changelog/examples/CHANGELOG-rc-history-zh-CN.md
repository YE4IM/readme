# 变更日志

[English](./CHANGELOG-rc-history.md) | [**中文**](./CHANGELOG-rc-history-zh-CN.md)

## v2.0.0 - 2026-11-26

JSON 输出现在以换行符结尾。从上一稳定版升级时，请参阅[完整迁移步骤](https://example.com/example/releases/tag/v2.0.0)。

### 行为变更

- JSON 输出以换行符结尾，在终端中显示更清晰。

### 完整变更日志

- [完整变更日志](https://example.com/example/compare/v2.0.0-rc.1...v2.0.0)

## v1.9.4 - 2026-11-25

行内存在空字段时，CSV 导出现在也能完成。

### 问题修复

- 导出保留行内空字段，并继续处理剩余数据。

### 完整变更日志

- [完整变更日志](https://example.com/example/compare/v1.9.3...v1.9.4)

## v2.0.0-rc.1 - 2026-11-24

CLI 引入新的输出参数。

> [!WARNING]
> 本预发布版用于测试与反馈，不建议在生产环境使用。

### 破坏性变更

- **CLI**：使用已移除输出参数的脚本需要更换参数。

**迁移步骤：**

1. 在选择 JSON 输出的脚本中，将 `--format` 替换为 `--output`。

### 完整变更日志

- [完整变更日志](https://example.com/example/compare/v1.9.3...v2.0.0-rc.1)

## v1.9.3 - 2026-11-20

首次发布支持在桌面窗口中打开并预览本地 CSV 文件。

### 新增功能

- 在桌面窗口中预览本地 CSV 文件。
