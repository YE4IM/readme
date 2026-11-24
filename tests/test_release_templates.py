"""Regression checks for rendering bilingual pre-release notes."""

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMMENTS = re.compile(r"<!--(.*?)-->", re.DOTALL)
PLACEHOLDERS = re.compile(r"\{\{([A-Z0-9_]+)\}\}")
RELEASE = ROOT / "releases readme" / "RELEASE.template.md"
CHANGELOG = ROOT / "changelog readme"
SHARED_FACTS = {
    "VERSION": "v2.0.0-rc.1",
    "RELEASE_DATE": "2026-11-24",
    "BREAKING_CHANGE_AREA": "CLI",
}


def render_prerelease(template, facts):
    def render_comment(match):
        comment = match[1].strip()
        if not comment.startswith("OPTIONAL:"):
            return ""
        _, _, body = comment.partition("\n\n")
        names = PLACEHOLDERS.findall(body)
        if "IMPORTANT_WARNING" in names:
            body = body.split("\n\n> [!IMPORTANT]", 1)[0]
            names = PLACEHOLDERS.findall(body)
        return body if names and facts.keys() >= set(names) else ""

    document = COMMENTS.sub(render_comment, template)
    document = PLACEHOLDERS.sub(lambda match: facts[match[1]], document)
    return re.sub(r"\n{3,}", "\n\n", document).strip()


class ReleaseTemplateTests(unittest.TestCase):
    def test_changelog_optional_sections_are_paired_and_self_contained(self):
        signatures = []
        for filename in ("CHANGELOG.version.template.md", "CHANGELOG.version.zh-CN.template.md"):
            with self.subTest(filename=filename):
                template = (CHANGELOG / filename).read_text(encoding="utf-8")
                visible = COMMENTS.sub("", template)
                self.assertEqual(
                    visible.strip(),
                    "## [{{VERSION}}] - {{RELEASE_DATE}}\n\n{{RELEASE_SUMMARY}}",
                )
                blocks = [
                    comment.strip().partition("\n\n")[2]
                    for comment in COMMENTS.findall(template)
                    if comment.strip().startswith("OPTIONAL:")
                ]
                self.assertEqual(len(blocks), 12)
                self.assertTrue(blocks[0].startswith("> [!WARNING]\n"))
                self.assertTrue(all(block.startswith("### ") for block in blocks[1:]))
                self.assertTrue(all(PLACEHOLDERS.search(block) for block in blocks))
                signatures.append([PLACEHOLDERS.findall(block) for block in blocks])
        self.assertEqual(*signatures)

    def test_prerelease_warning_and_migration_precede_release_screenshot(self):
        english_release, chinese_release = RELEASE.read_text(encoding="utf-8").split("\n---\n")
        for language, release, filename, heading, summary, warning, change, steps in (
            (
                "en", english_release, "CHANGELOG.version.template.md", "Breaking Changes",
                "The CLI now uses the new output flag.",
                "This pre-release is for testing and feedback. Avoid production use.",
                "Scripts using `--format` must switch flags.",
                ("Rename `--format` to `--output`.", "Run `example --output json`."),
            ),
            (
                "zh-CN", chinese_release, "CHANGELOG.version.zh-CN.template.md", "破坏性变更",
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
                "MIGRATION_STEP_1": steps[0],
                "MIGRATION_STEP_2": steps[1],
            }
            changelog = (CHANGELOG / filename).read_text(encoding="utf-8")
            screenshot = "docs/output-preview.png"
            for kind, template, prefix in (
                ("release", release, "##"),
                ("changelog", changelog, "###"),
            ):
                with self.subTest(language=language, kind=kind):
                    values = facts.copy()
                    if kind == "release":
                        values.update(DEMO_ALT_TEXT=summary, DEMO_IMAGE_PATH_OR_URL=screenshot)
                    rendered = render_prerelease(template, values)
                    expected = [
                        summary,
                        f"> [!WARNING]\n> {warning}",
                        f"{prefix} {heading}",
                        change,
                        f"1. {steps[0]}",
                        f"2. {steps[1]}",
                    ]
                    if kind == "release":
                        expected.append(f"![{summary}]({screenshot})")
                    positions = [rendered.index(item) for item in expected]
                    self.assertEqual(positions, sorted(positions))
                    headings = re.findall(r"^#{2,3} .+$", rendered, re.MULTILINE)
                    expected_headings = [f"{prefix} {heading}"]
                    if kind == "changelog":
                        expected_headings.insert(
                            0, f'## [{facts["VERSION"]}] - {facts["RELEASE_DATE"]}'
                        )
                    self.assertEqual(headings, expected_headings)
                    for residue in ("<!--", "{{", "OPTIONAL:", "[!IMPORTANT]"):
                        self.assertNotIn(residue, rendered)


if __name__ == "__main__":
    unittest.main()
