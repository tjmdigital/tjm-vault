---
tags: [index]
---
# Now

What is stuck, who it is sitting with, and for how long. **Nothing here is maintained by
hand** - it reads `waiting_on`, `blocked_by`, `blocked_on` and `since` off the notes
themselves. If a row looks wrong, the note behind it is wrong.

> [!info] Not a task list
> Things you have to *do*, with due dates and ticks, live in Notion. This page answers a
> different question: what is stuck and on whom.

## With other people

Names are links - open one to see everything sitting with that person.

```dataview
TABLE WITHOUT ID
  link(file.link, file.name) AS "Item",
  waiting_on AS "With",
  blocked_on AS "Needs",
  (date(today) - date(since)).days AS "days"
FROM "Clients"
WHERE waiting_on AND !contains(string(waiting_on), "Tom Mitchell")
SORT since ASC
```

## With me

Only things where I am the blocker and nothing upstream is holding them.

```dataview
TABLE WITHOUT ID
  link(file.link, file.name) AS "Item",
  blocked_on AS "Needs",
  (date(today) - date(since)).days AS "days"
FROM "Clients"
WHERE contains(string(waiting_on), "Tom Mitchell")
  AND !blocked_by
  AND length(waiting_on) = 1
SORT since ASC
```

## With me, but also someone else

Part mine, part theirs. Doing my half does not unblock it on its own.

```dataview
TABLE WITHOUT ID
  link(file.link, file.name) AS "Item",
  filter(waiting_on, (p) => !contains(string(p), "Tom Mitchell")) AS "Also with",
  blocked_on AS "Needs",
  (date(today) - date(since)).days AS "days"
FROM "Clients"
WHERE contains(string(waiting_on), "Tom Mitchell")
  AND length(waiting_on) > 1
SORT since ASC
```

## Downstream

Built and ready, waiting on something else in the chain rather than on a person. These
free themselves - no action needed.

```dataview
TABLE WITHOUT ID
  link(file.link, file.name) AS "Item",
  blocked_by AS "Waiting for",
  built AS "built"
FROM "Clients"
WHERE blocked_by
SORT built ASC
```

## Open questions

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
