---
type: check
client: Usecure
date: 2026-08-22
outcome: findings
automated: true
---
# Automated health check, 2026-08-22

Run by `scripts/run.py`. The metric notes below were updated in place.

## Numbers

| Metric | Now | Was |
|---|---|---|
| [[Conversions]] | 816 | - |
| [[Leads created and routed]] | 329 | - |
| [[Picked up and worked]] | 262 | - |
| [[Qualified]] | 98 | - |
| [[Open leads]] | 259 | - |
| [[Net new event contacts]] | 1249 | - |

## Checks

| Check | Result |
|---|---|
| Workflow state matches the vault | pass |
| Every open lead has an owner | **1 finding(s)** |
| No live work sitting with a deactivated user | **3 finding(s)** |
| New business deals have a contact attached | **1 finding(s)** |
| Two-stage triggers have all cleared | pass |
| Every marketing event has an event record | pass |
| Registrants and attendees are in sync | pass |

### Findings

- **Every open lead has an owner** - 2 open lead(s) with no owner
- **No live work sitting with a deactivated user** - 34 open lead(s) still owned by Albir Gendi, deactivated
- **No live work sitting with a deactivated user** - 801 open deal(s) held by 7 deactivated users
- **No live work sitting with a deactivated user** - 21,711 companies owned by 21 deactivated users - known backlog, not new
- **New business deals have a contact attached** - 4 new-business deal(s) since launch with no contact

## Detail

- Open deals by deactivated owner: Dexter Mapfumo (174), Melchor Dormido (163), Natalie Wallace (117), Albir Gendi (104), Richmond Asante (94), Sela Nicolas (81), Josh McCann (68)

## Vault lint

```
vault lint: clean (79 notes)
```
