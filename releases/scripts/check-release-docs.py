#!/usr/bin/env python3
"""Check the Markdown structure of delivered Release and CHANGELOG files."""

import argparse
import re
from collections import Counter
from datetime import date
from functools import lru_cache
from pathlib import Path


HEADING = re.compile(r"^ {0,3}(#{1,6})[ \t]+(.+?)(?:[ \t]+#+)?[ \t]*$", re.M)
ALERT = re.compile(r"^> \[!(WARNING|IMPORTANT|NOTE)\][ \t]*$", re.M)
FIELD = re.compile(r"\{\{\s*(TODO(?:\s*[:：][^{}]*)?|[A-Z][A-Z0-9_]*)\s*\}\}")
BROKEN_SECTION = {"Breaking Changes", "破坏性变更"}
MIGRATION = re.compile(r"(?im)^\s*\*\*(?:Migration|迁移步骤)(?:[:：]\*\*|\*\*[:：])[ \t]*$")
DATE_VALUE = r"(?:\d{4}-\d{2}-\d{2}|\{\{\s*TODO(?:\s*[:：][^{}\n]*)?\s*\}\})"
VERSION_DATE = re.compile(
    rf"^(?P<version>.+?)[ \t]+(?:[-–—][ \t]+(?P<date>{DATE_VALUE})"
    rf"|\((?P<parenthesized>{DATE_VALUE})\))(?:[ \t]+(?P<status>.+))?$"
)
PRERELEASE_VERSION = re.compile(
    r"(?:[-.](?:alpha|beta|rc|dev|preview|canary|nightly)(?:[.\d+-]|$)"
    r"|(?:^|[/@-])v?\d+(?:\.\d+)*(?:a|b|rc)\d+(?:[.\d+-]|$))",
    re.I,
)
PRERELEASE_LABELS = {"pre-release", "prerelease", "pre release", "预发布", "预发布版"}
STABLE_LABELS = {"stable", "正式版", "稳定版"}
UNRELEASED = {"unreleased", "未发布"}
LANGUAGE_TITLE = {"english", "中文", "简体中文", "chinese"}


INLINE_CODE = re.compile(r"(?<!\x60)(\x60+)(?!\x60)(?:(?!\n[ \t]*\n).)*?(?<!\x60)\1(?!\x60)", re.S)
MARKER = re.compile(r"(?m)^ {0,3}(?:(?P<bt>\x60{3,})[^\x60\n]*|(?P<tilde>~{3,})[^\n]*)$|<!--|\x60+")


def visible_markdown(text, *, keep_comments=False):
    """Keep source line positions while hiding comments and fenced examples."""
    text = text.lstrip("\ufeff")
    visible = []
    start = 0
    while marker := MARKER.search(text, start):
        visible.append(text[start:marker.start()])
        end = marker.end()
        fence = marker["bt"] or marker["tilde"]
        if fence:
            closing = re.compile(r"(?m)^ {0,3}" + re.escape(fence[0]) + rf"{{{len(fence)},}}[ \t]*$")
            close = closing.search(text, end)
            end = close.end() if close else len(text)
            if not keep_comments:
                visible.append("⟦code block⟧")
        elif marker[0] == "<!--":
            close = text.find("-->", end)
            end = close + 3 if close >= 0 else len(text)
            if keep_comments:
                visible.append(text[marker.start():end])
                start = end
                continue
        else:
            span = INLINE_CODE.match(text, marker.start())
            end = span.end() if span else end
            if keep_comments:
                visible.append(" " if "\n" not in text[marker.start():end] else "\n" * text.count("\n", marker.start(), end))
            else:
                visible.append(text[marker.start():end])
            start = end
            continue
        visible.append("\n" * text.count("\n", marker.start(), end))
        start = end
    visible.append(text[start:])
    return "".join(visible)


ROOT = Path(__file__).resolve().parents[2]


def normalize_comment(comment):
    return re.sub(r"\s+", " ", comment).strip()


@lru_cache(maxsize=None)
def template_fields(template):
    return set(FIELD.findall((ROOT / template).read_text(encoding="utf-8")))


@lru_cache(maxsize=None)
def template_comments(template):
    """Instruction comments from the template; any of them left in a delivery is residue."""
    text = (ROOT / template).read_text(encoding="utf-8")
    return {normalize_comment(comment) for comment in re.findall(r"<!--(.*?)-->", text, re.S)}


def residue_errors(text, visible, templates, *, draft):
    if isinstance(templates, str):
        templates = (templates,)
    errors = []
    expected_comments = set().union(*(template_comments(t) for t in templates))
    expected_fields = set().union(*(template_fields(t) for t in templates))
    prose = INLINE_CODE.sub(" ", visible)
    unquoted = visible_markdown(text, keep_comments=True)
    comments = re.findall(r"<!--(.*?)-->", unquoted, re.S)
    comment_residue = any(
        re.search(r"(?i)\b(?:OPTIONAL|REQUIRED)\b|必需", comment)
        or normalize_comment(comment) in expected_comments
        for comment in comments
    )
    uncommented_optional = bool(re.search(r"(?m)^[ \t]*OPTIONAL:", prose))
    if comment_residue or uncommented_optional:
        errors.append("template instructions remain")
    checked_fields = set(FIELD.findall(prose)) | expected_fields
    for field in FIELD.finditer(text):
        todo = field[1] == "TODO" or re.match(r"TODO\s*[:：]", field[1])
        if (todo and not draft) or (not todo and field[1] in checked_fields):
            errors.append(f"unresolved {'editorial TODO' if todo else 'template field'}")
    return list(dict.fromkeys(errors))


def sections(visible, level):
    headings = [m for m in HEADING.finditer(visible) if len(m[1]) <= level]
    for index, heading in enumerate(headings):
        if len(heading[1]) == level:
            end = headings[index + 1].start() if index + 1 < len(headings) else len(visible)
            yield heading[2], visible[heading.end():end].strip()


def section_errors(visible, level, *, draft):
    errors = []
    headings = list(sections(visible, level))
    for index, (heading, body) in enumerate(headings):
        if not body:
            errors.append(f"{heading} has no visible content")
        if heading in BROKEN_SECTION:
            if index:
                errors.append(f"{heading} must precede Highlights and other categories")
            migration = MIGRATION.search(body)
            steps = body[migration.end():] if migration else body
            if not re.search(r"(?m)^ {0,3}1[.)][ \t]+\S", steps) and not (
                draft and re.search(r"\{\{\s*TODO(?:\s*[:：]|\s*\}\})", steps)
            ):
                errors.append(f"{heading} needs numbered migration steps or a draft TODO")
        if level == 2 and heading in {"Highlights", "亮点展示"} and index:
            if index > 1 or headings[0][0] not in BROKEN_SECTION:
                errors.append(f"{heading} must follow the summary, alerts and any Breaking Changes")
    return errors


CATEGORY = {
    "破坏性变更": "Breaking Changes", "亮点展示": "Highlights",
    "新增功能": "Added", "行为变更": "Changed",
    "优化与改进": "Changed", "问题修复": "Fixed", "安全修复": "Security",
    "弃用与移除": "Deprecated & Removed", "维护与依赖更新": "Maintenance & Dependencies",
    "安装与升级": "Installation & Upgrade", "已知问题": "Known Issues",
    "贡献者": "Contributors", "完整变更日志": "Full Changelog",
}
KNOWN_CATEGORIES = set(CATEGORY.values())
CATEGORY_TITLES = KNOWN_CATEGORIES | set(CATEGORY)
CATEGORY_TITLES_CF = {title.casefold() for title in CATEGORY_TITLES}
LIST_ITEM = re.compile(r"^ {0,3}(?:[-+*]|\d+[.)])[ \t]+\S", re.M)
# A "#" after "#", a quote, or "=" (as in ##333 or fill="#333") is not an issue reference.
ISSUE = re.compile(r"(?<![A-Za-z0-9_/#\"'=])(?:[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)?#[0-9]+(?![A-Za-z0-9_])")
HANDLE = re.compile(r"(?<![A-Za-z0-9_./-])@[A-Za-z0-9-]+")
LINK = re.compile(r"(?:\[([^\[\]\n]*))?\]\(\s*(?:<([^>]+)>|([^\s)]+))")
IMAGE = re.compile(r"!\[[^\]]*\]\(\s*(?:<([^>]+)>|([^\s)]+))")
IMG_SRC = re.compile(r"<img\b[^>]*\bsrc=[\"']([^\"']+)[\"']", re.I)
ASSET = re.compile(
    r"/(?:releases/(?:download|tag)|compare|pull|issues)/"
    r"|\.(?:zip|gz|tgz|bz2|xz|zst|exe|msi|dmg|pkg|apk|deb|rpm|whl|appimage|flatpak|snap|sha256|sha512|asc|sig)(?:[?#]|$)",
    re.I,
)


DOWNLOAD_LABEL = re.compile(r"\b(?:download|installer|binary|app store|google play)\b|下载|安装包|二进制|应用商店", re.I)
GUIDE_LABEL = re.compile(r"\b(?:guides?|docs?|documentation|instructions?|manuals?|tutorials?)\b|指南|文档|手册|教程|说明", re.I)
GUIDE_PATH = re.compile(r"(?:^|/)(?:docs?|guides?|manual|wiki)(?:/|$)|\.(?:md|html?)$", re.I)
DOWNLOAD_PATH = re.compile(r"/(?:downloads?|releases/[^/]+|artifacts|builds)/|[-/]installer$", re.I)


def shared_link(label, url, category):
    if url.startswith("#"):
        return False
    if category == "Full Changelog" or ASSET.search(url):
        return True
    if category != "Installation & Upgrade":
        return False
    path = url.split("?", 1)[0].split("#", 1)[0]
    if GUIDE_LABEL.search(label) or GUIDE_PATH.search(path):
        return False
    return bool(DOWNLOAD_LABEL.search(label) or DOWNLOAD_PATH.search(path))


DEFINITION = re.compile(r"(?m)^ {0,3}\[([^\]\n]+)\]:[ \t]*(?:<([^>\n]+)>|(\S+))[^\n]*$")
REFERENCE = re.compile(r"(?<!\\)\[([^\]\n]+)\](?:\[([^\]\n]*)\])?(?![(:\[])")

def link_definitions(visible):
    definitions = {}
    errors = []
    for match in DEFINITION.finditer(visible):
        label = match[1].casefold()
        if label in definitions:
            errors.append(f"duplicate link definition: {match[1]}")
        definitions.setdefault(label, match[2] or match[3])
    return definitions, errors


def reference_links(visible, shared_definitions=None):
    """Resolve references in the namespace of the complete Markdown file."""
    if shared_definitions is None:
        definitions, errors = link_definitions(visible)
    else:
        definitions, errors = shared_definitions, []

    stripped = DEFINITION.sub("", visible)
    seen_missing = set()
    for match in REFERENCE.finditer(INLINE_CODE.sub(" ", stripped)):
        if match[2] is None:
            continue
        if match[2] and not match[2].strip():
            continue
        label = (match[2] or match[1]).strip()
        key = label.casefold()
        if label and key not in definitions and key not in seen_missing:
            seen_missing.add(key)
            errors.append(f"missing link definition for {label}")

    def expand(match):
        url = definitions.get((match[2] or match[1]).casefold())
        return f"[{match[1]}]({url})" if url else match[0]

    return REFERENCE.sub(expand, stripped), errors


def section_facts(body, category):
    prose = INLINE_CODE.sub(" ", body)
    shared = [angle or plain for label, angle, plain in LINK.findall(prose)
              if shared_link(label, angle or plain, category)]
    if category == "Highlights":
        shared.extend(angle or plain for angle, plain in IMAGE.findall(prose))
        shared.extend(IMG_SRC.findall(prose))
    # Contributor handles must match on both sides; GitHub usernames are case-insensitive.
    handles = [handle.lower() for handle in HANDLE.findall(prose)] if category == "Contributors" else []
    subheadings = tuple(len(heading[1]) for heading in HEADING.finditer(body))
    return (
        category, len(LIST_ITEM.findall(body)), Counter(ISSUE.findall(prose)), Counter(shared),
        Counter(handles), subheadings,
    )


def structure(part, level):
    first = HEADING.search(part)
    summary = part[:first.start()] if first else part
    facts = [section_facts(summary, "summary")]
    for heading, body in sections(part, level):
        category = CATEGORY.get(heading, heading)
        # Repository-specific translated titles need human review.
        facts.append(section_facts(body, category if category in KNOWN_CATEGORIES else "custom"))
    return facts, ALERT.findall(part)


def warning_errors(part):
    paragraphs = re.split(r"\n[ \t]*\n", part.strip(), maxsplit=1)
    if len(paragraphs) == 2:
        summary, remainder = paragraphs
        block_summary = re.search(r"(?m)^\s*(?:#|>|<details\b|[-*] |⟦code block⟧)", summary)
        warning = re.match(r"^> \[!WARNING\][ \t]*\n(?:>[ \t]*\n)*>[ \t]*[^\s>]", remainder.lstrip("\n"))
        if not block_summary and warning:
            return []
    return ["expected a visible, nonempty WARNING immediately after the summary"]


def check_release(text, *, draft=False, prerelease=False):
    visible = visible_markdown(text)
    errors = residue_errors(text, visible, "releases/release-template.md", draft=draft)
    visible, reference_errors = reference_links(visible)
    errors.extend(reference_errors)
    parts = re.split(r"(?m)^[ \t]*---[ \t]*$", visible)
    if len(parts) != 2 or any(not part.strip() for part in parts):
        return errors + ["expected English and Chinese release notes separated by one --- line"]
    layouts = []
    for label, part in zip(("English", "Chinese"), parts):
        part = part.strip()
        if part.startswith(("#", ">", "<", "⟦code block⟧")):
            errors.append(f"{label} release notes must begin with a summary")
        headings = list(HEADING.finditer(part))
        alerts = ALERT.findall(part)
        seen_h2 = False
        prev_level = 2
        level_error = False
        skip_error = False
        for heading in headings:
            depth = len(heading[1])
            if depth == 1:
                level_error = True
            elif depth == 2:
                seen_h2 = True
            else:
                if not seen_h2 or heading[2].casefold() in CATEGORY_TITLES_CF:
                    level_error = True
                elif depth > prev_level + 1:
                    skip_error = True
            prev_level = depth
        if level_error:
            errors.append(f"{label} release sections must use level-two headings")
        if skip_error:
            errors.append(f"{label} release subheadings must not skip heading levels")
        if any(
            heading[2].casefold() in LANGUAGE_TITLE
            or re.match(r"(?i)^v?\d+(?:[.\-]|$)", heading[2])
            for heading in headings
        ):
            errors.append(f"{label} release notes contain a language or version heading")
        if prerelease or "WARNING" in alerts:
            errors.extend(f"{label}: {error}" for error in warning_errors(part))
        errors.extend(f"{label}: {error}" for error in section_errors(part, 2, draft=draft))
        layouts.append(structure(part, 2))
    if layouts[0] != layouts[1]:
        errors.append("English and Chinese release categories, item counts, references, shared links or alerts differ")
    return errors


def heading_label(title):
    return re.sub(r"^\[([^\]]+)\](?:\(.*\)|\[[^\]]*\])?$", r"\1", title)


def inspect_changelog(text, *, draft, shared_definitions=None):
    visible = visible_markdown(text)
    errors = residue_errors(
        text,
        visible,
        ("changelog/changelog-version-template.md", "changelog/changelog-version-zh-CN-template.md"),
        draft=draft,
    )
    entries = []
    layout = []
    seen_versions = set()
    visible, reference_errors = reference_links(visible, shared_definitions)
    errors.extend(reference_errors)
    previous_date = None
    for heading, body in sections(visible, 2):
        status = ""
        datestamp = VERSION_DATE.fullmatch(heading)
        if datestamp:
            label = heading_label(datestamp["version"])
            if label.casefold() in UNRELEASED:
                errors.append(f"{heading}: Unreleased cannot have a publication date")
            stamp = datestamp["date"] or datestamp["parenthesized"]
            status = (datestamp["status"] or "").strip("()（）").casefold()
            # The residue check already rejects a date TODO in publishable copy.
            if not stamp.startswith("{{"):
                try:
                    current_date = date.fromisoformat(stamp)
                    if previous_date and current_date > previous_date:
                        errors.append(f"{heading} is out of newest-first order")
                    previous_date = current_date
                except ValueError:
                    errors.append(f"{heading} has an invalid calendar date")
                label = (label, stamp)
        elif heading_label(heading).casefold() in UNRELEASED:
            if entries:
                errors.append("Unreleased must be the first CHANGELOG entry")
            label = "Unreleased"
        elif draft and "{{TODO" in heading:
            label = heading_label(heading.split("{{TODO", 1)[0].rstrip(" -–—"))
        else:
            message = "unrecognized version heading format" if re.search(r"\d{4}-\d{2}-\d{2}", heading) else "needs a version and a YYYY-MM-DD date"
            errors.append(f"{heading}: {message}")
            label = heading
        version = label[0] if isinstance(label, tuple) else label
        if version in seen_versions:
            errors.append(f"duplicate CHANGELOG entry: {heading}")
        if version != "Unreleased" and not body:
            errors.append(f"{heading} has no visible content")
        prerelease = bool(PRERELEASE_VERSION.search(version)) or status in PRERELEASE_LABELS
        if prerelease and status in STABLE_LABELS:
            errors.append(f"{heading}: pre-release version has a stable label")
        if prerelease or "WARNING" in ALERT.findall(body):
            errors.extend(f"{heading}: {error}" for error in warning_errors(body))
        seen_versions.add(version)
        entries.append(label)
        target = re.match(r"^\[([^\]]+)\](?:\[([^\]]*)\]|\(([^)]+)\))?", heading)
        url = target[3] if target else None
        if target and not url:
            ref_name = (target[2] or target[1]).strip()
            msg = f"missing link definition for {ref_name}"
            if msg not in errors:
                errors.append(msg)
        layout.append((prerelease, url, structure(body, 3)))
        for subheading in HEADING.finditer(body):
            if subheading[2] in CATEGORY_TITLES and len(subheading[1]) != 3:
                errors.append(f"{heading}: {subheading[2]} must use a level-three heading")
        errors.extend(section_errors(body, 3, draft=draft))
    if not entries:
        errors.append("expected at least one level-two version or Unreleased heading")
    return entries, layout, errors


def changelog_entries(text, *, draft, shared_definitions=None):
    entries, _, errors = inspect_changelog(text, draft=draft, shared_definitions=shared_definitions)
    return entries, errors


def check_changelog(documents, *, draft=False, shared_definitions=None):
    errors = []
    versions = []
    layouts = []
    for name, text in documents:
        entries, layout, found = inspect_changelog(text, draft=draft, shared_definitions=shared_definitions)
        errors.extend(f"{name}: {error}" for error in found)
        versions.append(entries)
        layouts.append(layout)
    if len(documents) == 2:
        if versions[0] != versions[1]:
            errors.append("CHANGELOG versions, dates or order differ between languages")
        elif layouts[0] != layouts[1]:
            for version, en, zh in zip(versions[0], *layouts):
                if en != zh:
                    errors.append(f"{version}: CHANGELOG release status, categories, item counts, references, shared links or alerts differ")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="kind", required=True)
    release = subparsers.add_parser("release", help="check one bilingual GitHub Release body")
    release.add_argument("body", type=Path)
    release.add_argument("--prerelease", action="store_true")
    changelog = subparsers.add_parser("changelog", help="check a single-language file, a translated pair, or a bilingual file")
    changelog.add_argument("english", type=Path, metavar="FILE")
    changelog.add_argument("chinese", type=Path, nargs="?")
    changelog.add_argument("--bilingual", action="store_true", help="check one file with English and Chinese halves separated by ---")
    for mode in (release, changelog):
        mode.add_argument("--draft", action="store_true", help="allow editorial TODOs")
    args = parser.parse_args()
    try:
        if args.kind == "release":
            errors = check_release(args.body.read_text(encoding="utf-8"), draft=args.draft, prerelease=args.prerelease)
        else:
            paths = [args.english]
            if args.chinese:
                paths.append(args.chinese)
            documents = [(path, path.read_text(encoding="utf-8")) for path in paths]
            shared_definitions = None
            reference_errors = []
            if args.bilingual:
                if args.chinese:
                    parser.error("--bilingual accepts a single file")
                source = documents[0][1].lstrip("\ufeff")
                markdown = visible_markdown(source)
                shared_definitions, reference_errors = link_definitions(markdown)
                visible = markdown.splitlines()
                splits = [i for i, line in enumerate(visible) if line.strip() == "---"]
                if len(splits) != 1:
                    errors = ["single-file bilingual format requires one --- separator between languages"]
                else:
                    lines = source.splitlines()
                    cut = splits[0]
                    documents = [("English", "\n".join(lines[:cut])), ("Chinese", "\n".join(lines[cut + 1:]))]
                    errors = reference_errors + check_changelog(documents, draft=args.draft, shared_definitions=shared_definitions)
            else:
                errors = reference_errors + check_changelog(documents, draft=args.draft, shared_definitions=shared_definitions)
    except (OSError, UnicodeError) as error:
        errors = [str(error)]
    if errors:
        for error in errors:
            print(f"FAIL {error}")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
