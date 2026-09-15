# Evidence

Compliance is not a state of the code. It is a **claim you have to be able to
prove**, months or years later, to someone who was not there and is not inclined
to take your word for it. GDPR calls this accountability (Art. 5(2)); the AI
Act, the CRA and NIS2 all build the same idea into technical documentation and
record-keeping duties.

This file is what "provable" means in practice, and what a regulator, an
auditor, an acquirer's diligence team or an enterprise customer's security
questionnaire will actually ask for.

> **Not legal advice.** This is a practical checklist of documents, not a
> statement of what any particular regulator will accept.

## The uncomfortable property of evidence

**Evidence has to exist before you need it.** Every document below is trivial to
produce while you are building and nearly impossible to reconstruct honestly
eighteen months later — because the people have left, the vendor has changed
their terms, and the decision that seemed obvious at the time is now a story
someone is reconstructing under pressure.

The corollary is the reason these skills ask questions *before* building rather
than auditing afterwards: the moment a decision is made is the only cheap moment
to record why.

## What is actually asked for

### GDPR

| Document | Citation | The question it answers |
| --- | --- | --- |
| Record of processing activities (ROPA) | Art. 30 | What do you process, why, for how long, who gets it |
| Lawful basis per purpose, with an LIA where Art. 6(1)(f) is used | Art. 6, Art. 5(2) | Why were you allowed to do this at all |
| DPIA, where required | Art. 35 | Did you assess the risk to people before you built it |
| Data processing agreements with every processor | Art. 28(3) | Who else touches it, and under what terms |
| Transfer mechanism + transfer impact assessment | Ch. V | How does data leaving the EU stay protected |
| Privacy notice, as actually served | Arts. 13-14 | What were people told, and when |
| Consent records, where consent is the basis | Art. 7(1) | Prove this person agreed, to this, at this time |
| Data subject request log | Arts. 12, 15-22 | Did you answer, and within one month |
| Breach register — **including breaches you did not report** | Art. 33(5) | What happened and why you judged it not notifiable |
| Deletion and retention evidence | Art. 5(1)(e) | Did the data actually go away |

Art. 33(5) is the one teams miss: the register must cover **every** breach, not
just notified ones, *and* record the reasoning for not notifying. A register
containing only reported breaches looks like a register that was started after
the first report.

### AI Act

| Document | Citation | Notes |
| --- | --- | --- |
| Technical documentation | Art. 11, Annex IV | For high-risk systems; substantial, and best written as you build |
| Risk management system records | Art. 9 | Continuous and iterative, not a one-off document |
| Data governance records | Art. 10 | Training/validation/test data provenance, bias examination |
| Automatically generated logs | Art. 12 | **Retained by the provider** where under its control; the log design is an engineering decision made at build time |
| Instructions for use, for deployers | Art. 13 | |
| Human oversight design and evidence it works | Art. 14 | A claim of oversight with no evidence is a finding, not a control |
| Declaration of conformity + CE marking | Arts. 47-48 | |
| EU database registration | Art. 49 | |
| FRIA, where the deployer is in scope | Art. 27 | Overlaps the DPIA; reuse rather than contradict |
| GPAI: technical documentation, copyright policy, training-content summary | Art. 53 | For providers of general-purpose models |

### CRA

- Technical documentation and the EU declaration of conformity.
- **SBOM** covering at least the top-level dependencies (Annex I Part II).
- Coordinated vulnerability disclosure policy, published and reachable.
- Vulnerability handling records, and the security update history.
- The stated **support period** and what happens at its end.
- Reporting records for actively exploited vulnerabilities and severe incidents.

### NIS2

- Evidence that the **management body approved and is trained on** the
  cybersecurity risk-management measures (Art. 20) — this is personal
  accountability for directors and is frequently the first thing asked for.
- Policies covering each of the ten measures in Art. 21(2).
- Incident records and the 24h / 72h / one-month reporting trail.
- Supply chain security assessments for your critical suppliers.

### Accessibility

- Accessibility statement, current and reachable.
- Conformity assessment against EN 301 549 / WCAG, with the test method named.
- Any **disproportionate burden** assessment — documented, quantified, and
  reassessed periodically. An undocumented claim of disproportionate burden is
  not a derogation, it is an admission.

## Evidence that is generated, not written

Most of the list above is prose. The most credible parts are not:

- **An SBOM** produced by the build, not by hand. `syft`, `cdxgen` or your
  package manager's native output, committed per release.
- **A deletion test** that runs in CI: create a subject, exercise the deletion
  path, assert every store is clean. Prove the right to erasure works rather
  than describing it.
- **A consent log** written by the consent mechanism itself, with the version of
  the notice shown. Art. 7(1) requires you to *demonstrate* consent, and
  "the banner was up" is not a demonstration.
- **Model and dataset cards** generated at training time. Retrofitting the
  provenance of a dataset after the fact is usually impossible and always
  unconvincing.
- **Decision records** (ADR-style, in the repo, in git) for every compliance
  choice: the basis chosen and rejected, the classification reached, the
  exclusion relied on. Dated, attributed, diffable — which is more than most
  compliance systems can produce.

A generated artifact with a timestamp and a commit hash is worth more than a
polished PDF, because it cannot have been written the week the letter arrived.

## Where evidence lives

**In the repository, next to the code it describes.** Not in a wiki nobody
edits, not in a drive folder, not in a compliance SaaS that will be churned.

```
compliance/
├── compliance.yaml          # the brief - the machine-readable spine
├── COMPLIANCE-BRIEF.md      # generated from it
├── ropa.yaml                # Art. 30 record, generated from the data map
├── dpia/                    # per-processing assessments
├── decisions/               # ADRs: bases, classifications, exclusions
├── vendors/                 # one file per processor: DPA, sub-processors, location
├── sbom/                    # per-release, generated
├── incidents/               # register, including non-notified, with reasoning
└── statements/              # privacy notice, accessibility statement, CVD policy
```

Three properties this buys you and nothing else does:

1. **It is versioned.** "What did the privacy notice say in March" is `git
   show`, not an archaeology project.
2. **It is reviewable.** A change to the data map arrives in a pull request next
   to the migration that caused it.
3. **It can be checked by CI.** `eu-compliance-gates` reads it on every push and
   fails when the code drifts away from the record.

## The drift problem

Evidence rots the day it is written. A new dependency appears, a vendor adds a
sub-processor, a feature starts collecting a field the ROPA does not mention,
headcount crosses the NIS2 size cap, a model is swapped for one with different
training data.

None of this announces itself. Make the checks mechanical:

- New dependency that receives user data → no vendor record → **fail**.
- New field in the schema → not in the data map → **fail**.
- An exclusion's `expires_if` condition now true → **fail**.
- Privacy notice changed → consent version not bumped → **fail**.
- SBOM missing for the release tag → **fail**.

That is `eu-compliance-gates`, and it is the difference between compliance as a
one-time project and compliance as a property of the repository.

## What good evidence looks like

- **Dated and attributed.** A document with no author and no date is an assertion.
- **It shows the reasoning, not just the outcome.** "Legitimate interests,
  balancing test attached, these alternatives rejected because…" survives
  scrutiny; "Basis: legitimate interests" does not.
- **It records what you decided *not* to do**, and why. The ruled-out regimes,
  the non-notified breaches, the features descoped to stay under a trigger.
  This is the section diligence reads most closely and the one almost nobody
  writes.
- **It is boring.** Evidence written to persuade reads as written to persuade.
  Write it to be checked.
