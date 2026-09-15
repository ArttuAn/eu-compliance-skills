# Compliance gates — stop the record from rotting

Everything else produces a record of what is true today. This wires it into CI so
the code cannot drift away from it. A dependency is added, a field appears, the
50th person is hired, a due date passes — none of it announces itself, and by the
time anyone notices, the brief describes a product that has not existed for a
year.

> **Not legal advice.** A green build means the code matches the record. It does
> not mean the record is right — and the gate's own output should say so.

## Ask

1. "Which checks should fail the build today, and which should only warn?" — on
   an existing codebase the honest answer is "warn on everything for two weeks".
2. "What is your runtime dependency boundary?" — a linter does not need a DPA,
   and flagging dev dependencies destroys the signal.
3. "Where is the schema of record?"
4. "Who gets the failure?" — a gate failing to nobody gets disabled.
5. "Do you deploy somewhere I can probe?" — the consent and accessibility checks
   need a live URL.

## The checks

- **new-vendor** — a runtime dependency that can receive user data with no file
  in `compliance/vendors/` → fail, cite Art. 28, give the command to fix it.
- **exclusion-expiry** — evaluate every `expires_if` against current brief facts.
  **The most valuable check here.** No machine-evaluable condition → warn.
- **findings** — an open blocker, or an `open` finding past its due date → fail,
  naming the owner.
- **accepted-risk-expired** — `review_by` passed → fail, naming who accepted it.
- **unmapped-field** — a new personal-data field absent from the data map.
- **consent** — a live probe: anything non-essential before consent.
- **artifacts** — SBOM missing for a release tag; placeholder markers rising.

## Adoption, which is the part that decides whether this survives

Start in `warn` mode with a **dated promotion schedule** in
`compliance/gates.yaml`, and an owner per check. Everything enforced on day one
means four hundred failures, `continue-on-error: true`, and a gate that never
comes back. The promotion dates are themselves checked by the gate, which is the
only way they hold.

Run it **on push and on a schedule** — some conditions become true with the
passage of time, not with a commit.

**Annotate the PR, do not just fail it:**

```
::error file=package.json,line=34::[compliance] `@segment/analytics-node` is a new
runtime dependency that can receive user data and has no file in compliance/vendors/.
Art. 28 GDPR requires a written processor contract. Fix: run
`eu-evidence-pack vendor add @segment/analytics-node`, attach the DPA, and record
the transfer mechanism. Owner: @priya
```

"Compliance check failed" teaches people to re-run it. That message gets fixed in
the same pull request.

**Guard the brief itself.** The most corrosive failure is editing the brief to
make the gate pass: derive `status` rather than reading it, require a named human
and a review date for acceptances, and put `compliance/` in CODEOWNERS.

## Verify

`pytest -q`: a new runtime vendor fails and a new dev dependency does not; an
expired exclusion fails and a conditionless one warns; an open blocker fails; an
overdue finding fails naming its owner; an expired acceptance fails; an unmapped
schema field fails; warn mode never exits non-zero; a promotion date moves a
check to fail; `status` is recomputed not read; **every failure carries a fix**;
the gate output makes no compliance claim.

Report checks enabled, warn vs enforce, failures by check, and the promotion
schedule. On an existing codebase report the **initial backlog size** — that is
the honest measure of how far the code had already drifted.

Then introduce real drift deliberately: add a dependency that receives user data,
add a field, bump headcount past the cap. A gate that has never been shown to
fail has not been shown to work.
