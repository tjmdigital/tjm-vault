---
tags: [index]
---
# Now

What is stuck, who it is sitting with, and for how long. **Nothing here is maintained by
hand** - it reads `waiting_on`, `blocked_by`, `blocked_on` and `since` off the notes
themselves, wherever they live. If a row looks wrong, the note behind it is wrong.

The four blocked sections are mutually exclusive by construction: anything with `blocked_by`
appears only under Downstream, and `waiting_on` decides which of the other three. Found by the
weekly check holds what the automated run turned up that nobody has picked up yet, so it drops
out of that section the moment someone is named. Stale claims is a separate axis - a note can
be both stuck and out of date, and you would want to know both.

> [!info] Not a task list
> Things you have to *do*, with due dates and ticks, live in Notion. This page answers a
> different question: what is stuck and on whom.

## With other people

Names are links - open one to see everything sitting with that person. Unsettled decisions
appear here too: a decision note with `status: open` and a `waiting_on` is the open question,
and becomes the permanent record once it is answered.

```dataview
TABLE WITHOUT ID
  link(file.link, file.name) AS "Item",
  waiting_on AS "With",
  blocked_on AS "Needs",
  (date(today) - date(since)).days AS "days"
FROM "Clients"
WHERE waiting_on
  AND !contains(string(waiting_on), "Tom Mitchell")
  AND !blocked_by
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
  AND !blocked_by
SORT since ASC
```

## Downstream

Built and ready, waiting on something else in the chain rather than on a person. These
free themselves - no action needed.

```dataview
TABLE WITHOUT ID
  link(file.link, file.name) AS "Item",
  blocked_by AS "Waiting for",
  choice(waiting_on, waiting_on, "-") AS "Then with",
  built AS "built"
FROM "Clients"
WHERE blocked_by
SORT built ASC
```

## Found by the weekly check

Problems the automated run turned up, with the date they were first seen rather than the
date they were last mentioned. Nothing here has a person against it yet - add a
`waiting_on` to an issue note and it moves up into the sections above.

```dataview
TABLE WITHOUT ID
  link(file.link, file.name) AS "Problem",
  check AS "Found by",
  (date(today) - date(since)).days AS "days"
FROM "Clients"
WHERE type = "issue" AND status = "open" AND automated AND !waiting_on
SORT since ASC
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
