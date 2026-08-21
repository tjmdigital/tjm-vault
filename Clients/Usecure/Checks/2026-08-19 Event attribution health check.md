---
type: check
client: Usecure
date: 2026-08-19
outcome: "clean, one hygiene fix"
---
# One-week health check: event attribution

Ran a week after the backfill went live, as promised to Hetty.

## Passed

- No event-deal pair carries both labels; no renewal is Sourced; all 32 Sourced links
  respect attended-before-deal and the 12-month cap
- Every recompute tick self-cleared. The auto-run driver fired 7 times on 18 August as a
  webinar backfill landed - no manual step needed
- Contact coverage: 42 of 68 new-business and 34 of 50 renewal deals now have contacts

## Found and fixed

The 12-month cap script had removed the *Sourced label* from 25 old pairs but left the
bare association, so those deals still showed in event panels unlabelled. 23 of the 25 were
366+ days post-event. Counts were unaffected because they calculate off labels - it was
panel hygiene. All 25 archived; portfolio now reads 0 unlabelled, 32 Sourced, 46 Influenced.

**Lesson:** removing a label is not removing the association. Now noted in
[[Event to deal attribution]].
