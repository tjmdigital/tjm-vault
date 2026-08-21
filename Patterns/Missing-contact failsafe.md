---
type: pattern
---
# Missing-contact failsafe

## The problem

Deals created by hand from the deals list or a company record have no contact attached,
which breaks every attribution path downstream. HubSpot cannot make contact association
required for one pipeline only - it applies to all of them, which breaks partner pipelines
where the deal genuinely belongs to the company.

## How it works

Three layers, because education alone does not hold:

1. **Guidance** - create new-business deals from the contact record, and the contact attaches itself
2. **Failsafe** - any new-business deal still missing a contact an hour after creation notifies its owner
3. **Backfill** - a queued list of the historic ones for human review, worked down over time

## Watch for

- The failsafe usually covers one pipeline. Renewals quietly accumulate the same problem.
- Review lists must be pruned as deals get fixed, or the count looks static and the team
  looks idle when they are not.

## Implementations

```dataview
TABLE client, variant, enabled, verified
FROM "Clients"
WHERE contains(string(pattern), this.file.name)
```
