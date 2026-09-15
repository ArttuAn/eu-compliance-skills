# The regime map

One page: what each EU regime is, the fact that pulls you into it, and what it
costs to be wrong. Use it to decide which skills apply — `eu-applicability` is
the skill that does this properly against a brief.

> **Not legal advice.** This is an engineer's orientation map, not a scoping
> opinion. Applicability turns on facts and on national implementations that
> only a qualified lawyer can settle.

> **Dates move.** Everything below has a date, and EU timelines have been
> amended before — several were still being amended while this was written.
> **Verify every date against EUR-Lex before you rely on it**, and see
> `legal-citations.md` for how to do that and how to write about a date you
> could not verify.

## The triggers, in the order you should check them

| Regime | The fact that pulls you in | Key dates | Exposure |
| --- | --- | --- | --- |
| **GDPR** 2016/679 | You process any data about an identifiable person — including IPs, device IDs and logs — and you are established in the EU **or** you offer goods/services to, or monitor, people in the EU (Art. 3) | In force since 2018 | €20M or 4% of global annual turnover |
| **ePrivacy** 2002/58 (as amended) | You store or read anything on a user's device that is not strictly necessary — cookies, `localStorage`, pixels, fingerprinting | In force; national laws vary | National; often mirrors GDPR levels |
| **AI Act** 2024/1689 | You build, resell, or deploy an AI system in the EU, or its output is used in the EU | Prohibitions + AI literacy from 2 Feb 2025; GPAI from 2 Aug 2025; Annex III high-risk from 2 Aug 2026; Annex I from 2 Aug 2027 — **all subject to amendment, verify** | €35M/7% prohibited; €15M/3% most others |
| **EAA** 2019/882 | You sell covered consumer products or services in the EU — e-commerce, consumer banking, e-books, transport, telephony, AV media access | From 28 Jun 2025 | National; market withdrawal |
| **CRA** 2024/2847 | You place a product with digital elements on the EU market in the course of a commercial activity | Vulnerability reporting from 11 Sep 2026; full obligations from 11 Dec 2027 | €15M/2.5% |
| **NIS2** 2022/2555 | You are a medium-or-larger entity in an Annex I or II sector — including cloud, data centres, MSPs, online marketplaces, search, social platforms | Transposition was due 17 Oct 2024; **national laws differ and several are late** | €10M/2% essential; €7M/1.4% important; management liability |
| **DSA** 2022/2065 | You host information supplied by users, or run an online platform or marketplace | Fully applicable since 17 Feb 2024 | 6% of global annual turnover |
| **Data Act** 2023/2854 | You make a connected product or a related service, or you are a cloud/data-processing provider | Applicable from 12 Sep 2025 | National |
| **DORA** 2022/2554 | You are a regulated financial entity, or a critical ICT provider to one | Applicable since 17 Jan 2025 | Sectoral |
| **PLD** 2024/2853 | You supply software as a product — defective software can now ground a product liability claim | Member State transposition due 9 Dec 2026 | Civil liability, no cap |
| **MDR** 2017/745 | Your software has a medical purpose — diagnosis, prevention, monitoring, treatment | In force | Market withdrawal, criminal in some states |
| **eIDAS 2** 2024/1183 | You accept or issue EU Digital Identity Wallet credentials, or you are a large platform required to accept them | Wallets from Member States expected end-2026 | Sectoral |

## How they stack

The common mistake is picking one regime and treating it as "the compliance
work." Most real products sit under four or five at once, and the obligations
interlock rather than duplicating.

```
Any product touching people in the EU
├── GDPR            data about people           always check first
├── ePrivacy        anything on the device      before any analytics ships
└── PLD             defect liability            from Dec 2026

+ if it contains AI
  └── AI Act        classification first, then obligations follow the tier

+ if it is sold to consumers
  └── EAA           accessibility, from Jun 2025

+ if it is a product placed on the market
  └── CRA           secure by design, SBOM, vulnerability handling

+ if it hosts user content
  └── DSA           notice and action, statements of reasons, T&Cs

+ if the entity is in a critical sector and medium-sized or larger
  └── NIS2          governance, the Art. 21 measures, 24h/72h/1mo reporting
```

**GDPR is almost always in scope and is almost always the thing that actually
bites.** It has the broadest trigger, the longest enforcement record, and the
most data-subject complaints. A project that gets the AI Act classification
beautifully right and has no lawful basis for its training data has failed at
the part that matters.

## Overlaps worth knowing before you scope

- **AI Act × GDPR.** A high-risk AI system's Art. 10 data-governance duties do
  not give you a lawful basis to use the data. You need both, and the AI Act
  says so explicitly. Art. 22 GDPR (solely automated decisions with legal or
  similarly significant effects) applies independently of the AI Act tier.
- **AI Act Art. 27 FRIA × GDPR Art. 35 DPIA.** Different instruments, different
  triggers, overlapping content. Run the DPIA; reuse it where the FRIA allows
  rather than writing two documents that disagree.
- **CRA × NIS2.** CRA regulates the *product* you ship; NIS2 regulates the
  *organisation* running services. A cloud provider selling a device is under
  both, for different things.
- **CRA × AI Act.** For a high-risk AI system that is also a product with
  digital elements, meeting the CRA's cybersecurity requirements can satisfy the
  AI Act's Art. 15 cybersecurity requirement. Do not build two regimes' worth of
  controls for one property.
- **DSA × GDPR.** DSA Art. 26(3) bans ads targeted using special-category data;
  Art. 28(2) bans profiling-based ads to minors. Those are ad-tech constraints
  that live in your recommender, not in your privacy policy.
- **NIS2 × GDPR incident reporting.** Different regulators, different clocks,
  one incident. See `skills/incident-response` — the clocks are 24h, 72h and one
  month, and they are not the same 72 hours.

## What is usually *not* in scope, and why saying so matters

An applicability assessment that lists only what applies is half a document. The
ruled-out list, with the fact that rules it out, is what a regulator or an
acquirer actually reads — and it is what stops the next engineer re-litigating
the question every quarter.

Common honest exclusions:

- **DMA** — gatekeeper designation is a formal Commission decision. If you have
  not received one, you are not a gatekeeper.
- **VLOP/VLOSE duties under the DSA** — require designation at 45M+ monthly
  active EU recipients.
- **DSA online-platform duties (Section 3)** — do not apply to micro and small
  enterprises, though the hosting duties still do.
- **EAA** — microenterprises providing services (under 10 staff **and** turnover
  or balance sheet at or below €2M) are exempt for services; the product rules
  differ.
- **CRA** — free and open-source software supplied outside a commercial
  activity; pure SaaS is generally outside unless it is remote data processing
  integral to a product.
- **NIS2** — entities below the medium-enterprise size cap, unless a Member
  State has designated them anyway. Check the national law, not the Directive.
- **AI Act high-risk** — Art. 6(3) allows a narrow derogation for systems that
  perform a narrow procedural task, improve a prior human activity, detect
  decision patterns, or do a preparatory task — **but not if the system profiles
  natural persons**. If you rely on it, you must document the assessment and
  register the system anyway.

Record each exclusion as `{regime, reason, the fact that decides it, who
confirmed}`. When the fact changes — you hit the size cap, you add a hiring
feature, you start monetising the open-source project — the exclusion expires,
and `eu-compliance-gates` is how you notice.

## Where to check the current text

Primary sources only, every time:

- **EUR-Lex** (`eur-lex.europa.eu`) — the consolidated text of every instrument
  above. The consolidated version shows amendments; the original OJ version does
  not.
- **EDPB** (`edpb.europa.eu`) — guidelines and opinions on GDPR and ePrivacy.
- **ENISA** — CRA and NIS2 technical guidance.
- **The AI Office / Commission AI Act pages** — GPAI codes of practice,
  guidelines, and any amendment to the application dates.
- **Your Member State's supervisory authority and NIS2 transposition law** —
  NIS2 and ePrivacy are national in a way the Regulations are not.

A blog post is not a source. Neither is this file.
