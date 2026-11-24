"""Regression checks for rendering bilingual release templates."""

import re
import unittest
from pathlib import Path


TEMPLATE_DIR = Path(__file__).resolve().parents[1]
COMMENTS = re.compile(r"<!--(.*?)-->", re.DOTALL)
PLACEHOLDERS = re.compile(r"\{\{([A-Z0-9_]+)\}\}")
SHARED_FACTS = {
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
    def test_prerelease_warning_and_migration_precede_release_screenshot(self):
        english_release, chinese_release = (TEMPLATE_DIR / "release-template.md").read_text(encoding="utf-8").split("\n---\n")
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
                "MIGRATION_STEP_1": steps[0],
                "MIGRATION_STEP_2": steps[1],
            }
            with self.subTest(language=language):
                screenshot = "docs/output-preview.png"
                facts.update(DEMO_ALT_TEXT=summary, DEMO_IMAGE_PATH_OR_URL=screenshot)
                rendered = render_prerelease(template, facts)
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
                expected_headings = [f"## {heading}"]
                self.assertEqual(headings, expected_headings)
                for residue in ("<!--", "{{", "OPTIONAL:", "[!IMPORTANT]"):
                    self.assertNotIn(residue, rendered)


if __name__ == "__main__":
    unittest.main()
