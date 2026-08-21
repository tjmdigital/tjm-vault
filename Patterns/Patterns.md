---
tags: [index]
---
# Patterns

Reusable mechanisms. Each note carries the **decision points** that come up every time a
client asks for it - that table is the thing worth having when someone says "can we do
lead closure" and you would otherwise start from a blank page.

```dataview
TABLE WITHOUT ID
  link(file.link, file.name) AS "Pattern",
  length(filter(file.inlinks, (l) => contains(string(l), "Systems"))) AS "builds"
FROM "Patterns"
WHERE file.name != "Patterns"
SORT file.name ASC
```

## Where each one is built

```dataview
TABLE WITHOUT ID
  pattern AS "Pattern",
  link(file.link, file.name) AS "Implementation",
  client,
  variant
FROM "Clients"
WHERE pattern
SORT pattern ASC
```
