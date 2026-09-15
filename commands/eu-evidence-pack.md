# Evidence pack

Assemble what a regulator, auditor or acquirer actually asks for. The property
that matters: **evidence has to exist before you need it.** Every document here
is trivial to produce while building and nearly impossible to reconstruct
honestly eighteen months later.

> **Not legal advice.** A complete pack is material for an opinion, not the
> opinion.

## Ask

1. "Who is asking, and what for?" — a customer questionnaire, a data room and a
   supervisory authority want different subsets. Assembling everything for a
   questionnaire wastes a week.
2. "What exists, and when was it last true?" — dates matter more than contents.
3. "Name every processor, and where is the signed DPA for each?" — the gap
   between the vendor list and the DPA folder is usually the largest finding.
4. "Who is the accountable owner for each document?"
5. "Is there anything in here you would not want read aloud?" — ask it directly,
   now rather than later.

## Generate what can be generated

The most credible parts of a pack are the parts nobody wrote. A generated
artifact with a commit hash cannot have been written the week the letter arrived.

| Artifact | By | Duty |
| --- | --- | --- |
| SBOM | `syft`/`cdxgen` at build | CRA Annex I Part II |
| ROPA | from the data map | GDPR Art. 30 |
| Erasure test result | CI | Art. 17 — **proves** it works |
| Restore test result | CI | NIS2 Art. 21(2)(c) needs a *tested* restore |
| Consent log | the consent mechanism | Art. 7(1) demonstrability |
| Accessibility report | axe + manual, dated | EAA |
| Decision records | git | Art. 5(2) accountability |

## Produce

`compliance/` in the repository, next to the code: the brief, the ROPA,
`decisions/` (ADRs), `vendors/` (one file each), `dpia/`, `ai/` (Annex IV,
logs design), `sbom/`, `incidents/`, `statements/`, `tests/`, `COMPLETENESS.md`.

**The vendor file** is shaped so the gaps are visible: `dpa`, `subprocessors`
(`named: false` is a finding — Art. 28(2)), `location` including **support
access**, `transfer` with mechanism and TIA (`tia: null` is a finding),
`breach_notice_period` (the field nobody thinks about and the one that matters
most — 72 hours agreed means your whole GDPR window is gone before you knew),
`audit_rights`, `deletion_on_termination`, `reviewed`.

**The decision record** must include **options rejected, with reasons**. A record
stating only the outcome reads as reverse-engineered. This is the section
diligence reads most closely and almost nobody writes.

**Completeness is counted, never a percentage**: "37 of 41 present, 4 contain
unfilled placeholders, 2 are past their review period". A percentage invites a
target and the target gets met by loosening definitions.

**Never fill a placeholder with plausible text.** A fabricated provenance
paragraph in a document you are legally required to keep accurate is the worst
outcome in this skill. Keep the markers, count them, let the count be
uncomfortable.

## Verify

`pytest -q`: required documents follow the applicable regimes; every claimed
document exists and is non-empty; placeholders are counted not hidden; no
completeness percentage is reported; the vendor list reconciles with the runtime
manifest; a vendor without a DPA is a **blocker** (Art. 28(3)); a long vendor
notice period is a finding; decision records include rejected options; stale
documents are flagged; ruled-out regimes are rendered **in full with their
`expires_if`**; the pack makes no compliance claim; generated artifacts carry a
commit and a date.

Report the counts plus: vendors with no DPA, vendors with no TIA where a transfer
exists, and the longest breach notice period. Then hand the pack to someone who
was not interviewed and ask them to find a claim they know is wrong.
