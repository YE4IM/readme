<!--
Release title (separate GitHub field): use the actual release identifier by default, such as v2.0.0-rc.1 or v2.0.0. Follow an established project title convention and retain the pre-release identity.
Start directly with the English release summary. Do not add a project-name or version-number heading, a date/type line, a previous-release line, "English" / "中文" headings, or in-page language-switch links: the GitHub Release page already shows the title and tag.
Write the full English notes first, then a --- separator, then the full Chinese notes.
Keep the opening compact so the summary and any breaking changes stay close.
Keep compatibility, migration, security, and command versions where they carry verified information. Report copy readiness and publication status separately outside the body. Mark the delivery as a draft if key copy facts are missing. Remove editorial TODOs from publishable copy. Local anchors and official translated docs may use equivalent destinations.
-->

{{RELEASE_SUMMARY}}

<!-- Use one short sentence to state the main feature or fix users will notice. Do not paste raw commit subjects. Do not repeat the version number; GitHub already displays the tag. -->

<!--
OPTIONAL: Pre-release warning. Enable WARNING in both languages for a pre-release. Explain the testing purpose and the production guidance.

> [!WARNING]
> {{IMPORTANT_WARNING}}
-->

<!--
OPTIONAL: Stable release upgrade notice. Enable IMPORTANT in both languages when users need a breaking-change or upgrade caution first.

> [!IMPORTANT]
> {{IMPORTANT_NOTE}}
-->

<!--
OPTIONAL: Breaking Changes. Enable only when this release contains incompatible changes verified in commits, PRs, or docs.
Place this section immediately after the summary and any required alert. Explain what changed incompatibly and who is affected, then give migration steps.
Fill the migration field with one or more numbered steps. If migration steps cannot be fully verified, fill the migration field with {{TODO: ...}} and mention it in the delivery notes.
To enable: remove the surrounding comment markers and fill verified items. Otherwise delete this entire block.

## Breaking Changes

- **{{BREAKING_CHANGE_AREA}}**: {{BREAKING_CHANGE}}

**Migration:**

{{MIGRATION_STEPS}}
-->

<!--
OPTIONAL: Highlights visual or demo. Enable only if this release already has a real screenshot, GIF, or verified command output.
To enable: remove the surrounding comment markers and fill with existing assets or verified output. Otherwise delete this entire block.
Do not invent or generate a visual, and do not fabricate output or benchmark numbers.
Use descriptive alt text. Check images and documentation links in the target release preview. If preview is unavailable, prefer verified URLs pinned to the release tag or commit, or verified release attachments.
This is not a change category. Keep the heading. Place it after Breaking Changes when that section is present, and before any other change category. Otherwise place it after the summary and any required alert. Enable it in both languages with the same image.

## Highlights

![{{DEMO_ALT_TEXT}}]({{DEMO_IMAGE_PATH_OR_URL}})
-->

<!--
OPTIONAL: Added. Enable only for user-visible capabilities that actually landed in this release.
Write each item as a concrete change and benefit, not a slogan or a raw commit message. Cite a real PR or issue when one exists.
To enable: remove the surrounding comment markers and fill verified items. Otherwise delete this entire block.

## Added

- {{ADDED_1}}
-->

<!--
OPTIONAL: Changed. Enable only for verified changes in user-visible behavior, including neutral changes to defaults or output order, or documented improvements. Do not invent metrics.
To enable: remove the surrounding comment markers and fill verified items. Otherwise delete this entire block.

## Changed

- {{CHANGED_1}}
-->

<!--
OPTIONAL: Fixed. Enable only for defects that were actually fixed in this release.
Describe the symptom and when it happened. Cite a real issue or PR when one exists.
To enable: remove the surrounding comment markers and fill verified items. Otherwise delete this entire block.

## Fixed

- {{FIXED_1}}
-->

<!--
OPTIONAL: Security. Enable only for verified fixes or advisories with public disclosure clearance. Use details and links already published or explicitly approved by the maintainers.
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
Write only methods the repository actually supports. Keep the primary path visible. Use a fenced command, a download or store link, numbered steps, or a combination. If an installer is the only upgrade path, show its download link here.
If the real install or upgrade command requires a version argument, use the repository's actual form; do not invent a version pin, and do not add a version heading just to display the tag.
If you could not run the command, say so plainly and mention it in the delivery notes.
If the package or assets are not published yet, leave {{TODO: confirm the install command after this release is published}} rather than pretending it already works.
Never invent a package name, formula, container tag, or download URL.
To enable: remove the surrounding comment markers and fill verified content. Otherwise delete this entire block.

## Installation & Upgrade

{{INSTALLATION_INSTRUCTIONS}}
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
OPTIONAL: Full Changelog. Enable when both endpoints and the compare URL match the baseline in section 7 of the guide for the same package and release line or documented stable upgrade path.
Use a real compare URL (typically https://github.com/<owner>/<repo>/compare/<previous-tag>...<current-tag>). Put the URL in {{COMPARE_URL}}; keep the visible link text as "Full Changelog". Use version numbers where they carry substantive information.
Do not invent a range.
For an initial release, delete this block, or replace the link with a real tag or commit-history URL — do not fabricate a previous version, and do not write version numbers into the visible text.
To enable: remove the surrounding comment markers and fill verified links. Otherwise delete this entire block.

## Full Changelog

- [Full Changelog]({{COMPARE_URL}})
-->

---

<!-- GitHub 标题默认用真实发布标识，如 v2.0.0-rc.1。按项目标题惯例保留预发布身份。正文保留兼容、迁移、安全和命令所需的真实版本号。交付说明分列文案状态和发布状态。可发布成稿须清除编辑用 TODO。本页锚点和官方译版文档可使用等价地址。 -->

{{RELEASE_SUMMARY}}

<!-- 用一句短句概括本次最重要的功能或修复，直接写出用户可见的变化，不要粘贴原始 commit 标题。不要重复写版本号，GitHub 页面已展示 Tag。 -->

<!--
OPTIONAL: 预发布警示。预发布时，中英文都启用 WARNING，说明测试用途及生产环境使用建议。

> [!WARNING]
> {{IMPORTANT_WARNING}}
-->

<!--
OPTIONAL: 正式版升级提示。确需优先提示破坏性变更或升级注意事项时，中英文都启用 IMPORTANT。

> [!IMPORTANT]
> {{IMPORTANT_NOTE}}
-->

<!--
OPTIONAL: 破坏性变更。仅当本版本确有已在提交、PR 或文档中证实的不兼容改动时启用。
本节紧跟摘要及必要警示。先写清不兼容的改动及影响对象，再给出迁移步骤。
迁移字段填写一条或多条编号步骤。若迁移步骤无法完全核实，在迁移字段保留 {{TODO: ...}} 并在交付说明中列出。
启用：去掉包围的注释标记，填入已核实的条目。不需要则整块删除。

## 破坏性变更

- **{{BREAKING_CHANGE_AREA}}**：{{BREAKING_CHANGE}}

**迁移步骤：**

{{MIGRATION_STEPS}}
-->

<!--
OPTIONAL: 亮点视觉或演示。仅当本次发布已有真实截图、GIF 或可核实的命令输出时启用。
启用：去掉包围的注释标记，填入已有素材或已核实的输出。不需要则整块删除。
不要编造或生成视觉内容，也不要虚构输出或基准数据。
使用描述性 alt。在目标 Release 预览中核对图片与文档链接；无预览时优先使用固定到该版 Tag 或提交的已核实地址，或该版附件链接。
这不是变更分类。保留下面的标题。有破坏性变更时放在该节之后、其他变更分类之前；否则放在摘要和必要警示之后。两侧都启用时使用同一张图。

## 亮点展示

![{{DEMO_ALT_TEXT}}]({{DEMO_IMAGE_PATH_OR_URL}})
-->

<!--
OPTIONAL: 新增功能。仅当本版本确实落地了用户可见的新能力时启用。
每条写成具体改动与收益，不要写成口号或原始 commit message。若有真实 PR 或 Issue，一并引用。
启用：去掉包围的注释标记，填入已核实的条目。不需要则整块删除。

## 新增功能

- {{ADDED_1}}
-->

<!--
OPTIONAL: 行为变更。仅当确有用户可观察的行为变化，或有证据的性能、体验或可靠性改进时启用。不要编造数据。
启用：去掉包围的注释标记，填入已核实的条目。不需要则整块删除。

## 行为变更

- {{CHANGED_1}}
-->

<!--
OPTIONAL: 问题修复。仅当本版本确实修复了缺陷时启用。
写清问题现象与触发条件。若有真实 Issue 或 PR，一并引用。
启用：去掉包围的注释标记，填入已核实的条目。不需要则整块删除。

## 问题修复

- {{FIXED_1}}
-->

<!--
OPTIONAL: 安全修复。仅当修复或公告已核实且有公开披露依据时启用；使用维护者已公开或明确批准的细节和链接。
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
只写仓库确实支持的方法。主安装或升级路径必须展开。按渠道填写带围栏的命令、下载或商店链接、编号步骤，也可组合。若安装包是唯一升级途径，在此列主下载链接。
若真实安装或升级命令需要版本参数，使用仓库既有写法；不要编造版本参数，也不要为了展示 Tag 而另加版本号标题。
若未能实际执行这些命令，在此直说，并在交付说明中列出。
若包或附件尚未发布，留下 {{TODO: 待本次发布完成后再确认安装命令}}，不要写成已经可用。
永远不要编造包名、formula、容器标签或下载链接。
启用：去掉包围的注释标记，填入已核实的内容。不需要则整块删除。

## 安装与升级

{{INSTALLATION_INSTRUCTIONS}}
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
OPTIONAL: 完整变更日志。仅当起止引用和 Compare URL 均符合规范第 7 节时启用，核对同一包的发布线或既定稳定版升级路径。
使用可核对的 Compare 链接（典型形式为 https://github.com/<owner>/<repo>/compare/<上一 Tag>...<当前 Tag>）。把 URL 填入 {{COMPARE_URL}}，可见链接文字保持为“完整变更日志”。
不要编造对比区间。
若为首次发布：删除本块，或把链接改成真实的 Tag 页 / 提交历史链接，不要虚构上一版本，也不要把版本号写进可见文本。
启用：去掉包围的注释标记，填入已核实的链接。不需要则整块删除。

## 完整变更日志

- [完整变更日志]({{COMPARE_URL}})
-->
