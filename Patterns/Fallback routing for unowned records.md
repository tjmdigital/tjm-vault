---
type: pattern
---
# Fallback routing for unowned records

## The problem

Territory routing works off the company. A personal-email sign-up has no company, so
nothing assigns it and it sits unowned forever. Any automation that notifies "the owner"
silently does nothing for these.

## How it works

A [[Two-stage trigger]]: wait an hour so normal routing gets first go, then if the record
still has no owner, rotate one in from a named fallback pool and copy that owner to the
company if there is one.

## Trigger on the symptom, not the cause

Filter on **"lead has no owner"**, not on "email is a free provider". At Usecure, of two
unowned leads only one was a personal-email case - the other had a perfectly good company
that itself had no owner. Same symptom, different cause, one fix.

## Decision points

- Who is the fallback pool? Usecure: UK SDRs, per "unknown country goes to a UK SDR"
- Or close them off as not worth working? Worth asking - the answer is usually no,
  because free-trial and demo requests arrive on personal addresses too

## Implementations

```dataview
TABLE client, variant, enabled, verified
FROM "Clients"
WHERE contains(string(pattern), this.file.name)
```
