---
type: platform
verified: 2026-08-19
cost: "one 400 and twenty minutes"
---
# Lead create date is `hs_createdate`

On the lead object (`0-136`) the create date property is **`hs_createdate`**, not `createdate`.

Searching `createdate` returns a **400**, not an empty result, so it fails loudly - but only
once you have already written the filter.

Contacts, companies and deals all use `createdate`. Leads are the exception.
