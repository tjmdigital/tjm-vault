---
type: platform
verified: 2026-08-20
---
# Owner sync chain: company to contact to lead to deal

Ownership is not four independent fields. It is a chain, and only the first link is
really settable.

```
company owner
    v  (HubSpot native "OwnerChangeToContactUpdate" - overwrites, does not merge)
contact owner
    v  (native, property-promoter-worker - lead owner is calculated)
lead owner
```

Deals follow separately, via workflow rather than natively, where one is built.

**Consequences worth knowing:**

- Setting **lead owner** directly does not stick. It is recalculated from the primary
  contact's owner. To move a lead, move the company.
- The company-to-contact sync **overwrites a different existing owner**. Measured on
  60 recently created contacts: 9 had a company owner change stomp a different contact owner.
- Anything that writes contact owner directly - an integration, a booking tool - creates a
  split that survives only until the next company owner change.

Verified end to end in production: a manual company owner change at 12:18:39 produced a
deal owner change at 12:18:47. Eight seconds.
