# Citation discipline

An agent writing about regulation has one failure mode that dwarfs all others:
**it produces a citation that does not exist, in fluent legal register, and the
reader believes it.** A wrong retention period gets caught in review. A confident
"Art. 27(4) GDPR requires…" does not, because it reads exactly like the real
ones.

This file is the discipline that prevents that. Every skill in this repo cites
it, and `tools/check_skills.py` enforces part of it mechanically.

> **Not legal advice.** Citations locate the obligation. They do not interpret
> it, and interpretation is where lawyers earn their fees.

## The rule

**Every obligation you state must carry a citation, and every citation must be
one you could point to in the consolidated text on EUR-Lex.**

Every instrument this repo cites, with its CELEX number and a clickable EUR-Lex
link to the consolidated text, is in the **Primary legal sources** table at the
top of the repository README. If the instrument is not there, you have not
found a new regime — you have found an obligation to stop and verify.

If you cannot, you have three honest options and none of them is to guess:

1. State the obligation without an article number, and mark it `[citation
   needed]`. A true statement with a missing citation is fine; a false citation
   is not.
2. State that you believe the obligation exists and that the reader must verify
   the article, naming the instrument.
3. Say you do not know.

A fabricated citation is worse than silence because it converts a question into
a settled point and stops anyone from checking.

## Citation format

Use the same shape everywhere so the checks can find them and the reader can:

```
Art. 6(1)(b) GDPR
Art. 5(1)(a) AI Act
Annex III(4)(a) AI Act
Art. 21(2)(d) NIS2
Art. 16 DSA
Annex I Part II(1) CRA
EN 301 549 v3.2.1 § 9.1.1.1
```

- Article, then paragraph in parentheses, then point.
- Name the instrument by its common short name, and give the full number
  (`Regulation (EU) 2024/1689`) the first time it appears in a document.
- Recitals are numbered `Recital 26 GDPR` and are **interpretive aids, not
  obligations**. Never cite a recital as a requirement — say "Recital 26
  explains that…", never "Recital 26 requires…".
- For Directives — NIS2, ePrivacy, EAA, PLD — cite the Directive article, then
  add: *"as transposed in \<Member State\>"*. The binding text for a Directive
  is the national law, and it differs.

## The cutoff problem, stated honestly

A model's training has a cutoff. EU law does not stop at it. Between a cutoff
and today, application dates get amended, guidance is published, adequacy
decisions are challenged, and Member States transpose Directives differently
and late.

So:

- **Never state a date as settled fact from memory.** Write it with the source
  and a verification instruction: *"Prohibitions apply from 2 February 2025
  (Art. 113 AI Act) — confirm against the consolidated text, this timeline has
  been subject to amendment proposals."*
- **Flag anything you know was in flux**: AI Act high-risk timelines, EU–US
  transfer adequacy, NIS2 national transposition, the ePrivacy Regulation's
  status.
- **Prefer structural facts over dated ones.** "Annex III lists employment as a
  high-risk area" is stable. "This obligation starts on 2 August 2026" is not.
  Lean the analysis on the first kind.
- **When you have web access, use it.** Fetch the consolidated text from
  EUR-Lex rather than recalling it. When you do, record the CELEX number and the
  date you fetched it in the brief.

## Hierarchy of sources

Use in this order. Stop at the highest one that answers the question.

1. **The consolidated legal text** on EUR-Lex. The only binding source for a
   Regulation.
2. **The national transposition** for any Directive, plus any national
   derogation for a Regulation (GDPR has many — employment, research, age of
   consent, which ranges from 13 to 16).
3. **Official guidance**: EDPB guidelines and opinions, the Commission's AI Act
   guidelines, ENISA technical guidance, your national supervisory authority's
   published positions.
4. **Harmonised standards**: EN 301 549 for accessibility, the CEN/CENELEC work
   for the CRA and AI Act. Conformity with a harmonised standard gives a
   presumption of conformity — that is a legal effect, and it is the cheapest
   route to compliance when one exists.
5. **Case law**: CJEU judgments, then national courts.
6. **Everything else** — law-firm briefings, vendor whitepapers, blog posts,
   this repository. Orientation only. Never cite these to the user as authority.

## What an agent may and may not conclude

The line matters, and it is not about hedging language — it is about which
questions have an engineering answer.

**May state directly** (facts about the system, or about what the text says):

- "You store IP addresses in `access.log` for 90 days."
- "Art. 30 GDPR requires a record of processing activities."
- "Annex III(4)(a) lists AI systems intended to be used for recruitment."
- "This vendor's DPA does not name its sub-processors."
- "Nothing in this codebase implements a deletion path for `users.email`."

**May not state** (legal conclusions):

- "This is compliant." / "You are GDPR compliant."
- "This is not a high-risk AI system."
- "Legitimate interest applies here."
- "This transfer is lawful."

Write those as findings instead, with the facts, the citation, and the open
question:

> **F-004 · condition · AI Act** — The system ranks job applicants
> (answer to Q-12). Annex III(4)(a) covers AI systems intended for recruitment
> or selection. **If** that classification is confirmed, Chapter III obligations
> follow, including Art. 9 risk management, Art. 12 logging and Art. 14 human
> oversight. *Classification must be confirmed by counsel before build.*

That paragraph is useful, honest, and does not pretend to be a legal opinion.
"This is high-risk, here is your risk management system" is none of those.

## Not legal advice, said once and meant

Every skill carries the disclaimer, and it should appear once, near the top,
plainly. What that means in practice:

- These skills produce **questions, findings, documentation and code**. They do
  not produce legal opinions.
- A finding is an input to a lawyer's review, not a substitute for it. The
  highest-value output of this repo is a brief that makes an hour of a lawyer's
  time worth ten.
- Where a decision needs a lawyer or a DPO, the skill must say so **at that
  point**, naming what specifically needs deciding — not as a blanket caveat at
  the end that tells the reader nothing about what to go and ask.

Do not repeat the disclaimer every paragraph. A document that hedges constantly
teaches the reader to skip the hedges, including the one that mattered.

## The mechanical checks

`tools/check_citations.py` enforces the parts that can be enforced without a
lawyer:

- Every `Art. N` reference names an instrument this repo knows about.
- Article numbers fall within the real range for that instrument (GDPR ends at
  99, the AI Act at 113, NIS2 at 45, the DSA at 93) — this catches the most
  common fabrication, which is an article number past the end of the act.
- No recital is cited with a requirement verb ("requires", "mandates",
  "obliges").
- Every date is accompanied by either a citation or a verification instruction.
- Conclusion phrases ("is compliant", "is not high-risk") do not appear outside
  quoted examples of what *not* to write.

These catch fabrication and overreach. They cannot catch a citation that exists
but does not say what you claimed — only a human can, which is why findings name
the article and quote what turns on it.
