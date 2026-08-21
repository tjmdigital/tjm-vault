---
type: check
client: Usecure
date: 2026-08-21
outcome: "two reports wrong, both need UI edits"
---
# Dashboard audit

## Ties out

Conversions, leads, qualified, and the open-lead status split all match the API exactly
(28 / 119 / 84 / 1 = 232).

## Wrong

**"Picked up & worked" tile** reads 151, which is "reached Attempting or Connected". Its own
description says "or Qualified", which is 233. The dashboard and the status page were
publishing 52% and 81% for the same population. See [[Picked up and worked]].

**"Lead funnel - current year"** excludes One-off cleanup, which now removes 2,423 of this
year's 2,837 leads including 1,532 that reached Attempting. The rates shown are computed on
414 survivors and flatter the process. Should be re-cohorted to 21 July onwards with the
exclusion dropped.

Verifies [[Picked up and worked]] and [[Any movement out of New]].

## Still to fix

- [ ] Repoint the "Picked up & worked" tile to A/C/Q - target 233 📅 2026-08-22
- [ ] Re-cohort the lead funnel to 21 July and drop the cleanup exclusion 📅 2026-08-22

## Cannot be fixed from here

HubSpot has **no public API for editing report filters** - the dashboard endpoints 404 or
reject private app tokens. Reports are UI-only. Everything else in this vault was changed
via API; reports are the exception.
