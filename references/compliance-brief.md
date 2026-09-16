# The compliance brief

The spine of this repo. `eu-grill-me` produces it, every other skill reads and
extends it, and `eu-compliance-gates` enforces it in CI. One artifact, two
renderings:

- **`compliance.yaml`** — machine-readable. What the skills and CI consume.
- **`COMPLIANCE-BRIEF.md`** — generated from it. What a human, a lawyer, or an
  acquirer's diligence team reads.

Never hand-edit the Markdown. Regenerate it, so the two can never disagree.

> **Not legal advice.** The brief is a factual record and a list of open
> questions. It does not assert compliance and must not be presented as if it
> does.

## The two rules the schema exists to enforce

**1. Every claim traces to an answer.** No field in the brief may appear without
a `source` naming the question that produced it. A record with untraceable
claims is worse than no record: it reads as diligence and is a fabrication.

**2. Inference is labelled.** When the agent derived something rather than being
told it — read a vendor out of `package.json`, concluded a field is personal
data — `source.kind` is `inferred` and the reasoning is stored. A regulator
reading the brief must be able to tell what the company asserted from what a
tool guessed.

## `compliance.yaml`

```yaml
version: 1
generated_at: "2026-09-15T10:22:00Z"
generated_by: "eu-grill-me 1.0"
status: blocked            # blocked | conditional | clear
certainty: 78              # 0-100 — see references/certainty.md for the anchors

subject:
  product: "Hiring Copilot"
  description: "Ranks inbound applicants and drafts screening notes."
  repo: "github.com/example/hiring-copilot"
  markets: [DE, FI, NL]
  eu_establishment: false
  targets_eu_users: true       # GDPR Art. 3(2)
  headcount: 28
  turnover_eur: 4200000        # decides EAA, NIS2 and DSA size thresholds

roles:                          # who you are decides which duties land on you
  gdpr: controller              # controller | processor | joint | none
  ai_act: provider              # provider | deployer | importer | distributor | none
  cra: manufacturer             # manufacturer | open_source_steward | none
  dsa: none                     # intermediary | hosting | platform | marketplace | none

data:
  subjects: [job_applicants, employees]
  minors: false
  categories:
    - field: "applicant.cv_text"
      personal: true
      special_category: false   # Art. 9 - may be hidden inside free text
      source: {kind: answered, question: Q-07}
    - field: "access.log.ip"
      personal: true
      special_category: false
      source: {kind: inferred, reasoning: "nginx default log format in ops/nginx.conf"}
  purposes:
    - name: "rank applicants"
      lawful_basis: legitimate_interests   # Art. 6(1)(f)
      basis_confirmed_by: null             # must be a person before status can be `clear`
      lia_required: true                   # legitimate interests assessment
      retention_days: 180
      source: {kind: answered, question: Q-11}
  transfers:
    - vendor: "OpenAI"
      country: US
      mechanism: scc                       # adequacy | scc | bcr | derogation | none
      tia_done: false
      subprocessors_named: false
      source: {kind: answered, question: Q-16}

ai:
  uses_ai: true
  systems:
    - name: "applicant-ranker"
      role: provider
      purpose: "rank inbound applicants by fit"
      annex_iii_candidate: "III(4)(a) recruitment/selection"
      art_6_3_derogation_claimed: false
      profiles_natural_persons: true       # blocks the Art. 6(3) derogation
      art_22_gdpr_in_play: true            # solely automated decision?
      human_oversight: "recruiter reviews top 10"
      oversight_evidence: null             # a claim with no evidence is a finding
      gpai_used: ["gpt-4o via API"]
      source: {kind: answered, question: Q-12}

regimes:
  applicable:
    - {regime: gdpr, trigger: "processes applicant data, targets EU users", question: Q-01, certainty: 96}
    - {regime: ai_act, trigger: "provider of an AI system placed on the EU market", question: Q-12, certainty: 90}
    - {regime: eprivacy, trigger: "analytics on the careers site", question: Q-04, certainty: 71}
  ruled_out:
    - {regime: nis2, reason: "below the size cap and not in an Annex I/II sector",
       deciding_fact: "28 staff, SaaS for HR", question: Q-20,
       citation: "Art. 21(2)(d) NIS2", confirmed_by: "counsel, 2026-09-10",
       expires_if: "headcount >= 50 or turnover > 10M EUR", certainty: 66}
    - {regime: dsa, reason: "hosts no third-party content", deciding_fact: "Q-21", certainty: 92}

findings:
  - id: F-001
    severity: blocker            # blocker | condition | note
    regime: gdpr
    citation: "Art. 6(1)"
    question: Q-11
    certainty: 88                # 88% because the basis facts are answered, the citation is binding text
    statement: >
      No lawful basis has been identified for using historical applicant CVs as
      training data. The basis given for ranking (legitimate interests) was not
      assessed for the training purpose, which is a separate purpose.
    needs: "A documented basis per purpose, and an LIA if relying on Art. 6(1)(f)."
    owner: "Priya"
    due: "2026-10-01"
    status: open                 # open | accepted | resolved
  - id: F-002
    severity: condition
    regime: ai_act
    citation: "Annex III(4)(a)"
    question: Q-12
    requires_confirmation: true   # interpretation -> capped at 50 until confirmed
    certainty: 71                # capped: classification must be confirmed by counsel
    statement: >
      The system ranks job applicants. Annex III(4)(a) covers AI intended for
      recruitment or selection. If confirmed, Chapter III obligations follow.
    needs: "Classification confirmed by counsel before build."
    owner: "counsel"
    due: "2026-09-25"
    status: open

unknowns:
  - question: Q-16
    asked: "Where does your CV parsing vendor store and support data?"
    owner: "Sam"
    due: "2026-09-22"
    blocks: [F-003]

accepted_risks:                  # the escape hatch, and its receipt
  - finding: F-007
    accepted_by: "Dana Ruiz, CTO"
    accepted_at: "2026-09-14"
    rationale: "Analytics ships behind consent in v2; launch scope is EU-internal pilot only."
    review_by: "2026-11-01"

gate:
  blockers_open: 1
  conditions_open: 1
  unknowns_open: 1
  decision: blocked
  reason: "F-001 is an open blocker."

# The deterministic inputs every certainty is derived from. tools/certainty_engine.py
# computes the numbers; tools/hard_gate.py refuses any number this cannot support.
# Stored certainties are normalized on load -- typed numbers are overridden.
trace:
  screened_regimes: [gdpr, eprivacy, ai_act, eaa, cra, nis2, dsa, data_act,
                     dora, pld, mdr, eidas]
  answers:
    - {question: Q-07, grade: specific}
    - {question: Q-11, grade: specific}
    - {question: Q-12, grade: assumed}
    - {question: Q-16, grade: unknown}
  verifications:
    - {citation: "Art. 6(1) GDPR", celex: "32016R0679", checked_on: "2026-09-15"}
  directives:
    - {instrument: NIS2, member_state: FI, transposition_read: true}
  confirmations:
    - {item: F-002, confirmed_by: "Counsel", on: "2026-09-16"}
```

## Field notes that matter

**`status` is derived, never typed.** `blocked` if any open blocker;
`conditional` if conditions or unknowns remain; `clear` only when every finding
is `resolved` or `accepted` **and** every lawful basis has a
`basis_confirmed_by`. If a human can set `status: clear` by editing the file,
the gate is decorative.

**`ruled_out` carries `expires_if`.** An exclusion is only valid while the fact
that grounds it holds. "Below the NIS2 size cap" stops being true at the 50th
hire, and nothing will tell you unless the condition is written down and checked
— which is exactly what `eu-compliance-gates` does in CI.

**`source` on everything.** `{kind: answered, question: Q-07}` or `{kind:
inferred, reasoning: "..."}`. The checker rejects a brief with claims that carry
neither.

**`certainty` on every assessment, always.** The top level, each applicable and
`ruled_out` regime, and every finding carry `certainty` (0–100) — the honest
percent of the assessment that rests on verified sources and confirmed facts
rather than inference, open unknowns and interpretation. State it in the
generated Markdown with the single largest reason it is not higher; a brief
whose assessments show no certainty is a brief written in the voice of certainty
it has not earned. `references/certainty.md` holds the anchors and the rules —
including that `UNKNOWN` stays open and `VAGUE` stays rejected. A certainty never
turns a missing basis into a found one.

**`certainty` is derived, never typed.** The agent writes the `trace`, and
`tools/certainty_engine.py` computes the numbers; `tools/hard_gate.py` refuses a
number the trace cannot support and normalizes the rest on load. A brief without
a `trace` fails the gate outright: if there is no evidence from which to derive
a number, there is no number to trust.

**`severity` has exactly three values, and they mean different things:**

| Severity | Meaning | Effect on the gate |
| --- | --- | --- |
| `blocker` | Building this as described would be unlawful, or a basis is missing entirely | **Stops the build of the affected component** |
| `condition` | Lawful path exists; specific work must land before launch | Build proceeds; must be closed before release |
| `note` | Worth recording; no obligation identified yet | None |

Do not inflate. A repo where everything is a blocker gets the gate switched off
in week two, and then nothing is blocked.

**`accepted_risks` requires a named human, a date, a rationale and a review
date.** An acceptance with no name is not an acceptance, it is a bypass. This
field exists because refusing all escape hatches gets the skill deleted; a
recorded, dated, attributed acceptance is itself a compliance artifact and is
far better than the alternative, which is the same decision made silently.

## Lifecycle

```
eu-grill-me          creates it, sets the gate
eu-applicability     fills `regimes`, both lists, with expiry conditions
eu-gdpr-data-map     fills `data`, adds findings
eu-ai-act            fills `ai`, adds findings
… every regime skill appends findings and fills its own section
eu-evidence-pack     renders the brief plus the documents a regulator asks for
eu-compliance-gates  re-checks it in CI on every change, and fails on drift
```

Each skill **appends**; none rewrites another's section. Findings are
append-only — resolving one sets `status: resolved` with a note, and never
deletes the row. The history is the point: "we identified this and closed it on
this date" is the accountability record (Art. 5(2) GDPR), and a brief that only
shows the current state has thrown it away.

## Generating the Markdown

`COMPLIANCE-BRIEF.md` is a rendering, and its job is to be read by someone who
will not open the YAML. Lead with the gate decision and the open blockers.
Put the ruled-out regimes and their expiry conditions in full, because that is
the section diligence actually reads. Put the answer trace in an appendix.
Never render a claim without its source marker or its certainty.
