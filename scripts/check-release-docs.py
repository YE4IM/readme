#!/usr/bin/env python3
"""Check the Markdown structure of delivered Release and CHANGELOG files."""

import argparse
import re
from datetime import date
from functools import lru_cache
from pathlib import Path


HEADING = re.compile(r"^ {0,3}(#{1,6})[ \t]+(.+?)(?:[ \t]+#+)?[ \t]*$", re.M)
FENCE = re.compile(r"^ {0,3}(\x60{3,}|~{3,})(.*)$")
ALERT = re.compile(r"^> \[!(WARNING|IMPORTANT)\][ \t]*$", re.M)
FIELD = re.compile(r"\{\{\s*(TODO(?:\s*[:：][^{}]*)?|[A-Z][A-Z0-9_]*)\s*\}\}")
BROKEN_SECTION = {"Breaking Changes", "破坏性变更"}
MIGRATION = re.compile(r"(?im)^\s*\*\*(?:Migration|迁移步骤)[:：]\*\*[ \t]*$")
VERSION_DATE = re.compile(r"^(.+?)[ \t]+[-–—][ \t]+(\d{4}-\d{2}-\d{2})(?:[ \t].*)?$")
UNRELEASED = {"unreleased", "未发布"}
LANGUAGE_TITLE = {"english", "中文", "简体中文", "chinese"}


def visible_markdown(text):
    """Hide fenced examples before checking layout."""
    fence = None
    visible = []
    for line in text.splitlines():
        marker = FENCE.match(line)
        if fence:
            visible.append("")
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                fence = None
        elif marker:
            fence = marker[1]
            visible.append("")
        else:
            visible.append(line)
    return "\n".join(visible)


INLINE_CODE = re.compile(r"(?<!`)(`+)(?!`)(?:(?!\n[ \t]*\n).)*?(?<!`)\1(?!`)", re.S)
ROOT = Path(__file__).resolve().parents[1]


@lru_cache(maxsize=None)
def template_fields(template):
    return set(FIELD.findall((ROOT / template).read_text(encoding="utf-8")))


def residue_errors(text, visible, template, *, draft):
    errors = []
    if re.search(r"(?im)<!--(?:(?!-->).)*?(?:OPTIONAL|REQUIRED)|^[ \t]*OPTIONAL:", text, re.S):
        errors.append("template instructions remain")
    prose = INLINE_CODE.sub(" ", visible)
    checked_fields = set(FIELD.findall(prose)) | template_fields(template)
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
    for heading, body in sections(visible, level):
        if heading in BROKEN_SECTION:
            migration = MIGRATION.search(body)
            steps = body[migration.end():] if migration else body
            if not re.search(r"(?m)^ {0,3}1[.)][ \t]+\S", steps) and not (
                draft and re.search(r"\{\{\s*TODO(?:\s*[:：]|\s*\}\})", steps)
            ):
                errors.append(f"{heading} needs numbered migration steps or a draft TODO")
    return errors


def check_release(text, *, draft=False, prerelease=False):
    visible = visible_markdown(text)
    errors = residue_errors(text, visible, "releases readme/release-template.md", draft=draft)
    parts = re.split(r"(?m)^[ \t]*---[ \t]*$", visible)
    if len(parts) != 2 or any(not part.strip() for part in parts):
        return errors + ["expected English and Chinese release notes separated by one --- line"]
    layouts = []
    for label, part in zip(("English", "Chinese"), parts):
        part = part.strip()
        if part.startswith(("#", ">", "<!--")):
            errors.append(f"{label} release notes must begin with a summary")
        headings = list(HEADING.finditer(part))
        alerts = ALERT.findall(part)
        if any(len(heading[1]) != 2 for heading in headings):
            errors.append(f"{label} release sections must use level-two headings")
        if any(
            heading[2].casefold() in LANGUAGE_TITLE
            or re.match(r"(?i)^v?\d+(?:[.\-]|$)", heading[2])
            for heading in headings
        ):
            errors.append(f"{label} release notes contain a language or version heading")
        if prerelease and "WARNING" not in alerts:
            errors.append(f"{label} pre-release needs a WARNING")
        errors.extend(f"{label}: {error}" for error in section_errors(part, 2, draft=draft))
        layouts.append(([len(heading[1]) for heading in headings], alerts))
    if layouts[0] != layouts[1]:
        errors.append("English and Chinese release heading levels or alert types differ")
    return errors


def heading_label(title):
    return re.sub(r"^\[([^\]]+)\](?:\(.*\))?$", r"\1", title)


def changelog_entries(text, *, draft):
    visible = visible_markdown(text)
    errors = residue_errors(text, visible, "changelog readme/changelog-version-template.md", draft=draft)
    entries = []
    seen_versions = set()
    for heading, body in sections(visible, 2):
        if heading_label(heading).casefold() in UNRELEASED:
            if entries:
                errors.append("Unreleased must be the first CHANGELOG entry")
            label = "Unreleased"
        else:
            datestamp = VERSION_DATE.fullmatch(heading)
            if datestamp:
                label = heading_label(datestamp[1])
                try:
                    date.fromisoformat(datestamp[2])
                except ValueError:
                    errors.append(f"{heading} has an invalid calendar date")
                label = (label, datestamp[2])
            elif draft and "{{TODO" in heading:
                label = heading_label(heading.split("{{TODO", 1)[0].rstrip(" -–—"))
            else:
                errors.append(f"{heading} needs a version and a YYYY-MM-DD date")
                label = heading
        version = label[0] if isinstance(label, tuple) else label
        if version in seen_versions:
            errors.append(f"duplicate CHANGELOG entry: {heading}")
        seen_versions.add(version)
        entries.append(label)
        errors.extend(section_errors(body, 3, draft=draft))
    if not entries:
        errors.append("expected at least one level-two version or Unreleased heading")
    return entries, errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="kind", required=True)
    release = subparsers.add_parser("release", help="check one bilingual GitHub Release body")
    release.add_argument("body", type=Path)
    release.add_argument("--prerelease", action="store_true")
    changelog = subparsers.add_parser("changelog", help="check two Markdown CHANGELOG files")
    changelog.add_argument("english", type=Path)
    changelog.add_argument("chinese", type=Path)
    for mode in (release, changelog):
        mode.add_argument("--draft", action="store_true", help="allow editorial TODOs")
    args = parser.parse_args()
    try:
        if args.kind == "release":
            errors = check_release(args.body.read_text(encoding="utf-8"), draft=args.draft, prerelease=args.prerelease)
        else:
            en, en_errors = changelog_entries(args.english.read_text(encoding="utf-8"), draft=args.draft)
            zh, zh_errors = changelog_entries(args.chinese.read_text(encoding="utf-8"), draft=args.draft)
            errors = [f"{path}: {error}" for path, found in ((args.english, en_errors), (args.chinese, zh_errors))
                      for error in found]
            if en != zh:
                errors.append("CHANGELOG versions, dates or order differ between languages")
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
