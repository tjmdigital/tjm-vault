---
type: pattern
---
# Multi-thread alert

## The problem

A second person converts at a company where a colleague already has an open deal. Creating
a lead duplicates effort and confuses ownership. Creating nothing loses a real buying signal.

## How it works

No second lead. The **deal owner** gets told, and decides how to involve the new person.
Implemented as a [[Two-stage trigger]]: the conversion stamps the company, a deal-side
workflow finds the open deal and raises a task assigned to its owner.

## Why a task and not a notification

Notification recipients cannot be set through the API at all (see
[[Notification recipients cannot be set via API]]). A task can be assigned, is trackable,
and sits on the deal where the owner is already looking.

## Worth knowing

This is the pattern most likely to be *agreed and then never built*, because it looks
like a nice-to-have next to lead creation. At Usecure it was agreed in June and still
was not built in August, by which point sales had raised the same complaint twice in Slack.

## Implementations

```dataview
TABLE client, variant, enabled, verified
FROM "Clients"
WHERE contains(string(pattern), this.file.name)
```
