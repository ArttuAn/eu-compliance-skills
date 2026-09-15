# Grill Me — the compliance gate before the build

Before writing the thing the user asked for, find out what it actually is in the
detail regulation turns on, and **do not build the gated parts** until the
deciding facts are recorded or explicitly, attributably accepted as unknown.

> **Not legal advice.** Produce questions, findings and documentation — never
> legal conclusions. The goal is a brief that makes an hour of a lawyer's time
> worth ten.

## Orient first (4 questions)

1. "In one paragraph, what does it do and who uses it?" — mechanics, not pitch.
2. "Are any users, customers or data subjects physically in the EU/EEA?" —
   includes employees, applicants and marketing-site visitors. Yes → GDPR,
   wherever the company is (Art. 3(2)).
3. "Does anything use ML, an LLM, or an automated rule that decides something
   about a person?" — phrase it this way; "do you use AI" gets a marketing answer.
4. "Do you host it, ship it to someone else's machine, or put it in a device?" —
   decides CRA, and provider vs deployer under the AI Act.

**Then read the repo.** `package.json` names the vendors, the migrations name the
fields, the nginx config names the log format. Ask about what you could not find,
and show what you did — it is a better question and it proves you looked.

## Then work the branches

Open a branch only when its trigger is met; record the others as ruled out.

- **A (always)** — every field about a person; purpose per field; "if a user said
  stop tomorrow, what breaks?"; Art. 9 categories **including inside free text**;
  minors; retention as a number; **show me the deletion code**; every third party;
  where their servers *and support staff* are; who decides what is collected.
- **B (any automated decision)** — what decision does the output change; solely
  automated or human-reviewed, and *"in the last hundred cases how often did the
  human go against it?"*; does it score/rank/categorise individuals (this blocks
  the Art. 6(3) derogation); the Annex III list read out; emotion recognition,
  biometric categorisation, scraping (Art. 5 territory); training-data
  provenance; build/buy/API + own trademark (Art. 25); Art. 50 disclosure.
- **C (anything on the device)** — everything that writes before a click;
  strictly necessary or not; is reject as easy as accept; what stops on withdrawal.
- **D (shipped product)** — monetised in any way; support period; can the build
  produce an SBOM; where vulnerabilities get reported.
- **E (NIS2 sectors)** — headcount and turnover; the sector list read out;
  Member States; has the board approved and been trained.
- **F (user content)** — can one user publish what another sees; how is illegal
  content reported; are removals explained; ads, recommenders, minors.
- **G (EAA categories)** — is it e-commerce/banking/e-books/transport/telephony/AV;
  keyboard-only at 200% zoom with a screen reader; headcount and turnover.
- **H (closing)** — who is accountable; is there a DPO or counsel; **"is there
  anything you have been hoping I wouldn't ask?"**

## Grade every answer

`SPECIFIC` and `UNKNOWN` pass. `VAGUE`, `ASSUMED` and `EVASIVE` do not.
**`UNKNOWN` is a passing answer and `VAGUE` is not** — that inversion is the
design. Re-ask narrower (never just repeat), say what turns on it, cap at two
re-asks, then record `UNKNOWN` with an owner and a date. A third re-ask produces
a fabrication, which is worse than a gap.

**Never fill a gap from your own priors.** Mark anything you inferred as
`inferred`, with the reasoning.

## Gate, and be precise about the refusal

- `clear` → build it.
- `conditional` → **build it**, with conditions in the plan, owners and dates.
  This is the normal outcome; treating it as a stop gets the gate switched off.
- `blocked` → build everything not implicated, refuse the specific component.
  Name it, cite the article, explain why code cannot fix it, offer two concrete
  routes forward. Never refuse the whole task because one branch is blocked.

**Escape hatch**: `accept <finding> --by "<named human>" --review-by <date>
--rationale "..."`. All three required. Moves the gate to `conditional`, never
`clear`. Then build, and do not re-litigate it every turn.

## Produce

`compliance/compliance.yaml` (spine) + `COMPLIANCE-BRIEF.md` (generated). Every
claim carries a `source` (`answered` with a question id, or `inferred` with
reasoning). `status` is **derived, never typed**. Findings are append-only.
Ruled-out regimes carry `expires_if`. Write incrementally — a session that dies
at question 30 must not lose the first 29.

## Verify

`pytest -q`: vague answers are re-asked and never recorded; unknown records an
owner and date; two re-asks then unknown; a trigger answer opens its branch; the
interview cannot exit with an open branch; a prohibited practice is a blocker not
a condition; profiling blocks the Art. 6(3) derogation; blocked refuses only the
implicated component; accept requires a named human and a review date; every
claim has a source; no legal conclusions in the output; `status` is derived.

**The two negative controls matter most**: `fixtures/worst-case.yaml` must be
blocked, and `fixtures/static-site.yaml` must be clear. A gate that passes the
first is measuring nothing; one that blocks the second gets disabled.

Report questions asked, answers by grade, unknowns with owners, findings by
severity, trace coverage (must be 1.0) and inference share. Say explicitly what
you could not verify. Never close with a claim about compliance.
