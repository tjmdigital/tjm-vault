---
type: platform
verified: 2026-08-21
cost: "the Albir near-miss"
---
# Rotate takes user IDs, set-property takes owner IDs

Two different numbering systems for the same person, and they are only sometimes equal.

| Action | Field | ID type |
|---|---|---|
| Rotate record owner (`0-11`) | `user_ids` | **HubSpot user ID** |
| Set property (`0-5`) on `hubspot_owner_id` | `staticValue` | **Owner ID** |

For users created recently the two happen to match (Dominic is 77935198 for both). For
older users they diverge - Johanna is user `26191480` but owner `102034069`.

**How this bites:** scanning workflows for a departing user's *owner* ID finds nothing,
because rotate pools store *user* IDs. You conclude they are not in any pool. They are.

Resolve user IDs with `GET /settings/v3/users`, owner IDs with `GET /crm/v3/owners`.
Match on email, never on the number.

See [[Deactivated users do not leave rotation pools]].
