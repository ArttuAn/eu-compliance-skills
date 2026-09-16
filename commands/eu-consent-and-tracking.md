# Consent and tracking (ePrivacy Art. 5(3))

The most commonly broken rule in European software, and the cheapest to fix
before launch. Consent is required before **storing or reading anything on a
user's device** unless it is strictly necessary for a service the user explicitly
requested — and that is far broader than cookies.

**The engineering test**: open the site in a clean browser, click nothing, and
read the network tab and the storage inspector. Whatever happened there happened
without consent.

> **Not legal advice.** Whether something is strictly necessary, and whether a
> flow is valid, are legal judgements — and national authorities differ.

## Ask, after looking

1. Do the clean-profile load yourself and bring the list. It usually contradicts
   what the team believes.
2. "For each of these, what breaks for the user if it is not there?" —
   "we lose analytics" means not necessary.
3. "Is rejecting as easy as accepting — same layer, same click count, same
   prominence?" — "Reject all" behind "Manage preferences" is the most common
   finding.
4. "When someone withdraws, what actually stops? Show me." — usually nothing;
   the flag flips and the script stays loaded.
5. "Do you keep a record of who consented, to what, and when?" — Art. 7(1).
6. "Does any of this run on mobile? Which SDKs, what identifiers?" — usually
   scoped separately, then not scoped at all.

## Strictly necessary — the short list

**Yes**: session/auth cookies, CSRF and fraud tokens, load balancing, UI state
the user chose (language, theme, the cookie preference itself), cart contents.

**No, however routine**: analytics of any kind (including privacy-focused and
self-hosted — *some national authorities signal leniency for narrow first-party
measurement; that is a national question, verify it*), error tracking, session
replay, A/B testing, advertising and conversion pixels, **third-party fonts, maps
and embedded video** (they disclose the user's IP on load), chat widgets the user
did not open.

The consent standard is GDPR's: freely given, specific, informed, unambiguous,
affirmative action. No pre-ticked boxes, no implied consent, no bundling with
terms, and withdrawal as easy as giving (Art. 7(3)). Dark patterns: no
pre-selection, no nagging after a refusal. "Pay or consent" is under active
scrutiny — treat as a legal question, not a design choice.

## Produce

An inventory **generated from a real clean-profile browser session**, classified
per item with the necessity reasoning. Gating that actually gates:

```html
<!-- WRONG: runs, then checks a flag it set itself -->
<script src="https://cdn.example/analytics.js"></script>
<!-- RIGHT: nothing fetched until an affirmative signal -->
<script type="text/plain" data-consent="analytics"
        data-src="https://cdn.example/analytics.js"></script>
```

Withdrawal that tears down: stop collectors, delete the cookies and keys you set,
call the vendor deletion endpoint, record the withdrawal. A consent record with
the **notice version** — consent given against a notice that has since changed
does not cover the new purposes. And a CI test asserting nothing non-essential
fires before consent, which is what stops the first marketing tag regressing it.

## Verify

`pytest -q`: a clean load fires nothing non-essential; third-party fonts are not
strictly necessary; analytics is never classified necessary; a session cookie is;
reject is on the same layer with the same click count; no non-essential purpose
is preselected; the script is not fetched before opt-in; withdrawal deletes
cookies, stops collectors and calls vendor deletion; the consent record captures
the notice version; a notice version bump invalidates old consent for new
purposes; a refusal is respected for a period.

Report from a real clean-browser run: items fired before consent (must be zero),
third-party origins contacted before consent (must be zero), accept vs reject
click counts, and whether withdrawal was **observed** to stop collection. Name the
national positions you could not verify — the analytics one especially.


Show certainty on every legal-grounded claim, in the brief and in what you say:
each finding, each applicable or ruled-out regime, and the headline carry a
`certainty` 0–100 — the exact percent of the assessment that rests on verified
sources and confirmed facts — stated with the single largest reason it is not
higher. `references/certainty.md` has the anchors; an open unknown caps at 70,
an unread national transposition at 60, a counsel-pending classification at 50.
Certainty never rescues a VAGUE answer or an open blocker.
