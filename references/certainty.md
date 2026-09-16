# Certainty — the percent you can trust an assessment

The single rule: **anywhere the agent states something legal-grounded, it shows
its certainty as a percentage.** A claim without a certainty is a claim made in
the voice of certainty the work has not earned.

That percentage is **derived, never typed.** The agent records the evidence —
answer grades, verification against EUR-Lex, directive transpositions read,
counsel confirmations — in the brief's `trace`, and `tools/certainty_engine.py`
computes the number. `tools/hard_gate.py` refuses a number the trace cannot
support; a stored certainty that over-claims is a *failure*, not a preference.
Same trace in, same number out, on any machine. This is what makes the scale
deterministic for law purposes instead of a model's guess.

This file is the scale. Every skill cites it, and the alternates are forbidden:
a range ("70–90"), a hedge ("fairly sure"), or no number at all is a finding
that has stopped being honest.

> **Not legal advice.** A certainty is a confidence in the record behind a
> claim, not a probability that the product is lawful. Only a qualified lawyer
> can speak to the second.

## What the percentage is

Not a probability and not a score of how compliant something is. It is the
agent's honest confidence in the **record** behind a legal-grounded claim: how
much of it rests on verified sources and confirmed facts, versus inference,
open unknowns and interpretation that nobody has settled.

A certain claim is one you could defend to an engineer or a regulator the next
morning with the materials in the brief. Everything else is less than 100, and
the number says how much less.

## The anchors

Start from the strongest relevant anchor, then **take the minimum** of every
anchor that applies — a claim is only as certain as its weakest verifying step.

| Anchor | Certainty | When it applies |
| --- | --- | --- |
| **Verified** | 95–100 | Deciding facts are `SPECIFIC` answers, the citation was checked against the consolidated text on EUR-Lex, and the obligation is stable — no date in flux, no contested interpretation |
| **Read off the code** | 90 | Facts read from the repo (a vendor in `package.json`, a field in the schema, a retention cron) and recorded as `inferred` with the reasoning |
| **Assumed, being verified** | 80 | The answer graded `ASSUMED` was turned into a verification task with an owner and a due date and is not yet closed |
| **Open unknown underneath** | 70 | A deciding fact is still `UNKNOWN` — the assessment rests on an unclosed open unknown, and 70 is the ceiling until it closes |
| **Directive, transposition unread** | 60 | A Directive (NIS2, ePrivacy, EAA, PLD) — the EU article is the starting point, the binding text is national, and you have not read that Member State's law |
| **Interpretation pending counsel** | 50 at most | A classification, a lawful-basis conclusion, a transfer mechanism — exactly the things the skills refuse to conclude. Certainty is where that refusal becomes a number |
| **Text in flux** | 45 | Application dates or the instrument itself are subject to amendment and you could not verify the current consolidated state |

Two more rules, because they are where this repo's honesty usually leaks:

- **A fact nobody supplied has no certainty.** If a deciding question was never
  asked or went `VAGUE`, do not invent a percentage for the answer. Record the
  open unknown, and cap at 70 anything whose applicability turns on it.
- **Regime coverage is part of the headline.** `certainty: 100` also requires
  that every regime in `references/regime-map.md` was explicitly screened —
  applied or ruled out with a fact. If the agent cannot say it screened them
  all, the headline is capped at 90 and the unscanned list is stated.

## What 100% requires

All of it, at once — this should be rare early in a project:

- every deciding fact is a `SPECIFIC` answered fact;
- every citation was verified against the consolidated text on EUR-Lex;
- no Directive transposition is unread;
- no date in flux is asserted;
- no interpretation is pending counsel;
- every regime in the map was screened.

If any one is missing, the number says so instead of the prose.

## Where it lives

| Field | Carries | What it means |
| --- | --- | --- |
| Brief top level `certainty` | The whole assessment | The minimum across applicable regimes, open blockers and scanned coverage |
| `regimes.applicable[].certainty` | One regime applies | How sure the trigger fact holds and the trigger citation is right |
| `regimes.ruled_out[].certainty` | One regime is out | How sure the exclusion holds — dropping it later is how exclusions betray you |
| `findings[].certainty` | One finding | How sure the recorded fact, citation and open question are correct |

## Display rule — the agent makes it apparent

Whenever the agent states an applicability, a classification, a
citation-backed obligation or a finding, it states **the percentage and the
single largest reason it is not higher**:

> Ruled out NIS2 — certainty 66%: the Article 21 measures were not read against
> the Finnish transposition law.

> F-002 condition — certainty 71%: the Annex III tier turns on counsel
> confirmation and two open unknowns about the vendor.

Not a range, not a hedge, not a mood. A percentage and a reason. The reader
should be able to ask "why not higher?" and get the same answer the agent would.

## The guardrails

- **Certainty is visibility, not a free pass.** `UNKNOWN` passes and `VAGUE`
  does not; an open blocker stays a blocker; a missing lawful basis stays
  missing. 100% never resurrects a basis nobody documented.
- **A low certainty is not a blocker by itself.** It is a reason to read more,
  ask counsel, or record an unknown — which is the output. Do not inflate a
  note into a blocker because you feel unsure; name the missing verification
  and who will do it.
- **Findings under 60 must say what would raise them.** The missing
  verification, the transposition to read, the counsel confirmation — a finding
  that reports a low number without the way up is a complaint, not a finding.
- **A certainty that never moves is broken.** If every assessment marches out at
  90+, the numbers are decoration; vary with the actual evidence and say so in
  the report.

## What the engine needs from you (the trace)

`tools/hard_gate.py` will refuse a brief that cannot prove its numbers. The
brief's `trace` must therefore contain, for every item that carries a number:

- **`answers`** — the grade (`specific | assumed | unknown`) for every question
  the findings and regimes reference. `VAGUE` / `EVASIVE` in the trace is itself
  a violation. A finding whose question has no entry cannot be derived.
- **`verifications`** — every `citation` you relied on, matched by string, with
  the CELEX number and the date you checked it. An unverified citation caps at
  90; a fabricated citation fails outright.
- **`directives`** — for every Directive cited (NIS2, ePrivacy, EAA, PLD): the
  `member_state` and whether its national transposition was actually read.
  Missing either fails; an unread one caps at 60.
- **`confirmations`** — named human confirmations for items flagged
  `requires_confirmation`; without one the item caps at 50.
- **`screened_regimes`** — every regime you explicitly applied or ruled out.
  A shortlist is exactly the "did we neglect a regulation?" failure: it caps the
  headline at 90 and is reported by name.