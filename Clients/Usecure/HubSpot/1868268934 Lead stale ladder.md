---
type: workflow
client: Usecure
hubspot_id: 1868268934
object: "0-136 lead"
enabled: false
built: 2026-08-17
verified: 2026-08-21
depends_on: ["[[trigger_lead_reassignment]]"]
hardcodes: []
---
# 1868268934 Lead stale ladder

Warn day 2, stamp reassignment trigger day 3, close day 14.

Un-enrols on any activity. Enrolment guarded to leads older than 2 days.

Implements [[Stale lead ladder (Usecure)]].

> [!warning] Notification step has no recipient
> Must be set in the UI before switch-on.
