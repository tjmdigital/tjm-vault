---
type: property
client: Usecure
object: contacts
created: 2026-08-21
---
# `trigger_unowned_lead_routing`

Datetime property on **contacts**. Exists only to carry a [[Two-stage trigger]] across
objects - a workflow can only write to the enrolled object or its associations, so the
decision and the action have to be split.

Stamped on the primary contact when an open lead has no owner. [[1870371119 Unowned lead fallback]] reads it and clears it.

Part of [[Unowned lead fallback routing]].

> [!info] Should always be empty
> A record sitting with this set means the second workflow did not run. Worth a periodic
> check once the builds are live.
