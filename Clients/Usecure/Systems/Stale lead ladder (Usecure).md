---
type: system
client: Usecure
pattern: "[[Stale lead ladder]]"
variant: "2/3/14, single-person pools route to Molly, note counts as activity"
enabled: false
built: 2026-08-17
waiting_on: ["[[Nihil Morjaria]]", "[[Tom Mitchell]]"]
blocked_on: "Nihil to confirm the open-deal guard; notification recipient still to be set in the HubSpot UI"
since: 2026-08-21
verified: 2026-08-21
hardcodes: [Albir]
---
# Stale lead ladder (Usecure)

## As built

| Rung | Trigger | Action |
|---|---|---|
| Day 2 | no activity, nothing booked | warn the owner |
| Day 3 | still nothing | hand to [[Lead reassignment]] |
| Day 14 | still nothing | close as No engagement |

Any logged activity, email, note or booked meeting un-enrols instantly
(`unEnrollObjectsNotMeetingCriteria: true`).

Guarded so a lead must be **more than 2 days old** to enrol - without that, a lead created
an hour ago has an empty last-activity date and gets warned on day one.
See [[2026-08-19 Backlog close]] for the same bug caught live.

## Before it can go live

- [ ] Notification recipient set in the UI - cannot be done via API, and the step fires
      into nothing until it is. See [[Notification recipients cannot be set via API]].
- [ ] Molly's answer on [[2026-08-20 Albir deactivation]]

Workflow: [[1868268934 Lead stale ladder]]

Built against [[Lead create date is hs_createdate]] - the lead object does not use `createdate`.
