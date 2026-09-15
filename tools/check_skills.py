#!/usr/bin/env python3
"""Validate every skill in this repo.

The point of a skill library is that its contents are trustworthy on sight: the
code blocks compile, the frontmatter loads in both IDEs, every skill carries the
sections that make it worth more than the model's own priors, and -- in this repo
specifically -- every skill asks before it builds and refuses to state a legal
conclusion. Runs in CI; no network, no API key.

    python3 tools/check_skills.py [--quiet]
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
COMMANDS = ROOT / "commands"
REFERENCES = ROOT / "references"

PREFIX = "eu-"

# The load-bearing sections. "Ask first" is this repo's signature: a skill that
# builds without asking is the thing this library exists to prevent.
REQUIRED_SECTIONS = [
    "## Use this when",
    "## Ask first",
    "## What the law requires",
    "## What to produce",
    "## Failure modes",
    "## Verify",
]

# Every skill must point at the shared contracts rather than restating them.
REQUIRED_CITATIONS = ["references/verification.md"]

# Non-negotiable in a repo that writes about regulation.
DISCLAIMER = "Not legal advice"

FENCE = re.compile(r"^```(\w+)?[ \t]*$")
PLACEHOLDER = re.compile(r"<[a-z][a-z0-9_.\- ]*>")


def code_blocks(text: str, lang: str) -> list[tuple[int, str]]:
    blocks: list[tuple[int, str]] = []
    current: list[str] | None = None
    start = 0
    for number, line in enumerate(text.splitlines(), 1):
        match = FENCE.match(line)
        if match and current is None:
            if (match.group(1) or "") == lang:
                current, start = [], number + 1
        elif line.strip() == "```" and current is not None:
            blocks.append((start, "\n".join(current)))
            current = None
        elif current is not None:
            current.append(line)
    return blocks


def check_python(path: Path, text: str, errors: list[str]) -> int:
    checked = 0
    for start, source in code_blocks(text, "python"):
        checked += 1
        cleaned = PLACEHOLDER.sub("PLACEHOLDER", source)
        try:
            ast.parse(cleaned)
        except SyntaxError as exc:
            line = start + (exc.lineno or 1) - 1
            errors.append(
                f"{path.relative_to(ROOT)}:{line}: python block does not parse — {exc.msg}"
            )
    return checked


def check_json(path: Path, text: str, errors: list[str]) -> int:
    checked = 0
    for start, source in code_blocks(text, "json"):
        checked += 1
        try:
            json.loads(source)
        except json.JSONDecodeError as exc:
            errors.append(
                f"{path.relative_to(ROOT)}:{start + exc.lineno - 1}: "
                f"json block is invalid — {exc.msg}"
            )
    return checked


def check_yaml(path: Path, text: str, errors: list[str]) -> int:
    """Only if PyYAML is available; the repo must validate without it."""
    try:
        import yaml
    except ImportError:
        return 0
    checked = 0
    for start, source in code_blocks(text, "yaml"):
        checked += 1
        try:
            yaml.safe_load(source)
        except yaml.YAMLError as exc:
            errors.append(f"{path.relative_to(ROOT)}:{start}: yaml block is invalid — {exc}")
    return checked


def check_frontmatter(path: Path, text: str, errors: list[str]) -> dict[str, str]:
    if not text.startswith("---\n"):
        errors.append(f"{path.relative_to(ROOT)}: missing YAML frontmatter")
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        errors.append(f"{path.relative_to(ROOT)}: frontmatter is not terminated")
        return {}

    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if line.strip() and not line.startswith((" ", "#")) and ":" in line:
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip().strip('"').strip("'")

    for required in ("name", "description"):
        if not fields.get(required):
            errors.append(f"{path.relative_to(ROOT)}: frontmatter missing '{required}'")

    expected = f"{PREFIX}{path.parent.name}"
    if fields.get("name") != expected:
        errors.append(
            f"{path.relative_to(ROOT)}: frontmatter name '{fields.get('name')}' "
            f"does not match directory (expected '{expected}')"
        )
    if len(fields.get("description", "")) > 220:
        errors.append(f"{path.relative_to(ROOT)}: description is too long to skim (>220 chars)")
    return fields


def check_sections(path: Path, text: str, errors: list[str]) -> None:
    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"{path.relative_to(ROOT)}: missing required section '{section}'")


def check_disclaimer(path: Path, text: str, errors: list[str]) -> None:
    if DISCLAIMER not in text:
        errors.append(f"{path.relative_to(ROOT)}: missing the '{DISCLAIMER}' notice")
    if text.count(DISCLAIMER) > 3:
        errors.append(
            f"{path.relative_to(ROOT)}: repeats the disclaimer {text.count(DISCLAIMER)} times — "
            f"constant hedging teaches the reader to skip it"
        )


def check_citations(path: Path, text: str, errors: list[str]) -> None:
    for citation in REQUIRED_CITATIONS:
        if citation not in text:
            errors.append(f"{path.relative_to(ROOT)}: never cites '{citation}'")


URL = re.compile(r"https?://\S+")


def check_links(path: Path, text: str, errors: list[str]) -> None:
    # URLs contain path segments that look like repo paths ("...-skills/main/...").
    text = URL.sub(" ", text)
    for name in set(re.findall(r"references/([a-z0-9-]+\.md)", text)):
        if not (REFERENCES / name).exists():
            errors.append(f"{path.relative_to(ROOT)}: cites missing references/{name}")
    for name in set(re.findall(r"skills/([a-z0-9-]+)(?:/|\b)", text)):
        if name not in {"<skill>"} and not (SKILLS / name).exists():
            errors.append(f"{path.relative_to(ROOT)}: cites missing skills/{name}")


def check_schema() -> list[str]:
    path = ROOT / "schema" / "compliance.schema.json"
    if not path.exists():
        return ["schema/compliance.schema.json is missing"]
    try:
        schema = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"schema/compliance.schema.json is invalid — {exc}"]

    errors = []
    ruled_out = (schema["properties"]["regimes"]["properties"]["ruled_out"]["items"])
    if "expires_if" not in ruled_out.get("required", []):
        errors.append("schema: ruled_out entries must require 'expires_if'")
    accepted = schema["properties"]["accepted_risks"]["items"]
    for field in ("accepted_by", "review_by", "rationale"):
        if field not in accepted.get("required", []):
            errors.append(f"schema: accepted_risks must require '{field}'")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    errors: list[str] = check_schema()
    skills = sorted(p for p in SKILLS.glob("*/SKILL.md"))
    if not skills:
        print("no skills found", file=sys.stderr)
        return 1

    total_blocks = 0
    for path in skills:
        text = path.read_text(encoding="utf-8")
        check_frontmatter(path, text, errors)
        check_sections(path, text, errors)
        check_disclaimer(path, text, errors)
        check_citations(path, text, errors)
        check_links(path, text, errors)
        total_blocks += check_python(path, text, errors)
        total_blocks += check_json(path, text, errors)
        total_blocks += check_yaml(path, text, errors)

        command = COMMANDS / f"{PREFIX}{path.parent.name}.md"
        if not command.exists():
            errors.append(
                f"skills/{path.parent.name}: no matching "
                f"commands/{PREFIX}{path.parent.name}.md"
            )

    for path in sorted(COMMANDS.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        total_blocks += check_python(path, text, errors)
        total_blocks += check_json(path, text, errors)
        check_disclaimer(path, text, errors)
        if not (SKILLS / path.stem.removeprefix(PREFIX) / "SKILL.md").exists():
            errors.append(f"{path.relative_to(ROOT)}: no matching skill directory")

    for path in sorted(REFERENCES.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        total_blocks += check_python(path, text, errors)
        total_blocks += check_yaml(path, text, errors)
        check_links(path, text, errors)

    readme = ROOT / "README.md"
    if readme.exists():
        text = readme.read_text(encoding="utf-8")
        check_links(readme, text, errors)
        for path in skills:
            if f"{PREFIX}{path.parent.name}" not in text:
                errors.append(f"README.md: does not list skill '{PREFIX}{path.parent.name}'")

    if errors:
        print(f"FAIL — {len(errors)} problem(s):\n")
        for error in errors:
            print(f"  {error}")
        return 1

    if not args.quiet:
        print(
            f"OK — {len(skills)} skills, {total_blocks} code blocks compiled, "
            f"{len(REQUIRED_SECTIONS)} required sections present in each, "
            f"disclaimer present everywhere, all links resolve, schema enforces "
            f"expires_if and named acceptance"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
