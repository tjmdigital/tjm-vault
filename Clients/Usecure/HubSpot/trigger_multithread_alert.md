---
type: property
client: Usecure
object: companies
created: 2026-08-21
---
# `trigger_multithread_alert`

Datetime property on **companies**. Exists only to carry a [[Two-stage trigger]] across
objects - a workflow can only write to the enrolled object or its associations, so the
decision and the action have to be split.

Stamped on the company when a new contact converts where an open deal exists. [[1870335105 Multi-thread alert]] reads it and clears it.

Part of [[Multi-thread alert (Usecure)]].

> [!info] Should always be empty
> A record sitting with this set means the second workflow did not run. Worth a periodic
> check once the builds are live.
