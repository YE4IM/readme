"""Regression checks for rendering bilingual changelog templates."""

import re
import runpy
import unittest
from pathlib import Path


TEMPLATE_DIR = Path(__file__).resolve().parents[1]
CHECK = runpy.run_path(str(TEMPLATE_DIR / "scripts" / "check-release-docs.py"))
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
                "The initial release opens local CSV files for preview in a desktop window.",
                "Preview local CSV files in a desktop window.",
            ),
            (
                "changelog-version-zh-CN-template.md", "CHANGELOG-zh-CN.md",
                "行内存在空字段时，CSV 导出现在也能完成。",
                "导出保留行内空字段，并继续处理剩余数据。",
                "首次发布支持在桌面窗口中打开并预览本地 CSV 文件。",
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


    def test_bilingual_version_content(self):
        en = "## v2 (2026-01-01)\n\nChange.\n\n### Changed\n\n- Default changed. #22"
        zh = "## v2 - 2026-01-01\n\n变更。\n\n### 行为变更\n\n- 默认值调整。 #22"
        check = lambda other: CHECK["check_changelog"]([("en", en), ("zh", other)])
        self.assertEqual(check(zh), [])
        self.assertEqual(check(zh.replace("行为变更", "优化与改进")), [])
        for bad in (zh.split("###")[0], zh.split("\n")[0], zh.replace("#22", "#21"), zh + "\n- 更多"):
            self.assertTrue(check(bad))

    def test_nested_standard_category_must_use_expected_level(self):
        for name in ("Breaking Changes", "破坏性变更"):
            source = f"## v1 - 2026-01-01\nSummary.\n\n#### {name}\n\n- API removed."
            self.assertTrue(CHECK["changelog_entries"](source, draft=False)[1])
            correct = source.replace("####", "###") + "\n\n1. Replace the removed method."
            self.assertFalse(CHECK["changelog_entries"](correct, draft=False)[1])

    def test_date_order_and_formats(self):
        check = lambda text: CHECK["changelog_entries"](text, draft=False)[1]
        first = "## [v2](url) (2026-02-01)\nSummary.\n"
        older = "## v1 - 2026-01-31\nSummary.\n"
        self.assertFalse(check(first + older))
        self.assertFalse(check(first + older.replace("01-31", "02-01")))
        self.assertTrue(check(older + first))
        self.assertTrue(check(first.replace("02-01", "02-30")))
        self.assertIn("unrecognized", check(first.replace("(2026-02-01)", "on 2026-02-01"))[0])
        self.assertIn("needs a version", check(first.replace("(2026-02-01)", ""))[0])
        self.assertIn("needs a version", check(first.replace("(2026-02-01)", "(Feb 1)"))[0])

    def test_version_heading_label_after_either_date_style(self):
        entries = CHECK["changelog_entries"]
        expected = [("v2.0.0-rc.1", "2026-11-24")]
        for heading in ("## v2.0.0-rc.1 - 2026-11-24 Pre-release", "## v2.0.0-rc.1 (2026-11-24) Pre-release",
                        "## [v2.0.0-rc.1](url) (2026-11-24) Pre-release"):
            with self.subTest(heading=heading):
                labels, errors = entries(heading + "\nSummary.", draft=False)
                self.assertEqual(labels, expected)
                # The label is parsed; the only complaint is the missing pre-release warning.
                self.assertEqual(len(errors), 1, errors)
                self.assertTrue(errors[0].startswith(heading[3:]), errors)
        documents = [("en", "## v1 (2026-01-01) Stable\nSummary."), ("zh", "## v1 (2026-01-01) 稳定版\n摘要。")]
        self.assertEqual(CHECK["check_changelog"](documents), [])

    def test_explicit_prerelease_status_requires_warnings_and_bilingual_agreement(self):
        warning = "\n\n> [!WARNING]\n> Testing only."
        for date in ("- 2026-11-25", "(2026-11-25)"):
            en = f"## train-42 {date} Pre-release\n\nSummary."
            zh = f"## train-42 {date} 预发布版\n\n摘要。"
            with self.subTest(date=date):
                self.assertTrue(CHECK["check_changelog"]([("en", en)]))
                self.assertEqual(CHECK["check_changelog"]([("en", en + warning), ("zh", zh + warning)]), [])
                stable = zh.replace("预发布版", "稳定版")
                self.assertTrue(CHECK["check_changelog"]([("en", en + warning), ("zh", stable + warning)]))
                contradictory = en.replace("train-42", "v2.0.0-rc.1").replace("Pre-release", "Stable")
                self.assertTrue(CHECK["check_changelog"]([("en", contradictory + warning)]))
                pending = en.replace("2026-11-25", "{{TODO: verify publication date}}")
                self.assertTrue(CHECK["check_changelog"]([("en", pending)], draft=True))
                self.assertFalse(CHECK["check_changelog"]([("en", pending + warning)], draft=True))
                self.assertTrue(CHECK["check_changelog"]([("en", pending + warning)]))

    def test_unreleased_rejects_a_date_in_plain_and_linked_headings(self):
        for title in ("Unreleased", "未发布", "[Unreleased](https://host/compare/v1...main)"):
            self.assertEqual(CHECK["check_changelog"]([("file", f"## {title}\n\nPending.")]), [])
            for date in ("- 2026-11-25", "(2026-11-25)"):
                with self.subTest(title=title, date=date):
                    source = f"## {title} {date}\n\nPending."
                    self.assertTrue(CHECK["check_changelog"]([("file", source)]))

    def test_template_header_comments_cannot_remain(self):
        for filename in ("changelog-version-template.md", "changelog-version-zh-CN-template.md"):
            template = (TEMPLATE_DIR / filename).read_text(encoding="utf-8")
            comments = COMMENTS.findall(template)
            for comment in comments:
                with self.subTest(filename=filename, comment=comment[:40]):
                    body = f"<!--\n{comment.strip()}\n-->\n\n## v1.9.3 - 2026-11-20\nSummary."
                    self.assertIn("template instructions remain", CHECK["changelog_entries"](body, draft=False)[1])
        self.assertFalse(CHECK["changelog_entries"](
            "## v1.9.3 - 2026-11-20\n<!-- Internal note. -->\nSummary.", draft=False)[1])

    def test_reference_destinations_and_empty_referenced_version(self):
        en = "## [v2] - 2026-01-01\nSummary.\n### Fixed\n- [Patch][file]\n\n[v2]: https://host/compare/a...b\n[file]: https://host/a.zip"
        zh = en.replace("Fixed", "问题修复").replace("Patch", "修复").replace("[file]:", "[FILE]:")
        check = lambda text: CHECK["check_changelog"]([("en", en), ("zh", text)])
        self.assertFalse(check(zh))
        for bad in (zh.replace("a.zip", "b.zip"), zh.replace("/a...b", "/a...c"), zh.replace("[v2]:", "[unused]:"),
                    zh + "\n[V2]: https://host/other"):
            self.assertTrue(check(bad))
        empty = "## [v2] - 2026-01-01\n\n[v2]: https://host/v2"
        self.assertTrue(CHECK["check_changelog"]([("en", empty)]))

    def test_cli_single_pair_and_combined(self):
        import subprocess
        import sys
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as tmp:
            en, zh, combined = [Path(tmp) / name for name in ("en.md", "zh.md", "both.md")]
            source = "## v2 - 2026-02-01\n\nSummary.\n\n~~~md\n---\n~~~"
            en.write_text(source)
            zh.write_text(source.replace("Summary.", "摘要。"))
            combined.write_text(en.read_text() + "\n\n---\n\n" + zh.read_text())
            def run(*args):
                return subprocess.run([sys.executable, "-B", str(TEMPLATE_DIR / "scripts/check-release-docs.py"),
                                       "changelog", *args], capture_output=True, text=True)
            for args in ((en,), (en, zh), (combined, "--bilingual")):
                result = run(*args)
                self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            combined.write_text(en.read_text() + "\n---\n" + zh.read_text().replace("v2", "v3"))
            self.assertNotEqual(run(combined, "--bilingual").returncode, 0)
            # Markdown reference labels are shared by the entire bilingual document.
            release = "## [v2] - 2026-02-01\nSummary.\n"
            combined.write_text(release + "\n---\n" + release + "\n[v2]: https://host/tag/v2")
            self.assertEqual(run(combined, "--bilingual").returncode, 0)
            combined.write_text(combined.read_text().replace("---", "[V2]: https://host/other\n\n---"))
            self.assertNotEqual(run(combined, "--bilingual").returncode, 0)


if __name__ == "__main__":
    unittest.main()
