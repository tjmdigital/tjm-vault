---
tags: [index]
---
# Dashboard

## Everything, by age

Oldest at the top. This is the one to glance at - anything drifting down the list is
a claim nobody has re-checked.

```dataview
TABLE client, value, verified, (date(today) - date(verified)).days AS "days old"
FROM "Clients"
WHERE verified
SORT verified ASC
```

## Gone stale

Older than 14 days. **Empty here is good** - it means nothing has been left unchecked.

```dataview
TABLE client, value, verified, (date(today) - date(verified)).days AS "days old"
FROM "Clients"
WHERE verified AND (date(today) - date(verified)).days > 14
SORT verified ASC
```

## Built but switched off

Each of these should have a blocker and a named person.

```dataview
TABLE client, blocked_on, built
FROM "Clients"
WHERE enabled = false
SORT built ASC
```

## Anything hardcoding a person

The Albir question: if someone leaves tomorrow, what breaks silently?

```dataview
TABLE client, hardcodes, enabled
FROM "Clients"
WHERE hardcodes AND length(hardcodes) > 0
SORT client ASC
```

## Waiting on someone

```dataview
TABLE client, waiting_on, date
FROM "Clients"
WHERE status = "open"
SORT date ASC
```

## Patterns by reuse

Which mechanisms keep coming back. Two or more implementations means it is worth a
proper template rather than rebuilding it each time.

```dataview
TABLE length(rows) AS "builds", rows.client AS "clients"
FROM "Clients"
WHERE pattern
GROUP BY pattern
SORT length(rows) DESC
```

## Recent decisions

```dataview
TABLE client, decided_by, date
FROM "Clients"
WHERE type = "decision"
SORT date DESC
LIMIT 10
```
