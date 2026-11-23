#!/usr/bin/env python3
"""Check README pairs and the bilingual templates in this repository.

Usage:
  python3 scripts/check_readme.py all
  python3 scripts/check_readme.py templates
  python3 scripts/check_readme.py pair README.md README.zh-CN.md --signature local
  python3 scripts/check_readme.py pair A.md B.md --signature remote
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REMOTE_LIGHT = (
    "https://raw.githubusercontent.com/YE4IM/readme/main/assets/"
    "opc-fish-project-signature-readme-2400x800-on-cream.png"
)
REMOTE_DARK = (
    "https://raw.githubusercontent.com/YE4IM/readme/main/assets/"
    "opc-fish-project-signature-readme-2400x800-web-dark.png"
)
LOCAL_LIGHT = "./assets/opc-fish-project-signature-readme-2400x800-on-cream.png"
LOCAL_DARK = "./assets/opc-fish-project-signature-readme-2400x800-web-dark.png"
EN_SWITCH = "[**English**](./README.md) | [中文](./README.zh-CN.md)"
ZH_SWITCH = "[English](./README.md) | [**中文**](./README.zh-CN.md)"
PLACEHOLDER = re.compile(r"\{\{([^{}]+)\}\}")
FENCE = re.compile(r"```.*?```", re.S)
PICTURE = re.compile(r"<picture>\s*(.*?)\s*</picture>", re.S | re.I)
COMMENT = re.compile(r"<!--(.*?)-->", re.S)
HEADING = re.compile(r"^#{1,6} ", re.M)
SECRET_PATTERNS = (
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bghp_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"(?i)\b(api[_-]?key|token|password|secret)\b\s*[:=]\s*['\"][A-Za-z0-9_\-]{12,}['\"]"),
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check README template output.")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("templates", help="compare the English and Chinese templates")
    sub.add_parser("all", help="check templates, this repo, and the CLI specimen")

    pair = sub.add_parser("pair", help="check a delivered README pair")
    pair.add_argument("english")
    pair.add_argument("chinese")
    pair.add_argument("--signature", choices=("local", "remote"), required=True)

    args = parser.parse_args()
    errors: list[str] = []
    if args.command == "templates":
        errors.extend(check_templates())
    elif args.command == "all":
        errors.extend(check_templates())
        errors.extend(check_pair(ROOT / "README.md", ROOT / "README.zh-CN.md", "local"))
        errors.extend(
            check_pair(
                ROOT / "examples/sample-cli/README.md",
                ROOT / "examples/sample-cli/README.zh-CN.md",
                "remote",
            )
        )
    else:
        errors.extend(check_pair(Path(args.english), Path(args.chinese), args.signature))

    if errors:
        for error in errors:
            print(f"FAIL {error}")
        return 1
    print("OK")
    return 0


def check_templates() -> list[str]:
    english = (ROOT / "README.template.md").read_text(encoding="utf-8")
    chinese = (ROOT / "README.zh-CN.template.md").read_text(encoding="utf-8")
    errors: list[str] = []
    en_names = placeholder_names(english)
    zh_names = placeholder_names(chinese)
    if en_names != zh_names:
        errors.append(
            "template placeholders differ: "
            f"only English {sorted(en_names - zh_names)}; "
            f"only Chinese {sorted(zh_names - en_names)}"
        )
    en_comments = len(COMMENT.findall(english))
    zh_comments = len(COMMENT.findall(chinese))
    if en_comments != zh_comments:
        errors.append(f"template comment blocks differ: English {en_comments}, Chinese {zh_comments}")
    en_headings = len(HEADING.findall(english))
    zh_headings = len(HEADING.findall(chinese))
    if en_headings != zh_headings:
        errors.append(f"template headings differ: English {en_headings}, Chinese {zh_headings}")
    for label, text in (("English template", english), ("Chinese template", chinese)):
        if "opc-fish-project-signature-readme-2400x800-on-cream.png" not in text:
            errors.append(f"{label} is missing the light signature")
        if "opc-fish-project-signature-readme-2400x800-web-dark.png" not in text:
            errors.append(f"{label} is missing the dark signature")
        if text.count("> [!NOTE]") != 1 or text.count("> [!WARNING]") != 1:
            errors.append(f"{label} should keep NOTE and WARNING in separate blocks")
    return errors


def check_pair(english_path: Path, chinese_path: Path, signature: str) -> list[str]:
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

    if EN_SWITCH not in texts["English"]:
        errors.append(f"{english_path} is missing the English language switch")
    if ZH_SWITCH not in texts["Chinese"]:
        errors.append(f"{chinese_path} is missing the Chinese language switch")

    for label, text in texts.items():
        visible = strip_fences(text)
        errors.extend(placeholder_errors(label, visible))
        errors.extend(comment_errors(label, visible))
        errors.extend(secret_errors(label, text))
        errors.extend(signature_errors(label, visible, signature))
        badges = len(re.findall(r"\[!\[", text))
        if badges > 4:
            errors.append(f"{label} has {badges} badges; the default limit is 4")
    return errors


def placeholder_names(text: str) -> set[str]:
    names = set()
    for match in PLACEHOLDER.finditer(text):
        body = match.group(1).strip()
        if re.fullmatch(r"[A-Z0-9_]+", body):
            names.add(body)
    return names


def placeholder_errors(label: str, visible: str) -> list[str]:
    errors = []
    for match in PLACEHOLDER.finditer(visible):
        body = match.group(1).strip()
        if body.startswith("TODO:"):
            continue
        errors.append(f"{label} still has placeholder {match.group(0)}")
    return errors


def comment_errors(label: str, visible: str) -> list[str]:
    errors = []
    for comment in COMMENT.findall(visible):
        if re.search(r"OPTIONAL|REQUIRED|To enable|启用：|整块删除", comment):
            errors.append(f"{label} still contains a template instruction comment")
            break
    return errors


def secret_errors(label: str, text: str) -> list[str]:
    return [f"{label} matches a live-secret pattern: {pattern.pattern}" for pattern in SECRET_PATTERNS if pattern.search(text)]


def signature_errors(label: str, visible: str, signature: str) -> list[str]:
    pictures = PICTURE.findall(visible)
    if len(pictures) != 1:
        return [f"{label} should contain one signature <picture>, found {len(pictures)}"]
    block = pictures[0]
    light = REMOTE_LIGHT if signature == "remote" else LOCAL_LIGHT
    dark = REMOTE_DARK if signature == "remote" else LOCAL_DARK
    errors = []
    if 'href="https://opc.fish"' not in visible:
        errors.append(f"{label} signature link must be https://opc.fish")
    if 'media="(prefers-color-scheme: dark)"' not in block or f'srcset="{dark}"' not in block:
        errors.append(f"{label} is missing the dark signature source")
    img = re.search(r"<img\b([^>]*)>", block, re.I)
    if not img:
        return errors + [f"{label} signature is missing an img"]
    attrs = img.group(1)
    if f'src="{light}"' not in attrs:
        errors.append(f"{label} is missing the light signature src")
    if 'width="720"' not in attrs:
        errors.append(f'{label} signature width must be 720')
    alt = re.search(r'alt="([^"]+)"', attrs)
    if not alt or not alt.group(1).strip():
        errors.append(f"{label} signature needs a descriptive alt")
    return errors


def strip_fences(text: str) -> str:
    return FENCE.sub("", text)


if __name__ == "__main__":
    sys.exit(main())
