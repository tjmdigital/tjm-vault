---
type: client
portal: 2707865
token_env: USECURE_HUBSPOT_TOKEN
launched: 2026-07-21
---
# Usecure

Human Risk Management platform. RevOps and HubSpot work, direct with usecure.

Originally engaged via ToJupiter; that agency is no longer involved as of August 2026, so no
ToJupiter-facing reporting is needed.

New inbound lead process launched **21 July 2026**.

> [!warning] There are two API tokens in this portal
> Only the one in `USECURE_HUBSPOT_TOKEN` is correct. A second token beginning `pat-na1-fc53`
> exists and must never be used.

What is stuck and on whom lives on [[Now]] - not repeated here.

Most recent verification: [[2026-08-21 Inbound flow check]] and [[2026-08-21 Dashboard audit]].
Known open issue: [[RevenueHero writes contact owner]].

## People

| | Owns |
|---|---|
| [[Molly McManamon]] | routing, lead timings, where leaver records go |
| [[Scott Pointon]] | reporting definitions, form hygiene, RevenueHero |
| [[Jordan Daly]] | contract, integrations |
| [[Nihil Morjaria]] | AM behaviour, deal ownership |
| [[Hetty Jerram]] | events, webinars, channel reporting |

## Systems

```dataview
TABLE WITHOUT ID
  link(file.link, file.name) AS "System",
  pattern AS "Pattern",
  choice(enabled, "live", "off") AS "State",
  verified
FROM "Clients/Usecure/Systems"
SORT enabled DESC, file.name ASC
```

## Metrics

```dataview
TABLE WITHOUT ID
  link(file.link, file.name) AS "Metric",
  value,
  verified,
  choice(status = "retired", "retired", "") AS ""
FROM "Clients/Usecure/Metrics"
SORT status ASC, verified ASC
```

## Decisions

```dataview
TABLE WITHOUT ID
  link(file.link, file.name) AS "Decision",
  decided_by AS "By",
  status
FROM "Clients/Usecure/Decisions"
SORT date DESC
```

## Verification runs

```dataview
TABLE WITHOUT ID
  link(file.link, file.name) AS "Check",
  outcome
FROM "Clients/Usecure/Checks"
SORT date DESC
```

## Meetings

```dataview
LIST
FROM "Clients/Usecure/Meetings"
SORT date DESC
```

## HubSpot objects

```dataview
TABLE WITHOUT ID
  link(file.link, file.name) AS "Object",
  type,
  object AS "On",
  choice(enabled, "live", choice(type = "property", "-", "off")) AS "State"
FROM "Clients/Usecure/HubSpot"
SORT type ASC, file.name ASC
```
