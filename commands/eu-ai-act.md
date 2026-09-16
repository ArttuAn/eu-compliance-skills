# AI Act classification and obligations

Classify in this order — **prohibited, then role, then tier, then duties**. A
team that starts at "what documentation do we need" has skipped the two questions
that could have ended the project or moved the obligations onto someone else.

> **Not legal advice.** Classification carries a €35M ceiling. Produce the facts,
> the candidate classification and the citation; counsel confirms before build.
>
> **Dates move.** The AI Act timeline has been subject to amendment. Verify every
> date against the consolidated text on EUR-Lex, or say you could not.

## Ask (never "is this high-risk")

1. "What decision does the output change, and what happens to the person if it is
   wrong?"
2. "Does it infer, score, rank or categorise individual people?" — **the most
   consequential answer**: yes blocks the Art. 6(3) derogation.
3. "Do you train it, fine-tune it, or call an API? Do you put your name on the
   product?" — provider vs deployer, and Art. 25.
4. The Annex III list, read out: recruitment/worker management; education/exam
   scoring; credit/insurance; essential public or private services; law
   enforcement; migration/borders; justice; critical infrastructure safety;
   biometrics.
5. "Does it recognise emotions, categorise people by biometrics, scrape faces,
   score social behaviour, or exploit a group's vulnerability?" — Art. 5.
6. For oversight: "in the last hundred cases, how often did the human go against
   it, and did they see anything it did not?"

## The order

1. **Art. 5 prohibited** → **blocker**. No mitigation, no documentation route,
   no compliant version. Note that *emotion inference in the workplace* catches
   sentiment analysis on employee comms, and *untargeted facial scraping* catches
   a training pipeline, not just a feature.
2. **Role** → Art. 25 is the trap: a deployer becomes a **provider** — inheriting
   all of Chapter III — by putting their name on it, substantially modifying it,
   or changing the intended purpose to a high-risk one. Wrapping an LLM API and
   selling it for hiring is all three.
3. **Tier** → Annex I (safety component) or Annex III (the eight areas). Art. 6(3)
   derogation unavailable if it profiles natural persons; relying on it still
   requires a documented assessment **and** EU database registration.
4. **Duties** → Chapter III if high-risk (Arts. 9, 10, 11+Annex IV, 12, 13, 14,
   15, 17, 43, 47-49); **Art. 50 transparency at every tier including minimal**;
   Art. 4 AI literacy; Chapter V if you provide a GPAI model; Art. 27 FRIA for
   in-scope deployers.

Also flag **GDPR Art. 22** — it applies to solely automated decisions with legal
or similarly significant effects **whether or not there is any AI**.

## Produce

Classification in `compliance.yaml` with `role_reasoning`, `art_6_3_reasoning`
and `classification_confirmed_by: null` until counsel signs. Findings at the
right severity (prohibited = blocker; unconfirmed Annex III candidate =
condition; missing Art. 50 disclosure = condition with a one-line fix). An Annex
IV skeleton created now with `[to be completed: …]` markers CI can count.
**Art. 12 logging designed in** — decide what an event is, retention, and how it
reconciles with GDPR minimisation, because those pull in opposite directions.
**Oversight instrumented**: track the override rate; "a recruiter reviews the top
ten" is a claim, "overridden in 14 of the last 100" is a control.

## Verify

`pytest -q`: prohibited practice is a blocker and is checked before tier;
profiling blocks the derogation; the derogation still requires registration;
rebranding and repurposing each turn a deployer into a provider; Art. 50 applies
at minimal risk; high-risk emits the full Chapter III set; a deployer gets Art. 26
not Art. 11; Art. 22 GDPR is flagged with no AI present; Art. 10 is never treated
as a lawful basis; the Annex IV skeleton has every heading and reports its
unfilled markers; no classification is asserted as final; every date carries a
citation or a verify note.

Report: prohibited screening result, role with Art. 25 reasoning, Annex III
candidate, whether Art. 6(3) was claimed and why it is or is not available, and
the count of unfilled Annex IV sections. Say which dates you could not verify.


Show certainty on every legal-grounded claim, in the brief and in what you say:
each finding, each applicable or ruled-out regime, and the headline carry a
`certainty` 0–100 — the exact percent of the assessment that rests on verified
sources and confirmed facts — stated with the single largest reason it is not
higher. `references/certainty.md` has the anchors; an open unknown caps at 70,
an unread national transposition at 60, a counsel-pending classification at 50.
Certainty never rescues a VAGUE answer or an open blocker.
