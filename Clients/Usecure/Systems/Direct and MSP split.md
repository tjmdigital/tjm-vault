---
type: system
client: Usecure
pattern: "[[One definition per metric]]"
variant: "self-declared on the form, stamped onto the lead, blank means the form did not ask"
enabled: true
built: 2026-08-16
verified: 2026-08-21
---
# Direct and MSP split

Whether an enquiry is a direct prospect or an MSP, taken from what they tell us on the form
rather than inferred from the account. Lives on the lead as `declared_business_model`, so it
can be reported on directly.

Backfilled across 12,512 leads when built.

**Blank means the form did not ask** - not "unknown". That distinction matters, because a
blank rate is a form coverage problem, not a data quality one. It ran at 11% until Scott
added the question to the remaining forms on 19 August; now 4%.

> [!info] Not the same as MSP Partner Status
> `msp_partner_status` on the company says whether a partner is paying. This says what the
> person claimed at the point of enquiry. Both are useful, for different questions.

Workflow: [[1868140208 Stamp declared business model]]
