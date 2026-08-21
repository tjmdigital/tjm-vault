---
type: system
client: Usecure
pattern: "[[Missing-contact failsafe]]"
variant: "new business only, 1 hour delay, owner notified, review lists for the tail"
enabled: true
built: 2026-08-08
verified: 2026-08-19
---
# Missing-contact failsafe (Usecure)

Deals created by hand often have no contact, which breaks every attribution path
downstream - see [[Event to deal attribution]].

Three layers: create deals from the contact record; any new-business deal still missing a
contact an hour later notifies its owner; the historic tail sits in review lists.

## Coverage as at 19 August

| | Started | Fixed | Left |
|---|---|---|---|
| New business (list 3813) | 68 | 42 | 26 |
| Renewals (list 3814) | 50 | 34 | 16 |

4 new-business deals since launch have been caught and are still unfixed.

> [!warning] Renewals are not covered by the failsafe
> Only new business triggers the notification, so renewals quietly accumulate the same
> problem. 9 new contactless renewals appeared between 12 and 19 August.

Workflow: [[1863156311 Missing contact notify owner]]

Verified by [[2026-08-19 Event attribution health check]] and [[2026-08-21 Inbound flow check]].
