---
type: system
client: Usecure
pattern: "[[Event to deal attribution]]"
variant: "Sourced/Influenced, 12-month cap, renewals never Sourced, net new covers registrants"
enabled: true
built: 2026-08-12
verified: 2026-08-19
---
# Event attribution

Links deals and contacts back to the events that generated them, so marketing can show what
an event produced.

## Two labels

**Sourced** - the person attended before the deal existed. **Influenced** - the deal was
already in play. Renewals are never Sourced. Capped at 12 months post-event.

Current: 32 Sourced, 46 Influenced, 0 unlabelled.

## Net new contacts

Separately, every event-contact link is tagged **Net new** where the person had no CRM
record before the event brought them in - covering registrants as well as attendees, per
[[2026-08-17 Net new covers registrants]]. Webinars use the exact registration timestamp
from the marketing event. Currently [[Net new event contacts]].

## It maintains itself

No box to tick. [[1868265494 Event auto-run attribution]] watches the registration and
attendee rollups and triggers [[1865550884 Event attribution recompute]] on its own -
proven in production, firing 7 times as a webinar backfill landed.

New deals link themselves as soon as they get a contact, via
[[1865536645 Event attribution new deals]].

## Depends on

[[Missing-contact failsafe (Usecure)]] - a deal with no contact is invisible to all of this.

Verified by [[2026-08-19 Event attribution health check]].
