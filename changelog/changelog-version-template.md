<!--
Reusable template: one published-version section for a repository CHANGELOG (English).
Fill only verified facts, then paste the section into CHANGELOG.md or the repo's existing English changelog file.
Do not copy this filename into the changelog body.
To enable an OPTIONAL block: remove the surrounding comment markers, keep the section content, and delete the instruction text. Otherwise delete the entire block (including any empty heading).
Remove all editorial TODOs and template fields from publishable copy. Keep {{TODO: ...}} only in a draft marked as pending verification.
The version heading defaults to plain text. Follow existing inline links or reference definitions and verify the destination. Keep the comparison link in one place. Use the publication event and time zone defined in the guide.
Local anchors and official translated docs may use equivalent destinations.
Follow changelog-agent-instructions.md in this directory for scope, evidence, bilingual alignment, and cleanup rules.
Group by the verified publication date, newest first; entries published on the same local day may retain project order.
-->

## {{VERSION}} - {{RELEASE_DATE}}

{{RELEASE_SUMMARY}}

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
OPTIONAL: Breaking changes. Place this directly after the summary and any required warning.
Fill the migration field with one or more numbered steps. If migration steps cannot be verified, fill the migration field with {{TODO: ...}} in the draft and list it in the delivery notes.

### Breaking Changes

- **{{BREAKING_CHANGE_AREA}}**: {{BREAKING_CHANGE}}

**Migration:**

{{MIGRATION_STEPS}}
-->

<!--
OPTIONAL: User-visible capabilities that shipped in this version.

### Added

- {{ADDED_1}}
-->

<!--
OPTIONAL: Verified changes to behavior, performance, usability, or reliability. Use measured data where available.

### Changed

- {{CHANGED_1}}
-->

<!--
OPTIONAL: Verified fixes. Describe the symptoms and conditions, and cite the relevant issue or PR when available.

### Fixed

- {{FIXED_1}}
-->

<!--
OPTIONAL: Verified security fixes or advisories cleared for disclosure. Use impact, fix versions, and links that maintainers have published or explicitly approved.

### Security

- {{SECURITY_1}}
-->

<!--
OPTIONAL: Verified deprecations or removals.

### Deprecated & Removed

- {{DEPRECATED_1}}
-->

<!--
OPTIONAL: Maintenance changes that users or integrators need to know about.

### Maintenance & Dependencies

- {{MAINTENANCE_1}}
-->

<!--
OPTIONAL: Installation or upgrade instructions. Use a verified download or store link, numbered steps, or fenced commands with the correct language. Keep the primary path visible and label commands you could not run.

### Installation & Upgrade

{{INSTALLATION_INSTRUCTIONS}}
-->

<!--
OPTIONAL: Confirmed open issues affecting this version.

### Known Issues

- {{KNOWN_ISSUE_1}}
-->

<!--
OPTIONAL: Verified contributor handles for this version.

### Contributors

Thanks to {{CONTRIBUTORS}} for contributing to this release.
-->

<!--
OPTIONAL: Use a verified comparison against the comparable baseline selected under section 4 for the same package, release line or stable upgrade path.
Typical URL: https://github.com/<owner>/<repo>/compare/<previous-tag>...<current-tag>
Omit this section if the heading already links to the comparison or this is the first release.

### Full Changelog

- [Full Changelog]({{COMPARE_URL}})
-->
