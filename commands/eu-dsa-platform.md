# DSA — layer, notice-and-action, transparency

The DSA is layered and the layer decides the duty list. The costly mistake is
concluding "the DSA is for Big Tech": **hosting duties have no size exemption.**
If one user can publish something another user sees, you owe Arts. 16-18 whatever
your headcount. The micro/small exemption removes **Section 3 only**.

> **Not legal advice.** The layer analysis and any illegality assessment are
> legal judgements.

## Ask

1. "Can a user publish, upload or send something another user sees? List every
   surface." — comments, reviews, profiles, avatars, uploads, shared links,
   messages, forum posts.
2. "Is any of it visible to the **public**, or only to a chosen recipient?" —
   public dissemination is what turns hosting into an online platform. **Private
   messaging you store is still hosting.**
3. "Do third parties sell to consumers through you?" — marketplace duties.
4. Headcount and turnover — Section 3 only.
5. "How does someone report illegal content today, and what happens next?" — if
   the answer is "they email support", that is the finding.
6. "When you remove content or suspend an account, is the user told why, in a way
   they can challenge?"
7. "Do you profile for ads or recommendations? Any minors?"
8. "Established in the EU? If not, who is your Art. 13 legal representative?"

## The layers

- **All intermediaries** — points of contact (Arts. 11-12), legal representative
  if non-EU (Art. 13), T&Cs including moderation information (Art. 14),
  transparency reports (Art. 15, not micro/small).
- **Hosting** — notice and action (Art. 16), statement of reasons (Art. 17),
  report criminal suspicions threatening life or safety (Art. 18). **No size
  exemption.**
- **Online platforms** (hosting + public dissemination, not micro/small) —
  Section 3: complaint handling (20), out-of-court settlement (21), trusted
  flaggers (22), measures against misuse **in both directions** (23), **no dark
  patterns** (25), ads transparency and **no targeting on special-category data**
  (26), recommender transparency (27), **no profiling ads to minors** (28).
- **Marketplaces** — trader traceability (30-32).
- **VLOP/VLOSE** — by **Commission designation** only. No designation, no VLOP
  duties.

Arts. 26(3) and 28(2) are **prohibitions in the serving path**, not paragraphs in
a policy.

## Produce

The layer analysis with reasoning and an `expires_if`. A notice endpoint carrying
the Art. 16 elements (exact URL, substantiated explanation, notifier identity
where required, good-faith statement) with a **timestamped receipt** — that
timestamp is the actual-knowledge moment that removes the Art. 6 liability
exemption. A register of every notice **including rejected ones, with reasoning**
— that is the evidence you acted diligently and non-arbitrarily. Statements of
reasons on every restriction (decision, facts, whether automated, ground, appeal
route), submitted to the Commission's Transparency Database where required. Ad
and recommender constraints **as a function in the serving path**. T&Cs that
describe the actual moderation. A transparency report unless micro/small.

Remember over-removal is also a breach: diligent and non-arbitrary cuts both ways.

## Verify

`pytest -q`: hosting duties survive the size exemption while Section 3 does not;
private sharing is hosting not platform; public dissemination makes it a
platform; no-UGC is ruled out with an expiry; a notice requires URL and a
substantiated reason; the receipt timestamp is recorded; rejected notices keep
their reasoning; every restriction emits a statement of reasons; special-category
targeting is refused; profiling ads to minors are refused; a non-EU provider
needs an Art. 13 representative; VLOP duties require designation.

Report the layer and its reasoning, the duty list, whether the mechanism accepts
every required element, and the **median time from notice receipt to decision** —
that is what a Digital Services Coordinator asks about. Then submit a notice
yourself from outside and see whether a statement of reasons actually reaches the
affected user.
