---
type: check
client: Usecure
date: 2026-08-22
outcome: findings
automated: true
---
# Automated health check, 2026-08-22

Run by `scripts/checks.py`. The metric notes below have been updated in place.

## Numbers

| Metric | Now | Was |
|---|---|---|
| [[Conversions]] | 816 | - |
| [[Leads created and routed]] | 329 | - |
| [[Picked up and worked]] | 262 | - |
| [[Qualified]] | 98 | - |
| [[Open leads]] | 259 | - |
| [[Net new event contacts]] | 1249 | 1248 |

Worked rate **80%** of leads since launch. Read that alongside
[[Picked up and worked]] - most qualified leads self-convert without a rep touch.

## Build integrity

- **unowned** - 2 open lead(s) with no owner
- **leaver** - 34 open lead(s) still owned by Albir Gendi, deactivated
- **leaver deals** - 801 open deal(s) held by 7 deactivated users
- **backlog** - 21,711 companies owned by 21 deactivated users - known backlog, not new
- **deals** - 4 new-business deal(s) since launch with no contact

## Detail

- Open deals by deactivated owner: Dexter Mapfumo (174), Melchor Dormido (163), Natalie Wallace (117), Albir Gendi (104), Richmond Asante (94), Sela Nicolas (81), Josh McCann (68)

## Vault lint

```
vault lint: 6 problem(s) across 80 notes

ambiguous (1)
   2 notes named README.md - wikilinks to it resolve unpredictably

no type (2)
   Patterns/Patterns.md
   Platform/Platform.md

orphan (3)
   scripts/README.md - nothing links to it
   Clients/Usecure/Decisions/2026-08-21 Nihil confirms the reassignment rules.md - nothing links to it
   Platform/HubSpot/Association PUT replaces the label set.md - nothing links to it
```
