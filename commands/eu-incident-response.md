# Incident response — one incident, several clocks

One event, several regulators, different deadlines from different trigger
events. The failure is not ignorance of the rules; it is that at 02:00 on a
Saturday nobody remembers which clock started when, and the 24-hour ones are gone
before triage finishes.

The deliverable is not a policy. It is **a runbook that computes deadlines from
timestamps** and names the person who decides.

> **Not legal advice.** Notifiability is a judgement made under time pressure.
> Get counsel or the DPO into the runbook **by name**.

## Ask

1. "Detected at 02:00 on a Saturday — who decides whether to report, name them
   and their deputy, and how long to reach them?" — the 24h clocks are lost here.
2. "Which regulators, by name and Member State, for each applicable regime?" —
   a ten-minute lookup beforehand, an hour you do not have during.
3. "Where is the runbook, and does it work when your systems are down?"
4. "Have you ever run a drill?"
5. "What does your breach register contain **including incidents you decided not
   to report**?" — Art. 33(5). A register with only reported incidents looks like
   one started after the first report.
6. "Do your DPAs require vendors to tell you without undue delay? What is the
   shortest notice period you agreed?" — a vendor allowed 72 hours consumes your
   entire GDPR window.

## The clocks

- **GDPR Art. 33** — 72h to the supervisory authority from awareness of a
  *personal data breach*, unless unlikely to result in a risk. Art. 34: notify
  data subjects without undue delay where risk is **high** (exceptions:
  appropriate encryption, risk mitigated, disproportionate effort → public
  communication). Processors notify their controller. **Art. 33(5): document
  every breach including non-notified ones, with the reasoning.**
- **NIS2 Art. 23** — 24h early warning, 72h notification, **1 month** final, from
  awareness of a *significant incident*.
- **CRA Art. 14** — 24h, 72h, **14 days** final, from awareness of *active
  exploitation*.
- **DORA Art. 19** — financial entities, per the RTS.

**They start from different events.** You may know the service is down hours
before you know data was exfiltrated. Take **three separate awareness
timestamps**; a calculator that applies one timestamp to every regime produces
wrong deadlines in the common case. If NIS2 or the CRA applies, your effective
first deadline is 24 hours and the GDPR assessment has to fit inside it.

"Aware" = reasonable certainty an incident occurred, not the end of the
investigation. A short verification period is accepted; using triage to delay the
clock is not.

## Produce

A clock calculator taking separate `personal_data_aware_at`,
`significant_incident_aware_at` and `exploitation_aware_at`. An authority table
filled **in advance**: name, Member State, portal, form. A per-regime decision
record **including `reportable: false` entries with reasoning** — those *are* the
Art. 33(5) record, and they must be written at the time, not reconstructed. An
out-of-band comms plan independent of the systems that might be compromised. And
a drill, run and dated.

Maintain **one factual timeline** feeding every submission — the NIS2 early
warning and the GDPR notification will be read together.

## Verify

`pytest -q`: separate awareness timestamps produce separate clocks; the earliest
deadline is surfaced first; no clock exists without its triggering awareness; the
CRA final is 14 days not a month; every applicable regime produces a decision
even when not reporting; non-reported incidents still enter the register; a
missed deadline is surfaced not silently passed; an authority is named for every
regime; decision-maker and deputy are named; the runbook is reachable out of
band; a vendor notice period over 24h is a finding.

Report applicable regimes with named authorities and portals, the earliest clock,
whether a drill has run, and **the longest vendor notice period in your DPAs** —
that is the size of the hole in your 72 hours. Then run the drill at an
inconvenient hour without warning and measure time-to-submittable-draft.
