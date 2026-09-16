# Which EU regimes apply

From the facts in `compliance/compliance.yaml`, decide what applies — and, more
importantly, record what does not, with the fact that decides it and the
condition that would revive it.

> **Not legal advice.** Produce a defensible first pass and the list of what
> counsel must confirm, not a scoping opinion.

## Ask only what is missing

Headcount / turnover / balance sheet (**at group level**); Member States of
establishment and of sale; whether any part of the group is in a regulated
sector (finance, health, energy, transport, telecoms, public administration);
whether anyone has already scoped this — if so, check theirs rather than writing
a competing document.

## Evaluate the triggers

GDPR (Art. 3: establishment **or** offering/monitoring in the Union) · ePrivacy
(anything non-essential on the device) · AI Act (AI system placed on the market,
put into service, or its output used in the EU) · EAA (covered consumer product
or service) · CRA (product with digital elements, commercial activity) · NIS2
(Annex I/II sector × size cap, **per national law**) · DSA (hosting third-party
information, at any layer) · Data Act · DORA · PLD · MDR.

## The arithmetic, exactly

```python
def nis2_size_cap(headcount, turnover, balance_sheet):
    return headcount >= 50 or turnover > 10_000_000 or balance_sheet > 10_000_000

def eaa_service_microenterprise(headcount, turnover, balance_sheet):
    return headcount < 10 and (turnover <= 2_000_000 or balance_sheet <= 2_000_000)

def dsa_section3_exempt(headcount, turnover):
    return headcount < 50 and turnover <= 10_000_000
```

Three traps: **NIS2 is OR, the EAA microenterprise test is AND** — swapping them
inverts the answer. **The DSA exemption is partial** — hosting duties (Arts.
16-18) have no size exemption, only Section 3 does. **Use group figures** where
the law says to.

**AI Act Art. 6(3)**: the derogation from high-risk is unavailable if the system
**profiles natural persons** — scoring, ranking or categorising individuals is
profiling, however advisory the output. And relying on it requires a documented
assessment *before* placing on the market, plus EU database registration anyway.

## Produce both lists

```yaml
ruled_out:
  - regime: nis2
    reason: "below the size cap in every Member State of establishment"
    deciding_fact: "E-01: 28 staff, EUR 4.2M turnover, EUR 3.1M balance sheet"
    rule: "headcount >= 50 OR turnover > 10M OR balance sheet > 10M"
    confirmed_by: "counsel, 2026-09-10"
    expires_if: "headcount >= 50 or turnover_eur > 10000000"
```

`expires_if` is **mandatory and machine-evaluable where possible** —
`eu-compliance-gates` evaluates it on every push. `deciding_fact` cites a
question id. Never rule out GDPR on "we're not in the EU"; Art. 3(2) exists —
say which limb fails and why.

Then write a short "what we are not doing and why" section in the Markdown
brief. It is the most-read section of the document.

## Verify

`pytest -q`: both lists produced; every exclusion has an expiry and a deciding
fact; NIS2 cap at 49/50 and the OR limbs; EAA needs both limbs; the DSA exemption
keeps Art. 16 and drops Art. 20; an exclusion flips when its fact changes; GDPR
is not ruled out for a non-EU company; profiling blocks Art. 6(3); no legal
conclusions in the rendered output.

Report regimes applicable, ruled out, and how many exclusions have a
machine-evaluable `expires_if` — that ratio predicts whether the scoping survives
a growing company. Name every national transposition you could not read.


Show certainty on every legal-grounded claim, in the brief and in what you say:
each finding, each applicable or ruled-out regime, and the headline carry a
`certainty` 0–100 — the exact percent of the assessment that rests on verified
sources and confirmed facts — stated with the single largest reason it is not
higher. `references/certainty.md` has the anchors; an open unknown caps at 70,
an unread national transposition at 60, a counsel-pending classification at 50.
Certainty never rescues a VAGUE answer or an open blocker.
