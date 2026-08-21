---
type: decision
client: Usecure
date: 2026-08-19
decided_by: Room
status: settled
---
# Close the historic backlog as a line in the sand

713 of 897 open leads would have triggered the ladder on day one. Switching on as-is meant
713 notifications at once.

Agreed: close the historic backlog in one pass with a cleanup reason, keep the closed set
as a list for re-engagement, and let the rule govern a clean board from switch-on forward.

## What actually happened

**680 closed**, board went 910 -> 231. Contacts saved to list 3868 for re-engagement.

## The mistake worth remembering

The first run swept in **12 leads created in the previous week**, including one from that
morning. Cause: "no activity for 7 days" was implemented as *last activity is older than
7 days **or empty*** - and a lead created yesterday also has an empty last-activity date.

All 12 were reopened to their prior stage with the reason cleared. The same flaw was
sitting in the ladder itself and was fixed there too, by adding a "created more than N days
ago" guard.

**The general rule:** any filter using "or empty" to catch never-touched records needs an
age guard, or it catches brand new ones as well.

It also broke a published metric - see [[Picked up and worked]].
