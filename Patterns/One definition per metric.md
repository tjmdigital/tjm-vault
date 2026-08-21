---
type: pattern
---
# One definition per metric

## The problem

Two people pull the same metric and get different numbers. It is almost never a data
error - it is a definition gap. But it reads as a data error, which destroys trust in
the whole reporting layer.

## How it works

- One canonical note per metric, holding the **literal filter**, not a description of it
- The definition travels with the number - HubSpot report descriptions, chart subtitles,
  the "how these are defined" table on any status page
- When a definition changes, the old one is marked `supersedes` rather than deleted, so a
  stale number can be traced to the version it came from

## What goes wrong without it

Real example: "picked up and worked" was presented three ways within two weeks -
151 (reached Attempting or Connected), 233 (reached any working stage), 279 (moved out of
New at all). All three were defensible. Two were published. The dashboard and the status
page disagreed by 28 percentage points on the same population.

## The trap

A definition can be broken by an unrelated action. "Moved out of New" was sound until a
bulk backlog close moved 34 untouched leads out of New, at which point it read 96%.
**After any bulk operation, re-check every definition that could have been affected by it.**

## Implementations

```dataview
TABLE client, variant, enabled, verified
FROM "Clients"
WHERE contains(string(pattern), this.file.name)
```
