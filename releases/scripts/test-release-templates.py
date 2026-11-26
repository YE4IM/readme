"""Regression checks for rendering bilingual release templates."""

import re
import runpy
import unittest
from pathlib import Path


TEMPLATE_DIR = Path(__file__).resolve().parents[1]
CHECK = runpy.run_path(str(TEMPLATE_DIR / "scripts" / "check-release-docs.py"))
COMMENTS = re.compile(r"<!--(.*?)-->", re.DOTALL)
PLACEHOLDERS = re.compile(r"\{\{([A-Z0-9_]+)\}\}")
TEMPLATE = (TEMPLATE_DIR / "release-template.md").read_text(encoding="utf-8")
SHARED_FACTS = {
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


class ReleaseTemplateTests(unittest.TestCase):
    def assert_example(self, name, english, chinese):
        halves = [
            render_template(template, facts)
            for template, facts in zip(TEMPLATE.split("\n---\n"), (english, chinese))
        ]
        rendered = "\n\n---\n\n".join(halves)
        sample = (TEMPLATE_DIR / "examples" / f"{name}.md").read_text(encoding="utf-8")
        self.assertEqual(rendered, sample.strip())
        self.assertEqual(CHECK["check_release"](sample), [])
        self.assertNotIn("[!WARNING]", rendered)
        self.assertNotIn("{{", rendered)
        self.assertNotIn("<!--", rendered)

    def test_stable_patch_only_enables_fixed_and_real_compare(self):
        compare = "https://example.com/example/compare/v1.9.3...v1.9.4"
        self.assert_example(
            "patch",
            {"RELEASE_SUMMARY": "CSV exports now finish when a row contains an empty field.",
             "FIXED_1": "Keep empty fields in the exported row without stopping the export.",
             "COMPARE_URL": compare},
            {"RELEASE_SUMMARY": "行内存在空字段时，CSV 导出现在也能完成。",
             "FIXED_1": "导出保留行内空字段，并继续处理剩余数据。",
             "COMPARE_URL": compare},
        )

    def test_initial_release_uses_visible_download_steps_without_compare(self):
        download = "https://example.com/example/releases/v1.9.3/example-installer"
        self.assert_example(
            "initial",
            {"RELEASE_SUMMARY": "The first desktop release opens CSV files for preview.",
             "ADDED_1": "Preview local CSV files in a desktop window.",
             "INSTALLATION_INSTRUCTIONS": (
                 f"1. [Download the desktop installer]({download}).\n"
                 "2. Open the installer and follow the prompts."
             )},
            {"RELEASE_SUMMARY": "首个桌面版本支持打开并预览 CSV 文件。",
             "ADDED_1": "在桌面窗口中预览本地 CSV 文件。",
             "INSTALLATION_INSTRUCTIONS": (
                 f"1. [下载桌面安装包]({download})。\n"
                 "2. 打开安装包并按提示安装。"
             )},
        )
        text = (TEMPLATE_DIR / "examples" / "initial.md").read_text(encoding="utf-8")
        self.assertNotIn("/compare/", text)
        self.assertNotIn("<details>", text)
        self.assertNotIn("```", text)

    def test_prerelease_warning_and_migration_precede_release_screenshot(self):
        english_release, chinese_release = TEMPLATE.split("\n---\n")
        for language, template, heading, summary, warning, change, steps in (
            (
                "en", english_release, "Breaking Changes",
                "The CLI now uses the new output flag.",
                "This pre-release is for testing and feedback. Avoid production use.",
                "Scripts using `--format` must switch flags.",
                ("Rename `--format` to `--output`.", "Run `example --output json`."),
            ),
            (
                "zh-CN", chinese_release, "破坏性变更",
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
                screenshot = "https://example.com/example/blob/v2.0.0-rc.1/docs/output-preview.png"
                facts.update(DEMO_ALT_TEXT=summary, DEMO_IMAGE_PATH_OR_URL=screenshot)
                rendered = render_template(template, facts)
                expected = [
                    summary,
                    f"> [!WARNING]\n> {warning}",
                    f"## {heading}",
                    change,
                    f"1. {steps[0]}",
                    f"2. {steps[1]}",
                ]
                expected.append(f"![{summary}]({screenshot})")
                positions = [rendered.index(item) for item in expected]
                self.assertEqual(positions, sorted(positions))
                headings = re.findall(r"^#{2,3} .+$", rendered, re.MULTILINE)
                highlight = "## Highlights" if language == "en" else "## 亮点展示"
                expected_headings = [f"## {heading}", highlight]
                self.assertEqual(headings, expected_headings)
                self.assertLess(rendered.index(f"## {heading}"), rendered.index(highlight))
                for residue in ("<!--", "{{", "OPTIONAL:", "[!IMPORTANT]"):
                    self.assertNotIn(residue, rendered)

    def test_stable_alert_single_step_and_pending_migration(self):
        templates = TEMPLATE.split("\n---\n")
        for template in templates:
            for migration in ("1. Use the new option.", "{{TODO: Verify the replacement option.}}"):
                with self.subTest(migration=migration):
                    rendered = render_template(template, {
                        "RELEASE_SUMMARY": "The CLI uses a new flag.",
                        "IMPORTANT_NOTE": "Review the CLI flags before upgrading.",
                        "BREAKING_CHANGE_AREA": "CLI",
                        "BREAKING_CHANGE": "Existing scripts need an update.",
                        "MIGRATION_STEPS": migration,
                    })
                    self.assertIn("> [!IMPORTANT]", rendered)
                    self.assertNotIn("[!WARNING]", rendered)
                    self.assertIn("Existing scripts need an update.", rendered)
                    self.assertIn(migration, rendered)


    def test_stable_release_uses_stable_baseline_and_keeps_rc_migration(self):
        sample = (TEMPLATE_DIR / "examples" / "stable-after-rc.md").read_text(encoding="utf-8")
        halves = sample.split("\n---\n")
        self.assertEqual(len(halves), 2)
        for half in halves:
            self.assertIn("/compare/v1.9.3...v2.0.0)", half)
            self.assertNotIn("/compare/v1.9.4...v2.0.0)", half)
            self.assertNotIn("/compare/v2.0.0-rc.1...v2.0.0)", half)
            self.assertIn("1. ", half)
            self.assertIn("--format", half)
            self.assertIn("--output", half)
        self.assertEqual(CHECK["check_release"](sample), [])
        without_migration = re.sub(r"(?m)^1\. .*$", "", sample)
        self.assertEqual(len(CHECK["check_release"](without_migration)), 2)
        self.assertTrue(CHECK["check_release"](sample, prerelease=True))


    def test_equivalent_links_guidance_preserves_the_language_switch_rule(self):
        guide = (TEMPLATE_DIR / "release-agent-instructions.md").read_text(encoding="utf-8")
        rule = next(line for line in guide.splitlines() if "等价地址" in line)
        self.assertNotIn("语言切换", rule)
        self.assertIn("本页锚点", rule)
        self.assertIn("本地化文档", rule)

    def test_wrong_heading_levels_cannot_hide_missing_migration(self):
        sample = (TEMPLATE_DIR / "examples" / "stable-after-rc.md").read_text(encoding="utf-8")
        invalid = re.sub(r"(?m)^1\. .*$", "", sample.replace("## ", "### "))
        errors = CHECK["check_release"](invalid)
        for language in ("English", "Chinese"):
            self.assertIn(f"{language} release sections must use level-two headings", errors)

    def test_code_examples_allow_literal_fields_and_check_editorial_fields(self):
        for example in ("`{{USER_ID}}`", "```text\n{{USER_ID}}\n```"):
            half = "Summary.\n\n" + example
            body = half + "\n\n---\n\n" + half
            check = CHECK["check_release"]
            self.assertEqual(check(body), [])
            self.assertTrue(check(body.replace("USER_ID", "ADDED_1"), draft=True))
            todo = body.replace("USER_ID", "TODO: verify")
            self.assertTrue(check(todo))
            self.assertEqual(check(todo, draft=True), [])
        self.assertTrue(check("Summary {{USER_ID}}\n\n---\n\n摘要"))


    def test_visible_warning_immediately_follows_summary(self):
        check = CHECK["check_release"]
        warning = "> [!WARNING]\n> Testing only."
        for block in (warning, "<!--\n" + warning + "\n-->", "> [!WARNING]\n>", "## Added\n\n- Item\n\n" + warning,
                      "```md\n" + warning + "\n```", "```sh\necho ok\n```\n\n" + warning):
            half = "Summary.\n\n" + block
            self.assertEqual(bool(check(half + "\n---\n" + half, prerelease=True)), block != warning, block)

    def test_inline_literals_and_chinese_issue_boundaries(self):
        en = "Fixed `<!--` handling.\n\n## Fixed\n\n- Fix #12 in parser."
        zh = "改进行内标记解析。\n\n## 问题修复\n\n- 修复#12中的问题。"
        check = CHECK["check_release"]
        self.assertFalse(check(en + "\n---\n" + zh))
        self.assertTrue(check(en + "\n---\n" + zh.replace("#12", "#13")))
        self.assertFalse(check(en.replace("#12", "team/repo#12") + "\n---\n" + zh.replace("#12", "team/repo#12")))

    def test_bilingual_categories_counts_references_and_assets(self):
        en = "Fixed export.\n\n## Fixed\n\n- Export. #12\n\n## Installation & Upgrade\n\n1. [Download](https://host/v1/tool.zip)"
        zh = "修复导出。\n\n## 问题修复\n\n- 导出。 #12\n\n## 安装与升级\n\n1. [下载](https://host/v1/tool.zip)"
        check = lambda chinese: CHECK["check_release"](en + "\n---\n" + chinese)
        self.assertEqual(check(zh), [])
        for bad in (zh.replace("问题修复", "新增功能"), zh.replace("#12", "#39"),
                    zh.replace("#12", "#12\n- 其他"), zh.replace("/v1/", "/v2/")):
            self.assertTrue(check(bad), bad)
        en += "\n\n[Migration](https://host/docs/en/guide)"
        self.assertEqual(check(zh + "\n\n[迁移](https://host/docs/zh/guide)"), [])


    def test_highlight_image_must_match_on_both_sides(self):
        en = "Shipped.\n\n## Highlights\n\n![Demo](https://host/demo.png)\n\n## Fixed\n\n- Export."
        zh = "已发布。\n\n## 亮点展示\n\n![演示](https://host/demo.png)\n\n## 问题修复\n\n- 导出。"
        check = CHECK["check_release"]
        self.assertEqual(check(en + "\n---\n" + zh), [])
        self.assertTrue(check(en + "\n---\n" + zh.replace("https://host/demo.png", "")))
        self.assertTrue(check(en + "\n---\n" + "已发布。\n\n## 问题修复\n\n- 导出。"))

    def test_version_heading_accepts_a_label_after_either_date_style(self):
        entries = CHECK["changelog_entries"]
        expected = ([("v2.0.0", "2026-11-26")], [])
        for heading in ("## v2.0.0 - 2026-11-26 Stable", "## v2.0.0 (2026-11-26) Stable",
                        "## v2.0.0 (2026-11-26)", "## v2.0.0 - 2026-11-26"):
            with self.subTest(heading=heading):
                self.assertEqual(entries(heading + "\nSummary.", draft=False), expected)
        self.assertIn("invalid calendar date",
                      entries("## v2.0.0 (2026-02-30) Stable\nSummary.", draft=False)[1][0])

    def test_note_alerts_are_compared_between_languages(self):
        check = CHECK["check_release"]
        note = "Summary.\n\n> [!NOTE]\n> Read this first.\n\n## Fixed\n\n- Export."
        plain = "摘要。\n\n## 问题修复\n\n- 导出。"
        self.assertTrue(check(note + "\n---\n" + plain))
        both = note + "\n---\n" + "摘要。\n\n> [!NOTE]\n> 请先阅读。\n\n## 问题修复\n\n- 导出。"
        self.assertEqual(check(both), [])
        entries = CHECK["changelog_entries"]
        changelog = "## v2 - 2026-11-26\nSummary.\n\n### Fixed\n\n- Export."
        with_note = changelog.replace("Summary.", "Summary.\n\n> [!NOTE]\n> Read this first.")
        self.assertEqual(entries(with_note, draft=False), entries(changelog, draft=False))
        self.assertTrue(CHECK["check_changelog"]([("en", with_note), ("zh", changelog)]))

    def test_contributor_handles_must_match(self):
        en = "Summary.\n\n## Contributors\n\nThanks to @alice and @bob for contributing to this release."
        zh = "摘要。\n\n## 贡献者\n\n感谢 @alice、@bob 对本版本的贡献。"
        check = lambda other: CHECK["check_release"](en + "\n---\n" + other)
        self.assertEqual(check(zh), [])
        self.assertEqual(check(zh.replace("@alice", "@Alice")), [])
        self.assertTrue(check(zh.replace("@bob", "@bob、@carol")))
        self.assertTrue(check(zh.replace("、@bob", "")))
        with_mail = en.replace("@alice and @bob", "@alice, @bob (dev@example.com)")
        with_mail_zh = zh.replace("@alice、@bob", "@alice、@bob（dev@example.com）")
        self.assertEqual(CHECK["check_release"](with_mail + "\n---\n" + with_mail_zh), [])
        entry = "## v2 - 2026-11-26\nSummary.\n\n### Contributors\n\nThanks to @alice for contributing to this release."
        self.assertTrue(CHECK["check_changelog"]([("en", entry), ("zh", entry.replace("@alice", "@alice and @bob"))]))

    def test_template_instruction_comments_cannot_remain(self):
        check = CHECK["check_release"]
        template = (TEMPLATE_DIR / "release-template.md").read_text(encoding="utf-8")
        comments = COMMENTS.findall(template)
        # The header comments carry no OPTIONAL marker; the verbatim match must still catch them.
        headers = [comment for comment in comments if not comment.strip().startswith(("OPTIONAL:", "<!--"))]
        self.assertGreaterEqual(len(headers), 4)
        body = "Summary.\n\n---\n\n摘要。"
        for comment in comments:
            with self.subTest(comment=comment[:40]):
                self.assertIn("template instructions remain", check(f"<!--{comment}-->\n\n{body}"))
        for comment in headers:
            with self.subTest(rewrapped=comment[:40]):
                rewrapped = "<!--\n  " + comment.strip().replace("\n", " \n") + "  \n-->\n\n"
                self.assertIn("template instructions remain", check(rewrapped + body))
        self.assertEqual(check("Summary.\n\n<!-- Internal note: reviewed on 2026-11-26. -->\n\n---\n\n摘要。"), [])

    def test_issue_references_ignore_quoted_hex_colors(self):
        en = "Fixed.\n\n## Fixed\n\n- Use fill=\"#333\" for the icon."
        zh = "修复。\n\n## 问题修复\n\n- 图标使用 fill=\"#333\"。"
        check = lambda other: CHECK["check_release"](en + "\n---\n" + other)
        self.assertEqual(check(zh), [])
        self.assertEqual(check(zh.replace("fill=\"#333\"", "fill=#333")), [])
        self.assertEqual(check(zh.replace("fill=\"#333\"", "深灰色")), [])
        self.assertEqual(check("修复。\n\n## 问题修复\n\n- 标题里的 ##333 不是事项编号。"), [])
        self.assertTrue(check("修复。\n\n## 问题修复\n\n- 修复 #12。"))


if __name__ == "__main__":
    unittest.main()
