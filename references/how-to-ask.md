# How to ask

The shared mechanic of this repo. Every skill here asks questions before it
builds, and the quality of the build is capped by the quality of the answers.
This file is how you get real answers instead of polite ones.

> **Not legal advice.** These skills produce questions, findings and
> documentation. They do not produce legal conclusions, and nothing here
> substitutes for a qualified lawyer or a Data Protection Officer.

## The problem with a questionnaire

Asked "do you process personal data?", a builder says "no, just emails and
usage analytics." Both are personal data. Asked "what is your lawful basis?",
they say "the user agrees to our terms." That is not consent and usually not
contract necessity either.

Neither answer is a lie. They are what happens when you ask a legal question of
someone who has not been given the frame to answer it. A form collects those
answers and writes them into a record that now looks like diligence.

The fix is not a longer form. It is to **ask about the system, not about the
law**, and to do the legal mapping yourself.

| Do not ask | Ask instead |
| --- | --- |
| "Do you process personal data?" | "List every field you store about a person, including IDs, IPs and logs." |
| "What is your lawful basis?" | "If a user asked you to stop this processing tomorrow, what would break?" |
| "Do you transfer data outside the EU?" | "Name every vendor that touches this data and where their servers and support staff are." |
| "Is this a high-risk AI system?" | "What decision does the model's output change, and what happens to the person if it is wrong?" |
| "Do you have consent for cookies?" | "List everything that writes to the browser before the user clicks anything." |
| "Are you accessible?" | "Can the primary task be completed with a keyboard only, at 200% zoom, with a screen reader?" |

The left column asks the user to be a lawyer. The right column asks them to be
an engineer describing their own system, which they can do accurately.

## The answer-quality rubric

Grade every answer. This is the mechanism that makes the difference between a
gate and a form.

| Grade | Looks like | Action |
| --- | --- | --- |
| **SPECIFIC** | Names things: fields, vendors, countries, retention in days, a person | Accept, record |
| **VAGUE** | "Standard stuff", "the usual analytics", "not much", "as long as needed" | **Re-ask, narrower.** Do not record |
| **ASSUMED** | "I think Stripe is EU", "it should be anonymised" | Re-ask as a verification task with an owner |
| **EVASIVE** | Answers a different question; redirects to how unlikely a problem is | Name it and re-ask once, verbatim |
| **UNKNOWN** | "I genuinely do not know" | **Valid.** Record as an open unknown with an owner and a date |

**`UNKNOWN` is a passing answer and `VAGUE` is not.** That inversion is the
whole design. A recorded "we do not know where our analytics vendor stores data,
Sam is checking by 1 October" is an honest artifact that a regulator can read
and an engineer can close. "Standard analytics, should be fine" is a liability
written in the voice of diligence.

Never convert an `UNKNOWN` into an assumption to keep the interview moving. The
temptation is enormous because an assumption unblocks the build. It is also how
the wrong thing gets built and documented as deliberate.

## Re-asking without being insufferable

You will re-ask. Do it in a way that keeps the person in the room.

- **Narrow, do not repeat.** "Standard analytics" → "Which product? Plausible,
  GA4, PostHog, something else? Self-hosted or their cloud?" A repeated question
  reads as not listening; a narrower one reads as helping.
- **Offer a menu when the space is small.** Four options and "something else" is
  faster and more accurate than an open prompt, and it teaches the vocabulary.
- **Say what turns on it.** "I am asking because if it is their cloud, this
  becomes an international transfer question and needs two more answers." People
  answer precisely when they can see the consequence.
- **Cap it at two re-asks.** After two, record `UNKNOWN` with an owner and move
  on. A third re-ask produces a fabricated answer, which is worse than a gap,
  because gaps get closed and fabrications get built on.
- **Batch by topic, not by regime.** Nobody can answer four questions about
  four different regulations in a row. Ask everything about the analytics stack,
  then everything about the vendors.

## Answers that sound like answers

The common ones, and what each actually means. When you hear one, do not
correct the user's legal understanding — ask the follow-up that resolves it.

- **"We're just a processor."** Often wrong. If you decide what the data is used
  for, you are a controller for that purpose, whatever the contract says.
  → *"Who decided what fields to collect, and who decides when they are deleted?"*
- **"It's anonymised."** Usually pseudonymised, which is still personal data.
  → *"If I gave you one of these records and your other tables, could you get back
  to a person?"*
- **"The user consents in our terms."** Consent bundled into terms is not freely
  given or specific, and consent is usually the wrong basis for something the
  service cannot function without.
  → *"What happens if they say no — can they still use the product?"*
- **"We're not in the EU, so it doesn't apply."** GDPR Art. 3(2) reaches
  offering goods or services to people in the Union, or monitoring their
  behaviour.
  → *"Do you price in euros, ship to the EU, or run analytics on EU visitors?"*
- **"It's only internal / only employees."** Employees are data subjects, and
  consent is rarely valid in an employment relationship because of the power
  imbalance.
- **"We don't sell data."** Irrelevant to whether you have a lawful basis to
  collect it.
- **"The AI just assists, a human decides."** The decisive question is whether
  the human can and does actually overturn it.
  → *"In the last hundred cases, how many times did the human go against the
  model, and did they see anything the model did not?"*
- **"It's open source, so it's out of scope."** Only for software supplied
  outside a commercial activity. Monetised open source is in scope of the CRA.
- **"We'll add that before launch."** The most common one. Record it as a
  condition with a date and an owner, or it does not exist.

## When to stop asking

Stop when one of these is true, and not before or after:

1. **Every question in the active branches is `SPECIFIC` or a recorded
   `UNKNOWN`.** The bar, and the normal exit.
2. **A blocker has surfaced that makes the rest moot.** If the product depends
   on a prohibited practice, stop and say so. Twenty more questions about
   retention are theatre.
3. **The build has been descoped below the trigger.** "We will not use the model
   for the hiring decision, only to format the JD" closes the entire high-risk
   branch. Record the descope as a constraint with teeth, because it is now
   load-bearing.

Do **not** stop because the person is tired, because the session is long, or
because the remaining questions are uncomfortable. Those are the questions.

## Asking in an agent, not a meeting

These skills run inside an IDE, which changes the mechanics:

- **Read the repo before asking.** Half the questions have answers in the code:
  the dependency list names the vendors, the schema names the fields, the
  `Dockerfile` names the region. Ask about what you could not find, and *show*
  what you found — "I see `stripe`, `posthog-js` and `@sentry/node` in
  `package.json`; are those the only third parties that see user data?" is a
  better question than asking cold, and it demonstrates you looked.
- **Never fill a gap from the model's priors.** A plausible-sounding vendor
  location or retention period is a fabrication that will be read later as a
  fact the user supplied. Mark everything you inferred as inferred.
- **Write answers down as you get them**, into the brief, incrementally. A
  session that dies at question 30 should not lose the first 29.
- **One question at a time when the answer branches**, batched when it does not.
  A wall of twenty questions gets one paragraph back that answers four of them.

## What a good interview produces

Not a feeling of thoroughness. Three artifacts:

1. A **brief** (`compliance.yaml` + `COMPLIANCE-BRIEF.md`) where every claim
   traces to a question and an answer, and inferences are marked as inferences.
2. A list of **findings**, each with a severity, a citation, and the answer that
   triggered it.
3. A list of **open unknowns**, each with an owner and a date.

If the interview produced confidence but not those three, it produced nothing.
