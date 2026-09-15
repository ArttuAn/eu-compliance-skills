# CRA — secure by design

Cybersecurity as a market-access condition. Scope first, because the answer is
counterintuitive: **pure SaaS is generally out; monetised open source is
generally in.**

> **Not legal advice.** Scope, classification and the conformity route are legal
> judgements.
>
> **Dates move.** Reporting obligations expected from 11 Sep 2026, main
> obligations from 11 Dec 2027 — **verify against the consolidated text**. The
> reporting duty arriving first changes what to build first.

## Ask

1. "Is anything you make installed or run on a machine you do not operate?" —
   binaries, containers, SDKs, agents, firmware. The scope question in
   engineering terms.
2. "Is it sold, licensed, bundled or monetised in any way — paid tier, paid
   support, dual licence?" — the commercial-activity limb for open source.
3. "How long will you ship security updates, from when? What happens at the end,
   and how will users know?"
4. "Can your build produce an SBOM today? Show me."
5. "Where does someone report a vulnerability, and who reads that inbox?"
6. "At your last release, did you know of any unpatched exploitable vulnerability
   in it?" — Annex I Part I. Usually surfaces a stale transitive dependency.

## Build

**Annex I Part I** (product properties): no known exploitable vulnerabilities at
delivery; secure by default with a reset path; authentication; confidentiality
and integrity; **data minimisation** (yes, in a cybersecurity regulation);
resilience and DoS protection; minimised attack surface; **security logging with
a user opt-out**; secure update mechanism.

**Annex I Part II** (vulnerability handling): SBOM covering at least top-level
dependencies in a machine-readable format; remediate without delay with **free**
security updates; regular testing; public disclosure once fixed; a published CVD
policy and contact; secure, verifiable update distribution.

**Art. 14 reporting**, from **awareness**: 24h early warning → 72h notification →
14 days final (vulnerability) or 1 month (incident), to the CSIRT and ENISA.

**Support period**: at least 5 years or the expected lifetime if shorter, stated
at the point of sale.

## Produce

```bash
syft dir:. -o cyclonedx-json > compliance/sbom/$(git describe --tags).cdx.json
grype sbom:compliance/sbom/$(git describe --tags).cdx.json --fail-on high
```

The second line **is** the Annex I Part I requirement as a build step. An SBOM
with no vulnerability gate satisfies the paperwork and not the requirement. A
hand-written SBOM is stale on day one and worse than none, because it looks
authoritative.

Plus: `/.well-known/security.txt` and `SECURITY.md` naming an inbox a **named
person** triages; the support period in the docs, the declaration and the brief,
with an end-of-life notice **in the product**; vulnerability handling records
including the ones you decided not to report, with the reasoning; a technical
documentation skeleton; and a **tested** 24-hour reporting path — one that has
never been exercised is a document, not a capability.

## Verify

`pytest -q`: SaaS-only is out of scope **with an expiry naming agents/binaries**;
shipping an agent puts it in scope; monetised OSS is in and non-monetised is out;
the SBOM is generated not hand-committed, parses, and covers top-level deps; a
known-exploitable dependency blocks the release; the support period is recorded
and non-zero and its absence is a condition; the CVD contact resolves to a named
owner; clocks compute from awareness (24h/72h/14d); non-reported vulnerabilities
record their reasoning; dates carry verification notes.

Report SBOM component count and format, open known-exploitable findings at HEAD,
the support period, whether the CVD contact has a named owner, and whether the
drill has run. Then **send a report to your own published address from outside**
and time how long it takes to reach a human who can act. That number is usually a
surprise.
