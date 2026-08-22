---
type: platform
verified: 2026-08-22
cost: "silently stripped 3 Registered labels before it was spotted"
---
# A v4 association PUT replaces the whole label set

`PUT /crm/v4/objects/{type}/{id}/associations/{type}/{id}` with a body of label objects
**replaces every label on that pair**. It does not add to them.

Adding `Attended` to three contacts who already held `Registered` removed `Registered`,
and the event's `total_registrations` rollup dropped from 162 to 159. Nothing errored.

**Always read the current labels first and PUT the union**, or anything already there -
including `Net new` - is lost.

## Two other things about these labels

**Category matters.** Custom labels are `USER_DEFINED`, not `HUBSPOT_DEFINED`. Sending the
wrong category returns a misleading 400 naming an unrelated object type - the event object
was reported as `TICKET=... is not valid`, which sends you looking in the wrong place entirely.

**Removing a label is not removing the association.** See [[Event to deal attribution]] -
25 links kept showing in event panels with no label after a cap change removed only the label.

Confirmed working association labels between an event (`0-162`) and a contact:

| Label | typeId | Category |
|---|---|---|
| Registered | 14 | USER_DEFINED |
| Attended | 16 | USER_DEFINED |
| 🆕 Net new | 23 | USER_DEFINED |

Used by `scripts/checks.py --fix`.
