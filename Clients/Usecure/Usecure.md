---
type: client
portal: 2707865
token_env: USECURE_HUBSPOT_TOKEN
launched: 2026-07-21
---
# Usecure

Human Risk Management platform. RevOps and HubSpot work, direct with usecure.

Originally engaged via ToJupiter; that agency is no longer involved as of August 2026, so
no ToJupiter-facing reporting is needed.
New inbound lead process launched **21 July 2026**.

> [!warning] There are two API tokens in this portal
> Only the one in `USECURE_HUBSPOT_TOKEN` is correct. A second token beginning `pat-na1-fc53`
> exists and must never be used.

## Current state

```dataview
TABLE enabled, blocked_on, verified
FROM "Clients/Usecure/Systems"
SORT enabled DESC
```

## Metrics

```dataview
TABLE value, verified, (date(today) - date(verified)).days AS "days old"
FROM "Clients/Usecure/Metrics"
SORT verified ASC
```

## Open

```dataview
LIST waiting_on
FROM "Clients/Usecure"
WHERE status = "open"
```

## People
[[Molly McManamon]] - sales lead, owns routing and timings decisions
[[Scott Pointon]] - demand gen, owns reporting definitions and RevenueHero
[[Jordan Daly]] - contract holder, owns integrations
[[Nihil Morjaria]] - sales, owns AM behaviour
[[Hetty Jerram]] - events and campaigns
