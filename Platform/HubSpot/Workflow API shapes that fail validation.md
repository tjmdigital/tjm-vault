---
type: platform
verified: 2026-08-21
---
# v4 workflow shapes that fail validation

The API returns `"Invalid request to flow creation"` with no detail, so these were all
found by bisecting.

**Object type decides the flow type.**
- Contacts (`0-1`) need `"type": "CONTACT_FLOW"`
- Everything else needs `"type": "PLATFORM_FLOW"`
- Sending `PLATFORM_FLOW` for `0-1` errors with the almost comic
  `Expected an object type other than "0-1" objectType but got "0-1"`

**`defaultBranch` with `edgeType: "GOTO"` fails.** Use `"STANDARD"`.

**Branch leaves cannot converge on a shared final action** via GOTO. Restructure so every
leaf terminates - if you need a shared cleanup step, do it *first*, before the branch.

**Always required:** `flowType: "WORKFLOW"`, `startActionId`, `nextAvailableActionId`
(must exceed every action ID used).

**Re-enrolment on every change**, not just empty-to-set, uses the `hs_name` trick:
```json
{"property": "hs_name", "operator": "IS_EQUAL_TO", "value": "<propertyName>"}
```
A plain `IS_KNOWN` trigger only fires on the transition from empty.
