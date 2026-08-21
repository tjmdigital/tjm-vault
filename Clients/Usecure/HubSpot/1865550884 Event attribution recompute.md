---
type: workflow
client: Usecure
hubspot_id: 1865550884
object: "0-162 event"
enabled: true
built: 2026-08-12
verified: 2026-08-21
depends_on: []
hardcodes: []
---
# 1865550884 Event attribution recompute

Two code steps: net new tagging from registration timestamps, then deal attribution.

Split into two because one run measured 15.7s against a 20s limit.
See [[Currency and code step limits]].
