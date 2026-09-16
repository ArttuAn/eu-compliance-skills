# GDPR data map, ROPA and deletion paths

Build the table everything else hangs off: *field → purpose → lawful basis →
retention → deletion path → recipients*, from the schema and the code, not from
the privacy policy.

> **Not legal advice.** Choosing and defending a basis is a legal judgement.
> Produce the facts, the gaps and the questions.

## Ask, after reading

1. Point me at the schema, migrations and log config — then **enumerate the
   fields yourself and bring a list to correct.** Far more accurate than a blank
   prompt.
2. Per purpose: "if a user told you to stop this tomorrow, what would break?"
   Nothing → not necessary. They can't use the product → contract, not consent.
   We lose insight → legitimate interests, and you owe a balancing test.
3. "Which fields can contain free text a person typed?" — this is where Art. 9
   data hides, and it changes the analysis more than any other answer.
4. "Show me the code that deletes a person — **all** of it: primary tables,
   backups, logs, search index, analytics vendor, CRM."
5. "Who signs off that a basis is correct?" — `basis_confirmed_by` must be a
   person; the gate cannot clear without one.

## The rules that catch the real errors

- **One row per `(field, purpose)`.** A field serving two purposes is two rows
  with potentially two different bases.
- **Consent is usually wrong.** If the service does not work without it, refusal
  is not real, so the consent is invalid. Use contract (Art. 6(1)(b)). Consent is
  also invalid in employment because of the power imbalance.
- **Legitimate interests owes a written, dated LIA.** `lia_required: true` with
  no document is a finding.
- **Art. 9 needs a condition *in addition to* Art. 6**, not instead of.
- **Free text is `special_category: possible`**, never `false`. You cannot know
  what someone typed into a support ticket, and intention is not the test.
- **"As long as necessary" is not a retention period.** Re-ask for a number and
  the job that enforces it.
- **The Art. 30(5) under-250 exemption is a trap** — three cumulative limbs, and
  routine product processing fails "occasional" on its own. Assume the ROPA is
  required.
- **DPIA is required *prior to* processing** (Art. 35). Written after launch, it
  is evidence of the breach. If the risk cannot be mitigated, Art. 36 prior
  consultation is a **blocker**, not a condition.

## Produce

The map in `compliance.yaml`; `compliance/ropa.yaml` **generated** from it, never
hand-written; the erasure code wired to every store; and a
`test_erasure_leaves_nothing` test in CI. That test is the most convincing item
in the entire evidence pack, because it is generated and dated.

Two details usually wrong: **logs get redacted, not deleted** (you need the event
for security — redact the identifier), and **backups** usually cannot be
rewritten, so document the approach (applied on restore, ages out in N days)
rather than claiming an erasure that did not happen.

## Verify

`pytest -q`: every schema field appears in the map; every purpose has exactly one
basis; a special category with no Art. 9 condition is a blocker; free text is
never marked not-special; vague retention is rejected; every field has a deletion
path; **erasure leaves nothing in any store**; consent is rejected where the
service requires the processing; legitimate interests requires an LIA; the DPIA
trigger fires on a statutory limb; prior consultation is a blocker; the ROPA
generates and validates; `basis_confirmed_by` is required before `clear`.

Report four numbers: schema fields vs mapped fields, purposes with an unconfirmed
basis, fields with no deletion path, and whether the erasure test passes. Name
every basis that is your reading rather than a confirmed decision.


Show certainty on every legal-grounded claim, in the brief and in what you say:
each finding, each applicable or ruled-out regime, and the headline carry a
`certainty` 0–100 — the exact percent of the assessment that rests on verified
sources and confirmed facts — stated with the single largest reason it is not
higher. `references/certainty.md` has the anchors; an open unknown caps at 70,
an unread national transposition at 60, a counsel-pending classification at 50.
Certainty never rescues a VAGUE answer or an open blocker.
