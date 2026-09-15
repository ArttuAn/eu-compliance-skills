# Verification contract

You cannot unit-test "is this GDPR compliant." That is the objection people
raise to automating any of this, and it is correct about the legal conclusion
and wrong about everything else.

What you *can* test, deterministically and offline, is whether the machinery
that produces the legal conclusion is sound: that no citation is fabricated,
that every claim traces to an answer, that the gate actually blocks, that vague
answers are actually caught, and that an exclusion expires when the fact behind
it changes.

That is the contract below. A skill in this repo is not done until it passes all
three tiers.

> **Not legal advice.** Passing every tier proves the process ran correctly. It
> does not mean the product is lawful — only a qualified lawyer reviewing the
> brief can speak to that.

## Tier 0 — it is real

```bash
uv pip install -e ".[dev]"          # or: pip install -e ".[dev]"
python -c "import <package>"
<command> --help
<command> validate compliance.yaml  # the brief parses against the schema
```

Catches: bad packaging, a schema that does not load, a CLI entry point pointing
at a function that does not exist.

## Tier 1 — the machinery behaves (offline, no key)

Every test here is deterministic and runs in milliseconds against fixture
briefs and scripted answers. This is the tier that matters and the one that
distinguishes a gate from a form.

### The universal set — every skill in this repo

| Test | Asserts |
| --- | --- |
| `test_every_claim_has_a_source` | No field in the brief lacks `source`; inferred claims carry reasoning |
| `test_no_fabricated_citations` | Every `Art. N` names a known instrument and N is within its real range |
| `test_no_recital_is_cited_as_a_requirement` | "Recital … requires" never appears |
| `test_no_legal_conclusions` | "is compliant", "is not high-risk" and friends never reach the user |
| `test_vague_answers_are_rejected` | A scripted "standard analytics, should be fine" grades `VAGUE`, is re-asked, and is never recorded |
| `test_unknown_is_a_valid_answer` | "I don't know" records an unknown with an owner and a due date, and does not block the interview |
| `test_gate_blocks_on_an_open_blocker` | Given a fixture brief with one open blocker, the build of the affected component refuses |
| `test_status_is_derived_not_settable` | Hand-editing `status: clear` into a brief with an open blocker is overridden on load |
| `test_findings_are_append_only` | Resolving a finding sets `status: resolved`; the row survives |
| `test_ruled_out_carries_an_expiry_condition` | Every exclusion has `expires_if` and a deciding fact |
| `test_brief_round_trips` | yaml → object → yaml is stable; the Markdown regenerates identically |
| `test_dates_are_never_asserted_bare` | Any date in generated output carries a citation or a verification instruction |

### The per-skill set

| Skill | Must also prove |
| --- | --- |
| **grill-me** | A branch opens when its trigger answer is given; the interview cannot exit with an active branch unanswered; two re-asks then `UNKNOWN`; an accepted risk requires a named human and a review date |
| **applicability** | Both lists are produced; a ruled-out regime flips to applicable when its deciding fact changes; the size-cap arithmetic is tested at the boundary |
| **gdpr-data-map** | Each purpose has exactly one basis; a special-category field without an Art. 9 condition is a blocker; a retention of "as long as needed" is rejected; every field has a deletion path |
| **ai-act** | The Art. 6(3) derogation is refused when `profiles_natural_persons` is true; role (provider vs deployer) drives which duties are emitted; a prohibited practice is a blocker, not a condition |
| **accessibility** | Every acceptance criterion maps to a numbered EN 301 549 / WCAG clause; the microenterprise exemption applies only when both thresholds are met |
| **cra-secure-by-design** | An SBOM is produced and parses; a known-exploitable dependency at release is a blocker; the support period is recorded and non-zero |
| **nis2-readiness** | Size-cap and sector logic at the boundary; all ten Art. 21(2) measures are addressed or explicitly deferred with an owner |
| **dsa-platform** | The layer (intermediary / hosting / platform) drives the duty list; micro/small exemption applies only to Section 3 duties |
| **consent-and-tracking** | Nothing non-essential fires before a consent signal; reject is as easy as accept; withdrawal actually stops the writes |
| **incident-response** | The three clocks are computed from one incident time and do not collide; a missed clock is surfaced, not silently passed |
| **evidence-pack** | Every document the pack claims to contain exists and is non-empty; no placeholder text ships |
| **compliance-gates** | The gate fails on a drifted brief; it fails when a new dependency appears that no vendor answer covers |

### The negative control

The most important test in this repo, and the one nobody writes:

```python
def test_gate_fails_an_obviously_unlawful_fixture():
    """A gate that passes the worst case is measuring nothing."""
    brief = load("fixtures/worst-case.yaml")   # scraped biometric data, no basis,
                                               # Annex III use, no oversight, US transfer
    result = run_gate(brief)
    assert result.decision == "blocked"
    assert {f.regime for f in result.blockers} >= {"gdpr", "ai_act"}
```

Keep `fixtures/worst-case.yaml` in the repo and run it in CI. If a change to the
rules ever lets that fixture through, you have broken the gate, and no other
test in the suite would have told you.

Pair it with the opposite control, which catches the other failure:

```python
def test_gate_clears_a_benign_fixture():
    """A gate that blocks everything gets switched off in week two."""
    result = run_gate(load("fixtures/static-site.yaml"))  # no personal data, no AI
    assert result.decision == "clear"
```

## Tier 2 — the numbers

Not metrics about the law. Metrics about the interview and the record.

| Metric | Definition | Target |
| --- | --- | --- |
| **Answer specificity** | Share of recorded answers graded `SPECIFIC` | > 0.8 |
| **Trace coverage** | Share of brief claims with a `source` | **1.0 — a gate, not a threshold** |
| **Inference share** | Share of claims marked `inferred` | < 0.3, and every one reviewed |
| **Unknown closure** | Share of unknowns closed by their due date | tracked over time |
| **Blocker precision** | Share of blockers a reviewing lawyer agrees were blockers | > 0.7 after review |

Trace coverage is the gate. A brief with untraceable claims is a fabrication
wearing the clothes of a compliance record, and it is worse than having no
record at all — a regulator reading it will reasonably treat every claim in it
as something the company asserted.

Blocker precision is the one that keeps the tool usable. Measure it the first
few times a lawyer reviews a brief: if they disagree with most of your blockers,
the rules are too aggressive and the gate is about to be disabled by whoever is
trying to ship.

## Tier 3 — a human reads it

There is no substitute and no way to automate this one.

1. **A lawyer or DPO reads the brief.** Not the code, the brief. Time how long
   it takes them to get to a view. The purpose of this entire repo is to make
   that hour worth ten, and the honest measure is whether they say the document
   saved them time or created work.
2. **Someone who was not interviewed reads it** and tries to find a claim they
   know is wrong. Untraceable claims and stale inferences surface here.
3. **Re-run the gate after the review** with whatever the lawyer corrected, and
   confirm the corrections actually changed the decision. A gate whose output
   does not move when its inputs are corrected is not reading its inputs.

## What to tell the user when you finish

Report what actually ran, not what it means:

- Questions asked, answers by grade, unknowns left open with owners and dates.
- Findings by severity, and what specifically is blocked.
- Trace coverage and inference share.
- **Which parts you could not verify** — every date you could not check against
  EUR-Lex, every national transposition you could not read, every classification
  that needs counsel.

And never close with a claim about compliance. Close with what is decided, what
is open, and who has to decide the rest.
