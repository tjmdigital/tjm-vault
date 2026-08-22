---
type: metric
client: Usecure
value: 262
verified: 2026-08-22
decays: 7
filter: "hs_v2_date_entered_{attempting|connected|qualified} IS_KNOWN AND hs_createdate >= 2026-07-21"
supersedes: "[[Any movement out of New]]"
---
# Picked up and worked

**233 of 293 (80%)** since launch.

Counts a lead that reached Attempting, Connected **or** Qualified at any point.

**Read it carefully:** most qualified leads get there by the prospect booking a demo
themselves, not by rep effort. Only 4 of 80 RevenueHero-booked leads were worked first.
So 80% is not 80% of leads receiving rep attention.

## Versions

| Definition | Value | Status |
|---|---|---|
| Reached Attempting or Connected | 151 (52%) | old, still live on the dashboard tile |
| Reached Attempting, Connected or Qualified | **233 (80%)** | current |
| Moved out of New at all | 279 (96%) | broken - see below |

"Moved out of New" was sound until [[2026-08-19 Backlog close]] bulk-moved 34 never-touched
leads out of New. Do not use it.

Presented as 81% on [[2026-08-18 RevOps call]]. See [[One definition per metric]].
