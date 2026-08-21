---
type: platform
verified: 2026-08-21
---
# Deactivating a user does not clean up after them

Deactivating a HubSpot user archives their **owner** record. It does not:

- remove them from rotate pools in workflows
- reassign the records they own
- stop `GET /settings/v3/users` still listing them as a user

Ownership routing that reads company owner will keep landing new work on them, because
the company still has their name on it. See [[Owner sync chain]].

**Offboarding checklist that actually works:**
1. Remove from every rotate pool (search by **user** ID, see [[Rotate actions take user IDs, set-property takes owner IDs]])
2. Reassign companies - contacts and leads follow automatically
3. Reassign open deals, or accept they move with the company
4. Check the external booking tool separately - it has its own router
5. Reassign upcoming meetings they are hosting

Step 5 is the urgent one and the one everybody forgets. A deactivated host still has
prospects turning up to their calendar.
