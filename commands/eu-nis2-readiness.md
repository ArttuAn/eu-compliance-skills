# NIS2 readiness

NIS2 regulates the **organisation**, not the product — which is why teams who
scope their software carefully miss it entirely. A large number of ordinary SaaS
companies are "cloud computing service providers" under Annex I and do not know
it. And it is a **Directive**: the binding text is the national transposition.

> **Not legal advice.** Scope and classification are decided by national law.

## Ask

1. Headcount, turnover, balance sheet — **at group level**. The cap is **OR**:
   ≥50 staff, **or** >€10M turnover, **or** >€10M balance sheet.
2. The sector list, read out: cloud, data centres, managed IT/security services,
   CDN, DNS, digital infrastructure, online marketplaces, search, social
   networks, energy, transport, banking, health, water, public administration,
   postal, waste, chemicals, food, manufacturing, research.
3. "Which Member States are you established in?" — decides which transposition
   binds and which authority supervises.
4. "Has your **board** formally approved the security measures, and been
   trained?" — Art. 20, personal liability, usually asked first. "The CTO looked
   at it" is not board approval.
5. "Who are your critical suppliers, and when did you last assess them?"
6. "If you detected a significant incident at 02:00 on a Saturday, who decides
   whether to report, and how long to reach them?"

Note: size caps are overridden for some entity types (DNS providers, TLD
registries, trust service providers, some public administration) and Member
States may designate entities regardless of size. Check the national law.

## The ten Art. 21(2) measures

(a) risk analysis and IS policies · (b) incident handling · (c) continuity,
backup, **tested restore**, crisis management · (d) supply chain security ·
(e) security in acquisition/development/maintenance incl. vulnerability handling
· (f) policies to assess effectiveness · (g) cyber hygiene and training ·
(h) cryptography policy · (i) HR security, access control, asset management ·
(j) MFA, secure comms, **emergency communications that survive the incident**.

Two that get skipped: (c) needs a *dated successful restore test* — an untested
backup is not continuity; (j) means not the Slack the ransomware encrypted.

**Art. 23 reporting**: 24h early warning → 72h notification → **1 month** final,
from awareness. Recipients of your services may also need telling.

Essential vs important changes supervision and the penalty ceiling (€10M/2% vs
€7M/1.4%), not the measures.

## Produce

The scoping decision with the arithmetic shown and `national_law_checked` per
Member State (**be honest about the gaps**). A measure register, one row per
point, with owner, evidence path and status — `deferred` is allowed **only** with
an owner and a date; without one it is absent, not deferred. The reporting
runbook with clocks pre-computed and the decision-maker and deputy named with
phone numbers, stored somewhere reachable when the network is down. A dated board
minute. A supplier register with last-assessed dates — which doubles as the
answer to your own customers' questionnaires.

## Verify

`pytest -q`: the size cap is OR not AND, tested at 49/50; group figures are used;
multi-tenant SaaS classifies as cloud computing under Annex I; the exclusion
records a machine-evaluable expiry; all ten measures present; a measure without an
owner is not "deferred"; an untested backup fails continuity; clocks compute from
awareness (24h/72h/1mo); missing board approval is a condition; a national-law gap
is reported rather than assumed; no legal conclusion about scope.

Report sector and size arithmetic, essential/important, the ten measures by
status, suppliers assessed vs total, and whether a drill has run. **The count of
measures at `deferred` with no owner is the number that predicts trouble.** Then
run the drill at 02:00 without warning and measure time-to-decision against 24
hours.
