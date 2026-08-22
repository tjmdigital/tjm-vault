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
| [[Conversions]] | 817 | - |
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
| No live work sitting with a deactivated user | **9 finding(s)** |
| Notes about a leaver quote the live numbers | pass |
| New business deals have a contact attached | **1 finding(s)** |
| Two-stage triggers have all cleared | pass |
| Every marketing event has an event record | pass |
| Registrants and attendees are in sync | pass |

### Findings

- **Every open lead has an owner** - 2 open lead(s) with no owner
- **No live work sitting with a deactivated user** - 117 open deal(s) still held by Natalie Wallace, deactivated
- **No live work sitting with a deactivated user** - 174 open deal(s) still held by Dexter Mapfumo, deactivated
- **No live work sitting with a deactivated user** - 68 open deal(s) still held by Josh McCann, deactivated
- **No live work sitting with a deactivated user** - 94 open deal(s) still held by Richmond Asante, deactivated
- **No live work sitting with a deactivated user** - 34 open lead(s) still owned by Albir Gendi, deactivated
- **No live work sitting with a deactivated user** - 104 open deal(s) still held by Albir Gendi, deactivated
- **No live work sitting with a deactivated user** - 81 open deal(s) still held by Sela Nicolas, deactivated
- **No live work sitting with a deactivated user** - 163 open deal(s) still held by Melchor Dormido, deactivated
- **No live work sitting with a deactivated user** - 21,711 companies owned by 21 deactivated users - known backlog, not new
- **New business deals have a contact attached** - 4 new-business deal(s) since launch with no contact

## Detail

- Companies by deactivated owner: Natalie Wallace (3,696), Dexter Mapfumo (3,549), Josh McCann (2,914), Michelle Dickman (2,586), Liam Wright (1,748), Melchor Dormido (1,511), Richmond Asante (1,491), Albir Gendi (1,098), and 13 more

## Vault lint

```
vault lint: clean (91 notes)
```
