---
type: system
client: Usecure
pattern: "[[Two-stage trigger]]"
variant: "company-level move, open-deal guard, one handover then close"
enabled: false
built: 2026-08-21
blocked_on: "goes live with the ladder"
verified: 2026-08-21
hardcodes: [Dominic, AJ, Alex Campbell, Alex Legeay, Gerson, Molly]
---
# Lead reassignment

## Why it moves the company, not the lead

Lead owner is calculated from the primary contact's owner, so setting it directly does not
stick. See [[Owner sync chain]]. Moving the company keeps contact, lead and deal in step.

## Order of operations

1. **Open-deal guard first.** Company has any open deal, ownership goes to Molly to triage,
   no rotation. A live renewal must never change hands because an unrelated enquiry went quiet.
2. Otherwise hand to the other person in that territory pool.
3. Single-person pools, or an owner in no pool, go to Molly.

One move, never a loop - which answers Scott's "don't just keep moving it and moving it"
structurally rather than with a counter.

## The pairs

Dominic <-> AJ, Alex Campbell <-> Alex Legeay, Gerson -> Dominic.
Tor, Johanna, Aira Mae, Molly, Scott -> Molly.

> [!danger] These are hardcoded owner IDs
> This is exactly what broke when Albir left. When anyone joins or leaves, these pairs need
> updating or leads will be handed to a deactivated user.
> See [[Deactivated users do not leave rotation pools]].

Workflow: [[1870325562 Lead reassignment]]
