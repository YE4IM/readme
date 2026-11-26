#!/usr/bin/env python3
"""Check README pairs and the bilingual templates in this repository.

Usage:
  python3 scripts/check-readme.py all
  python3 scripts/check-readme.py templates
  python3 scripts/check-readme.py pair README.md README-zh-CN.md --signature local
  python3 scripts/check-readme.py pair A.md B.md --signature remote
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
REMOTE_LIGHT = (
    "https://raw.githubusercontent.com/YE4IM/readme/main/project%20readme/assets/"
    "opc-fish-project-signature.svg"
)
REMOTE_DARK = (
    "https://raw.githubusercontent.com/YE4IM/readme/main/project%20readme/assets/"
    "opc-fish-project-signature-web-dark.svg"
)
PLACEHOLDER = re.compile(r"\{\{([^{}]+)\}\}")
FENCE_START = re.compile(r"^[ \t]*(`{3,}|~{3,})(.*)$")
SECTION_HEADING = re.compile(r"^ {0,3}(#{1,6})[ \t]+(.+?)\s*#*\s*$")
COMMAND_HEADINGS = {
    "installation": "installation",
    "安装": "installation",
    "quick start": "quick start",
    "快速开始": "quick start",
}
SHELL_LANGUAGES = {
    "bash", "sh", "shell", "zsh", "fish", "ksh", "shell-session", "console",
    "powershell", "pwsh", "ps1", "cmd", "bat", "batch", "dos",
}
PROMPT = re.compile(r"^(?:\$ |>>>? |PS(?: [^>]+)?> )")
SIGNATURE_LINK = re.compile(r"\A\s*<a\b([^>]*)>\s*(<picture\b[^>]*>.*?</picture>)\s*</a>", re.S | re.I)
HTML_ATTRIBUTE = re.compile(r"\s+([^\s=/>]+)\s*=\s*(?:\x22([^\x22]*)\x22|\x27([^\x27]*)\x27)")
TEMPLATE_TOKEN = re.compile(
    r"<!--(.*?)-->|^(#{1,6}[ \t]+[^\n]+)|^[ \t]*(`{3,}|~{3,})[^\n]*|\{\{([A-Z0-9_]+)\}\}",
    re.S | re.M,
)
COMMENT = re.compile(r"<!--(.*?)-->", re.S)
SECRET_PATTERNS = (
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bghp_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"(?i)\b(api[_-]?key|token|password|secret)\b\s*[:=]\s*(['\"])([A-Za-z0-9_-]{12,})\2"),
)
EXAMPLE_SECRETS = {"YOUR_API_KEY", "YOUR_API_TOKEN", "YOUR_TOKEN", "YOUR_PASSWORD", "YOUR_SECRET"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Check README template output.")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("templates", help="compare the English and Chinese templates")
    sub.add_parser("all", help="check templates, bundled examples and the repository README pair")

    pair = sub.add_parser("pair", help="check a delivered README pair")
    pair.add_argument("english")
    pair.add_argument("chinese")
    pair.add_argument("--signature", choices=("local", "remote"), required=True)

    pair.add_argument("--draft", action="store_true", help="allow editorial TODO markers")

    args = parser.parse_args()
    errors: list[str] = []
    if args.command == "templates":
        errors.extend(check_templates())
    elif args.command == "all":
        errors.extend(check_templates())
        errors.extend(check_pair(ROOT.parent / "README.md", ROOT.parent / "README-zh-CN.md", "remote"))
        errors.extend(
            check_pair(
                ROOT / "docs" / "project.md",
                ROOT / "docs" / "project-zh-CN.md",
                "local",
                switch_filenames=("project.md", "project-zh-CN.md"),
            )
        )
    else:
        errors.extend(check_pair(Path(args.english), Path(args.chinese), args.signature, draft=args.draft))

    if errors:
        for error in errors:
            print(f"FAIL {error}")
        return 1
    print("OK")
    return 0


def check_templates(directory: Path = ROOT / "templates") -> list[str]:
    english_path = directory / "readme-template.md"
    chinese_path = directory / "readme-zh-CN-template.md"
    english = english_path.read_text(encoding="utf-8")
    chinese = chinese_path.read_text(encoding="utf-8")
    errors = template_alignment_errors(english, chinese)
    for label, text, path in (
        ("English template", english, english_path),
        ("Chinese template", chinese, chinese_path),
    ):
        errors.extend(signature_errors(label, text, "remote", path))
        if text.count("> [!NOTE]") != 1 or text.count("> [!WARNING]") != 1:
            errors.append(f"{label} should keep NOTE and WARNING in separate blocks")
    return errors


def template_structure(text: str) -> list:
    """Keep headings, fences, comments and fields in order, ignoring translated prose."""
    structure = []
    for token in TEMPLATE_TOKEN.finditer(text):
        comment, heading, fence, field = token.groups()
        if comment is not None:
            structure.append(("comment", template_structure(comment)))
        elif heading:
            structure.append(("heading", len(heading.split()[0]), tuple(PLACEHOLDER.findall(heading))))
        elif fence:
            structure.append(("fence", fence[0], tuple(PLACEHOLDER.findall(token[0]))))
        else:
            structure.append(("field", field))
    return structure


def template_alignment_errors(english: str, chinese: str) -> list[str]:
    if template_structure(english) != template_structure(chinese):
        return ["template section levels, block order or fields differ between English and Chinese"]
    return []


def check_pair(
    english_path: Path,
    chinese_path: Path,
    signature: str,
    *,
    switch_filenames: tuple[str, str] = ("README.md", "README-zh-CN.md"),
    draft: bool = False,
) -> list[str]:
    errors: list[str] = []
    files = {"English": english_path, "Chinese": chinese_path}
    texts: dict[str, str] = {}
    for label, path in files.items():
        if not path.is_file():
            errors.append(f"missing {label} file: {path}")
            continue
        texts[label] = path.read_text(encoding="utf-8")
    if len(texts) != 2:
        return errors

    fields = set()
    for template in (ROOT / "templates").glob("readme*-template.md"):
        fields.update(placeholder_names(template.read_text(encoding="utf-8")))
    errors.extend(command_errors(texts["English"], texts["Chinese"]))

    for label, text in texts.items():
        prose, visible, uncommented = document_views(text)
        errors.extend(language_switch_errors(label, visible, files, switch_filenames))
        errors.extend(link_errors(files[label], visible))
        errors.extend(placeholder_errors(label, INLINE_CODE.sub(mask, prose), draft=draft))
        for snippet in INLINE_CODE.finditer(prose):
            errors.extend(placeholder_errors(label, snippet[0], fields=fields, draft=draft))
        for _, _, language, lines in fenced_blocks(uncommented):
            snippet = "\n".join([language, *lines])
            errors.extend(placeholder_errors(label, snippet, fields=fields, draft=draft))
        errors.extend(comment_errors(label, prose))
        errors.extend(secret_errors(label, text))
        errors.extend(signature_errors(label, text, signature, files[label]))
        badges = len(re.findall(r"\[!\[", INLINE_CODE.sub(mask, visible)))
        if badges > 4:
            errors.append(f"{label} has {badges} badges; the default limit is 4")
        errors.extend(badge_layout_errors(label, visible))
    return errors


INLINE_CODE = re.compile(r"(?<!\x60)(\x60+)(?!\x60)(?:(?!\n[ \t]*\n).)*?(?<!\x60)\1(?!\x60)", re.S)
SWITCH = {
    "English": re.compile(r"\[\*\*English\*\*\]\(([^)]+)\) \| \[中文\]\(([^)]+)\)"),
    "Chinese": re.compile(r"\[English\]\(([^)]+)\) \| \[\*\*中文\*\*\]\(([^)]+)\)"),
}
MARKDOWN_DESTINATION = r"(?:<([^<>\n]+)>|([^\s()<>]+))"
MARKDOWN_LINK = re.compile(
    r"(?<!\\)\]\(\s*" + MARKDOWN_DESTINATION + r"""(?:[ \t]+(?:"[^"\n]*"|'[^'\n]*'))?\s*\)"""
)
REFERENCE_DEFINITION = re.compile(r"(?m)^ {0,3}\[([^\]\n]+)\]:[ \t]*" + MARKDOWN_DESTINATION)
SETEXT = re.compile(r"(?m)^ {0,3}([^\s#<>][^\n]*)\n {0,3}(=+|-+)[ \t]*$")


def mask(match: re.Match) -> str:
    return re.sub(r"[^\n]", " ", match[0])


def language_switch_errors(
    label: str, text: str, files: dict[str, Path], filenames: tuple[str, str]
) -> list[str]:
    lines = [line for line in text.lstrip("\ufeff").splitlines() if line.strip()]
    title = next(
        (index for index, line in enumerate(lines) if re.match(r"^ {0,3}#[ \t]+\S", line)),
        None,
    )
    offset = 1
    if title is None:
        title = next(
            (index for index in range(len(lines) - 1)
             if re.fullmatch(r" {0,3}=+[ \t]*", lines[index + 1])),
            None,
        )
        offset = 2
    switch_at = title + offset if title is not None else len(lines)
    switch = SWITCH[label].fullmatch(lines[switch_at].strip()) if switch_at < len(lines) else None
    if not switch:
        return [f"{files[label]} needs a visible {label} language switch immediately after its title"]
    for target, filename, path in zip(switch.groups(), filenames, files.values()):
        try:
            parts = urlsplit(target)
        except ValueError:
            parts = None
        if parts:
            relative = Path(unquote(parts.path))
            if (
                not (parts.scheme or parts.netloc or parts.query or parts.fragment)
                and not relative.is_absolute() and relative.name == filename
                and (files[label].parent / relative).resolve() == path.resolve()
            ):
                continue
        return [f"{files[label]} language switch must link relatively to both README files"]
    return []


def heading_anchors(text: str) -> set[str]:
    anchors = set()
    for tag in re.findall(r"<[A-Za-z][^>]*>", INLINE_CODE.sub(mask, text)):
        attrs = html_attributes(tag)
        if attrs.get("id"):
            anchors.add(attrs["id"])
        if re.match(r"<a\b", tag, re.I) and attrs.get("name"):
            anchors.add(attrs["name"])
    titles = [(m.start(), m[2]) for m in re.finditer(SECTION_HEADING.pattern, text, re.M)]
    titles.extend((m.start(), m[1]) for m in SETEXT.finditer(text))
    heading_ids: set[str] = set()
    for _, title in sorted(titles):
        title = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", title)
        title = re.sub(r"<[^>]+>", "", title).lower().replace(" ", "-")
        base = "".join(
            char for char in title
            if char in "_-" or unicodedata.category(char)[0] in "LMN"
        )
        candidate = base
        suffix = 1
        while candidate in heading_ids:
            candidate = f"{base}-{suffix}"
            suffix += 1
        heading_ids.add(candidate)
    return anchors | heading_ids


def link_errors(path: Path, visible: str) -> list[str]:
    markdown = INLINE_CODE.sub(mask, visible)
    destinations = [angle or plain for angle, plain in MARKDOWN_LINK.findall(markdown)]
    for tag in re.findall(r"<img\b[^>]*>", markdown, re.I):
        source = html_attributes(tag).get("src")
        if source:
            destinations.append(source)
    destinations.extend(
        angle or plain for label, angle, plain in REFERENCE_DEFINITION.findall(markdown)
        if re.search(r"\[" + re.escape(label) + r"\](?!:)", markdown, re.I)
    )
    errors = []
    anchors_by_file = {path.resolve(): heading_anchors(visible)}
    for destination in dict.fromkeys(destinations):
        try:
            parts = urlsplit(destination)
        except ValueError:
            continue
        if parts.scheme or parts.netloc or parts.path.startswith("/"):
            continue
        target = path.parent / unquote(parts.path) if parts.path else path
        if not target.exists():
            errors.append(f"{path} links to missing path: {destination}")
        elif parts.fragment and target.suffix.lower() in {".md", ".markdown"} and target.is_file():
            key = target.resolve()
            if key not in anchors_by_file:
                anchors_by_file[key] = heading_anchors(document_views(target.read_text(encoding="utf-8"))[1])
            if unquote(parts.fragment) not in anchors_by_file[key]:
                errors.append(f"{path} links to missing heading or HTML anchor: {destination}")
    return errors


BADGE = re.compile(r"\[!\[[^\]]*\]\([^)\s]+\)\]\([^)\s]+\)")
BADGE_LINE = re.compile(r"^(?:\[!\[[^\]]*\]\([^)\s]+\)\]\([^)\s]+\)\s*)+$")


def badge_layout_errors(label: str, visible: str) -> list[str]:
    """Several badges on separate lines stack vertically. Keep them on one line."""
    lines_in_run = 0
    badges_in_run = 0
    for raw in visible.splitlines():
        line = raw.strip()
        if not line:
            continue
        found = BADGE.findall(line)
        if found and BADGE_LINE.match(line):
            lines_in_run += 1
            badges_in_run += len(found)
            continue
        if lines_in_run >= 2 and badges_in_run >= 2:
            return [f"{label} badges must share one line so they sit side by side"]
        lines_in_run = 0
        badges_in_run = 0
    if lines_in_run >= 2 and badges_in_run >= 2:
        return [f"{label} badges must share one line so they sit side by side"]
    return []


def placeholder_names(text: str) -> set[str]:
    names = set()
    for match in PLACEHOLDER.finditer(text):
        body = match.group(1).strip()
        if re.fullmatch(r"[A-Z0-9_]+", body):
            names.add(body)
    return names


def placeholder_errors(
    label: str, text: str, *, fields: set[str] | None = None, draft: bool = False
) -> list[str]:
    errors = []
    for match in PLACEHOLDER.finditer(text):
        body = match[1].strip()
        if re.match(r"^TODO(?:\s*[:：]|$)", body):
            if not draft:
                errors.append(f"{label} still has an editorial TODO")
        elif fields is None or body in fields:
            errors.append(f"{label} still has placeholder {match[0]}")
    return errors


def comment_errors(label: str, visible: str) -> list[str]:
    errors = []
    for comment in COMMENT.findall(visible):
        if re.search(r"OPTIONAL|REQUIRED|To enable|启用：|整块删除", comment):
            errors.append(f"{label} still contains a template instruction comment")
            break
    return errors


def secret_errors(label: str, text: str) -> list[str]:
    *formats, assigned_value = SECRET_PATTERNS
    errors = [f"{label} matches a live-secret pattern: {pattern.pattern}" for pattern in formats if pattern.search(text)]
    if any(match[3] not in EXAMPLE_SECRETS for match in assigned_value.finditer(text)):
        errors.append(f"{label} matches a possible secret assignment")
    return errors


def local_asset(readme_path: Path, filename: str) -> str:
    parent = readme_path.resolve().parent
    root = ROOT.resolve()
    if parent == root or root in parent.parents:
        return Path(os.path.relpath(root / "assets" / filename, parent)).as_posix()
    return f"./assets/{filename}"


def html_attributes(tag: str) -> dict[str, str]:
    return {
        name.lower(): double or single
        for name, double, single in HTML_ATTRIBUTE.findall(tag)
    }


def signature_errors(label: str, text: str, signature: str, readme_path: Path) -> list[str]:
    text = re.sub(r"\A(?:\s|<!--.*?-->)*", "", text.lstrip("\ufeff"), flags=re.S)
    anchor = SIGNATURE_LINK.match(text)
    if not anchor or html_attributes(anchor[1]).get("href") != "https://opc.fish":
        return [f"{label} must begin with the signature picture linked to https://opc.fish"]
    errors = []
    if html_attributes(anchor[1]).get("title") != "OPC.FISH Project.":
        errors.append(f"{label} signature needs the OPC.FISH Project. link title")
    if signature == "remote":
        light, dark = REMOTE_LIGHT, REMOTE_DARK
    else:
        light = local_asset(readme_path, "opc-fish-project-signature.svg")
        dark = local_asset(readme_path, "opc-fish-project-signature-web-dark.svg")
        for path in (light, dark):
            if not (readme_path.parent / path).is_file():
                errors.append(f"{label} local signature asset is missing: {path}")
    picture = COMMENT.sub("", anchor[2])
    sources = [html_attributes(tag) for tag in re.findall(r"<source\b[^>]*>", picture, re.I)]
    if not any(
        source.get("media") == "(prefers-color-scheme: dark)" and source.get("srcset") == dark
        for source in sources
    ):
        errors.append(f"{label} is missing the dark signature source")
    images = re.findall(r"<img\b[^>]*>", picture, re.I)
    if len(images) != 1:
        return errors + [f"{label} signature needs one fallback img"]
    attrs = html_attributes(images[0])
    if attrs.get("src") != light:
        errors.append(f"{label} is missing the light signature src")
    if attrs.get("width") != "720":
        errors.append(f"{label} signature width must be 720")
    if not attrs.get("alt", "").strip():
        errors.append(f"{label} signature needs a descriptive alt")
    return errors


def fenced_blocks(text: str):
    """Yield line bounds, info strings, and content for backtick and tilde fences."""
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        start = FENCE_START.match(lines[index])
        if not start:
            index += 1
            continue
        fence, language = start.groups()
        first = index
        closing = re.compile(r"^\s*" + re.escape(fence[0]) + rf"{{{len(fence)},}}\s*$")
        index += 1
        while index < len(lines) and not closing.fullmatch(lines[index]):
            index += 1
        yield first, min(index + 1, len(lines)), language.strip(), lines[first + 1:index]
        index += 1


def document_views(text: str) -> tuple[str, str, str]:
    """Return source without fences, visible Markdown, and source without comments."""
    prose, visible, uncommented = [], [], []
    # Scan the two block types together, ignoring their markers inside each other.
    token = re.compile(r"(?m)^[ \t]*(\x60{3,}|~{3,})[^\n]*|<!--|\x60+")
    position = 0
    while match := token.search(text, position):
        prefix = text[position:match.start()]
        for view in (prose, visible, uncommented):
            view.append(prefix)
        end = match.end()
        fence = match[1]
        if not fence and match[0] != "<!--":
            span = INLINE_CODE.match(text, match.start())
            end = span.end() if span else end
            for view in (prose, visible, uncommented):
                view.append(text[match.start():end])
            position = end
            continue
        if fence:
            closing = re.search(r"(?m)^[ \t]*" + re.escape(fence[0]) + rf"{{{len(fence)},}}[ \t]*$", text[end:])
            end += closing.end() if closing else len(text) - end
        else:
            closing = text.find("-->", end)
            end = closing + 3 if closing != -1 else len(text)
        block = text[match.start():end]
        blank = re.sub(r"[^\n]", " ", block)
        prose.append(blank if fence else block)
        visible.append(blank)
        uncommented.append(block if fence else blank)
        position = end
    tail = text[position:]
    return "".join(prose) + tail, "".join(visible) + tail, "".join(uncommented) + tail


def shell_commands(lines: list[str], language: str) -> list[str]:
    commands = []
    prompt_mode = language in {"console", "shell-session"} or any(
        PROMPT.match(line.lstrip()) for line in lines
    )
    continued = False
    for raw in lines:
        line = raw.strip()
        prompt = PROMPT.match(line)
        if prompt:
            line = line[prompt.end():]
        elif prompt_mode and not continued:
            continue
        if not line or line.startswith("#"):
            continue
        # Comments separated by whitespace on the same line may be localized.
        line = re.split(r"(\x22[^\x22]*\x22|\x27[^\x27]*\x27)", line)
        command = ""
        for part in line:
            if part.startswith(('"', "'")):
                command += part
                continue
            comment = re.search(r"(?<!\\)\s+#", part) if language not in {"cmd", "bat", "batch", "dos"} else None
            if comment:
                command += part[:comment.start()]
                break
            command += part
        commands.append(command.rstrip())
        continued = command.rstrip().endswith(("\\", "^", "`"))
    return commands


def section_commands(text: str) -> dict[str, list[tuple[str, list[str]]]]:
    text = document_views(text)[2]
    blocks = {start: (end, info, lines) for start, end, info, lines in fenced_blocks(text)}
    commands: dict[str, list[tuple[str, list[str]]]] = {}
    section = None
    level = 0
    index = 0
    source = text.splitlines()
    while index < len(source):
        if index in blocks:
            index, info, lines = blocks[index]
            language = info.lower().split(maxsplit=1)[0] if info else ""
            if section and language not in {"text", "plaintext", "output"}:
                commands.setdefault(section, []).append(
                    (language, shell_commands(lines, language) if language in SHELL_LANGUAGES else [])
                )
            continue
        heading = SECTION_HEADING.match(source[index])
        if heading:
            depth, title = heading.groups()
            match = COMMAND_HEADINGS.get(title.strip().casefold())
            if match or len(depth) <= level:
                section = match
                level = len(depth)
        index += 1
    return commands


def command_errors(english: str, chinese: str) -> list[str]:
    en_commands = section_commands(english)
    zh_commands = section_commands(chinese)
    return [
        f"{section} commands differ between English and Chinese"
        for section in sorted(en_commands.keys() | zh_commands.keys())
        if en_commands.get(section, []) != zh_commands.get(section, [])
    ]


if __name__ == "__main__":
    sys.exit(main())
