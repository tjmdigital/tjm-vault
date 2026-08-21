---
type: property
client: Usecure
object: companies
created: 2026-08-21
---
# `trigger_lead_reassignment`

Datetime property on **companies**. Exists only to carry a [[Two-stage trigger]] across
objects - a workflow can only write to the enrolled object or its associations, so the
decision and the action have to be split.

Stamped on the lead's primary company at day 3 of the ladder. [[1870325562 Lead reassignment]] reads it and clears it.

Part of [[Stale lead ladder (Usecure)]].

> [!info] Should always be empty
> A record sitting with this set means the second workflow did not run. Worth a periodic
> check once the builds are live.
