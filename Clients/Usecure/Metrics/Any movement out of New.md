---
type: metric
client: Usecure
value: 279
verified: 2026-08-21
decays: 14
status: retired
filter: "hs_v2_date_exited_new_stage_id IS_KNOWN"
---
# Any movement out of New

> [!danger] Retired - do not use
> This reads **279 of 293 (96%)** and is meaningless.

It was a sound definition of "worked" until [[2026-08-19 Backlog close]] bulk-moved 34
never-touched leads from New to Closed. Those now count as "moved out of New", so the
metric measures the cleanup rather than the team.

Superseded by [[Picked up and worked]].

Kept as a tombstone so that if the number resurfaces in an old report or screenshot, it
can be traced rather than argued about. See [[One definition per metric]].
