---
type: system
client: Usecure
status: open
waiting_on: ["[[Scott Pointon]]"]
blocked_on: "Scott to make the router change now he owns RevenueHero"
since: 2026-08-19
verified: 2026-08-21
---
# RevenueHero writes contact owner

## What happens

When a prospect books a demo, RevenueHero writes the hosting AE onto the **contact** as
contact owner. The lead owner follows within seconds, so a lead changes hands moments
before it qualifies.

Timeline on one record, 5 August:

```
05:03:27  RevenueHero sets contact owner to the AE   (INTEGRATION)
05:03:30  lead owner follows                          (property-promoter-worker)
05:03:50  deal created, owner copied from contact     (workflow)
05:03:54  lead qualifies
```

## Why it needs fixing - and it is not the reporting

The reporting gap is small: 80 of 83 qualified leads came via a booking and only 4 had
been worked first, so little rep effort is actually being hidden. Scott was right about this.

The real problem is that the **company keeps its previous owner**, so the record splits -
company with one rep, contact/lead/deal with another. That split does not survive the next
change to the account, because of the [[Owner sync chain]]. Verified in production: a
manual company owner change moved an open deal to a different rep eight seconds later.

## Proposed fix

RevenueHero stops writing contact owner; the deal takes its owner from the meeting host,
which RevenueHero already stamps (populated on all 106 bookings since launch).

Agreed in principle by Jordan and Scott, 19 August. Scott now owns RevenueHero.
