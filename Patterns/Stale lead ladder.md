---
type: pattern
---
# Stale lead ladder

## The problem

Leads only ever leave the board by qualifying, so "open" stops meaning anything. At
Usecure, 2 of 207 leads had ever been closed - the board was a graveyard being read as
a pipeline.

## How it works

A ladder with three rungs, and instant escape at every rung:

1. **Warn** - no activity and nothing booked for N days, tell the owner
2. **Reassign** - still nothing after M more days, move it to someone else
3. **Close** - still nothing after P more days, close with a reason

Any logged activity, email, **note**, or booked meeting un-enrols the record instantly.
Anyone actually working their leads never sees any of it.

## Decision points

Every client argues about these, so ask early:

| Question | Usecure answer |
|---|---|
| Timings? | 2 / 3 / 14 |
| Reassign to whom? | Other person in the territory pool |
| Pool of one? | Goes to the manager, not a loop and not a close |
| Does a note count as working it? | Yes - a deliberate "leave this alone" is a decision |
| Close reason? | Distinct from real disqualification, reportable by owner |
| Existing backlog? | Close in one pass first, or day one is a notification storm |

## What always comes up

- **The backlog must be handled separately from the rule.** Switching on with 700 stale
  leads means 700 notifications at once. Close them as a line in the sand, keep the list
  for re-engagement. See [[Backlog close]].
- **Reassignment moves more than the lead.** Because of the [[Owner sync chain]],
  rotating a lead moves company ownership and drags open deals with it. Needs a guard.
- **Never-touched and gone-quiet are different cases.** A lead nobody ever opened does not
  deserve the same warning as one someone worked and then dropped.

## Implementations

```dataview
TABLE client, variant, enabled, verified
FROM "Clients"
WHERE contains(string(pattern), this.file.name)
```
