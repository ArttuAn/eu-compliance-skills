#!/usr/bin/env python3
"""Deterministic certainty engine.

The brief carries the trace; this engine derives every certainty number from
the trace. A number the trace cannot support is not a style problem -- it is a
failure, and tools/hard_gate.py makes that failure a gate.

This module is pure: same trace in, same numbers out, on any machine. The agent
may not type a certainty; it supplies the trace, and the numbers follow.
    references/certainty.md documents the anchors this implements.

    python3 tools/certainty_engine.py brief.yaml   # print derived numbers as JSON
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INSTRUMENTS = json.loads(
    (ROOT / "tools" / "instruments.json").read_text(encoding="utf-8")
)

# regime (the schema enum) -> the short instrument name used in citations.
REGIME_TO_INSTRUMENT = {
    "gdpr": "GDPR",
    "eprivacy": "ePrivacy",
    "ai_act": "AI Act",
    "eaa": "EAA",
    "cra": "CRA",
    "nis2": "NIS2",
    "dsa": "DSA",
    "data_act": "Data Act",
    "dora": "DORA",
    "pld": "PLD",
    "mdr": "MDR",
    "eidas": "eIDAS 2",
}

INSTRUMENT_NAMES = set(INSTRUMENTS)

# Find the instrument name inside a citation string: "Art. 21(2)(d) NIS2",
# "Art. 6 GDPR", "Annex III(4)(a) AI Act".
ART = re.compile(r"Art\.\s*(\d+)")
NAME = re.compile(r"|".join(re.escape(n) for n in sorted(INSTRUMENT_NAMES, key=len, reverse=True)))

# The six regimes' worth of supported answer grades. VAGUE / EVASIVE must never
# be recorded -- a trace that contains one is itself a violation.
VALID_GRADES = {"specific", "assumed", "unknown"}


def instrument_for(regime: str | None) -> str | None:
    return REGIME_TO_INSTRUMENT.get(regime) if regime else None


def article_of(citation: str | None) -> int | None:
    if not citation:
        return None
    m = ART.search(citation)
    return int(m.group(1)) if m else None


def instrument_of_citation(citation: str | None) -> str | None:
    """Instrument named inside the citation text, if any."""
    if not citation:
        return None
    m = NAME.search(citation)
    return m.group(0) if m else None


def resolve_instrument(citation: str | None, regime: str | None) -> str | None:
    """Citation-first, then the item's regime. Neither naming one is a violation
    for the caller to report."""
    return instrument_of_citation(citation) or instrument_for(regime)


def is_directive(instrument: str | None) -> bool:
    return bool(instrument and INSTRUMENTS[instrument]["type"] == "directive")


def last_article(instrument: str | None) -> int | None:
    if not instrument:
        return None
    return INSTRUMENTS[instrument]["last_article"]


def _grade_of(trace: dict, question: str) -> str | None:
    for entry in trace.get("answers", []):
        if entry.get("question") == question:
            return entry.get("grade")
    return None


def _transposition(trace: dict, instrument: str | None) -> dict | None:
    if not instrument:
        return None
    for entry in trace.get("directives", []):
        if entry.get("instrument") == instrument:
            return entry
    return None


def _verification(trace: dict, citation: str | None) -> dict | None:
    if not citation:
        return None
    for entry in trace.get("verifications", []):
        if entry.get("citation", "").strip() == citation.strip():
            return entry
    return None


def _confirmed(trace: dict, item_id: str | None) -> bool:
    if not item_id:
        return False
    return any(
        c.get("item") == item_id for c in trace.get("confirmations", [])
    )


def derive_item(
    *,
    item_id: str,
    citation: str | None,
    regime: str | None,
    source_kind: str = "answered",
    question: str | None = None,
    requires_confirmation: bool = False,
    asserts_date: bool = False,
    trace: dict,
) -> dict:
    """Derive the certainty for one finding or regime.

    Returns {"certainty": int, "reasons": [str, ...], "violations": [str, ...]}.
    Every violation here is deterministic and independent of the stored number.
    """
    reasons: list[str] = []
    violations: list[str] = []
    value = 95  # any single item starts at the verified ceiling; 100 is brief-level

    instrument = resolve_instrument(citation, regime)
    if citation and not instrument:
        violations.append(
            f"{item_id}: citation '{citation}' names an unknown instrument "
            f"or has no regime to resolve it to"
        )
    elif instrument:
        artic = article_of(citation)
        if artic is not None:
            bound = last_article(instrument)
            if bound is None or artic > bound:
                violations.append(
                    f"{item_id}: 'Art. {artic} {instrument}' is past the end "
                    f"of the instrument (last article {bound})"
                )
        if is_directive(instrument):
            trans = _transposition(trace, instrument)
            if trans is None:
                violations.append(
                    f"{item_id}: {instrument} is a Directive and no Member State "
                    f"transposition is recorded -- a Directive binds through "
                    f"national law"
                )
                value = min(value, 60)
                reasons.append(
                    "directive cited, national transposition not recorded"
                )
            elif not trans.get("transposition_read"):
                violations.append(
                    f"{item_id}: {instrument} transposition for "
                    f"{trans.get('member_state')} recorded but not read"
                )
                value = min(value, 60)
                reasons.append(
                    f"{instrument} transposition ({trans.get('member_state')}) "
                    f"recorded but not read"
                )

    if source_kind == "inferred":
        value = min(value, 90)
        reasons.append("fact read off the code, not answered")
    elif question:
        grade = _grade_of(trace, question)
        if grade == "specific":
            pass
        elif grade == "assumed":
            value = min(value, 80)
            reasons.append(f"answer {question} assumed, verification still open")
        elif grade == "unknown":
            value = min(value, 70)
            reasons.append(f"open UNKNOWN answer {question} underneath")
        else:
            violations.append(
                f"{item_id}: no trace entry for {question} -- the certainty "
                f"cannot be derived from evidence"
            )
            value = min(value, 70)
            reasons.append(f"no trace for {question}")

    if citation and not _verification(trace, citation):
        value = min(value, 90)
        reasons.append(f"citation '{citation}' not verified against EUR-Lex")

    if requires_confirmation and not _confirmed(trace, item_id):
        value = min(value, 50)
        reasons.append("interpretation pending counsel confirmation")

    if asserts_date and not _verification(trace, citation or item_id):
        value = min(value, 45)
        reasons.append("date in flux, not verified against the consolidated text")

    return {"certainty": value, "reasons": reasons, "violations": violations}


def derive_brief(brief: dict) -> dict:
    """Derive per-item numbers and the headline for a whole brief.

    Returns {"items": {path: derived}, "certainty": headline,
             "reasons": [...], "violations": [...], "all_screened": bool}.
    """
    trace = brief.get("trace", {})
    violations: list[str] = []
    items: dict[str, dict] = {}
    item_values: list[int] = []

    def add(path: str, item: dict, source_kind: str = "answered",
            question: str | None = None) -> None:
        derived = derive_item(
            item_id=item.get("id") or item.get("regime") or path,
            citation=item.get("citation"),
            regime=item.get("regime"),
            source_kind=item.get("source", {}).get("kind", source_kind),
            question=item.get("question") or question,
            requires_confirmation=bool(item.get("requires_confirmation")),
            asserts_date=bool(item.get("asserts_date")),
            trace=trace,
        )
        items[path] = derived
        violations.extend(derived["violations"])
        item_values.append(derived["certainty"])

    for index, item in enumerate(brief.get("regimes", {}).get("applicable", [])):
        add(f"regimes.applicable[{index}]", item, question=item.get("question"))
    for index, item in enumerate(brief.get("regimes", {}).get("ruled_out", [])):
        add(f"regimes.ruled_out[{index}]", item, question=item.get("question"))
    for index, item in enumerate(brief.get("findings", [])):
        add(f"findings[{index}]", item)

    reasons: list[str] = []
    head = min(item_values) if item_values else 95

    all_screened = set(trace.get("screened_regimes", [])) >= set(REGIME_TO_INSTRUMENT)
    if not all_screened:
        missing = sorted(set(REGIME_TO_INSTRUMENT) - set(trace.get("screened_regimes", [])))
        violations.append(
            "not every regime in references/regime-map.md was screened -- "
            f"missing: {', '.join(missing) or 'all'}"
        )
        head = min(head, 90)
        reasons.append("not every regime was screened (a regulation may be neglected)")

    # 100 only when every global condition holds -- see references/certainty.md.
    any_open = any(_grade_of(trace, q.get("question")) == "unknown"
                   for q in trace.get("answers", []))
    perfect = (
        head == 95
        and all_screened
        and not any_open
        and all(v["certainty"] >= 95 for v in items.values())
        and not any(v["reasons"] for v in items.values())
    )
    if perfect:
        head = 100

    return {
        "items": items,
        "certainty": head,
        "reasons": reasons,
        "violations": violations,
        "all_screened": all_screened,
    }


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: python3 tools/certainty_engine.py brief.yaml", file=sys.stderr)
        return 2
    try:
        import yaml  # PyYAML, installed in CI and packaged with the tools
    except ImportError:
        print("PyYAML is required for the brief path", file=sys.stderr)
        return 2
    brief = yaml.safe_load(Path(sys.argv[1]).read_text(encoding="utf-8"))
    result = derive_brief(brief)
    print(json.dumps(result, indent=2))
    return 0 if not result["violations"] else 1


if __name__ == "__main__":
    raise SystemExit(main())