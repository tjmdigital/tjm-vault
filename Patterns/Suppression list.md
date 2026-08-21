---
type: pattern
---
# Suppression list

## The problem

Marketing wants to send to a segment. Sales is already working some of those people.
Both are right, and nobody finds out until the prospect gets two approaches in a day.

## How it works

A single dynamic **suppression list** holding everyone sales considers theirs, referenced
as a `NOT_IN_LIST` filter by every send list. Because the API only allows `IN_LIST` at
association-branch level (see [[List API constraints]]), the exclusion has to live in a
separate list rather than inline.

Usual membership rules, OR'd:
- has an open lead being worked
- contacted in the last 30 days (rolling)
- currently enrolled in a sequence

## Why dynamic beats a one-off cut

It self-maintains. Someone drops out 30 days after their last contact, or when their
sequence ends, and rejoins the send list on their own. A static exclusion is out of date
the day after it is built.

## What it caught

At Usecure, 73 contacts on a re-engagement send had an open lead being worked, 34 of them
at Connected stage. Found before the send, not after.

## Implementations

```dataview
TABLE client, variant, enabled, verified
FROM "Clients"
WHERE contains(string(pattern), this.file.name)
```
