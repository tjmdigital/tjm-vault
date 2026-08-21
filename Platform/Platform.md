---
tags: [index]
---
# Platform

Client-agnostic facts about the tools. Mostly things learned the hard way, written down so
the next hour is not spent rediscovering them.

**Check here before trial and error.**

```dataview
TABLE WITHOUT ID
  link(file.link, file.name) AS "Note",
  cost AS "What it cost to learn",
  verified
FROM "Platform"
WHERE file.name != "Platform"
SORT file.name ASC
```
