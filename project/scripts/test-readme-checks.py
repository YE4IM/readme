"""Regression tests for the README checker."""

import runpy
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


SCRIPTS = Path(__file__).resolve().parent
CHECK = runpy.run_path(str(SCRIPTS / "check-readme.py"))
ROOT = SCRIPTS.parent
ENGLISH = (ROOT / "docs" / "project.md").read_text(encoding="utf-8")
CHINESE = (ROOT / "docs" / "project-zh-CN.md").read_text(encoding="utf-8")
SWITCH_NAMES = ("project.md", "project-zh-CN.md")


class ReadmeCheckTests(unittest.TestCase):
    def check_pair(self, english, chinese, *, draft=False):
        with TemporaryDirectory() as directory:
            kit = Path(directory) / "project"
            kit.mkdir()
            (kit.parent / "LICENSE").write_bytes((ROOT.parent / "LICENSE").read_bytes())
            root = kit / "docs"
            root.mkdir()
            for subdir in ("templates",):
                (kit / subdir).mkdir()
                for source in (ROOT / subdir).glob("*.md"):
                    (kit / subdir / source.name).write_bytes(source.read_bytes())
            guide = ROOT / "project-agent-instructions.md"
            if guide.exists():
                (kit / guide.name).write_bytes(guide.read_bytes())
            for name, text in zip(SWITCH_NAMES, (english, chinese)):
                (root / name).write_text(text, encoding="utf-8")
            (root / "assets").mkdir()
            for asset in (ROOT / "assets").glob("*.svg"):
                (root / "assets" / asset.name).write_bytes(asset.read_bytes())
            return CHECK["check_pair"](
                root / SWITCH_NAMES[0], root / SWITCH_NAMES[1], "local",
                switch_filenames=SWITCH_NAMES, draft=draft,
            )

    def test_signature_ignores_other_pictures(self):
        example = ROOT / "docs" / "project.md"
        with_picture = ENGLISH + '\n<picture><img src="demo.png" alt="Demo"></picture>\n'
        self.assertEqual(CHECK["signature_errors"]("English", with_picture, "local", example), [])

    def test_signature_picture_must_be_inside_first_link(self):
        example = ROOT / "docs" / "project.md"
        unlinked = ENGLISH.replace("><picture>", "></a><picture>", 1).replace("</picture></a>", "</picture>", 1)
        self.assertTrue(CHECK["signature_errors"]("English", unlinked, "local", example))

    def test_local_signature_files_must_exist(self):
        with TemporaryDirectory() as directory:
            example = Path(directory) / "README.md"
            errors = CHECK["signature_errors"](
                "English", ENGLISH.replace("../assets/", "./assets/"), "local", example,
            )
        self.assertEqual(len(errors), 2)
        self.assertTrue(all("local signature asset is missing" in error for error in errors))

    def test_signature_source_requires_matching_dark_media(self):
        example = ROOT / "docs" / "project.md"
        broken = ENGLISH.replace("(prefers-color-scheme: dark)", "(prefers-color-scheme: light)", 1)
        self.assertIn("English is missing the dark signature source",
                      CHECK["signature_errors"]("English", broken, "local", example))

    def test_signature_source_cannot_be_commented_out(self):
        example = ROOT / "docs" / "project.md"
        broken = ENGLISH.replace("<source ", "<!-- <source ", 1).replace("><img", "> --><img", 1)
        self.assertIn("English is missing the dark signature source",
                      CHECK["signature_errors"]("English", broken, "local", example))

    def test_templates_reject_incorrect_signature_links(self):
        with TemporaryDirectory() as directory:
            templates = Path(directory)
            for filename in ("readme-template.md", "readme-zh-CN-template.md"):
                original = (ROOT / "templates" / filename).read_text(encoding="utf-8")
                broken = original.replace('href="https://opc.fish"', 'href="https://example.org"', 1)
                (templates / filename).write_text(broken, encoding="utf-8")
            self.assertCountEqual(CHECK["check_templates"](templates), [
                f"{label} template must begin with the signature picture linked to https://opc.fish"
                for label in ("English", "Chinese")
            ])

    def test_template_fields_cannot_swap_sections_or_change_heading_levels(self):
        english = (ROOT / "templates" / "readme-template.md").read_text(encoding="utf-8")
        chinese = (ROOT / "templates" / "readme-zh-CN-template.md").read_text(encoding="utf-8")
        self.assertFalse(CHECK["template_alignment_errors"](english, chinese))
        swapped = chinese.replace("{{INSTALL_COMMAND}}", "@@TEMP@@").replace(
            "{{USAGE_SNIPPET}}", "{{INSTALL_COMMAND}}"
        ).replace("@@TEMP@@", "{{USAGE_SNIPPET}}")
        self.assertTrue(CHECK["template_alignment_errors"](english, swapped))
        self.assertTrue(CHECK["template_alignment_errors"](
            english, chinese.replace("## 快速开始", "### 快速开始", 1),
        ))
        lower = chinese.replace("{{INSTALL_SNIPPET_LANGUAGE}}", "bash", 1)
        self.assertTrue(CHECK["template_alignment_errors"](english, lower))

    def test_code_fences_catch_template_fields_but_allow_foreign_syntax(self):
        en = ENGLISH.replace("../assets/", "./assets/") + "\n~~~~jinja\n{{ item }}\n~~~~\n"
        zh = CHINESE.replace("../assets/", "./assets/")
        self.assertEqual(self.check_pair(en, zh), [])
        invalid = en.replace("{{ item }}", "{{QUICK_START_COMMANDS}}")
        self.assertTrue(any("{{QUICK_START_COMMANDS}}" in error for error in self.check_pair(invalid, zh)))

    def test_editorial_todos_require_draft_mode(self):
        en = ENGLISH.replace("../assets/", "./assets/") + "\n~~~text\n{{TODO: verify}}\n~~~\n"
        zh = CHINESE.replace("../assets/", "./assets/") + "\n{{TODO: 核实}}\n"
        self.assertEqual(len(self.check_pair(en, zh)), 2)
        self.assertEqual(self.check_pair(en, zh, draft=True), [])

    def test_bilingual_commands_allow_local_comments_and_prompt_output(self):
        english = """## Installation

~~~bash
# Install the package
example install --profile "a # b" # Keep defaults
~~~

## Quick Start

~~~console
$ example --output json
Wrote a report
~~~
"""
        chinese = """## 安装

~~~bash
# 安装包
example install --profile "a # b" # 保留默认值
~~~

## 快速开始

~~~console
$ example --output json
已写出报告
~~~
"""
        self.assertEqual(CHECK["command_errors"](english, chinese), [])
        changed = chinese.replace("--output json", "--output text").replace("--profile", "--mode")
        self.assertEqual(CHECK["command_errors"](english, changed), [
            "installation commands differ between English and Chinese",
            "quick start commands differ between English and Chinese",
        ])

    def test_fenced_example_headings_do_not_change_section(self):
        english = "## Quick Start\n~~~text\n## Output\n~~~\n~~~sh\nexample run\n~~~"
        chinese = "## 快速开始\n~~~sh\nexample run\n~~~\n## 用法\n~~~sh\nexample info\n~~~"
        self.assertEqual(CHECK["command_errors"](english, chinese), [])
        self.assertTrue(CHECK["command_errors"](english, chinese.replace("example run\n", "")))

    def test_language_switch_must_be_visible_immediately_after_title(self):
        en = ENGLISH.replace("../assets/", "./assets/")
        zh = CHINESE.replace("../assets/", "./assets/")
        line = "[**English**](./project.md) | [中文](./project-zh-CN.md)"
        for replacement in (f"<!-- {line} -->", f"~~~md\n{line}\n~~~", f"An introduction.\n\n{line}"):
            with self.subTest(replacement=replacement):
                self.assertTrue(any("visible English language switch" in error
                                    for error in self.check_pair(en.replace(line, replacement), zh)))
        self.assertTrue(any("link relatively to both README files" in error for error in
                            self.check_pair(en.replace("./project-zh-CN.md", "./project.md", 1), zh)))

    def test_inline_comment_delimiters_do_not_hide_following_links(self):
        en = ENGLISH.replace("../assets/", "./assets/")
        zh = CHINESE.replace("../assets/", "./assets/")
        text = en + "\nWrite `<!--` to begin a comment.\n\n[Guide](./missing.md)"
        self.assertTrue(any("missing path" in error for error in self.check_pair(text, zh)))
        self.assertFalse(self.check_pair(text.replace("./missing.md", "./project.md"), zh))

    def test_navigation_checks_relative_files_and_localized_anchors(self):
        en = ENGLISH.replace("../assets/", "./assets/")
        zh = CHINESE.replace("../assets/", "./assets/")
        en += "\n[Start](#quick-start) · [Chinese](./project-zh-CN.md#快速开始)\n"
        self.assertEqual(self.check_pair(en, zh), [])
        broken = en.replace("#quick-start", "#no-such-heading")
        broken += "\n[missing][doc]\n\n[doc]: ../missing%20file.md\n"
        errors = self.check_pair(broken, zh)
        self.assertTrue(any("missing heading" in error for error in errors))
        self.assertTrue(any("missing path" in error for error in errors))

    def test_fence_languages_and_command_block_boundaries_must_match(self):
        english = "## Installation\n~~~bash\necho ok\n~~~"
        chinese = "## 安装\n~~~pwsh\necho ok\n~~~"
        self.assertTrue(CHECK["command_errors"](english, chinese))
        self.assertTrue(CHECK["command_errors"](
            english.replace("bash", "python"), chinese.replace("pwsh", "ruby"),
        ))
        one_block = english.replace("echo ok", "echo ok\necho again")
        two_blocks = english + "\n~~~bash\necho again\n~~~"
        self.assertTrue(CHECK["command_errors"](one_block, two_blocks))

    def test_inline_syntax_and_example_secret_values_are_allowed(self):
        en = ENGLISH.replace("../assets/", "./assets/")
        zh = CHINESE.replace("../assets/", "./assets/")
        inline = chr(96) + "{{ item }}" + chr(96)
        example = '\n~~~bash\nTOKEN="YOUR_API_TOKEN"\n~~~\n'
        en += f"\nUse {inline}.\n" + example
        self.assertEqual(self.check_pair(en, zh), [])
        self.assertTrue(any("{{QUICK_START_COMMANDS}}" in error for error in
                            self.check_pair(en.replace("{{ item }}", "{{QUICK_START_COMMANDS}}"), zh)))
        self.assertTrue(any("editorial TODO" in error for error in
                            self.check_pair(en.replace("{{ item }}", "{{TODO: verify}}"), zh)))
        self.assertTrue(any("possible secret assignment" in error for error in
                            self.check_pair(en.replace("YOUR_API_TOKEN", "YOUR_PRIVATE_TOKEN_123"), zh)))
        fake_token = "ghp_" + "X" * 36
        self.assertTrue(CHECK["secret_errors"]("English", fake_token))


    def test_templates_use_the_actual_shell_for_command_examples(self):
        for path in sorted((ROOT / "templates").glob("readme*-template.md")):
            template = path.read_text(encoding="utf-8")
            for field in ("INSTALL_SNIPPET_LANGUAGE", "QUICK_START_SNIPPET_LANGUAGE"):
                guidance = next(line for line in template.splitlines() if line.startswith(field))
                self.assertIn("powershell", guidance, path.name)
            self.assertIn("```{{TEST_SNIPPET_LANGUAGE}}\n{{TEST_COMMAND}}", template)
        snippet = "\n\n```powershell\nGet-Item .\n```"
        english, chinese = "## Quick Start" + snippet, "## 快速开始" + snippet
        self.assertEqual(CHECK["command_errors"](english, chinese), [])
        self.assertTrue(CHECK["command_errors"](english, chinese.replace("powershell", "bash")))


    def test_template_logo_with_real_local_image(self):
        rendered = []
        for path, example in zip(("readme-template.md", "readme-zh-CN-template.md"), (ENGLISH, CHINESE)):
            source = (ROOT / "templates" / path).read_text()
            switch = next(line for line in source.splitlines() if "./README-zh-CN.md)" in line)
            self.assertLess(source.index(switch), source.index("{{LOGO_PATH}}"))
            logo = next(line for line in source.splitlines() if "{{LOGO_PATH}}" in line)
            image = logo.replace("{{LOGO_PATH}}", "./assets/opc-fish-project-signature.svg").replace("{{PROJECT_NAME}}", "Example")
            header = example.replace("../assets/", "./assets/").split("\n\n", 3)
            rendered.append("\n\n".join([*header[:3], image, header[3]]))
        self.assertEqual(self.check_pair(*rendered), [])
        self.assertTrue(self.check_pair(rendered[0].replace('src="./assets/opc-fish-project-signature.svg" alt="Example', 'src="missing.svg" alt="Example'), rendered[1]))

    def test_core_sections_cannot_be_folded_into_details(self):
        en = ENGLISH.replace("../assets/", "./assets/")
        zh = CHINESE.replace("../assets/", "./assets/")
        folded = "<details>\n<summary>Steps</summary>\n\n## Quick Start\n\n1. Run it.\n\n</details>\n\n"
        errors = self.check_pair(en.replace("## Quick Start", folded.rstrip("\n"), 1), zh)
        self.assertEqual(errors, ["English folds Quick Start into <details>; Installation and Quick Start must stay expanded"])
        folded_zh = "<details>\n<summary>安装步骤</summary>\n\n### 安装\n\nRun it.\n\n</details>\n\n"
        self.assertIn("Chinese folds 安装 into <details>; Installation and Quick Start must stay expanded",
                      self.check_pair(en, zh.replace("## 检查", folded_zh + "## 检查", 1)))
        secondary = (
            "\n<details>\n<summary>Extra platforms</summary>\n\n### Notes\n\n- a\n\n</details>\n"
            "\n```html\n<details>\n## Quick Start\n</details>\n```\n"
            "\nUse `<details>` for secondary material.\n"
        )
        self.assertEqual(self.check_pair(en + secondary, zh + secondary), [])

    def test_primary_steps_must_be_visible_under_an_expanded_heading(self):
        en = ENGLISH.replace("../assets/", "./assets/").split("## Quick Start")[0]
        zh = CHINESE.replace("../assets/", "./assets/").split("## 快速开始")[0]
        command = "~~~sh\ntool run\n~~~"
        steps = "<details>\n<summary>Steps</summary>\n\n" + command + "\n\n</details>"
        for heading, translation in (("Quick Start", "快速开始"), ("Installation", "安装")):
            for outside in ("", "Follow these steps:\n", "Run the following command.\n", "<!-- internal note -->\n"):
                with self.subTest(heading=heading, outside=outside):
                    result = self.check_pair(en + f"## {heading}\n\n{outside}{steps}",
                                             zh + f"## {translation}\n\n{outside}{steps}")
                    self.assertTrue(any("fold" in error for error in result), result)
            for outside in (command, "1. Open the guide.", "[Open the guide](./project.md)"):
                with self.subTest(heading=heading, outside=outside):
                    self.assertEqual(self.check_pair(en + f"## {heading}\n\n{outside}\n\n{steps}",
                                                     zh + f"## {translation}\n\n{outside}\n\n{steps}"), [])
        self.assertTrue(self.check_pair(en + "Quick Start\n-----------\n\n" + steps,
                                        zh + "快速开始\n--------\n\n" + steps))

    def test_template_instruction_comments_cannot_remain(self):
        en = ENGLISH.replace("../assets/", "./assets/")
        zh = CHINESE.replace("../assets/", "./assets/")
        for template in sorted((ROOT / "templates").glob("readme*-template.md")):
            comments = CHECK["COMMENT"].findall(template.read_text(encoding="utf-8"))
            for comment in comments:
                with self.subTest(template=template.name, comment=comment[:40]):
                    left = f"<!--\n{comment.strip()}\n-->\n\n"
                    self.assertTrue(any("still contains a template instruction comment" in error
                                        for error in self.check_pair(left + en, zh)))
        self.assertEqual(self.check_pair(en + "\n<!-- Reviewed on 2026-11-26. -->\n", zh), [])
        self.assertEqual(self.check_pair(en + "\nWrite `<!--` to open a comment.\n", zh), [])

    def test_unquoted_secret_assignments_are_caught(self):
        en = ENGLISH.replace("../assets/", "./assets/")
        zh = CHINESE.replace("../assets/", "./assets/")
        for snippet in ("~~~bash\nAPI_KEY=sk-live-abcdefghijklmnop\n~~~", "~~~bash\nTOKEN='abcdefgh12345678'\n~~~",
                        "~~~bash\npassword: hunter2-hunter2-hunter2\n~~~"):
            with self.subTest(snippet=snippet):
                self.assertIn("English matches a possible secret assignment", self.check_pair(en + "\n" + snippet, zh))
        allowed = "~~~bash\nAPI_KEY=YOUR_API_KEY\nexport TOKEN=$API_TOKEN\nPASSWORD=\n~~~"
        self.assertEqual(self.check_pair(en + "\n" + allowed, zh), [])
        self.assertEqual(CHECK["secret_errors"]("English", "The token is read from the environment. secret: none"), [])

    def test_badge_limit_is_a_hard_limit(self):
        en = ENGLISH.replace("../assets/", "./assets/")
        zh = CHINESE.replace("../assets/", "./assets/")
        badge = "[![Status](https://example.com/b{}.svg)](https://example.com)"
        five = "\n" + " ".join(badge.format(n) for n in range(5)) + "\n"
        self.assertIn("English has 5 badges; the limit is 4", self.check_pair(en + five, zh))
        four = "\n" + " ".join(badge.format(n) for n in range(4)) + "\n"
        self.assertEqual(self.check_pair(en + four, zh), [])


if __name__ == "__main__":
    unittest.main()
