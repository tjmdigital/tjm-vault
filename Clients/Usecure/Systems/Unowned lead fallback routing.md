---
type: system
client: Usecure
pattern: "[[Fallback routing for unowned records]]"
variant: "1 hour grace, rotate UK SDRs, copy owner to company"
enabled: false
built: 2026-08-21
blocked_by: "[[Stale lead ladder (Usecure)]]"
blocked_on: "goes live with the ladder"
since: 2026-08-21
verified: 2026-08-21
hardcodes: [Dominic, AJ]
---
# Unowned lead fallback routing

Agreed 11 August: personal-email sign-ups join the SDR rotation, unknown country goes to
a UK SDR.

Waits an hour so normal routing gets first go, then stamps the primary contact; a
contact-side workflow rotates Dominic / AJ in and copies that owner to the company.

**Triggers on "lead has no owner", not on email domain.** Of the two unowned leads on the
board, only one was a personal-email case - the other had a real company that itself had
no owner.

Built as a separate pair rather than editing the live master allocation workflow, so
nothing about current routing changes.

Workflows: [[1870368615 Unowned lead flag]], [[1870371119 Unowned lead fallback]]

Uses [[trigger_unowned_lead_routing]] to cross from lead to contact.
