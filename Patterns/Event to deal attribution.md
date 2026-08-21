---
type: pattern
---
# Event to deal attribution

## The problem

Marketing runs events and cannot show what they generated, because deals are not linked
to the events whose attendees they came from - and often are not linked to a contact at all.

## How it works

Two labels on the event-to-deal association:

- **Sourced** - the person attended *before* the deal existed. The event started it.
- **Influenced** - the deal was already in play when they attended.

Renewals are never Sourced, only Influenced. An event cannot have originated a customer
who already existed, but it can have helped keep them.

## Decision points

| Question | Usecure answer |
|---|---|
| Time cap on Sourced? | 12 months post-event |
| Renewals in scope? | Yes, separately labelled |
| Attendees only, or registrants too? | Deals: attendees. Net new tagging: everyone. |

## Prerequisites nobody expects

**Every deal needs a contact.** Without one there is no path from deal to event. Expect a
large backfill: at Usecure 306 of 396 new-business deals had no contact. 237 were
recoverable from the meetings, emails and calls already logged against them; the rest
needed a human who knew the deal.

## Watch for

- Currency - see [[Currency and code step limits]]
- Removing a *label* does not remove the *association*. Leftover unlabelled links keep
  showing in the deal panel looking like attribution.

## Implementations

```dataview
TABLE client, variant, enabled, verified
FROM "Clients"
WHERE contains(string(pattern), this.file.name)
```
