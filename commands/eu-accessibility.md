# Accessibility (EAA / EN 301 549)

Turn "make it accessible" into numbered, testable acceptance criteria. This is
the only regime in the repo that is fully testable — use that.

> **Not legal advice.** Scope, the microenterprise exemption and any
> disproportionate-burden claim are legal judgements.

## Ask

1. "What is the primary task users come here to do? Name the top three." —
   accessibility is assessed on **journeys**, not pages. This makes the work
   finishable.
2. "Can each be completed with a keyboard only, at 200% zoom, with a screen
   reader?" — the honest triage.
3. "Which surfaces: web, native mobile, email, PDFs, video, kiosk?" — PDFs (§ 10)
   and video are the two that get forgotten and cost the most to retrofit.
4. Headcount / turnover / balance sheet — the microenterprise **service**
   exemption needs **both** limbs (<10 staff AND ≤€2M).
5. "Is there an existing audit or statement?" — its **date** matters more than
   its contents. Older than the last redesign = evidence about dead software.

## Build against EN 301 549

It is the harmonised standard, so conformity gives a **presumption of
conformity** — a legal effect and the cheapest route. v3.2.1 references WCAG 2.1
AA; later versions align with 2.2. *Check which version the current OJ list
cites.* Target **WCAG 2.2 AA** anyway: superset, cheap extras, future-proof.

Clause groups: § 9 web · § 10 non-web documents · § 11 software · **§ 12 support
services** (your help desk and docs are in scope — a perfect product with an
inaccessible chat widget fails) · § 6 two-way comms · § 8 hardware/terminals.

## Produce

Numbered acceptance criteria, one per applicable clause, each citing
`EN 301 549 § X.Y.Z (WCAG N.N.N)`, tagged `automated` or `manual`, with a journey
and an evidence path.

**Automated tooling catches roughly a third of WCAG failures.** axe/Lighthouse/
pa11y find missing alt text, contrast, labels and landmarks; they cannot tell you
whether the alt text is *right*, whether focus order preserves meaning, or
whether an error message is understandable. **Never report an automated pass as
conformance.**

CI gate on the **journeys only** — a gate that fails on a marketing-page typo
gets disabled, and then checkout regresses unnoticed.

Accessibility statement: standard and version, **what is not accessible with
reasons and dates**, any disproportionate-burden claim, a feedback mechanism, and
the date and method of the last assessment. A statement claiming full conformity
with no exceptions reads as untested. Public sector bodies must use the
prescribed model format (Implementing Decision (EU) 2018/1523).

Manual evidence per journey: keyboard only, screen reader (named, with version),
200% zoom, 320px viewport, dated.

**Disproportionate burden** must be assessed, documented, quantified and
periodically reassessed. An undocumented claim is not a derogation — it is a
written admission.

## Verify

`pytest -q`: every criterion cites a numbered clause; automated share is under
half; an automated pass is not reported as conformance; the microenterprise test
needs both limbs and records an expiry; §§ 10 and 12 are in scope when documents
and support exist; a burden claim requires a quantified document; the statement
lists known gaps; a manual pass with no evidence file is a finding; the CI gate
covers journeys not every page; an accessibility-overlay dependency is a finding.

Report criteria total, automated/manual split, pass rate on each, and journeys
fully covered — **lead with the manual pass rate**, because the automated one
flatters. Say which EN 301 549 version you assessed against and that you could
not verify which version the OJ currently cites.

Then: get one person who uses a screen reader daily through the primary journey.
No tool substitutes for it.
