---
type: pattern
---
# Two-stage trigger

## The problem

A workflow can only set properties on the enrolled object or its associations. So when
the *decision* belongs to one object and the *action* belongs to another - decide on a
lead, act on a company - one workflow cannot do it.

## How it works

1. Workflow A, on the deciding object, stamps a timestamp property on the acting object
   via its association.
2. Workflow B, on the acting object, enrols on that property being known, does the work,
   and **clears the property** so it can fire again.

```
[Lead workflow] --stamps trigger_x on company--> [Company workflow] --acts, clears trigger_x-->
```

## Decision points

- **Clear the trigger first or last?** Last is more correct but forces every branch leaf
  to converge, which the API rejects (see [[Workflow API shapes that fail validation]]).
  Clearing first is the practical answer; the cost is that a mid-flow failure loses the trigger.
- Re-enrolment needs the `hs_name` trick, or it only ever fires once per record.

## Where it has been used

Lead reassignment, multi-thread alerts, unowned lead fallback, deal owner following
company owner. It is the workaround for most cross-object automation in HubSpot.

## Implementations

```dataview
TABLE client, variant, enabled, verified
FROM "Clients"
WHERE contains(string(pattern), this.file.name)
```
