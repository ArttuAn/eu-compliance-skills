#!/usr/bin/env python3
"""Catch fabricated citations and legal overreach across the repo.

An agent writing about regulation has one failure mode that dwarfs the rest: a
citation that does not exist, in fluent legal register, that the reader believes.
This catches the mechanically catchable part of that -- see
references/legal-citations.md for the discipline it enforces.

    python3 tools/check_citations.py [--quiet]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Highest article number in each instrument. An article past the end is the most
# common shape of a fabricated citation.
#
# These bounds are deliberately GENEROUS. The goal is catching gross fabrication
# ("Art. 214 GDPR"), not policing the last article of each act -- a bound that is
# a little too high lets one bad citation through, while a bound that is a little
# too low fails the build on a real one, and nobody trusts the checker after that.
LAST_ARTICLE = {
    "GDPR": 99,
    "AI Act": 113,
    "NIS2": 46,
    "DSA": 93,
    "CRA": 75,
    "DORA": 64,
    "Data Act": 50,
    "EAA": 35,
    "ePrivacy": 21,
}

# Which instrument a file is primarily about, so bare "Art. N" can be checked too.
# Most citations in a skill omit the instrument because the section already named it.
FILE_INSTRUMENT = {
    "gdpr-data-map": "GDPR",
    "ai-act": "AI Act",
    "nis2-readiness": "NIS2",
    "dsa-platform": "DSA",
    "cra-secure-by-design": "CRA",
    "consent-and-tracking": "ePrivacy",
}

# "Art. 33(5) GDPR" / "Art. 21(2)(d) NIS2" / "Annex III(4)(a) AI Act"
CITATION = re.compile(
    r"Art\.\s*(\d+)(?:\([^)]*\))*\s+(GDPR|AI Act|NIS2|DSA|CRA|DORA|Data Act|EAA|ePrivacy)"
)
# A bare "Art. N" with no instrument nearby is only acceptable inside a section
# that already named one; we report it as a warning, not an error.
BARE_ARTICLE = re.compile(r"Art\.\s*(\d+)")

# Recitals are interpretive aids. Citing one with a requirement verb is overreach.
RECITAL_REQUIRES = re.compile(
    r"Recital\s+\d+[^.\n]{0,80}\b(requires|mandates|obliges|prohibits)\b", re.I
)

# Legal conclusions an agent must not state. Quoted examples of what NOT to write
# are exempted by the marker below.
CONCLUSIONS = [
    r"\byou are (?:fully )?(?:GDPR[- ])?compliant\b",
    r"\bthis is (?:fully )?compliant\b",
    r"\bis not (?:a )?high[- ]risk\b",
    r"\bthis transfer is lawful\b",
    r"\blegitimate interest(?:s)? applies here\b",
]
CONCLUSION = re.compile("|".join(CONCLUSIONS), re.I)

# Lines that deliberately quote a forbidden phrase in order to forbid it.
EXEMPT_MARKERS = (
    "may not state", "never state", "must not", "do not write", "is not yours to say",
    "assert phrase not in", "assert ", "forbidden", "not a legal conclusion",
    "counterexample", "someone has claimed",
    # "never X" / "rather than X" forbid the thing they quote, even across a line break
    'never "', 'rather than "', "interpretive aids",
)

# Text inside quotation marks is being displayed, not asserted. The repo quotes
# the phrases it forbids in order to forbid them.
QUOTED = re.compile(r"[\"\u201c\u2018\'`]([^\"\u201c\u201d\u2018\u2019\'`\n]{0,200})"
                    r"[\"\u201d\u2019\'`]")


def quoted_spans(line: str) -> list[tuple[int, int]]:
    return [m.span(1) for m in QUOTED.finditer(line)]


def inside_quotes(match, line: str) -> bool:
    start, end = match.span()
    return any(qs <= start and end <= qe for qs, qe in quoted_spans(line))

# Dates must carry either a citation or an instruction to verify.
DATE = re.compile(r"\b(?:\d{1,2}\s+)?(?:January|February|March|April|May|June|July|"
                  r"August|September|October|November|December)\s+\d{4}\b")


def exempt(line: str) -> bool:
    low = line.lower()
    return any(marker in low for marker in EXEMPT_MARKERS)


def default_instrument(path: Path) -> str | None:
    """The instrument a file is primarily about, if any."""
    stem = path.parent.name if path.name == "SKILL.md" else path.stem.removeprefix("eu-")
    return FILE_INSTRUMENT.get(stem)


def check_file(path: Path, errors: list[str], warnings: list[str]) -> int:
    text = path.read_text(encoding="utf-8")
    rel = path.relative_to(ROOT)
    citations = 0
    fallback = default_instrument(path)

    for number, line in enumerate(text.splitlines(), 1):
        explicit = CITATION.findall(line)
        for article, instrument in explicit:
            citations += 1
            last = LAST_ARTICLE[instrument]
            if int(article) > last:
                errors.append(
                    f"{rel}:{number}: 'Art. {article} {instrument}' is past the end of "
                    f"the instrument (last article is {last}) — likely fabricated"
                )
            if int(article) < 1:
                errors.append(f"{rel}:{number}: 'Art. {article}' is not a valid article")

        # Bare "Art. N" on a line that names no instrument: check it against the
        # one the file is about. Skip lines that name a different instrument.
        if fallback and not explicit and not any(
            name in line for name in LAST_ARTICLE if name != fallback
        ):
            for article in BARE_ARTICLE.findall(line):
                citations += 1
                if int(article) > LAST_ARTICLE[fallback]:
                    errors.append(
                        f"{rel}:{number}: 'Art. {article}' (this file is about {fallback}, "
                        f"which ends at Art. {LAST_ARTICLE[fallback]}) — likely fabricated"
                    )

        recital = RECITAL_REQUIRES.search(line)
        if recital and not exempt(line) and not inside_quotes(recital, line):
            errors.append(
                f"{rel}:{number}: a recital is cited with a requirement verb — "
                f"recitals are interpretive aids, not obligations"
            )

        conclusion = CONCLUSION.search(line)
        if conclusion and not exempt(line) and not inside_quotes(conclusion, line):
            errors.append(
                f"{rel}:{number}: states a legal conclusion — write it as a finding "
                f"with the facts, the citation and the open question"
            )

    # Every document that talks about the law must carry the disclaimer once.
    if citations and "Not legal advice" not in text:
        errors.append(f"{rel}: cites legal provisions but carries no 'Not legal advice' notice")

    # Dates need a citation on the line, or a verification instruction in the file.
    if DATE.search(text) and "verify" not in text.lower() and "Art." not in text:
        warnings.append(f"{rel}: contains dates with neither a citation nor a verification note")

    return citations


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []
    total = 0
    files = sorted(
        [*(ROOT / "skills").glob("*/SKILL.md"),
         *(ROOT / "commands").glob("*.md"),
         *(ROOT / "references").glob("*.md")]
    )
    readme = ROOT / "README.md"
    if readme.exists():
        files.append(readme)

    for path in files:
        total += check_file(path, errors, warnings)

    for warning in warnings:
        print(f"  warn: {warning}")

    if errors:
        print(f"\nFAIL — {len(errors)} citation problem(s):\n")
        for error in errors:
            print(f"  {error}")
        return 1

    if not args.quiet:
        print(f"OK — {total} citations checked across {len(files)} files, "
              f"no fabricated article numbers, no recitals cited as requirements, "
              f"no legal conclusions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
