# Changelog

[**English**](./CHANGELOG-rc-history.md) | [中文](./CHANGELOG-rc-history-zh-CN.md)

## v2.0.0 - 2026-11-26

JSON output now ends with a newline. If your scripts still use the old output flag, follow the [complete migration instructions](https://example.com/example/releases/tag/v2.0.0).

### Changed

- JSON output ends with a newline, so it displays cleanly in terminals.

### Full Changelog

- [Full Changelog](https://example.com/example/compare/v2.0.0-rc.1...v2.0.0)

## v1.9.4 - 2026-11-25

CSV exports now finish when a row contains an empty field.

### Fixed

- Keep empty fields in the exported row without stopping the export.

### Full Changelog

- [Full Changelog](https://example.com/example/compare/v1.9.3...v1.9.4)

## v2.0.0-rc.1 - 2026-11-24

The CLI introduces a new output flag.

> [!WARNING]
> This pre-release is for testing and feedback. Avoid production use.

### Breaking Changes

- **CLI**: Scripts using the removed output flag must switch flags.

**Migration:**

1. Replace `--format` with `--output` in scripts that select JSON output.

### Full Changelog

- [Full Changelog](https://example.com/example/compare/v1.9.3...v2.0.0-rc.1)

## v1.9.3 - 2026-11-20

The initial release opens local CSV files for preview in a desktop window.

### Added

- Preview local CSV files in a desktop window.
