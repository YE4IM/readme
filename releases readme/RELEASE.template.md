<!--
Start directly with the English release summary. Do not add a project-name or version-number heading, a date/type line, a previous-release line, "English" / "中文" headings, or in-page language-switch links: the GitHub Release page already shows the title and tag.
Write the full English notes first, then a --- separator, then the full Chinese notes.
Keep the opening compact so the summary and any breaking changes stay close.
No banners, badge walls, or decorative animation.
-->

{{RELEASE_SUMMARY}}

<!-- Keep this to 1–3 sentences. Lead with the user-visible outcome of this release. Do not paste raw commit subjects. Do not repeat the version number; GitHub already displays the tag. -->

<!--
OPTIONAL: Pre-release or important notice. Use a GitHub native alert only for a pre-release warning, a breaking-change caution, or a required upgrade note — not for ordinary summary text.
For a pre-release, enable WARNING in both languages. Otherwise keep one alert only when a caution is needed. Remove the comment markers and the instructions from enabled blocks, and delete unused blocks in full.

> [!WARNING]
> {{IMPORTANT_WARNING}}

> [!IMPORTANT]
> {{IMPORTANT_NOTE}}
-->

<!--
OPTIONAL: Breaking Changes. Enable only when this release contains incompatible changes verified in commits, PRs, or docs.
Place this section immediately after the summary and any required alert. Explain what changed incompatibly and who is affected, then give migration steps.
If migration steps cannot be fully verified, keep {{TODO: ...}} and mention it in the delivery notes.
To enable: remove the surrounding comment markers and fill verified items. Otherwise delete this entire block.

## Breaking Changes

- **{{BREAKING_CHANGE_AREA}}**: {{BREAKING_CHANGE}}

**Migration:**

1. {{MIGRATION_STEP_1}}
2. {{MIGRATION_STEP_2}}
-->

<!--
OPTIONAL: Highlights visual or demo. Enable only if this release already has a real screenshot, GIF, or verified command output.
To enable: remove the surrounding comment markers and fill with existing assets or verified output. Otherwise delete this entire block.
Do not invent or generate a visual, and do not fabricate output or benchmark numbers.
Use a descriptive alt, not "screenshot". Prefer an existing project path or a stable URL already used by the project.
Keep the visual compact and place it after Breaking Changes when that section is present.

![{{DEMO_ALT_TEXT}}]({{DEMO_IMAGE_PATH_OR_URL}})
-->

<!--
OPTIONAL: Added. Enable only for user-visible capabilities that actually landed in this release.
Write each item as a concrete change and benefit, not a slogan or a raw commit message. Cite a real PR or issue when one exists.
To enable: remove the surrounding comment markers and fill verified items. Otherwise delete this entire block.

## Added

- {{ADDED_1}}
- {{ADDED_2}}
-->

<!--
OPTIONAL: Changed. Enable only for verified improvements to behavior, performance, usability, or reliability. Do not invent metrics.
To enable: remove the surrounding comment markers and fill verified items. Otherwise delete this entire block.

## Changed

- {{CHANGED_1}}
- {{CHANGED_2}}
-->

<!--
OPTIONAL: Fixed. Enable only for defects that were actually fixed in this release.
Describe the symptom and when it happened. Cite a real issue or PR when one exists.
To enable: remove the surrounding comment markers and fill verified items. Otherwise delete this entire block.

## Fixed

- {{FIXED_1}}
- {{FIXED_2}}
-->

<!--
OPTIONAL: Security. Enable only for verified security fixes or a published advisory.
State the impact and the fix at a high level. Link a real advisory if one exists. Do not invent a CVE, and do not include exploit steps.
To enable: remove the surrounding comment markers and fill verified items. Otherwise delete this entire block.

## Security

- {{SECURITY_1}}
-->

<!--
OPTIONAL: Deprecated & Removed. Enable only when APIs, flags, config, files, or behaviors were actually deprecated or removed in this release.
Mention replacements when they already exist.
To enable: remove the surrounding comment markers and fill verified items. Otherwise delete this entire block.

## Deprecated & Removed

- {{DEPRECATED_1}}
-->

<!--
OPTIONAL: Maintenance & Dependencies. Enable only for dependency, toolchain, CI, or documentation updates that users or integrators need to know about.
Omit purely internal chore commits.
To enable: remove the surrounding comment markers and fill verified items. Otherwise delete this entire block.

## Maintenance & Dependencies

- {{MAINTENANCE_1}}
-->

<!--
OPTIONAL: Installation & Upgrade. Enable only when the repo has a verified install or upgrade path, or this release attaches real assets.
Write only methods the repository actually supports. The primary command must stay visible — do not wrap it in <details>.
If the real install or upgrade command requires a version argument, use the repository's actual form; do not invent a version pin, and do not add a version heading just to display the tag.
If you could not run the command, say so plainly and mention it in the delivery notes.
If the package or assets are not published yet, leave {{TODO: confirm the install command after this release is published}} rather than pretending it already works.
Never invent a package name, formula, container tag, or download URL.
To enable: remove the surrounding comment markers and fill verified content. Otherwise delete this entire block.

## Installation & Upgrade

{{INSTALLATION_INSTRUCTIONS}}

```bash
{{INSTALL_OR_UPGRADE_COMMAND}}
```
-->

<!--
OPTIONAL: Extra platforms, release assets, or checksums. Fold only secondary material, never the primary install or upgrade command.
Enable only for assets actually attached to this release or published by the project.
If a download URL or SHA256 is unknown, omit that cell or column — do not invent filenames, sizes, or hashes.
To enable: remove the surrounding comment markers and fill verified content. Otherwise delete this entire block.

<details>
<summary>{{DETAILS_SUMMARY}}</summary>

| File | Platform | SHA256 |
|---|---|---|
| [{{ASSET_FILE}}]({{ASSET_DOWNLOAD_URL}}) | {{ASSET_PLATFORM}} | `{{ASSET_SHA256}}` |

</details>
-->

<!--
OPTIONAL: Known Issues. Enable only for limitations or defects confirmed in this release (issues, docs, or maintainer notes). Do not invent a list to look complete.
To enable: remove the surrounding comment markers and fill verified items. Otherwise delete this entire block.

## Known Issues

- {{KNOWN_ISSUE_1}}
-->

<!--
OPTIONAL: Contributors. Enable only for GitHub handles that can be verified as having contributed in this tag range.
Do not invent names or thank people who did not contribute.
To enable: remove the surrounding comment markers and fill verified handles. Otherwise delete this entire block.

## Contributors

Thanks to {{CONTRIBUTORS}} for contributing to this release.
-->

<!--
OPTIONAL: Full Changelog. Enable when a previous tag exists and a compare URL can be verified.
Use a real compare URL (typically https://github.com/<owner>/<repo>/compare/<previous-tag>...<current-tag>). Put the URL in {{COMPARE_URL}}; keep the visible link text as "Full Changelog". Do not repeat version numbers in the body.
Do not invent a range.
For an initial release, delete this block, or replace the link with a real tag or commit-history URL — do not fabricate a previous version, and do not write version numbers into the visible text.
To enable: remove the surrounding comment markers and fill verified links. Otherwise delete this entire block.

## Full Changelog

- [Full Changelog]({{COMPARE_URL}})
-->

---

{{RELEASE_SUMMARY}}

<!-- 用 1–3 句概括。先写用户可见的结果，不要粘贴原始 commit 标题。不要重复写版本号，GitHub 页面已展示 Tag。 -->

<!--
OPTIONAL: 预发布或重要提示。仅在预发布警示、破坏性变更提醒或必须说明的升级注意事项时，使用 GitHub 原生提示块；不要把普通摘要放进提示块。
预发布时，中英文都必须启用 WARNING。其他版本确有警示需求时，只保留一种适用的提示类型。启用时删除注释标记和说明，再填入已核实的文字。不需要则整块删除。

> [!WARNING]
> {{IMPORTANT_WARNING}}

> [!IMPORTANT]
> {{IMPORTANT_NOTE}}
-->

<!--
OPTIONAL: 破坏性变更。仅当本版本确有已在提交、PR 或文档中证实的不兼容改动时启用。
本节紧跟摘要及必要警示。先写清不兼容的改动及影响对象，再给出迁移步骤。
若迁移步骤无法完全核实，保留 {{TODO: ...}} 并在交付说明中列出。
启用：去掉包围的注释标记，填入已核实的条目。不需要则整块删除。

## 破坏性变更

- **{{BREAKING_CHANGE_AREA}}**：{{BREAKING_CHANGE}}

**迁移步骤：**

1. {{MIGRATION_STEP_1}}
2. {{MIGRATION_STEP_2}}
-->

<!--
OPTIONAL: 亮点视觉或演示。仅当本次发布已有真实截图、GIF 或可核实的命令输出时启用。
启用：去掉包围的注释标记，填入已有素材或已核实的输出。不需要则整块删除。
不要编造或生成视觉内容，也不要虚构输出或基准数据。
使用描述性 alt，不要只写“截图”。优先使用项目中已有路径，或项目已在使用的稳定 URL。
展示须保持紧凑，有破坏性变更时放在该节之后。

![{{DEMO_ALT_TEXT}}]({{DEMO_IMAGE_PATH_OR_URL}})
-->

<!--
OPTIONAL: 新增功能。仅当本版本确实落地了用户可见的新能力时启用。
每条写成具体改动与收益，不要写成口号或原始 commit message。若有真实 PR 或 Issue，一并引用。
启用：去掉包围的注释标记，填入已核实的条目。不需要则整块删除。

## 新增功能

- {{ADDED_1}}
- {{ADDED_2}}
-->

<!--
OPTIONAL: 优化与改进。仅当确有行为、性能、体验或可靠性方面的改进时启用。不要编造数据。
启用：去掉包围的注释标记，填入已核实的条目。不需要则整块删除。

## 优化与改进

- {{CHANGED_1}}
- {{CHANGED_2}}
-->

<!--
OPTIONAL: 问题修复。仅当本版本确实修复了缺陷时启用。
写清问题现象与触发条件。若有真实 Issue 或 PR，一并引用。
启用：去掉包围的注释标记，填入已核实的条目。不需要则整块删除。

## 问题修复

- {{FIXED_1}}
- {{FIXED_2}}
-->

<!--
OPTIONAL: 安全修复。仅当确有安全相关修复，或已有公开公告时启用。
只写已核实的影响与修复方式。若有真实公告请给出链接。不要编造 CVE，也不要写利用步骤。
启用：去掉包围的注释标记，填入已核实的条目。不需要则整块删除。

## 安全修复

- {{SECURITY_1}}
-->

<!--
OPTIONAL: 弃用与移除。仅当本版本确实弃用或移除了 API、标志、配置、文件或行为时启用。
若已有替代方案，一并说明。
启用：去掉包围的注释标记，填入已核实的条目。不需要则整块删除。

## 弃用与移除

- {{DEPRECATED_1}}
-->

<!--
OPTIONAL: 维护与依赖更新。仅当依赖、工具链、CI 或文档等维护性变更对使用者或集成方有必要知晓时启用。
纯内部琐碎提交可省略。
启用：去掉包围的注释标记，填入已核实的条目。不需要则整块删除。

## 维护与依赖更新

- {{MAINTENANCE_1}}
-->

<!--
OPTIONAL: 安装与升级。仅当仓库确有安装/升级途径，或本次 Release 附带真实产物时启用。
只写仓库确实支持的方法。默认安装或升级命令必须展开，不要把主命令包进 <details>。
若真实安装或升级命令需要版本参数，使用仓库既有写法；不要编造版本参数，也不要为了展示 Tag 而另加版本号标题。
若未能实际执行这些命令，在此直说，并在交付说明中列出。
若包或附件尚未发布，留下 {{TODO: 待本次发布完成后再确认安装命令}}，不要写成已经可用。
永远不要编造包名、formula、容器标签或下载链接。
启用：去掉包围的注释标记，填入已核实的内容。不需要则整块删除。

## 安装与升级

{{INSTALLATION_INSTRUCTIONS}}

```bash
{{INSTALL_OR_UPGRADE_COMMAND}}
```
-->

<!--
OPTIONAL: 额外平台、发布产物或校验和。只折叠次要内容，不可折叠主安装/升级命令。
仅列出本次 Release 实际附带或项目已发布的产物。
若下载链接或 SHA256 未知，省略该单元格或该列，不要编造文件名、体积或哈希。
启用：去掉包围的注释标记，填入已核实的内容。不需要则整块删除。

<details>
<summary>{{DETAILS_SUMMARY}}</summary>

| 文件 | 平台 | SHA256 |
|---|---|---|
| [{{ASSET_FILE}}]({{ASSET_DOWNLOAD_URL}}) | {{ASSET_PLATFORM}} | `{{ASSET_SHA256}}` |

</details>
-->

<!--
OPTIONAL: 已知问题。仅当本版本已确认仍存在限制或缺陷时启用（来自 Issue、文档或维护者说明）。不要为了显得完整而编造列表。
启用：去掉包围的注释标记，填入已核实的条目。不需要则整块删除。

## 已知问题

- {{KNOWN_ISSUE_1}}
-->

<!--
OPTIONAL: 贡献者。仅当能核实某 GitHub handle 在本 Tag 范围内确有贡献时启用。
不要编造姓名，也不要感谢未参与本版本的人。
启用：去掉包围的注释标记，填入已核实的 handle。不需要则整块删除。

## 贡献者

感谢 {{CONTRIBUTORS}} 对本版本的贡献。
-->

<!--
OPTIONAL: 完整变更日志。仅当上一 Tag 存在，且 Compare URL 可核实时启用。
使用可核对的 Compare 链接（典型形式为 https://github.com/<owner>/<repo>/compare/<上一 Tag>...<当前 Tag>）。把 URL 填入 {{COMPARE_URL}}，可见链接文字保持为“完整变更日志”，不要在正文中重复写版本号。
不要编造对比区间。
若为首次发布：删除本块，或把链接改成真实的 Tag 页 / 提交历史链接，不要虚构上一版本，也不要把版本号写进可见文本。
启用：去掉包围的注释标记，填入已核实的链接。不需要则整块删除。

## 完整变更日志

- [完整变更日志]({{COMPARE_URL}})
-->
