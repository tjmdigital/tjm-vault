---
tags: [index]
---
# Now

Everything not moving, and who it is sitting with. **Nothing here is maintained by hand** -
it reads `waiting_on`, `blocked_on` and `since` off the notes themselves. If something is
wrong here, fix it on the note.

> [!info] This is not a task list
> Things you have to *do* live in Notion, with due dates and ticks. This page answers a
> different question: what is stuck, on whom, and for how long.

## Waiting on other people

```dataview
TABLE WITHOUT ID
  link(file.link, file.name) AS "Item",
  waiting_on AS "With",
  blocked_on AS "Needs",
  (date(today) - date(since)).days AS "days"
FROM "Clients"
WHERE waiting_on AND waiting_on != "Tom Mitchell"
SORT since ASC
```

## Waiting on me

```dataview
TABLE WITHOUT ID
  link(file.link, file.name) AS "Item",
  blocked_on AS "Needs",
  (date(today) - date(since)).days AS "days"
FROM "Clients"
WHERE waiting_on = "Tom Mitchell"
SORT since ASC
```

## Built but not live

```dataview
TABLE WITHOUT ID
  link(file.link, file.name) AS "Item",
  client,
  blocked_on AS "Needs",
  built AS "built"
FROM "Clients"
WHERE enabled = false AND type = "system"
SORT built ASC
```

## Open questions

Decisions raised but not settled.

```dataview
TABLE WITHOUT ID
  link(file.link, file.name) AS "Question",
  client,
  waiting_on AS "With",
  date AS "raised"
FROM "Clients"
WHERE type = "decision" AND status = "open"
SORT date ASC
```

## Stale claims

Numbers nobody has re-checked in over a fortnight.

```dataview
TABLE WITHOUT ID
  link(file.link, file.name) AS "Claim",
  value,
  (date(today) - date(verified)).days AS "days old"
FROM "Clients"
WHERE verified AND (date(today) - date(verified)).days > 14
SORT verified ASC
```
