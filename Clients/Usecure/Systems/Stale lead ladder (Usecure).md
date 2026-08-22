---
type: system
client: Usecure
pattern: "[[Stale lead ladder]]"
variant: "2/3/14, single-person pools route to Molly, note counts as activity"
enabled: false
built: 2026-08-17
waiting_on: ["[[Tom Mitchell]]"]
blocked_on: "notification recipient to be set in the HubSpot UI, then agree a go-live date with the team"
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

- [ ] Set the notification recipient on the warning step in the HubSpot UI - cannot be done via API 📅 2026-08-22
- [ ] Announce a go-live date to the SDRs and AMs, then switch on 📅 2026-08-26

## Status

Confirmed by both. Molly on 21 August; Nihil the same evening - see
[[2026-08-21 Nihil confirms the reassignment rules]], which also raised **annual leave** as an
unhandled gap: rotation pools have no idea who is away, so a rep on holiday still receives
leads and at 2/3/14 those start warning within days.

## Albir guard

Enrolment excludes leads owned by Albir Gendi, so his 30 stale leads stay frozen while Molly
is away. See [[2026-08-20 Albir deactivation]].

> [!danger] Remove this guard once his records move
> It is a hardcoded owner ID in the enrolment filter. Left in place after his leads are
> reassigned, it silently exempts whoever inherits them.

Workflow: [[1868268934 Lead stale ladder]]

Built against [[Lead create date is hs_createdate]] - the lead object does not use `createdate`.
