---
type: workflow
client: Usecure
hubspot_id: 1808815387
object: "0-3 deal"
enabled: true
built: 
verified: 2026-08-21
depends_on: []
hardcodes: []
---
# 1808815387 Update open deal owners 2 of 2

Reads the trigger, and if the deal is open sets its owner from the primary company.
Skipped where `lock_deal_owner` is true - only 5 deals in the portal have it.

This is the workflow that moves a live deal when an unrelated account change happens.
