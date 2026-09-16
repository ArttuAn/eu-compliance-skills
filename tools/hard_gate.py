#!/usr/bin/env python3
"""The hard constraint.

The skills are the soft front-end: they instruct the agent what to record.
This tool is the deterministic back-end: it derives every certainty from the
trace, refuses a number the trace cannot support, and refuses a citation the
registry cannot resolve. Same brief in, same result out, on any machine.

    python3 tools/hard_gate.py --brief compliance.yaml                 # block   (CI, default)
    python3 tools/hard_gate.py --brief compliance.yaml --policy record # block + record (agent, pre-build)
    python3 tools/hard_gate.py --brief compliance.yaml --policy warn   # advisory only

Policy decides what a violation does every time it runs:
  block   exit 2 on any violation -- nothing is written
  record  append an append-only finding per violation, normalize numbers, exit 0
  warn    report only, write nothing, exit 0

Anything the agent recorded that the trace cannot support is a violation, not
a preference. VAGUE answers, fabricated article numbers, Directives without a
Member State, and certainty values the trace does not earn are all "-- the
documentation is lying --" level failures.

    EU_COMPLIANCE_POLICY=block|record|warn can default the --policy flag.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

from certainty_engine import (
    VALID_GRADES,
    derive_brief,
)

# A violation that means the record is not trustworthy at all.
INTEGRITY = ("cannot be derived", "unknown instrument", "past the end",
             "no Member State", "no trace entry", "recorded but never", "VAGUE")

SEVERITY = {
    "blocker": 3,
    "condition": 2,
    "note": 1,
}


def _norm(text: str) -> str:
    return " ".join(text.split())


def load_brief(path: Path) -> dict:
    try:
        import yaml
    except ImportError:
        sys.exit("PyYAML is required (pip install pyyaml)")
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def violations_of(brief: dict) -> list[dict]:
    """Every violation, deterministic, each tagged with a signature for
    append-only recording and a severity."""
    out: list[dict] = []
    trace = brief.get("trace")
    if not isinstance(trace, dict):
        out.append({"sig": "HARD:no-trace", "severity": "blocker",
                    "statement": "the brief carries no trace -- certainty cannot "
                                 "be derived, nothing here is trusted"})
        return out

    for entry in trace.get("answers", []):
        grade = entry.get("grade")
        if grade not in VALID_GRADES:
            sig = f"HARD:vague:{entry.get('question')}"
            if not _already_open(brief, sig):
                out.append({"sig": sig, "severity": "blocker",
                            "statement": f"answer {entry.get('question')} was "
                                         f"recorded as '{grade}', but VAGUE and "
                                         f"EVASIVE answers are never recorded"})

    derived = derive_brief(brief)

    for path, item in derived["items"].items():
        base = _item_pointer(brief, path)
        stored = base.get("certainty") if isinstance(base, dict) else None
        want = item["certainty"]
        if stored is None:
            out.append({"sig": f"HARD:no-certainty:{path}", "severity": "blocker",
                        "statement": f"{path} carries no certainty; derived value "
                                     f"is {want}"})
        elif not isinstance(stored, int):
            out.append({"sig": f"HARD:bad-certainty:{path}", "severity": "blocker",
                        "statement": f"{path} certainty '{stored}' is not an integer 0-100"})
        elif stored > want:
            out.append({"sig": f"HARD:drift:{path}", "severity": "blocker",
                        "statement": f"{path} claims certainty {stored} but the trace "
                                     f"earns at most {want} -- difference {stored - want}"})
        elif stored != want:
            # under-claiming is not a violation; record mode normalizes it.
            pass

    head_stored = brief.get("certainty")
    head_want = derived["certainty"]
    if head_stored is None:
        out.append({"sig": "HARD:no-certainty:headline", "severity": "blocker",
                    "statement": "the brief headline carries no certainty"})
    elif not isinstance(head_stored, int):
        out.append({"sig": "HARD:bad-certainty:headline", "severity": "blocker",
                    "statement": f"headline certainty '{head_stored}' is not an integer"})
    elif head_stored > head_want:
        out.append({"sig": "HARD:drift:headline", "severity": "blocker",
                    "statement": f"headline claims certainty {head_stored} but the trace "
                                 f"earns at most {head_want}"})

    for message in derived["violations"]:
        sig = "HARD:" + "".join(c for c in _norm(message) if c.islower() or c.isdigit())[:48]
        if any(v["sig"] == sig for v in out):
            continue
        severity = "blocker" if any(word in message for word in INTEGRITY) else "condition"
        out.append({"sig": sig, "severity": severity, "statement": _norm(message)})

    return out


_POINTER = re.compile(r"(\w+)(?:\[(\d+)\])?")


def _item_pointer(brief: dict, path: str):
    node = brief
    for match in _POINTER.finditer(path):
        node = node[match.group(1)]
        if match.group(2) is not None:
            node = node[int(match.group(2))]
    return node


def _already_open(brief: dict, signature: str) -> bool:
    for f in brief.get("findings", []):
        if f.get("status") == "open" and f.get("statement", "").startswith(f"[hard-gate] {signature}"):
            return True
    return False


def heading_signature(statement: str) -> str:
    key = "".join(c for c in _norm(statement) if c.islower() or c.isdigit())[:48]
    return f"HARD:{key}"


def write_record(brief: dict, violations: list[dict], path: Path) -> None:
    """Normalize every certainty to the derived value and append each violation
    once, append-only, as a finding whose severity drives the gate."""
    import yaml

    derived = derive_brief(brief)
    for item_path, item in derived["items"].items():
        node = _item_pointer(brief, item_path)
        if isinstance(node, dict):
            node["certainty"] = item["certainty"]
    brief["certainty"] = derived["certainty"]

    existing = brief.setdefault("findings", [])
    numbers = [f["id"] for f in existing if f.get("id", "").startswith("F-")]
    high = max((int(n[2:]) for n in numbers), default=0)

    for v in violations:
        statement = f"[hard-gate] {v['sig']} -- {v['statement']}"
        if any(f.get("status") == "open" and f.get("statement") == statement
               for f in existing):
            continue
        # A hard-gate finding records a defect in the record itself. It is an
        # item with no citation and no answering trace, so its own derived
        # ceiling is 95 -- store exactly that, or the engine drifts on its own
        # output and the loop never ends.
        if v["severity"] == "blocker":
            sev = "condition" if "not every regime" in v["statement"] else "blocker"
        else:
            sev = v["severity"]
        high += 1
        existing.append({
            "id": f"F-{high:03d}",
            "severity": sev,
            "regime": "gdpr",
            "statement": statement,
            "needs": "Resolve the underlying trace or record the missing verification.",
            "status": "open",
            "certainty": 95,
        })

    path.write_text(yaml.safe_dump(brief, sort_keys=False), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--brief", required=True, help="path to compliance.yaml")
    parser.add_argument("--policy", choices=["block", "record", "warn"],
                        default=os.environ.get("EU_COMPLIANCE_POLICY", "block"))
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    path = Path(args.brief)
    brief = load_brief(path)
    violations = violations_of(brief)

    if not args.quiet:
        if not violations:
            head = brief.get("certainty", derive_brief(brief)["certainty"])
            print(f"HARD GATE OK -- certainty {head}; every number derived from the trace")
        else:
            print(f"HARD GATE -- {len(violations)} violation(s):")
            for v in violations:
                print(f"  [{v['severity']}] {v['statement']}")

    if not violations:
        return 0
    if args.policy == "block":
        print("blocking: fix the trace or re-run with --policy record", file=sys.stderr)
        return 2
    if args.policy == "record":
        write_record(brief, violations, path)
        if not args.quiet:
            print(f"recorded {len(violations)} append-only finding(s) and normalized "
                  f"certainty; the gate now reflects them")
        return 0
    return 0  # warn


if __name__ == "__main__":
    raise SystemExit(main())