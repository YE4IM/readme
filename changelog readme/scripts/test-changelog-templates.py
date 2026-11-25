"""Regression checks for rendering bilingual changelog templates."""

import re
import runpy
import unittest
from pathlib import Path


TEMPLATE_DIR = Path(__file__).resolve().parents[1]
CHECK = runpy.run_path(str(TEMPLATE_DIR.parent / "scripts" / "check-release-docs.py"))
COMMENTS = re.compile(r"<!--(.*?)-->", re.DOTALL)
PLACEHOLDERS = re.compile(r"\{\{([A-Z0-9_]+)\}\}")
SHARED_FACTS = {
    "VERSION": "v2.0.0-rc.1",
    "RELEASE_DATE": "2026-11-24",
    "BREAKING_CHANGE_AREA": "CLI",
}


def render_template(template, facts):
    def render_comment(match):
        comment = match[1].strip()
        if not comment.startswith("OPTIONAL:"):
            return ""
        _, _, body = comment.partition("\n\n")
        names = PLACEHOLDERS.findall(body)
        return body if names and facts.keys() >= set(names) else ""

    document = COMMENTS.sub(render_comment, template)
    document = PLACEHOLDERS.sub(lambda match: facts[match[1]], document)
    return re.sub(r"\n{3,}", "\n\n", document).strip()


class ChangelogTemplateTests(unittest.TestCase):
    def test_changelog_optional_sections_are_paired_and_self_contained(self):
        signatures = []
        for filename in ("changelog-version-template.md", "changelog-version-zh-CN-template.md"):
            with self.subTest(filename=filename):
                template = (TEMPLATE_DIR / filename).read_text(encoding="utf-8")
                visible = COMMENTS.sub("", template)
                self.assertEqual(
                    visible.strip(),
                    "## {{VERSION}} - {{RELEASE_DATE}}\n\n{{RELEASE_SUMMARY}}",
                )
                blocks = [
                    comment.strip().partition("\n\n")[2]
                    for comment in COMMENTS.findall(template)
                    if comment.strip().startswith("OPTIONAL:")
                ]
                self.assertEqual(len(blocks), 13)
                self.assertTrue(blocks[0].startswith("> [!WARNING]\n"))
                self.assertTrue(blocks[1].startswith("> [!IMPORTANT]\n"))
                self.assertTrue(all(block.startswith("### ") for block in blocks[2:]))
                self.assertTrue(all(PLACEHOLDERS.search(block) for block in blocks))
                signatures.append([PLACEHOLDERS.findall(block) for block in blocks])
        self.assertEqual(*signatures)

    def test_patch_and_first_release_match_the_bilingual_examples(self):
        cases = (
            (
                "changelog-version-template.md", "CHANGELOG.md",
                "CSV exports now finish when a row contains an empty field.",
                "Keep empty fields in the exported row without stopping the export.",
                "You can open local CSV files for preview in the first release of this line.",
                "Preview local CSV files in a desktop window.",
            ),
            (
                "changelog-version-zh-CN-template.md", "CHANGELOG-zh-CN.md",
                "行内存在空字段时，CSV 导出现在也能完成。",
                "导出保留行内空字段，并继续处理剩余数据。",
                "这条发布线的首个版本支持打开并预览本地 CSV 文件。",
                "在桌面窗口中预览本地 CSV 文件。",
            ),
        )
        compare = "https://example.com/example/compare/v1.9.3...v1.9.4"
        for template_name, sample_name, patch_summary, fix, initial_summary, addition in cases:
            with self.subTest(sample=sample_name):
                template = (TEMPLATE_DIR / template_name).read_text(encoding="utf-8")
                sample = (TEMPLATE_DIR / "examples" / sample_name).read_text(encoding="utf-8")
                patch = render_template(template, {
                    "VERSION": "v1.9.4", "RELEASE_DATE": "2026-11-25",
                    "RELEASE_SUMMARY": patch_summary, "FIXED_1": fix, "COMPARE_URL": compare,
                })
                initial = render_template(template, {
                    "VERSION": "v1.9.3", "RELEASE_DATE": "2026-11-20",
                    "RELEASE_SUMMARY": initial_summary, "ADDED_1": addition,
                })
                unreleased, published = sample.split("## v1.9.4", 1)
                self.assertEqual("## v1.9.4" + published.strip("\n"), f"{patch}\n\n{initial}")
                self.assertIn("## Unreleased\n", unreleased)
                self.assertNotIn(fix, unreleased)
                self.assertNotIn("/compare/", initial)
                self.assertNotIn("[!WARNING]", published)
                self.assertFalse(any(token in sample for token in ("{{", "<!--")))

    def test_prerelease_warning_and_migration_order(self):
        for language, filename, heading, summary, warning, change, steps in (
            (
                "en", "changelog-version-template.md", "Breaking Changes",
                "The CLI now uses the new output flag.",
                "This pre-release is for testing and feedback. Avoid production use.",
                "Scripts using `--format` must switch flags.",
                ("Rename `--format` to `--output`.", "Run `example --output json`."),
            ),
            (
                "zh-CN", "changelog-version-zh-CN-template.md", "破坏性变更",
                "CLI 现已使用新的输出参数。",
                "本预发布版用于测试与反馈，不建议在生产环境使用。",
                "使用 `--format` 的脚本需要更换参数。",
                ("将 `--format` 改为 `--output`。", "运行 `example --output json`。"),
            ),
        ):
            facts = {
                **SHARED_FACTS,
                "RELEASE_SUMMARY": summary,
                "IMPORTANT_WARNING": warning,
                "BREAKING_CHANGE": change,
                "MIGRATION_STEPS": "\n".join(f"{n}. {step}" for n, step in enumerate(steps, 1)),
            }
            with self.subTest(language=language):
                template = (TEMPLATE_DIR / filename).read_text(encoding="utf-8")
                rendered = render_template(template, facts)
                expected = [
                    summary,
                    f"> [!WARNING]\n> {warning}",
                    f"### {heading}",
                    change,
                    f"1. {steps[0]}",
                    f"2. {steps[1]}",
                ]
                positions = [rendered.index(item) for item in expected]
                self.assertEqual(positions, sorted(positions))
                headings = re.findall(r"^#{2,3} .+$", rendered, re.MULTILINE)
                expected_headings = [f"### {heading}"]
                expected_headings.insert(
                    0, f'## {facts["VERSION"]} - {facts["RELEASE_DATE"]}'
                )
                self.assertEqual(headings, expected_headings)
                for residue in ("<!--", "{{", "OPTIONAL:", "[!IMPORTANT]"):
                    self.assertNotIn(residue, rendered)

    def test_installation_accepts_download_steps_without_a_shell(self):
        for path in sorted(TEMPLATE_DIR.glob("changelog-version*-template.md")):
            steps = "1. [Download the installer](https://example.com/installer).\n2. Open it."
            rendered = render_template(path.read_text(encoding="utf-8"), {
                "VERSION": "v1.0.0", "RELEASE_DATE": "2026-11-25",
                "RELEASE_SUMMARY": "The desktop app is available.",
                "INSTALLATION_INSTRUCTIONS": steps,
            })
            self.assertIn(steps, rendered)
            self.assertNotIn(chr(96) * 3, rendered)

    def test_stable_alert_single_step_and_pending_migration(self):
        templates = [path.read_text(encoding="utf-8") for path in sorted(TEMPLATE_DIR.glob("changelog-version*-template.md"))]
        for template in templates:
            for migration in ("1. Use the new option.", "{{TODO: Verify the replacement option.}}"):
                with self.subTest(migration=migration):
                    rendered = render_template(template, {
                        "VERSION": "v2.0.0", "RELEASE_DATE": "2026-11-26", "RELEASE_SUMMARY": "The CLI uses a new flag.",
                        "IMPORTANT_NOTE": "Review the CLI flags before upgrading.",
                        "BREAKING_CHANGE_AREA": "CLI",
                        "BREAKING_CHANGE": "Existing scripts need an update.",
                        "MIGRATION_STEPS": migration,
                    })
                    self.assertIn("> [!IMPORTANT]", rendered)
                    self.assertNotIn("[!WARNING]", rendered)
                    self.assertIn("Existing scripts need an update.", rendered)
                    self.assertIn(migration, rendered)


    def test_rc_history_preserves_maintenance_range_and_uses_rc_delta(self):
        documents = [
            (TEMPLATE_DIR / "examples" / name).read_text(encoding="utf-8")
            for name in ("CHANGELOG-rc-history.md", "CHANGELOG-rc-history-zh-CN.md")
        ]
        self.assertEqual(
            CHECK["changelog_entries"](documents[0], draft=False),
            CHECK["changelog_entries"](documents[1], draft=False),
        )
        labels, errors = CHECK["changelog_entries"](documents[0], draft=False)
        self.assertEqual(errors, [])
        self.assertEqual(labels[0], ("v2.0.0", "2026-11-26"))
        for document in documents:
            stable, patch, rc, _ = re.split(r"(?m)^## ", document)[1:]
            self.assertIn("/compare/v2.0.0-rc.1...v2.0.0)", stable)
            self.assertIn("/releases/tag/v2.0.0)", stable)
            self.assertNotIn("--format", stable)
            self.assertIn("/compare/v1.9.3...v1.9.4)", patch)
            self.assertIn("--format", rc)
        broken_date = documents[0].replace("2026-11-26", "2026-11-31")
        self.assertTrue(CHECK["changelog_entries"](broken_date, draft=False)[1])


    def test_rc_examples_link_to_each_other_below_the_title(self):
        names = ("CHANGELOG-rc-history.md", "CHANGELOG-rc-history-zh-CN.md")
        for name, labels in zip(names, (("**English**", "中文"), ("English", "**中文**"))):
            lines = (TEMPLATE_DIR / "examples" / name).read_text(encoding="utf-8").splitlines()
            switch = " | ".join(f"[{label}](./{target})" for label, target in zip(labels, names))
            self.assertEqual(next(line for line in lines[1:] if line.strip()), switch)

    def test_duplicate_version_with_different_date_and_heading_style(self):
        text = "## [v1](url) - 2026-11-25\nA\n## v1 - 2026-11-24\nB"
        entries, errors = CHECK["changelog_entries"](text, draft=False)
        self.assertEqual(entries, [("v1", "2026-11-25"), ("v1", "2026-11-24")])
        self.assertTrue(any("duplicate" in error for error in errors))

    def test_linked_unreleased_must_come_first(self):
        published = "## v1 - 2026-11-25\nFix.\n"
        for name in ("Unreleased", "未发布"):
            pending = f"## [{name}](https://example.com/compare/v1...main)\nChanges.\n"
            check = CHECK["changelog_entries"]
            self.assertEqual(check(pending + published, draft=False),
                             (["Unreleased", ("v1", "2026-11-25")], []))
            self.assertIn("Unreleased must be the first CHANGELOG entry",
                          check(published + pending, draft=False)[1])

    def test_changelog_example_fields_use_the_changelog_template(self):
        sample = "## Unreleased\n\n~~~text\n{{USER_ID}}\n~~~"
        check = CHECK["changelog_entries"]
        self.assertEqual(check(sample, draft=False)[1], [])
        self.assertTrue(check(sample.replace("USER_ID", "RELEASE_DATE"), draft=True)[1])
        self.assertTrue(check(sample.replace("USER_ID", "TODO"), draft=False)[1])


if __name__ == "__main__":
    unittest.main()
